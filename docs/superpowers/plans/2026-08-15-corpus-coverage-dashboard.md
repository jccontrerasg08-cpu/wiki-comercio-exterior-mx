# Corpus Coverage Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a deterministic public + machine-readable corpus governance dashboard with CI regression gates.

**Architecture:** Add one focused `scripts.coverage_report.py` module that consumes canonical `sources/page_metadata.yaml`, reuses page-metadata validation, computes one report model, renders JSON and Markdown from that model, and evaluates `coverage-policy.yaml`. Generated files are committed and verified in CI and before Pages deployment.

**Tech Stack:** Python 3.12 stdlib, PyYAML 6.0.3, unittest, MkDocs Material.

## Global Constraints

- Do not change legal validity semantics or RAG eligibility semantics.
- Do not use wall-clock timestamps in generated outputs.
- Do not add network calls or new runtime dependencies.
- Treat dashboard metrics as governance/readiness indicators, not substantive legal correctness.
- Keep all generated output deterministic and reviewable in git.
- Keep one PR and preserve all existing CI, provenance, temporal, RAG, MkDocs strict, and legacy-route gates.

---

### Task 1: Coverage model and regression tests

**Files:**
- Create: `tests/fixtures/coverage/page_metadata.yaml`
- Create: `tests/test_coverage_report.py`
- Create: `scripts/coverage_report.py`

**Interfaces:**
- Produces: `build_report(root: Path) -> dict[str, object]`
- Produces: `risk_reasons(page: dict[str, object]) -> tuple[str, ...]`
- Produces: `evaluate_policy(report: dict[str, object], policy: dict[str, object]) -> tuple[str, ...]`

- [ ] **Step 1: Write fixture and failing unit tests** for deterministic totals, status distributions, retrieval eligibility, risk reasons, section grouping, and policy pass/fail.
- [ ] **Step 2: Run focused tests** with `python -m unittest tests.test_coverage_report -v` and confirm RED because `scripts.coverage_report` does not exist.
- [ ] **Step 3: Implement the smallest report model** using only canonical page metadata and existing validation.
- [ ] **Step 4: Re-run focused tests** and require PASS.
- [ ] **Step 5: Inspect the diff** for duplicated RAG eligibility semantics and keep the predicate byte-for-byte equivalent in behavior to `scripts.rag_eval._page_is_currently_retrievable`.

### Task 2: Deterministic renderers and drift check

**Files:**
- Modify: `scripts/coverage_report.py`
- Modify: `tests/test_coverage_report.py`
- Create: `reports/corpus-coverage.json`
- Create: `docs/status/corpus-coverage.md`

**Interfaces:**
- Produces: `render_json(report) -> str`
- Produces: `render_markdown(report, policy_findings=()) -> str`
- Produces: `run_check(root: Path) -> CheckResult`

- [ ] **Step 1: Add failing tests** proving stable ordering, trailing newline, no wall-clock field, and drift detection when either generated artifact differs.
- [ ] **Step 2: Run focused tests** and confirm RED for missing render/check functions.
- [ ] **Step 3: Implement canonical JSON and Markdown rendering** from the same report object.
- [ ] **Step 4: Implement CLI write/check modes**. `--check` must validate metadata, compare both generated outputs, evaluate policy, print summary, and exit 1 on any finding.
- [ ] **Step 5: Run focused tests** and require PASS.

### Task 3: Establish reviewed policy baseline

**Files:**
- Create: `coverage-policy.yaml`
- Modify: `reports/corpus-coverage.json`
- Modify: `docs/status/corpus-coverage.md`

**Interfaces:**
- Consumes exact current report metrics from `build_report`.
- Produces minimum floors and maximum ceilings that match current repository state.

- [ ] **Step 1: Run the report against the real repository** and capture current metrics.
- [ ] **Step 2: Set floors to current positive metrics** for retrieval eligibility, sourced pages, instrument-linked pages, and reviewed pages.
- [ ] **Step 3: Set ceilings to current risk counts** for pending review, non-current corpus states, and unknown source states.
- [ ] **Step 4: Generate the JSON and Markdown outputs** from the exact same report.
- [ ] **Step 5: Run `python -m scripts.coverage_report --check`** and require exit 0.

### Task 4: CI, Pages, and navigation integration

**Files:**
- Modify: `.github/workflows/ci.yml`
- Modify: `.github/workflows/pages.yml`
- Modify: `mkdocs.yml`
- Modify: `tests/test_workflows.py`
- Modify: `tests/test_mkdocs_ux.py`

**Interfaces:**
- CI/Pages command: `python -m scripts.coverage_report --check`
- Public route: `status/corpus-coverage.md`

- [ ] **Step 1: Add failing workflow/UI tests** requiring the coverage check in CI + Pages and `Estado del corpus` in navigation.
- [ ] **Step 2: Run affected tests** and confirm RED.
- [ ] **Step 3: Wire the coverage check** immediately after page provenance validation in both workflows.
- [ ] **Step 4: Add the dashboard to MkDocs navigation** without changing legacy redirects.
- [ ] **Step 5: Re-run affected tests** and require PASS.

### Task 5: Full verification and publication review

**Files:**
- Review all changed files only.

- [ ] **Step 1: Run full unittest discovery**: `python -m unittest discover -s tests -v`.
- [ ] **Step 2: Run repository integrity**: `python -m scripts.validate_repository --check`.
- [ ] **Step 3: Run catalog check**: `python -m scripts.build_catalog --check`.
- [ ] **Step 4: Run provenance check**: `python -m scripts.page_metadata --check`.
- [ ] **Step 5: Run coverage check**: `python -m scripts.coverage_report --check`.
- [ ] **Step 6: Run temporal graph**: `python -m scripts.temporal_graph --check`.
- [ ] **Step 7: Run temporal RAG evaluation**: `python -m scripts.rag_eval --check`.
- [ ] **Step 8: Run strict site build**: `mkdocs build --strict`.
- [ ] **Step 9: Run legacy route verification**: `python -m scripts.verify_site`.
- [ ] **Step 10: Review PR changed filenames and patches** for unrelated edits, secrets, generated drift, or semantic changes.
- [ ] **Step 11: Merge only with fresh green CI on the final head SHA**, then verify the main-branch Pages deployment succeeds.
