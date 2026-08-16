# RGCE 2026 Annex Review Implementation Plan

> Design: `docs/superpowers/specs/2026-08-15-rgce-2026-annex-review-design.md`

## Goal

Replace the 32 RGCE annex digests with conservative, reviewed summaries tied to a deterministic 1–30 annex manifest, correct the May 2026 temporal event, and make the reviewed digests safe for current retrieval while keeping extraction explicitly partial.

## Task 1 — RED: define the annex contract

Create `tests/test_rgce_annex_review.py` before production edits.

Tests must require:

- `sources/rgce_2026_annexes.yaml` exists;
- exactly 30 annex entries, numbered 1..30;
- unique official title and corpus path;
- publication source IDs match the official publication blocks;
- only 5, 22 and 29 include `mx_sidof_rgce_2026_mod1_anexos` as a published modification;
- Anexo 2 has no published modification entry;
- `mx_sidof_rgce_2026_mod1_anexos` has temporal event `2026-05-20`;
- all 30 individual digests and two composite digests have current source, partial extraction, reviewed legal status, current corpus, and `current_through: 2026-05-20`;
- every individual digest contains a source/currentness block and an explicit non-exhaustive disclosure;
- forbidden stale phrases do not appear.

Open a draft PR with the test-only RED state and confirm CI fails for missing manifest/status/content, not syntax.

## Task 2 — add the canonical editorial annex manifest

Create `sources/rgce_2026_annexes.yaml` with records for 1–30.

Each record:

- `annex`
- `title`
- `publication_source_id`
- `publication_date`
- `modification_source_ids`
- `reviewed_through`
- `corpus_path`

Official title list follows the SAT 2026 index. Publication mapping:

- A1 -> `mx_sidof_rgce_2026_anexo_1`
- A2 -> `mx_sidof_rgce_2026_anexo_2`
- A3–12/A14–20 -> `mx_sidof_rgce_2026_anexos_3_20`
- A13 -> `mx_sidof_rgce_2026`
- A21–30 -> `mx_sidof_rgce_2026_anexos_21_30`
- A5/A22/A29 additionally -> `mx_sidof_rgce_2026_mod1_anexos`

`reviewed_through` is `2026-05-20` for every record because the review explicitly checks the first modification’s scope and confirms whether the annex was affected.

## Task 3 — validator/helper

Create `scripts/rgce_annexes.py`.

Responsibilities:

- load/validate manifest shape without new dependencies;
- verify number coverage and uniqueness;
- verify source IDs exist in `sources/registry.yaml`;
- verify corpus paths exist;
- verify modification set is exactly {5, 22, 29};
- cross-check page metadata status and source IDs;
- emit deterministic findings;
- support `--check`.

Wire `python -m scripts.rgce_annexes --check` into CI and Pages before RAG evaluation.

No network calls in deterministic CI.

## Task 4 — correct temporal graph

Change `mx_sidof_rgce_2026_mod1_anexos` event from `2026-05-22` to `2026-05-20`.

Add a regression test that pins the date and documents that provision-specific effective rules, especially the Anexo 22 AL key, remain content-level nuance rather than being collapsed into a fake universal effective date.

## Task 5 — rewrite Anexos 1–10

Replace current digests with reviewed, bounded summaries.

Each file contains:

- official title;
- `Estado al 15-08-2026`;
- source publication date;
- what the annex covers;
- operational use;
- 2026 modification status;
- `Límites del digest`;
- source IDs / official references.

Special corrections:

- A1: remove nonexistent published/anticipated “1ra modification” claim from local digest unless it is actually present in SAT’s current anticipated section at the cutoff;
- A2: record that an anticipated future modification exists but is not DOF-published/current law;
- A5: describe 2026-05-20 first modification; do not call its prior anticipated versions a second modification;
- A6: use official title “Reglas de operación de clasificación arancelaria”, not an invented council title.

## Task 6 — rewrite Anexos 11–20

Use exact SAT official titles:

11. Rutas fiscales autorizadas para el tránsito internacional
12. Mercancías por las que procede exportación temporal
13. Multas y cantidades actualizadas de LA y RLA
14. Importación o exportación de hidrocarburos, petrolíferos, petroquímicos y azufre
15. Distancias y plazos máximos para tránsitos
16. Aduanas para tránsito de frontera norte a frontera sur y viceversa
17. Mercancías por las que no procede el tránsito internacional
18. Mercancías que no pueden ser objeto de depósito fiscal
19. Datos inexactos, falsos u omitidos para efectos del art. 184 fr. III LA
20. Mercancías sujetas a declaración de marcas nominativas o mixtas

Do not retain absolute decision trees that infer legal consequences beyond each annex.

## Task 7 — rewrite Anexos 21–30

Use exact SAT official titles and current publication state.

Special handling:

- A22: incorporate that a first modification was published 2026-05-20 and note the AL-key transitory nuance without trying to summarize every apéndice;
- A24/A30: preserve the legally cleaned Wave 3 substance but normalize source/currentness disclosure;
- A29: remove false “2da modification” language and absolute “can/cannot use regime” chatbot decisions that ignore exceptions; state the first modification was published 2026-05-20;
- A27/A28: do not reproduce large tariff lists; point to official source and structured tariff layer where useful.

## Task 8 — rewrite composite digests

`anexos-formatos-tramites.md`:
- map A1/A2 publication state;
- explain the anticipated A2 distinction;
- link individual digests.

`anexos-riesgo-logistica.md`:
- map annexes by operational question;
- no new legal obligations;
- link to individual digests.

## Task 9 — metadata promotion after content review

Update exactly the 32 RGCE-annex corpus records:

- `source_status: current`
- `extraction_status: partial`
- `legal_review_status: reviewed`
- `corpus_status: current`
- `current_through: 2026-05-20`

Preserve/increase source IDs; never remove a published modification from A5/A22/A29.

## Task 10 — RAG and coverage

Add representative evals for A1, A2, A5, A13, A22, A29 and A30.

Regenerate:

- `docs/status/corpus-coverage.md`
- `reports/corpus-coverage.json`
- `docs/catalog/registry.md` if temporal/source rendering changes.

Update `coverage-policy.yaml` only as a ratchet improvement: raise minimum reviewed/current metrics and lower maximum pending/non-current metrics to the newly verified baseline. Never relax a threshold.

## Task 11 — full verification and merge

Final gates:

1. full unit suite;
2. `scripts.validate_repository`;
3. `scripts.build_catalog --check`;
4. `scripts.page_metadata --check`;
5. `scripts.rgce_annexes --check`;
6. `scripts.coverage_report --check`;
7. `scripts.temporal_graph --check`;
8. `scripts.rag_eval --check`;
9. `mkdocs build --strict`;
10. `scripts.verify_site site`;
11. Dependency Review;
12. fresh PR CI on exact head;
13. squash merge with expected SHA;
14. main CI and Pages green on merge SHA.

## Task 12 — handoff to PR B

After merge, create a fresh branch from main for:

- other corpus digests;
- 19 wiki pages;
- source/instrument refs for authored/synthetic material;
- selected non-overlapping fixes salvaged from closed PR #35.

Do not carry PR A’s temporary migration scaffolding into main.
