import tempfile
import unittest
from pathlib import Path

from scripts.build_catalog import render_registry, run_check


REGISTRY = """sources:
  - id: snice_source
    jurisdiction: MEX
    title: Zeta
    url: https://www.snice.gob.mx/zeta
    note_id: null
    authority: SNICE
    evidence_class: official_operational
    allowed_hosts: [www.snice.gob.mx]
    media_types: [text/html]
    harvest: false
    cadence_days: 30
  - id: dof_source
    jurisdiction: MEX
    title: Alpha
    url: https://sidof.segob.gob.mx/notas/1
    note_id: "1"
    authority: DOF
    evidence_class: primary_legal
    instrument_ids: [law_one, program_one]
    publication_date: 2026-01-01
    allowed_hosts: [sidof.segob.gob.mx]
    media_types: [text/html]
    harvest: true
    cadence_days: 365
"""

INSTRUMENTS = """instruments:
  - id: law_one
    jurisdiction: MEX
    title: Law one
    instrument_type: law
    status: current
    publication_date: 2026-01-01
    effective_from: 2026-01-02
    effective_to: null
    current_through: 2026-01-02
    consolidated_source_id: dof_source
    events: []
  - id: program_one
    jurisdiction: MEX
    title: Program one
    instrument_type: program
    status: partial
    publication_date: 2026-01-01
    effective_from: 2026-01-02
    effective_to: null
    current_through: 2026-01-02
    consolidated_source_id: dof_source
    events: []
"""


class CatalogGenerationTests(unittest.TestCase):
    def test_render_is_deterministic_and_groups_by_authority(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            registry = root / "registry.yaml"
            instruments = root / "instruments.yaml"
            registry.write_text(REGISTRY, encoding="utf-8")
            instruments.write_text(INSTRUMENTS, encoding="utf-8")
            first = render_registry(registry, instruments)
            second = render_registry(registry, instruments)
        self.assertEqual(first, second)
        self.assertLess(first.index("## DOF"), first.index("## SNICE"))
        self.assertIn("law_one / current", first)
        self.assertIn("program_one / partial", first)
        self.assertTrue(first.endswith("\n"))
        self.assertFalse(first.endswith("\n\n"))

    def test_check_detects_drift(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "sources").mkdir()
            (root / "docs" / "catalog").mkdir(parents=True)
            (root / "sources" / "registry.yaml").write_text(REGISTRY, encoding="utf-8")
            (root / "sources" / "instruments.yaml").write_text(INSTRUMENTS, encoding="utf-8")
            (root / "docs" / "catalog" / "registry.md").write_text("stale\n", encoding="utf-8")
            result = run_check(root)
        self.assertEqual(result.exit_code, 1)
        self.assertIn("regenerate with: python -m scripts.build_catalog", result.message)


if __name__ == "__main__":
    unittest.main()
