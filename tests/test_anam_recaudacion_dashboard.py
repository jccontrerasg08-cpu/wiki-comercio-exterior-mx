import json
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


class AnamRecaudacionDashboardTests(unittest.TestCase):
    def setUp(self):
        self.config = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
        self.page = ROOT / "docs/wiki/aduana/recaudacion-anam.md"
        self.data_path = ROOT / "docs/assets/data/anam-recaudacion-q2-2026.json"
        self.script_path = ROOT / "docs/assets/javascripts/anam-dashboard.js"

    def test_dashboard_is_discoverable_and_progressively_enhanced(self):
        nav = yaml.safe_dump(self.config["nav"], allow_unicode=True, sort_keys=False)
        self.assertIn("Recaudación ANAM", nav)
        self.assertIn("wiki/aduana/recaudacion-anam.md", nav)
        self.assertIn("assets/javascripts/anam-dashboard.js", self.config["extra_javascript"])
        page = self.page.read_text(encoding="utf-8")
        self.assertIn('data-anam-dashboard', page)
        self.assertIn('data-source="../../../assets/data/anam-recaudacion-q2-2026.json"', page)
        self.assertIn("Fuente primaria", page)
        self.assertIn("Sin JavaScript", page)
        self.assertIn('aria-live="polite"', page)

    def test_dashboard_groups_filters_with_native_semantics(self):
        page = self.page.read_text(encoding="utf-8")
        self.assertIn("<fieldset", page)
        self.assertIn("<legend>Filtros del tablero de recaudación</legend>", page)

    def test_dashboard_data_preserves_period_unit_and_source(self):
        data = json.loads(self.data_path.read_text(encoding="utf-8"))
        self.assertEqual(data["scope"]["country"], "MEX")
        self.assertEqual(data["scope"]["period"], "2026-Q2")
        self.assertEqual(data["scope"]["currency"], "MXN")
        self.assertEqual(data["scope"]["unit"], "MDP")
        self.assertEqual(data["source"]["url"], "https://www.anam.gob.mx/wp-content/uploads/Informe_trimestral_Q2_2026_f.pdf")
        self.assertEqual(data["indicators"]["recaudacion_q2_mdp"]["value"], 336190)
        self.assertEqual(data["indicators"]["recaudacion_semestre_mdp"]["value"], 659393)
        self.assertEqual(len(data["series"]["recaudacion_mensual_mdp"]), 6)
        self.assertEqual(len(data["rankings"]["recaudacion_aduanas_q2_mdp"]), 15)

    def test_recaudacion_catalog_is_discoverable_and_keeps_document_scope(self):
        nav = yaml.safe_dump(self.config["nav"], allow_unicode=True, sort_keys=False)
        catalog = ROOT / "docs/catalog/mexico/recaudacion-anam.md"
        self.assertIn("Recaudación ANAM", nav)
        self.assertIn("catalog/mexico/recaudacion-anam.md", nav)
        self.assertTrue(catalog.exists())
        text = catalog.read_text(encoding="utf-8")
        normalized = text.casefold()
        self.assertIn("22 informes de recaudación", normalized)
        self.assertIn("noviembre de 2024", normalized)
        self.assertIn("julio de 2026", normalized)
        self.assertIn("no son informes de recaudación", normalized)
        self.assertIn("informe_trimestral_q2_2026_f.pdf", normalized)
        dashboard_page = self.page.read_text(encoding="utf-8")
        self.assertIn("../../catalog/mexico/recaudacion-anam.md", dashboard_page)

    def test_dashboard_script_renders_dataset_text_without_html_interpolation(self):
        script = self.script_path.read_text(encoding="utf-8")
        self.assertNotIn(".innerHTML", script)
        self.assertIn("textContent", script)
        self.assertIn("createElement", script)

    def test_dashboard_script_has_keyboard_safe_filtering_and_no_remote_dependency(self):
        script = self.script_path.read_text(encoding="utf-8")
        self.assertIn("data-anam-dashboard", script)
        self.assertIn("change", script)
        self.assertNotIn("https://", script)
        self.assertNotIn("animation", script.casefold())


if __name__ == "__main__":
    unittest.main()
