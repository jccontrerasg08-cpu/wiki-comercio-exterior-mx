# Temporal Legal Knowledge Platform Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver one integrated, provenance-first legal knowledge platform with temporal instrument metadata, current official-source coverage, deterministic documentation generation, offline validation, external-source monitoring, an integrated MkDocs site, and local RAG evaluation.

**Architecture:** Preserve the existing wiki, catalog, originals, and corpus responsibilities while adding a canonical instrument graph and JSON Schema contracts. Keep PR CI offline and deterministic; isolate all network checks in scheduled/manual workflows. Generate the registry catalog from canonical YAML and expose legal status without treating project-authored content as authoritative.

**Tech Stack:** Python 3.12, PyYAML 6.0.3, jsonschema 4.25.1, requests 2.34.2, MkDocs Material 9.7.7, GitHub Actions, JSON Schema Draft 2020-12.

## Global Constraints

- Use one integrated feature branch and one draft pull request.
- Keep structured tariff rows in `arancel-mx`; do not duplicate them here.
- Never scrape INEGI TIGIE-SCIAN, SNICE Mi Fraccion, ICC rule text, or WCO explanatory notes.
- Do not commit PDFs or other official binary payloads.
- DOF/SIDOF establishes publication; Diputados supplies consolidated text.
- Pull-request CI must not require network access.
- Every GitHub Action must use a full commit SHA.
- External downloads are untrusted and must have bounded time, redirects, and size.
- A successful HTTP response does not establish legal validity.
- No online LLM, API key, or embedding model is required for CI.

---

## File map

### Canonical data and schemas

- Create `schemas/source.schema.json`: source-record contract.
- Create `schemas/instrument.schema.json`: instrument/event temporal contract.
- Create `schemas/page-metadata.schema.json`: sidecar page metadata contract used during incremental front-matter migration.
- Create `sources/instruments.yaml`: canonical instrument and legal-event graph.
- Create `sources/page_metadata.yaml`: page provenance/status sidecar for all existing wiki and corpus pages.
- Modify `sources/registry.yaml`: add current core laws, regulations, SE rules, programs, and publication events.

### Python modules

- Create `scripts/schema_validation.py`: local-only Draft 2020-12 schema loading and deterministic error formatting.
- Create `scripts/temporal_graph.py`: instrument graph and temporal invariant validation.
- Create `scripts/build_catalog.py`: deterministic Markdown generation.
- Create `scripts/page_metadata.py`: page inventory and sidecar validation.
- Create `scripts/source_health.py`: bounded probes and content classification.
- Create `scripts/legal_watch.py`: official-candidate normalization and deduplication.
- Create `scripts/rag_eval.py`: lexical retrieval, temporal filtering, and metrics.
- Modify `scripts/validate_repository.py`: compose the new validation domains.

### Tests and fixtures

- Create `tests/test_schema_validation.py`.
- Create `tests/test_temporal_graph.py`.
- Create `tests/test_catalog_generation.py`.
- Create `tests/test_page_metadata.py`.
- Create `tests/test_source_health.py`.
- Create `tests/test_legal_watch.py`.
- Create `tests/test_rag_eval.py`.
- Create JSON/YAML/HTML fixtures under `tests/fixtures/` for valid and invalid cases.
- Create `evals/questions.yaml` with hand-checked expected source IDs and temporal cutoffs.

### Documentation

- Create `docs/index.md`, `docs/methodology/index.md`, `docs/methodology/status-model.md`, `docs/methodology/external-patterns.md`, `docs/changes/index.md`, and `docs/glossary.md`.
- Create core legal explainers under `docs/wiki/fundamentos/`, `docs/wiki/rrna/`, `docs/wiki/programas/`, `docs/wiki/aduana/`, and `docs/wiki/contribuciones/`.
- Generate `docs/catalog/registry.md`.
- Modify `mkdocs.yml`, `README.md`, `docs/wiki/index.md`, `docs/catalog/index.md`, and `docs/catalog/catalog.md`.
- Modify `CONTRIBUTING.md`; create `GOVERNANCE.md` and `MAINTAINERS.md`.

### Automation

- Modify `.github/workflows/ci.yml`.
- Create `.github/workflows/pages.yml`, `.github/workflows/source-health.yml`, `.github/workflows/links.yml`, and `.github/workflows/codeql.yml`.
- Create `.lychee.toml` and `sources/watch.yaml`.

---

### Task 1: Local JSON Schema validation foundation

**Files:**
- Create: `schemas/source.schema.json`
- Create: `schemas/instrument.schema.json`
- Create: `schemas/page-metadata.schema.json`
- Create: `scripts/schema_validation.py`
- Test: `tests/test_schema_validation.py`
- Create: `tests/fixtures/schema/invalid-source.yaml`
- Modify: `requirements-docs.txt`

**Interfaces:**
- Produces: `load_local_schema(root: Path, name: str) -> dict[str, object]`
- Produces: `validate_instance(instance: object, schema: dict[str, object], path: str) -> list[SchemaFinding]`
- Produces: immutable `SchemaFinding(code: str, path: str, message: str)`.
- Remote `$ref` retrieval is forbidden; schemas use local definitions only.

- [ ] **Step 1: Write failing schema tests**

```python
def test_invalid_source_reports_sorted_paths(self):
    schema = load_local_schema(ROOT, "source.schema.json")
    findings = validate_instance(
        {"id": "Bad ID", "url": "javascript:alert(1)", "harvest": "yes"},
        schema,
        "fixture",
    )
    self.assertEqual([f.path for f in findings], ["fixture.harvest", "fixture.id", "fixture.url"])

def test_format_validation_is_explicitly_enabled(self):
    schema = load_local_schema(ROOT, "source.schema.json")
    findings = validate_instance(
        {"id": "valid_id", "title": "x", "url": "not-a-uri", "authority": "DOF",
         "evidence_class": "primary_legal", "harvest": False},
        schema,
        "source",
    )
    self.assertEqual(findings[0].path, "source.url")
```

- [ ] **Step 2: Run the tests and confirm RED**

Run: `python -m unittest tests.test_schema_validation -v`
Expected: import failure for `scripts.schema_validation`.

- [ ] **Step 3: Add pinned dependency and schemas**

Add `jsonschema==4.25.1` and `requests==2.34.2` to `requirements-docs.txt`. Define Draft 2020-12 schemas with `additionalProperties: false`, lowercase underscore IDs, HTTPS URLs except explicitly allowlisted legacy HTTP catalog sources, ISO dates, closed status enums, and local `$defs`.

- [ ] **Step 4: Implement deterministic local validation**

Use `Draft202012Validator(schema, format_checker=FormatChecker())`, call `check_schema`, never configure a remote resolver, and format paths by joining mapping keys and list indexes. Sort by `(path, code, message)`.

- [ ] **Step 5: Verify GREEN**

Run: `python -m unittest tests.test_schema_validation -v`
Expected: all schema tests pass.

- [ ] **Step 6: Commit the slice**

Stage only the seven Task 1 paths and commit `feat: add local legal metadata schemas`.

### Task 2: Temporal instrument graph and current legal core

**Files:**
- Create: `scripts/temporal_graph.py`
- Create: `sources/instruments.yaml`
- Modify: `sources/registry.yaml`
- Test: `tests/test_temporal_graph.py`
- Create: `tests/fixtures/temporal/cycle.yaml`
- Create: `tests/fixtures/temporal/impossible-dates.yaml`

**Interfaces:**
- Consumes: `validate_instance` from Task 1.
- Produces: `load_instruments(path: Path) -> list[dict[str, object]]`.
- Produces: `validate_temporal_graph(root: Path) -> list[TemporalFinding]`.
- Produces: `sources_effective_on(instrument, cutoff: date) -> tuple[str, ...]`.

- [ ] **Step 1: Write failing temporal behavior tests**

```python
def test_rejects_event_after_current_through(self):
    findings = validate_temporal_graph(FIXTURES / "impossible-dates.yaml")
    self.assertEqual(findings[0].code, "EVENT_AFTER_CURRENT_THROUGH")

def test_detects_supersession_cycle(self):
    findings = validate_temporal_graph(FIXTURES / "cycle.yaml")
    self.assertEqual(findings[0].code, "RELATION_CYCLE")

def test_lce_uses_2026_reform_at_august_cutoff(self):
    instruments = {x["id"]: x for x in load_instruments(ROOT / "sources/instruments.yaml")}
    self.assertIn(
        "mx_sidof_lce_reform_20260501",
        sources_effective_on(instruments["mx_ley_comercio_exterior"], date(2026, 8, 15)),
    )
```

- [ ] **Step 2: Run and confirm RED**

Run: `python -m unittest tests.test_temporal_graph -v`
Expected: import failure for `scripts.temporal_graph`.

- [ ] **Step 3: Add verified official registry records**

Add records for:

- Constitution consolidated PDF.
- Customs Law Regulation consolidated PDF and SIDOF `5780677`.
- Foreign Trade Law consolidated PDF, its Regulation, and SIDOF `5786538`.
- CFF, VAT Law, IEPS Law, Federal Duties Law, and Infrastructure Quality Law consolidated PDFs.
- SE Rules and Criteria baseline plus known modifications through 2026-05-29.
- IMMEX, PROSEC, Drawback, importer register, VUCEM, and SNICE legal indexes.

Every source includes `instrument_id`, `publication_date` when known, `cadence_days`, authority, evidence class, allowed hosts, media types, and content probes. Use `cadence_days: 1` for active DOF event feeds, `7` for consolidated laws, and `30` for stable program indexes.

- [ ] **Step 4: Add canonical instruments**

Define at minimum: Constitution, Customs Law, Customs Law Regulation, LIGIE, RGCE 2025, RGCE 2026, Foreign Trade Law, Foreign Trade Law Regulation, CFF, VAT, IEPS, Federal Duties, Infrastructure Quality, SE Rules, IMMEX, PROSEC, Drawback, T-MEC, TIPAT, TLCUEM, UK continuity agreement, Japan, Chile, and Pacific Alliance. Mark incomplete families `partial` rather than `current`.

- [ ] **Step 5: Implement graph validation**

Validate unique IDs, source references, allowed relation types, date order, no supersession/amendment cycle, consolidated source existence, and `current_through >= latest included effective event`. The graph does not infer status from HTTP results.

- [ ] **Step 6: Verify GREEN and existing registry compatibility**

Run: `python -m unittest tests.test_temporal_graph tests.test_repository_validator -v`
Expected: all tests pass.

- [ ] **Step 7: Commit the slice**

Commit `feat: model temporal legal instruments` with only Task 2 paths.

### Task 3: Generated catalog as a single source of truth

**Files:**
- Create: `scripts/build_catalog.py`
- Create: `docs/catalog/registry.md`
- Modify: `docs/catalog/catalog.md`
- Modify: `docs/catalog/index.md`
- Test: `tests/test_catalog_generation.py`

**Interfaces:**
- Produces: `render_registry(registry_path: Path, instruments_path: Path) -> str`.
- Produces CLI: `python -m scripts.build_catalog [--check] [root]`.
- `--check` returns 1 and prints one stable message when committed output differs.

- [ ] **Step 1: Write failing generator tests**

```python
def test_render_is_deterministic_and_groups_by_authority(self):
    first = render_registry(FIXTURE_REGISTRY, FIXTURE_INSTRUMENTS)
    second = render_registry(FIXTURE_REGISTRY, FIXTURE_INSTRUMENTS)
    self.assertEqual(first, second)
    self.assertLess(first.index("## DOF"), first.index("## SNICE"))

def test_check_detects_drift(self):
    result = run_check(root=FIXTURE_DRIFT_ROOT)
    self.assertEqual(result.exit_code, 1)
    self.assertIn("regenerate with: python -m scripts.build_catalog", result.message)
```

- [ ] **Step 2: Run and confirm RED**

Run: `python -m unittest tests.test_catalog_generation -v`.

- [ ] **Step 3: Implement stable Markdown generation**

Sort authorities, then jurisdiction, title, and source ID. Render ID, title, authority, evidence class, harvest mode, cadence, publication date, and official URL. Do not render hashes that are not present. End with exactly one newline.

- [ ] **Step 4: Replace the manual registry snapshot**

Keep human guidance in `catalog.md`, remove its manually duplicated table, and link to generated `registry.md`.

- [ ] **Step 5: Generate and verify GREEN**

Run:

```bash
python -m scripts.build_catalog
python -m scripts.build_catalog --check
python -m unittest tests.test_catalog_generation -v
```

Expected: generated output is stable and tests pass.

- [ ] **Step 6: Commit the slice**

Commit `feat: generate the official source catalog`.

### Task 4: Complete page provenance inventory

**Files:**
- Create: `sources/page_metadata.yaml`
- Create: `scripts/page_metadata.py`
- Test: `tests/test_page_metadata.py`
- Create: `tests/fixtures/page-metadata/missing-page.yaml`
- Create: `docs/methodology/status-model.md`

**Interfaces:**
- Produces: `inventory_content_pages(root: Path) -> tuple[str, ...]`.
- Produces: `validate_page_metadata(root: Path) -> list[PageFinding]`.
- Every `docs/wiki/**/*.md` and `data/corpus/*.{md,csv}` except README files must have one sidecar record.

- [ ] **Step 1: Write failing inventory tests**

```python
def test_every_content_page_has_metadata(self):
    self.assertEqual(validate_page_metadata(ROOT), [])

def test_missing_page_is_reported(self):
    findings = validate_page_metadata(FIXTURES / "page-metadata")
    self.assertEqual(findings[0].code, "PAGE_NOT_FOUND")
```

- [ ] **Step 2: Run and confirm RED**

Run: `python -m unittest tests.test_page_metadata -v`.

- [ ] **Step 3: Implement inventory and validation**

Validate paths, source IDs, instrument IDs, dates, closed statuses, content type, and legal authority. Require `current_through` for `current` corpus pages. Reject a page marked current when its instrument has a later known effective event.

- [ ] **Step 4: Inventory all current pages**

Generate a temporary list, then author reviewed metadata records. Use `unknown` or `partial` rather than inventing certainty. Preserve `stale_pending_full_rebuild` by mapping it to `corpus_status: stale` and `legal_review_status: pending_review`.

- [ ] **Step 5: Document the status semantics**

Explain independently: source availability, legal status, extraction completeness, review status, and corpus status. Include examples of a current source with stale digest and a superseded source retained for historical queries.

- [ ] **Step 6: Verify GREEN**

Run: `python -m unittest tests.test_page_metadata -v`.

- [ ] **Step 7: Commit the slice**

Commit `feat: inventory page provenance and status`.

### Task 5: External source health and legal candidate discovery

**Files:**
- Create: `scripts/source_health.py`
- Create: `scripts/legal_watch.py`
- Create: `sources/watch.yaml`
- Test: `tests/test_source_health.py`
- Test: `tests/test_legal_watch.py`
- Create: `tests/fixtures/http/valid-dof.html`
- Create: `tests/fixtures/http/soft-404.html`
- Create: `tests/fixtures/http/candidates.json`

**Interfaces:**
- Produces: `ProbePolicy(timeout_seconds=15, max_bytes=20_000_000, max_redirects=3)`.
- Produces: `classify_response(source, response, body) -> ProbeResult`.
- Produces: `probe_source(source, transport, policy) -> ProbeResult` with injected transport.
- Produces: `normalize_candidates(payload, watch_config) -> tuple[Candidate, ...]`.
- Produces CLI JSON reports without issue creation logic.

- [ ] **Step 1: Write failing probe tests**

```python
def test_http_200_soft_404_is_suspicious(self):
    result = classify_response(SOURCE, response(status=200, mime="text/html"), SOFT_404)
    self.assertEqual(result.classification, "suspicious_response")

def test_oversized_response_stops_without_hashing(self):
    result = probe_source(SOURCE, OversizedTransport(), ProbePolicy(max_bytes=100))
    self.assertEqual(result.classification, "size_limit")
    self.assertIsNone(result.sha256)
```

- [ ] **Step 2: Write failing discovery tests**

```python
def test_candidates_are_deduplicated_by_note_id(self):
    candidates = normalize_candidates(load_fixture("candidates.json"), WATCH_CONFIG)
    self.assertEqual([x.note_id for x in candidates], ["5786538", "5787425"])

def test_discovery_never_marks_candidate_current(self):
    candidate = normalize_candidates(load_fixture("candidates.json"), WATCH_CONFIG)[0]
    self.assertEqual(candidate.review_status, "candidate")
```

- [ ] **Step 3: Run and confirm RED**

Run: `python -m unittest tests.test_source_health tests.test_legal_watch -v`.

- [ ] **Step 4: Implement bounded probing**

Use a session with explicit User-Agent, stream bodies, validate every redirect host against `allowed_hosts`, stop at the byte cap, reject invalid MIME and configured marker text, then hash valid bytes. Never log response bodies.

- [ ] **Step 5: Implement candidate normalization**

Normalize note IDs, Unicode titles, ISO dates, official URLs, matched keywords, and stable candidate keys. Compare with registry IDs and note IDs. Output candidates only; a workflow may create a review issue later.

- [ ] **Step 6: Verify GREEN**

Run: `python -m unittest tests.test_source_health tests.test_legal_watch -v`.

- [ ] **Step 7: Commit the slice**

Commit `feat: add bounded official source monitoring`.

### Task 6: Temporal RAG retrieval evaluation

**Files:**
- Create: `scripts/rag_eval.py`
- Create: `evals/questions.yaml`
- Test: `tests/test_rag_eval.py`

**Interfaces:**
- Produces: `tokenize(text: str) -> frozenset[str]` with Unicode normalization.
- Produces: `rank_documents(query, documents, cutoff, k) -> tuple[RankedDocument, ...]`.
- Produces: `evaluate_cases(cases, documents, k=5) -> EvaluationReport`.
- Report contains `recall_at_k`, `mean_reciprocal_rank`, `temporal_accuracy`, `citation_coverage`, and per-case failures.

- [ ] **Step 1: Write failing evaluation tests**

```python
def test_future_source_is_excluded(self):
    ranked = rank_documents("reglamento aduanero", DOCUMENTS, date(2026, 2, 23), 5)
    self.assertNotIn("mx_dof_rla_reform_20260223", [x.source_id for x in ranked])

def test_metrics_use_hand_checked_expected_ids(self):
    report = evaluate_cases(CASES, DOCUMENTS, k=3)
    self.assertEqual(report.recall_at_k, 1.0)
    self.assertEqual(report.temporal_accuracy, 1.0)
```

- [ ] **Step 2: Run and confirm RED**

Run: `python -m unittest tests.test_rag_eval -v`.

- [ ] **Step 3: Implement dependency-free lexical baseline**

Normalize with NFKD, remove combining marks, lowercase, tokenize alphanumeric terms, remove a small checked Spanish stopword set, score Jaccard plus exact source-title term overlap, and use source ID as the deterministic tie-breaker.

- [ ] **Step 4: Author evaluation cases**

Include RGCE 2025/2026 confusion, RLA before/after 2026-02-24, LCE before/after 2026-05-02, law versus regulation versus rules, Anexo 24/30, NOM framework, and abstention when evidence is absent.

- [ ] **Step 5: Verify GREEN**

Run: `python -m unittest tests.test_rag_eval -v`.

- [ ] **Step 6: Commit the slice**

Commit `feat: evaluate temporal source retrieval`.

### Task 7: Integrated documentation site and essential explainers

**Files:**
- Create: `docs/index.md`
- Create: `docs/methodology/index.md`
- Create: `docs/methodology/external-patterns.md`
- Create: `docs/changes/index.md`
- Create: `docs/glossary.md`
- Create: `docs/wiki/fundamentos/marco-juridico.md`
- Create: `docs/wiki/rrna/index.md`
- Create: `docs/wiki/rrna/reglas-criterios-se.md`
- Create: `docs/wiki/rrna/anexo-2-2-1.md`
- Create: `docs/wiki/rrna/anexo-2-4-1.md`
- Create: `docs/wiki/programas/drawback.md`
- Create: `docs/wiki/aduana/regimenes-aduaneros.md`
- Create: `docs/wiki/aduana/cambios-2026.md`
- Create: `docs/wiki/contribuciones/impuestos-importacion.md`
- Modify: `mkdocs.yml`
- Modify: `README.md`
- Modify: `docs/wiki/index.md`

**Interfaces:**
- MkDocs root becomes `docs/`.
- Existing wiki paths move only in navigation, not on disk.
- Every explainer cites official URLs/source IDs, states current-through date, and separates facts, operational implications, and verification steps.

- [ ] **Step 1: Update navigation and create the site home**

Use `docs_dir: docs`; navigation paths start with `wiki/`, `catalog/`, `methodology/`, and `changes/`. Enable search, navigation sections, content tabs, admonitions, tables, and attribute lists without adding unpinned plugins.

- [ ] **Step 2: Write methodology and external-pattern notes**

Document ideas adapted from OASIS LegalDocML, python-jsonschema, MkDocs Material, Lychee, CodeQL, OpenSSF Scorecard, and RAG evaluation repositories. Record direct URL, license, adopted pattern, rejected pattern, and local rationale.

- [ ] **Step 3: Write essential legal explainers from verified primary sources**

Cover the legal hierarchy, RRNA, SE Rules, Annexes 2.2.1 and 2.4.1, Drawback, customs regimes, import taxes, the 2026 RLA reform, and the 2026 LCE agroexport reform. Paraphrase; do not reproduce full official texts.

- [ ] **Step 4: Update provenance inventory for new pages**

Add records to `sources/page_metadata.yaml`; mark explainers `legal_authority: non_authoritative`.

- [ ] **Step 5: Build in strict mode**

Run: `python -m mkdocs build --strict`
Expected: exit 0, no missing navigation or local-link warning.

- [ ] **Step 6: Run page and catalog tests**

Run: `python -m unittest tests.test_page_metadata tests.test_catalog_generation -v`.

- [ ] **Step 7: Commit the slice**

Commit `docs: publish integrated trade knowledge site`.

### Task 8: Deterministic CI, scheduled monitoring, Pages, links, and security

**Files:**
- Modify: `.github/workflows/ci.yml`
- Create: `.github/workflows/pages.yml`
- Create: `.github/workflows/source-health.yml`
- Create: `.github/workflows/links.yml`
- Create: `.github/workflows/codeql.yml`
- Create: `.lychee.toml`
- Modify: `.github/dependabot.yml`
- Test: `tests/test_workflows.py`

**Interfaces:**
- CI runs all deterministic validators and MkDocs only.
- Source health and legal watch run on schedule/manual dispatch and upload JSON artifacts.
- Link check is scheduled/manual and does not block PR CI.
- Pages build has read-only permissions; deploy job alone gets `pages: write` and `id-token: write`.

- [ ] **Step 1: Write failing workflow-policy tests**

```python
def test_all_third_party_actions_are_sha_pinned(self):
    self.assertEqual(find_unpinned_actions(ROOT / ".github/workflows"), [])

def test_pull_request_jobs_have_no_write_permissions(self):
    self.assertEqual(find_pr_write_permissions(ROOT / ".github/workflows"), [])

def test_external_checks_are_not_in_ci(self):
    ci = load_workflow(ROOT / ".github/workflows/ci.yml")
    self.assertNotIn("source_health", dump_workflow(ci))
    self.assertNotIn("legal_watch", dump_workflow(ci))
```

- [ ] **Step 2: Run and confirm RED**

Run: `python -m unittest tests.test_workflows -v`.

- [ ] **Step 3: Resolve exact Action SHAs**

Resolve tags through GitHub's API and record comments with version names for checkout, setup-python, upload-pages-artifact, deploy-pages, upload-artifact, CodeQL init/analyze, Lychee, and cache. Never guess a SHA.

- [ ] **Step 4: Expand deterministic CI**

Run the full unittest discovery, repository validator, catalog `--check`, page metadata validation, temporal graph validation, RAG evaluation, and MkDocs strict build.

- [ ] **Step 5: Add scheduled workflows**

Use concurrency, timeouts, least privilege, bounded artifacts, and issue deduplication. Scheduled failures create or update a single issue keyed by report type; workflows never edit legal status.

- [ ] **Step 6: Add Pages and CodeQL**

Use the official artifact-based Pages deployment pattern and CodeQL `build-mode: none` for Python. Do not run deployment for pull requests.

- [ ] **Step 7: Verify GREEN and parse YAML**

Run:

```bash
python -m unittest tests.test_workflows -v
python -c "from pathlib import Path; import yaml; [yaml.safe_load(p.read_text()) for p in Path('.github/workflows').glob('*.yml')]"
```

- [ ] **Step 8: Commit the slice**

Commit `ci: add legal monitoring and secure documentation delivery`.

### Task 9: Governance, contribution safety, and repository integration

**Files:**
- Modify: `CONTRIBUTING.md`
- Create: `GOVERNANCE.md`
- Create: `MAINTAINERS.md`
- Modify: `SECURITY.md`
- Modify: `.github/PULL_REQUEST_TEMPLATE.md`
- Modify: `.github/ISSUE_TEMPLATE/catalog.yml`
- Modify: `.github/ISSUE_TEMPLATE/wiki.yml`
- Modify: `docs/ARCHITECTURE.md`

**Interfaces:**
- Contribution policy allows integrated source-family PRs when canonical IDs and per-event commits remain reviewable.
- Interactive official portals are catalog-only unless an approved official API/download exists.
- Legal review decisions and maintainer responsibilities are explicit.

- [ ] **Step 1: Fix the contradictory scrape instruction**

Replace it with an explicit prohibition and describe the exception process for a documented official API or downloadable dataset.

- [ ] **Step 2: Document integrated change governance**

Define owner authority, maintainer review, source hierarchy, status transitions, correction procedure, stale-content handling, and release evidence policy.

- [ ] **Step 3: Update templates**

Require source ID, instrument ID, publication/effective dates, authority, page status, generated catalog update, test evidence, and copyright check.

- [ ] **Step 4: Update architecture documentation**

Describe schemas, graph, sidecar metadata, generator, external monitors, RAG evaluation, and site build.

- [ ] **Step 5: Run deterministic checks**

Run: `python -m scripts.validate_repository && python -m scripts.build_catalog --check && python -m mkdocs build --strict`.

- [ ] **Step 6: Commit the slice**

Commit `docs: define legal knowledge governance`.

### Task 10: Integrated validation, independent review, and draft PR

**Files:**
- Modify as required by verified review findings only.
- Create no report artifact in Git unless it is durable project documentation.

**Interfaces:**
- One clean branch diff against `origin/main`.
- One draft PR to `main`.

- [ ] **Step 1: Run the full fresh verification suite**

```bash
python -m unittest discover -s tests -v
python -m scripts.validate_repository
python -m scripts.build_catalog --check
python -m scripts.page_metadata --check
python -m scripts.temporal_graph --check
python -m scripts.rag_eval --check
python -m mkdocs build --strict
git diff --check origin/main...HEAD
```

- [ ] **Step 2: Run a bounded official-source smoke test**

Probe only the consolidated LCE, RLA reform SIDOF note, RGCE 2026 note, and SNICE legal library. Use the production byte/time/redirect limits. Record classifications, final URLs, MIME types, and hashes without logging bodies.

- [ ] **Step 3: Inspect repository hygiene and diff**

```bash
git status --short
git diff --stat origin/main...HEAD
git diff --name-status origin/main...HEAD
git diff --numstat origin/main...HEAD
```

Confirm there are no binaries, secrets, unrelated generated files, `.env`, tokens, downloaded PDFs, or site output.

- [ ] **Step 4: Request independent code review**

Provide the reviewer the base SHA, head SHA, design, plan, exact source boundaries, and verification output. Fix all Critical and Important findings with regression tests where behavior changes.

- [ ] **Step 5: Re-run the complete verification after review fixes**

Repeat Step 1 from a clean working tree. Completion requires zero test failures and exit code 0 for every deterministic command.

- [ ] **Step 6: Synchronize the GitHub feature branch**

Ensure remote branch `feat/temporal-legal-knowledge-platform` contains exactly the reviewed local tree and no duplicate or unrelated commits. Verify by fetching the remote tree and comparing file hashes.

- [ ] **Step 7: Apply repository settings that are independently safe**

Correct topic `tarriffs` to `tariffs`, enable automatic branch deletion after merge, retain squash merge, and do not weaken branch protection. Report any connector-permission setting that cannot be verified.

- [ ] **Step 8: Create one draft PR**

Title: `Build temporal legal knowledge platform`.

Body sections:

- Scope and architecture.
- Current legal-source additions.
- External code patterns adapted.
- Deterministic versus networked workflows.
- RAG evaluation metrics.
- Compatibility with `arancel-mx` and existing releases.
- Exact verification commands/results.
- Remaining coverage and known uncertainty.

- [ ] **Step 9: Verify PR checks**

Fetch the PR, changed-file list, commit head, and Actions runs. Confirm the PR targets canonical `main`, is draft, includes only the intended branch, and all required GitHub checks complete successfully. If checks fail, inspect logs, fix on the same branch, re-run local verification, and update the same PR.

---

## Plan self-review

- Every design requirement maps to Tasks 1–10.
- Network behavior is isolated from PR CI.
- Temporal legal status is human-reviewed and never inferred from transport success.
- Existing pages migrate through a complete sidecar inventory without mass-editing legal prose.
- All new executable behavior begins with a failing test.
- Generated catalog drift is tested by execution, not source-text assertions.
- External repositories influence design patterns only; no large copied implementation is planned.
- The final PR is created only after integrated verification and independent review.
