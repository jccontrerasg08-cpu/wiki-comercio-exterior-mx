"""Validate the governed RGCE 2026 annex editorial manifest and corpus metadata."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


EXPECTED_ANNEXES = tuple(range(1, 31))
EXPECTED_MODIFIED = {5, 22, 29}
MOD_SOURCE_ID = "mx_sidof_rgce_2026_mod1_anexos"
REVIEWED_THROUGH = "2026-05-20"
COMPOSITES = (
    "data/corpus/anexos-formatos-tramites.md",
    "data/corpus/anexos-riesgo-logistica.md",
)


@dataclass(frozen=True, slots=True)
class ValidationResult:
    findings: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.findings


def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected mapping")
    return data


def _as_date(value: object) -> str:
    return str(value) if value is not None else ""


def validate(root: Path) -> ValidationResult:
    findings: list[str] = []
    manifest_path = root / "sources" / "rgce_2026_annexes.yaml"
    registry_path = root / "sources" / "registry.yaml"
    metadata_path = root / "sources" / "page_metadata.yaml"

    if not manifest_path.is_file():
        return ValidationResult(("missing sources/rgce_2026_annexes.yaml",))

    manifest = _load_yaml(manifest_path)
    annexes = manifest.get("annexes")
    if not isinstance(annexes, list):
        return ValidationResult(("annex manifest must contain an annexes list",))

    numbers = [item.get("annex") for item in annexes if isinstance(item, dict)]
    if numbers != list(EXPECTED_ANNEXES):
        findings.append(f"annex coverage must be exactly 1..30; got {numbers}")

    titles = [str(item.get("title", "")) for item in annexes if isinstance(item, dict)]
    if len(set(titles)) != len(titles) or any(not title for title in titles):
        findings.append("annex titles must be non-empty and unique")

    paths = [str(item.get("corpus_path", "")) for item in annexes if isinstance(item, dict)]
    if len(set(paths)) != len(paths) or any(not path for path in paths):
        findings.append("annex corpus paths must be non-empty and unique")

    registry = _load_yaml(registry_path)
    source_ids = {
        str(item.get("id"))
        for item in registry.get("sources", [])
        if isinstance(item, dict) and item.get("id")
    }

    modified: set[int] = set()
    for item in annexes:
        if not isinstance(item, dict):
            findings.append("annex entries must be mappings")
            continue
        annex = item.get("annex")
        source_id = item.get("publication_source_id")
        if source_id not in source_ids:
            findings.append(f"annex {annex}: unknown publication source {source_id}")
        modifications = item.get("modification_source_ids", [])
        if not isinstance(modifications, list):
            findings.append(f"annex {annex}: modification_source_ids must be a list")
            modifications = []
        for mod_source_id in modifications:
            if mod_source_id not in source_ids:
                findings.append(f"annex {annex}: unknown modification source {mod_source_id}")
        if MOD_SOURCE_ID in modifications and isinstance(annex, int):
            modified.add(annex)
        if _as_date(item.get("reviewed_through")) != REVIEWED_THROUGH:
            findings.append(f"annex {annex}: reviewed_through must be {REVIEWED_THROUGH}")
        corpus_path = item.get("corpus_path")
        if not isinstance(corpus_path, str) or not (root / corpus_path).is_file():
            findings.append(f"annex {annex}: missing corpus path {corpus_path}")

    if modified != EXPECTED_MODIFIED:
        findings.append(
            f"published first-modification annex set must be {sorted(EXPECTED_MODIFIED)}; got {sorted(modified)}"
        )

    metadata = _load_yaml(metadata_path)
    pages = {
        str(item.get("path")): item
        for item in metadata.get("pages", [])
        if isinstance(item, dict) and item.get("path")
    }
    governed_paths = tuple(paths) + COMPOSITES
    for path in governed_paths:
        page = pages.get(path)
        if page is None:
            findings.append(f"missing page metadata for {path}")
            continue
        expected = {
            "source_status": "current",
            "extraction_status": "partial",
            "legal_review_status": "reviewed",
            "corpus_status": "current",
            "current_through": REVIEWED_THROUGH,
        }
        for key, expected_value in expected.items():
            actual = _as_date(page.get(key)) if key == "current_through" else page.get(key)
            if actual != expected_value:
                findings.append(f"{path}: {key} must be {expected_value}; got {actual}")

    return ValidationResult(tuple(sorted(findings)))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument("--check", action="store_true", help="Validate and exit nonzero on findings")
    args = parser.parse_args(argv)

    result = validate(args.root)
    if result.ok:
        print("RGCE 2026 annex manifest and governed metadata passed")
        return 0
    for finding in result.findings:
        print(f"FAIL {finding}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
