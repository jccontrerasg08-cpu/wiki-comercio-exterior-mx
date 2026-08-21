import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


class MkDocsUxTests(unittest.TestCase):
    def setUp(self):
        self.config = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))

    def test_pages_url_and_material_navigation_features_are_enabled(self):
        self.assertEqual(
            self.config["site_url"],
            "https://jccontrerasg08-cpu.github.io/wiki-comercio-exterior-mx/",
        )
        features = set(self.config["theme"]["features"])
        expected = {
            "navigation.instant",
            "navigation.instant.prefetch",
            "navigation.instant.progress",
            "navigation.tracking",
            "navigation.tabs",
            "navigation.tabs.sticky",
            "navigation.sections",
            "navigation.indexes",
            "navigation.path",
            "navigation.top",
            "navigation.footer",
            "toc.follow",
            "content.tabs.link",
            "content.tooltips",
            "search.suggest",
            "search.highlight",
            "search.share",
        }
        self.assertTrue(expected.issubset(features))

    def test_theme_is_offline_friendly_and_has_trade_identity(self):
        theme = self.config["theme"]
        self.assertFalse(theme["font"])
        self.assertEqual(theme["icon"]["logo"], "material/earth")
        self.assertEqual(len(theme["palette"]), 2)
        self.assertIn("stylesheets/extra.css", self.config["extra_css"])

    def test_global_trade_glossary_is_auto_appended(self):
        extensions = self.config["markdown_extensions"]
        self.assertIn("abbr", extensions)
        self.assertIn("md_in_html", extensions)
        snippets = next(
            item["pymdownx.snippets"]
            for item in extensions
            if isinstance(item, dict) and "pymdownx.snippets" in item
        )
        self.assertIn("includes/abbreviations.md", snippets["auto_append"])
        glossary = (ROOT / "includes" / "abbreviations.md").read_text(encoding="utf-8")
        for acronym in ("LIGIE", "NICO", "RGCE", "RRNA", "ANAM", "SNICE", "VUCEM"):
            self.assertIn(f"*[{acronym}]:", glossary)

    def test_homepage_has_operation_route_and_primary_entry_points(self):
        home = (ROOT / "docs" / "index.md").read_text(encoding="utf-8")
        self.assertIn('class="trade-hero"', home)
        self.assertIn('class="trade-route"', home)
        for target in (
            "wiki/clasificacion/tigie-nico.md",
            "wiki/rrna/index.md",
            "wiki/contribuciones/impuestos-importacion.md",
            "wiki/aduana/pedimento-rgce/",
            "wiki/logistica/logistica-internacional/",
            "catalog/registry.md",
        ):
            self.assertIn(target, home)

    def test_corpus_status_dashboard_is_in_top_level_navigation(self):
        nav = yaml.safe_dump(self.config["nav"], allow_unicode=True, sort_keys=False)
        self.assertIn("Estado del corpus", nav)
        self.assertIn("status/corpus-coverage.md", nav)

    def test_explorer_and_document_library_are_discoverable(self):
        nav = yaml.safe_dump(self.config["nav"], allow_unicode=True, sort_keys=False)
        self.assertIn("Explorar", nav)
        self.assertIn("explore/index.md", nav)
        self.assertIn("Biblioteca de originales", nav)
        self.assertIn("catalog/library.md", nav)
        self.assertIn("Originales faltantes", nav)
        self.assertIn("status/missing-primary-sources.md", nav)
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
            self.assertIn(label, nav)

    def test_anam_faq_entry_is_discoverable_from_navigation_and_home(self):
        nav = yaml.safe_dump(self.config["nav"], allow_unicode=True, sort_keys=False)
        home = (ROOT / "docs" / "index.md").read_text(encoding="utf-8")
        self.assertIn("Preguntas frecuentes ANAM", nav)
        self.assertIn("wiki/aduana/faq-anam.md", nav)
        self.assertIn("wiki/aduana/faq-anam.md", home)

    def test_official_publications_library_is_discoverable(self):
        nav = yaml.safe_dump(self.config["nav"], allow_unicode=True, sort_keys=False)
        self.assertIn("Publicaciones oficiales preservadas", nav)
        self.assertIn("catalog/publicaciones-oficiales.md", nav)

    def test_export_route_is_discoverable_from_navigation_and_home(self):
        nav = yaml.safe_dump(self.config["nav"], allow_unicode=True, sort_keys=False)
        home = (ROOT / "docs" / "index.md").read_text(encoding="utf-8")
        self.assertIn("Ruta de exportación", nav)
        self.assertIn("wiki/exportacion/index.md", nav)
        self.assertIn("wiki/exportacion/index.md", home)

    def test_modular_tools_catalog_is_discoverable_and_evidence_first(self):
        nav = yaml.safe_dump(self.config["nav"], allow_unicode=True, sort_keys=False)
        home = (ROOT / "docs" / "index.md").read_text(encoding="utf-8")
        catalog_path = ROOT / "docs" / "explore" / "herramientas.md"
        self.assertIn("Herramientas verificables", nav)
        self.assertIn("explore/herramientas.md", nav)
        self.assertIn("explore/herramientas.md", home)
        self.assertTrue(catalog_path.exists())
        catalog = catalog_path.read_text(encoding="utf-8")
        for module in (
            "Buscar fracción y tasa",
            "Explorar RRNA y NOM",
            "Tratados y origen",
            "Ruta de importación",
            "Dashboard de recaudación",
        ):
            self.assertIn(module, catalog)
        self.assertIn("no clasifica mercancías", catalog)
        self.assertIn("fecha de corte", catalog)

    def test_motion_is_decorative_and_respects_reduced_motion(self):
        css = (ROOT / "docs" / "stylesheets" / "extra.css").read_text(encoding="utf-8")
        self.assertIn("@keyframes trade-route-flow", css)
        self.assertIn("@media (prefers-reduced-motion: reduce)", css)
        self.assertNotIn("url(http", css.casefold())
        self.assertIn("--trade-ease-out:", css)
        self.assertIn("@media (hover: hover) and (pointer: fine)", css)
        self.assertIn(".trade-route__step:active", css)
        self.assertIn(".md-typeset .md-button:active", css)
        self.assertIn(".grid.cards > ul > li:focus-within", css)


if __name__ == "__main__":
    unittest.main()
