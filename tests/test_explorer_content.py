import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPLORE = ROOT / "docs" / "explore"


class ExplorerContentTests(unittest.TestCase):
    def test_hub_exposes_all_approved_domains_and_canonical_repositories(self):
        text = (EXPLORE / "index.md").read_text(encoding="utf-8")
        for label in (
            "Aranceles",
            "Marco jurídico",
            "RGCE y anexos",
            "Tratados y origen",
            "Programas",
            "RRNA y NOM",
            "Aduanas y mapa",
            "Fuentes oficiales",
        ):
            self.assertIn(label, text)
        self.assertIn("arancel-mx", text)
        self.assertIn("aduanamap-mx", text)
        self.assertIn("../catalog/library.md", text)

    def test_legal_explorer_routes_to_core_instruments_and_provenance(self):
        text = (EXPLORE / "marco-juridico.md").read_text(encoding="utf-8")
        for term in (
            "Ley Aduanera",
            "Reglamento de la Ley Aduanera",
            "LIGIE",
            "Ley de Comercio Exterior",
            "RGCE",
            "sources/instruments.yaml",
            "Biblioteca de originales",
        ):
            self.assertIn(term, text)

    def test_rgce_explorer_preserves_publication_vs_archive_distinction(self):
        text = (EXPLORE / "rgce.md").read_text(encoding="utf-8")
        self.assertIn("2026", text)
        self.assertIn("Anexos 1–30", text)
        self.assertIn("SIDOF", text)
        self.assertIn("SAT", text)
        self.assertIn("equivalente oficial", text)
        self.assertIn("../catalog/library.md", text)

    def test_tariff_explorer_keeps_structured_data_in_arancel_mx(self):
        text = (EXPLORE / "aranceles.md").read_text(encoding="utf-8")
        for term in ("HS", "capítulo", "partida", "subpartida", "fracción MX", "NICO"):
            self.assertIn(term, text)
        self.assertIn("arancel-mx", text)
        self.assertIn("../wiki/clasificacion/tigie-nico.md", text)

    def test_operational_explorers_link_existing_pages_and_sources(self):
        treaties = (EXPLORE / "tratados-origen.md").read_text(encoding="utf-8")
        programs = (EXPLORE / "programas.md").read_text(encoding="utf-8")
        rrna = (EXPLORE / "rrna-nom.md").read_text(encoding="utf-8")
        self.assertIn("T-MEC", treaties)
        self.assertIn("reglas de origen", treaties.casefold())
        for term in ("IMMEX", "PROSEC", "Drawback", "Anexo 24", "Anexo 30"):
            self.assertIn(term, programs)
        self.assertIn("NICO", rrna)
        self.assertIn("no determina", rrna.casefold())
        self.assertIn("../catalog/library.md", treaties)
        self.assertIn("../catalog/library.md", programs)
        self.assertIn("../catalog/library.md", rrna)

    def test_map_explorer_degrades_to_text_and_points_to_canonical_app(self):
        text = (EXPLORE / "mapa.md").read_text(encoding="utf-8")
        self.assertIn("aduanamap-mx", text)
        self.assertIn("countries-50m.geojson", text)
        self.assertIn("sin mapa", text.casefold())
        self.assertIn("GeoJSON", text)


if __name__ == "__main__":
    unittest.main()
