from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import tempfile
import unittest

from scripts.schema_validation import load_local_schema, validate_instance
from scripts.snice_discovery import (
    DiscoveryPolicy,
    build_payloads,
    fetch_index_html,
    write_payloads,
)


ROOT = Path(__file__).resolve().parents[1]
INDEX_URL = "https://www.snice.gob.mx/~oracle/SNICE_DOCS/"
DISCOVERED_AT = datetime(2026, 8, 15, 19, 0, tzinfo=timezone.utc)
INDEX_HTML = """
<html><body><pre>
<a href="IMMEX_MAYO2026-DIRECTORIO_20260622-20260622.xlsx">IMMEX_MAYO2026-DIRECTORIO_20260622-20260622.xlsx</a> 22-Jun-2026 17:34 848K
<a href="IMMEX_MAYO-2026-DIRECTORIO_20260622-20260622.xlsx">IMMEX_MAYO-2026-DIRECTORIO_20260622-20260622.xlsx</a> 22-Jun-2026 18:04 1.7M
<a href="PROSEC_MAYO2026-DIRECTORIO_20260622-20260622.xlsx">PROSEC_MAYO2026-DIRECTORIO_20260622-20260622.xlsx</a> 22-Jun-2026 17:35 629K
<a href="SIDERURGICO_DIC_2016-AVISO-AUTOMATICO-IMPORTACION_20201209-20201209.xlsx">SIDERURGICO_DIC_2016-AVISO-AUTOMATICO-IMPORTACION_20201209-20201209.xlsx</a> 09-Dec-2020 12:03 3.8M
</pre></body></html>
"""


class FakeResponse:
    def __init__(
        self,
        body: bytes,
        *,
        status_code: int = 200,
        url: str = INDEX_URL,
        content_type: str = "text/html; charset=UTF-8",
        content_length: int | None = None,
    ) -> None:
        self.body = body
        self.status_code = status_code
        self.url = url
        self.headers = {"content-type": content_type}
        if content_length is not None:
            self.headers["content-length"] = str(content_length)

    def iter_content(self, chunk_size: int):
        for offset in range(0, len(self.body), chunk_size):
            yield self.body[offset : offset + chunk_size]

    def close(self) -> None:
        return None


class FakeTransport:
    def __init__(self, response: FakeResponse) -> None:
        self.response = response
        self.calls: list[tuple[str, dict[str, object]]] = []

    def get(self, url: str, **kwargs):
        self.calls.append((url, kwargs))
        return self.response


class SniceDiscoveryTransportTests(unittest.TestCase):
    def test_rejects_non_https_or_non_snice_host_before_fetch(self) -> None:
        transport = FakeTransport(FakeResponse(INDEX_HTML.encode()))

        with self.assertRaises(ValueError):
            fetch_index_html(transport, "http://www.snice.gob.mx/~oracle/SNICE_DOCS/")
        with self.assertRaises(ValueError):
            fetch_index_html(transport, "https://example.com/~oracle/SNICE_DOCS/")

        self.assertEqual(transport.calls, [])

    def test_fetch_is_bounded_and_requires_html_identity(self) -> None:
        transport = FakeTransport(FakeResponse(INDEX_HTML.encode()))

        result = fetch_index_html(transport, INDEX_URL)

        self.assertIn("IMMEX_MAYO2026", result)
        self.assertEqual(len(transport.calls), 1)
        _, kwargs = transport.calls[0]
        self.assertFalse(kwargs["allow_redirects"])
        self.assertTrue(kwargs["stream"])
        self.assertGreater(kwargs["timeout"], 0)

    def test_declared_oversize_is_rejected_without_streaming(self) -> None:
        policy = DiscoveryPolicy(max_bytes=100)
        response = FakeResponse(
            b"not read",
            content_length=101,
        )
        transport = FakeTransport(response)

        with self.assertRaises(ValueError):
            fetch_index_html(transport, INDEX_URL, policy=policy)


class SnicePayloadTests(unittest.TestCase):
    def test_payloads_separate_documents_series_findings_and_changes(self) -> None:
        payloads = build_payloads(
            INDEX_HTML,
            source_url=INDEX_URL,
            discovered_at=DISCOVERED_AT,
        )

        self.assertEqual(set(payloads), {"documents", "series", "findings", "changes"})
        self.assertEqual(payloads["documents"]["schema_version"], "1.0")
        self.assertEqual(len(payloads["documents"]["documents"]), 4)
        self.assertEqual(len(payloads["series"]["series"]), 3)
        immex = next(
            item
            for item in payloads["series"]["series"]
            if item["logical_dataset_id"] == "immex:directorio:2026-05"
        )
        self.assertEqual([doc["version"] for doc in immex["documents"]], [1, 2])
        siderurgico = next(
            item
            for item in payloads["documents"]["documents"]
            if item["family"] == "SIDERURGICO"
        )
        self.assertTrue(siderurgico["is_backfill"])
        self.assertEqual(payloads["changes"]["changes"], [])

    def test_payloads_validate_against_local_schemas(self) -> None:
        payloads = build_payloads(
            INDEX_HTML,
            source_url=INDEX_URL,
            discovered_at=DISCOVERED_AT,
        )
        schema_names = {
            "documents": "snice-document.schema.json",
            "series": "snice-series.schema.json",
            "findings": "snice-finding.schema.json",
            "changes": "snice-change.schema.json",
        }

        for key, schema_name in schema_names.items():
            with self.subTest(payload=key):
                schema = load_local_schema(ROOT, schema_name)
                self.assertEqual(validate_instance(payloads[key], schema, key), [])

    def test_outputs_are_deterministic_for_fixed_discovery_time(self) -> None:
        payloads = build_payloads(
            INDEX_HTML,
            source_url=INDEX_URL,
            discovered_at=DISCOVERED_AT,
        )
        with tempfile.TemporaryDirectory() as first_dir, tempfile.TemporaryDirectory() as second_dir:
            first = write_payloads(payloads, Path(first_dir))
            second = write_payloads(payloads, Path(second_dir))

            self.assertEqual(set(first), {"documents", "series", "findings", "changes"})
            for key in first:
                self.assertEqual(first[key].read_bytes(), second[key].read_bytes())
                parsed = json.loads(first[key].read_text(encoding="utf-8"))
                self.assertEqual(parsed["generated_at"], "2026-08-15T19:00:00Z")


if __name__ == "__main__":
    unittest.main()
