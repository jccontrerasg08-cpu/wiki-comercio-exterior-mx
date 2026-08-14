import shutil
import tempfile
import unittest
from pathlib import Path

from scripts import validate_repository as validator

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "invalid"


class RepositoryValidatorTests(unittest.TestCase):
    def test_validator_module_exists(self):
        self.assertTrue(
            (ROOT / "scripts" / "validate_repository.py").is_file(),
            "scripts.validate_repository must exist",
        )

    def test_duplicate_source_id_is_rejected(self):
        validate_registry = getattr(validator, "validate_registry", None)
        self.assertIsNotNone(validate_registry, "validate_registry must exist")
        findings = validate_registry(FIXTURES / "duplicate-source-id.yaml")
        self.assertIn("REGISTRY_DUPLICATE_ID", {item.code for item in findings})

    def test_real_registry_has_no_structural_findings(self):
        validate_registry = getattr(validator, "validate_registry", None)
        self.assertIsNotNone(validate_registry, "validate_registry must exist")
        findings = validate_registry(ROOT / "sources" / "registry.yaml")
        self.assertEqual(findings, [])

    def test_invalid_manifest_sha_is_rejected(self):
        validate_manifest = getattr(validator, "validate_manifest", None)
        self.assertIsNotNone(validate_manifest, "validate_manifest must exist")
        findings = validate_manifest(FIXTURES / "invalid-sha256.yaml")
        self.assertIn("MANIFEST_SHA256", {item.code for item in findings})

    def test_real_manifest_fragments_have_valid_structure(self):
        validate_manifest = getattr(validator, "validate_manifest", None)
        self.assertIsNotNone(validate_manifest, "validate_manifest must exist")
        fragment_paths = [
            ROOT / "data" / "originals" / "diputados" / "MANIFEST.yaml",
            ROOT / "data" / "originals" / "sidof" / "5778300" / "MANIFEST.yaml",
            ROOT / "data" / "originals" / "tmec" / "MANIFEST.yaml",
        ]
        for path in fragment_paths:
            with self.subTest(path=path):
                self.assertEqual(validate_manifest(path), [])

    def test_missing_originals_fragment_is_rejected(self):
        validate_originals = getattr(validator, "validate_originals", None)
        self.assertIsNotNone(validate_originals, "validate_originals must exist")
        with tempfile.TemporaryDirectory() as temp_dir:
            originals = Path(temp_dir)
            shutil.copyfile(
                FIXTURES / "missing-fragment.yaml", originals / "manifest.yaml"
            )
            (originals / "SHA256SUMS").write_text("", encoding="utf-8")
            findings = validate_originals(originals)
        self.assertIn("ORIGINALS_MISSING_FRAGMENT", {item.code for item in findings})

    def test_real_originals_index_and_checksums_are_consistent(self):
        validate_originals = getattr(validator, "validate_originals", None)
        self.assertIsNotNone(validate_originals, "validate_originals must exist")
        findings = validate_originals(ROOT / "data" / "originals")
        self.assertEqual(findings, [])

    def test_official_binary_committed_under_originals_is_rejected(self):
        validate_hygiene = getattr(validator, "validate_repository_hygiene", None)
        self.assertIsNotNone(validate_hygiene, "validate_repository_hygiene must exist")
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            originals = root / "data" / "originals"
            originals.mkdir(parents=True)
            (originals / "example.PDF").write_bytes(b"not a real pdf")
            findings = validate_hygiene(root)
        self.assertIn("REPOSITORY_BINARY_IN_GIT", {item.code for item in findings})

    def test_real_repository_has_no_original_binary_payloads(self):
        validate_hygiene = getattr(validator, "validate_repository_hygiene", None)
        self.assertIsNotNone(validate_hygiene, "validate_repository_hygiene must exist")
        self.assertEqual(validate_hygiene(ROOT), [])


if __name__ == "__main__":
    unittest.main()
