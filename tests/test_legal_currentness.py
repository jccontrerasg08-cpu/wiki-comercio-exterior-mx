import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data" / "corpus"


class LegalCurrentnessTests(unittest.TestCase):
    def test_ley_aduanera_currentness_metadata(self):
        text = (CORPUS / "ley-aduanera.md").read_text(encoding="utf-8")
        self.assertIn("**Última reforma:** DOF 19-11-2025", text)
        self.assertIn(
            "**Cantidades actualizadas por:** RGCE y Anexo 13 DOF 27-12-2025",
            text,
        )
        self.assertNotIn("**Última reforma:** DOF 12-11-2021", text)
        self.assertIn("digest_status: stale_pending_full_rebuild", text)

    def test_nom_documents_use_ley_infraestructura_calidad_as_current_framework(self):
        for filename in (
            "noms-comercio-exterior.md",
            "noms-maestro-anexo-241.md",
        ):
            with self.subTest(filename=filename):
                text = (CORPUS / filename).read_text(encoding="utf-8")
                self.assertIn("Ley de Infraestructura de la Calidad", text)
                self.assertIn("LFMN", text)
                self.assertIn("abrogada", text.lower())
                self.assertNotIn("**Marco legal:** Ley Federal sobre Metrología", text)

    def test_rgce_2026_prevalidation_amount_is_not_attributed_to_first_modification(self):
        text = (CORPUS / "anexo-13-multas-cantidades.md").read_text(
            encoding="utf-8"
        )
        false_attribution = (
            "la 1a. Resolución de Modificaciones a las RGCE 2026, DOF 14-05-2026, "
            "reformó la regla 1.8.3. para establecer este nuevo monto"
        )
        self.assertNotIn(false_attribution, text)
        self.assertIn("$350.00 de pago base por pedimento prevalidado", text)
        self.assertIn("$330.00", text)
        self.assertIn("$20.00", text)
        self.assertIn("RGCE 2026 originales", text)
        self.assertIn("no reformó la regla 1.8.3", text)

    def test_rgce_2026_anexo_13_uses_current_update_factor(self):
        text = (CORPUS / "anexo-13-multas-cantidades.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("**1.1321**", text)
        self.assertIn("**13.21%**", text)
        self.assertNotIn("**1.1245**", text)
        self.assertNotIn("**12.45%**", text)


if __name__ == "__main__":
    unittest.main()
