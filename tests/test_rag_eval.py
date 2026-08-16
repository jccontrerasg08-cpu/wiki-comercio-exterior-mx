import tempfile
import unittest
from datetime import date
from pathlib import Path

from scripts.rag_eval import documents_from_repository, evaluate_cases, rank_documents, retrieve_case, tokenize


DOCUMENTS = [
    {
        "source_id": "mx_diputados_reg_ley_aduanera",
        "title": "Reglamento de la Ley Aduanera consolidado",
        "text": "reglamento aduanero despacho agentes aduanales",
        "effective_from": "2015-06-20",
        "effective_to": None,
    },
    {
        "source_id": "mx_sidof_rla_reform_20260223",
        "title": "Reforma al Reglamento de la Ley Aduanera 2026",
        "text": "reforma reglamento aduanero obligaciones agentes agencias",
        "effective_from": "2026-02-24",
        "effective_to": None,
    },
]

CASES = [
    {
        "id": "rla-before",
        "query": "reglamento aduanero",
        "cutoff": "2026-02-23",
        "expected_source_ids": ["mx_diputados_reg_ley_aduanera"],
    },
    {
        "id": "rla-after",
        "query": "reforma obligaciones agencias aduanales",
        "cutoff": "2026-02-24",
        "expected_source_ids": ["mx_sidof_rla_reform_20260223"],
    },
]


class RagEvaluationTests(unittest.TestCase):
    def test_tokenization_normalizes_accents(self):
        self.assertEqual(tokenize("Clasificación aduanera"), tokenize("clasificacion aduanera"))

    def test_future_source_is_excluded(self):
        ranked = rank_documents("reglamento aduanero", DOCUMENTS, date(2026, 2, 23), 5)
        self.assertNotIn(
            "mx_sidof_rla_reform_20260223", [item.source_id for item in ranked]
        )

    def test_metrics_use_hand_checked_expected_ids(self):
        report = evaluate_cases(CASES, DOCUMENTS, k=3)
        self.assertEqual(report.recall_at_k, 1.0)
        self.assertEqual(report.temporal_accuracy, 1.0)
        self.assertEqual(report.citation_coverage, 1.0)

    def test_forbidden_ranked_source_fails_case(self):
        cases = [{
            "id": "forbidden",
            "query": "reglamento aduanero",
            "cutoff": "2026-02-24",
            "expected_source_ids": ["mx_diputados_reg_ley_aduanera"],
            "forbidden_source_ids": ["mx_sidof_rla_reform_20260223"],
        }]
        report = evaluate_cases(cases, DOCUMENTS, k=5)
        self.assertTrue(any("forbidden" in finding for finding in report.failures))
        self.assertLess(report.temporal_accuracy, 1.0)

    def test_mutable_current_consolidation_is_not_backdated(self):
        documents = documents_from_repository(Path(__file__).resolve().parents[1])
        ranked = rank_documents("Ley de Comercio Exterior vigente", documents, date(1994, 1, 1), 10)
        self.assertNotIn("mx_diputados_lce_current", [item.source_id for item in ranked])

    def test_repository_documents_include_governed_content(self):
        documents = documents_from_repository(Path(__file__).resolve().parents[1])
        rla = next(item for item in documents if item["source_id"] == "mx_sidof_rla_reform_20260223")
        self.assertIn("agencias aduanales", rla["text"].casefold())

    def test_grouped_source_uses_governed_page_titles_for_search(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "sources").mkdir()
            (root / "docs").mkdir()
            (root / "sources" / "registry.yaml").write_text(
                """sources:\n  - id: mx_bundle\n    jurisdiction: MEX\n    title: Anexos 21-30 RGCE 2026\n    url: https://example.gob.mx/bundle\n    authority: Example\n    evidence_class: primary_legal\n    instrument_id: mx_rules\n    publication_date: 2026-01-15\n    allowed_hosts: [example.gob.mx]\n    media_types: [text/html]\n    harvest: false\n  - id: mx_single\n    jurisdiction: MEX\n    title: Anexo 1 RGCE 2026\n    url: https://example.gob.mx/single\n    authority: Example\n    evidence_class: primary_legal\n    instrument_id: mx_rules\n    publication_date: 2026-01-08\n    allowed_hosts: [example.gob.mx]\n    media_types: [text/html]\n    harvest: false\n""",
                encoding="utf-8",
            )
            (root / "sources" / "instruments.yaml").write_text(
                """instruments:\n  - id: mx_rules\n    jurisdiction: MEX\n    title: Reglas ejemplo\n    instrument_type: administrative_rules\n    status: current\n    publication_date: 2025-12-27\n    effective_from: 2026-01-01\n    effective_to: null\n    current_through: 2026-08-15\n    consolidated_source_id: mx_single\n    events:\n      - source_id: mx_bundle\n        relation: has_annex\n        effective_from: 2026-01-15\n""",
                encoding="utf-8",
            )
            (root / "sources" / "page_metadata.yaml").write_text(
                """pages:\n  - path: docs/anexo24.md\n    title: Anexo 24 control de inventarios SECIIT\n    source_ids: [mx_bundle]\n    source_status: current\n    legal_review_status: reviewed\n    corpus_status: current\n""",
                encoding="utf-8",
            )
            (root / "docs" / "anexo24.md").write_text(
                "apartado B SECIIT sistema corporativo 24 horas",
                encoding="utf-8",
            )

            documents = documents_from_repository(root)
            bundle = next(item for item in documents if item["source_id"] == "mx_bundle")
            ranked = rank_documents(
                "Anexo 24 2026 apartado B SECIIT 24 horas sistema corporativo",
                documents,
                date(2026, 8, 15),
                5,
            )

        self.assertIn("Anexo 24 control de inventarios SECIIT", bundle["search_title"])
        self.assertEqual(ranked[0].source_id, "mx_bundle")

    def test_repository_documents_exclude_stale_and_pending_text(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "sources").mkdir()
            (root / "docs").mkdir()
            (root / "sources" / "registry.yaml").write_text(
                """sources:\n  - id: mx_example_source\n    jurisdiction: MEX\n    title: Example source\n    url: https://example.gob.mx/source\n    authority: Example\n    evidence_class: official_consolidated\n    instrument_id: mx_example_instrument\n    publication_date: 2026-01-01\n    content_valid_from: 2026-01-01\n    allowed_hosts: [example.gob.mx]\n    media_types: [text/html]\n    harvest: false\n""",
                encoding="utf-8",
            )
            (root / "sources" / "instruments.yaml").write_text(
                """instruments:\n  - id: mx_example_instrument\n    jurisdiction: MEX\n    title: Example instrument\n    instrument_type: law\n    status: current\n    publication_date: 2026-01-01\n    effective_from: 2026-01-01\n    effective_to: null\n    current_through: 2026-08-15\n    consolidated_source_id: mx_example_source\n    events: []\n""",
                encoding="utf-8",
            )
            (root / "sources" / "page_metadata.yaml").write_text(
                """pages:\n  - path: docs/reviewed.md\n    source_ids: [mx_example_source]\n    source_status: current\n    legal_review_status: reviewed\n    corpus_status: current\n  - path: docs/stale.md\n    source_ids: [mx_example_source]\n    source_status: current\n    legal_review_status: reviewed\n    corpus_status: stale\n  - path: docs/pending.md\n    source_ids: [mx_example_source]\n    source_status: current\n    legal_review_status: pending_review\n    corpus_status: current\n""",
                encoding="utf-8",
            )
            (root / "docs" / "reviewed.md").write_text("eligible reviewed phrase", encoding="utf-8")
            (root / "docs" / "stale.md").write_text("stale forbidden phrase", encoding="utf-8")
            (root / "docs" / "pending.md").write_text("pending forbidden phrase", encoding="utf-8")

            documents = documents_from_repository(root)
            text = next(item for item in documents if item["source_id"] == "mx_example_source")["text"]

        self.assertIn("eligible reviewed phrase", text)
        self.assertNotIn("stale forbidden phrase", text)
        self.assertNotIn("pending forbidden phrase", text)

    def test_retrieval_result_emits_citations_and_abstention_disclaimer(self):
        cited = retrieve_case(CASES[1], DOCUMENTS, k=3)
        self.assertIn("mx_sidof_rla_reform_20260223", cited.cited_source_ids)
        abstained = retrieve_case(
            {"query": "antimateria lunar", "cutoff": "2026-02-24"},
            DOCUMENTS,
            k=3,
        )
        self.assertEqual(abstained.cited_source_ids, ())
        self.assertIn("No hay evidencia oficial pertinente", abstained.disclaimer)


if __name__ == "__main__":
    unittest.main()
