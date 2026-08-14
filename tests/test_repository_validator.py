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


if __name__ == "__main__":
    unittest.main()
