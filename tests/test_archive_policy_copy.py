import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC_PATHS = (
    ROOT / "docs" / "catalog" / "index.md",
    ROOT / "docs" / "catalog" / "mexico" / "index.md",
    ROOT / "docs" / "catalog" / "mexico" / "arancel.md",
    ROOT / "data" / "originals" / "README.md",
)
FORBIDDEN = (
    "does not ship official PDF bytes",
    "This tree is not a DOF dump",
    "This page is a URL catalog, not a DOF dump",
    "Portals (do not scrape)",
    "Catalog-only; do not scrape",
    "catalog-only; as of",
)


class ArchivePolicyCopyTests(unittest.TestCase):
    def test_no_blanket_policy_blocks_preserving_official_originals(self):
        text = "\n".join(path.read_text(encoding="utf-8") for path in DOC_PATHS)
        for phrase in FORBIDDEN:
            self.assertNotIn(phrase, text)

    def test_policy_affirms_reproducible_archive_and_official_authority(self):
        text = "\n".join(path.read_text(encoding="utf-8") for path in DOC_PATHS).casefold()
        self.assertIn("reproduc", text)
        self.assertIn("github release", text)
        self.assertIn("official", text)
        self.assertIn("sha-256", text)

    def test_tariff_database_boundary_remains_explicit(self):
        text = (ROOT / "docs" / "catalog" / "mexico" / "arancel.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("arancel-mx", text)
        self.assertIn("structured", text.casefold())

    def test_private_proprietary_text_is_not_reclassified_as_archivable_original(self):
        text = (ROOT / "data" / "originals" / "README.md").read_text(encoding="utf-8")
        self.assertIn("Incoterms", text)
        self.assertIn("No ICC rule text", text)


if __name__ == "__main__":
    unittest.main()
