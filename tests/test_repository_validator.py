import importlib.util
import unittest


class RepositoryValidatorBootstrapTests(unittest.TestCase):
    def test_validator_module_exists(self):
        self.assertIsNotNone(importlib.util.find_spec("scripts.validate_repository"))


if __name__ == "__main__":
    unittest.main()
