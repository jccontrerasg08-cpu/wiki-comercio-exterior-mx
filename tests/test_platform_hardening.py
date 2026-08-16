from __future__ import annotations

from datetime import date
from pathlib import Path
import tempfile
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]


class PlatformHardeningTests(unittest.TestCase):
    def test_web_profile_has_governed_discovery_features(self) -> None:
        config = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
        plugins = config["plugins"]
        self.assertIsInstance(plugins, dict)
        self.assertIn("meta", plugins)
        self.assertIn("tags", plugins)
        tags = plugins["tags"]
        self.assertTrue(tags["tags_hierarchy"])
        self.assertEqual(
            set(tags["tags_allowed"]),
            {
                "Tema/Fundamentos",
                "Tema/Aduana",
                "Tema/Clasificación",
                "Tema/RRNA",
                "Tema/Contribuciones",
                "Tema/Programas",
                "Tema/Logística",
                "Tipo/Fuente",
                "Tipo/Metodología",
                "Tipo/Estado",
            },
        )
        features = set(config["theme"]["features"])
        self.assertIn("content.footnote.tooltips", features)
        self.assertIn("navigation.instant.preview", features)
        self.assertIn("footnotes", config["markdown_extensions"])
        nav = yaml.safe_dump(config["nav"], allow_unicode=True, sort_keys=False)
        self.assertIn("Explorar", nav)
        self.assertIn("topics.md", nav)
        self.assertIn("explore/knowledge-map.md", nav)

    def test_offline_profile_disables_fetch_dependent_navigation(self) -> None:
        path = ROOT / "mkdocs.offline.yml"
        self.assertTrue(path.is_file())
        config = yaml.safe_load(path.read_text(encoding="utf-8"))
        self.assertEqual(config["INHERIT"], "mkdocs.yml")
        self.assertIsNone(config["repo_url"])
        self.assertIn("offline", config["plugins"])
        features = set(config["theme"]["features"])
        self.assertFalse(any(item.startswith("navigation.instant") for item in features))

    def test_ci_enforces_generated_map_and_offline_build(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        self.assertIn("python -m scripts.build_knowledge_map --check", workflow)
        self.assertIn("mkdocs.offline.yml", workflow)
        self.assertIn("python -m scripts.verify_offline_site site-offline", workflow)

    def test_knowledge_map_is_generated_from_canonical_metadata(self) -> None:
        from scripts.build_knowledge_map import (
            build_index,
            render_knowledge_json,
            render_knowledge_map,
        )

        rendered = render_knowledge_map(ROOT)
        records = build_index(ROOT)
        self.assertEqual(rendered, render_knowledge_map(ROOT))
        self.assertEqual(records, build_index(ROOT))
        self.assertIn("Reglas Generales de Comercio Exterior para 2026", rendered)
        self.assertIn('"mx_sidof_rgce_2026_anexos_21_30"', render_knowledge_json(ROOT))
        self.assertTrue(records)
        self.assertTrue(
            any(
                source["url"].startswith("https://")
                for record in records
                for source in record["sources"]
                if source["url"]
            )
        )

    def test_local_query_returns_source_backed_temporal_hits(self) -> None:
        script = ROOT / "scripts" / "query_knowledge.py"
        self.assertTrue(script.is_file())

        from scripts.query_knowledge import search_repository

        hits = search_repository(ROOT, "IMMEX Anexo 24", date(2026, 8, 15), k=5)
        self.assertTrue(hits)
        self.assertTrue(all(hit.source_id and hit.url.startswith("https://") for hit in hits))
        self.assertTrue(
            {hit.source_id for hit in hits}.intersection(
                {"mx_sidof_rgce_2026_anexos_21_30", "mx_snice_immex"}
            )
        )

    def test_offline_validator_rejects_remote_runtime_assets(self) -> None:
        script = ROOT / "scripts" / "verify_offline_site.py"
        self.assertTrue(script.is_file())

        from scripts.verify_offline_site import verify_offline_site

        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            (site / "index.html").write_text(
                '<html><head><script src="https://cdn.example/a.js"></script></head></html>',
                encoding="utf-8",
            )
            (site / "search").mkdir()
            (site / "search" / "search_index.js").write_text("", encoding="utf-8")
            findings = verify_offline_site(site)
        self.assertTrue(any("remote runtime asset" in item for item in findings))

    def test_contributor_guide_documents_modern_github_review_practices(self) -> None:
        guide = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8").casefold()
        for phrase in (
            "rendered prose",
            "relative links",
            "permanent links",
            "task list",
            "build_knowledge_map --check",
            "mkdocs.offline.yml",
        ):
            self.assertIn(phrase.casefold(), guide)


if __name__ == "__main__":
    unittest.main()
