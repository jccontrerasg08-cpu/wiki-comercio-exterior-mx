import hashlib
import io
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from scripts import validate_repository as validator

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "invalid"


class RepositoryValidatorTests(unittest.TestCase):
    def test_validator_module_exists(self):
        self.assertTrue(
            (ROOT / "scripts" / "validate_repository.py").is_file(),
            "scripts.validate_repository must exist",
        )

    def test_duplicate_source_id_is_rejected(self):
        validate_registry = getattr(validator, "validate_registry", None)
        self.assertIsNotNone(validate_registry, "validate_registry must exist")
        findings = validate_registry(FIXTURES / "duplicate-source-id.yaml")
        self.assertIn("REGISTRY_DUPLICATE_ID", {item.code for item in findings})

    def test_real_registry_has_no_structural_findings(self):
        validate_registry = getattr(validator, "validate_registry", None)
        self.assertIsNotNone(validate_registry, "validate_registry must exist")
        findings = validate_registry(ROOT / "sources" / "registry.yaml")
        self.assertEqual(findings, [])

    def test_registry_uses_local_json_schema(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "sources").mkdir()
            (root / "schemas").mkdir()
            shutil.copyfile(ROOT / "schemas" / "source.schema.json", root / "schemas" / "source.schema.json")
            (root / "sources" / "registry.yaml").write_text(
                "sources:\n  - id: Bad ID\n    jurisdiction: mexico\n    title: Test\n    url: https://example.com\n    authority: Test\n    evidence_class: primary_legal\n    allowed_hosts: [example.com]\n    media_types: [text/html]\n    harvest: false\n    unexpected: true\n",
                encoding="utf-8",
            )
            findings = validator.validate_registry(root / "sources" / "registry.yaml")
        self.assertIn("REGISTRY_SCHEMA", {item.code for item in findings})

    def test_invalid_manifest_sha_is_rejected(self):
        validate_manifest = getattr(validator, "validate_manifest", None)
        self.assertIsNotNone(validate_manifest, "validate_manifest must exist")
        findings = validate_manifest(FIXTURES / "invalid-sha256.yaml")
        self.assertIn("MANIFEST_SHA256", {item.code for item in findings})

    def test_real_manifest_fragments_have_valid_structure(self):
        validate_manifest = getattr(validator, "validate_manifest", None)
        self.assertIsNotNone(validate_manifest, "validate_manifest must exist")
        fragment_paths = [
            ROOT / "data" / "originals" / "diputados" / "MANIFEST.yaml",
            ROOT / "data" / "originals" / "sidof" / "5778300" / "MANIFEST.yaml",
            ROOT / "data" / "originals" / "tmec" / "MANIFEST.yaml",
        ]
        for path in fragment_paths:
            with self.subTest(path=path):
                self.assertEqual(validate_manifest(path), [])

    def test_missing_originals_fragment_is_rejected(self):
        validate_originals = getattr(validator, "validate_originals", None)
        self.assertIsNotNone(validate_originals, "validate_originals must exist")
        with tempfile.TemporaryDirectory() as temp_dir:
            originals = Path(temp_dir)
            shutil.copyfile(
                FIXTURES / "missing-fragment.yaml", originals / "manifest.yaml"
            )
            (originals / "SHA256SUMS").write_text("", encoding="utf-8")
            findings = validate_originals(originals)
        self.assertIn("ORIGINALS_MISSING_FRAGMENT", {item.code for item in findings})

    def test_real_originals_index_and_checksums_are_consistent(self):
        validate_originals = getattr(validator, "validate_originals", None)
        self.assertIsNotNone(validate_originals, "validate_originals must exist")
        findings = validate_originals(ROOT / "data" / "originals")
        self.assertEqual(findings, [])

    def test_official_binary_committed_under_originals_is_rejected(self):
        validate_hygiene = getattr(validator, "validate_repository_hygiene", None)
        self.assertIsNotNone(validate_hygiene, "validate_repository_hygiene must exist")
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            originals = root / "data" / "originals"
            originals.mkdir(parents=True)
            (originals / "example.PDF").write_bytes(b"not a real pdf")
            findings = validate_hygiene(root)
        self.assertIn("REPOSITORY_BINARY_IN_GIT", {item.code for item in findings})

    def _write_declared_local_binary(self, root: Path, *, wrong_sha: bool = False) -> None:
        originals = root / "data" / "originals"
        batch = originals / "batch"
        batch.mkdir(parents=True)
        payload = b"%PDF-1.7\nverified fixture bytes\n"
        digest = hashlib.sha256(payload).hexdigest()
        declared_digest = "f" * 64 if wrong_sha else digest
        (batch / "source.pdf").write_bytes(payload)
        (originals / "manifest.yaml").write_text(
            "fragments:\n- batch/MANIFEST.yaml\n", encoding="utf-8"
        )
        (originals / "SHA256SUMS").write_text("", encoding="utf-8")
        (batch / "MANIFEST.yaml").write_text(
            "documents:\n"
            "- id: declared_local\n"
            "  storage: local_git\n"
            "  file: source.pdf\n"
            "  url: https://example.gob.mx/source.pdf\n"
            f"  sha256: {declared_digest}\n"
            f"  bytes: {len(payload)}\n"
            "  license: official-not-relicensed\n"
            "  redistribution: Official source preserved for provenance.\n",
            encoding="utf-8",
        )

    def test_declared_verified_local_git_binary_is_allowed(self):
        validate_hygiene = getattr(validator, "validate_repository_hygiene", None)
        self.assertIsNotNone(validate_hygiene, "validate_repository_hygiene must exist")
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_declared_local_binary(root)
            findings = validate_hygiene(root)
        self.assertNotIn("REPOSITORY_BINARY_IN_GIT", {item.code for item in findings})

    def test_declared_local_git_checksum_mismatch_is_rejected(self):
        validate_originals = getattr(validator, "validate_originals", None)
        self.assertIsNotNone(validate_originals, "validate_originals must exist")
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_declared_local_binary(root, wrong_sha=True)
            findings = validate_originals(root / "data" / "originals")
        self.assertIn(
            "ORIGINALS_LOCAL_SHA256_MISMATCH", {item.code for item in findings}
        )

    def test_real_repository_has_no_undeclared_original_binary_payloads(self):
        validate_hygiene = getattr(validator, "validate_repository_hygiene", None)
        self.assertIsNotNone(validate_hygiene, "validate_repository_hygiene must exist")
        self.assertEqual(validate_hygiene(ROOT), [])

    def test_real_repository_passes_composed_validator(self):
        validate_all = getattr(validator, "validate_repository", None)
        self.assertIsNotNone(validate_all, "validate_repository must exist")
        self.assertEqual(validate_all(ROOT), [])

    def test_cli_reports_successful_domains(self):
        main = getattr(validator, "main", None)
        self.assertIsNotNone(main, "main must exist")
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            exit_code = main([str(ROOT)])
        self.assertEqual(exit_code, 0)
        output = stdout.getvalue()
        self.assertIn("PASS registry", output)
        self.assertIn("PASS originals", output)
        self.assertIn("PASS repository-hygiene", output)
        self.assertIn("PASS temporal-graph", output)
        self.assertIn("PASS page-metadata", output)
        self.assertIn("PASS generated-catalog", output)
        self.assertIn("Repository validation passed", output)


if __name__ == "__main__":
    unittest.main()
