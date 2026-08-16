"""Offline validation helpers for archived official-source originals."""

from __future__ import annotations

import hashlib
import re
from datetime import date
from pathlib import Path, PurePosixPath
from typing import Any


ARCHIVE_STATUSES = {"local_git", "release_asset", "external_only"}
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def _safe_relative_path(value: str) -> bool:
    path = PurePosixPath(value)
    return bool(value) and not path.is_absolute() and ".." not in path.parts


def _validate_common_binary_fields(
    source_id: str, archive: dict[str, Any], *, prefix: str
) -> list[str]:
    errors: list[str] = []
    sha256 = archive.get("sha256")
    if not isinstance(sha256, str) or not _SHA256_RE.fullmatch(sha256):
        errors.append(f"{source_id}: {prefix} archive sha256 must be 64 lowercase hex chars")

    size_bytes = archive.get("size_bytes")
    if not isinstance(size_bytes, int) or isinstance(size_bytes, bool) or size_bytes <= 0:
        errors.append(f"{source_id}: {prefix} archive size_bytes must be a positive integer")

    mime_type = archive.get("mime_type")
    if not isinstance(mime_type, str) or not mime_type.strip():
        errors.append(f"{source_id}: {prefix} archive missing mime_type")

    captured_at = archive.get("captured_at")
    if not isinstance(captured_at, str):
        errors.append(f"{source_id}: {prefix} archive missing captured_at")
    else:
        try:
            date.fromisoformat(captured_at)
        except ValueError:
            errors.append(f"{source_id}: {prefix} archive captured_at must be YYYY-MM-DD")
    return errors


def validate_archive(source: dict[str, Any], root: Path) -> list[str]:
    """Return deterministic validation errors for one optional source archive block."""

    archive = source.get("archive")
    if archive is None:
        return []

    source_id = str(source.get("id", "<unknown>"))
    if not isinstance(archive, dict):
        return [f"{source_id}: archive must be a mapping"]

    status = archive.get("status")
    if status not in ARCHIVE_STATUSES:
        return [f"{source_id}: invalid archive status {status!r}"]

    errors: list[str] = []
    if status == "local_git":
        errors.extend(_validate_common_binary_fields(source_id, archive, prefix="local_git"))
        path_value = archive.get("path")
        if not isinstance(path_value, str) or not _safe_relative_path(path_value):
            errors.append(
                f"{source_id}: local_git archive path must be a safe repository-relative path"
            )
            return errors

        target = root / path_value
        if not target.is_file():
            errors.append(f"{source_id}: archive path does not exist: {path_value}")
            return errors

        size_bytes = archive.get("size_bytes")
        actual_size = target.stat().st_size
        if isinstance(size_bytes, int) and not isinstance(size_bytes, bool) and size_bytes > 0:
            if actual_size != size_bytes:
                errors.append(
                    f"{source_id}: size_bytes mismatch for {path_value}: expected {size_bytes}, got {actual_size}"
                )

        sha256 = archive.get("sha256")
        if isinstance(sha256, str) and _SHA256_RE.fullmatch(sha256):
            actual_hash = hashlib.sha256(target.read_bytes()).hexdigest()
            if actual_hash != sha256:
                errors.append(
                    f"{source_id}: sha256 mismatch for {path_value}: expected {sha256}, got {actual_hash}"
                )

    elif status == "release_asset":
        errors.extend(
            _validate_common_binary_fields(source_id, archive, prefix="release_asset")
        )
        release_tag = archive.get("release_tag")
        if not isinstance(release_tag, str) or not release_tag.strip():
            errors.append(f"{source_id}: release_asset archive missing release_tag")
        asset_name = archive.get("asset_name")
        if not isinstance(asset_name, str) or not asset_name.strip():
            errors.append(f"{source_id}: release_asset archive missing asset_name")

    else:
        reason = archive.get("reason")
        if not isinstance(reason, str) or not reason.strip():
            errors.append(f"{source_id}: external_only archive requires reason")

    return sorted(dict.fromkeys(errors))


def archive_label(source: dict[str, Any]) -> str:
    """Return one stable display label for a source archive state."""

    archive = source.get("archive")
    if not isinstance(archive, dict):
        return "unclassified"
    status = archive.get("status")
    return str(status) if status in ARCHIVE_STATUSES else "unclassified"
