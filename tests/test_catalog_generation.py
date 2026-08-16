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

RELEASES = """releases:
  - tag: originals-2026.01.01
    snapshot_date: 2026-01-01
    published_at: 2026-01-02T00:00:00Z
    assets:
      - name: originals-test.zip
        domains: [sat, sidof]
        sha256: cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        bytes: 789
        media_type: application/zip
"""

PRESERVATION_REGISTRY = """sources:
  - id: direct_source
    jurisdiction: MEX
    title: Directly preserved publication
    url: https://sidof.segob.gob.mx/notas/900
    note_id: "900"
    authority: DOF / SIDOF
    evidence_class: primary_legal
    instrument_id: law_one
    publication_date: 2026-01-05
    allowed_hosts: [sidof.segob.gob.mx]
    media_types: [text/html]
    harvest: true
    cadence_days: 365
  - id: equivalent_source
    jurisdiction: MEX
    title: Publication with official equivalent
    url: https://sidof.segob.gob.mx/notas/901
    note_id: "901"
    authority: DOF / SIDOF
    evidence_class: primary_legal
    instrument_id: law_one
    publication_date: 2026-01-06
    allowed_hosts: [sidof.segob.gob.mx]
    media_types: [text/html]
    harvest: true
    cadence_days: 365
"""

PRESERVATION_INSTRUMENTS = """instruments:
  - id: law_one
    jurisdiction: MEX
    title: Law one
    instrument_type: law
    status: current
    publication_date: 2026-01-01
    effective_from: 2026-01-02
    effective_to: null
    current_through: 2026-01-06
    consolidated_source_id: direct_source
    events:
      - source_id: equivalent_source
        publication_date: 2026-01-06
        effective_from: 2026-01-07
"""

PRESERVATION_MANIFEST = """documents:
  - id: manifest_direct
    file: direct.doc
    url: https://sidof.segob.gob.mx/notas/900
    title: Directly preserved publication
    sha256: dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
    bytes: 900
    license: official-not-relicensed
  - id: manifest_equivalent
    file: equivalent.pdf
    url: https://www.sat.gob.mx/equivalent.pdf
    title: Official equivalent copy
    sha256: eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
    bytes: 901
    license: official-not-relicensed
"""

PRESERVATION_EQUIVALENTS = """equivalences:
  - source_id: equivalent_source
    manifest_document_ids: [manifest_equivalent]
    basis: Official equivalent preserves the same bounded publication material.
"""


class CatalogGenerationTests(unittest.TestCase):
    def _write_fixture(self, root: Path, *, releases: bool = False) -> tuple[Path, Path]:
        (root / "sources").mkdir(parents=True, exist_ok=True)
        registry = root / "sources" / "registry.yaml"
        instruments = root / "sources" / "instruments.yaml"
        registry.write_text(REGISTRY, encoding="utf-8")
        instruments.write_text(INSTRUMENTS, encoding="utf-8")
        if releases:
            originals = root / "data" / "originals"
            originals.mkdir(parents=True)
            (originals / "releases.yaml").write_text(RELEASES, encoding="utf-8")
        return registry, instruments

    def _write_preservation_fixture(self, root: Path) -> tuple[Path, Path]:
        sources = root / "sources"
        sources.mkdir(parents=True)
        registry = sources / "registry.yaml"
        instruments = sources / "instruments.yaml"
        registry.write_text(PRESERVATION_REGISTRY, encoding="utf-8")
        instruments.write_text(PRESERVATION_INSTRUMENTS, encoding="utf-8")

        originals = root / "data" / "originals"
        manifest_dir = originals / "sidof" / "test"
        manifest_dir.mkdir(parents=True)
        (originals / "manifest.yaml").write_text(
            "fragments:\n  - sidof/test/MANIFEST.yaml\n", encoding="utf-8"
        )
        (manifest_dir / "MANIFEST.yaml").write_text(PRESERVATION_MANIFEST, encoding="utf-8")
        (originals / "equivalents.yaml").write_text(PRESERVATION_EQUIVALENTS, encoding="utf-8")
        return registry, instruments

    def test_render_is_deterministic_and_groups_by_authority(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            registry, instruments = self._write_fixture(root)
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
            registry, instruments = self._write_fixture(root)
            first = render_library(registry, instruments)
            second = render_library(registry, instruments)
        self.assertEqual(first, second)
        self.assertIn("# Official document library", first)
        self.assertIn("## Source-specific Local Git originals", first)
        self.assertIn("## Source-specific GitHub Release assets", first)
        self.assertIn("## External-only references", first)
        self.assertIn("`local_source`", first)
        self.assertIn("sources-2026-01-01 / alpha.pdf", first)
        self.assertIn("Interactive portal retained as a live reference.", first)
        self.assertIn("bbbbbbbbbbbb", first)

    def test_library_surfaces_manifest_and_equivalent_preservation(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            registry, instruments = self._write_preservation_fixture(root)
            library = render_library(registry, instruments)
        self.assertIn("## Sources preserved by document manifests", library)
        self.assertIn("`direct_source`", library)
        self.assertIn("data/originals/sidof/test/MANIFEST.yaml", library)
        self.assertIn("## Sources preserved through verified official equivalents", library)
        self.assertIn("`equivalent_source`", library)
        self.assertIn("manifest_equivalent", library)
        self.assertIn("Official equivalent preserves the same bounded publication material.", library)

    def test_library_surfaces_indexed_release_bundles(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            registry, instruments = self._write_fixture(root, releases=True)
            library = render_library(registry, instruments)
        self.assertIn("## Original-source release bundles", library)
        self.assertIn("originals-2026.01.01", library)
        self.assertIn("originals-test.zip", library)
        self.assertIn("sat, sidof", library)
        self.assertIn("cccccccccccc", library)

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
            (root / "sources").mkdir()
            registry = root / "sources" / "registry.yaml"
            instruments = root / "sources" / "instruments.yaml"
            registry.write_text(registry_text, encoding="utf-8")
            instruments.write_text(INSTRUMENTS, encoding="utf-8")
            library = render_library(registry, instruments)
        self.assertIn("No sources are classified in this archive state yet.", library)
        self.assertIn("## Unclassified sources", library)

    def test_library_surfaces_indexed_release_bundles(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            registry, instruments = self._write_fixture(root, releases=True)
            library = render_library(registry, instruments)
        self.assertIn("## Original-source release bundles", library)
        self.assertIn("originals-2026.01.01", library)
        self.assertIn("originals-test.zip", library)
        self.assertIn("sat, sidof", library)
        self.assertIn("cccccccccccc", library)

    def test_check_detects_drift_in_either_generated_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            registry, instruments = self._write_fixture(root)
            (root / "docs" / "catalog").mkdir(parents=True)
            (root / "docs" / "catalog" / "registry.md").write_text(
                render_registry(registry, instruments), encoding="utf-8"
            )
            (root / "docs" / "catalog" / "library.md").write_text("stale\n", encoding="utf-8")
            result = run_check(root)
        self.assertEqual(result.exit_code, 1)
        self.assertIn("library.md", result.message)
        self.assertIn("regenerate with: python -m scripts.build_catalog", result.message)


if __name__ == "__main__":
    unittest.main()
