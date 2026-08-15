import unittest
from datetime import date
from pathlib import Path

from scripts.temporal_graph import (
    load_instruments,
    sources_effective_on,
    validate_temporal_graph,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "temporal"


class TemporalGraphTests(unittest.TestCase):
    def test_rejects_event_after_current_through(self):
        findings = validate_temporal_graph(FIXTURES / "impossible-dates.yaml")
        self.assertEqual(findings[0].code, "EVENT_AFTER_CURRENT_THROUGH")

    def test_detects_supersession_cycle(self):
        findings = validate_temporal_graph(FIXTURES / "cycle.yaml")
        self.assertEqual(findings[0].code, "RELATION_CYCLE")

    def test_lce_uses_2026_reform_at_august_cutoff(self):
        instruments = {
            item["id"]: item
            for item in load_instruments(ROOT / "sources" / "instruments.yaml")
        }
        self.assertIn(
            "mx_sidof_lce_reform_20260501",
            sources_effective_on(
                instruments["mx_ley_comercio_exterior"], date(2026, 8, 15)
            ),
        )

    def test_real_graph_is_valid(self):
        self.assertEqual(validate_temporal_graph(ROOT), [])


if __name__ == "__main__":
    unittest.main()
