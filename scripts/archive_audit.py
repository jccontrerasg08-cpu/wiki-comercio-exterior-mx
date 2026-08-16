"""Conservatively audit whether important legal sources have preserved originals."""

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


def _is_target(source: dict[str, Any]) -> bool:
    return (
        source.get("evidence_class") in TARGET_EVIDENCE_CLASSES
        and bool(_instrument_ids(source))
    )


def audit_registry(root: Path) -> list[AuditRow]:
    registry = _load_yaml(root / "sources" / "registry.yaml")
    sources = registry.get("sources", []) if isinstance(registry, dict) else []
    by_id, by_url = _manifest_index(root)
    rows: list[AuditRow] = []

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
        elif _is_target(source):
            status = "missing_primary"
            what_repo_has = "Canonical source registry entry and official URL, but no matching original manifest or explicit archive state."
            missing = "A preserved primary/consolidated original or an explicit documented storage exception."
            why_needed = "Needed to make this legal source reproducible and auditable without relying only on an external URL."
        else:
            status = "not_target"
            what_repo_has = "Canonical source registry entry."
            missing = "Nothing requested automatically."
            why_needed = "This conservative audit only auto-flags primary legal or consolidated sources linked to an instrument."

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

    return sorted(rows, key=lambda row: (row.status, row.authority.casefold(), row.title.casefold(), row.source_id))


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
        "This is a conservative request queue, not a legal-currentness report. A source is listed only when it is primary legal or an official consolidated text, is linked to a known instrument, and has neither an explicit archive state nor an equivalent document in the existing originals manifests.",
        "",
        "Before asking the repository owner for a document, re-check the official source, manifests, current uploads and equivalent/newer versions. Do not request documents merely because a wiki page is incomplete.",
        "",
        "## Audit summary",
        "",
        f"- Archived by document manifest: {counts.get('archived_manifest', 0)}",
        f"- Explicit source archive metadata: {counts.get('explicit_archive', 0)}",
        f"- Explicit external-only decisions: {counts.get('external_only', 0)}",
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
        for row in sorted(missing, key=lambda item: (item.authority.casefold(), item.publication_date, item.source_id)):
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
