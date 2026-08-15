"""Inventory and validate provenance metadata for wiki and corpus pages."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import yaml

from scripts.schema_validation import load_local_schema, validate_instance
from scripts.temporal_graph import load_instruments


@dataclass(frozen=True, slots=True)
class PageFinding:
    code: str
    path: str
    message: str


def inventory_content_pages(root: Path) -> tuple[str, ...]:
    """Return every governed page path relative to the repository root."""

    paths: list[str] = []
    for base, patterns in ((root / "docs" / "wiki", ("*.md",)), (root / "data" / "corpus", ("*.md", "*.csv"))):
        if not base.exists():
            continue
        for pattern in patterns:
            for path in base.rglob(pattern):
                if path.name.lower() == "readme.md":
                    continue
                paths.append(path.relative_to(root).as_posix())
    return tuple(sorted(set(paths)))


def _normalize(value: Any) -> Any:
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: _normalize(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_normalize(item) for item in value]
    return value


def _known_ids(root: Path) -> tuple[set[str], dict[str, dict[str, object]]]:
    source_ids: set[str] = set()
    registry = root / "sources" / "registry.yaml"
    if registry.exists():
        data = yaml.safe_load(registry.read_text(encoding="utf-8"))
        if isinstance(data, dict) and isinstance(data.get("sources"), list):
            source_ids = {
                item["id"]
                for item in data["sources"]
                if isinstance(item, dict) and isinstance(item.get("id"), str)
            }
    instruments_path = root / "sources" / "instruments.yaml"
    instruments = (
        {item["id"]: item for item in load_instruments(instruments_path)}
        if instruments_path.exists()
        else {}
    )
    return source_ids, instruments


def validate_page_metadata(root: Path) -> list[PageFinding]:
    """Validate sidecar shape, inventory coverage, references, and status dates."""

    metadata_path = root / "sources" / "page_metadata.yaml"
    try:
        data = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        return [PageFinding("PAGE_METADATA_INVALID", str(metadata_path), str(exc))]
    if not isinstance(data, dict) or not isinstance(data.get("pages"), list):
        return [PageFinding("PAGE_METADATA_INVALID", str(metadata_path), "expected top-level pages list")]

    project_root = Path(__file__).resolve().parents[1]
    schema_root = root if (root / "schemas" / "page-metadata.schema.json").exists() else project_root
    schema = load_local_schema(schema_root, "page-metadata.schema.json")
    source_ids, instruments = _known_ids(root)
    inventory = set(inventory_content_pages(root))
    seen: set[str] = set()
    findings: list[PageFinding] = []

    for index, raw_page in enumerate(data["pages"]):
        page = _normalize(raw_page)
        item_path = f"pages[{index}]"
        for finding in validate_instance(page, schema, item_path):
            findings.append(PageFinding("PAGE_SCHEMA", finding.path, finding.message))
        if not isinstance(page, dict):
            continue
        path = page.get("path")
        if not isinstance(path, str):
            continue
        if path in seen:
            findings.append(PageFinding("PAGE_DUPLICATE", path, "duplicate metadata record"))
        seen.add(path)
        if path not in inventory:
            findings.append(PageFinding("PAGE_NOT_FOUND", path, "metadata path is not a governed content file"))
        for source_id in page.get("source_ids", []):
            if source_ids and source_id not in source_ids:
                findings.append(PageFinding("PAGE_UNKNOWN_SOURCE", path, f"unknown source {source_id}"))
        for instrument_id in page.get("instrument_ids", []):
            if instruments and instrument_id not in instruments:
                findings.append(PageFinding("PAGE_UNKNOWN_INSTRUMENT", path, f"unknown instrument {instrument_id}"))
        if page.get("corpus_status") == "current" and page.get("current_through") is None:
            findings.append(PageFinding("PAGE_CURRENT_WITHOUT_DATE", path, "current corpus requires current_through"))
        if (
            page.get("content_type") == "wiki_explainer"
            and page.get("source_status") == "current"
            and page.get("legal_review_status") == "reviewed"
            and page.get("current_through") is None
        ):
            findings.append(PageFinding("PAGE_CURRENT_WITHOUT_DATE", path, "current reviewed wiki page requires current_through"))
        current_through = page.get("current_through")
        if isinstance(current_through, str):
            for instrument_id in page.get("instrument_ids", []):
                instrument = instruments.get(instrument_id)
                if not instrument:
                    continue
                latest = max(
                    (
                        str(event.get("effective_from"))
                        for event in instrument.get("events", [])
                        if isinstance(event, dict) and event.get("effective_from")
                    ),
                    default=str(instrument.get("effective_from", "")),
                )
                if page.get("corpus_status") == "current" and latest > current_through:
                    findings.append(
                        PageFinding(
                            "PAGE_BEHIND_INSTRUMENT",
                            path,
                            f"current_through {current_through} precedes known event {latest}",
                        )
                    )

    for missing in sorted(inventory - seen):
        findings.append(PageFinding("PAGE_METADATA_MISSING", missing, "content file has no metadata record"))
    return sorted(findings, key=lambda item: (item.code, item.path, item.message))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    findings = validate_page_metadata(args.root)
    for finding in findings:
        print(f"{finding.code} {finding.path}: {finding.message}")
    if findings:
        return 1
    print("Page metadata validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
