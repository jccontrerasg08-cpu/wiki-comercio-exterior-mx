import tempfile
import unittest
from pathlib import Path

import yaml

from scripts.coverage_report import (
    build_report,
    build_report_from_pages,
    evaluate_policy,
    render_json,
    render_markdown,
    risk_reasons,
    run_check,
    write_outputs,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "coverage" / "page_metadata.yaml"


def fixture_pages():
    return yaml.safe_load(FIXTURE.read_text(encoding="utf-8"))["pages"]


def write_fixture_repository(root: Path) -> None:
    pages = fixture_pages()
    (root / "sources").mkdir(parents=True)
    (root / "sources" / "page_metadata.yaml").write_text(
        FIXTURE.read_text(encoding="utf-8"), encoding="utf-8"
    )
    for page in pages:
        path = root / page["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# {page['title']}\n", encoding="utf-8")


def policy_for(report: dict) -> dict:
    summary = report["summary"]
    return {
        "policy_version": 1,
        "minimums": {
            "retrieval_eligible_pages": summary["retrieval_eligible_pages"],
            "pages_with_sources": summary["pages_with_sources"],
            "pages_with_instruments": summary["pages_with_instruments"],
            "legally_reviewed_pages": summary["legally_reviewed_pages"],
        },
        "maximums": {
            "pending_legal_review_pages": summary["pending_legal_review_pages"],
            "non_current_corpus_pages": summary["non_current_corpus_pages"],
            "unknown_source_status_pages": summary["unknown_source_status_pages"],
        },
    }


class CoverageReportTests(unittest.TestCase):
    def test_report_counts_statuses_sections_and_retrieval_eligibility(self):
        report = build_report_from_pages(fixture_pages())
        summary = report["summary"]

        self.assertEqual(summary["total_pages"], 5)
        self.assertEqual(summary["wiki_pages"], 4)
        self.assertEqual(summary["corpus_pages"], 1)
        self.assertEqual(summary["pages_with_sources"], 4)
        self.assertEqual(summary["pages_with_instruments"], 3)
        self.assertEqual(summary["retrieval_eligible_pages"], 3)
        self.assertEqual(summary["legally_reviewed_pages"], 4)
        self.assertEqual(summary["pending_legal_review_pages"], 1)
        self.assertEqual(summary["non_current_corpus_pages"], 2)
        self.assertEqual(summary["unknown_source_status_pages"], 0)
        self.assertEqual(report["latest_reviewed_at"], "2026-08-15")

        self.assertEqual(report["status_counts"]["legal_review_status"], {
            "pending_review": 1,
            "reviewed": 4,
        })
        sections = {item["section"]: item for item in report["sections"]}
        self.assertEqual(sections["aduana"]["total_pages"], 2)
        self.assertEqual(sections["aduana"]["retrieval_eligible_pages"], 1)
        self.assertEqual(sections["corpus"]["total_pages"], 1)

    def test_risk_reasons_are_deterministic_and_data_fixture_instrument_is_optional(self):
        pages = {page["path"]: page for page in fixture_pages()}
        self.assertEqual(
            risk_reasons(pages["docs/wiki/aduana/pending.md"]),
            ("corpus_not_current", "extraction_incomplete", "pending_legal_review"),
        )
        self.assertEqual(
            risk_reasons(pages["docs/wiki/rrna/stale.md"]),
            ("corpus_not_current", "source_not_current"),
        )
        self.assertEqual(
            risk_reasons(pages["docs/wiki/logistica/missing-links.md"]),
            ("missing_instrument_reference", "missing_source_reference"),
        )
        self.assertEqual(risk_reasons(pages["data/corpus/reference.md"]), ())

    def test_policy_allows_improvement_and_rejects_regression(self):
        report = build_report_from_pages(fixture_pages())
        policy = policy_for(report)
        self.assertEqual(evaluate_policy(report, policy), ())

        regression = {**report, "summary": dict(report["summary"])}
        regression["summary"]["retrieval_eligible_pages"] -= 1
        regression["summary"]["pending_legal_review_pages"] += 1
        findings = evaluate_policy(regression, policy)
        self.assertEqual(len(findings), 2)
        self.assertTrue(any("retrieval_eligible_pages" in item for item in findings))
        self.assertTrue(any("pending_legal_review_pages" in item for item in findings))

        improvement = {**report, "summary": dict(report["summary"])}
        improvement["summary"]["retrieval_eligible_pages"] += 1
        improvement["summary"]["pending_legal_review_pages"] -= 1
        self.assertEqual(evaluate_policy(improvement, policy), ())

    def test_renderers_are_deterministic_and_do_not_use_wall_clock_time(self):
        report = build_report_from_pages(fixture_pages())
        first_json = render_json(report)
        second_json = render_json(report)
        first_md = render_markdown(report)
        second_md = render_markdown(report)

        self.assertEqual(first_json, second_json)
        self.assertEqual(first_md, second_md)
        self.assertTrue(first_json.endswith("\n"))
        self.assertTrue(first_md.endswith("\n"))
        self.assertNotIn("generated_at", first_json)
        self.assertIn("Última revisión registrada", first_md)
        self.assertIn("No mide corrección jurídica sustantiva", first_md)
        self.assertIn("docs/wiki/aduana/pending.md", first_md)

    def test_write_and_check_detect_generated_drift(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_fixture_repository(root)
            report = build_report(root)
            (root / "coverage-policy.yaml").write_text(
                yaml.safe_dump(policy_for(report), sort_keys=False), encoding="utf-8"
            )
            write_outputs(root)
            self.assertEqual(run_check(root).exit_code, 0)

            (root / "reports" / "corpus-coverage.json").write_text("{}\n", encoding="utf-8")
            result = run_check(root)
            self.assertEqual(result.exit_code, 1)
            self.assertIn("corpus-coverage.json", result.message)

    def test_real_repository_report_matches_governed_inventory(self):
        report = build_report(ROOT)
        self.assertGreater(report["summary"]["total_pages"], 50)
        self.assertEqual(report["summary"]["total_pages"], len(report["pages"]))
        self.assertGreater(report["summary"]["pages_with_sources"], 0)
        self.assertGreater(report["summary"]["legally_reviewed_pages"], 0)


if __name__ == "__main__":
    unittest.main()
