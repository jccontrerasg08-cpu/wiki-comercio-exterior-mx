import unittest
from datetime import date

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
        documents = documents_from_repository(__import__("pathlib").Path(__file__).resolve().parents[1])
        ranked = rank_documents("Ley de Comercio Exterior vigente", documents, date(1994, 1, 1), 10)
        self.assertNotIn("mx_diputados_lce_current", [item.source_id for item in ranked])

    def test_repository_documents_include_governed_content(self):
        documents = documents_from_repository(__import__("pathlib").Path(__file__).resolve().parents[1])
        rla = next(item for item in documents if item["source_id"] == "mx_sidof_rla_reform_20260223")
        self.assertIn("agencias aduanales", rla["text"].casefold())

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
