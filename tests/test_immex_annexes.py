from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
PROGRAMS = ROOT / "docs" / "wiki" / "programas"
CORPUS = ROOT / "data" / "corpus"


def read(rel: str | Path) -> str:
    path = rel if isinstance(rel, Path) else ROOT / rel
    return path.read_text(encoding="utf-8")


def load_yaml(rel: str) -> dict:
    return yaml.safe_load(read(rel)) or {}


class ImmexAnnexContractTests(unittest.TestCase):
    def test_public_annex_guides_exist(self):
        required = (
            PROGRAMS / "anexo-24-control-inventarios.md",
            PROGRAMS / "anexo-30-scccyg.md",
        )
        for path in required:
            with self.subTest(path=path.name):
                self.assertTrue(path.exists(), str(path.relative_to(ROOT)))

    def test_immex_hub_connects_both_annexes_conditionally(self):
        text = read(PROGRAMS / "immex.md")
        self.assertIn("anexo-24-control-inventarios.md", text)
        self.assertIn("anexo-30-scccyg.md", text)
        self.assertIn("no aplica automáticamente", text.lower())
        self.assertIn("último día hábil", text.lower())
        self.assertIn("2026", text)

    def test_annex_24_guide_preserves_distinct_scopes(self):
        text = read(PROGRAMS / "anexo-24-control-inventarios.md")
        for marker in (
            "Apartado A",
            "Apartado B",
            "Apartado C",
            "SECIIT",
            "PEPS",
            "24 horas",
            "48 horas",
            "Lo que no debe inferirse",
        ):
            self.assertIn(marker.lower(), text.lower())
        self.assertNotIn("Anexo 24 = SECIIT", text)

    def test_annex_30_guide_is_not_universal_immex(self):
        text = read(PROGRAMS / "anexo-30-scccyg.md")
        self.assertIn("SCCCyG", text)
        self.assertIn("no significa", text.lower())
        self.assertIn("resolución definitiva", text.lower())
        self.assertIn("plazos", text.lower())
        self.assertIn("PEPS", text)

    def test_unsafe_legacy_claims_are_removed_from_annex_digests(self):
        corpus = "\n".join(
            (
                read(CORPUS / "anexo-24-control-inventarios-immex.md"),
                read(CORPUS / "anexo-30-scccyg.md"),
            )
        )
        forbidden = (
            "Plan Maestro 2026",
            "El Anexo 24 no es una hoja de cálculo",
            "reconciliación del SACI vs. el sistema del SAT cada 12 meses",
            "riesgo de PAMA",
            "El SAT puede jalar datos directamente",
            "No posible — datos inmutables",
        )
        for phrase in forbidden:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, corpus)

    def test_primary_immex_reform_sources_are_registered(self):
        source_ids = {item["id"] for item in load_yaml("sources/registry.yaml")["sources"]}
        self.assertTrue(
            {
                "mx_sidof_immex_reform_20241219",
                "mx_sidof_immex_reform_20250828",
                "mx_sidof_immex_suspension_2026",
            }.issubset(source_ids)
        )

    def test_immex_instrument_tracks_latest_primary_reforms(self):
        instruments = {
            item["id"]: item for item in load_yaml("sources/instruments.yaml")["instruments"]
        }
        immex = instruments["mx_programa_immex"]
        events = {
            (event["source_id"], str(event["effective_from"]))
            for event in immex.get("events", [])
        }
        self.assertIn(("mx_sidof_immex_reform_20241219", "2024-12-20"), events)
        self.assertIn(("mx_sidof_immex_reform_20250828", "2025-08-29"), events)
        self.assertNotIn(
            "mx_sidof_immex_suspension_2026",
            {event["source_id"] for event in immex.get("events", [])},
        )

    def test_page_metadata_governs_new_guides(self):
        pages = {
            item["path"]: item for item in load_yaml("sources/page_metadata.yaml")["pages"]
        }
        for rel in (
            "docs/wiki/programas/anexo-24-control-inventarios.md",
            "docs/wiki/programas/anexo-30-scccyg.md",
        ):
            with self.subTest(path=rel):
                self.assertIn(rel, pages)
                self.assertTrue(pages[rel].get("source_ids"))
                self.assertTrue(pages[rel].get("instrument_ids"))

    def test_navigation_surfaces_both_guides(self):
        text = read("mkdocs.yml")
        self.assertIn("wiki/programas/anexo-24-control-inventarios.md", text)
        self.assertIn("wiki/programas/anexo-30-scccyg.md", text)


if __name__ == "__main__":
    unittest.main()
