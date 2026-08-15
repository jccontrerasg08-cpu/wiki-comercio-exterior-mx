import unittest
from datetime import date

from scripts.source_health import (
    ProbePolicy,
    classify_response,
    probe_source,
    select_due_sources,
    select_sources,
)


SOURCE = {
    "id": "dof",
    "url": "https://sidof.segob.gob.mx/notas/1",
    "allowed_hosts": ["sidof.segob.gob.mx"],
    "media_types": ["text/html"],
    "probe": {
        "expected_status": [200],
        "min_bytes": 20,
        "reject_if_contains": ["not found"],
    },
}


class Response:
    status_code = 200
    headers = {"content-type": "text/html; charset=utf-8"}
    url = "https://sidof.segob.gob.mx/notas/1"
    history = []

    def iter_content(self, chunk_size):
        yield b"RGCE publication identity 1" * 4

    def close(self):
        pass


class RedirectResponse(Response):
    status_code = 302
    headers = {"location": "https://169.254.169.254/latest/meta-data"}


class RecordingRedirectTransport:
    def __init__(self):
        self.urls = []

    def get(self, url, **kwargs):
        self.urls.append(url)
        return RedirectResponse()


class OversizedTransport:
    def get(self, url, **kwargs):
        class Oversized(Response):
            def iter_content(self, chunk_size):
                yield b"x" * 101

        return Oversized()


class SourceHealthTests(unittest.TestCase):
    def test_http_200_soft_404_is_suspicious(self):
        body = b"The requested legal publication was not found"
        result = classify_response(SOURCE, Response(), body)
        self.assertEqual(result.classification, "suspicious_response")

    def test_oversized_response_stops_without_hashing(self):
        result = probe_source(
            SOURCE, OversizedTransport(), ProbePolicy(max_bytes=100)
        )
        self.assertEqual(result.classification, "size_limit")
        self.assertIsNone(result.sha256)

    def test_explicit_smoke_source_can_be_catalog_only(self):
        sources = [
            {"id": "harvested", "harvest": True},
            {"id": "catalog", "harvest": False},
        ]
        self.assertEqual(
            [item["id"] for item in select_sources(sources, ["catalog"])],
            ["catalog"],
        )

    def test_rejected_redirect_target_is_never_requested(self):
        transport = RecordingRedirectTransport()
        result = probe_source(SOURCE, transport)
        self.assertEqual(result.classification, "redirect_host_rejected")
        self.assertEqual(transport.urls, [SOURCE["url"]])

    def test_unknown_explicit_source_is_an_error(self):
        with self.assertRaisesRegex(ValueError, "unknown source id"):
            select_sources([{"id": "known", "harvest": True}], ["typo"])

    def test_due_selection_uses_cadence_and_last_success(self):
        sources = [
            {"id": "weekly", "harvest": True, "cadence_days": 7},
            {"id": "failed", "harvest": True, "cadence_days": 30},
        ]
        observations = {
            "weekly": {"observed_at": "2026-08-10", "classification": "healthy_transport"},
            "failed": {"observed_at": "2026-08-14", "classification": "unreachable"},
        }
        selected = select_due_sources(sources, observations, date(2026, 8, 15))
        self.assertEqual([item["id"] for item in selected], ["failed"])

    def test_identity_mismatch_rejects_unrelated_200_page(self):
        source = {**SOURCE, "note_id": "999"}
        result = classify_response(source, Response(), b"unrelated but sufficiently large response")
        self.assertEqual(result.classification, "identity_mismatch")

    def test_default_identity_requires_exact_registered_path(self):
        class WrongPage(Response):
            url = "https://sidof.segob.gob.mx/notas/unrelated"

        result = classify_response(SOURCE, WrongPage(), b"x" * 50)
        self.assertEqual(result.classification, "identity_mismatch")

    def test_due_selection_rotates_past_recent_failures(self):
        sources = [
            {"id": f"source_{index:02d}", "harvest": True, "cadence_days": 1}
            for index in range(21)
        ]
        observations = {
            item["id"]: {"observed_at": "2026-08-01", "classification": "unreachable"}
            for item in sources
        }
        first = select_due_sources(sources, observations, date(2026, 8, 15))[:20]
        for item in first:
            observations[item["id"]]["observed_at"] = "2026-08-15"
        second = select_due_sources(sources, observations, date(2026, 8, 16))[:20]
        self.assertIn("source_20", [item["id"] for item in second])


if __name__ == "__main__":
    unittest.main()
