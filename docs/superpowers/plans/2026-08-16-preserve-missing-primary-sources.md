# Preserve Missing Primary Sources Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Preserve the 17 active primary/consolidated originals currently reported by `scripts.archive_audit` so the wiki can reproduce its legal source layer without relying only on live external URLs.

**Architecture:** Keep legal currentness separate from preservation. The source registry remains the canonical list of official URLs and SIDOF note IDs; a new local-original manifest fragment records immutable captured bytes with SHA256 and size. `archive_audit` validates any manifest document declared `storage: local_git` before counting it as preserved. Direct Cámara de Diputados PDFs are captured from their official URLs; SIDOF publication events are captured from the official `notas/docFuente/<note_id>` representation while keeping `/notas/<note_id>` as the canonical publication URL.

**Tech Stack:** Python 3.12 standard library, PyYAML, GitHub Actions, GitHub contents/git-data APIs, Cámara de Diputados PDFs, DOF/SIDOF HTML source snapshots.

## Global Constraints

- Archive presence, HTTP health, size, or checksum must never promote `source_status`, `legal_review_status`, `corpus_status`, or `current_through`.
- Do not alter the legal-content remediation owned by PR #36.
- Preserve the exact official bytes fetched for this batch; do not OCR, normalize, rewrite, or reserialize source documents.
- Keep canonical publication URLs from `sources/registry.yaml`; use `capture_url` only to record a byte-bearing official endpoint when it differs.
- Reject redirects or capture endpoints that leave the source's `allowed_hosts` boundary.
- A local manifest entry is valid only when its path is safe, its file exists, byte count matches, and SHA256 matches.
- Do not commit an unexpectedly large binary merely to make the audit green; route such a document to a Release asset instead.
- Do not request a document from the repository owner until registry, manifests, equivalents, current uploads, and official alternatives have been checked.

---

### Task 1: Make local manifest preservation cryptographically enforceable

**Files:**
- Modify: `scripts/archive_audit.py`
- Modify: `tests/test_archive_audit.py`

**Interfaces:**
- Consumes: root `data/originals/manifest.yaml` and each referenced fragment.
- Produces: `_manifest_index(root)` that refuses invalid `storage: local_git` entries before they can satisfy an audit row.

- [ ] **Step 1: Write failing tests for valid, missing, unsafe, wrong-size, and wrong-hash local files**

Add fixture documents with `storage: local_git` and assert that `audit_registry(root)` accepts an exact file but raises `ValueError` for path traversal, missing files, byte mismatch, and SHA256 mismatch.

- [ ] **Step 2: Run the focused test and verify RED**

Run: `python -m unittest tests.test_archive_audit -v`
Expected: new local-byte validation tests fail because `_manifest_index` currently trusts manifest metadata.

- [ ] **Step 3: Implement local byte verification**

In `scripts/archive_audit.py`, add a helper that:

```python
def _verify_local_manifest_document(root: Path, manifest_path: Path, document: dict[str, Any]) -> None:
    if document.get("storage") != "local_git":
        return
    file_value = document.get("file")
    expected_sha = document.get("sha256")
    expected_bytes = document.get("bytes")
    if not isinstance(file_value, str) or not file_value:
        raise ValueError("local_git manifest document requires file")
    if not isinstance(expected_sha, str) or len(expected_sha) != 64:
        raise ValueError("local_git manifest document requires sha256")
    if not isinstance(expected_bytes, int) or expected_bytes < 0:
        raise ValueError("local_git manifest document requires bytes")
    candidate = (manifest_path.parent / file_value).resolve()
    originals_root = (root / "data" / "originals").resolve()
    if candidate != originals_root and originals_root not in candidate.parents:
        raise ValueError("local_git manifest path escapes data/originals")
    payload = candidate.read_bytes()
    if len(payload) != expected_bytes:
        raise ValueError("local_git manifest byte count mismatch")
    if hashlib.sha256(payload).hexdigest() != expected_sha.casefold():
        raise ValueError("local_git manifest sha256 mismatch")
```

Call it for each manifest document before adding the document to the index.

- [ ] **Step 4: Run the focused test and verify GREEN**

Run: `python -m unittest tests.test_archive_audit -v`
Expected: all archive-audit tests pass.

- [ ] **Step 5: Commit**

Commit message: `test: verify local original bytes`

---

### Task 2: Add a deterministic maintainer capture command

**Files:**
- Create: `scripts/capture_primary_originals.py`
- Create: `tests/test_capture_primary_originals.py`

**Interfaces:**
- Consumes: `sources/registry.yaml`, `scripts.archive_audit.audit_registry(root)`, and an HTTP fetch function injected for tests.
- Produces: deterministic capture records with `id`, `file`, `url`, optional `capture_url`, `sha256`, `bytes`, `media_type`, `storage: local_git`, `license`, and `redistribution`.

- [ ] **Step 1: Write failing tests for URL selection and payload validation**

Cover:
- a direct `application/pdf` Cámara source uses `source["url"]` and a `.pdf` filename;
- a SIDOF source with `note_id` uses `https://sidof.segob.gob.mx/notas/docFuente/<note_id>` as `capture_url` and `.html` filename;
- host escape is rejected;
- a PDF response without `%PDF-` is rejected;
- an HTML response below 500 bytes or containing `Access Denied`/`Captcha` is rejected;
- IDs and filenames are deterministic.

- [ ] **Step 2: Run the focused test and verify RED**

Run: `python -m unittest tests.test_capture_primary_originals -v`
Expected: import failure because the module does not exist.

- [ ] **Step 3: Implement the capture planner/validator**

Expose these functions:

```python
def capture_url_for(source: dict[str, Any]) -> tuple[str, str]: ...
def validate_payload(source: dict[str, Any], url: str, media_type: str, payload: bytes) -> None: ...
def build_manifest_document(source: dict[str, Any], file_name: str, capture_url: str, media_type: str, payload: bytes) -> dict[str, Any]: ...
```

CLI behavior:

```text
python -m scripts.capture_primary_originals --output data/originals/primary-2026-08-16
```

The command captures only rows whose current audit status is `missing_primary`; it writes bytes without modification and writes a deterministically sorted `MANIFEST.yaml`. It does not edit `sources/registry.yaml`, `sources/instruments.yaml`, or page metadata.

- [ ] **Step 4: Run focused tests and verify GREEN**

Run: `python -m unittest tests.test_capture_primary_originals -v`
Expected: all capture tests pass.

- [ ] **Step 5: Commit**

Commit message: `feat: add primary-source capture command`

---

### Task 3: Capture and register the 17 official originals

**Files:**
- Create: `data/originals/primary-2026-08-16/MANIFEST.yaml`
- Create: 17 immutable source files under `data/originals/primary-2026-08-16/`
- Modify: `data/originals/manifest.yaml`

**Interfaces:**
- Consumes: the 17 `missing_primary` rows from the committed audit report and current source registry.
- Produces: one local manifest fragment referenced by the root manifest.

- [ ] **Step 1: Capture the four Cámara de Diputados consolidated PDFs**

Capture exact bytes for:

```text
mx_diputados_constitucion  -> CPEUM.pdf
mx_diputados_liva_current -> LIVA.pdf
mx_diputados_lieps_current -> LIEPS.pdf
mx_diputados_lfd_current -> LFD.pdf
```

Verify every payload starts with `%PDF-`, record byte size and SHA256, and retain the registry URL as `url`.

- [ ] **Step 2: Capture the thirteen SIDOF publication snapshots**

Use `notas/docFuente/<note_id>` for:

```text
mx_sidof_reglas_se_2022               5651333
mx_sidof_immex_reform_20241219        5745788
mx_sidof_immex_reform_20250828        5766797
mx_sidof_reglas_se_mod_20250902       5767158
mx_sidof_reglas_se_mod_20260212       5779942
mx_sidof_rla_reform_20260223          5780677
mx_sidof_lineamientos_159bis_20260331 5783669
mx_sidof_reglas_se_mod_20260402       5783929
mx_sidof_ligie_prosec_20260423        5785818
mx_sidof_lce_reform_20260501          5786538
mx_sidof_ventanilla_unica_20260504    5786598
mx_sidof_reglas_se_mod_20260528       5788843
mx_sidof_reglas_se_mod_20260529       5788992
```

For each manifest entry keep `url` equal to the registry `/notas/<note_id>` page and add `capture_url` equal to the exact `docFuente` endpoint used for the stored bytes.

- [ ] **Step 3: Enforce size policy before commit**

Measure all 17 files. If a file is unexpectedly large for Git history, exclude only that file from the local batch, leave its audit row unresolved, and record it for later `release_asset` preservation rather than forcing it into Git.

- [ ] **Step 4: Register the fragment**

Append exactly:

```yaml
- primary-2026-08-16/MANIFEST.yaml
```

to `data/originals/manifest.yaml` without changing older release-backed fragments.

- [ ] **Step 5: Run archive tests**

Run:

```text
python -m unittest tests.test_archive_audit tests.test_capture_primary_originals -v
python -m scripts.archive_audit --check
```

Expected: local bytes are cryptographically accepted and all successfully captured IDs are no longer `missing_primary`.

- [ ] **Step 6: Commit**

Commit message: `data: preserve active primary originals`

---

### Task 4: Regenerate human-facing archive state and verify the repository

**Files:**
- Modify: `docs/status/missing-primary-sources.md`
- Modify only if generator output changes: `docs/catalog/library.md`, `docs/catalog/registry.md`, `docs/explore/knowledge-map.md`, `docs/assets/data/knowledge-index.json`

**Interfaces:**
- Consumes: committed manifest fragment and original bytes.
- Produces: drift-free generated documentation reflecting the real preservation state.

- [ ] **Step 1: Regenerate the audit report**

Run:

```text
python -m scripts.archive_audit
```

Expected if all 17 captures are local and valid: `Missing primary originals requiring review: 0`. If any file was routed out of Git by the size policy, the exact unresolved source remains visible instead of being hidden.

- [ ] **Step 2: Regenerate dependent generated surfaces**

Run:

```text
python -m scripts.build_catalog
python -m scripts.build_knowledge_map
```

Commit only actual generator changes.

- [ ] **Step 3: Run the full repository verification**

Run the same gates as CI:

```text
python -m unittest discover -s tests -v
python -m scripts.validate_repository
python -m scripts.validate_data_contracts
python -m scripts.archive_audit --check
python -m scripts.build_catalog --check
python -m scripts.page_metadata --check
python -m scripts.coverage_report --check
python -m scripts.build_knowledge_map --check
python -m scripts.temporal_graph --check
python -m scripts.rag_eval --check
python -m mkdocs build --strict
python -m scripts.verify_site site
python -m mkdocs build --strict -f mkdocs.offline.yml -d site-offline
python -m scripts.verify_offline_site site-offline
```

Expected: every command exits 0; legal/RAG eligibility metrics are unchanged by preservation alone.

- [ ] **Step 4: Commit**

Commit message: `docs: refresh preserved-source inventory`

---

### Task 5: Open one preservation PR and verify the exact head

**Files:**
- No additional source files required.

**Interfaces:**
- Consumes: branch `feat/preserve-missing-primary-sources`.
- Produces: one draft PR against `main`, leaving PR #36 isolated.

- [ ] **Step 1: Open a draft PR**

Title: `Preserve active primary-source originals`

Body must state the exact count captured, total byte size, storage strategy, remaining missing count, and the invariant that preservation did not promote legal currentness.

- [ ] **Step 2: Verify exact-head Actions**

Require fresh success for the repository CI and Dependency Review on the PR head. Inspect CodeQL results for changed code where available.

- [ ] **Step 3: Review PR diff for accidental legal-content changes**

Confirm no modifications to RGCE annex content, legal review statuses, temporal events, or tariff tables outside generated archive/catalog outputs.

- [ ] **Step 4: Stop for maintainer integration decision**

Do not merge this PR automatically. Report the exact head SHA, checks, captured source count, unresolved source count, and any file routed to Release storage because of size.
