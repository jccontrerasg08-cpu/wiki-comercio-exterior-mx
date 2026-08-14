"""Offline integrity validation for wiki-comercio-exterior-mx."""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlparse

import yaml


@dataclass(frozen=True, slots=True)
class ValidationFinding:
    """One deterministic repository-integrity finding."""

    code: str
    path: str
    message: str


_REQUIRED_SOURCE_FIELDS = (
    "id",
    "jurisdiction",
    "title",
    "url",
    "authority",
    "evidence_class",
    "allowed_hosts",
    "media_types",
    "harvest",
)

_REQUIRED_DOCUMENT_FIELDS = (
    "id",
    "file",
    "url",
    "sha256",
    "bytes",
    "license",
    "redistribution",
)

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_CHECKSUM_LINE_RE = re.compile(r"^([0-9a-f]{64})  (.+)$")


def _load_yaml(path: Path) -> tuple[Any | None, list[ValidationFinding]]:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")), []
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        return None, [
            ValidationFinding("YAML_INVALID", str(path), f"cannot parse YAML: {exc}")
        ]


def _is_safe_relative_path(value: str) -> bool:
    path = PurePosixPath(value)
    return bool(value) and not path.is_absolute() and ".." not in path.parts


def _resolve_logical_document_path(fragment_parent: Path, file_name: str) -> str:
    """Normalize legacy manifest file paths to paths relative to originals/."""

    file_path = PurePosixPath(file_name)
    parent_path = PurePosixPath(fragment_parent.as_posix())
    parent_parts = () if parent_path.as_posix() == "." else parent_path.parts
    if parent_parts and file_path.parts[: len(parent_parts)] == parent_parts:
        return file_path.as_posix()
    return (parent_path / file_path).as_posix()


def validate_registry(path: Path) -> list[ValidationFinding]:
    """Validate the structural contract of the canonical source registry."""

    data, findings = _load_yaml(path)
    if findings:
        return findings
    if not isinstance(data, dict) or not isinstance(data.get("sources"), list):
        return [
            ValidationFinding(
                "REGISTRY_SHAPE", str(path), "expected top-level sources list"
            )
        ]

    seen: set[str] = set()
    for index, source in enumerate(data["sources"]):
        item_path = f"{path}:sources[{index}]"
        if not isinstance(source, dict):
            findings.append(
                ValidationFinding(
                    "REGISTRY_SOURCE_SHAPE", item_path, "source must be a mapping"
                )
            )
            continue

        for field in _REQUIRED_SOURCE_FIELDS:
            if field not in source:
                findings.append(
                    ValidationFinding(
                        "REGISTRY_REQUIRED_FIELD", item_path, f"missing {field}"
                    )
                )

        source_id = source.get("id")
        if isinstance(source_id, str):
            if source_id in seen:
                findings.append(
                    ValidationFinding(
                        "REGISTRY_DUPLICATE_ID",
                        item_path,
                        f"duplicate id {source_id}",
                    )
                )
            seen.add(source_id)

        url = source.get("url")
        if isinstance(url, str):
            parsed = urlparse(url)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                findings.append(
                    ValidationFinding(
                        "REGISTRY_URL",
                        item_path,
                        f"expected absolute HTTP(S) URL: {url}",
                    )
                )
            elif source.get("harvest") is True and parsed.scheme != "https":
                findings.append(
                    ValidationFinding(
                        "REGISTRY_INSECURE_HARVEST_URL",
                        item_path,
                        f"harvested source must use HTTPS: {url}",
                    )
                )

            allowed_hosts = source.get("allowed_hosts")
            if isinstance(allowed_hosts, list) and parsed.hostname:
                if parsed.hostname not in allowed_hosts:
                    findings.append(
                        ValidationFinding(
                            "REGISTRY_ALLOWED_HOST",
                            item_path,
                            f"URL host {parsed.hostname} missing from allowed_hosts",
                        )
                    )

    return findings


def validate_manifest(path: Path) -> list[ValidationFinding]:
    """Validate one original-document manifest fragment."""

    data, findings = _load_yaml(path)
    if findings:
        return findings
    if not isinstance(data, dict) or not isinstance(data.get("documents"), list):
        return [
            ValidationFinding(
                "MANIFEST_SHAPE", str(path), "expected top-level documents list"
            )
        ]

    seen: set[str] = set()
    for index, document in enumerate(data["documents"]):
        item_path = f"{path}:documents[{index}]"
        if not isinstance(document, dict):
            findings.append(
                ValidationFinding(
                    "MANIFEST_DOCUMENT_SHAPE", item_path, "document must be a mapping"
                )
            )
            continue

        for field in _REQUIRED_DOCUMENT_FIELDS:
            if field not in document:
                findings.append(
                    ValidationFinding(
                        "MANIFEST_REQUIRED_FIELD", item_path, f"missing {field}"
                    )
                )

        document_id = document.get("id")
        if isinstance(document_id, str):
            if document_id in seen:
                findings.append(
                    ValidationFinding(
                        "MANIFEST_DUPLICATE_ID",
                        item_path,
                        f"duplicate id {document_id}",
                    )
                )
            seen.add(document_id)

        file_name = document.get("file")
        if isinstance(file_name, str) and not _is_safe_relative_path(file_name):
            findings.append(
                ValidationFinding(
                    "MANIFEST_FILE_PATH",
                    item_path,
                    f"file must be a safe relative path: {file_name}",
                )
            )

        url = document.get("url")
        if isinstance(url, str):
            parsed = urlparse(url)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                findings.append(
                    ValidationFinding(
                        "MANIFEST_URL",
                        item_path,
                        f"expected absolute HTTP(S) URL: {url}",
                    )
                )

        sha256 = document.get("sha256")
        if not isinstance(sha256, str) or not _SHA256_RE.fullmatch(sha256):
            findings.append(
                ValidationFinding(
                    "MANIFEST_SHA256", item_path, "sha256 must be 64 lowercase hex chars"
                )
            )

        byte_count = document.get("bytes")
        if not isinstance(byte_count, int) or isinstance(byte_count, bool) or byte_count <= 0:
            findings.append(
                ValidationFinding(
                    "MANIFEST_BYTES", item_path, "bytes must be a positive integer"
                )
            )

    return findings


def _load_checksums(path: Path) -> tuple[dict[str, str], list[ValidationFinding]]:
    findings: list[ValidationFinding] = []
    checksums: dict[str, str] = {}
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        return {}, [
            ValidationFinding(
                "ORIGINALS_CHECKSUM_FORMAT", str(path), f"cannot read SHA256SUMS: {exc}"
            )
        ]

    for line_number, line in enumerate(lines, start=1):
        if not line:
            continue
        match = _CHECKSUM_LINE_RE.fullmatch(line)
        item_path = f"{path}:{line_number}"
        if match is None:
            findings.append(
                ValidationFinding(
                    "ORIGINALS_CHECKSUM_FORMAT",
                    item_path,
                    "expected '<64 lowercase hex><two spaces><relative path>'",
                )
            )
            continue
        digest, relative_path = match.groups()
        if not _is_safe_relative_path(relative_path):
            findings.append(
                ValidationFinding(
                    "ORIGINALS_CHECKSUM_FORMAT",
                    item_path,
                    f"checksum path must be safe and relative: {relative_path}",
                )
            )
            continue
        if relative_path in checksums:
            findings.append(
                ValidationFinding(
                    "ORIGINALS_DUPLICATE_CHECKSUM_PATH",
                    item_path,
                    f"duplicate checksum path {relative_path}",
                )
            )
            continue
        checksums[relative_path] = digest

    return checksums, findings


def validate_originals(originals_dir: Path) -> list[ValidationFinding]:
    """Cross-check manifest fragments and logical release checksums."""

    findings: list[ValidationFinding] = []
    root_manifest = originals_dir / "manifest.yaml"
    root_data, root_findings = _load_yaml(root_manifest)
    findings.extend(root_findings)
    if root_findings:
        return findings
    if not isinstance(root_data, dict) or not isinstance(root_data.get("fragments"), list):
        return [
            ValidationFinding(
                "ORIGINALS_ROOT_SHAPE",
                str(root_manifest),
                "expected top-level fragments list",
            )
        ]

    raw_fragments = root_data["fragments"]
    fragment_counts = Counter(item for item in raw_fragments if isinstance(item, str))
    listed_fragments: list[str] = []
    for index, fragment_value in enumerate(raw_fragments):
        item_path = f"{root_manifest}:fragments[{index}]"
        if not isinstance(fragment_value, str) or not _is_safe_relative_path(fragment_value):
            findings.append(
                ValidationFinding(
                    "ORIGINALS_ROOT_SHAPE",
                    item_path,
                    f"fragment must be a safe relative path: {fragment_value!r}",
                )
            )
            continue
        listed_fragments.append(fragment_value)
        if fragment_counts[fragment_value] > 1:
            findings.append(
                ValidationFinding(
                    "ORIGINALS_DUPLICATE_FRAGMENT",
                    item_path,
                    f"fragment listed more than once: {fragment_value}",
                )
            )

    listed_set = set(listed_fragments)
    actual_set = {
        path.relative_to(originals_dir).as_posix()
        for path in originals_dir.rglob("MANIFEST.yaml")
    }

    for fragment_value in sorted(listed_set - actual_set):
        findings.append(
            ValidationFinding(
                "ORIGINALS_MISSING_FRAGMENT",
                str(root_manifest),
                f"listed fragment does not exist: {fragment_value}",
            )
        )

    for fragment_value in sorted(actual_set - listed_set):
        findings.append(
            ValidationFinding(
                "ORIGINALS_UNLISTED_FRAGMENT",
                str(originals_dir / fragment_value),
                "manifest fragment is not listed in root manifest",
            )
        )

    checksums, checksum_findings = _load_checksums(originals_dir / "SHA256SUMS")
    findings.extend(checksum_findings)

    for fragment_value in listed_fragments:
        fragment_path = originals_dir / fragment_value
        if not fragment_path.is_file():
            continue

        manifest_findings = validate_manifest(fragment_path)
        findings.extend(manifest_findings)

        manifest_data, load_findings = _load_yaml(fragment_path)
        if load_findings or not isinstance(manifest_data, dict):
            continue
        documents = manifest_data.get("documents")
        if not isinstance(documents, list):
            continue

        fragment_parent = fragment_path.parent.relative_to(originals_dir)
        for index, document in enumerate(documents):
            if not isinstance(document, dict):
                continue
            file_name = document.get("file")
            digest = document.get("sha256")
            if not isinstance(file_name, str) or not _is_safe_relative_path(file_name):
                continue
            if not isinstance(digest, str) or not _SHA256_RE.fullmatch(digest):
                continue

            expected_path = _resolve_logical_document_path(fragment_parent, file_name)
            actual_digest = checksums.get(expected_path)
            item_path = f"{fragment_path}:documents[{index}]"
            if actual_digest is None:
                findings.append(
                    ValidationFinding(
                        "ORIGINALS_CHECKSUM_MISSING",
                        item_path,
                        f"missing SHA256SUMS entry for {expected_path}",
                    )
                )
            elif actual_digest != digest:
                findings.append(
                    ValidationFinding(
                        "ORIGINALS_CHECKSUM_MISMATCH",
                        item_path,
                        f"manifest/checksum digest differs for {expected_path}",
                    )
                )

    return findings
