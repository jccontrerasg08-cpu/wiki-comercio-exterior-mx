from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\wÁÉÍÓÚÜÑáéíóúüñ-]+\b", text))


class WikiLegalDepthTests(unittest.TestCase):
    def test_padron_explains_general_rule_and_exceptions(self):
        text = read("docs/wiki/fundamentos/padron-importadores.md")
        self.assertNotIn("Sin inscripción vigente, el pedimento no procede", text)
        for marker in ("Como regla general", "1.3.1", "1.3.5", "1.3.6", "Anexo 7", "Anexo 8", "Anexo 9"):
            self.assertIn(marker, text)

    def test_cuotas_are_not_presented_as_part_of_tigie_tariff(self):
        text = read("docs/wiki/contribuciones/cuotas-compensatorias.md")
        self.assertIn("separ", text.lower())
        for marker in ("resolución", "origen", "productor", "exportador", "vigencia", "excepc"):
            self.assertIn(marker, text.lower())
        self.assertNotIn("Se suman al arancel TIGIE cuando la fracción y el país coinciden", text)

    def test_aranceles_distinguishes_igi_from_compensatory_duties(self):
        text = read("docs/wiki/contribuciones/aranceles.md")
        self.assertIn("IGI", text)
        self.assertIn("cuotas compensatorias", text.lower())
        self.assertIn("distint", text.lower())

    def test_incoterms_does_not_determine_customs_procedure_by_itself(self):
        text = read("docs/wiki/logistica/incoterms.md")
        self.assertIn("no determina", text.lower())
        self.assertIn("procedimiento aduanero", text.lower())
        self.assertIn("valor en aduana", text.lower())

    def test_documentary_credit_page_cites_ucp_600(self):
        text = read("docs/wiki/logistica/pagos-internacionales.md")
        self.assertIn("UCP 600", text)
        self.assertIn("document", text.lower())
        self.assertIn("banco", text.lower())

    def test_2026_timeline_contains_major_verified_events(self):
        text = read("docs/wiki/aduana/cambios-2026.md")
        for marker in ("31 de marzo", "159 bis", "23 de abril", "185 fracciones", "4 de mayo", "Ventanilla Única", "14 de mayo", "20 de mayo"):
            self.assertIn(marker, text)

    def test_high_risk_new_pages_exist_and_are_substantive(self):
        pages = {
            "docs/wiki/aduana/vucem.md": 450,
            "docs/wiki/aduana/agente-agencia-aduanal.md": 550,
            "docs/wiki/aduana/manifestacion-valor.md": 450,
            "docs/wiki/aduana/proceso-despacho.md": 650,
            "docs/wiki/aduana/infracciones-pama.md": 550,
        }
        for path, minimum in pages.items():
            with self.subTest(path=path):
                file_path = ROOT / path
                self.assertTrue(file_path.exists(), path)
                self.assertGreaterEqual(word_count(file_path.read_text(encoding="utf-8")), minimum)

    def test_customs_valuation_is_deep_enough_for_the_topic(self):
        text = read("docs/wiki/contribuciones/valor-en-aduana.md")
        self.assertGreaterEqual(word_count(text), 900)
        for marker in ("valor de transacción", "mercancías idénticas", "mercancías similares", "método deductivo", "método computado", "último recurso", "Ejemplo"):
            self.assertIn(marker, text)

    def test_new_pages_are_in_mkdocs_navigation(self):
        config = read("mkdocs.yml")
        for path in (
            "wiki/aduana/vucem.md",
            "wiki/aduana/agente-agencia-aduanal.md",
            "wiki/aduana/manifestacion-valor.md",
            "wiki/aduana/proceso-despacho.md",
            "wiki/aduana/infracciones-pama.md",
        ):
            self.assertIn(path, config)


if __name__ == "__main__":
    unittest.main()
