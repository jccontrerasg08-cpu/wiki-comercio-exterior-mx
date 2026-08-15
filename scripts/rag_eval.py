"""Dependency-free lexical and temporal retrieval evaluation."""

from __future__ import annotations

import argparse
import json
import unicodedata
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

import yaml

from scripts.temporal_graph import load_instruments


_STOPWORDS = frozenset(
    {"a", "al", "de", "del", "el", "en", "la", "las", "los", "para", "por", "que", "un", "una", "y"}
)


@dataclass(frozen=True, slots=True)
class RankedDocument:
    source_id: str
    score: float
    title: str
    effective_from: str
    effective_to: str | None


@dataclass(frozen=True, slots=True)
class EvaluationReport:
    recall_at_k: float
    mean_reciprocal_rank: float
    temporal_accuracy: float
    citation_coverage: float
    failures: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RetrievalResult:
    ranked: tuple[RankedDocument, ...]
    cited_source_ids: tuple[str, ...]
    disclaimer: str


_ABSTENTION_DISCLAIMER = (
    "No hay evidencia oficial pertinente para el corte solicitado; "
    "no hay una manifestacion historica versionada cuando la fuente "
    "consolidada actual queda fuera del intervalo. Requiere revision humana."
)


def tokenize(text: str) -> frozenset[str]:
    """Normalize Spanish accents and return checked alphanumeric terms."""

    normalized = unicodedata.normalize("NFKD", text)
    plain = "".join(char for char in normalized if not unicodedata.combining(char)).casefold()
    terms: list[str] = []
    current: list[str] = []
    for char in plain:
        if char.isalnum():
            current.append(char)
        elif current:
            terms.append("".join(current))
            current = []
    if current:
        terms.append("".join(current))
    return frozenset(term for term in terms if term not in _STOPWORDS and len(term) > 1)


def _iso_date(value: object) -> date:
    return date.fromisoformat(str(value))


def _page_is_currently_retrievable(page: dict) -> bool:
    """Gate current-answer text on explicit review and freshness metadata."""

    if page.get("legal_review_status") != "reviewed":
        return False
    if page.get("source_status") != "current":
        return False
    return page.get("corpus_status") in {None, "current", "not_applicable"}


def rank_documents(
    query: str, documents: list[dict], cutoff: date, k: int
) -> tuple[RankedDocument, ...]:
    """Rank eligible sources by stable lexical overlap."""

    query_terms = tokenize(query)
    ranked: list[RankedDocument] = []
    for document in documents:
        start = _iso_date(document.get("effective_from", "0001-01-01"))
        end_value = document.get("effective_to")
        end = _iso_date(end_value) if end_value else None
        if start > cutoff or (end is not None and cutoff > end):
            continue
        body_terms = tokenize(f"{document.get('title', '')} {document.get('text', '')}")
        title_terms = tokenize(str(document.get("title", "")))
        union = query_terms | body_terms
        jaccard = len(query_terms & body_terms) / len(union) if union else 0.0
        title_overlap = len(query_terms & title_terms) / len(query_terms) if query_terms else 0.0
        score = jaccard + title_overlap
        if score < 0.05:
            continue
        ranked.append(
            RankedDocument(
                source_id=str(document["source_id"]),
                score=score,
                title=str(document.get("title", "")),
                effective_from=start.isoformat(),
                effective_to=end.isoformat() if end else None,
            )
        )
    ranked.sort(key=lambda item: (-item.score, item.source_id))
    return tuple(ranked[:k])


def retrieve_case(case: dict, documents: list[dict], k: int = 5) -> RetrievalResult:
    """Produce the concrete retrieval output evaluated by the offline suite."""

    ranked = rank_documents(
        str(case["query"]),
        documents,
        _iso_date(case["cutoff"]),
        k,
    )
    citations = tuple(item.source_id for item in ranked)
    return RetrievalResult(
        ranked=ranked,
        cited_source_ids=citations,
        disclaimer="" if citations else _ABSTENTION_DISCLAIMER,
    )


def evaluate_cases(
    cases: list[dict], documents: list[dict], k: int = 5
) -> EvaluationReport:
    """Evaluate hand-checked source expectations and temporal eligibility."""

    recalls: list[float] = []
    reciprocal_ranks: list[float] = []
    temporal: list[float] = []
    coverage: list[float] = []
    failures: list[str] = []
    for case in cases:
        cutoff = _iso_date(case["cutoff"])
        expected = tuple(case.get("expected_source_ids", []))
        forbidden = set(case.get("forbidden_source_ids", []))
        result = retrieve_case(case, documents, k)
        ranked = result.ranked
        ranked_ids = [item.source_id for item in ranked]
        cited_ids = list(result.cited_source_ids)
        case_id = str(case.get("id", "case"))
        if expected:
            found = [source_id for source_id in expected if source_id in ranked_ids]
            recall = len(found) / len(expected)
            first_positions = [ranked_ids.index(source_id) + 1 for source_id in found]
            reciprocal = 1 / min(first_positions) if first_positions else 0.0
            cited_expected = [source_id for source_id in expected if source_id in cited_ids]
            citation = len(cited_expected) / len(expected)
        else:
            recall = 1.0 if not ranked else 0.0
            reciprocal = recall
            citation = 1.0 if not cited_ids else 0.0
        forbidden_ranked = sorted(forbidden.intersection(ranked_ids))
        eligible = not forbidden_ranked and all(
            _iso_date(item.effective_from) <= cutoff
            and (item.effective_to is None or cutoff <= _iso_date(item.effective_to))
            for item in ranked
        )
        recalls.append(recall)
        reciprocal_ranks.append(reciprocal)
        temporal.append(1.0 if eligible else 0.0)
        coverage.append(citation)
        if recall < 1.0:
            failures.append(f"{case_id}: expected {list(expected)}, ranked {ranked_ids}")
        if forbidden_ranked:
            failures.append(f"{case_id}: forbidden sources ranked {forbidden_ranked}")
        required_disclaimer = str(case.get("required_disclaimer", "")).strip()
        if required_disclaimer and required_disclaimer.casefold() not in result.disclaimer.casefold():
            coverage[-1] = 0.0
            failures.append(f"{case_id}: required disclaimer missing")
    divisor = len(cases) or 1
    return EvaluationReport(
        recall_at_k=sum(recalls) / divisor,
        mean_reciprocal_rank=sum(reciprocal_ranks) / divisor,
        temporal_accuracy=sum(temporal) / divisor,
        citation_coverage=sum(coverage) / divisor,
        failures=tuple(failures),
    )


def documents_from_repository(root: Path) -> list[dict]:
    registry = yaml.safe_load((root / "sources" / "registry.yaml").read_text(encoding="utf-8"))
    sources = {item["id"]: item for item in registry["sources"]}
    metadata = yaml.safe_load((root / "sources" / "page_metadata.yaml").read_text(encoding="utf-8"))
    governed_text: dict[str, list[str]] = {}
    for page in metadata.get("pages", []):
        if not isinstance(page, dict) or not _page_is_currently_retrievable(page):
            continue
        path = root / str(page.get("path", ""))
        if not path.is_file() or path.suffix != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        for source_id in page.get("source_ids", []):
            governed_text.setdefault(str(source_id), []).append(text)

    by_source: dict[str, dict] = {}
    for instrument in load_instruments(root / "sources" / "instruments.yaml"):
        consolidated_source = sources[instrument["consolidated_source_id"]]
        consolidated_start = (
            consolidated_source.get("content_valid_from")
            if consolidated_source.get("evidence_class") == "official_consolidated"
            else instrument["effective_from"]
        )
        source_ids = [
            (
                instrument["consolidated_source_id"],
                consolidated_start,
                consolidated_source.get("content_valid_to") or instrument["effective_to"],
            )
        ]
        source_ids.extend(
            (event["source_id"], event["effective_from"], event.get("effective_to"))
            for event in instrument.get("events", [])
        )
        for source_id, start, end in source_ids:
            source = sources[source_id]
            if not start:
                continue
            body = "\n\n".join(governed_text.get(source_id, []))
            by_source[source_id] = {
                "source_id": source_id,
                "title": source["title"],
                "text": body or f"{instrument['title']} {instrument['instrument_type']} {source.get('authority', '')}",
                "effective_from": str(start),
                "effective_to": str(end) if end else None,
            }
    return list(by_source.values())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--k", type=int, default=5)
    args = parser.parse_args(argv)
    cases_data = yaml.safe_load((args.root / "evals" / "questions.yaml").read_text(encoding="utf-8"))
    report = evaluate_cases(cases_data["cases"], documents_from_repository(args.root), args.k)
    print(json.dumps(asdict(report), ensure_ascii=False, indent=2, sort_keys=True))
    return 1 if args.check and (report.recall_at_k < 1.0 or report.temporal_accuracy < 1.0 or report.citation_coverage < 1.0) else 0


if __name__ == "__main__":
    raise SystemExit(main())
