import tempfile
import unittest
from pathlib import Path

from scripts.build_catalog import render_library, render_registry, run_check


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
    archive:
      status: external_only
      reason: Interactive portal retained as a live reference.
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
    archive:
      status: release_asset
      release_tag: sources-2026-01-01
      asset_name: alpha.pdf
      sha256: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
      size_bytes: 123
      mime_type: application/pdf
      captured_at: 2026-01-01
  - id: local_source
    jurisdiction: MEX
    title: Beta
    url: https://example.gob.mx/beta.pdf
    authority: Example
    evidence_class: official_consolidated
    instrument_id: law_one
    publication_date: 2026-01-02
    content_valid_from: 2026-01-03
    allowed_hosts: [example.gob.mx]
    media_types: [application/pdf]
    harvest: false
    archive:
      status: local_git
      path: data/originals/beta.pdf
      sha256: bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
      size_bytes: 456
      mime_type: application/pdf
      captured_at: 2026-01-04
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

    def test_library_groups_sources_by_archive_state(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            registry = root / "registry.yaml"
            instruments = root / "instruments.yaml"
            registry.write_text(REGISTRY, encoding="utf-8")
            instruments.write_text(INSTRUMENTS, encoding="utf-8")
            first = render_library(registry, instruments)
            second = render_library(registry, instruments)
        self.assertEqual(first, second)
        self.assertIn("# Official document library", first)
        self.assertIn("## Local Git originals", first)
        self.assertIn("## GitHub Release assets", first)
        self.assertIn("## External-only references", first)
        self.assertIn("`local_source`", first)
        self.assertIn("sources-2026-01-01 / alpha.pdf", first)
        self.assertIn("Interactive portal retained as a live reference.", first)
        self.assertIn("bbbbbbbbbbbb", first)

    def test_library_has_stable_empty_state_for_unclassified_registry(self):
        registry_text = REGISTRY.replace(
            "    archive:\n      status: external_only\n      reason: Interactive portal retained as a live reference.\n",
            "",
        ).replace(
            "    archive:\n      status: release_asset\n      release_tag: sources-2026-01-01\n      asset_name: alpha.pdf\n      sha256: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n      size_bytes: 123\n      mime_type: application/pdf\n      captured_at: 2026-01-01\n",
            "",
        ).replace(
            "    archive:\n      status: local_git\n      path: data/originals/beta.pdf\n      sha256: bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n      size_bytes: 456\n      mime_type: application/pdf\n      captured_at: 2026-01-04\n",
            "",
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            registry = root / "registry.yaml"
            instruments = root / "instruments.yaml"
            registry.write_text(registry_text, encoding="utf-8")
            instruments.write_text(INSTRUMENTS, encoding="utf-8")
            library = render_library(registry, instruments)
        self.assertIn("No sources are classified in this archive state yet.", library)

    def test_check_detects_drift_in_either_generated_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "sources").mkdir()
            (root / "docs" / "catalog").mkdir(parents=True)
            (root / "sources" / "registry.yaml").write_text(REGISTRY, encoding="utf-8")
            (root / "sources" / "instruments.yaml").write_text(INSTRUMENTS, encoding="utf-8")
            (root / "docs" / "catalog" / "registry.md").write_text(
                render_registry(root / "sources" / "registry.yaml", root / "sources" / "instruments.yaml"),
                encoding="utf-8",
            )
            (root / "docs" / "catalog" / "library.md").write_text("stale\n", encoding="utf-8")
            result = run_check(root)
        self.assertEqual(result.exit_code, 1)
        self.assertIn("library.md", result.message)
        self.assertIn("regenerate with: python -m scripts.build_catalog", result.message)


if __name__ == "__main__":
    unittest.main()
