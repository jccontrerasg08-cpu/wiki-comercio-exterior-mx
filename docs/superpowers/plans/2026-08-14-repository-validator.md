# Repository Validator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add one offline command, `python -m scripts.validate_repository`, that rejects structural corruption in the source registry, original-document manifests, checksums, and repository layout before merge.

**Architecture:** Keep validation repository-owned and dependency-light. Parse YAML with an explicitly pinned PyYAML dependency, model findings as small immutable records, validate each domain with focused functions, and expose one CLI entry point. The first release deliberately validates the schema the repository already uses; canonical registry-to-manifest ID migration and corpus front matter come in later PRs.

**Tech Stack:** Python 3.12 standard library, PyYAML 6.0.3, `unittest`, existing GitHub Actions `repository-ci`.

## Global Constraints

- Required PR validation remains offline and deterministic.
- Do not fetch government URLs in `repository-ci`.
- `sources/registry.yaml` remains the canonical source registry.
- Original binary bytes remain outside normal Git history and are represented by manifests plus `SHA256SUMS`.
- Do not enforce manifest `id == source_id` yet; current historical manifests are not fully migrated to the canonical registry identity model.
- Do not require corpus front matter yet; that is a later migration.
- One contributor command: `python -m scripts.validate_repository`.
- Prefer clear stable error codes over a single opaque pass/fail message.
- Keep the implementation small enough to understand without a framework.

---

## File Structure

- Create `scripts/__init__.py`: marks repository validation utilities as an importable package.
- Create `scripts/validate_repository.py`: validation functions, finding model, formatter, and CLI.
- Create `tests/test_repository_validator.py`: unit and integration-style tests using temporary repositories and the real repository.
- Create `tests/fixtures/invalid/duplicate-source-id.yaml`: known-bad registry fixture.
- Create `tests/fixtures/invalid/invalid-sha256.yaml`: known-bad manifest fixture.
- Create `tests/fixtures/invalid/missing-fragment.yaml`: known-bad root manifest fixture.
- Modify `requirements-docs.txt`: explicitly pin `PyYAML==6.0.3` because repository validation imports it directly.
- Modify `.github/workflows/ci.yml`: run the validator after unit tests and before `mkdocs build --strict`.

---

### Task 1: Establish the validator entry point with TDD

**Files:**
- Create: `tests/test_repository_validator.py`
- Create: `scripts/__init__.py`
- Create: `scripts/validate_repository.py`

**Interfaces:**
- Produces: `ValidationFinding`, `validate_repository(root: Path) -> list[ValidationFinding]`, and CLI `main() -> int`.

- [ ] **Step 1: Write a failing test proving the module does not yet exist**

Create `tests/test_repository_validator.py` initially with:

```python
import importlib.util
import unittest


class RepositoryValidatorBootstrapTests(unittest.TestCase):
    def test_validator_module_exists(self):
        self.assertIsNotNone(importlib.util.find_spec("scripts.validate_repository"))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the new test and verify RED**

Run:

```bash
python -m unittest tests.test_repository_validator
```

Expected: FAIL because `scripts.validate_repository` does not exist.

- [ ] **Step 3: Add the minimal importable module**

Create empty `scripts/__init__.py` and create `scripts/validate_repository.py` with:

```python
"""Offline integrity validation for wiki-comercio-exterior-mx."""
```

- [ ] **Step 4: Run the bootstrap test and verify GREEN**

Run:

```bash
python -m unittest tests.test_repository_validator
```

Expected: PASS.

- [ ] **Step 5: Commit the bootstrap cycle**

```bash
git add scripts tests/test_repository_validator.py
git commit -m "test: bootstrap repository validator"
```

---

### Task 2: Add a stable finding model and registry validation

**Files:**
- Modify: `tests/test_repository_validator.py`
- Modify: `scripts/validate_repository.py`
- Create: `tests/fixtures/invalid/duplicate-source-id.yaml`
- Modify: `requirements-docs.txt`

**Interfaces:**
- Produces:

```python
@dataclass(frozen=True, slots=True)
class ValidationFinding:
    code: str
    path: str
    message: str
```

and:

```python
def validate_registry(path: Path) -> list[ValidationFinding]: ...
```

- [ ] **Step 1: Add direct YAML dependency**

Append to `requirements-docs.txt`:

```text
PyYAML==6.0.3
```

This version is the PyYAML release currently resolved by the repository's verified MkDocs 9.7.7 CI environment.

- [ ] **Step 2: Add known-bad duplicate source fixture**

Create `tests/fixtures/invalid/duplicate-source-id.yaml`:

```yaml
sources:
  - id: duplicate
    jurisdiction: MEX
    title: Source A
    url: https://example.gob.mx/a
    authority: Example Authority
    evidence_class: primary_legal
    allowed_hosts: [example.gob.mx]
    media_types: [application/pdf]
    harvest: false

  - id: duplicate
    jurisdiction: MEX
    title: Source B
    url: https://example.gob.mx/b
    authority: Example Authority
    evidence_class: primary_legal
    allowed_hosts: [example.gob.mx]
    media_types: [application/pdf]
    harvest: false
```

- [ ] **Step 3: Write failing registry tests**

Add tests that import the intended API and assert:

```python
from pathlib import Path
from scripts.validate_repository import validate_registry

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "invalid"


def test_duplicate_source_id_is_rejected(self):
    findings = validate_registry(FIXTURES / "duplicate-source-id.yaml")
    self.assertIn("REGISTRY_DUPLICATE_ID", {item.code for item in findings})


def test_real_registry_has_no_structural_findings(self):
    findings = validate_registry(ROOT / "sources" / "registry.yaml")
    self.assertEqual(findings, [])
```

- [ ] **Step 4: Run registry tests and verify RED**

Run:

```bash
python -m unittest tests.test_repository_validator
```

Expected: FAIL because `validate_registry` and `ValidationFinding` are not implemented.

- [ ] **Step 5: Implement minimal registry validation**

Implement:

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml


@dataclass(frozen=True, slots=True)
class ValidationFinding:
    code: str
    path: str
    message: str


_REQUIRED_SOURCE_FIELDS = (
    "id",
    "jurisdiction",
    "title",
    "url",
    "authority",
    "evidence_class",
    "allowed_hosts",
    "media_types",
    "harvest",
)


def _load_yaml(path: Path) -> tuple[Any | None, list[ValidationFinding]]:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")), []
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        return None, [
            ValidationFinding("YAML_INVALID", str(path), f"cannot parse YAML: {exc}")
        ]


def validate_registry(path: Path) -> list[ValidationFinding]:
    data, findings = _load_yaml(path)
    if findings:
        return findings
    if not isinstance(data, dict) or not isinstance(data.get("sources"), list):
        return [ValidationFinding("REGISTRY_SHAPE", str(path), "expected top-level sources list")]

    seen: set[str] = set()
    for index, source in enumerate(data["sources"]):
        item_path = f"{path}:sources[{index}]"
        if not isinstance(source, dict):
            findings.append(ValidationFinding("REGISTRY_SOURCE_SHAPE", item_path, "source must be a mapping"))
            continue
        for field in _REQUIRED_SOURCE_FIELDS:
            if field not in source:
                findings.append(ValidationFinding("REGISTRY_REQUIRED_FIELD", item_path, f"missing {field}"))
        source_id = source.get("id")
        if isinstance(source_id, str):
            if source_id in seen:
                findings.append(ValidationFinding("REGISTRY_DUPLICATE_ID", item_path, f"duplicate id {source_id}"))
            seen.add(source_id)
        url = source.get("url")
        if isinstance(url, str):
            parsed = urlparse(url)
            if parsed.scheme != "https" or not parsed.netloc:
                findings.append(ValidationFinding("REGISTRY_URL", item_path, f"expected absolute HTTPS URL: {url}"))
        allowed_hosts = source.get("allowed_hosts")
        if isinstance(allowed_hosts, list) and isinstance(url, str):
            host = urlparse(url).hostname
            if host and host not in allowed_hosts:
                findings.append(ValidationFinding("REGISTRY_ALLOWED_HOST", item_path, f"URL host {host} missing from allowed_hosts"))
    return findings
```

If the real registry reveals a legitimate exception to the host rule, adjust the rule to reflect the actual repository contract rather than adding a one-off filename exception.

- [ ] **Step 6: Run tests and verify GREEN**

Run:

```bash
python -m unittest tests.test_repository_validator
```

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add requirements-docs.txt scripts/validate_repository.py tests
git commit -m "feat: validate source registry structure"
```

---

### Task 3: Validate original-manifest structure and SHA metadata

**Files:**
- Modify: `tests/test_repository_validator.py`
- Modify: `scripts/validate_repository.py`
- Create: `tests/fixtures/invalid/invalid-sha256.yaml`

**Interfaces:**
- Produces:

```python
def validate_manifest(path: Path) -> list[ValidationFinding]: ...
```

- [ ] **Step 1: Add invalid SHA fixture**

Create `tests/fixtures/invalid/invalid-sha256.yaml`:

```yaml
documents:
  - id: bad-sha
    file: example.pdf
    url: https://example.gob.mx/example.pdf
    summary: data/corpus/README.md
    sha256: not-a-sha256
    bytes: 100
    license: official-not-relicensed
    redistribution: official publication
```

- [ ] **Step 2: Write failing manifest tests**

Add:

```python
from scripts.validate_repository import validate_manifest


def test_invalid_sha_is_rejected(self):
    findings = validate_manifest(FIXTURES / "invalid-sha256.yaml")
    self.assertIn("MANIFEST_SHA256", {item.code for item in findings})


def test_real_manifest_fragments_have_valid_structure(self):
    fragment_paths = [
        ROOT / "data" / "originals" / "diputados" / "MANIFEST.yaml",
        ROOT / "data" / "originals" / "sidof" / "5778300" / "MANIFEST.yaml",
        ROOT / "data" / "originals" / "tmec" / "MANIFEST.yaml",
    ]
    for path in fragment_paths:
        self.assertEqual(validate_manifest(path), [], path)
```

- [ ] **Step 3: Run and verify RED**

```bash
python -m unittest tests.test_repository_validator
```

Expected: FAIL because `validate_manifest` is missing.

- [ ] **Step 4: Implement minimal manifest validation**

Required document fields:

```python
_REQUIRED_DOCUMENT_FIELDS = (
    "id",
    "file",
    "url",
    "sha256",
    "bytes",
    "license",
    "redistribution",
)
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
```

For each document reject:

- non-mapping document
- missing required field
- duplicate document ID within a fragment
- non-HTTPS or non-absolute `url`
- SHA not 64 lowercase hex characters
- `bytes` that is not a positive integer
- `file` containing an absolute path or `..`

Do not require `title`, `summary`, or `note`, because current valid manifests use them optionally.

- [ ] **Step 5: Run and verify GREEN**

```bash
python -m unittest tests.test_repository_validator
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add scripts/validate_repository.py tests
git commit -m "feat: validate original manifests"
```

---

### Task 4: Validate the root fragment index and checksum cross-reference

**Files:**
- Modify: `tests/test_repository_validator.py`
- Modify: `scripts/validate_repository.py`
- Create: `tests/fixtures/invalid/missing-fragment.yaml`

**Interfaces:**
- Produces:

```python
def validate_originals(originals_dir: Path) -> list[ValidationFinding]: ...
```

- [ ] **Step 1: Add missing-fragment fixture**

Create `tests/fixtures/invalid/missing-fragment.yaml`:

```yaml
fragments:
  - does-not-exist/MANIFEST.yaml
license: official-not-relicensed
redistribution: official publication
```

- [ ] **Step 2: Write failing originals tests**

Use `tempfile.TemporaryDirectory` to create a minimal originals directory whose root manifest points at a missing fragment, then assert `ORIGINALS_MISSING_FRAGMENT`.

Also add a real-repository test:

```python
def test_real_originals_index_and_checksums_are_consistent(self):
    findings = validate_originals(ROOT / "data" / "originals")
    self.assertEqual(findings, [])
```

- [ ] **Step 3: Run and verify RED**

```bash
python -m unittest tests.test_repository_validator
```

Expected: FAIL because `validate_originals` is missing.

- [ ] **Step 4: Implement root originals validation**

Implement these invariants:

1. `data/originals/manifest.yaml` parses and contains a `fragments` list.
2. Each fragment path is relative, contains no `..`, and exists.
3. Every listed fragment passes `validate_manifest`.
4. Every actual `**/MANIFEST.yaml` beneath `data/originals/` except the root manifest is listed exactly once.
5. `SHA256SUMS` lines must match:

```text
<64 lowercase hex><two spaces><relative path>
```

6. For every manifest document, compute its expected logical checksum path as:

```python
fragment.parent.relative_to(originals_dir) / document["file"]
```

and require a matching SHA entry with the same digest.
7. Reject duplicate checksum paths.
8. Do not require the binary to exist in the Git clone; the design intentionally stores bytes in Releases.

Use stable codes:

```text
ORIGINALS_ROOT_SHAPE
ORIGINALS_MISSING_FRAGMENT
ORIGINALS_UNLISTED_FRAGMENT
ORIGINALS_CHECKSUM_FORMAT
ORIGINALS_DUPLICATE_CHECKSUM_PATH
ORIGINALS_CHECKSUM_MISSING
ORIGINALS_CHECKSUM_MISMATCH
```

- [ ] **Step 5: Run and verify GREEN against the entire real originals tree**

```bash
python -m unittest tests.test_repository_validator
```

Expected: PASS. If the real repository exposes an inconsistency, stop and fix or explicitly classify the existing inconsistency before weakening the invariant.

- [ ] **Step 6: Commit**

```bash
git add scripts/validate_repository.py tests
git commit -m "feat: cross-check manifests and checksums"
```

---

### Task 5: Reject official binary payloads accidentally committed to Git

**Files:**
- Modify: `tests/test_repository_validator.py`
- Modify: `scripts/validate_repository.py`

**Interfaces:**
- Produces:

```python
def validate_repository_hygiene(root: Path) -> list[ValidationFinding]: ...
```

- [ ] **Step 1: Write failing hygiene test**

Create a temporary repository-like directory with:

```text
data/originals/example.pdf
```

and assert that validation emits `REPOSITORY_BINARY_IN_GIT`.

- [ ] **Step 2: Run and verify RED**

```bash
python -m unittest tests.test_repository_validator
```

Expected: FAIL because hygiene validation is absent.

- [ ] **Step 3: Implement minimal binary guard**

Reject files physically present under `data/originals/` with case-insensitive suffixes:

```python
_BINARY_SUFFIXES = {
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip", ".7z", ".rar"
}
```

Do not inspect paths recorded in `SHA256SUMS`; only inspect files physically present in the clone.

- [ ] **Step 4: Verify GREEN on fixture and real repo**

```bash
python -m unittest tests.test_repository_validator
```

Expected: PASS and no false positives from the manifest/checksum metadata.

- [ ] **Step 5: Commit**

```bash
git add scripts/validate_repository.py tests
git commit -m "feat: guard original binaries from git"
```

---

### Task 6: Compose one repository command and human-readable report

**Files:**
- Modify: `tests/test_repository_validator.py`
- Modify: `scripts/validate_repository.py`

**Interfaces:**
- Produces:

```python
def validate_repository(root: Path) -> list[ValidationFinding]: ...
def main() -> int: ...
```

- [ ] **Step 1: Write failing composition and CLI tests**

Add:

```python
def test_real_repository_passes_validator(self):
    self.assertEqual(validate_repository(ROOT), [])
```

and capture stdout for `main([str(ROOT)])` or design `main(argv: Sequence[str] | None = None) -> int` so tests can invoke it directly.

Expected success output contains:

```text
PASS registry
PASS originals
PASS repository-hygiene
Repository validation passed
```

- [ ] **Step 2: Run and verify RED**

```bash
python -m unittest tests.test_repository_validator
```

Expected: FAIL because the composed API/CLI is not yet implemented.

- [ ] **Step 3: Implement composition and formatter**

Use:

```python
def validate_repository(root: Path) -> list[ValidationFinding]:
    findings = []
    findings.extend(validate_registry(root / "sources" / "registry.yaml"))
    findings.extend(validate_originals(root / "data" / "originals"))
    findings.extend(validate_repository_hygiene(root))
    return sorted(findings, key=lambda item: (item.path, item.code, item.message))
```

`main()` should:

- resolve root from optional CLI positional argument, defaulting to repository root relative to `__file__`
- print compact PASS domain lines when no findings occur
- print each finding as `<CODE> <path> <message>` to stderr when failures occur
- return `0` on success, `1` on validation findings, `2` on invalid CLI usage

Do not use color codes so CI logs remain machine-readable.

- [ ] **Step 4: Verify GREEN**

```bash
python -m unittest tests.test_repository_validator
python -m scripts.validate_repository
```

Expected: tests PASS and CLI exits 0 with the PASS summary.

- [ ] **Step 5: Run all current unit tests**

```bash
python -m unittest tests.test_career_wiki tests.test_repository_validator
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add scripts/validate_repository.py tests
git commit -m "feat: add repository validation command"
```

---

### Task 7: Make the validator a required part of deterministic CI

**Files:**
- Modify: `.github/workflows/ci.yml`

**Interfaces:**
- Consumes: `python -m scripts.validate_repository`.
- Produces: the existing stable required-check candidate `repository-ci`, now covering repository provenance structure.

- [ ] **Step 1: Add the validator after tests and before MkDocs**

Use:

```yaml
      - name: Validate repository integrity
        run: python -m scripts.validate_repository
```

The complete deterministic order becomes:

```text
install dependencies
→ unit tests
→ repository validator
→ mkdocs build --strict
```

- [ ] **Step 2: Verify no live source probe was introduced**

Search `.github/workflows/ci.yml` and confirm it contains no `curl`, `wget`, `requests`, government hostname, or source-health command.

- [ ] **Step 3: Push implementation PR and verify fresh CI**

Required evidence before merge:

```text
repository-ci       success
CodeQL              success
Analyze (actions)   success
Analyze (python)    success
pr-labeler          success
```

`repository-ci` logs must show all three repository commands executing successfully:

```text
python -m unittest ...
python -m scripts.validate_repository
mkdocs build --strict
```

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/ci.yml
git commit -m "ci: enforce repository integrity validation"
```

---

## Verification Checklist

Before merge:

- [ ] New tests were observed failing before each production behavior was added.
- [ ] `python -m unittest tests.test_repository_validator` passes.
- [ ] `python -m unittest tests.test_career_wiki tests.test_repository_validator` passes.
- [ ] `python -m scripts.validate_repository` exits 0 on the real repository.
- [ ] Real `sources/registry.yaml` passes structural validation.
- [ ] All listed manifest fragments exist and every actual fragment is listed.
- [ ] Every manifest SHA is 64 lowercase hex characters.
- [ ] Every manifest document has a matching `SHA256SUMS` path and digest.
- [ ] No official PDF/DOC/XLS/ZIP payload is physically committed beneath `data/originals/`.
- [ ] `repository-ci` remains offline.
- [ ] MkDocs strict build remains green.
- [ ] CodeQL reports no new alerts in changed code.

## Deferred Deliberately

The following are separate migrations, not hidden in this PR:

- canonicalize historical manifest IDs to registry `source_id`
- add `document_id`, legal status, publication/effective dates, and change events
- add corpus YAML front matter
- add claim-level source locators
- generate catalog/root manifests rather than maintaining them manually
- live source-health monitoring
- RAG benchmark and retrieval evaluation
