"""Bounded, host-restricted health probes for registered official sources."""

from __future__ import annotations

import argparse
import hashlib
import json
import unicodedata
from dataclasses import asdict, dataclass
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
import yaml


@dataclass(frozen=True, slots=True)
class ProbePolicy:
    timeout_seconds: int = 15
    max_bytes: int = 20_000_000
    max_redirects: int = 3


@dataclass(frozen=True, slots=True)
class ProbeResult:
    source_id: str
    classification: str
    final_url: str | None = None
    status_code: int | None = None
    media_type: str | None = None
    bytes_read: int | None = None
    sha256: str | None = None
    detail: str | None = None


def _normalized_text(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value)
    plain = "".join(char for char in decomposed if not unicodedata.combining(char))
    return " ".join(plain.casefold().split())


def classify_response(source: dict, response: object, body: bytes) -> ProbeResult:
    """Classify already-bounded bytes without treating success as legal validity."""

    probe = source.get("probe", {})
    source_id = str(source.get("id", "unknown"))
    status = int(getattr(response, "status_code", 0))
    final_url = str(getattr(response, "url", source.get("url", "")))
    headers = getattr(response, "headers", {})
    raw_type = str(headers.get("content-type", ""))
    media_type = raw_type.split(";", 1)[0].strip().lower() or None
    expected = probe.get("expected_status", [200])
    if status not in expected:
        return ProbeResult(source_id, "unexpected_status", final_url, status, media_type, len(body), detail=f"expected {expected}")
    allowed_media = [str(value).lower() for value in source.get("media_types", [])]
    if allowed_media and media_type not in allowed_media:
        return ProbeResult(source_id, "unexpected_media_type", final_url, status, media_type, len(body))
    min_bytes = int(probe.get("min_bytes", 0))
    if len(body) < min_bytes:
        return ProbeResult(source_id, "too_small", final_url, status, media_type, len(body), detail=f"minimum {min_bytes}")
    folded = body.decode("utf-8", errors="ignore").casefold()
    markers = [str(value) for value in probe.get("reject_if_contains", [])]
    if any(marker.casefold() in folded for marker in markers):
        return ProbeResult(source_id, "suspicious_response", final_url, status, media_type, len(body))
    normalized_body = _normalized_text(body.decode("utf-8", errors="ignore"))
    expected_title = probe.get("expected_title")
    if expected_title and _normalized_text(str(expected_title)) not in normalized_body:
        return ProbeResult(source_id, "identity_mismatch", final_url, status, media_type, len(body), detail="expected title not found")
    note_id = source.get("note_id")
    if note_id:
        path_note_id = urlparse(final_url).path.rstrip("/").rsplit("/", 1)[-1]
        if path_note_id != str(note_id) and str(note_id) not in normalized_body:
            return ProbeResult(source_id, "identity_mismatch", final_url, status, media_type, len(body), detail="SIDOF note id not found")
    expected_path = probe.get("expected_path") or urlparse(str(source.get("url", ""))).path
    if expected_path and urlparse(final_url).path != expected_path:
        return ProbeResult(source_id, "identity_mismatch", final_url, status, media_type, len(body), detail="unexpected final path")
    return ProbeResult(
        source_id,
        "healthy_transport",
        final_url,
        status,
        media_type,
        len(body),
        hashlib.sha256(body).hexdigest(),
        "transport only; legal status requires review",
    )


def probe_source(
    source: dict, transport: object, policy: ProbePolicy = ProbePolicy()
) -> ProbeResult:
    """Fetch one source with bounded redirects, bytes, time, and allowed hosts."""

    source_id = str(source.get("id", "unknown"))
    allowed_hosts = set(source.get("allowed_hosts", []))
    redirect_codes = {301, 302, 303, 307, 308}

    def reject_url(url: str) -> ProbeResult | None:
        parsed = urlparse(url)
        if parsed.scheme != "https":
            return ProbeResult(source_id, "redirect_scheme_rejected", final_url=url, detail="only HTTPS is allowed")
        if not parsed.hostname or parsed.hostname not in allowed_hosts:
            return ProbeResult(source_id, "redirect_host_rejected", final_url=url, detail=f"host {parsed.hostname!r} is not allowlisted")
        return None

    current_url = str(source["url"])
    try:
        for redirect_count in range(policy.max_redirects + 1):
            rejected = reject_url(current_url)
            if rejected is not None:
                return rejected
            response = transport.get(
                current_url,
                headers={"User-Agent": "wiki-comercio-exterior-mx-source-health/1.0"},
                timeout=policy.timeout_seconds,
                allow_redirects=False,
                stream=True,
            )
            try:
                status = int(getattr(response, "status_code", 0))
                headers = getattr(response, "headers", {})
                if status in redirect_codes:
                    location = headers.get("location")
                    if not location:
                        return ProbeResult(source_id, "redirect_without_location", final_url=current_url, status_code=status)
                    next_url = urljoin(current_url, str(location))
                    rejected = reject_url(next_url)
                    if rejected is not None:
                        return rejected
                    if redirect_count >= policy.max_redirects:
                        return ProbeResult(source_id, "redirect_limit", final_url=current_url, status_code=status, detail=f"maximum {policy.max_redirects}")
                    current_url = next_url
                    continue
                if not getattr(response, "url", None):
                    try:
                        setattr(response, "url", current_url)
                    except AttributeError:
                        pass
                max_bytes = min(int(source.get("probe", {}).get("max_bytes", policy.max_bytes)), policy.max_bytes)
                content_length = headers.get("content-length")
                if content_length and int(content_length) > max_bytes:
                    return ProbeResult(source_id, "size_limit", final_url=current_url, status_code=status, detail=f"declared {content_length} bytes")
                chunks: list[bytes] = []
                total = 0
                for chunk in response.iter_content(chunk_size=64 * 1024):
                    if not chunk:
                        continue
                    total += len(chunk)
                    if total > max_bytes:
                        return ProbeResult(source_id, "size_limit", final_url=current_url, status_code=status, bytes_read=total)
                    chunks.append(chunk)
                return classify_response(source, response, b"".join(chunks))
            finally:
                close = getattr(response, "close", None)
                if callable(close):
                    close()
    except (OSError, ValueError, requests.RequestException) as exc:
        return ProbeResult(source_id, "unreachable", detail=type(exc).__name__)


def select_sources(sources: list[dict], requested: list[str]) -> list[dict]:
    """Select all harvestable sources, or an exact explicit smoke-test subset."""

    requested_ids = set(requested)
    if requested_ids:
        known_ids = {str(source.get("id")) for source in sources}
        unknown = sorted(requested_ids - known_ids)
        if unknown:
            raise ValueError("unknown source id(s): " + ", ".join(unknown))
        return [source for source in sources if source.get("id") in requested_ids]
    return [source for source in sources if source.get("harvest") is True]


def select_due_sources(
    sources: list[dict], observations: dict[str, dict], as_of: date
) -> list[dict]:
    """Select harvestable sources whose last successful observation is due."""

    due: list[dict] = []
    for source in sources:
        if source.get("harvest") is not True:
            continue
        observation = observations.get(str(source.get("id")), {})
        if observation.get("classification") != "healthy_transport":
            due.append(source)
            continue
        try:
            observed_at = date.fromisoformat(str(observation["observed_at"]))
            cadence = int(source.get("cadence_days", 1))
        except (KeyError, TypeError, ValueError):
            due.append(source)
            continue
        if observed_at + timedelta(days=cadence) <= as_of:
            due.append(source)
    def observation_order(source: dict) -> tuple[date, str]:
        observation = observations.get(str(source.get("id")), {})
        try:
            observed_at = date.fromisoformat(str(observation["observed_at"]))
        except (KeyError, TypeError, ValueError):
            observed_at = date.min
        return observed_at, str(source.get("id", ""))

    return sorted(due, key=observation_order)


def _load_observations(path: Path | None) -> dict[str, dict]:
    if path is None or not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data.get("observations", {}) if isinstance(data, dict) else {}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument("--source", action="append", default=[])
    parser.add_argument("--mode", choices=("all", "due"), default="all")
    parser.add_argument("--as-of", type=date.fromisoformat, default=date.today())
    parser.add_argument("--state", type=Path)
    parser.add_argument("--state-output", type=Path)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    data = yaml.safe_load((args.root / "sources" / "registry.yaml").read_text(encoding="utf-8"))
    observations = _load_observations(args.state)
    try:
        selected = (
            select_sources(data["sources"], args.source)
            if args.source or args.mode == "all"
            else select_due_sources(data["sources"], observations, args.as_of)
        )
    except ValueError as exc:
        parser.error(str(exc))
    if args.limit < 0:
        parser.error("--limit must be non-negative")
    if args.limit:
        selected = selected[: args.limit]
    session = requests.Session()
    session.max_redirects = ProbePolicy().max_redirects
    results = [asdict(probe_source(source, session)) for source in selected]
    payload = json.dumps(results, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    if args.state_output:
        updated = dict(observations)
        for item in results:
            updated[item["source_id"]] = {
                "observed_at": args.as_of.isoformat(),
                "classification": item["classification"],
                "sha256": item["sha256"],
            }
        args.state_output.write_text(
            yaml.safe_dump({"observations": updated}, sort_keys=True),
            encoding="utf-8",
        )
    return 1 if any(item["classification"] != "healthy_transport" for item in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
