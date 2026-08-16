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
"""

MASTER = """fragments:
- example/MANIFEST.yaml
"""

FRAGMENT = """documents:
- id: archived_copy
  file: example/law.pdf
  url: https://example.gob.mx/law.pdf
  sha256: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
  bytes: 123
"""


class ArchiveAuditTests(unittest.TestCase):
    def _write_fixture(self, root: Path) -> None:
        (root / "sources").mkdir(parents=True)
        (root / "data" / "originals" / "example").mkdir(parents=True)
        (root / "sources" / "registry.yaml").write_text(REGISTRY, encoding="utf-8")
        (root / "data" / "originals" / "manifest.yaml").write_text(MASTER, encoding="utf-8")
        (root / "data" / "originals" / "example" / "MANIFEST.yaml").write_text(
            FRAGMENT, encoding="utf-8"
        )

    def test_report_only_lists_genuinely_missing_primary_legal_sources(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_fixture(root)
            rows = audit_registry(root)
            report = render_missing_report(rows)
        self.assertIn("`missing_primary`", report)
        self.assertNotIn("`already_local`", report)
        self.assertNotIn("`intentional_external`", report)
        self.assertNotIn("`operational_unclassified`", report)

    def test_manifest_url_match_counts_as_preserved_even_when_ids_differ(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_fixture(root)
            rows = {row.source_id: row for row in audit_registry(root)}
        self.assertEqual(rows["already_local"].status, "archived_manifest")
        self.assertIn("example/MANIFEST.yaml", rows["already_local"].what_repo_has)

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


if __name__ == "__main__":
    unittest.main()
