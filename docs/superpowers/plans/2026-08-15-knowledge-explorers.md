# Knowledge Explorers Implementation Plan

> **For agentic workers:** use the existing approved design in `docs/superpowers/specs/2026-08-15-explorers-originals-map-integration-design.md`. Implement with focused tests and keep existing public URLs stable.

**Goal:** Add a first-class `Explorar` experience that lets users enter the corpus by operation or legal domain without duplicating the underlying wiki pages or canonical structured datasets.

**Architecture:** Build a lightweight static explorer hub on top of the existing MkDocs Material site. Reuse existing pages, `sources/registry.yaml`, `sources/instruments.yaml`, `sources/page_metadata.yaml`, generated catalogs and cross-repo canonical links. Do not introduce a parallel SPA.

**Tech Stack:** MkDocs Material, Markdown, existing CSS/JS components, Python/YAML tests.

## Constraints

- Existing wiki URLs remain stable.
- The explorer is navigation/relationship UX, not a second content corpus.
- `arancel-mx` remains canonical for structured tariff data.
- `aduanamap-mx` remains canonical for geospatial datasets and advanced map UX.
- Legal-currentness badges/claims continue to come from the existing review/currentness model.
- Every explorer must expose official-source provenance rather than hiding it behind prose.

### Task 1: Add the explorer hub and navigation

**Files:**
- Create: `docs/explore/index.md`
- Modify: `mkdocs.yml`
- Modify: `tests/test_mkdocs_ux.py`

- [ ] Add failing tests requiring top-level `Explorar`, `catalog/library.md`, and all eight approved explorer entry labels.
- [ ] Add `docs/explore/index.md` using MkDocs Material cards/grid with: Aranceles, Marco jurídico, RGCE y anexos, Tratados y origen, Programas, RRNA y NOM, Aduanas y mapa, Fuentes oficiales.
- [ ] Link cards to existing canonical pages/catalogs first; avoid placeholder dead routes.
- [ ] Add visible source-library navigation under `Fuentes`.
- [ ] Verify `python -m unittest tests.test_mkdocs_ux -v` and `mkdocs build --strict` in CI.

### Task 2: Add relationship-driven legal and RGCE entry pages

**Files:**
- Create: `docs/explore/marco-juridico.md`
- Create: `docs/explore/rgce.md`
- Modify: `mkdocs.yml`
- Create: `tests/test_explorer_content.py`

- [ ] Test that legal explorer links Ley Aduanera, Reglamento, LIGIE, LCE, RGCE, instruments/catalog and official originals.
- [ ] Test that RGCE explorer exposes 2026 rules, annexes, modifications, provenance and the distinction between publication events and preserved equivalent originals.
- [ ] Use existing wiki/corpus/catalog URLs; do not copy rule text into the explorer.
- [ ] Include explicit links to `docs/catalog/library.md` and temporal/currentness methodology.

### Task 3: Add operational explorer entry pages

**Files:**
- Create: `docs/explore/tratados-origen.md`
- Create: `docs/explore/programas.md`
- Create: `docs/explore/rrna-nom.md`
- Create: `docs/explore/aranceles.md`
- Modify: `mkdocs.yml`
- Extend: `tests/test_explorer_content.py`

- [ ] Aranceles: explain HS -> capítulo -> partida -> subpartida -> fracción MX -> NICO and route structured queries to `arancel-mx`; link local legal LIGIE/TIGIE pages.
- [ ] Tratados: expose list/map path, T-MEC and existing treaty pages/source catalog; preserve rule-of-origin nuance.
- [ ] Programas: route IMMEX, PROSEC, Drawback and related annexes/trámites.
- [ ] RRNA/NOM: route to existing RRNA/NOM pages and source guidance; explicitly avoid inferring applicability from NICO alone.
- [ ] No new legal-currentness assertions without reviewed metadata.

### Task 4: Add source-driven discoverability and quality checks

**Files:**
- Modify: `docs/explore/index.md`
- Modify: `docs/catalog/index.md`
- Extend: `tests/test_explorer_content.py`
- Modify if useful: `llms.txt`

- [ ] Ensure each explorer has a route back to official sources/originals.
- [ ] Ensure cross-repo links clearly identify canonical responsibilities.
- [ ] Test all new relative Markdown targets exist.
- [ ] Ensure the explorer hub is represented in machine-readable navigation (`llms.txt`) if the existing generation/model supports manual curated entries.
- [ ] Run full unit suite, repository validator, generated-doc checks and strict MkDocs build.

## Acceptance

1. `Explorar` is top-level and immediately visible.
2. All eight approved domains are reachable without deep menu hunting.
3. No structured tariff data or GeoJSON is manually duplicated.
4. Existing pages remain the source of substantive content.
5. Every route leads back to official provenance/originals.
6. Strict build and full test suite remain green.
