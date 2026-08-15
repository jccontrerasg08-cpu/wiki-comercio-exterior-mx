# Temporal Legal Knowledge Platform Design

**Status:** approved direction, implementation gated by this written specification  
**Date:** 2026-08-15  
**Repository:** `jccontrerasg08-cpu/wiki-comercio-exterior-mx`

## Objective

Evolve the repository from a curated collection of legal documents into a temporal, provenance-first knowledge system. Every legal assertion must be traceable to an official source, scoped to a period of validity, and explicit about whether it is authoritative text, a project-authored explanation, or a retrieval digest.

The work preserves the current four-layer architecture and the boundary with `arancel-mx`. Structured tariff rows remain in `arancel-mx`; this repository owns explanatory documentation, official-source discovery, immutable evidence manifests, and RAG-oriented derived content.

## Binding constraints

1. Preserve `docs/wiki/`, `docs/catalog/`, `sources/`, `data/originals/`, and `data/corpus/` as distinct responsibilities until a compatibility migration is complete.
2. Do not scrape INEGI TIGIE-SCIAN, SNICE Mi Fraccion, ICC rule text, or WCO explanatory notes.
3. Do not commit official binary payloads to Git. Store manifests and checksums in Git and payloads in immutable GitHub Releases.
4. Treat DOF/SIDOF as publication authority, Diputados as a consolidated-text source, and SAT, ANAM, SE, SNICE, and VUCEM as administrative sources.
5. Keep pull-request CI deterministic and offline. External-source checks run only in scheduled or manually dispatched workflows.
6. Preserve the repository rule of one coherent legal or source event per pull request. Platform-only changes may use their own pull request.
7. Use primary official sources for legal status. Secondary sources may aid discovery but never establish validity.
8. Do not present the wiki or corpus as legal advice or as a substitute for the official publication.
9. Keep international tariff coverage at HS6. National tariff extensions remain external catalog references except for Mexico-specific explanations.
10. All generated files must be reproducible from reviewed source data.

## Delivery model

The requested scope is a program of compatible pull requests, not one oversized change. Mixing unrelated legal events would contradict `CONTRIBUTING.md` and make review, rollback, and temporal attribution unreliable.

### Pull request sequence

1. **Platform foundation:** schemas, temporal model, catalog generator, validators, front matter contract, deterministic CI, site integration, governance, and RAG evaluation harness.
2. **Reglamento de la Ley Aduanera event:** DOF publication 5780677 dated 2026-02-23, consolidated-source relation, change digest, and currentness tests.
3. **Ley de Comercio Exterior family:** law and regulation as separate instruments with consolidated-text metadata.
4. **SE Rules baseline:** agreement published 2022-05-09 and its modification graph.
5. **SE modification events:** one PR for each 2025-09-02, 2026-02-12, 2026-04-02, 2026-05-28, and 2026-05-29 publication.
6. **Tax framework:** CFF, VAT, IEPS, and Federal Duties instruments, split by coherent source event where required.
7. **Programs:** IMMEX, PROSEC, Drawback, certification schemes, and related source relationships.
8. **RRNA authority families:** Economy, Health, Agriculture, Environment, Energy, Defense, Culture, and Telecommunications.
9. **Treaties and origin:** one treaty family per PR, using existing captured evidence first.
10. **Operational explainers:** customs regimes, clearance, valuation, enforcement, remedies, and electronic systems.

Only the first pull request is created from this branch. Later legal-event branches must start from the merged platform foundation so they all use the same schema and validation rules.

## Architecture

### Existing layers

| Layer | Responsibility | Authority |
|---|---|---|
| `docs/wiki/` | Project-authored explanations | Non-authoritative |
| `docs/catalog/` | Human-readable official-source catalog | Derived from registry |
| `sources/` | Canonical source and legal-event metadata | Reviewed project data |
| `data/originals/` | Manifests and checksums for immutable evidence | Evidence metadata |
| `data/corpus/` | Retrieval-oriented digests | Non-authoritative derivative |

### New foundation components

| Component | Responsibility |
|---|---|
| `schemas/source.schema.json` | Validate official source records |
| `schemas/instrument.schema.json` | Validate legal instruments and temporal status |
| `schemas/page-frontmatter.schema.json` | Validate wiki and corpus provenance metadata |
| `sources/instruments.yaml` | Canonical instrument and relationship graph |
| `scripts/build_catalog.py` | Generate the human catalog from canonical YAML |
| `scripts/validate_frontmatter.py` | Enforce page metadata and source references |
| `scripts/validate_temporal_graph.py` | Validate dates, relation targets, cycles, and status consistency |
| `scripts/source_health.py` | Probe external sources outside PR CI |
| `scripts/legal_watch.py` | Detect candidate official publications without asserting legal conclusions |
| `evals/` | Deterministic retrieval and temporal-answer fixtures |

Each component has one responsibility. Network access is injected into health and discovery functions so unit tests use local fixtures rather than live services.

## Canonical data model

### Source record

Existing `sources/registry.yaml` remains the canonical URL registry. Records gain optional, backward-compatible fields:

```yaml
id: mx_dof_rla_reform_20260223
jurisdiction: MEX
title: Decreto de reforma al Reglamento de la Ley Aduanera
url: https://www.dof.gob.mx/nota_detalle.php?codigo=5780677&fecha=23/02/2026
note_id: "5780677"
authority: DOF
evidence_class: primary_legal
instrument_id: mx_reglamento_ley_aduanera
publication_date: 2026-02-23
retrieved_at: 2026-08-15T00:00:00Z
harvest: true
cadence_days: 1
```

`retrieved_at` records observation, not validity. `publication_date` records the official event date. A successful HTTP response never establishes legal status by itself.

### Instrument record

```yaml
id: mx_reglamento_ley_aduanera
jurisdiction: MEX
title: Reglamento de la Ley Aduanera
instrument_type: regulation
status: current
publication_date: 2015-04-20
effective_from: 2015-06-20
effective_to: null
consolidated_source_id: mx_diputados_reg_ley_aduanera
current_through: 2026-02-23
events:
  - source_id: mx_dof_rla_reform_20260223
    relation: amends
    effective_from: 2026-02-24
```

Allowed relations are `implements`, `regulates`, `amends`, `repeals`, `supersedes`, `references`, `has_annex`, `applies_to`, `interpreted_by`, and `corrected_by`.

Allowed status values are `current`, `stale`, `superseded`, `partial`, `pending_review`, `withdrawn`, and `unknown`. Source status, extraction status, legal-review status, and corpus status remain separate dimensions.

### Page metadata

Wiki and corpus pages use validated YAML front matter:

```yaml
---
title: Control de inventarios IMMEX
source_ids:
  - mx_sidof_rgce_2026_anexos_21_30
instrument_ids:
  - mx_rgce_2026_anexo_24
jurisdiction: MEX
topic: immex
effective_from: 2026-01-01
current_through: 2026-05-20
reviewed_at: 2026-08-15
source_status: current
extraction_status: complete
legal_review_status: pending_review
corpus_status: current
content_type: explanatory_digest
legal_authority: non_authoritative
---
```

Migration is incremental. Existing pages without front matter produce a bounded migration report at first; strict enforcement is enabled only after all tracked pages are migrated in reviewed batches.

## Data flows

### Deterministic pull-request flow

1. Validate YAML and JSON Schema.
2. Validate unique IDs and relationship targets.
3. Validate temporal ordering and reject impossible date ranges.
4. Generate the catalog into a temporary directory.
5. Compare generated output with committed output.
6. Validate front matter and local links.
7. Run unit tests and RAG fixture evaluations.
8. Build MkDocs in strict mode.

No PR check calls DOF, SAT, SNICE, or another external service.

### Scheduled source-health flow

1. Select due registry entries by cadence.
2. Use conditional requests when ETag or Last-Modified metadata exists.
3. Validate status, final host, MIME type, minimum size, rejection markers, and expected title or note ID.
4. Calculate SHA-256 only for valid payloads.
5. Classify changes as unchanged, transport failure, suspicious response, or candidate content change.
6. Upload a bounded JSON report as an Actions artifact.
7. Open or update one deduplicated issue for actionable findings. The workflow does not modify legal content automatically.

### Legal-watch flow

1. Query configured official discovery endpoints.
2. Normalize publication identifiers and dates.
3. Compare candidates against known `note_id` and URLs.
4. Produce a candidate report with official links and matched keywords.
5. Open a review issue. A human-reviewed PR establishes instrument relationships and currentness.

## Documentation site

The site root becomes `docs/` so the wiki, catalog, methodology, changes, glossary, and architecture are built together. Existing public file URLs receive compatibility stub pages or redirects where MkDocs supports them.

Proposed navigation:

```text
Inicio
Aprender
  Fundamentos
  Aduana
  Clasificacion
  Contribuciones
  Programas
  Logistica
Fuentes oficiales
Cambios normativos
Glosario
Metodologia
Arquitectura
```

Every rendered knowledge page shows review date, current-through date, status, source links, and a non-authoritative notice. Stale or partial pages receive a visible warning.

GitHub Pages deployment occurs only after deterministic CI succeeds on `main`. The deployment workflow uses GitHub's Pages artifact and OIDC flow with minimal permissions.

## RAG evaluation

The repository adds deterministic evaluation cases without adding an online LLM dependency. Each case contains a question, expected source IDs, forbidden superseded sources, temporal cutoff, and required disclaimer.

Initial metrics are source recall at k, reciprocal rank, temporal-source accuracy, and citation presence. A lexical baseline is sufficient for CI; future embedding or hybrid retrieval evaluation may run manually or offline with pinned models.

Tests must cover:

- confusion between RGCE 2025 and RGCE 2026;
- confusion between a law, its regulation, rules, and annexes;
- questions whose answer changed after a dated modification;
- abstention when the repository lacks evidence;
- rejection of a source dated after the query cutoff.

## Legal coverage roadmap

### Priority 0

- Constitution provisions relevant to customs and taxation.
- Customs Law and the 2026 reformed Customs Law Regulation.
- Foreign Trade Law and its Regulation.
- 2026 RGCE and modification events.
- Economy Ministry Rules and Criteria, including Annexes 2.2.1 and 2.4.1.
- Federal Tax Code, VAT Law, IEPS Law, Federal Duties Law, and applicable regulations.
- Infrastructure Quality Law for the current NOM framework.

### Priority 1

- IMMEX, PROSEC, Drawback, certification, VAT/IEPS guarantees, importer registers, VUCEM, electronic value declaration, DODA, and PITA.
- RRNA families by competent authority.
- Customs valuation, contributions, guarantees, sanctions, PAMA, and remedies.

### Priority 2

- Treaty families and origin procedures.
- Customs regimes and operational explainers.
- Country catalogs and international data sources, without duplicating tariff databases.

## Repository governance

- Fix the contradictory scraping instruction in `CONTRIBUTING.md` immediately in the platform foundation PR.
- Add `GOVERNANCE.md`, `MAINTAINERS.md`, and a documented page-status policy.
- Correct the repository topic spelling from `tarriffs` to `tariffs` through repository settings.
- Prefer squash merging and automatic branch deletion after merge; branch protection remains a repository-owner setting verified separately.
- Use generated changelogs for legal events, never semantic-version claims about legal validity.
- Label candidate issues by `authority`, `instrument`, `event-date`, and `review-status`.

## Failure handling

- Network failures do not fail pull-request CI.
- A suspicious HTTP 200 response is classified separately from a valid document.
- Discovery never changes `status: current` automatically.
- A missing or cyclic relationship fails deterministic validation.
- A digest older than a known modifying event is marked stale or rejected from a current-only RAG evaluation.
- Generated-output drift fails CI with the regeneration command.
- Workflow issue creation is deduplicated by stable source or candidate key.

## Security and supply chain

- Pin third-party Actions by full commit SHA.
- Use minimal job permissions and disable persisted checkout credentials.
- Treat downloaded HTML, PDFs, and metadata as untrusted input.
- Bound download size, redirects, decompression, parsing time, and logged response bodies.
- Never execute content extracted from official documents.
- Add CodeQL for Python and Actions workflow scanning.
- Keep secrets out of fork-triggered workflows and do not run untrusted PR code with write tokens.

## Verification and acceptance criteria

The platform foundation is complete only when fresh evidence shows:

1. Existing 18 baseline tests still pass.
2. New schema, temporal graph, generator, health-probe, legal-watch, front matter, and RAG tests pass.
3. Repository validation passes with no findings.
4. Generated catalog matches committed output.
5. MkDocs builds in strict mode from the integrated documentation root.
6. Workflow YAML parses and all Actions remain SHA pinned.
7. External probes are covered by fixture tests and a bounded manual smoke test against official sources.
8. The full diff contains no binaries, credentials, unrelated refactors, or accidental copied proprietary text.
9. The pull request describes scope, source authority, test evidence, compatibility, and deferred legal-event PRs.

Each later legal-event PR must additionally prove that its official URL, publication identifier, date, effective date, relationship, digest status, and current-through date agree across registry, instrument graph, wiki/corpus metadata, and tests.

## Explicit non-goals

- Legal advice or automatic compliance decisions.
- Automatic declaration that a legal instrument is current.
- A worldwide national-tariff database.
- Copying ICC Incoterms rules or WCO explanatory notes.
- Scraping interactive classifiers without an approved official data interface.
- Moving structured TIGIE/NICO tariff rows out of `arancel-mx`.
- Bulk-importing every official publication before the temporal model and validators are merged.

## Official evidence used for this design

- RGCE 2026: DOF note `5777199`.
- First RGCE 2026 modification: DOF note `5787425`, published 2026-05-14.
- Customs Law Regulation reform: DOF note `5780677`, published 2026-02-23 and effective the following day.
- Economy Ministry legal library: modification sequence through 2026-05-29.
- SNICE IMMEX normative index and customs/foreign-trade legal library.

