import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


class DocsEngineCompatibilityTests(unittest.TestCase):
    def test_production_docs_stack_is_explicit_and_deterministic(self):
        requirements = (ROOT / "requirements-docs.txt").read_text(encoding="utf-8").splitlines()
        self.assertIn("mkdocs==1.6.1", requirements)
        self.assertIn("mkdocs-material==9.7.7", requirements)
        self.assertIn("mkdocs-redirects==1.2.3", requirements)
        self.assertIn("properdocs==1.6.7", requirements)

    def test_legacy_redirects_remain_a_production_contract(self):
        config = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
        redirects = next(
            item["redirects"]
            for item in config["plugins"]
            if isinstance(item, dict) and "redirects" in item
        )
        redirect_maps = redirects["redirect_maps"]
        self.assertGreaterEqual(len(redirect_maps), 20)
        self.assertEqual(
            redirect_maps["aduana/documentos.md"],
            "wiki/aduana/documentos.md",
        )

    def test_migration_note_records_current_candidate_and_blocker(self):
        note = (ROOT / "docs" / "methodology" / "docs-engine-compatibility.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Zensical 0.0.54", note)
        self.assertIn("mkdocs-redirects", note)
        self.assertIn("zensical/backlog#23", note)
        self.assertIn("producción", note.casefold())
        self.assertIn("legacy", note.casefold())
        self.assertIn("properdocs>=1.6.5", note)


if __name__ == "__main__":
    unittest.main()
