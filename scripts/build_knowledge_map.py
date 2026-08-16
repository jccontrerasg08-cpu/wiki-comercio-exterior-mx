"""Generate deterministic human and machine views of governed wiki metadata."""

from __future__ import annotations

import argparse
from collections import defaultdict
import difflib
import json
from pathlib import Path
from typing import Any

import yaml


MARKDOWN_PATH = Path("docs/explore/knowledge-map.md")
JSON_PATH = Path("docs/assets/data/knowledge-index.json")


def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a mapping")
    return data


def _text(value: object) -> str:
    return "" if value is None else str(value)


def build_index(root: Path) -> list[dict[str, object]]:
    """Build stable wiki records from canonical repository metadata."""

    metadata = _load_yaml(root / "sources" / "page_metadata.yaml")
    registry = _load_yaml(root / "sources" / "registry.yaml")
    source_by_id = {
        str(item["id"]): item
        for item in registry.get("sources", [])
        if isinstance(item, dict) and item.get("id")
    }
    records: list[dict[str, object]] = []
    for page in metadata.get("pages", []):
        if not isinstance(page, dict):
            continue
        path = _text(page.get("path"))
        if not path.startswith("docs/wiki/") or page.get("content_type") != "wiki_explainer":
            continue
        sources: list[dict[str, str]] = []
        for raw_id in page.get("source_ids", []):
            source_id = str(raw_id)
            source = source_by_id.get(source_id, {})
            sources.append(
                {
                    "id": source_id,
                    "title": _text(source.get("title")),
                    "authority": _text(source.get("authority")),
                    "url": _text(source.get("url")),
                }
            )
        records.append(
            {
                "path": path,
                "title": _text(page.get("title")),
                "topic": _text(page.get("topic")) or "sin-clasificar",
                "source_status": _text(page.get("source_status")),
                "legal_review_status": _text(page.get("legal_review_status")),
                "current_through": _text(page.get("current_through")),
                "instrument_ids": sorted(str(item) for item in page.get("instrument_ids", [])),
                "sources": sorted(sources, key=lambda item: item["id"]),
            }
        )
    return sorted(records, key=lambda item: (str(item["topic"]), str(item["title"]), str(item["path"])))


def _escape(value: object) -> str:
    return _text(value).replace("|", "\\|").replace("\n", " ")


def _page_link(path: str) -> str:
    relative = path.removeprefix("docs/")
    return "../" + relative


def render_knowledge_map(root: Path) -> str:
    """Render a deterministic Markdown knowledge map from the index."""

    records = build_index(root)
    by_topic: dict[str, list[dict[str, object]]] = defaultdict(list)
    by_instrument: dict[str, list[dict[str, object]]] = defaultdict(list)
    for record in records:
        by_topic[str(record["topic"])].append(record)
        for instrument_id in record["instrument_ids"]:
            by_instrument[str(instrument_id)].append(record)

    lines = [
        "---",
        'title: "Mapa de conocimiento"',
        'description: "Vista generada de páginas, fuentes, instrumentos y estado de revisión del conocimiento gobernado."',
        "---",
        "",
        "# Mapa de conocimiento",
        "",
        "Esta vista se genera desde `sources/page_metadata.yaml`, `sources/registry.yaml` y `sources/instruments.yaml`. Los estados que aparecen aquí describen **metadatos de revisión del repositorio**, no una opinión jurídica independiente ni sustituyen la fuente oficial.",
        "",
        f"**Páginas gobernadas visibles:** {len(records)}",
        "",
        "## Por tema",
        "",
    ]
    for topic in sorted(by_topic, key=str.casefold):
        lines.extend(
            [
                f"### {topic}",
                "",
                "| Página | Fuente | Revisión | Vigente hasta | Instrumentos | Fuentes oficiales |",
                "|---|---|---|---|---|---|",
            ]
        )
        for record in by_topic[topic]:
            title = _escape(record["title"] or record["path"])
            page = f"[{title}]({_page_link(str(record['path']))})"
            instruments = ", ".join(f"`{_escape(item)}`" for item in record["instrument_ids"]) or "—"
            source_links = []
            for source in record["sources"]:
                source_id = _escape(source["id"])
                url = _text(source["url"])
                source_links.append(f"[`{source_id}`]({url})" if url else f"`{source_id}`")
            lines.append(
                "| "
                + " | ".join(
                    (
                        page,
                        _escape(record["source_status"]) or "—",
                        _escape(record["legal_review_status"]) or "—",
                        _escape(record["current_through"]) or "—",
                        instruments,
                        ", ".join(source_links) or "—",
                    )
                )
                + " |"
            )
        lines.append("")

    lines.extend(["## Conexiones por instrumento", ""])
    if not by_instrument:
        lines.append("No hay instrumentos enlazados en los metadatos gobernados.")
    else:
        lines.extend(["| Instrumento | Páginas relacionadas |", "|---|---|"])
        for instrument_id in sorted(by_instrument):
            pages = ", ".join(
                f"[{_escape(record['title'])}]({_page_link(str(record['path']))})"
                for record in sorted(by_instrument[instrument_id], key=lambda item: str(item["title"]))
            )
            lines.append(f"| `{_escape(instrument_id)}` | {pages} |")
    lines.extend(
        [
            "",
            "## Uso por herramientas",
            "",
            "La vista equivalente para máquinas está en [`knowledge-index.json`](../assets/data/knowledge-index.json). Un consumidor puede usarla para navegación o para preparar contexto, pero las respuestas sobre vigencia deben seguir pasando por los gates temporales y de revisión del repositorio.",
            "",
        ]
    )
    return "\n".join(lines)


def _json_text(root: Path) -> str:
    return json.dumps(build_index(root), ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _diff(path: Path, actual: str, expected: str) -> str:
    return "".join(
        difflib.unified_diff(
            actual.splitlines(keepends=True),
            expected.splitlines(keepends=True),
            fromfile=str(path),
            tofile=f"generated:{path}",
        )
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    expected = {
        root / MARKDOWN_PATH: render_knowledge_map(root),
        root / JSON_PATH: _json_text(root),
    }
    if args.check:
        drift = False
        for path, content in expected.items():
            actual = path.read_text(encoding="utf-8") if path.is_file() else ""
            if actual != content:
                drift = True
                print(_diff(path.relative_to(root), actual, content), end="")
        if drift:
            return 1
        print("Knowledge map is up to date")
        return 0
    for path, content in expected.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"wrote {path.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
