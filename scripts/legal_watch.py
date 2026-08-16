"""Normalize official legal-publication candidates for human review."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from dataclasses import asdict, dataclass
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import urlparse

import requests
import yaml


@dataclass(frozen=True, slots=True)
class Candidate:
    key: str
    note_id: str
    title: str
    publication_date: str
    url: str
    matched_keywords: tuple[str, ...]
    review_status: str = "candidate"


@dataclass(frozen=True, slots=True)
class KnownPublications:
    note_ids: frozenset[str]
    urls: frozenset[str]


def _text(value: object) -> str:
    return " ".join(unicodedata.normalize("NFKC", str(value)).split())


def known_publications(registry_path: Path) -> KnownPublications:
    """Load already-curated note IDs and URLs from the canonical registry."""

    data = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
    sources = data.get("sources", []) if isinstance(data, dict) else []
    return KnownPublications(
        frozenset(str(item["note_id"]) for item in sources if isinstance(item, dict) and item.get("note_id")),
        frozenset(str(item["url"]).rstrip("/") for item in sources if isinstance(item, dict) and item.get("url")),
    )


def normalize_candidates(
    payload: object,
    watch_config: dict,
    known: KnownPublications | None = None,
) -> tuple[Candidate, ...]:
    """Return unique, relevant official candidates without promoting legal status."""

    raw_items = payload.get("items", []) if isinstance(payload, dict) else payload
    if not isinstance(raw_items, list):
        return ()
    official_hosts = set(watch_config.get("official_hosts", []))
    keywords = tuple(_text(item).casefold() for item in watch_config.get("keywords", []))
    selected: dict[str, Candidate] = {}
    for raw in raw_items:
        if not isinstance(raw, dict):
            continue
        note_id = _text(raw.get("note_id", ""))
        title = _text(raw.get("title", ""))
        publication_date = _text(raw.get("publication_date", ""))
        url = _text(raw.get("url", ""))
        parsed = urlparse(url)
        try:
            date.fromisoformat(publication_date)
        except ValueError:
            continue
        if (
            not re.fullmatch(r"[0-9]+", note_id)
            or parsed.scheme != "https"
            or parsed.username is not None
            or parsed.password is not None
            or parsed.hostname not in official_hosts
            or parsed.port not in {None, 443}
            or parsed.path.rstrip("/") != f"/notas/{note_id}"
        ):
            continue
        normalized_url = url.rstrip("/")
        if known and (note_id in known.note_ids or normalized_url in known.urls):
            continue
        folded = title.casefold()
        matched = tuple(keyword for keyword in keywords if keyword in folded)
        if not matched:
            continue
        selected.setdefault(
            note_id,
            Candidate(
                key=f"sidof:{note_id}",
                note_id=note_id,
                title=title,
                publication_date=publication_date,
                url=normalized_url,
                matched_keywords=matched,
            ),
        )
    return tuple(sorted(selected.values(), key=lambda item: (item.publication_date, int(item.note_id))))


def sidof_items(payload: object, watch_config: dict) -> list[dict[str, str]]:
    """Adapt a documented SIDOF per-diary JSON response to candidate records."""

    if not isinstance(payload, dict):
        return []
    note_url = str(watch_config.get("note_url_template", "https://sidof.segob.gob.mx/notas/{note_id}"))
    records: list[dict[str, str]] = []
    for key in ("Notas", "notas"):
        raw_items = payload.get(key, [])
        if not isinstance(raw_items, list):
            continue
        for raw in raw_items:
            if not isinstance(raw, dict):
                continue
            raw_date = _text(raw.get("fecha", ""))
            try:
                day, month, year = raw_date.split("-")
                publication_date = date(int(year), int(month), int(day)).isoformat()
            except (ValueError, TypeError):
                continue
            note_id = _text(raw.get("codNota", ""))
            records.append(
                {
                    "note_id": note_id,
                    "title": _text(raw.get("titulo", "")),
                    "publication_date": publication_date,
                    "url": note_url.format(note_id=note_id),
                }
            )
    return records


def _fetch_sidof_json(
    url: str,
    watch_config: dict,
    transport: object,
    *,
    allow_no_publication: bool = False,
) -> object:
    """Fetch and validate one bounded JSON response from an allowlisted SIDOF API."""

    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname not in set(watch_config.get("official_hosts", [])):
        raise ValueError("SIDOF API URL is not an allowlisted HTTPS endpoint")
    response = transport.get(
        url,
        headers={"User-Agent": "wiki-comercio-exterior-mx-legal-watch/1.0"},
        timeout=15,
        allow_redirects=False,
        stream=True,
    )
    try:
        if int(response.status_code) != 200:
            raise RuntimeError(f"SIDOF API returned HTTP {response.status_code}")
        body = b""
        for chunk in response.iter_content(chunk_size=64 * 1024):
            body += chunk
            if len(body) > 5_000_000:
                raise RuntimeError("SIDOF API response exceeded 5 MB")
        payload = json.loads(body.decode("utf-8"))
        if not isinstance(payload, dict):
            raise RuntimeError("SIDOF API returned a non-object JSON payload")
        message_code = int(payload.get("messageCode", 0))
        response_text = str(payload.get("response", ""))
        if allow_no_publication and message_code == 400:
            return {}
        if message_code != 200 or response_text.upper() != "OK":
            raise RuntimeError(f"SIDOF API payload reported {message_code}: {response_text}")
        return payload
    finally:
        response.close()


def fetch_sidof_day(day: date, watch_config: dict, transport: object = requests) -> object:
    """Fetch one bounded official SIDOF daily index response."""

    template = str(watch_config["daily_api_template"])
    url = template.format(date=day.strftime("%d-%m-%Y"))
    return _fetch_sidof_json(
        url,
        watch_config,
        transport,
        allow_no_publication=True,
    )


def enrich_sidof_items(
    daily_payload: object,
    watch_config: dict,
    transport: object = requests,
) -> list[dict[str, str]]:
    """Resolve daily note indexes through the documented per-diary title API."""

    if not isinstance(daily_payload, dict):
        return []
    diary_ids: set[str] = set()
    for key in ("NotasMatutinas", "NotasVespertinas", "NotasExtraordinarias"):
        for raw in daily_payload.get(key, []):
            if isinstance(raw, dict) and re.fullmatch(r"[0-9]+", str(raw.get("codDiario", ""))):
                diary_ids.add(str(raw["codDiario"]))
    maximum = int(watch_config.get("max_diaries_per_day", 3))
    template = str(watch_config["diary_api_template"])
    records: list[dict[str, str]] = []
    for diary_id in sorted(diary_ids)[:maximum]:
        url = template.format(diary_id=diary_id)
        records.extend(
            sidof_items(_fetch_sidof_json(url, watch_config, transport), watch_config)
        )
    return records


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("payload", nargs="?", type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--date", type=date.fromisoformat, default=date.today())
    parser.add_argument("--lookback-days", type=int, default=1)
    parser.add_argument("--config", type=Path, default=Path("sources/watch.yaml"))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--fail-on-candidates", action="store_true")
    args = parser.parse_args(argv)
    config_path = args.config if args.config.is_absolute() else args.root / args.config
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    if args.lookback_days < 1 or args.lookback_days > 14:
        parser.error("--lookback-days must be between 1 and 14")
    if args.payload:
        payload = json.loads(args.payload.read_text(encoding="utf-8"))
    else:
        payload = []
        for offset in range(args.lookback_days):
            day = args.date - timedelta(days=offset)
            payload.extend(enrich_sidof_items(fetch_sidof_day(day, config), config))
    known = known_publications(args.root / "sources" / "registry.yaml")
    candidates = normalize_candidates(payload, config, known)
    output = json.dumps(
        [asdict(item) for item in candidates],
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 3 if args.fail_on_candidates and candidates else 0


if __name__ == "__main__":
    raise SystemExit(main())
