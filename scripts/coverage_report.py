"""Build deterministic corpus-governance coverage reports and enforce policy gates."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import yaml

from scripts.page_metadata import validate_page_metadata


_JSON_OUTPUT = Path("reports/corpus-coverage.json")
_MARKDOWN_OUTPUT = Path("docs/status/corpus-coverage.md")
_POLICY_PATH = Path("coverage-policy.yaml")
_NON_CURRENT_CORPUS = frozenset({"stale", "superseded", "partial", "unknown"})


@dataclass(frozen=True, slots=True)
class CheckResult:
    exit_code: int
    message: str


def _normalize(value: Any) -> Any:
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, dict):
        return {str(key): _normalize(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_normalize(item) for item in value]
    return value


def _is_retrieval_eligible(page: dict[str, object]) -> bool:
    """Mirror the current-answer page gate used by scripts.rag_eval."""

    if page.get("legal_review_status") != "reviewed":
        return False
    if page.get("source_status") != "current":
        return False
    return page.get("corpus_status") in {None, "current", "not_applicable"}


def risk_reasons(page: dict[str, object]) -> tuple[str, ...]:
    """Return stable governance reasons that put a page in the attention queue."""

    reasons: list[str] = []
    if page.get("legal_review_status") == "pending_review":
        reasons.append("pending_legal_review")
    if page.get("source_status") != "current":
        reasons.append("source_not_current")
    if page.get("extraction_status") in {"partial", "unknown"}:
        reasons.append("extraction_incomplete")
    if page.get("corpus_status") in _NON_CURRENT_CORPUS:
        reasons.append("corpus_not_current")
    source_ids = page.get("source_ids")
    if not isinstance(source_ids, list) or not source_ids:
        reasons.append("missing_source_reference")
    instrument_ids = page.get("instrument_ids")
    if (
        page.get("content_type") in {"wiki_explainer", "explanatory_digest"}
        and (not isinstance(instrument_ids, list) or not instrument_ids)
    ):
        reasons.append("missing_instrument_reference")
    return tuple(sorted(reasons))


def _section_for(path: str) -> str:
    parts = path.split("/")
    if path.startswith("docs/wiki/"):
        return parts[2] if len(parts) > 3 else "wiki"
    if path.startswith("data/corpus/"):
        return "corpus"
    return "other"


def _status_counts(pages: list[dict[str, object]], field: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for page in pages:
        value = str(page.get(field, "unknown"))
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def build_report_from_pages(raw_pages: list[dict[str, object]]) -> dict[str, object]:
    """Build one canonical report from already-loaded page metadata."""

    pages = [_normalize(page) for page in raw_pages]
    pages.sort(key=lambda page: str(page.get("path", "")))

    source_ids = {
        str(source_id)
        for page in pages
        for source_id in page.get("source_ids", [])
        if isinstance(source_id, str)
    }
    instrument_ids = {
        str(instrument_id)
        for page in pages
        for instrument_id in page.get("instrument_ids", [])
        if isinstance(instrument_id, str)
    }
    reviewed_dates = [
        str(page["reviewed_at"])
        for page in pages
        if isinstance(page.get("reviewed_at"), str)
    ]

    page_rows: list[dict[str, object]] = []
    section_accumulator: dict[str, dict[str, int]] = {}
    for page in pages:
        path = str(page.get("path", ""))
        section = _section_for(path)
        eligible = _is_retrieval_eligible(page)
        risks = risk_reasons(page)
        section_metrics = section_accumulator.setdefault(
            section,
            {
                "total_pages": 0,
                "retrieval_eligible_pages": 0,
                "legally_reviewed_pages": 0,
                "pages_needing_attention": 0,
            },
        )
        section_metrics["total_pages"] += 1
        if eligible:
            section_metrics["retrieval_eligible_pages"] += 1
        if page.get("legal_review_status") == "reviewed":
            section_metrics["legally_reviewed_pages"] += 1
        if risks:
            section_metrics["pages_needing_attention"] += 1

        page_rows.append(
            {
                "path": path,
                "title": str(page.get("title", "")),
                "section": section,
                "content_type": str(page.get("content_type", "")),
                "source_status": str(page.get("source_status", "")),
                "extraction_status": str(page.get("extraction_status", "")),
                "legal_review_status": str(page.get("legal_review_status", "")),
                "corpus_status": str(page.get("corpus_status", "")),
                "reviewed_at": page.get("reviewed_at"),
                "current_through": page.get("current_through"),
                "source_ids": list(page.get("source_ids", [])),
                "instrument_ids": list(page.get("instrument_ids", [])),
                "retrieval_eligible": eligible,
                "risk_reasons": list(risks),
            }
        )

    sections = [
        {"section": section, **metrics}
        for section, metrics in sorted(section_accumulator.items())
    ]
    status_counts = {
        field: _status_counts(pages, field)
        for field in (
            "source_status",
            "extraction_status",
            "legal_review_status",
            "corpus_status",
        )
    }
    summary = {
        "total_pages": len(pages),
        "wiki_pages": sum(str(page.get("path", "")).startswith("docs/wiki/") for page in pages),
        "corpus_pages": sum(str(page.get("path", "")).startswith("data/corpus/") for page in pages),
        "pages_with_sources": sum(bool(page.get("source_ids")) for page in pages),
        "pages_with_instruments": sum(bool(page.get("instrument_ids")) for page in pages),
        "retrieval_eligible_pages": sum(_is_retrieval_eligible(page) for page in pages),
        "legally_reviewed_pages": sum(page.get("legal_review_status") == "reviewed" for page in pages),
        "pending_legal_review_pages": sum(page.get("legal_review_status") == "pending_review" for page in pages),
        "non_current_corpus_pages": sum(page.get("corpus_status") in _NON_CURRENT_CORPUS for page in pages),
        "unknown_source_status_pages": sum(page.get("source_status") == "unknown" for page in pages),
        "pages_needing_attention": sum(bool(risk_reasons(page)) for page in pages),
        "distinct_source_ids": len(source_ids),
        "distinct_instrument_ids": len(instrument_ids),
    }
    return {
        "schema_version": 1,
        "latest_reviewed_at": max(reviewed_dates, default=None),
        "summary": summary,
        "status_counts": status_counts,
        "sections": sections,
        "pages": page_rows,
    }


def _load_pages(root: Path) -> list[dict[str, object]]:
    path = root / "sources" / "page_metadata.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("pages"), list):
        raise ValueError(f"{path}: expected top-level pages list")
    return [page for page in data["pages"] if isinstance(page, dict)]


def build_report(root: Path) -> dict[str, object]:
    return build_report_from_pages(_load_pages(root))


def render_json(report: dict[str, object]) -> str:
    """Render a compact machine-readable governance snapshot.

    The internal report retains full per-page metadata for tests and Markdown rendering.
    The committed JSON intentionally stores only aggregate metrics and pages that need
    attention, avoiding a second verbose copy of the canonical page metadata registry.
    """

    attention_queue = [
        {
            "path": page["path"],
            "section": page["section"],
            "risk_reasons": page["risk_reasons"],
        }
        for page in report["pages"]
        if page["risk_reasons"]
    ]
    snapshot = {
        "schema_version": report["schema_version"],
        "latest_reviewed_at": report["latest_reviewed_at"],
        "summary": report["summary"],
        "status_counts": report["status_counts"],
        "sections": report["sections"],
        "attention_queue": attention_queue,
    }
    return json.dumps(snapshot, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _pct(value: int, total: int) -> str:
    return "0.0%" if total == 0 else f"{(value / total) * 100:.1f}%"


def render_markdown(report: dict[str, object]) -> str:
    summary = report["summary"]
    total = int(summary["total_pages"])
    lines = [
        "# Estado del corpus",
        "",
        "!!! warning \"Métrica de gobernanza, no dictamen jurídico\"",
        "    Este dashboard mide revisión, frescura, extracción y trazabilidad del repositorio. **No mide corrección jurídica sustantiva** ni sustituye la revisión de la fuente oficial aplicable.",
        "",
        f"Última revisión registrada en metadata: **{report.get('latest_reviewed_at') or '-'}**.",
        "",
        "## Resumen",
        "",
        "| Métrica | Valor |",
        "|---|---:|",
        f"| Páginas gobernadas | {summary['total_pages']} |",
        f"| Wiki | {summary['wiki_pages']} |",
        f"| Corpus de apoyo | {summary['corpus_pages']} |",
        f"| Elegibles por estado para recuperación vigente | {summary['retrieval_eligible_pages']} ({_pct(int(summary['retrieval_eligible_pages']), total)}) |",
        f"| Con fuente referenciada | {summary['pages_with_sources']} ({_pct(int(summary['pages_with_sources']), total)}) |",
        f"| Con instrumento referenciado | {summary['pages_with_instruments']} ({_pct(int(summary['pages_with_instruments']), total)}) |",
        f"| Revisión jurídica `reviewed` | {summary['legally_reviewed_pages']} ({_pct(int(summary['legally_reviewed_pages']), total)}) |",
        f"| Requieren atención | {summary['pages_needing_attention']} |",
        f"| Fuentes distintas referenciadas | {summary['distinct_source_ids']} |",
        f"| Instrumentos distintos referenciados | {summary['distinct_instrument_ids']} |",
        "",
        "## Cobertura por sección",
        "",
        "| Sección | Total | Elegibles | Reviewed | Atención |",
        "|---|---:|---:|---:|---:|",
    ]
    for section in report["sections"]:
        lines.append(
            f"| `{section['section']}` | {section['total_pages']} | {section['retrieval_eligible_pages']} | {section['legally_reviewed_pages']} | {section['pages_needing_attention']} |"
        )

    lines.extend(["", "## Estados", ""])
    for field, counts in report["status_counts"].items():
        lines.extend([f"### `{field}`", "", "| Estado | Páginas |", "|---|---:|"])
        for value, count in counts.items():
            lines.append(f"| `{value}` | {count} |")
        lines.append("")

    risks = [page for page in report["pages"] if page["risk_reasons"]]
    lines.extend(["## Cola de atención", ""])
    if not risks:
        lines.append("No hay páginas con señales de atención según la política de gobernanza actual.")
    else:
        lines.append("Estas señales describen estado editorial/provenance. No equivalen por sí mismas a una conclusión jurídica incorrecta.")
        lines.append("")
        lines.extend(["| Página | Sección | Señales |", "|---|---|---|"])
        for page in risks:
            reasons = ", ".join(f"`{reason}`" for reason in page["risk_reasons"])
            lines.append(f"| `{page['path']}` | `{page['section']}` | {reasons} |")

    lines.extend(
        [
            "",
            "## Cómo se calcula",
            "",
            "Una página es elegible por estado para recuperación vigente cuando `source_status=current`, `legal_review_status=reviewed` y `corpus_status` es `current` o `not_applicable`. El JSON canónico está en `reports/corpus-coverage.json` y los límites de regresión están en `coverage-policy.yaml`.",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def evaluate_policy(report: dict[str, object], policy: dict[str, object]) -> tuple[str, ...]:
    findings: list[str] = []
    if policy.get("policy_version") != 1:
        findings.append("coverage policy requires policy_version: 1")
    summary = report.get("summary")
    if not isinstance(summary, dict):
        return tuple(findings + ["coverage report has no summary mapping"])

    for group, comparator in (("minimums", "minimum"), ("maximums", "maximum")):
        rules = policy.get(group, {})
        if not isinstance(rules, dict):
            findings.append(f"coverage policy {group} must be a mapping")
            continue
        for metric, threshold in sorted(rules.items()):
            current = summary.get(metric)
            if not isinstance(threshold, int) or not isinstance(current, int):
                findings.append(f"coverage policy metric {metric} must compare integers")
                continue
            if comparator == "minimum" and current < threshold:
                findings.append(f"minimum regression: {metric}={current} < {threshold}")
            if comparator == "maximum" and current > threshold:
                findings.append(f"maximum regression: {metric}={current} > {threshold}")
    return tuple(findings)


def _load_policy(root: Path) -> dict[str, object]:
    path = root / _POLICY_PATH
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected policy mapping")
    return data


def write_outputs(root: Path) -> dict[str, object]:
    report = build_report(root)
    json_path = root / _JSON_OUTPUT
    markdown_path = root / _MARKDOWN_OUTPUT
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(render_json(report), encoding="utf-8")
    markdown_path.write_text(render_markdown(report), encoding="utf-8")
    return report


def _summary_line(report: dict[str, object]) -> str:
    summary = report["summary"]
    return (
        "coverage: "
        f"total={summary['total_pages']} "
        f"eligible={summary['retrieval_eligible_pages']} "
        f"reviewed={summary['legally_reviewed_pages']} "
        f"pending={summary['pending_legal_review_pages']} "
        f"non_current={summary['non_current_corpus_pages']} "
        f"attention={summary['pages_needing_attention']} "
        f"sourced={summary['pages_with_sources']} "
        f"instrumented={summary['pages_with_instruments']} "
        f"unknown_source={summary['unknown_source_status_pages']}"
    )


def run_check(root: Path) -> CheckResult:
    metadata_findings = validate_page_metadata(root)
    if metadata_findings:
        detail = "; ".join(
            f"{finding.code} {finding.path}: {finding.message}"
            for finding in metadata_findings[:5]
        )
        return CheckResult(1, f"page metadata invalid: {detail}")

    try:
        report = build_report(root)
    except (OSError, UnicodeError, yaml.YAMLError, ValueError) as exc:
        return CheckResult(1, f"coverage report invalid: {exc}")
    summary = _summary_line(report)

    try:
        policy = _load_policy(root)
    except (OSError, UnicodeError, yaml.YAMLError, ValueError) as exc:
        return CheckResult(1, summary + f"\ncoverage configuration invalid: {exc}")

    findings = list(evaluate_policy(report, policy))
    expected = {
        _JSON_OUTPUT: render_json(report),
        _MARKDOWN_OUTPUT: render_markdown(report),
    }
    for relative_path, expected_text in expected.items():
        path = root / relative_path
        try:
            actual = path.read_text(encoding="utf-8")
        except OSError:
            actual = ""
        if actual != expected_text:
            findings.append(f"generated drift: {relative_path.as_posix()}")

    if findings:
        return CheckResult(1, summary + "\n" + "\n".join(sorted(findings)))
    return CheckResult(0, summary + "\ncoverage policy and generated outputs are current")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)

    if args.check:
        result = run_check(args.root)
        print(result.message)
        return result.exit_code

    report = write_outputs(args.root)
    print(_summary_line(report))
    print(f"wrote {_JSON_OUTPUT.as_posix()} and {_MARKDOWN_OUTPUT.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())