# Corpus Coverage Dashboard Design

## Goal

Add a reproducible governance dashboard that summarizes how much of the governed wiki/corpus is reviewed, current, traceable, and eligible for current-answer retrieval without presenting the result as a measure of legal truth.

## Scope

The dashboard covers only content already governed by `sources/page_metadata.yaml`, currently `docs/wiki/**` Markdown and `data/corpus/**` Markdown/CSV. It does not infer legal validity from network availability, does not score substantive legal correctness, and does not change any RAG eligibility rule.

## Architecture

One dependency-free Python module, `scripts/coverage_report.py`, loads and validates existing page metadata, computes a deterministic `CoverageReport`, renders both machine-readable JSON and a public Markdown dashboard, and evaluates an explicit regression policy.

Generated outputs:

- `reports/corpus-coverage.json`: canonical machine-readable snapshot.
- `docs/status/corpus-coverage.md`: public human-readable dashboard.
- `coverage-policy.yaml`: reviewed minimum/maximum guardrails used by CI.

The report is deterministic: it contains no wall-clock timestamp. Its freshness marker is derived from metadata, using the maximum `reviewed_at` value in the governed corpus.

## Metrics

Top-level counts:

- total governed pages
- wiki pages
- corpus pages
- pages with at least one source reference
- pages with at least one instrument reference
- current-answer retrieval-eligible pages
- distinct referenced source IDs
- distinct referenced instrument IDs

Status distributions are emitted for:

- `source_status`
- `extraction_status`
- `legal_review_status`
- `corpus_status`

A page is **retrieval eligible** when all of these hold:

- `source_status == current`
- `legal_review_status == reviewed`
- `corpus_status in {current, not_applicable}`

This mirrors the current RAG admission rule and must not diverge from it.

## Risk queue

Every governed page receives zero or more deterministic risk reasons. The public page lists only pages that need attention. Reasons include:

- `pending_legal_review`
- `source_not_current`
- `extraction_incomplete`
- `corpus_not_current`
- `missing_source_reference`
- `missing_instrument_reference`

A missing instrument reference is informational for data fixtures and becomes a governance risk for wiki explainers/explanatory digests.

## Section coverage

The report groups wiki pages by their first directory below `docs/wiki/` (for example `aduana`, `clasificacion`, `rrna`) and groups `data/corpus/**` under `corpus`. Each group exposes total pages, retrieval-eligible pages, reviewed pages, and pages needing attention.

## Regression policy

`coverage-policy.yaml` contains reviewed guardrails, not generated values. CI enforces:

Minimum floors:

- retrieval-eligible page count
- pages with source references
- pages with instrument references
- legally reviewed page count

Maximum ceilings:

- pending legal review page count
- stale/partial/unknown corpus page count
- unknown source-status page count

Improvements pass without editing policy. A regression fails until the data is fixed or a deliberate policy change is reviewed in the PR.

The policy does not freeze total page count so adding well-governed content does not require a baseline edit.

## CLI

`python -m scripts.coverage_report`

Writes both generated outputs.

`python -m scripts.coverage_report --check`

Validates page metadata first, verifies generated outputs match the canonical render, evaluates policy guardrails, prints a concise summary, and exits non-zero on drift or regression.

## CI and Pages

Repository CI runs `python -m scripts.coverage_report --check` after the existing provenance inventory check.

The Pages workflow runs the same check before the strict MkDocs build, ensuring the public dashboard cannot be stale at deployment time.

## Public UX

The dashboard is linked from top-level MkDocs navigation as `Estado del corpus`. It starts with a warning that the numbers measure repository governance/readiness, not whether a legal conclusion is substantively correct.

## Testing

Tests cover:

- deterministic aggregation from a fixture
- exact retrieval-eligibility semantics
- deterministic risk reasons
- policy pass/fail behavior
- generated Markdown/JSON drift detection
- real repository report generation
- workflow wiring

The final verification remains the repository's full CI suite, strict MkDocs build, provenance validation, temporal graph validation, RAG evaluation, and legacy-route verification.
