import re
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
SHA_ACTION = re.compile(r"^\s*uses:\s*[^\s]+@([0-9a-f]{40})(?:\s+#.*)?$", re.MULTILINE)
ANY_ACTION = re.compile(r"^\s*uses:\s*([^\s]+)@([^\s#]+)", re.MULTILINE)


def find_unpinned_actions(directory: Path) -> list[str]:
    findings = []
    for path in sorted(directory.glob("*.yml")):
        text = path.read_text(encoding="utf-8")
        for action, ref in ANY_ACTION.findall(text):
            if not re.fullmatch(r"[0-9a-f]{40}", ref):
                findings.append(f"{path.name}:{action}@{ref}")
    return findings


def find_pr_write_permissions(directory: Path) -> list[str]:
    findings = []
    for path in sorted(directory.glob("*.yml")):
        text = path.read_text(encoding="utf-8")
        if re.search(r"^\s{2}pull_request:\s*$", text, re.MULTILINE) and re.search(
            r"^\s{2,}[a-z-]+:\s*write\s*$", text, re.MULTILINE
        ):
            findings.append(path.name)
    return findings


def load_workflow(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def dump_workflow(value) -> str:
    return yaml.safe_dump(value)


class WorkflowPolicyTests(unittest.TestCase):
    def test_required_workflows_exist(self):
        expected = {"ci.yml", "pages.yml", "source-health.yml", "links.yml", "codeql.yml"}
        self.assertTrue(expected.issubset({path.name for path in WORKFLOWS.glob("*.yml")}))

    def test_all_third_party_actions_are_sha_pinned(self):
        self.assertEqual(find_unpinned_actions(WORKFLOWS), [])

    def test_pull_request_jobs_have_no_write_permissions(self):
        self.assertEqual(find_pr_write_permissions(WORKFLOWS), [])

    def test_external_checks_are_not_in_ci(self):
        ci = dump_workflow(load_workflow(WORKFLOWS / "ci.yml"))
        self.assertNotIn("source_health", ci)
        self.assertNotIn("legal_watch", ci)

    def test_scheduled_workflow_runs_due_monitor_and_legal_watch(self):
        workflow = dump_workflow(load_workflow(WORKFLOWS / "source-health.yml"))
        self.assertIn("--mode due", workflow)
        self.assertIn("scripts.legal_watch", workflow)

    def test_pages_runs_deterministic_gate_before_upload(self):
        text = (WORKFLOWS / "pages.yml").read_text(encoding="utf-8")
        upload = text.index("actions/upload-pages-artifact")
        for command in (
            "unittest discover",
            "scripts.validate_repository",
            "scripts.build_catalog --check",
            "scripts.page_metadata --check",
            "scripts.temporal_graph --check",
            "scripts.rag_eval --check",
        ):
            self.assertLess(text.index(command), upload)
        self.assertLess(text.index("scripts.verify_site"), upload)

    def test_codeql_scans_python_and_actions(self):
        workflow = dump_workflow(load_workflow(WORKFLOWS / "codeql.yml"))
        self.assertIn("python", workflow)
        self.assertIn("actions", workflow)

    def test_legacy_routes_are_configured(self):
        config = load_workflow(ROOT / "mkdocs.yml")
        redirects = next(item["redirects"] for item in config["plugins"] if isinstance(item, dict) and "redirects" in item)
        self.assertEqual(redirects["redirect_maps"]["aduana/documentos.md"], "wiki/aduana/documentos.md")


if __name__ == "__main__":
    unittest.main()
