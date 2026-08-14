"""Offline integrity validation for wiki-comercio-exterior-mx."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
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
            if parsed.scheme != "https" or not parsed.netloc:
                findings.append(
                    ValidationFinding(
                        "REGISTRY_URL",
                        item_path,
                        f"expected absolute HTTPS URL: {url}",
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
