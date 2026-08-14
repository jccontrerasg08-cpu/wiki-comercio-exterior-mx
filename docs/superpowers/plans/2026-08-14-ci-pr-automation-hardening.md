# CI and PR Automation Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Harden deterministic pull-request CI and add low-risk automatic PR labeling without increasing the repository's runtime or infrastructure complexity.

**Architecture:** Keep one required offline `repository-ci` job for repository correctness and a separate metadata-only `pr-labeler` workflow for triage. All third-party Actions are pinned to full commit SHAs. `pr-labeler` uses `pull_request_target` only because it does not check out or execute pull-request code; it reads the base-repository label configuration and has only `contents: read` plus `pull-requests: write`.

**Tech Stack:** GitHub Actions, Python 3.12, MkDocs Material, YAML, existing `unittest` suite.

## Global Constraints

- Preserve the approved Mexico-first project scope and keep `arancel-mx` as the canonical structured Mexican tariff/NICO data layer.
- Required PR CI must remain offline and deterministic.
- Do not introduce `tj-actions/changed-files`; use native Git behavior or official GitHub Actions when change information is needed.
- Pin every referenced GitHub Action to a full commit SHA and retain the human-readable release in a trailing comment.
- Do not check out pull-request code in any `pull_request_target` workflow.
- Keep workflow permissions minimal and explicit.
- Do not add a backend, database, vector store, container runtime, or JavaScript application.

---

## File Structure

- Modify `.github/workflows/ci.yml`: pin existing Actions to immutable SHAs while preserving the current deterministic MkDocs/test gate.
- Create `.github/labeler.yml`: path-to-label rules using labels that already exist in this repository.
- Create `.github/workflows/labeler.yml`: metadata-only automatic PR labeler with minimal permissions.
- Modify `.github/dependabot.yml`: no functional expansion unless required to keep full-SHA Action references maintainable.
- No production content, corpus, registry, or legal-source files change in this plan.

---

### Task 1: Pin deterministic CI Actions to immutable SHAs

**Files:**
- Modify: `.github/workflows/ci.yml`

**Interfaces:**
- Consumes: current `repository-ci` workflow and `requirements-docs.txt`.
- Produces: the same `repository-ci` check name, now using immutable Action references.

- [ ] **Step 1: Confirm the current workflow contract**

Verify `.github/workflows/ci.yml` still contains:

```yaml
permissions:
  contents: read

jobs:
  repository-ci:
    name: repository-ci
```

and these deterministic commands:

```yaml
- run: python -m unittest tests.test_career_wiki
- run: mkdocs build --strict
```

Expected: both commands are present and no live government URL probe exists in this workflow.

- [ ] **Step 2: Replace floating `actions/checkout@v4`**

Use the current `actions/checkout` release `v7.0.1` commit:

```yaml
- name: Checkout repository
  uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
  with:
    persist-credentials: false
```

- [ ] **Step 3: Replace floating `actions/setup-python@v5`**

Use the current `actions/setup-python` release `v7.0.0` commit:

```yaml
- name: Set up Python
  uses: actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97 # v7.0.0
  with:
    python-version: "3.12"
```

- [ ] **Step 4: Verify no floating Action refs remain in CI**

Run a repository search equivalent to:

```text
.github/workflows/ci.yml: "uses:"
```

Expected exact Action references:

```text
actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97
```

- [ ] **Step 5: Verify the PR workflow run**

Expected checks on the implementation PR:

```text
repository-ci  success
CodeQL         success
```

The `repository-ci` job must still install `requirements-docs.txt`, run `python -m unittest tests.test_career_wiki`, and run `mkdocs build --strict`.

- [ ] **Step 6: Commit**

```bash
git add .github/workflows/ci.yml
git commit -m "ci: pin core GitHub Actions by SHA"
```

---

### Task 2: Add deterministic path-based PR labels

**Files:**
- Create: `.github/labeler.yml`
- Create: `.github/workflows/labeler.yml`

**Interfaces:**
- Consumes: existing repository labels `documentation`, `dependencies`, `github_actions`, and `python`.
- Produces: automatic labels on pull requests based on changed paths.

- [ ] **Step 1: Create the label configuration using only existing labels**

Create `.github/labeler.yml` with:

```yaml
changed-files-labels-limit: 4
max-files-changed: 500

documentation:
  - changed-files:
      - any-glob-to-any-file:
          - "**/*.md"
          - "mkdocs.yml"
          - "docs/**"

dependencies:
  - changed-files:
      - any-glob-to-any-file:
          - "requirements*.txt"
          - ".github/dependabot.yml"

github_actions:
  - changed-files:
      - any-glob-to-any-file:
          - ".github/workflows/**"
          - ".github/labeler.yml"
          - ".github/dependabot.yml"

python:
  - changed-files:
      - any-glob-to-any-file:
          - "**/*.py"
```

Expected behavior:

| Change | Labels |
|---|---|
| `docs/wiki/foo.md` | `documentation` |
| `requirements-docs.txt` | `dependencies` |
| `.github/workflows/ci.yml` | `github_actions` |
| `.github/dependabot.yml` | `dependencies`, `github_actions` |
| `scripts/validate_repository.py` | `python` |

- [ ] **Step 2: Create the metadata-only workflow**

Create `.github/workflows/labeler.yml` with:

```yaml
name: pr-labeler

on:
  pull_request_target:
    types:
      - opened
      - synchronize
      - reopened

permissions:
  contents: read
  pull-requests: write

concurrency:
  group: pr-labeler-${{ github.event.pull_request.number }}
  cancel-in-progress: true

jobs:
  label:
    name: pr-labeler
    runs-on: ubuntu-latest
    timeout-minutes: 5

    steps:
      - name: Label pull request
        uses: actions/labeler@bf12e9b00b37c5c0ca2b87b79b2daf7891dbda13 # v7.0.0
        with:
          sync-labels: true
```

- [ ] **Step 3: Confirm the `pull_request_target` safety invariant**

The workflow must contain none of the following:

```text
actions/checkout
head.sha
pull_request.head
run:
```

Expected: the workflow only invokes the pinned `actions/labeler` Action and never executes content from the pull-request branch.

- [ ] **Step 4: Verify permissions are minimal**

Expected exact workflow permissions:

```yaml
permissions:
  contents: read
  pull-requests: write
```

No `issues: write`, `actions: write`, `contents: write`, `id-token: write`, or `security-events: write` permission is allowed.

- [ ] **Step 5: Verify labels on the implementation PR after the workflow exists on the base branch**

After this workflow is merged, the next PR that edits `.github/workflows/**` should automatically receive:

```text
github_actions
```

A documentation-only PR should receive:

```text
documentation
```

- [ ] **Step 6: Commit**

```bash
git add .github/labeler.yml .github/workflows/labeler.yml
git commit -m "ci: add safe pull request labeling"
```

---

### Task 3: Resolve superseded dependency PRs cleanly

**Files:**
- No repository file changes required.

**Interfaces:**
- Consumes: Dependabot PRs #4, #5, and #6.
- Produces: a clean PR queue without redundant Action-version updates.

- [ ] **Step 1: Confirm the hardening PR uses newer immutable versions**

Expected:

```text
checkout       v7.0.1 full SHA
setup-python   v7.0.0 full SHA
```

- [ ] **Step 2: Close Dependabot PR #4 after the pinning PR merges**

Reason:

```text
Superseded by the repository hardening PR, which upgrades setup-python to v7.0.0 and pins the immutable full commit SHA.
```

- [ ] **Step 3: Close Dependabot PR #5 after the pinning PR merges**

Reason:

```text
Superseded by the repository hardening PR, which upgrades checkout to v7.0.1 and pins the immutable full commit SHA.
```

- [ ] **Step 4: Keep PR #6 separate**

Do not bundle `mkdocs-material 9.6.22 -> 9.7.7` into the Action-pinning PR. The docs dependency update includes a security fix and should be validated independently by the now-existing `mkdocs build --strict` gate.

Expected: PR #6 remains independently reviewable until its own checks are evaluated.

---

### Task 4: Document the change-detection dependency decision

**Files:**
- Modify: `docs/superpowers/specs/2026-08-14-repository-hardening-design.md` only if a permanent architecture note is needed during implementation review.

**Interfaces:**
- Consumes: the approved repository hardening design.
- Produces: an explicit rule that change detection should not add a third-party Action unless native Git/GitHub capabilities are insufficient.

- [ ] **Step 1: Preserve the no-extra-dependency default**

The implementation must not add:

```yaml
uses: tj-actions/changed-files@...
```

- [ ] **Step 2: Use the appropriate mechanism by purpose**

Use:

```text
actions/labeler     -> PR triage based on changed paths
native git diff     -> future deterministic CI path filtering, if needed
GitHub API          -> PR metadata when a workflow genuinely needs API context
```

- [ ] **Step 3: Keep any future `git diff` helper local and testable**

If later required, implement it as repository-owned Python or shell logic covered by tests rather than adding another external Action solely for file selection.

---

## Verification Checklist

Before merging the implementation PR:

- [ ] `repository-ci` passes.
- [ ] CodeQL passes.
- [ ] `mkdocs build --strict` still passes.
- [ ] All workflow `uses:` entries changed by this plan are full 40-character SHAs.
- [ ] `pr-labeler` has no checkout and no `run:` step.
- [ ] `pr-labeler` has only `contents: read` and `pull-requests: write`.
- [ ] `.github/labeler.yml` references only labels that already exist in the repository.
- [ ] No `tj-actions/changed-files` dependency is introduced.
- [ ] Dependabot PR #6 remains separate for independent docs/security validation.

## Follow-on Plan

After this plan is merged and verified, the next implementation plan is the repository validator:

```text
registry schema
→ manifest references
→ SHA format
→ temporal invariants
→ corpus metadata
→ known-bad fixtures
→ one `python -m scripts.validate_repository` entry point
```
