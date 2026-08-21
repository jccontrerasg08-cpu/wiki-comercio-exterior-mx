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
_RELEASE_TAG_RE = re.compile(r"^data-\d{4}\.\d{2}\.\d{2}$")
_ALLOWED_FALLBACKS = {"text_links", "none"}
_CONTRACT_TYPES = {"geospatial", "release_bundle", "monitor_state"}
_RELEASE_ASSETS = {
    "arancel_mx.duckdb",
    "arancel_mx.csv",
    "arancel_mx.json",
    "manifest.json",
    "SHA256SUMS",
    "official-sources.tar.gz",
}


def _safe_repo_path(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts


def _validate_consumption(consumption: object, prefix: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(consumption, dict):
        return [f"{prefix}.consumption must be a mapping"]

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
            errors.append(f"{prefix}.consumption.public_artifact must use https when configured")
        checksum = consumption.get("sha256")
        if not isinstance(checksum, str) or not re.fullmatch(r"[0-9a-f]{64}", checksum):
            errors.append(f"{prefix}.consumption.sha256 is required for a public_artifact")

    return errors


def _validate_geospatial(dataset: dict[str, Any], prefix: str) -> list[str]:
    errors: list[str] = []
    srid = dataset.get("srid")
    if not isinstance(srid, int) or isinstance(srid, bool) or srid <= 0:
        errors.append(f"{prefix}.srid must be a positive integer")

    geometry_type = dataset.get("geometry_type")
    if not isinstance(geometry_type, str) or not geometry_type.strip():
        errors.append(f"{prefix}.geometry_type is required")
    return errors


def _validate_release_bundle(dataset: dict[str, Any], prefix: str) -> list[str]:
    errors: list[str] = []
    release = dataset.get("release")
    if not isinstance(release, dict):
        return [f"{prefix}.release must be a mapping"]

    tag = release.get("tag")
    if not isinstance(tag, str) or not _RELEASE_TAG_RE.fullmatch(tag):
        errors.append(f"{prefix}.release.tag must use data-YYYY.MM.DD")

    target = release.get("target_commit")
    if not isinstance(target, str) or not _COMMIT_RE.fullmatch(target):
        errors.append(f"{prefix}.release.target_commit must be a lowercase 40-hex commit SHA")

    url = release.get("release_url")
    if not isinstance(url, str) or not url.startswith("https://github.com/"):
        errors.append(f"{prefix}.release.release_url must use GitHub https")

    if release.get("manifest_schema_version") != 2:
        errors.append(f"{prefix}.release.manifest_schema_version must equal 2")

    assets = release.get("assets")
    if not isinstance(assets, list) or set(assets) != _RELEASE_ASSETS or len(assets) != len(_RELEASE_ASSETS):
        errors.append(f"{prefix}.release.assets must declare the six verified release assets")
    return errors


def _validate_monitor_state(dataset: dict[str, Any], prefix: str) -> list[str]:
    errors: list[str] = []
    monitor = dataset.get("monitor")
    if not isinstance(monitor, dict):
        return [f"{prefix}.monitor must be a mapping"]

    if monitor.get("state_version") != 1:
        errors.append(f"{prefix}.monitor.state_version must equal 1")
    if monitor.get("source_primary") != "official_publication_url":
        errors.append(f"{prefix}.monitor.source_primary must equal official_publication_url")
    if monitor.get("review_rule") != "human_review_required":
        errors.append(f"{prefix}.monitor.review_rule must require human review")
    if monitor.get("interpretation_limit") != "detected_change_is_not_legal_currentness":
        errors.append(f"{prefix}.monitor.interpretation_limit must preserve the legal-currentness limit")
    return errors


def validate_contract(data: Any, root: Path) -> list[str]:
    """Return deterministic contract validation errors without network access."""

    errors: list[str] = []
    if not isinstance(data, dict):
        return ["contract must be a mapping"]

    if data.get("contract_version") != 1:
        errors.append("contract_version must equal 1")

    contract_type = data.get("contract_type", "geospatial")
    if contract_type not in _CONTRACT_TYPES:
        errors.append(f"contract_type must be one of {sorted(_CONTRACT_TYPES)}")

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
            errors.append(f"{prefix}.wiki_local_copy is forbidden for data canonical in {repository}")

        errors.extend(_validate_consumption(dataset.get("consumption"), prefix))
        if contract_type == "geospatial":
            errors.extend(_validate_geospatial(dataset, prefix))
        elif contract_type == "release_bundle":
            errors.extend(_validate_release_bundle(dataset, prefix))
        elif contract_type == "monitor_state":
            errors.extend(_validate_monitor_state(dataset, prefix))

    if contract_type == "geospatial" and isinstance(repository, str) and repository != "jccontrerasg08-cpu/wiki-comercio-exterior-mx":
        vendored = [path for path in root.rglob("*.geojson") if ".git" not in path.parts]
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
    contract_dir = args.root / "data" / "contracts"
    contracts = sorted(contract_dir.glob("*.yaml"))
    if not contracts:
        print(f"ERROR: no data contracts found: {contract_dir}")
        return 1

    errors: list[str] = []
    validated_contracts = 0
    for contract in contracts:
        data = yaml.safe_load(contract.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or (
            "canonical_repository" not in data and "contract_type" not in data
        ):
            continue
        validated_contracts += 1
        errors.extend(f"{contract.name}: {error}" for error in validate_contract(data, args.root))
    if not validated_contracts:
        print(f"ERROR: no external integration contracts found: {contract_dir}")
        return 1
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("data contracts: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
