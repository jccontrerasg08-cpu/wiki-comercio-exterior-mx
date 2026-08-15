import unittest
from pathlib import Path

from scripts.page_metadata import inventory_content_pages, validate_page_metadata


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "page-metadata"


class PageMetadataTests(unittest.TestCase):
    def test_every_content_page_has_metadata(self):
        self.assertGreater(len(inventory_content_pages(ROOT)), 50)
        self.assertEqual(validate_page_metadata(ROOT), [])

    def test_missing_page_is_reported(self):
        findings = validate_page_metadata(FIXTURES)
        self.assertEqual(findings[0].code, "PAGE_NOT_FOUND")

    def test_current_reviewed_wiki_pages_have_current_through(self):
        import yaml

        data = yaml.safe_load((ROOT / "sources" / "page_metadata.yaml").read_text(encoding="utf-8"))
        for page in data["pages"]:
            if page["path"].startswith("docs/wiki/") and page["source_status"] == "current" and page["legal_review_status"] == "reviewed":
                self.assertIsNotNone(page["current_through"], page["path"])


if __name__ == "__main__":
    unittest.main()
