"""Bounded discovery and deterministic export for the SNICE document collection."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Mapping
from urllib.parse import urlparse

from scripts.snice_intelligence import (
    SniceDocument,
    SniceSeries,
    build_series,
    detect_missing_companions,
    detect_size_anomaly,
    parse_index_snapshot,
)


SNICE_INDEX_URL = "https://www.snice.gob.mx/~oracle/SNICE_DOCS/"
SCHEMA_VERSION = "1.0"
STATE_VERSION = "1.0"
OUTPUT_NAMES = {
    "documents": "documents.json",
    "series": "series.json",
    "findings": "findings.json",
    "changes": "changes.json",
}
_DATE_PAIR = re.compile(r"_\d{8}-\d{8}", re.IGNORECASE)
_STATE_METADATA_FIELDS = ("bytes", "last_modified", "source_url")


@dataclass(frozen=True, slots=True)
class DiscoveryPolicy:
    timeout_s: float = 20.0
    max_bytes: int = 16 * 1024 * 1024
    chunk_size: int = 65_536
    allowed_hosts: tuple[str, ...] = ("www.snice.gob.mx", "snice.gob.mx")

    def __post_init__(self) -> None:
        if self.timeout_s <= 0:
            raise ValueError("timeout_s must be positive")
        if self.max_bytes <= 0:
            raise ValueError("max_bytes must be positive")
        if self.chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        if not self.allowed_hosts:
            raise ValueError("allowed_hosts must not be empty")


def _validate_collection_url(url: str, policy: DiscoveryPolicy) -> None:
    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise ValueError("SNICE discovery requires HTTPS")
    if parsed.username or parsed.password:
        raise ValueError("SNICE discovery URL must not contain credentials")
    if (parsed.hostname or "").casefold() not in {
        host.casefold() for host in policy.allowed_hosts
    }:
        raise ValueError(f"SNICE discovery host is not allowed: {parsed.hostname}")
    if parsed.port not in {None, 443}:
        raise ValueError("SNICE discovery URL must use the default HTTPS port")
    if not parsed.path.startswith("/~oracle/SNICE_DOCS/"):
        raise ValueError("URL is outside the registered SNICE_DOCS collection")


def fetch_index_html(
    transport: Any,
    url: str = SNICE_INDEX_URL,
    *,
    policy: DiscoveryPolicy | None = None,
) -> str:
    """Fetch the Apache-style collection index with strict host and size bounds."""

    selected = policy or DiscoveryPolicy()
    _validate_collection_url(url, selected)
    response = transport.get(
        url,
        timeout=selected.timeout_s,
        stream=True,
        allow_redirects=False,
        headers={
            "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.1",
            "User-Agent": "wiki-comercio-exterior-mx/1.0 (+GitHub Actions)",
        },
    )
    try:
        status = int(response.status_code)
        if status != 200:
            raise ValueError(f"SNICE index returned HTTP {status}")
        final_url = str(getattr(response, "url", url))
        _validate_collection_url(final_url, selected)
        if final_url.rstrip("/") != url.rstrip("/"):
            raise ValueError(f"unexpected SNICE index response URL: {final_url}")

        headers = {
            str(key).casefold(): str(value)
            for key, value in getattr(response, "headers", {}).items()
        }
        content_type = headers.get("content-type", "").casefold()
        if "text/html" not in content_type and "application/xhtml+xml" not in content_type:
            raise ValueError(f"SNICE index returned unexpected media type: {content_type!r}")
        declared = headers.get("content-length")
        if declared:
            try:
                declared_bytes = int(declared)
            except ValueError as exc:
                raise ValueError("SNICE index returned invalid Content-Length") from exc
            if declared_bytes > selected.max_bytes:
                raise ValueError(
                    f"SNICE index exceeds max_bytes ({declared_bytes} > {selected.max_bytes})"
                )

        chunks: list[bytes] = []
        total = 0
        for chunk in response.iter_content(chunk_size=selected.chunk_size):
            if not chunk:
                continue
            total += len(chunk)
            if total > selected.max_bytes:
                raise ValueError(
                    f"SNICE index exceeded max_bytes while streaming ({total} > {selected.max_bytes})"
                )
            chunks.append(bytes(chunk))
        body = b"".join(chunks)
        if not body:
            raise ValueError("SNICE index returned an empty body")
        try:
            text = body.decode("utf-8")
        except UnicodeDecodeError:
            text = body.decode("latin-1")
        if "<a" not in text.casefold() or not _DATE_PAIR.search(text):
            raise ValueError("SNICE index does not expose expected document-link markers")
        return text
    finally:
        response.close()


def _utc_iso(value: datetime) -> str:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("generated/discovered timestamps must be timezone-aware")
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def _local_iso(value: datetime) -> str:
    return value.replace(microsecond=0).isoformat()


def _index_sha256(index_html: str) -> str:
    return hashlib.sha256(index_html.encode("utf-8")).hexdigest()


def _document_id(document: SniceDocument) -> str:
    digest = hashlib.sha256(document.source_url.encode("utf-8")).hexdigest()
    return f"snice-url-{digest}"


def _document_record(
    document: SniceDocument,
    *,
    family_sizes: Mapping[str, list[int]],
) -> dict[str, object]:
    size_anomaly = detect_size_anomaly(
        document.bytes,
        list(family_sizes.get(document.family, [])),
    )
    anomalies: list[str] = []
    if document.bytes == 0:
        anomalies.append("zero_bytes")
    if size_anomaly:
        anomalies.append("size_outlier")
    return {
        "document_id": _document_id(document),
        "logical_dataset_id": document.logical_dataset_id,
        "filename": document.filename,
        "normalized_name": document.normalized_name,
        "family": document.family,
        "category": document.category,
        "period_year": document.period_year,
        "period_month": document.period_month,
        "filename_date": document.filename_date.isoformat(),
        "source_date": document.source_date.isoformat(),
        "last_modified": _local_iso(document.last_modified),
        "last_modified_timezone_known": bool(
            document.last_modified.tzinfo is not None
            and document.last_modified.utcoffset() is not None
        ),
        "discovered_at": _utc_iso(document.discovered_at),
        "extension": document.extension,
        "bytes": document.bytes,
        "sha256": document.sha256,
        "version": document.version,
        "is_replacement": document.is_replacement,
        "is_backfill": document.is_backfill,
        "is_anomaly": bool(anomalies),
        "anomalies": anomalies,
        "source_url": document.source_url,
    }


def _series_record(series: SniceSeries) -> dict[str, object]:
    return {
        "logical_dataset_id": series.logical_dataset_id,
        "family": series.family,
        "category": series.category,
        "period_year": series.period_year,
        "period_month": series.period_month,
        "documents": [
            {
                "document_id": _document_id(document),
                "filename": document.filename,
                "source_url": document.source_url,
                "last_modified": _local_iso(document.last_modified),
                "bytes": document.bytes,
                "sha256": document.sha256,
                "version": document.version,
                "is_replacement": document.is_replacement,
                "is_backfill": document.is_backfill,
            }
            for document in series.documents
        ],
    }


def _finding_records(
    documents: list[SniceDocument],
    *,
    family_sizes: Mapping[str, list[int]],
) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    for document in sorted(documents, key=lambda item: (item.family, item.filename)):
        if document.bytes == 0:
            findings.append(
                {
                    "finding_type": "zero_bytes",
                    "severity": "warning",
                    "family": document.family,
                    "logical_dataset_id": document.logical_dataset_id,
                    "filename": document.filename,
                    "message": "Index reports a zero-byte document; do not treat it as usable evidence.",
                }
            )
        if detect_size_anomaly(document.bytes, list(family_sizes.get(document.family, []))):
            findings.append(
                {
                    "finding_type": "size_outlier",
                    "severity": "info",
                    "family": document.family,
                    "logical_dataset_id": document.logical_dataset_id,
                    "filename": document.filename,
                    "message": "Document size is a robust outlier within the discovered family sample.",
                }
            )
    for item in detect_missing_companions(documents):
        findings.append(
            {
                "finding_type": "missing_companion",
                "severity": "info",
                "family": item["family"],
                "missing_family": item["missing_family"],
                "period_year": item["period_year"],
                "period_month": item["period_month"],
                "message": (
                    f"{item['family']} has a discovered period without expected companion "
                    f"{item['missing_family']}; this is a review signal, not a legal-status decision."
                ),
            }
        )
    return sorted(
        findings,
        key=lambda item: (
            str(item.get("finding_type", "")),
            str(item.get("family", "")),
            int(item.get("period_year") or 0),
            int(item.get("period_month") or 0),
            str(item.get("filename", "")),
            str(item.get("missing_family", "")),
        ),
    )


def _state_document(record: Mapping[str, object]) -> dict[str, object]:
    return {
        "document_id": record["document_id"],
        "logical_dataset_id": record["logical_dataset_id"],
        "family": record["family"],
        "filename": record["filename"],
        "source_url": record["source_url"],
        "last_modified": record["last_modified"],
        "bytes": record["bytes"],
    }


def build_state(payloads: Mapping[str, Mapping[str, object]]) -> dict[str, object]:
    """Reduce output payloads to the minimal state needed for the next comparison."""

    documents_payload = payloads.get("documents")
    if not isinstance(documents_payload, Mapping):
        raise ValueError("documents payload is required to build state")
    documents_value = documents_payload.get("documents")
    if not isinstance(documents_value, list):
        raise ValueError("documents payload must contain a document list")
    state_documents = [
        _state_document(record)
        for record in documents_value
        if isinstance(record, Mapping)
    ]
    state_documents.sort(key=lambda item: str(item["document_id"]))
    return {
        "state_version": STATE_VERSION,
        "source_url": documents_payload["source_url"],
        "generated_at": documents_payload["generated_at"],
        "index_sha256": documents_payload["index_sha256"],
        "documents": state_documents,
    }


def _metadata(record: Mapping[str, object]) -> dict[str, object]:
    return {field: record.get(field) for field in _STATE_METADATA_FIELDS}


def _collection_changes(
    previous_state: Mapping[str, object] | None,
    current_state: Mapping[str, object],
    *,
    detected_at: str,
) -> list[dict[str, object]]:
    if previous_state is None:
        return []
    previous_documents = previous_state.get("documents")
    current_documents = current_state.get("documents")
    if not isinstance(previous_documents, list) or not isinstance(current_documents, list):
        raise ValueError("SNICE state documents must be lists")

    old = {
        str(item["document_id"]): item
        for item in previous_documents
        if isinstance(item, Mapping) and "document_id" in item
    }
    new = {
        str(item["document_id"]): item
        for item in current_documents
        if isinstance(item, Mapping) and "document_id" in item
    }

    changes: list[dict[str, object]] = []
    for document_id in sorted(new.keys() - old.keys()):
        current = new[document_id]
        changes.append(
            {
                "change_type": "document_added",
                "document_id": document_id,
                "family": current["family"],
                "logical_dataset_id": current["logical_dataset_id"],
                "filename": current["filename"],
                "detected_at": detected_at,
                "previous": None,
                "current": _metadata(current),
            }
        )
    for document_id in sorted(old.keys() - new.keys()):
        previous = old[document_id]
        changes.append(
            {
                "change_type": "document_removed",
                "document_id": document_id,
                "family": previous["family"],
                "logical_dataset_id": previous["logical_dataset_id"],
                "filename": previous["filename"],
                "detected_at": detected_at,
                "previous": _metadata(previous),
                "current": None,
            }
        )
    for document_id in sorted(old.keys() & new.keys()):
        previous = old[document_id]
        current = new[document_id]
        if _metadata(previous) == _metadata(current):
            continue
        changes.append(
            {
                "change_type": "document_metadata_changed",
                "document_id": document_id,
                "family": current["family"],
                "logical_dataset_id": current["logical_dataset_id"],
                "filename": current["filename"],
                "detected_at": detected_at,
                "previous": _metadata(previous),
                "current": _metadata(current),
            }
        )
    return changes


def build_payloads(
    index_html: str,
    *,
    source_url: str = SNICE_INDEX_URL,
    discovered_at: datetime,
    previous_state: Mapping[str, object] | None = None,
) -> dict[str, dict[str, object]]:
    """Build physical, logical and observation payloads from one index snapshot."""

    if discovered_at.tzinfo is None or discovered_at.utcoffset() is None:
        raise ValueError("discovered_at must be timezone-aware")
    parsed = parse_index_snapshot(
        index_html,
        base_url=source_url,
        discovered_at=discovered_at,
    )
    physical = list(parsed.documents)
    logical = build_series(physical)
    versioned = [document for series in logical for document in series.documents]
    versioned.sort(key=lambda item: (item.last_modified, item.filename))
    family_sizes: dict[str, list[int]] = {}
    for document in versioned:
        family_sizes.setdefault(document.family, []).append(document.bytes)
    generated_at = _utc_iso(discovered_at)
    index_sha256 = _index_sha256(index_html)
    unparsed_entries = [
        {
            "filename": item.filename,
            "source_url": item.source_url,
            "last_modified": _local_iso(item.last_modified),
            "bytes": item.bytes,
            "reason": item.reason,
        }
        for item in parsed.unparsed_entries
    ]

    documents_payload: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "source_url": source_url,
        "generated_at": generated_at,
        "index_sha256": index_sha256,
        "index_entry_count": parsed.index_entry_count,
        "document_count": len(versioned),
        "unparsed_count": len(unparsed_entries),
        "unparsed_entries": unparsed_entries,
        "documents": [
            _document_record(document, family_sizes=family_sizes)
            for document in versioned
        ],
    }
    series_payload: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "source_url": source_url,
        "generated_at": generated_at,
        "index_sha256": index_sha256,
        "series_count": len(logical),
        "series": [_series_record(item) for item in logical],
    }
    findings = _finding_records(versioned, family_sizes=family_sizes)
    findings_payload: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "source_url": source_url,
        "generated_at": generated_at,
        "index_sha256": index_sha256,
        "finding_count": len(findings),
        "findings": findings,
    }

    provisional: dict[str, dict[str, object]] = {
        "documents": documents_payload,
        "series": series_payload,
        "findings": findings_payload,
        "changes": {},
    }
    current_state = build_state(provisional)
    changes = _collection_changes(
        previous_state,
        current_state,
        detected_at=generated_at,
    )
    changes_payload: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "source_url": source_url,
        "generated_at": generated_at,
        "previous_index_sha256": (
            previous_state.get("index_sha256")
            if isinstance(previous_state, Mapping)
            else None
        ),
        "current_index_sha256": index_sha256,
        "change_count": len(changes),
        "changes": changes,
    }
    provisional["changes"] = changes_payload
    return provisional


def write_payloads(
    payloads: Mapping[str, Mapping[str, object]],
    output_dir: Path,
) -> dict[str, Path]:
    """Write canonical UTF-8 JSON files with stable ordering and trailing newline."""

    output_dir.mkdir(parents=True, exist_ok=True)
    written: dict[str, Path] = {}
    if set(payloads) != set(OUTPUT_NAMES):
        raise ValueError(f"unexpected payload keys: {sorted(payloads)}")
    for key in sorted(OUTPUT_NAMES):
        path = output_dir / OUTPUT_NAMES[key]
        rendered = json.dumps(
            payloads[key],
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ) + "\n"
        path.write_text(rendered, encoding="utf-8", newline="\n")
        written[key] = path
    return written


def write_state(state: Mapping[str, object], path: Path) -> Path:
    """Persist canonical comparison state for the next scheduled run."""

    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    path.write_text(rendered, encoding="utf-8", newline="\n")
    return path


def load_state(path: Path) -> dict[str, object]:
    """Load and minimally validate comparison state."""

    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("SNICE state root must be an object")
    if value.get("state_version") != STATE_VERSION:
        raise ValueError(f"unsupported SNICE state version: {value.get('state_version')!r}")
    if not isinstance(value.get("documents"), list):
        raise ValueError("SNICE state must contain a document list")
    if not re.fullmatch(r"[0-9a-f]{64}", str(value.get("index_sha256", ""))):
        raise ValueError("SNICE state has invalid index_sha256")
    return value


def _parse_discovered_at(value: str | None) -> datetime:
    if value is None:
        return datetime.now(timezone.utc).replace(microsecond=0)
    normalized = value.strip().replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("--discovered-at must include a timezone")
    return parsed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Discover and normalize the official SNICE_DOCS index."
    )
    parser.add_argument("--url", default=SNICE_INDEX_URL)
    parser.add_argument("--input-html", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--state", type=Path)
    parser.add_argument("--state-output", type=Path)
    parser.add_argument("--max-bytes", type=int, default=DiscoveryPolicy().max_bytes)
    parser.add_argument("--timeout", type=float, default=DiscoveryPolicy().timeout_s)
    parser.add_argument("--discovered-at")
    args = parser.parse_args(argv)

    discovered_at = _parse_discovered_at(args.discovered_at)
    if args.input_html:
        index_html = args.input_html.read_text(encoding="utf-8")
    else:
        import requests

        policy = DiscoveryPolicy(timeout_s=args.timeout, max_bytes=args.max_bytes)
        with requests.Session() as session:
            index_html = fetch_index_html(session, args.url, policy=policy)

    previous_state = None
    if args.state and args.state.exists():
        previous_state = load_state(args.state)
    payloads = build_payloads(
        index_html,
        source_url=args.url,
        discovered_at=discovered_at,
        previous_state=previous_state,
    )
    written = write_payloads(payloads, args.output_dir)
    state = build_state(payloads)
    if args.state_output:
        write_state(state, args.state_output)

    print(
        json.dumps(
            {
                "source_url": args.url,
                "index_sha256": payloads["documents"]["index_sha256"],
                "index_entries": payloads["documents"]["index_entry_count"],
                "documents": payloads["documents"]["document_count"],
                "unparsed": payloads["documents"]["unparsed_count"],
                "series": payloads["series"]["series_count"],
                "findings": payloads["findings"]["finding_count"],
                "changes": payloads["changes"]["change_count"],
                "outputs": {key: str(path) for key, path in sorted(written.items())},
                "state_output": str(args.state_output) if args.state_output else None,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
