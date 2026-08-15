"""Offline validation and cutoff selection for legal instrument metadata."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import yaml

from scripts.schema_validation import load_local_schema, validate_instance


@dataclass(frozen=True, slots=True)
class TemporalFinding:
    """One deterministic temporal-graph finding."""

    code: str
    path: str
    message: str


def load_instruments(path: Path) -> list[dict[str, object]]:
    """Load an instrument list from canonical YAML."""

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("instruments"), list):
        raise ValueError(f"{path}: expected top-level instruments list")
    def normalize(value: Any) -> Any:
        if isinstance(value, date):
            return value.isoformat()
        if isinstance(value, dict):
            return {key: normalize(item) for key, item in value.items()}
        if isinstance(value, list):
            return [normalize(item) for item in value]
        return value

    return normalize(data["instruments"])


def _as_date(value: object) -> date | None:
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value)
        except ValueError:
            return None
    return None


def _sources(registry_path: Path) -> dict[str, dict[str, object]]:
    data = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("sources"), list):
        return {}
    return {
        item["id"]: item
        for item in data["sources"]
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }


def _cycle_findings(instruments: list[dict[str, object]]) -> list[TemporalFinding]:
    graph: dict[str, set[str]] = {
        str(item.get("id")): set() for item in instruments if item.get("id")
    }
    for instrument in instruments:
        source_id = instrument.get("id")
        events = instrument.get("events", [])
        if not isinstance(source_id, str) or not isinstance(events, list):
            continue
        for event in events:
            if not isinstance(event, dict):
                continue
            if event.get("relation") not in {"amends", "repeals", "supersedes"}:
                continue
            target = event.get("target_instrument_id")
            if isinstance(target, str):
                graph[source_id].add(target)

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str, trail: tuple[str, ...]) -> TemporalFinding | None:
        if node in visiting:
            cycle = trail[trail.index(node) :] + (node,)
            return TemporalFinding(
                "RELATION_CYCLE",
                f"instruments.{node}",
                "cyclic legal relationship: " + " -> ".join(cycle),
            )
        if node in visited:
            return None
        visiting.add(node)
        for target in sorted(graph.get(node, ())):
            finding = visit(target, trail + (target,))
            if finding is not None:
                return finding
        visiting.remove(node)
        visited.add(node)
        return None

    for node in sorted(graph):
        finding = visit(node, (node,))
        if finding is not None:
            return [finding]
    return []


def validate_temporal_graph(path_or_root: Path) -> list[TemporalFinding]:
    """Validate schemas, references, date order, and directed relationship cycles."""

    is_fixture = path_or_root.is_file()
    root = Path(__file__).resolve().parents[1] if is_fixture else path_or_root
    instruments_path = path_or_root if is_fixture else root / "sources" / "instruments.yaml"
    try:
        instruments = load_instruments(instruments_path)
    except (OSError, UnicodeError, yaml.YAMLError, ValueError) as exc:
        return [TemporalFinding("INSTRUMENTS_INVALID", str(instruments_path), str(exc))]

    findings: list[TemporalFinding] = []
    schema = load_local_schema(root, "instrument.schema.json")
    seen: set[str] = set()
    known_sources = {} if is_fixture else _sources(root / "sources" / "registry.yaml")

    for index, instrument in enumerate(instruments):
        item_path = f"instruments[{index}]"
        for finding in validate_instance(instrument, schema, item_path):
            findings.append(
                TemporalFinding("INSTRUMENT_SCHEMA", finding.path, finding.message)
            )
        instrument_id = instrument.get("id")
        if isinstance(instrument_id, str):
            if instrument_id in seen:
                findings.append(
                    TemporalFinding(
                        "INSTRUMENT_DUPLICATE_ID", item_path, f"duplicate {instrument_id}"
                    )
                )
            seen.add(instrument_id)

        start = _as_date(instrument.get("effective_from"))
        end = _as_date(instrument.get("effective_to"))
        current_through = _as_date(instrument.get("current_through"))
        if start is not None and end is not None and end < start:
            findings.append(
                TemporalFinding("INVALID_DATE_RANGE", item_path, "effective_to precedes effective_from")
            )

        consolidated = instrument.get("consolidated_source_id")
        if known_sources and consolidated not in known_sources:
            findings.append(
                TemporalFinding(
                    "UNKNOWN_SOURCE",
                    f"{item_path}.consolidated_source_id",
                    f"unknown source {consolidated}",
                )
            )
        elif isinstance(consolidated, str) and consolidated in known_sources:
            source_instrument = known_sources[consolidated].get("instrument_id")
            if source_instrument != instrument_id:
                findings.append(
                    TemporalFinding(
                        "SOURCE_INSTRUMENT_MISMATCH",
                        f"{item_path}.consolidated_source_id",
                        f"source declares {source_instrument!r}, expected {instrument_id!r}",
                    )
                )

        events = instrument.get("events", [])
        if not isinstance(events, list):
            continue
        for event_index, event in enumerate(events):
            if not isinstance(event, dict):
                continue
            event_path = f"{item_path}.events[{event_index}]"
            effective = _as_date(event.get("effective_from"))
            event_end = _as_date(event.get("effective_to"))
            if effective is not None and current_through is not None and effective > current_through:
                findings.append(
                    TemporalFinding(
                        "EVENT_AFTER_CURRENT_THROUGH",
                        event_path,
                        f"event {effective.isoformat()} is after {current_through.isoformat()}",
                    )
                )
            if effective is not None and event_end is not None and event_end < effective:
                findings.append(
                    TemporalFinding(
                        "INVALID_DATE_RANGE", event_path, "effective_to precedes effective_from"
                    )
                )
            source_id = event.get("source_id")
            if known_sources and source_id not in known_sources:
                findings.append(
                    TemporalFinding(
                        "UNKNOWN_SOURCE", f"{event_path}.source_id", f"unknown source {source_id}"
                    )
                )
            elif isinstance(source_id, str) and source_id in known_sources:
                source = known_sources[source_id]
                source_instrument = source.get("instrument_id")
                if source_instrument != instrument_id:
                    findings.append(
                        TemporalFinding(
                            "SOURCE_INSTRUMENT_MISMATCH",
                            f"{event_path}.source_id",
                            f"source declares {source_instrument!r}, expected {instrument_id!r}",
                        )
                    )
                publication = _as_date(source.get("publication_date"))
                if publication is None:
                    findings.append(
                        TemporalFinding(
                            "SOURCE_PUBLICATION_DATE_MISSING",
                            f"{event_path}.source_id",
                            "event source requires a valid publication_date",
                        )
                    )
                elif effective is not None and publication > effective:
                    findings.append(
                        TemporalFinding(
                            "SOURCE_PUBLISHED_AFTER_EFFECTIVE",
                            f"{event_path}.source_id",
                            f"publication {publication.isoformat()} follows effective date {effective.isoformat()}",
                        )
                    )

    findings.extend(_cycle_findings(instruments))
    return sorted(findings, key=lambda item: (item.code, item.path, item.message))


def sources_effective_on(
    instrument: dict[str, object], cutoff: date
) -> tuple[str, ...]:
    """Return consolidated and event sources effective on or before a cutoff."""

    selected: list[str] = []
    consolidated = instrument.get("consolidated_source_id")
    start = _as_date(instrument.get("effective_from"))
    end = _as_date(instrument.get("effective_to"))
    if isinstance(consolidated, str) and (start is None or start <= cutoff) and (
        end is None or cutoff <= end
    ):
        selected.append(consolidated)
    events = instrument.get("events", [])
    if isinstance(events, list):
        for event in events:
            if not isinstance(event, dict):
                continue
            event_start = _as_date(event.get("effective_from"))
            event_end = _as_date(event.get("effective_to"))
            source_id = event.get("source_id")
            if (
                isinstance(source_id, str)
                and event_start is not None
                and event_start <= cutoff
                and (event_end is None or cutoff <= event_end)
            ):
                selected.append(source_id)
    return tuple(dict.fromkeys(selected))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument("--check", action="store_true", help="validate and exit")
    args = parser.parse_args(argv)
    findings = validate_temporal_graph(args.root)
    for finding in findings:
        print(f"{finding.code} {finding.path}: {finding.message}")
    if findings:
        return 1
    print("Temporal graph validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
