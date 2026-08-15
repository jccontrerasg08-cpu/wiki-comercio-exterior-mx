from pathlib import Path
import re
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "docs" / "wiki"
GENERIC_DESCRIPTION = "Conocimiento temporal y verificable de comercio exterior mexicano."


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def front_matter(text: str) -> dict:
    if not text.startswith("---\n"):
        return {}
    _, raw, _ = text.split("---", 2)
    data = yaml.safe_load(raw) or {}
    return data if isinstance(data, dict) else {}


def words(text: str) -> int:
    body = re.sub(r"^---.*?---", "", text, flags=re.S)
    body = re.sub(r"[`#*_>|\[\](){}]", " ", body)
    return len(re.findall(r"\b[\wÁÉÍÓÚÜÑáéíóúüñ-]+\b", body))


class EditorialQualityTests(unittest.TestCase):
    def test_every_public_wiki_page_has_specific_description(self):
        descriptions = {}
        failures = []
        for path in sorted(WIKI.rglob("*.md")):
            meta = front_matter(read(path))
            description = str(meta.get("description", "")).strip()
            if not description or description == GENERIC_DESCRIPTION:
                failures.append(str(path.relative_to(ROOT)))
                continue
            descriptions.setdefault(description, []).append(str(path.relative_to(ROOT)))
        duplicates = {k: v for k, v in descriptions.items() if len(v) > 1}
        self.assertEqual([], failures, f"missing/generic descriptions: {failures}")
        self.assertEqual({}, duplicates, f"duplicate descriptions: {duplicates}")

    def test_substantive_wiki_pages_keep_sources_and_related_links(self):
        exceptions = {WIKI / "index.md"}
        failures = []
        for path in sorted(WIKI.rglob("*.md")):
            if path in exceptions:
                continue
            text = read(path)
            if not re.search(r"^## Fuentes(?: oficiales| de referencia| oficiales y multilaterales)?\b", text, re.M):
                failures.append(f"{path.relative_to(ROOT)}: sources")
            if "## Ver también" not in text:
                failures.append(f"{path.relative_to(ROOT)}: related")
        self.assertEqual([], failures)

    def test_reader_facing_wiki_index_is_concise(self):
        count = words(read(WIKI / "index.md"))
        self.assertGreaterEqual(count, 350)
        self.assertLessEqual(count, 650)
        self.assertNotIn("### Cómo iniciar un negocio de importación", read(WIKI / "index.md"))

    def test_content_roadmap_owns_coverage_gaps(self):
        roadmap = ROOT / "docs" / "status" / "content-roadmap.md"
        self.assertTrue(roadmap.exists())
        text = read(roadmap)
        self.assertIn("cubierto", text.lower())
        self.assertIn("hueco", text.lower())
        self.assertIn("Fuente oficial", text)

    def test_editorial_governance_documents_exist(self):
        required = {
            "docs/methodology/editorial-policy.md": ("Como regla general", "Excepciones", "Vigencia"),
            "docs/methodology/citation-policy.md": ("fuente primaria", "SIDOF", "texto consolidado"),
            "docs/methodology/page-review-checklist.md": ("current_through", "pending_review", "reviewed"),
            "docs/methodology/accessibility.md": ("WCAG 2.2 AA", "teclado", "reflow"),
            "docs/about/scope.md": ("arancel-mx", "fuente oficial", "no sustituye"),
        }
        for rel, markers in required.items():
            path = ROOT / rel
            with self.subTest(path=rel):
                self.assertTrue(path.exists(), rel)
                text = read(path)
                for marker in markers:
                    self.assertIn(marker, text)

    def test_known_false_absolutes_do_not_return(self):
        forbidden = (
            "Sin inscripción vigente, el pedimento no procede",
            "Se suman al arancel TIGIE cuando la fracción y el país coinciden",
            "El término pactado cambia el valor en aduana y quién tramita el pedimento",
            "Siempre (despacho definitivo)",
        )
        corpus = "\n".join(read(p) for p in WIKI.rglob("*.md"))
        for phrase in forbidden:
            self.assertNotIn(phrase, corpus)

    def test_no_project_subpath_robots_file(self):
        self.assertFalse((ROOT / "docs" / "robots.txt").exists())


if __name__ == "__main__":
    unittest.main()
