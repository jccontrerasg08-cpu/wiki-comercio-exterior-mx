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


def _instrument_index(root: Path) -> dict[str, dict[str, Any]]:
    data = _load_yaml(root / "sources" / "instruments.yaml")
    return {
        str(item["id"]): item
        for item in data.get("instruments", [])
        if isinstance(item, dict) and item.get("id")
    }


def build_index(root: Path) -> list[dict[str, object]]:
    """Build stable wiki records from canonical repository metadata."""

    metadata = _load_yaml(root / "sources" / "page_metadata.yaml")
    registry = _load_yaml(root / "sources" / "registry.yaml")
    instruments = _instrument_index(root)
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
        instrument_ids = sorted(str(item) for item in page.get("instrument_ids", []))
        unknown_instruments = [item for item in instrument_ids if item not in instruments]
        if unknown_instruments:
            raise ValueError(
                f"{path}: unknown instrument_ids: {', '.join(unknown_instruments)}"
            )
        records.append(
            {
                "path": path,
                "title": _text(page.get("title")),
                "topic": _text(page.get("topic")) or "sin-clasificar",
                "source_status": _text(page.get("source_status")),
                "legal_review_status": _text(page.get("legal_review_status")),
                "current_through": _text(page.get("current_through")),
                "instrument_ids": instrument_ids,
                "sources": sorted(sources, key=lambda item: item["id"]),
            }
        )
    return sorted(records, key=lambda item: (str(item["topic"]), str(item["title"]), str(item["path"])))


def build_machine_index(root: Path) -> dict[str, object]:
    """Normalize page, source, and instrument nodes for lightweight consumers."""

    records = build_index(root)
    instruments = _instrument_index(root)
    pages: list[dict[str, object]] = []
    source_catalog: dict[str, dict[str, str]] = {}
    used_instruments: set[str] = set()

    for record in records:
        source_ids: list[str] = []
        for source in record["sources"]:
            source_id = str(source["id"])
            source_ids.append(source_id)
            source_catalog[source_id] = {
                "authority": str(source["authority"]),
                "title": str(source["title"]),
                "url": str(source["url"]),
            }
        instrument_ids = [str(item) for item in record["instrument_ids"]]
        used_instruments.update(instrument_ids)
        pages.append(
            {
                "path": record["path"],
                "title": record["title"],
                "topic": record["topic"],
                "source_status": record["source_status"],
                "legal_review_status": record["legal_review_status"],
                "current_through": record["current_through"],
                "instrument_ids": instrument_ids,
                "source_ids": source_ids,
            }
        )

    instrument_catalog = {
        instrument_id: {
            "title": _text(instruments[instrument_id].get("title")),
            "status": _text(instruments[instrument_id].get("status")),
            "current_through": _text(instruments[instrument_id].get("current_through")),
        }
        for instrument_id in sorted(used_instruments)
    }
    return {
        "schema_version": 1,
        "pages": pages,
        "sources": {key: source_catalog[key] for key in sorted(source_catalog)},
        "instruments": instrument_catalog,
    }


def _escape(value: object) -> str:
    return _text(value).replace("|", "\\|").replace("\n", " ")


def _page_link(path: str) -> str:
    relative = path.removeprefix("docs/")
    return "../" + relative


def render_knowledge_map(root: Path) -> str:
    """Render a compact deterministic Markdown knowledge map from the index."""

    records = build_index(root)
    instruments = _instrument_index(root)
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
        "Esta vista se genera desde `sources/page_metadata.yaml`, `sources/registry.yaml` y `sources/instruments.yaml`. Los estados describen **metadatos de revisión del repositorio**, no una opinión jurídica independiente ni sustituyen la fuente oficial.",
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
                "| Página | Estado | Vigente hasta | Instrumentos | Fuentes |",
                "|---|---|---|---|---|",
            ]
        )
        for record in by_topic[topic]:
            title = _escape(record["title"] or record["path"])
            page = f"[{title}]({_page_link(str(record['path']))})"
            state = " · ".join(
                item
                for item in (
                    _escape(record["source_status"]),
                    _escape(record["legal_review_status"]),
                )
                if item
            ) or "—"
            instrument_ids = ", ".join(
                f"`{_escape(item)}`" for item in record["instrument_ids"]
            ) or "—"
            source_ids = ", ".join(
                f"`{_escape(source['id'])}`" for source in record["sources"]
            ) or "—"
            lines.append(
                "| "
                + " | ".join(
                    (
                        page,
                        state,
                        _escape(record["current_through"]) or "—",
                        instrument_ids,
                        source_ids,
                    )
                )
                + " |"
            )
        lines.append("")

    lines.extend(["## Conexiones por instrumento", ""])
    if not by_instrument:
        lines.append("No hay instrumentos enlazados en los metadatos gobernados.")
    else:
        lines.extend(
            [
                "| Instrumento | Estado | Vigente hasta | Páginas relacionadas |",
                "|---|---|---|---|",
            ]
        )
        for instrument_id in sorted(by_instrument):
            instrument = instruments[instrument_id]
            title = _escape(instrument.get("title") or instrument_id)
            pages = ", ".join(
                f"[{_escape(record['title'])}]({_page_link(str(record['path']))})"
                for record in sorted(by_instrument[instrument_id], key=lambda item: str(item["title"]))
            )
            lines.append(
                "| "
                + " | ".join(
                    (
                        f"{title} (`{_escape(instrument_id)}`)",
                        _escape(instrument.get("status")) or "—",
                        _escape(instrument.get("current_through")) or "—",
                        pages,
                    )
                )
                + " |"
            )
    lines.extend(
        [
            "",
            "## Uso por herramientas",
            "",
            "El detalle normalizado, incluidas autoridades y URLs oficiales, está en [`knowledge-index.json`](../assets/data/knowledge-index.json). Un consumidor puede usarlo para navegación o para preparar contexto, pero las respuestas sobre vigencia deben seguir pasando por los gates temporales y de revisión del repositorio.",
            "",
        ]
    )
    return "\n".join(lines)


def render_knowledge_json(root: Path) -> str:
    """Render a compact normalized machine index."""

    return json.dumps(
        build_machine_index(root),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ) + "\n"


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
        root / JSON_PATH: render_knowledge_json(root),
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
