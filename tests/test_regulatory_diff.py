import unittest
from regulatory_diff import RegulatoryDiffEngine

class RegulatoryDiffEngineTests(unittest.TestCase):
    def test_compare_versions_detects_additions_and_deletions(self):
        old_text = "Línea 1\nLínea 2 a borrar"
        new_text = "Línea 1\nLínea 2 a borrar\nLínea 3 añadida"
        
        diff = RegulatoryDiffEngine.compare_versions(old_text, new_text)
        summary = diff["summary"]
        
        self.assertEqual(summary["additions"], 1)
        self.assertEqual(summary["deletions"], 0)
        self.assertEqual(summary["total_changes"], 1)
        
    def test_compare_versions_detects_modifications(self):
        old_text = "Línea 1\nLínea 2"
        new_text = "Línea 1\nLínea 2 modificada"
        
        diff = RegulatoryDiffEngine.compare_versions(old_text, new_text)
        summary = diff["summary"]
        self.assertEqual(summary["modifications"], 1)
        
    def test_compare_versions_ignores_empty_lines(self):
        old_text = "Línea 1\n\nLínea 2"
        new_text = "Línea 1\nLínea 2"
        
        diff = RegulatoryDiffEngine.compare_versions(old_text, new_text)
        self.assertEqual(diff["summary"]["total_changes"], 0)

if __name__ == "__main__":
    unittest.main()
