"""Conservatively audit whether important active legal sources have preserved originals."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit

import yaml

from scripts.archive_metadata import archive_label


TARGET_EVIDENCE_CLASSES = {"primary_legal", "official_consolidated"}
REPORT_PATH = Path("docs/status/missing-primary-sources.md")


@dataclass(frozen=True, slots=True)
class AuditRow:
    source_id: str
    title: str
    authority: str
    publication_date: str
    evidence_class: str
    instruments: tuple[str, ...]
    status: str
    what_repo_has: str
    missing: str
    why_needed: str


def _load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _normalized_url(value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        return ""
    parts = urlsplit(value.strip())
    path = parts.path.rstrip("/") or "/"
    return urlunsplit((parts.scheme.casefold(), parts.netloc.casefold(), path, parts.query, ""))


def _instrument_ids(source: dict[str, Any]) -> tuple[str, ...]:
    result: list[str] = []
    single = source.get("instrument_id")
    if isinstance(single, str) and single:
        result.append(single)
    multiple = source.get("instrument_ids")
    if isinstance(multiple, list):
        result.extend(item for item in multiple if isinstance(item, str) and item)
    return tuple(dict.fromkeys(result))


def _manifest_index(root: Path) -> tuple[dict[str, str], dict[str, str]]:
    originals = root / "data" / "originals"
    master_path = originals / "manifest.yaml"
    if not master_path.is_file():
        return {}, {}

    master = _load_yaml(master_path)
    fragments = master.get("fragments", []) if isinstance(master, dict) else []
    by_id: dict[str, str] = {}
    by_url: dict[str, str] = {}
    for fragment in fragments:
        if not isinstance(fragment, str):
            continue
        manifest_path = originals / fragment
        if not manifest_path.is_file():
            continue
        data = _load_yaml(manifest_path)
        documents = data.get("documents", []) if isinstance(data, dict) else []
        for document in documents:
            if not isinstance(document, dict):
                continue
            document_id = document.get("id")
            if isinstance(document_id, str) and document_id:
                by_id[document_id] = fragment
            url = _normalized_url(document.get("url"))
            if url:
                by_url[url] = fragment
    return by_id, by_url


def _manifest_match(
    source: dict[str, Any], by_id: dict[str, str], by_url: dict[str, str]
) -> str | None:
    source_id = source.get("id")
    if isinstance(source_id, str) and source_id in by_id:
        return by_id[source_id]
    url = _normalized_url(source.get("url"))
    if url and url in by_url:
        return by_url[url]
    return None


def _instrument_source_sets(root: Path) -> tuple[set[str], set[str]]:
    path = root / "sources" / "instruments.yaml"
    if not path.is_file():
        return set(), set()
    data = _load_yaml(path)
    instruments = data.get("instruments", []) if isinstance(data, dict) else []
    active: set[str] = set()
    superseded: set[str] = set()

    for instrument in instruments:
        if not isinstance(instrument, dict):
            continue
        target = superseded if instrument.get("status") == "superseded" else active
        consolidated = instrument.get("consolidated_source_id")
        if isinstance(consolidated, str) and consolidated:
            target.add(consolidated)
        events = instrument.get("events")
        if isinstance(events, list):
            for event in events:
                if not isinstance(event, dict):
                    continue
                source_id = event.get("source_id")
                if isinstance(source_id, str) and source_id:
                    target.add(source_id)

    return active, superseded - active


def _load_equivalences(
    root: Path, manifest_by_id: dict[str, str]
) -> dict[str, tuple[tuple[str, ...], str]]:
    path = root / "data" / "originals" / "equivalents.yaml"
    if not path.is_file():
        return {}
    data = _load_yaml(path)
    entries = data.get("equivalences", []) if isinstance(data, dict) else []
    result: dict[str, tuple[tuple[str, ...], str]] = {}

    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise ValueError(f"equivalents.yaml entry {index} must be a mapping")
        source_id = entry.get("source_id")
        ids = entry.get("manifest_document_ids")
        basis = entry.get("basis")
        if not isinstance(source_id, str) or not source_id:
            raise ValueError(f"equivalents.yaml entry {index} missing source_id")
        if source_id in result:
            raise ValueError(f"equivalents.yaml duplicate source_id: {source_id}")
        if not isinstance(ids, list) or not ids or not all(isinstance(item, str) and item for item in ids):
            raise ValueError(f"{source_id}: manifest_document_ids must be a non-empty string list")
        if not isinstance(basis, str) or not basis.strip():
            raise ValueError(f"{source_id}: equivalence basis is required")
        missing_ids = sorted(item for item in ids if item not in manifest_by_id)
        if missing_ids:
            raise ValueError(
                f"{source_id}: equivalence references unknown manifest document(s): {', '.join(missing_ids)}"
            )
        result[source_id] = (tuple(dict.fromkeys(ids)), basis.strip())
    return result


def _equivalent_description(
    source_id: str,
    equivalents: dict[str, tuple[tuple[str, ...], str]],
    manifest_by_id: dict[str, str],
) -> str | None:
    equivalent = equivalents.get(source_id)
    if equivalent is None:
        return None
    document_ids, basis = equivalent
    locations = sorted(
        {
            f"{document_id} ({manifest_by_id[document_id]})"
            for document_id in document_ids
        }
    )
    return f"Verified official equivalent(s): {', '.join(locations)}. Basis: {basis}"


def _is_target(source: dict[str, Any], source_id: str, active_source_ids: set[str]) -> bool:
    return (
        source.get("evidence_class") in TARGET_EVIDENCE_CLASSES
        and bool(_instrument_ids(source))
        and source_id in active_source_ids
    )


def audit_registry(root: Path) -> list[AuditRow]:
    registry = _load_yaml(root / "sources" / "registry.yaml")
    sources = registry.get("sources", []) if isinstance(registry, dict) else []
    by_id, by_url = _manifest_index(root)
    active_source_ids, superseded_only_ids = _instrument_source_sets(root)
    equivalents = _load_equivalences(root, by_id)
    rows: list[AuditRow] = []

    registry_ids = {
        str(source.get("id"))
        for source in sources
        if isinstance(source, dict) and isinstance(source.get("id"), str)
    }
    unknown_equivalence_sources = sorted(set(equivalents) - registry_ids)
    if unknown_equivalence_sources:
        raise ValueError(
            "equivalents.yaml references unknown registry source(s): "
            + ", ".join(unknown_equivalence_sources)
        )

    for source in sources:
        if not isinstance(source, dict):
            continue
        source_id = str(source.get("id", "<unknown>"))
        title = str(source.get("title", source_id))
        authority = str(source.get("authority", "-"))
        publication_date = str(source.get("publication_date", "-"))
        evidence_class = str(source.get("evidence_class", "-"))
        instruments = _instrument_ids(source)
        archive_state = archive_label(source)
        manifest_fragment = _manifest_match(source, by_id, by_url)
        equivalent_description = _equivalent_description(source_id, equivalents, by_id)

        if archive_state == "external_only":
            archive = source.get("archive")
            reason = archive.get("reason") if isinstance(archive, dict) else None
            status = "external_only"
            what_repo_has = f"Explicit external-only decision: {reason or '-'}"
            missing = "Nothing requested automatically."
            why_needed = "Storage exception is documented; review only if the source strategy changes."
        elif archive_state in {"local_git", "release_asset"}:
            status = "explicit_archive"
            what_repo_has = f"Explicit source archive metadata: {archive_state}."
            missing = "Nothing."
            why_needed = "Preservation state is explicitly recorded."
        elif manifest_fragment:
            status = "archived_manifest"
            what_repo_has = f"Document-level original in data/originals/{manifest_fragment}."
            missing = "Nothing."
            why_needed = "The original is already represented by a manifest with provenance/checksum."
        elif equivalent_description:
            status = "archived_equivalent"
            what_repo_has = equivalent_description
            missing = "Nothing."
            why_needed = "The publication event remains separately traceable while equivalent official bytes are already preserved."
        elif source_id in superseded_only_ids:
            status = "superseded_only"
            what_repo_has = "Canonical historical source registry entry linked only to a superseded instrument."
            missing = "Nothing requested automatically."
            why_needed = "Historical preservation remains useful, but it is not an automatic current-source request."
        elif _is_target(source, source_id, active_source_ids):
            status = "missing_primary"
            what_repo_has = "Canonical source registry entry and official URL, but no matching manifest, verified official equivalence, or explicit archive state."
            missing = "A preserved primary/consolidated original, verified official equivalent, or explicit documented storage exception."
            why_needed = "Needed to make this active legal source reproducible and auditable without relying only on an external URL."
        else:
            status = "not_target"
            what_repo_has = "Canonical source registry entry."
            missing = "Nothing requested automatically."
            why_needed = "This conservative audit only auto-flags active primary legal or consolidated sources referenced by the temporal instrument graph."

        rows.append(
            AuditRow(
                source_id=source_id,
                title=title,
                authority=authority,
                publication_date=publication_date,
                evidence_class=evidence_class,
                instruments=instruments,
                status=status,
                what_repo_has=what_repo_has,
                missing=missing,
                why_needed=why_needed,
            )
        )

    return sorted(
        rows,
        key=lambda row: (row.status, row.authority.casefold(), row.title.casefold(), row.source_id),
    )


def _escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_missing_report(rows: list[AuditRow]) -> str:
    missing = [row for row in rows if row.status == "missing_primary"]
    counts: dict[str, int] = {}
    for row in rows:
        counts[row.status] = counts.get(row.status, 0) + 1

    lines = [
        "# Missing primary-source originals",
        "",
        "<!-- Generated by python -m scripts.archive_audit. Do not edit manually. -->",
        "",
        "This is a conservative request queue, not a legal-currentness report. A source is listed only when it is an active primary legal or official consolidated source referenced by the temporal instrument graph and has no explicit archive state, direct manifest match, or declared verified official equivalent.",
        "",
        "Before asking the repository owner for a document, re-check the official source, manifests, declared equivalents, current uploads and equivalent/newer versions. Do not request documents merely because a wiki page is incomplete.",
        "",
        "## Audit summary",
        "",
        f"- Archived by document manifest: {counts.get('archived_manifest', 0)}",
        f"- Archived through verified official equivalence: {counts.get('archived_equivalent', 0)}",
        f"- Explicit source archive metadata: {counts.get('explicit_archive', 0)}",
        f"- Explicit external-only decisions: {counts.get('external_only', 0)}",
        f"- Superseded-only sources kept out of auto-request: {counts.get('superseded_only', 0)}",
        f"- Outside conservative auto-request scope: {counts.get('not_target', 0)}",
        f"- Missing primary originals requiring review: {len(missing)}",
        "",
        "## Request queue",
        "",
    ]

    if not missing:
        lines.extend(
            [
                "No genuinely missing primary-source originals were identified by this conservative audit.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "| Source | Authority | Published | Instrument(s) | What the repository has | What is missing | Why it is needed |",
                "|---|---|---|---|---|---|---|",
            ]
        )
        for row in sorted(
            missing,
            key=lambda item: (item.authority.casefold(), item.publication_date, item.source_id),
        ):
            instruments = ", ".join(row.instruments) or "-"
            lines.append(
                "| "
                + " | ".join(
                    [
                        f"`{_escape(row.source_id)}`<br>{_escape(row.title)}",
                        _escape(row.authority),
                        _escape(row.publication_date),
                        _escape(instruments),
                        _escape(row.what_repo_has),
                        _escape(row.missing),
                        _escape(row.why_needed),
                    ]
                )
                + " |"
            )
        lines.append("")

    lines.extend(
        [
            "## Interpretation",
            "",
            "A SIDOF/DOF publication event and an official consolidated or SAT/SE copy can serve different provenance roles. Declared equivalence means the repository has verified official bytes for the same bounded material; it never replaces the publication event as the authority for chronology or legal effect.",
            "",
            "The absence of a preserved copy does not mean the official source is invalid, and preservation does not prove that a source is legally current. Those decisions remain governed by the separate legal-review and temporal-instrument model.",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def run_check(root: Path) -> tuple[int, str]:
    expected = render_missing_report(audit_registry(root))
    target = root / REPORT_PATH
    actual = target.read_text(encoding="utf-8") if target.is_file() else ""
    if actual != expected:
        return 1, "missing-primary-source report is stale; regenerate with: python -m scripts.archive_audit"
    return 0, "missing-primary-source report is current"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)

    if args.check:
        code, message = run_check(args.root)
        print(message)
        return code

    report = render_missing_report(audit_registry(args.root))
    target = args.root / REPORT_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(report, encoding="utf-8")
    print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
