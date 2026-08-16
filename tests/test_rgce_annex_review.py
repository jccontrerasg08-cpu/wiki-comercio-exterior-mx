from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "sources" / "rgce_2026_annexes.yaml"
METADATA = ROOT / "sources" / "page_metadata.yaml"
INSTRUMENTS = ROOT / "sources" / "instruments.yaml"

ANNEX_PATHS = (
    "data/corpus/anexo-01-formatos-modelos.md",
    "data/corpus/anexo-02-tramites.md",
    "data/corpus/anexo-03-aduanas-pita.md",
    "data/corpus/anexo-04-horarios-aduanas.md",
    "data/corpus/anexo-05-criterios-practicas-indebidas.md",
    "data/corpus/anexo-06-consejo-clasificacion-arancelaria.md",
    "data/corpus/anexo-07-ejidatarios-sin-padron.md",
    "data/corpus/anexo-08-uso-exclusivo-importador-sin-padron.md",
    "data/corpus/anexo-09-exentos-igi-equipo-medico.md",
    "data/corpus/anexo-10-padron-sectorial.md",
    "data/corpus/anexo-11-rutas-fiscales-transito.md",
    "data/corpus/anexo-12-exportacion-temporal.md",
    "data/corpus/anexo-13-multas-cantidades.md",
    "data/corpus/anexo-14-hidrocarburos-petroliferos.md",
    "data/corpus/anexo-15-distancias-plazos-transito.md",
    "data/corpus/anexo-16-aduanas-transito-norte-sur.md",
    "data/corpus/anexo-17-sin-transito-internacional.md",
    "data/corpus/anexo-18-sin-deposito-fiscal.md",
    "data/corpus/anexo-19-datos-inexactos-multa-184.md",
    "data/corpus/anexo-20-marcas-nominativas.md",
    "data/corpus/anexo-21-aduanas-exclusivas.md",
    "data/corpus/anexo-22.md",
    "data/corpus/anexo-23-mercancias-peligrosas-muestreo.md",
    "data/corpus/anexo-24-control-inventarios-immex.md",
    "data/corpus/anexo-25-puntos-revision-franja.md",
    "data/corpus/anexo-26-noms-informacion-comercial.md",
    "data/corpus/anexo-27-fracciones-sin-iva.md",
    "data/corpus/anexo-28-mercancias-certificacion-iva-ieps.md",
    "data/corpus/anexo-29-regimenes-prohibidos.md",
    "data/corpus/anexo-30-scccyg.md",
)
COMPOSITES = (
    "data/corpus/anexos-formatos-tramites.md",
    "data/corpus/anexos-riesgo-logistica.md",
)


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


class RgceAnnexReviewTests(unittest.TestCase):
    def test_manifest_has_exactly_annexes_1_through_30(self):
        data = load_yaml(MANIFEST)
        items = data["annexes"]
        self.assertEqual([item["annex"] for item in items], list(range(1, 31)))
        self.assertEqual(len({item["title"] for item in items}), 30)
        self.assertEqual(len({item["corpus_path"] for item in items}), 30)

    def test_manifest_maps_official_publication_blocks(self):
        items = {item["annex"]: item for item in load_yaml(MANIFEST)["annexes"]}
        self.assertEqual(items[1]["publication_source_id"], "mx_sidof_rgce_2026_anexo_1")
        self.assertEqual(items[2]["publication_source_id"], "mx_sidof_rgce_2026_anexo_2")
        for annex in (*range(3, 13), *range(14, 21)):
            self.assertEqual(items[annex]["publication_source_id"], "mx_sidof_rgce_2026_anexos_3_20")
        self.assertEqual(items[13]["publication_source_id"], "mx_sidof_rgce_2026")
        for annex in range(21, 31):
            self.assertEqual(items[annex]["publication_source_id"], "mx_sidof_rgce_2026_anexos_21_30")

    def test_only_5_22_29_have_published_annex_modification(self):
        items = {item["annex"]: item for item in load_yaml(MANIFEST)["annexes"]}
        modified = {
            annex
            for annex, item in items.items()
            if "mx_sidof_rgce_2026_mod1_anexos" in item.get("modification_source_ids", [])
        }
        self.assertEqual(modified, {5, 22, 29})
        self.assertEqual(items[2].get("modification_source_ids", []), [])

    def test_manifest_is_reviewed_through_first_published_annex_modification(self):
        for item in load_yaml(MANIFEST)["annexes"]:
            self.assertEqual(str(item["reviewed_through"]), "2026-05-20")

    def test_modification_bundle_event_uses_dof_publication_date(self):
        instruments = {item["id"]: item for item in load_yaml(INSTRUMENTS)["instruments"]}
        rgce = instruments["mx_rgce_2026"]
        event = next(
            event for event in rgce["events"]
            if event["source_id"] == "mx_sidof_rgce_2026_mod1_anexos"
        )
        self.assertEqual(str(event["effective_from"]), "2026-05-20")

    def test_all_annex_and_composite_digests_are_governed_as_current_reviewed_partial_extractions(self):
        pages = {item["path"]: item for item in load_yaml(METADATA)["pages"]}
        for rel in (*ANNEX_PATHS, *COMPOSITES):
            with self.subTest(path=rel):
                page = pages[rel]
                self.assertEqual(page.get("source_status"), "current")
                self.assertEqual(page.get("extraction_status"), "partial")
                self.assertEqual(page.get("legal_review_status"), "reviewed")
                self.assertEqual(page.get("corpus_status"), "current")
                self.assertEqual(str(page.get("current_through")), "2026-05-20")

    def test_individual_digests_disclose_non_exhaustive_scope_and_current_review(self):
        for rel in ANNEX_PATHS:
            with self.subTest(path=rel):
                text = (ROOT / rel).read_text(encoding="utf-8").casefold()
                self.assertIn("estado al 15-08-2026", text)
                self.assertIn("digest no reproduce", text)
                self.assertIn("dof", text)

    def test_known_stale_or_unsafe_phrases_are_removed(self):
        corpus = "\n".join((ROOT / rel).read_text(encoding="utf-8") for rel in (*ANNEX_PATHS, *COMPOSITES))
        forbidden = (
            "Versión anticipada 2da Modificación",
            "1ra Modificación): https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/documentos2026/rgce/anexos/../anticipadas/1raModificacionalAnexo1",
            "No procede ninguno de los cuatro regímenes",
            "Puede destinarse al régimen solicitado",
            "Solo importación definitiva",
            "riesgo de PAMA",
            "Lógica para el chatbot",
            "Árbol de decisión para el chatbot",
        )
        for phrase in forbidden:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, corpus)

    def test_manifest_paths_match_the_30_individual_digests(self):
        manifest_paths = tuple(item["corpus_path"] for item in load_yaml(MANIFEST)["annexes"])
        self.assertEqual(manifest_paths, ANNEX_PATHS)


if __name__ == "__main__":
    unittest.main()
