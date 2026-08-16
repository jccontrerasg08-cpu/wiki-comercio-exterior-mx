# Archive, Provenance, and Catalog Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the existing official-source registry into a verifiable document library that records whether each important source is archived in Git, stored as a GitHub Release asset, or intentionally external-only, and expose that state through generated docs and validation.

**Architecture:** Extend the existing `sources/registry.yaml` schema with one optional `archive` block and keep `sources/instruments.yaml` as the legal-temporal graph. Add focused validation/generation helpers under `scripts/` so the generated catalog remains deterministic. The implementation must never infer legal currentness from transport availability or archive presence.

**Tech Stack:** Python 3, PyYAML, unittest/pytest-compatible tests, MkDocs Material, existing generated Markdown pipeline.

## Global Constraints

- `wiki-comercio-exterior-mx` remains the canonical legal/documentary/provenance layer.
- `arancel-mx` remains the canonical structured HS/TIGIE/fracción/NICO/tariff layer.
- `aduanamap-mx` remains the canonical geospatial/map application layer.
- Archive statuses are exactly `local_git`, `release_asset`, and `external_only`.
- `external_only` requires a documented reason.
- Archive availability never promotes a source or page to legally current.
- Before requesting a document from the owner, code/reports must check existing originals, manifests, source registry, uploaded equivalents, and newer versions.
- Large binaries may live as GitHub Release assets instead of Git history.
- Existing source IDs and public page URLs must remain stable.
- `mkdocs build --strict` and the existing Python test suite must remain green.

---

### Task 1: Define and validate the archive metadata contract

**Files:**
- Create: `scripts/archive_metadata.py`
- Create: `tests/test_archive_metadata.py`
- Modify: `scripts/schema_validation.py`

**Interfaces:**
- Consumes: source dictionaries loaded from `sources/registry.yaml`.
- Produces: `validate_archive(source: dict[str, Any], root: Path) -> list[str]` and `archive_label(source: dict[str, Any]) -> str`.

- [ ] **Step 1: Write failing tests for the three supported archive states**

```python
from pathlib import Path
from scripts.archive_metadata import validate_archive


def test_local_git_requires_verifiable_local_fields(tmp_path: Path):
    source = {
        "id": "mx_test",
        "archive": {
            "status": "local_git",
            "path": "data/originals/test.pdf",
            "sha256": "a" * 64,
            "size_bytes": 123,
            "mime_type": "application/pdf",
            "captured_at": "2026-08-15",
        },
    }
    assert "archive path does not exist" in "\n".join(validate_archive(source, tmp_path))


def test_release_asset_requires_tag_asset_and_checksum(tmp_path: Path):
    source = {"id": "mx_test", "archive": {"status": "release_asset"}}
    errors = validate_archive(source, tmp_path)
    assert any("release_tag" in error for error in errors)
    assert any("asset_name" in error for error in errors)
    assert any("sha256" in error for error in errors)


def test_external_only_requires_reason(tmp_path: Path):
    source = {"id": "mx_test", "archive": {"status": "external_only"}}
    assert any("reason" in error for error in validate_archive(source, tmp_path))
```

- [ ] **Step 2: Run tests to verify RED**

Run: `python -m pytest tests/test_archive_metadata.py -q`
Expected: FAIL because `scripts.archive_metadata` does not exist.

- [ ] **Step 3: Implement minimal archive validation**

```python
from __future__ import annotations

from pathlib import Path
from typing import Any

ARCHIVE_STATUSES = {"local_git", "release_asset", "external_only"}


def validate_archive(source: dict[str, Any], root: Path) -> list[str]:
    archive = source.get("archive")
    if archive is None:
        return []
    if not isinstance(archive, dict):
        return [f"{source.get('id')}: archive must be a mapping"]

    source_id = str(source.get("id", "<unknown>"))
    status = archive.get("status")
    if status not in ARCHIVE_STATUSES:
        return [f"{source_id}: invalid archive status {status!r}"]

    errors: list[str] = []
    if status == "local_git":
        for key in ("path", "sha256", "size_bytes", "mime_type", "captured_at"):
            if archive.get(key) in (None, ""):
                errors.append(f"{source_id}: local_git archive missing {key}")
        path = archive.get("path")
        if isinstance(path, str) and not (root / path).is_file():
            errors.append(f"{source_id}: archive path does not exist: {path}")
    elif status == "release_asset":
        for key in ("release_tag", "asset_name", "sha256", "size_bytes", "mime_type", "captured_at"):
            if archive.get(key) in (None, ""):
                errors.append(f"{source_id}: release_asset archive missing {key}")
    else:
        if not str(archive.get("reason", "")).strip():
            errors.append(f"{source_id}: external_only archive requires reason")
    return errors


def archive_label(source: dict[str, Any]) -> str:
    archive = source.get("archive")
    if not isinstance(archive, dict):
        return "unclassified"
    return str(archive.get("status", "unclassified"))
```

- [ ] **Step 4: Integrate archive errors into the existing schema validation entry point**

Import `validate_archive` in `scripts/schema_validation.py` and append returned errors for each registry source without altering legal-status validation.

- [ ] **Step 5: Run focused and existing schema tests**

Run: `python -m pytest tests/test_archive_metadata.py tests/test_schema_validation.py -q`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add scripts/archive_metadata.py scripts/schema_validation.py tests/test_archive_metadata.py
git commit -m "feat: validate source archive metadata"
```

---

### Task 2: Add deterministic archive information to generated catalogs

**Files:**
- Modify: `scripts/build_catalog.py`
- Modify: `tests/test_catalog_generation.py`
- Generate/Modify: `docs/catalog/registry.md`
- Create/Generate: `docs/catalog/library.md`

**Interfaces:**
- Consumes: `archive_label(source)` from Task 1.
- Produces: `render_library(registry_path: Path, instruments_path: Path) -> str` and a second deterministic generated document.

- [ ] **Step 1: Add failing catalog tests**

Add an `archive` block to the `REGISTRY` fixture and assert:

```python
self.assertIn("Archive", first)
self.assertIn("local_git", first)

library = render_library(registry, instruments)
self.assertIn("# Official document library", library)
self.assertIn("## Local Git originals", library)
self.assertIn("## GitHub Release assets", library)
self.assertIn("## External-only references", library)
```

- [ ] **Step 2: Run the focused test**

Run: `python -m pytest tests/test_catalog_generation.py -q`
Expected: FAIL because archive output and `render_library` do not exist.

- [ ] **Step 3: Extend the registry table with an Archive column**

Use `archive_label(source)` and keep all current sort keys unchanged so output remains stable.

- [ ] **Step 4: Implement `render_library`**

Group sources by archive status and render source ID, title, authority, publication date, instrument IDs, official URL, archive location, SHA256, and captured date. For `external_only`, render the reason instead of pretending a local copy exists.

- [ ] **Step 5: Update `run_check` and `main` to manage both generated files**

`--check` must fail if either `docs/catalog/registry.md` or `docs/catalog/library.md` is stale. Normal generation writes both files in one deterministic run.

- [ ] **Step 6: Regenerate catalog outputs and run tests**

Run:

```bash
python -m scripts.build_catalog
python -m scripts.build_catalog --check
python -m pytest tests/test_catalog_generation.py -q
```

Expected: PASS and no generated drift.

- [ ] **Step 7: Commit**

```bash
git add scripts/build_catalog.py tests/test_catalog_generation.py docs/catalog/registry.md docs/catalog/library.md
git commit -m "feat: generate verifiable document library"
```

---

### Task 3: Audit existing originals and generate the missing-primary-sources report

**Files:**
- Create: `scripts/archive_audit.py`
- Create: `tests/test_archive_audit.py`
- Create/Generate: `docs/status/missing-primary-sources.md`
- Read-only inputs: `data/originals/**/MANIFEST.yaml`, `data/originals/SHA256SUMS`, `sources/registry.yaml`

**Interfaces:**
- Produces: `audit_registry(root: Path) -> list[AuditRow]`, `render_missing_report(rows: list[AuditRow]) -> str`, and CLI `python -m scripts.archive_audit [--check]`.

- [ ] **Step 1: Write a fixture-based failing test**

```python
def test_report_only_lists_sources_that_really_need_a_primary_copy(tmp_path):
    # Registry contains: one local_git file present, one external_only with reason,
    # and one primary_legal source with no archive block.
    rows = audit_registry(tmp_path)
    report = render_missing_report(rows)
    assert "missing_primary" in report
    assert "already_local" not in report
    assert "intentional_external" not in report
```

- [ ] **Step 2: Run RED test**

Run: `python -m pytest tests/test_archive_audit.py -q`
Expected: FAIL because `scripts.archive_audit` does not exist.

- [ ] **Step 3: Implement conservative audit classification**

The audit may mark a source missing only when all are true:

```python
needs_primary_copy = (
    source.get("evidence_class") in {"primary_legal", "official_consolidated", "official_operational"}
    and source.get("archive") is None
    and not equivalent_original_found_in_manifests(source, root)
)
```

Do not infer missing from a page being incomplete. Do not request tariff table dumps that belong in `arancel-mx`.

- [ ] **Step 4: Generate a human-readable report with exact request fields**

Each row must show: document/source ID, authority, publication date, what the repo already has, what is missing, and why it is useful. If nothing is missing, render an explicit empty-state statement.

- [ ] **Step 5: Add `--check` drift behavior and run tests**

Run:

```bash
python -m scripts.archive_audit
python -m scripts.archive_audit --check
python -m pytest tests/test_archive_audit.py -q
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add scripts/archive_audit.py tests/test_archive_audit.py docs/status/missing-primary-sources.md
git commit -m "feat: audit missing primary source originals"
```

---

### Task 4: Backfill archive metadata for verified critical originals only

**Files:**
- Modify: `sources/registry.yaml`
- Modify as verified: `data/originals/**/MANIFEST.yaml`
- Generate: `docs/catalog/registry.md`
- Generate: `docs/catalog/library.md`
- Generate: `docs/status/missing-primary-sources.md`

**Interfaces:**
- Uses Task 1 validation and Task 3 audit.
- Does not create legal-currentness changes.

- [ ] **Step 1: Inventory the existing critical source IDs**

At minimum inspect records for LIGIE/TIGIE, Ley Aduanera, Reglamento de la Ley Aduanera, Ley de Comercio Exterior, RGCE 2026 and annex source blocks, T-MEC/trade agreements, SAT padrón sources, SNICE, VUCEM, ANAM, and NOM-related sources.

- [ ] **Step 2: Match each source against existing originals/manifests before editing metadata**

For each verified match, compute or reuse the existing SHA256 and exact byte size. Never invent hashes, file paths, dates, or MIME types.

- [ ] **Step 3: Add archive blocks only for verified matches**

Example shape:

```yaml
archive:
  status: local_git
  path: data/originals/diputados/ley-aduanera/LAdua.pdf
  sha256: <verified 64-char hash>
  size_bytes: <verified integer>
  mime_type: application/pdf
  captured_at: 2026-08-15
```

Use `release_asset` only after the asset exists and its checksum is known. Use `external_only` only with an explicit reason.

- [ ] **Step 4: Regenerate all generated docs and run archive checks**

Run:

```bash
python -m scripts.build_catalog
python -m scripts.archive_audit
python -m scripts.build_catalog --check
python -m scripts.archive_audit --check
python -m pytest tests/test_archive_metadata.py tests/test_archive_audit.py tests/test_catalog_generation.py -q
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add sources/registry.yaml data/originals docs/catalog docs/status/missing-primary-sources.md
git commit -m "data: register verified critical source originals"
```

---

### Task 5: Remove contradictory archive policy language

**Files:**
- Modify: `docs/catalog/index.md`
- Modify: `docs/catalog/mexico/index.md`
- Modify: `docs/catalog/mexico/arancel.md`
- Modify: `data/originals/README.md`
- Modify if matches are found: `README.md`, `CONTRIBUTING.md`, `docs/**/*.md`
- Create: `tests/test_archive_policy_copy.py`

**Interfaces:**
- Policy text must align with the archive contract without authorizing indiscriminate scraping.

- [ ] **Step 1: Write failing policy-copy tests**

```python
FORBIDDEN = (
    "does not ship official PDF bytes",
    "this tree is not a DOF dump",
)


def test_no_generic_policy_prohibits_archiving_official_originals():
    text = "\n".join(path.read_text(encoding="utf-8") for path in DOC_PATHS)
    for phrase in FORBIDDEN:
        assert phrase not in text
```

Also assert the catalog contains affirmative wording that critical official originals may be archived with provenance/checksums.

- [ ] **Step 2: Run RED test**

Run: `python -m pytest tests/test_archive_policy_copy.py -q`
Expected: FAIL on current contradictory wording.

- [ ] **Step 3: Replace blanket prohibitions with precise policy**

Required meaning:

```text
This repository archives primary legal documents and operational datasets when a local copy materially improves reproducibility, auditability, or resilience. Large originals may be stored as GitHub Release assets. Interactive portals and redundant copies may remain external-only when documented. Official publication remains authoritative for legal effect.
```

For `catalog-only; do not scrape`, distinguish interactive portals from documents that should be archived; do not create a blanket scraping rule.

- [ ] **Step 4: Run policy and catalog tests**

Run: `python -m pytest tests/test_archive_policy_copy.py tests/test_catalog_generation.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add docs data/originals/README.md README.md CONTRIBUTING.md tests/test_archive_policy_copy.py
git commit -m "docs: align source archive policy"
```

---

### Task 6: Expose the library in MkDocs navigation and verify the whole repository

**Files:**
- Modify: `mkdocs.yml`
- Modify: `docs/catalog/index.md`
- Modify: `tests/test_mkdocs_ux.py`
- Modify: `tests/test_docs_engine_compatibility.py` only if a deterministic generated-path assertion is needed.

**Interfaces:**
- Adds visible navigation to `docs/catalog/library.md` and `docs/status/missing-primary-sources.md` without changing existing URLs.

- [ ] **Step 1: Add failing nav assertions**

Assert that `mkdocs.yml` exposes a human-facing document library entry and that the generated library exists.

- [ ] **Step 2: Run focused test**

Run: `python -m pytest tests/test_mkdocs_ux.py -q`
Expected: FAIL until nav is updated.

- [ ] **Step 3: Add navigation and contextual links**

Add the library under the existing source/catalog section. The missing-source report belongs under project/status documentation, not as a primary user navigation destination.

- [ ] **Step 4: Run full verification**

Run:

```bash
python -m scripts.build_catalog --check
python -m scripts.archive_audit --check
python -m pytest -q
mkdocs build --strict
```

Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add mkdocs.yml docs/catalog/index.md tests/test_mkdocs_ux.py tests/test_docs_engine_compatibility.py
git commit -m "feat: expose official document library"
```

---

## Self-review checklist

- Every archive state has explicit validation.
- No task promotes legal currentness based on file presence, URL health, or checksum success.
- The generated missing-source report enforces the owner's rule to ask only for genuinely absent originals.
- Existing source IDs and page URLs remain stable.
- `arancel-mx` is not duplicated into the wiki as a tariff database.
- The plan contains no placeholder implementation steps.
- Final verification includes generated-file drift, full tests, and strict MkDocs build.
