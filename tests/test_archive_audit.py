import tempfile
import unittest
from pathlib import Path

from scripts.archive_audit import audit_registry, render_missing_report


REGISTRY = """sources:
  - id: already_local
    jurisdiction: MEX
    title: Already archived law
    url: https://example.gob.mx/law.pdf
    authority: Example
    evidence_class: primary_legal
    instrument_id: law_one
    publication_date: 2026-01-01
    allowed_hosts: [example.gob.mx]
    media_types: [application/pdf]
    harvest: true
    cadence_days: 30
  - id: missing_primary
    jurisdiction: MEX
    title: Missing decree
    url: https://example.gob.mx/missing.pdf
    authority: Example
    evidence_class: primary_legal
    instrument_id: law_one
    publication_date: 2026-02-01
    allowed_hosts: [example.gob.mx]
    media_types: [application/pdf]
    harvest: true
    cadence_days: 30
  - id: equivalent_primary
    jurisdiction: MEX
    title: Publication event preserved elsewhere
    url: https://example.gob.mx/event
    authority: Example Gazette
    evidence_class: primary_legal
    instrument_id: law_one
    publication_date: 2026-03-01
    allowed_hosts: [example.gob.mx]
    media_types: [text/html]
    harvest: true
    cadence_days: 30
  - id: intentional_external
    jurisdiction: MEX
    title: Interactive portal
    url: https://example.gob.mx/portal
    authority: Example
    evidence_class: official_operational
    allowed_hosts: [example.gob.mx]
    media_types: [text/html]
    harvest: false
    archive:
      status: external_only
      reason: Interactive service; no stable source document.
  - id: operational_unclassified
    jurisdiction: MEX
    title: Another portal
    url: https://example.gob.mx/portal-2
    authority: Example
    evidence_class: official_operational
    allowed_hosts: [example.gob.mx]
    media_types: [text/html]
    harvest: false
  - id: old_primary
    jurisdiction: MEX
    title: Historical superseded source
    url: https://example.gob.mx/old.pdf
    authority: Example Gazette
    evidence_class: primary_legal
    instrument_id: old_law
    publication_date: 2025-01-01
    allowed_hosts: [example.gob.mx]
    media_types: [application/pdf]
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
    current_through: 2026-03-01
    consolidated_source_id: already_local
    events:
      - source_id: missing_primary
        relation: amends
        effective_from: 2026-02-02
      - source_id: equivalent_primary
        relation: amends
        effective_from: 2026-03-02
      - source_id: intentional_external
        relation: implements
        effective_from: 2026-03-02
  - id: old_law
    jurisdiction: MEX
    title: Old law
    instrument_type: law
    status: superseded
    publication_date: 2025-01-01
    effective_from: 2025-01-02
    effective_to: 2025-12-31
    current_through: 2025-12-31
    consolidated_source_id: old_primary
    events: []
"""

MASTER = """fragments:
- example/MANIFEST.yaml
"""

LOCAL_PAYLOAD = b"official local bytes"
LOCAL_SHA256 = "1fb45711dd3d28e0f6440c23b2e027e9cf9ac55243504cfab0da8dc411f14d9b"

FRAGMENT = f"""documents:
- id: archived_copy
  file: example/law.pdf
  url: https://example.gob.mx/law.pdf
  sha256: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
  bytes: 123
- id: archived_equivalent
  file: example/event.pdf
  url: https://example.gob.mx/event.pdf
  sha256: bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
  bytes: 456
- id: verified_local_blob
  storage: local_git
  file: local.bin
  url: https://example.gob.mx/local.bin
  sha256: {LOCAL_SHA256}
  bytes: 20
"""

EQUIVALENTS = """equivalences:
  - source_id: equivalent_primary
    manifest_document_ids: [archived_equivalent]
    basis: Same official publication preserved as a stable PDF from the issuing authority.
"""


class ArchiveAuditTests(unittest.TestCase):
    def _write_fixture(self, root: Path) -> None:
        (root / "sources").mkdir(parents=True)
        (root / "data" / "originals" / "example").mkdir(parents=True)
        (root / "sources" / "registry.yaml").write_text(REGISTRY, encoding="utf-8")
        (root / "sources" / "instruments.yaml").write_text(INSTRUMENTS, encoding="utf-8")
        (root / "data" / "originals" / "manifest.yaml").write_text(MASTER, encoding="utf-8")
        (root / "data" / "originals" / "equivalents.yaml").write_text(
            EQUIVALENTS, encoding="utf-8"
        )
        (root / "data" / "originals" / "example" / "MANIFEST.yaml").write_text(
            FRAGMENT, encoding="utf-8"
        )
        (root / "data" / "originals" / "example" / "local.bin").write_bytes(LOCAL_PAYLOAD)

    def test_report_only_lists_genuinely_missing_active_primary_sources(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_fixture(root)
            rows = audit_registry(root)
            report = render_missing_report(rows)
        self.assertIn("`missing_primary`", report)
        self.assertNotIn("`already_local`", report)
        self.assertNotIn("`equivalent_primary`", report)
        self.assertNotIn("`old_primary`", report)
        self.assertNotIn("`intentional_external`", report)
        self.assertNotIn("`operational_unclassified`", report)

    def test_manifest_url_match_counts_as_preserved_even_when_ids_differ(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_fixture(root)
            rows = {row.source_id: row for row in audit_registry(root)}
        self.assertEqual(rows["already_local"].status, "archived_manifest")
        self.assertIn("example/MANIFEST.yaml", rows["already_local"].what_repo_has)

    def test_verified_equivalence_counts_as_preserved(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_fixture(root)
            rows = {row.source_id: row for row in audit_registry(root)}
        self.assertEqual(rows["equivalent_primary"].status, "archived_equivalent")
        self.assertIn("archived_equivalent", rows["equivalent_primary"].what_repo_has)
        self.assertIn("Same official publication", rows["equivalent_primary"].what_repo_has)

    def test_equivalence_with_unknown_manifest_document_is_configuration_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_fixture(root)
            path = root / "data" / "originals" / "equivalents.yaml"
            path.write_text(
                EQUIVALENTS.replace("archived_equivalent", "missing_manifest_id"),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "missing_manifest_id"):
                audit_registry(root)

    def test_local_git_manifest_accepts_exact_bytes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_fixture(root)
            rows = audit_registry(root)
        self.assertTrue(rows)

    def test_local_git_manifest_rejects_missing_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_fixture(root)
            (root / "data" / "originals" / "example" / "local.bin").unlink()
            with self.assertRaisesRegex(ValueError, "local_git.*missing"):
                audit_registry(root)

    def test_local_git_manifest_rejects_path_escape(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_fixture(root)
            manifest = root / "data" / "originals" / "example" / "MANIFEST.yaml"
            manifest.write_text(FRAGMENT.replace("file: local.bin", "file: ../../escape.bin"), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "escapes data/originals"):
                audit_registry(root)

    def test_local_git_manifest_rejects_wrong_size(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_fixture(root)
            manifest = root / "data" / "originals" / "example" / "MANIFEST.yaml"
            manifest.write_text(FRAGMENT.replace("bytes: 20", "bytes: 21"), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "byte count mismatch"):
                audit_registry(root)

    def test_local_git_manifest_rejects_wrong_sha256(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_fixture(root)
            manifest = root / "data" / "originals" / "example" / "MANIFEST.yaml"
            manifest.write_text(FRAGMENT.replace(LOCAL_SHA256, "f" * 64), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "sha256 mismatch"):
                audit_registry(root)

    def test_superseded_only_sources_are_not_automatic_requests(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_fixture(root)
            rows = {row.source_id: row for row in audit_registry(root)}
        self.assertEqual(rows["old_primary"].status, "superseded_only")

    def test_explicit_external_only_is_never_reported_as_missing_primary(self):
        registry = REGISTRY.replace(
            "evidence_class: official_operational\n    allowed_hosts",
            "evidence_class: primary_legal\n    instrument_id: law_one\n    allowed_hosts",
            1,
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_fixture(root)
            (root / "sources" / "registry.yaml").write_text(registry, encoding="utf-8")
            rows = {row.source_id: row for row in audit_registry(root)}
        self.assertEqual(rows["intentional_external"].status, "external_only")

    def test_non_legal_operational_sources_are_not_automatic_document_requests(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_fixture(root)
            rows = {row.source_id: row for row in audit_registry(root)}
        self.assertEqual(rows["operational_unclassified"].status, "not_target")

    def test_report_contains_exact_request_context_fields(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_fixture(root)
            report = render_missing_report(audit_registry(root))
        self.assertIn("Authority", report)
        self.assertIn("Published", report)
        self.assertIn("What the repository has", report)
        self.assertIn("What is missing", report)
        self.assertIn("Why it is needed", report)
        self.assertIn("law_one", report)
        self.assertIn("Archived through verified official equivalence", report)
        self.assertIn("Superseded-only sources kept out of auto-request", report)


if __name__ == "__main__":
    unittest.main()
