# Map Interoperability Implementation Plan

> **For agentic workers:** use the approved explorer/originals/map design. Keep `aduanamap-mx` canonical for geospatial data and the wiki resilient when map assets are unavailable.

**Goal:** Add a lightweight map entry point and a stable cross-repository data contract without copying canonical GeoJSON into the wiki.

**Architecture:** The wiki stores only a versioned contract/manifest that identifies the canonical AduanaMap dataset, its producer path, schema expectations and preferred immutable consumption route. The wiki exposes human-facing map guidance and contextual links; AduanaMap remains responsible for full MapLibre rendering, layer management and advanced geographic analysis.

**Tech Stack:** YAML/JSON metadata contract, MkDocs Material, lightweight JavaScript only when static embedding is safe, existing AduanaMap GeoJSON/MapLibre pipeline.

## Constraints

- Do not commit a second manually maintained `countries-50m.geojson` to the wiki.
- Do not add Google Maps, Mapbox or another paid/commercial API as a truth dependency.
- Essential legal/documentary wiki content must work with maps unavailable.
- Canonical world geometry remains `aduanamap-mx/data/geojson/countries-50m.geojson`.
- Cross-repo references must be immutable or checksum-verifiable before they are treated as reproducible build inputs.
- Contextual maps in the wiki are filtered views, not a competing AduanaMap product.

### Task 1: Define and validate the cross-repo geodata contract

**Files:**
- Create: `data/contracts/aduanamap.yaml`
- Create: `scripts/validate_data_contracts.py`
- Create: `tests/test_data_contracts.py`

- [ ] Record canonical repository, dataset path, generator path, schema fields, SRID, geometry type, fallback behavior and consumption policy.
- [ ] Record the current known producer commit/tag only when verified from GitHub; prefer immutable refs over moving `main` for reproducible builds.
- [ ] Validate required IDs/URLs/paths and reject a local wiki GeoJSON path for a dataset marked `canonical_repository: aduanamap-mx`.
- [ ] Add checksum/release fields once AduanaMap publishes a stable artifact; do not invent them.

### Task 2: Add the wiki map explorer page

**Files:**
- Create: `docs/explore/mapa.md`
- Modify: `docs/explore/index.md`
- Modify: `mkdocs.yml`
- Extend: `tests/test_explorer_content.py`

- [ ] Explain available/current layers and planned context layers without claiming nonexistent datasets.
- [ ] Link to AduanaMap advanced map and source repository.
- [ ] Explain that the wiki consumes canonical geodata and degrades to textual/legal navigation when map data is unavailable.
- [ ] Add contextual links to customs/transit/Annex 21/treated-country pages where available.

### Task 3: Provide a lightweight embed contract, not a duplicated application

**Files:**
- Create if supported by current site patterns: `docs/assets/javascripts/context-map.js`
- Modify if needed: `mkdocs.yml`
- Create/extend: `tests/test_map_integration.py`

- [ ] Implement only after the contract has an immutable or checksum-verifiable public artifact.
- [ ] Accept dataset URL + layer/filter configuration declaratively.
- [ ] Render a clear fallback link/text if MapLibre or data loading fails.
- [ ] Never block page content or legal navigation on map initialization.
- [ ] Do not ship duplicate country geometry in wiki assets.

### Task 4: Document shared entity identifiers

**Files:**
- Create: `docs/methodology/cross-repo-contracts.md`
- Modify: `docs/explore/mapa.md`
- Modify: `docs/explore/aranceles.md`
- Create/extend: `tests/test_data_contracts.py`

- [ ] Define stable cross-repo identifiers for countries (ISO2/ISO3), tariff codes, source IDs and legal instrument IDs.
- [ ] State which repository is canonical per identifier/data domain.
- [ ] Document how consumers detect incompatible versions and how fallbacks work.

### Task 5: Full verification

- [ ] Run data-contract tests and full unit suite.
- [ ] Run repository validation and generated-doc drift checks.
- [ ] Run `mkdocs build --strict`.
- [ ] Confirm no new `*.geojson` is added to the wiki unless explicitly generated/cache-only and excluded from canonical ownership.
- [ ] Confirm no map dependency changes legal-currentness or retrieval eligibility.

## Acceptance

1. The wiki exposes a discoverable map explorer.
2. AduanaMap remains the sole canonical geospatial source/app.
3. The wiki records a machine-readable, validated consumption contract.
4. No manual duplicate of the world GeoJSON exists in the wiki.
5. Map failure leaves the legal/documentary experience functional.
6. Shared entity identifiers and version boundaries are documented.
