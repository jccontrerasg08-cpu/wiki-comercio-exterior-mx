import hashlib
import tempfile
import unittest
from pathlib import Path

from scripts.archive_metadata import archive_label, validate_archive


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


if __name__ == "__main__":
    unittest.main()
