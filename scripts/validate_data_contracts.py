"""Validate cross-repository data ownership and consumption contracts offline."""

from __future__ import annotations

import argparse
import re
from pathlib import Path, PurePosixPath
from typing import Any

import yaml


_REPO_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
_ID_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
_ALLOWED_FALLBACKS = {"text_links", "none"}


def _safe_repo_path(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts


def validate_contract(data: Any, root: Path) -> list[str]:
    """Return deterministic contract validation errors without network access."""

    errors: list[str] = []
    if not isinstance(data, dict):
        return ["contract must be a mapping"]

    if data.get("contract_version") != 1:
        errors.append("contract_version must equal 1")

    repository = data.get("canonical_repository")
    if not isinstance(repository, str) or not _REPO_RE.fullmatch(repository):
        errors.append("canonical_repository must use owner/name form")

    datasets = data.get("datasets")
    if not isinstance(datasets, list) or not datasets:
        errors.append("datasets must be a non-empty list")
        return errors

    seen_ids: set[str] = set()
    for index, dataset in enumerate(datasets):
        prefix = f"datasets[{index}]"
        if not isinstance(dataset, dict):
            errors.append(f"{prefix} must be a mapping")
            continue

        dataset_id = dataset.get("id")
        if not isinstance(dataset_id, str) or not _ID_RE.fullmatch(dataset_id):
            errors.append(f"{prefix}.id must be a stable snake_case identifier")
        elif dataset_id in seen_ids:
            errors.append(f"{prefix}.id duplicates {dataset_id}")
        else:
            seen_ids.add(dataset_id)

        for key in ("canonical_path", "generator_path"):
            if not _safe_repo_path(dataset.get(key)):
                errors.append(f"{prefix}.{key} must be a safe repository-relative path")

        observed_commit = dataset.get("observed_commit")
        if not isinstance(observed_commit, str) or not _COMMIT_RE.fullmatch(observed_commit):
            errors.append(f"{prefix}.observed_commit must be a lowercase 40-hex commit SHA")

        srid = dataset.get("srid")
        if not isinstance(srid, int) or isinstance(srid, bool) or srid <= 0:
            errors.append(f"{prefix}.srid must be a positive integer")

        geometry_type = dataset.get("geometry_type")
        if not isinstance(geometry_type, str) or not geometry_type.strip():
            errors.append(f"{prefix}.geometry_type is required")

        fields = dataset.get("schema_fields")
        if (
            not isinstance(fields, list)
            or not fields
            or not all(isinstance(field, str) and field.strip() for field in fields)
        ):
            errors.append(f"{prefix}.schema_fields must be a non-empty string list")
        elif len(fields) != len(set(fields)):
            errors.append(f"{prefix}.schema_fields must be unique")

        wiki_local_copy = dataset.get("wiki_local_copy")
        if wiki_local_copy not in (None, ""):
            errors.append(
                f"{prefix}.wiki_local_copy is forbidden for data canonical in {repository}"
            )

        consumption = dataset.get("consumption")
        if not isinstance(consumption, dict):
            errors.append(f"{prefix}.consumption must be a mapping")
            continue

        fallback = consumption.get("fallback")
        if fallback not in _ALLOWED_FALLBACKS:
            errors.append(
                f"{prefix}.consumption.fallback must be one of {sorted(_ALLOWED_FALLBACKS)}"
            )

        embed_ready = consumption.get("embed_ready")
        if not isinstance(embed_ready, bool):
            errors.append(f"{prefix}.consumption.embed_ready must be boolean")

        artifact = consumption.get("public_artifact")
        if artifact is not None and not isinstance(artifact, str):
            errors.append(f"{prefix}.consumption.public_artifact must be string or null")
        if artifact is None and embed_ready is True:
            errors.append(
                f"{prefix}.consumption.embed_ready cannot be true without a public_artifact"
            )

        if isinstance(artifact, str) and artifact:
            if not artifact.startswith("https://"):
                errors.append(
                    f"{prefix}.consumption.public_artifact must use https when configured"
                )
            checksum = consumption.get("sha256")
            if not isinstance(checksum, str) or not re.fullmatch(r"[0-9a-f]{64}", checksum):
                errors.append(
                    f"{prefix}.consumption.sha256 is required for a public_artifact"
                )

    # An externally canonical contract must not be implemented by silently vendoring GeoJSON.
    if isinstance(repository, str) and repository != "jccontrerasg08-cpu/wiki-comercio-exterior-mx":
        vendored = [
            path
            for path in root.rglob("*.geojson")
            if ".git" not in path.parts
        ]
        if vendored:
            errors.append(
                "wiki contains GeoJSON despite external canonical ownership: "
                + ", ".join(str(path.relative_to(root)) for path in vendored)
            )

    return sorted(dict.fromkeys(errors))


def validate_file(path: Path, root: Path) -> list[str]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return validate_contract(data, root)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    contract = args.root / "data" / "contracts" / "aduanamap.yaml"
    if not contract.is_file():
        print(f"ERROR: missing data contract: {contract}")
        return 1
    errors = validate_file(contract, args.root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("data contracts: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
