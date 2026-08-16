import hashlib
import tempfile
import unittest
from pathlib import Path

import yaml

from scripts.archive_metadata import archive_label, validate_archive
from scripts.schema_validation import load_local_schema, validate_instance


ROOT = Path(__file__).resolve().parents[1]


class ArchiveMetadataTests(unittest.TestCase):
    def test_local_git_requires_existing_verifiable_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = {
                "id": "mx_test",
                "archive": {
                    "status": "local_git",
                    "path": "data/originals/test.pdf",
                    "sha256": "a" * 64,
                    "size_bytes": 123,
                    "mime_type": "application/pdf",
                    "captured_at": "2026-08-15",
                },
            }
            errors = validate_archive(source, root)
        self.assertTrue(any("archive path does not exist" in error for error in errors))

    def test_local_git_detects_size_and_checksum_drift(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            target = root / "data" / "originals" / "test.pdf"
            target.parent.mkdir(parents=True)
            target.write_bytes(b"official-bytes")
            source = {
                "id": "mx_test",
                "archive": {
                    "status": "local_git",
                    "path": "data/originals/test.pdf",
                    "sha256": "0" * 64,
                    "size_bytes": 1,
                    "mime_type": "application/pdf",
                    "captured_at": "2026-08-15",
                },
            }
            errors = validate_archive(source, root)
        self.assertTrue(any("size_bytes mismatch" in error for error in errors))
        self.assertTrue(any("sha256 mismatch" in error for error in errors))

    def test_local_git_accepts_verified_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            target = root / "data" / "originals" / "test.pdf"
            target.parent.mkdir(parents=True)
            payload = b"official-bytes"
            target.write_bytes(payload)
            source = {
                "id": "mx_test",
                "archive": {
                    "status": "local_git",
                    "path": "data/originals/test.pdf",
                    "sha256": hashlib.sha256(payload).hexdigest(),
                    "size_bytes": len(payload),
                    "mime_type": "application/pdf",
                    "captured_at": "2026-08-15",
                },
            }
            errors = validate_archive(source, root)
        self.assertEqual(errors, [])
        self.assertEqual(archive_label(source), "local_git")

    def test_release_asset_requires_identity_and_checksum_fields(self):
        source = {"id": "mx_test", "archive": {"status": "release_asset"}}
        errors = validate_archive(source, Path("."))
        self.assertTrue(any("release_tag" in error for error in errors))
        self.assertTrue(any("asset_name" in error for error in errors))
        self.assertTrue(any("sha256" in error for error in errors))
        self.assertTrue(any("size_bytes" in error for error in errors))

    def test_external_only_requires_reason(self):
        source = {"id": "mx_test", "archive": {"status": "external_only"}}
        errors = validate_archive(source, Path("."))
        self.assertTrue(any("reason" in error for error in errors))

    def test_rejects_unsafe_local_path(self):
        source = {
            "id": "mx_test",
            "archive": {
                "status": "local_git",
                "path": "../outside.pdf",
                "sha256": "a" * 64,
                "size_bytes": 10,
                "mime_type": "application/pdf",
                "captured_at": "2026-08-15",
            },
        }
        errors = validate_archive(source, Path("."))
        self.assertTrue(any("safe repository-relative path" in error for error in errors))

    def test_unclassified_source_has_explicit_label(self):
        self.assertEqual(archive_label({"id": "mx_test"}), "unclassified")

    def test_source_schema_accepts_release_asset_archive(self):
        schema = load_local_schema(ROOT, "source.schema.json")
        findings = validate_instance(
            {
                "id": "mx_test",
                "jurisdiction": "MEX",
                "title": "Test source",
                "url": "https://example.gob.mx/test.pdf",
                "authority": "Example authority",
                "evidence_class": "primary_legal",
                "allowed_hosts": ["example.gob.mx"],
                "media_types": ["application/pdf"],
                "harvest": False,
                "archive": {
                    "status": "release_asset",
                    "release_tag": "sources-2026-08-15",
                    "asset_name": "test.pdf",
                    "sha256": "a" * 64,
                    "size_bytes": 123,
                    "mime_type": "application/pdf",
                    "captured_at": "2026-08-15",
                },
            },
            schema,
            "source",
        )
        self.assertEqual(findings, [])

    def test_source_schema_rejects_external_only_without_reason(self):
        schema = load_local_schema(ROOT, "source.schema.json")
        findings = validate_instance(
            {
                "id": "mx_test",
                "jurisdiction": "MEX",
                "title": "Test source",
                "url": "https://example.gob.mx/portal",
                "authority": "Example authority",
                "evidence_class": "official_operational",
                "allowed_hosts": ["example.gob.mx"],
                "media_types": ["text/html"],
                "harvest": False,
                "archive": {"status": "external_only"},
            },
            schema,
            "source",
        )
        self.assertTrue(any(finding.path.startswith("source.archive") for finding in findings))

    def test_all_declared_registry_archive_blocks_are_valid(self):
        data = yaml.safe_load((ROOT / "sources" / "registry.yaml").read_text(encoding="utf-8"))
        errors: list[str] = []
        for source in data["sources"]:
            if isinstance(source, dict) and "archive" in source:
                errors.extend(validate_archive(source, ROOT))
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
