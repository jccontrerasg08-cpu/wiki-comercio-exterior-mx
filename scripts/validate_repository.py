"""Offline integrity validation for wiki-comercio-exterior-mx."""

from __future__ import annotations

import re
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


def _load_yaml(path: Path) -> tuple[Any | None, list[ValidationFinding]]:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")), []
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        return None, [
            ValidationFinding("YAML_INVALID", str(path), f"cannot parse YAML: {exc}")
        ]


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
        if isinstance(file_name, str):
            pure_path = PurePosixPath(file_name)
            if pure_path.is_absolute() or ".." in pure_path.parts:
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
            if parsed.scheme != "https" or not parsed.netloc:
                findings.append(
                    ValidationFinding(
                        "MANIFEST_URL",
                        item_path,
                        f"expected absolute HTTPS URL: {url}",
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
