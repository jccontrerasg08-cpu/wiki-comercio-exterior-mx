# Wiki Legal Depth Wave 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Correct legally over-broad public statements, add missing 2026 operational pages, and deepen the highest-risk wiki topics while preserving temporal provenance and offline deterministic CI.

**Architecture:** Keep `docs/wiki/` as non-authoritative, source-linked explainers. Every legal statement must identify the governing instrument or official source and use conditional language where applicability depends on merchandise, regime, origin, actor, value, date, or authorization. Extend `sources/registry.yaml`, `sources/instruments.yaml`, and `sources/page_metadata.yaml` only for new official instruments/pages, then regenerate the coverage outputs.

**Tech Stack:** MkDocs Material, Markdown, YAML provenance registries, Python repository validators, `unittest`/repository test suite, GitHub Actions.

## Global Constraints

- Official source first: DOF/SIDOF, SAT, ANAM, SNICE/Secretaría de Economía, Cámara de Diputados, ICC or WTO only for their own instruments.
- A successful HTTP response is not evidence of legal currentness.
- Do not promote legal content automatically from network observations; review status changes are explicit repository changes.
- Preserve `arancel-mx` as the structured TIGIE/NICO data layer; the wiki explains legal context without duplicating its catalog.
- Preserve legacy redirects and strict MkDocs build behavior.
- Use conditional wording instead of false absolutes such as `siempre`, `sin inscripción no procede`, or `fracción + país basta`.
- New public legal pages must have page metadata and source/instrument traceability before merge.

---

### Task 1: Lock the legal accuracy contract in tests

**Files:**
- Create: `tests/test_wiki_legal_depth.py`

**Interfaces:**
- Consumes: public Markdown files and `mkdocs.yml`.
- Produces: regression checks for source-linked wording and the new operational pages.

- [x] **Step 1: Write failing tests** requiring Padrón exceptions (RGCE 1.3.1/1.3.5/1.3.6 + Annexes 7/8/9), separate treatment of cuotas compensatorias from IGI, Incoterms caveat, UCP 600 on documentary credits, a 2026 timeline containing 31-Mar/23-Apr/4-May, and new pages for VUCEM, agente/agencia aduanal, manifestación de valor, despacho and PAMA.
- [x] **Step 2: Run the focused test in CI/PR and confirm it fails only because the approved content is absent.**
- [x] **Step 3: Keep the test semantic rather than line-number based so editorial improvements do not create unnecessary churn.**

### Task 2: Correct the high-risk existing explainers

**Files:**
- Modify: `docs/wiki/fundamentos/padron-importadores.md`
- Modify: `docs/wiki/contribuciones/cuotas-compensatorias.md`
- Modify: `docs/wiki/contribuciones/aranceles.md`
- Modify: `docs/wiki/logistica/incoterms.md`
- Modify: `docs/wiki/logistica/pagos-internacionales.md`
- Modify: `docs/wiki/aduana/anam.md`
- Modify: `docs/wiki/aduana/documentos.md`
- Modify: `docs/wiki/aduana/cambios-2026.md`

**Interfaces:**
- Consumes: existing official source IDs and current 2026 publications.
- Produces: public explanations that distinguish general rules from exceptions and legal concepts from operational shorthand.

- [x] **Step 1:** Replace the Padrón absolute with the general-rule/exceptions formulation tied to RGCE 1.3.1, 1.3.5, 1.3.6 and Annexes 7, 8 and 9.
- [x] **Step 2:** Explain cuotas compensatorias as legally separate measures whose applicability depends on the exact resolution, including product scope, origin/exporter/producer/value/vigency/exceptions, not merely fraction + country.
- [x] **Step 3:** Clarify that preferential treatment can lower IGI, while cuotas compensatorias are separate additional obligations when applicable.
- [x] **Step 4:** Clarify Incoterms: allocation of costs/risks/clearance obligations can affect valuation inputs, but Incoterms do not determine Mexican customs procedure, legal importer, tariff or pedimento filer by themselves.
- [x] **Step 5:** Ground documentary-credit material in ICC UCP 600 and distinguish bank document examination from customs compliance.
- [x] **Step 6:** Reframe VUCEM references in light of the 4-May-2026 Ventanilla Única decree.
- [x] **Step 7:** Replace `Siempre (despacho definitivo)` with a conditional document matrix and explicit dependence on regime, merchandise, transport and legal assumption.
- [x] **Step 8:** Convert `Cambios 2026` into a dated timeline including the 31-Mar article 159 bis lineamientos, 23-Apr TIGIE/PROSEC decree, 4-May Ventanilla Única decree, 14-May 1st RMRGCE and 20-May annex modifications.

### Task 3: Deepen customs valuation

**Files:**
- Modify: `docs/wiki/contribuciones/valor-en-aduana.md`
- Create: `docs/wiki/aduana/manifestacion-valor.md`

**Interfaces:**
- Consumes: Ley Aduanera valuation framework, WTO Customs Valuation Agreement context and VUCEM/MV operational references.
- Produces: a 900–1,400 word valuation explainer and a focused MV page.

- [x] **Step 1:** Explain transaction value as the primary method subject to legal conditions and adjustments.
- [x] **Step 2:** Explain incrementables/non-incrementables, relationship between parties and when method 1 is not acceptable.
- [x] **Step 3:** Describe the sequence of identical, similar, deductive, computed and fallback methods without presenting the summary as the binding text.
- [x] **Step 4:** Add a worked numerical example clearly labeled pedagogical.
- [x] **Step 5:** Separate Incoterm allocation from legal customs-valuation adjustments.
- [x] **Step 6:** Add MV purpose, responsible actor, evidence and VUCEM relationship on the new page.

### Task 4: Add missing 2026 customs operation pages

**Files:**
- Create: `docs/wiki/aduana/vucem.md`
- Create: `docs/wiki/aduana/agente-agencia-aduanal.md`
- Create: `docs/wiki/aduana/proceso-despacho.md`
- Create: `docs/wiki/aduana/infracciones-pama.md`
- Modify: `mkdocs.yml`
- Modify: `docs/wiki/index.md`

**Interfaces:**
- Consumes: Ley Aduanera, RLA reform, 159 bis lineamientos, RGCE 2026 and the Ventanilla Única decree.
- Produces: navigable operational explanations linked into the public wiki.

- [x] **Step 1:** Explain the 2026 Ventanilla Única legal transition and distinguish the platform/service layer from the customs authority and legal effects of each filing.
- [x] **Step 2:** Explain agent vs agency, patent/authorization, responsibility and the 159 bis Council process without treating the private customs agent as ANAM.
- [x] **Step 3:** Add an end-to-end dispatch flow: classify, RRNA, value, documents, pedimento, payment/validation, activation, automated-selection/review where applicable, release and post-entry evidence.
- [x] **Step 4:** Add a PAMA/infringement overview that distinguishes inspection findings, precautionary seizure and administrative procedure, with explicit instruction to consult the current Ley Aduanera for grounds and deadlines.
- [x] **Step 5:** Add the pages to MkDocs navigation and the wiki map with correct Spanish accents.

### Task 5: Extend provenance and legal-time graph

**Files:**
- Modify: `sources/registry.yaml`
- Modify: `sources/instruments.yaml`
- Modify: `sources/page_metadata.yaml`
- Regenerate: `docs/catalog/registry.md`
- Regenerate: `docs/status/corpus-coverage.md`
- Regenerate: `reports/corpus-coverage.json`

**Interfaces:**
- Consumes: source IDs for SIDOF 5783669 (159 bis) and SIDOF 5786598 (Ventanilla Única), existing LIGIE/RGCE/LA sources.
- Produces: source IDs/instruments referenced by new pages and deterministic governance outputs.

- [x] **Step 1:** Register the 31-Mar-2026 lineamientos source with publication/effective dates and the appropriate legal instrument relationship.
- [x] **Step 2:** Register the 4-May-2026 Ventanilla Única decree with publication/effective dates and instrument relationship.
- [x] **Step 3:** Add page metadata for every new wiki page, using `reviewed/current` only where this change actually reviews the cited official sources through 15-Aug-2026.
- [x] **Step 4:** Update existing affected page metadata source lists where the new sources materially support the public explanation.
- [x] **Step 5:** Regenerate catalog and coverage outputs using the repository scripts; do not hand-edit generated semantics.

### Task 6: Verify and merge Wave 1

**Files:**
- Verify all modified/generated files.

**Interfaces:**
- Produces: one mergeable PR with no known regression.

- [x] **Step 1:** Run focused legal-depth tests.
- [x] **Step 2:** Run all repository tests.
- [x] **Step 3:** Run repository integrity, catalog drift, page metadata, coverage policy/drift, temporal graph and RAG evaluation.
- [x] **Step 4:** Run strict MkDocs build and legacy route verification.
- [ ] **Step 5:** Inspect the PR diff and review threads for accidental scope or unsupported legal promotions.
- [ ] **Step 6:** Merge only after fresh CI is green, then verify CI and Pages on the merge SHA.
