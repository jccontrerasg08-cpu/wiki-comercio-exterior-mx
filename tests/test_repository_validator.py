import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RepositoryValidatorBootstrapTests(unittest.TestCase):
    def test_validator_module_exists(self):
        self.assertTrue(
            (ROOT / "scripts" / "validate_repository.py").is_file(),
            "scripts.validate_repository must exist",
        )


if __name__ == "__main__":
    unittest.main()
