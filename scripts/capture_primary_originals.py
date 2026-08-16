"""Capture missing official primary-source bytes into a deterministic local manifest."""

from __future__ import annotations

import argparse
import hashlib
import html
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

import yaml

from scripts.archive_audit import audit_registry


MAX_CAPTURE_BYTES = 25 * 1024 * 1024
BLOCK_MARKERS = (b"access denied", b"captcha", b"forbidden")
_IFRAME_SRC_RE = re.compile(
    rb"<iframe\b[^>]*\bsrc\s*=\s*['\"]([^'\"]+)['\"]", re.IGNORECASE
)
_EMBEDDED_DOF_HOST = "dof.gob.mx"


def _normalized_media_type(value: str) -> str:
    return value.split(";", 1)[0].strip().casefold()


def _allowed_hosts(source: dict[str, Any]) -> set[str]:
    values = source.get("allowed_hosts")
    if not isinstance(values, list) or not values:
        raise ValueError(f"{source.get('id', '<unknown>')}: allowed_hosts is required")
    hosts = {str(value).strip().casefold() for value in values if str(value).strip()}
    if not hosts:
        raise ValueError(f"{source.get('id', '<unknown>')}: allowed_hosts is required")
    return hosts


def _validate_capture_url(source: dict[str, Any], url: str) -> None:
    parts = urlsplit(url)
    if parts.scheme.casefold() != "https":
        raise ValueError(f"{source.get('id', '<unknown>')}: capture URL must use HTTPS")
    host = (parts.hostname or "").casefold()
    if host not in _allowed_hosts(source):
        raise ValueError(
            f"{source.get('id', '<unknown>')}: capture host {host or '<missing>'} "
            "is outside allowed_hosts"
        )


def _is_sidof_source(source: dict[str, Any]) -> bool:
    canonical = source.get("url")
    return (
        isinstance(canonical, str)
        and (urlsplit(canonical).hostname or "").casefold() == "sidof.segob.gob.mx"
    )


def _validate_manifest_capture_url(source: dict[str, Any], url: str) -> None:
    parts = urlsplit(url)
    host = (parts.hostname or "").casefold()
    if _is_sidof_source(source) and host == _EMBEDDED_DOF_HOST:
        if parts.scheme.casefold() != "https" or not parts.path.casefold().endswith(".pdf"):
            raise ValueError(
                f"{source.get('id', '<unknown>')}: embedded DOF capture must be an HTTPS PDF"
            )
        return
    _validate_capture_url(source, url)


def embedded_official_pdf_url(payload: bytes) -> str | None:
    """Return a single DOF PDF embedded by a SIDOF visor, if present."""

    candidates: list[str] = []
    for raw_src in _IFRAME_SRC_RE.findall(payload):
        try:
            src = html.unescape(raw_src.decode("utf-8", errors="strict")).strip()
        except UnicodeDecodeError as exc:
            raise ValueError("embedded PDF URL is not valid UTF-8") from exc
        parts = urlsplit(src)
        if not parts.path.casefold().endswith(".pdf"):
            continue
        if parts.scheme.casefold() != "https":
            raise ValueError("embedded PDF must use HTTPS")
        host = (parts.hostname or "").casefold()
        if host != _EMBEDDED_DOF_HOST:
            raise ValueError(f"embedded PDF host {host or '<missing>'} is not dof.gob.mx")
        candidates.append(src)

    unique = list(dict.fromkeys(candidates))
    if len(unique) > 1:
        raise ValueError("SIDOF visor contains multiple distinct official PDF candidates")
    return unique[0] if unique else None


def capture_url_for(source: dict[str, Any]) -> tuple[str, str]:
    canonical = source.get("url")
    if not isinstance(canonical, str) or not canonical.strip():
        raise ValueError(f"{source.get('id', '<unknown>')}: canonical source URL is required")

    note_id = source.get("note_id")
    canonical_host = (urlsplit(canonical).hostname or "").casefold()
    if canonical_host == "sidof.segob.gob.mx" and isinstance(note_id, (str, int)):
        note_value = str(note_id).strip()
        if not note_value.isdigit():
            raise ValueError(f"{source.get('id', '<unknown>')}: SIDOF note_id must be numeric")
        capture_url = f"https://sidof.segob.gob.mx/notas/docFuente/{note_value}"
        suffix = ".html"
    else:
        capture_url = canonical
        media_types = {
            _normalized_media_type(str(value))
            for value in source.get("media_types", [])
            if isinstance(value, str)
        }
        suffix = ".pdf" if (
            "application/pdf" in media_types
            or urlsplit(canonical).path.casefold().endswith(".pdf")
        ) else ".html"

    _validate_capture_url(source, capture_url)
    return capture_url, suffix


def validate_payload(
    source: dict[str, Any], url: str, media_type: str, payload: bytes
) -> None:
    _validate_capture_url(source, url)
    if len(payload) > MAX_CAPTURE_BYTES:
        raise ValueError(
            f"{source.get('id', '<unknown>')}: payload exceeds local capture size limit"
        )

    normalized_media = _normalized_media_type(media_type)
    if normalized_media == "application/pdf":
        if not payload.startswith(b"%PDF-"):
            raise ValueError(
                f"{source.get('id', '<unknown>')}: PDF signature is missing"
            )
        return

    if normalized_media in {"text/html", "application/xhtml+xml"}:
        if len(payload) < 500:
            raise ValueError(
                f"{source.get('id', '<unknown>')}: HTML payload is too small to preserve"
            )
        folded = payload.lower()
        if any(marker in folded for marker in BLOCK_MARKERS):
            raise ValueError(
                f"{source.get('id', '<unknown>')}: HTML payload appears blocked"
            )
        return

    raise ValueError(
        f"{source.get('id', '<unknown>')}: unsupported capture media type {normalized_media or '<missing>'}"
    )


def build_manifest_document(
    source: dict[str, Any],
    file_name: str,
    capture_url: str,
    media_type: str,
    payload: bytes,
) -> dict[str, Any]:
    source_id = source.get("id")
    canonical_url = source.get("url")
    if not isinstance(source_id, str) or not source_id:
        raise ValueError("source id is required")
    if not isinstance(canonical_url, str) or not canonical_url:
        raise ValueError(f"{source_id}: canonical source URL is required")

    _validate_manifest_capture_url(source, capture_url)
    document: dict[str, Any] = {
        "id": source_id,
        "storage": "local_git",
        "file": file_name,
        "url": canonical_url,
        "media_type": _normalized_media_type(media_type),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "bytes": len(payload),
        "license": "official-not-relicensed",
        "redistribution": (
            "Official Mexican government source preserved for provenance; "
            "the repository does not relicense the material."
        ),
    }
    if capture_url.rstrip("/") != canonical_url.rstrip("/"):
        document["capture_url"] = capture_url
    return document


class _AllowedRedirectHandler(HTTPRedirectHandler):
    def __init__(self, source: dict[str, Any]) -> None:
        super().__init__()
        self.source = source

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[override]
        _validate_capture_url(self.source, newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _fetch_once(source: dict[str, Any], url: str) -> tuple[str, str, bytes]:
    opener = build_opener(_AllowedRedirectHandler(source))
    request = Request(
        url,
        headers={
            "User-Agent": "wiki-comercio-exterior-mx-source-archive/1.0",
            "Accept": "application/pdf,text/html;q=0.9,*/*;q=0.1",
        },
    )
    with opener.open(request, timeout=45) as response:
        final_url = response.geturl()
        _validate_capture_url(source, final_url)
        content_length = response.headers.get("Content-Length")
        if content_length and content_length.isdigit() and int(content_length) > MAX_CAPTURE_BYTES:
            raise ValueError(
                f"{source.get('id', '<unknown>')}: declared payload exceeds local capture size limit"
            )
        payload = response.read(MAX_CAPTURE_BYTES + 1)
        if len(payload) > MAX_CAPTURE_BYTES:
            raise ValueError(
                f"{source.get('id', '<unknown>')}: payload exceeds local capture size limit"
            )
        media_type = response.headers.get_content_type()
    validate_payload(source, final_url, media_type, payload)
    return final_url, media_type, payload


def _fetch_source(source: dict[str, Any], url: str) -> tuple[str, str, bytes]:
    final_url, media_type, payload = _fetch_once(source, url)
    if _is_sidof_source(source) and _normalized_media_type(media_type) in {
        "text/html",
        "application/xhtml+xml",
    }:
        embedded_pdf = embedded_official_pdf_url(payload)
        if embedded_pdf:
            embedded_source = dict(source)
            embedded_source["allowed_hosts"] = [_EMBEDDED_DOF_HOST]
            embedded_source["media_types"] = ["application/pdf"]
            return _fetch_once(embedded_source, embedded_pdf)
    return final_url, media_type, payload


def _load_registry(root: Path) -> dict[str, dict[str, Any]]:
    data = yaml.safe_load((root / "sources" / "registry.yaml").read_text(encoding="utf-8"))
    sources = data.get("sources", []) if isinstance(data, dict) else []
    return {
        str(source["id"]): source
        for source in sources
        if isinstance(source, dict) and isinstance(source.get("id"), str)
    }


def capture_missing_sources(root: Path, output: Path) -> list[dict[str, Any]]:
    registry = _load_registry(root)
    missing_ids = sorted(
        row.source_id for row in audit_registry(root) if row.status == "missing_primary"
    )
    output.mkdir(parents=True, exist_ok=True)
    documents: list[dict[str, Any]] = []

    for source_id in missing_ids:
        source = registry[source_id]
        planned_capture_url, _ = capture_url_for(source)
        final_capture_url, media_type, payload = _fetch_source(source, planned_capture_url)
        suffix = ".pdf" if _normalized_media_type(media_type) == "application/pdf" else ".html"
        file_name = f"{source_id}{suffix}"
        (output / file_name).write_bytes(payload)
        documents.append(
            build_manifest_document(
                source, file_name, final_capture_url, media_type, payload
            )
        )

    documents.sort(key=lambda item: str(item["id"]))
    manifest = {
        "version": 1,
        "captured_at": output.name.removeprefix("primary-") or "unspecified",
        "documents": documents,
    }
    (output / "MANIFEST.yaml").write_text(
        yaml.safe_dump(manifest, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    return documents


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/originals/primary-2026-08-16"),
    )
    args = parser.parse_args(argv)
    output = args.output if args.output.is_absolute() else args.root / args.output
    documents = capture_missing_sources(args.root, output)
    print(f"captured {len(documents)} primary original(s) into {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
