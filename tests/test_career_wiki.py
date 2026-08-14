import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "wiki"

PAGES = [
    "index.md",
    "incoterms.md",
    "tigie-nico.md",
    "aranceles.md",
    "rrna.md",
    "tlc-tmec.md",
    "reglas-de-origen.md",
    "prosec.md",
    "immex.md",
    "pedimento-rgce.md",
    "logistica-internacional.md",
    "valor-en-aduana.md",
    "padron-importadores.md",
    "cuotas-compensatorias.md",
    "pagos-internacionales.md",
    "anam.md",
    "sistema-armonizado.md",
]

HEADINGS = (
    "## Qué es",
    "## Cómo aplica en México",
    "## Fuentes oficiales",
    "## Ver también",
)


class CareerWikiTests(unittest.TestCase):
    def test_pages_exist_with_skeleton_and_citation(self):
        for name in PAGES:
            path = DOCS / name
            self.assertTrue(path.is_file(), name)
            text = path.read_text(encoding="utf-8")
            self.assertIn("docs/catalog/", text, name)
            if name == "index.md":
                self.assertIn("https://", text)
                self.assertIn("No es asesoría legal", text)
                continue
            for heading in HEADINGS:
                self.assertIn(heading, text, f"{name} missing {heading}")
            self.assertIn("https://", text, name)
            self.assertIn("No es asesoría legal", text, name)
            self.assertNotIn("linkedin.com/learning", text.lower(), name)

    def test_corroborated_official_urls(self):
        blob = "\n".join((DOCS / name).read_text(encoding="utf-8") for name in PAGES)
        self.assertNotIn("https://www.gob.mx/anam", blob)
        self.assertIn("https://anam.gob.mx/", blob)
        self.assertIn("https://sidof.segob.gob.mx/notas/5777199", blob)
        self.assertIn("https://sidof.segob.gob.mx/notas/5778300", blob)
        self.assertIn("PadronImportadoresExportadores", blob)
        self.assertIn("unidad-de-practicas-comerciales-internacionales-upci", blob)
        self.assertIn("ligie.info22.html", (DOCS / "tigie-nico.md").read_text(encoding="utf-8"))
        self.assertNotIn("Consulta operativa", blob)


if __name__ == "__main__":
    unittest.main()
