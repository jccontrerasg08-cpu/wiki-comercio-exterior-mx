import json
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


class WorldExplorerTests(unittest.TestCase):
    def setUp(self):
        self.config = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
        self.page = ROOT / "docs/explore/mundo.md"
        self.data_path = ROOT / "docs/assets/data/world-explorer-sources.json"
        self.script_path = ROOT / "docs/assets/javascripts/world-explorer.js"

    def test_world_explorer_is_discoverable_and_has_a_text_first_fallback(self):
        nav = yaml.safe_dump(self.config["nav"], allow_unicode=True, sort_keys=False)
        self.assertIn("Mundo y fuentes comparables", nav)
        self.assertIn("explore/mundo.md", nav)
        self.assertIn("assets/javascripts/world-explorer.js", self.config["extra_javascript"])
        page = self.page.read_text(encoding="utf-8")
        self.assertIn('data-world-explorer', page)
        self.assertIn('data-source="../../assets/data/world-explorer-sources.json"', page)
        self.assertIn("Sin JavaScript", page)
        self.assertIn("Lista accesible", page)
        self.assertIn("No hay globo WebGL", page)
        self.assertIn('aria-live="polite"', page)

    def test_world_explorer_groups_filters_and_reflows_on_mobile(self):
        page = self.page.read_text(encoding="utf-8")
        styles = (ROOT / "docs/stylesheets/extra.css").read_text(encoding="utf-8")
        self.assertIn("<fieldset", page)
        self.assertIn("<legend>Filtros de guías de país</legend>", page)
        self.assertIn("min-width: 0;", styles)
        self.assertNotIn("min-width: 36rem", styles)

    def test_world_explorer_exposes_an_empty_result_message(self):
        page = self.page.read_text(encoding="utf-8")
        script = self.script_path.read_text(encoding="utf-8")
        self.assertIn("data-world-empty", page)
        self.assertIn("No hay guías que coincidan con estos filtros.", script)

    def test_world_data_keeps_scope_sources_and_contract_boundary(self):
        data = json.loads(self.data_path.read_text(encoding="utf-8"))
        self.assertEqual(data["scope"]["coverage"], "curated-country-guides")
        self.assertEqual(data["scope"]["geometry_mode"], "contract-only")
        self.assertFalse(data["scope"]["embed_ready"])
        self.assertEqual(len(data["country_guides"]), 7)
        self.assertIn("global_un_comtrade", {source["id"] for source in data["international_sources"]})
        self.assertIn("version", data["source"])
        self.assertIn("license_note", data["scope"])

    def test_world_script_uses_native_filters_without_remote_map_dependency(self):
        script = self.script_path.read_text(encoding="utf-8")
        self.assertIn("data-world-explorer", script)
        self.assertIn("change", script)
        self.assertIn("input", script)
        self.assertNotIn("https://", script)
        self.assertNotIn("maplibre", script.casefold())
        self.assertNotIn("webgl", script.casefold())


if __name__ == "__main__":
    unittest.main()
