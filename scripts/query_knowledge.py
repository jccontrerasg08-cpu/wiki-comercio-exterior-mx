"""Query governed local evidence with an explicit temporal cutoff."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import date
import json
from pathlib import Path

import yaml

from scripts.rag_eval import documents_from_repository, rank_documents


@dataclass(frozen=True, slots=True)
class KnowledgeHit:
    source_id: str
    title: str
    score: float
    effective_from: str
    effective_to: str | None
    url: str


def _source_urls(root: Path) -> dict[str, str]:
    data = yaml.safe_load((root / "sources" / "registry.yaml").read_text(encoding="utf-8"))
    return {
        str(item["id"]): str(item.get("url", ""))
        for item in data.get("sources", [])
        if isinstance(item, dict) and item.get("id")
    }


def search_repository(
    root: Path,
    query: str,
    cutoff: date,
    k: int = 5,
) -> tuple[KnowledgeHit, ...]:
    """Return source-backed hits using the repository's existing temporal ranker."""

    urls = _source_urls(root)
    ranked = rank_documents(query, documents_from_repository(root), cutoff, k)
    return tuple(
        KnowledgeHit(
            source_id=item.source_id,
            title=item.title,
            score=item.score,
            effective_from=item.effective_from,
            effective_to=item.effective_to,
            url=urls.get(item.source_id, ""),
        )
        for item in ranked
    )


def _cutoff(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("cutoff must use YYYY-MM-DD") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="Lexical query over governed repository evidence")
    parser.add_argument("--cutoff", required=True, type=_cutoff, help="Temporal cutoff YYYY-MM-DD")
    parser.add_argument("--k", type=int, default=5, help="Maximum number of hits")
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    if args.k < 1:
        parser.error("--k must be at least 1")

    hits = search_repository(args.root, args.query, args.cutoff, args.k)
    if args.as_json:
        print(json.dumps([asdict(item) for item in hits], ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    if not hits:
        print("No hay evidencia gobernada pertinente para ese corte; requiere revisión humana.")
        return 0
    for index, hit in enumerate(hits, start=1):
        interval = hit.effective_from
        if hit.effective_to:
            interval += f" a {hit.effective_to}"
        print(f"{index}. {hit.title}")
        print(f"   source_id: {hit.source_id}")
        print(f"   vigencia indexada: {interval}")
        print(f"   score: {hit.score:.4f}")
        print(f"   fuente: {hit.url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
