"""Deterministic, local-only JSON Schema validation helpers."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


@dataclass(frozen=True, slots=True)
class SchemaFinding:
    code: str
    path: str
    message: str


def load_local_schema(root: Path, name: str) -> dict[str, object]:
    """Load and validate one repository-owned schema without remote retrieval."""

    path = root / "schemas" / name
    schema = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(schema, dict):
        raise ValueError(f"schema must be a JSON object: {path}")
    Draft202012Validator.check_schema(schema)
    return schema


def _format_path(prefix: str, parts: list[Any]) -> str:
    rendered = prefix
    for part in parts:
        rendered += f"[{part}]" if isinstance(part, int) else f".{part}"
    return rendered


def _error_code(validator_name: str) -> str:
    snake_case = re.sub(r"(?<!^)(?=[A-Z])", "_", validator_name).upper()
    return f"SCHEMA_{snake_case}"


def validate_instance(
    instance: object,
    schema: dict[str, object],
    path: str,
) -> list[SchemaFinding]:
    """Return stable findings using explicit JSON Schema format validation."""

    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    findings = [
        SchemaFinding(
            code=_error_code(str(error.validator)),
            path=_format_path(path, list(error.absolute_path)),
            message=error.message,
        )
        for error in validator.iter_errors(instance)
    ]
    return sorted(findings, key=lambda item: (item.path, item.code, item.message))
