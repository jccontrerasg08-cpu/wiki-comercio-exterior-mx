# Docs Discovery, Offline, and Retrieval Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add governed topic discovery, a real offline build profile, a static legal-knowledge map, a deterministic local retrieval CLI, and the missing SNICE FancyIndex parser fix without changing legal semantics.

**Architecture:** Keep canonical legal/source metadata unchanged and derive all new discovery outputs from it. The normal MkDocs profile remains optimized for GitHub Pages, while an inherited offline profile disables fetch-dependent features and is independently verified. Local retrieval reuses the existing temporal/lexical gating and exposes source-backed results for optional downstream LLM use.

**Tech Stack:** Python 3.12, unittest, MkDocs 1.6.1, Material for MkDocs 9.7.7, PyYAML, GitHub Actions.

## Global Constraints

- Do not modify the RGCE annex corpus or PR #36 work surface.
- Do not introduce external runtime assets, analytics, or CDN dependencies.
- Do not let automated source health or an LLM promote legal currentness.
- Keep structured tariff rows outside this repository.
- Preserve existing redirects and GitHub Pages URLs.
- All generated outputs must be deterministic and checkable in CI.

---

### Task 1: Lock the missing behaviors with failing tests

**Files:**
- Modify: `tests/test_snice_intelligence.py`
- Create: `tests/test_platform_hardening.py`

**Interfaces:**
- Consumes: current `mkdocs.yml`, CI workflow, contributor docs, and existing SNICE parser.
- Produces: regression/invariant tests for later tasks.

- [ ] **Step 1: Add a FancyIndex table regression**

Add a test in `SniceIndexTests` with the filename anchor in one table cell and date/time/size in following cells. Assert one document is parsed with the expected byte count.

- [ ] **Step 2: Add platform hardening invariants**

Assert the future configuration contains built-in `meta` and hierarchical controlled `tags`, footnote tooltips, web instant preview, an offline profile without `navigation.instant*`, CI offline/knowledge-map gates, generated knowledge-map output, local retrieval CLI behavior, and GitHub Markdown-review guidance.

- [ ] **Step 3: Run the focused suite on the PR branch**

Run through GitHub Actions after opening the draft PR. Expected: RED because these capabilities are absent from current `main`.

### Task 2: Make SNICE FancyIndex parsing resilient

**Files:**
- Modify: `scripts/snice_intelligence.py`
- Test: `tests/test_snice_intelligence.py`

**Interfaces:**
- Consumes: raw Apache/FancyIndex HTML, `base_url`, `discovered_at`.
- Produces: unchanged `SniceIndexSnapshot` / `SniceDocument` public API.

- [ ] **Step 1: Replace the monolithic row regex**

Use an anchor regex to discover file hrefs, strip nearby tags, and then parse an adjacent `DD-Mon-YYYY HH:MM SIZE` tuple. Preserve filtering of query/root links and unparsed filename behavior.

- [ ] **Step 2: Verify plain and table-style index fixtures**

Run `python -m unittest tests.test_snice_intelligence -v`. Expected: all SNICE tests pass.

### Task 3: Add governed Material discovery features

**Files:**
- Modify: `mkdocs.yml`
- Create: `docs/topics.md`
- Create: `docs/wiki/fundamentos/.meta.yml`
- Create: `docs/wiki/aduana/.meta.yml`
- Create: `docs/wiki/clasificacion/.meta.yml`
- Create: `docs/wiki/rrna/.meta.yml`
- Create: `docs/wiki/contribuciones/.meta.yml`
- Create: `docs/wiki/programas/.meta.yml`
- Create: `docs/wiki/logistica/.meta.yml`
- Create: `docs/catalog/.meta.yml`
- Create: `docs/methodology/.meta.yml`
- Create: `docs/status/.meta.yml`
- Test: `tests/test_platform_hardening.py`

**Interfaces:**
- Consumes: page paths and folder taxonomy.
- Produces: controlled tags and a topic listing with no legal-state inference.

- [ ] **Step 1: Convert plugins/extensions to inheritance-safe mapping syntax**

Configure `search`, `meta`, `tags`, and `redirects` as mappings. Enable `tags_hierarchy: true` and only these tags: `Tema/Fundamentos`, `Tema/Aduana`, `Tema/Clasificación`, `Tema/RRNA`, `Tema/Contribuciones`, `Tema/Programas`, `Tema/Logística`, `Tipo/Fuente`, `Tipo/Metodología`, `Tipo/Estado`.

- [ ] **Step 2: Enable modern web-only UX**

Add `content.footnote.tooltips`, `navigation.instant.preview`, and the `footnotes` Markdown extension. Keep current navigation/search features.

- [ ] **Step 3: Add inherited folder tags and topic listing**

Each `.meta.yml` contains one controlled tag. `docs/topics.md` contains front matter, a short explanation, and `<!-- material/tags -->`.

- [ ] **Step 4: Add `Explorar` navigation**

Expose `Temas` and the generated knowledge map under one top-level `Explorar` group.

### Task 4: Build and verify a real offline profile

**Files:**
- Create: `mkdocs.offline.yml`
- Create: `scripts/verify_offline_site.py`
- Modify: `.github/workflows/ci.yml`
- Modify: `README.md`
- Modify: `docs/methodology/docs-engine-compatibility.md`
- Test: `tests/test_platform_hardening.py`

**Interfaces:**
- Consumes: inherited MkDocs configuration and built `site-offline` directory.
- Produces: `verify_offline_site(site_dir: Path) -> list[str]` and CLI exit status.

- [ ] **Step 1: Define the inherited offline config**

Set `INHERIT: mkdocs.yml`, `repo_url: null`, enable the built-in `offline` plugin, and replace `theme.features` with the non-fetch subset. Explicitly omit `navigation.instant`, `navigation.instant.prefetch`, `navigation.instant.progress`, and `navigation.instant.preview`.

- [ ] **Step 2: Implement deterministic offline validation**

Parse built HTML and report remote `script src`, `link href`, or `img src` runtime assets. Require Material's generated offline search JavaScript artifact to exist. Return a non-zero CLI status when findings exist.

- [ ] **Step 3: Add CI gates**

After the web build/site verification, run `python -m mkdocs build --strict -f mkdocs.offline.yml -d site-offline` and `python -m scripts.verify_offline_site site-offline`.

- [ ] **Step 4: Document both profiles**

Add reproducible web/offline commands to README and explain why Instant Navigation is intentionally disabled for `file://` builds in docs-engine compatibility.

### Task 5: Generate a static knowledge map

**Files:**
- Create: `scripts/build_knowledge_map.py`
- Create: `docs/explore/knowledge-map.md`
- Create: `docs/assets/data/knowledge-index.json`
- Modify: `.github/workflows/ci.yml`
- Test: `tests/test_platform_hardening.py`

**Interfaces:**
- Consumes: `sources/page_metadata.yaml`, `sources/registry.yaml`, `sources/instruments.yaml`.
- Produces: `render_knowledge_map(root: Path) -> str`, `build_index(root: Path) -> list[dict[str, object]]`, deterministic Markdown/JSON, `--check` CLI.

- [ ] **Step 1: Build normalized wiki records**

Include governed wiki explainers only. Record path, title, topic, review/source status, current-through date, instrument IDs, and source IDs/official URLs. Sort by topic/title/path.

- [ ] **Step 2: Render human and machine views**

Render a topic-grouped Markdown table and stable JSON (`ensure_ascii=False`, sorted keys, two-space indent, trailing newline). State that metadata is repository review state, not an independent legal opinion.

- [ ] **Step 3: Add deterministic check mode and CI gate**

`python -m scripts.build_knowledge_map --check` compares committed files byte-for-byte and exits 1 on drift. Run it in CI before MkDocs builds.

### Task 6: Add deterministic local retrieval CLI

**Files:**
- Create: `scripts/query_knowledge.py`
- Modify: `README.md`
- Test: `tests/test_platform_hardening.py`

**Interfaces:**
- Consumes: `scripts.rag_eval.documents_from_repository`, `rank_documents`, source registry, explicit cutoff date.
- Produces: `KnowledgeHit`, `search_repository(root: Path, query: str, cutoff: date, k: int = 5) -> tuple[KnowledgeHit, ...]`, text/JSON CLI.

- [ ] **Step 1: Reuse governed retrieval**

Do not implement a second ranking/currentness system. Map ranked source IDs back to official registry URLs and return stable hit records.

- [ ] **Step 2: Require an explicit cutoff**

CLI syntax: `python -m scripts.query_knowledge "IMMEX Anexo 24" --cutoff 2026-08-15 [--k 5] [--json]`. No implicit today/current-law assumption.

- [ ] **Step 3: Abstain when empty**

If no sources rank, print a concise human-review message; JSON mode returns `[]`.

### Task 7: Modernize GitHub review ergonomics and verification docs

**Files:**
- Modify: `CONTRIBUTING.md`
- Modify: `.github/PULL_REQUEST_TEMPLATE.md`

**Interfaces:**
- Produces: contributor/reviewer workflow guidance only.

- [ ] **Step 1: Add Markdown review practices**

Document rendered-prose diff for Markdown, relative repo links, permanent commit links for exact evidence, scoped PR file/commit views, and task-list use. Do not add obsolete Travis/Jekyll/hub instructions.

- [ ] **Step 2: Expand verification commands/checklist**

Include corpus coverage, knowledge-map check, `scripts.verify_site`, strict offline build, and offline verifier.

### Task 8: Full integrated verification

**Files:** none expected.

- [ ] **Step 1: Run full unit discovery**

`python -m unittest discover -s tests -v`

- [ ] **Step 2: Run deterministic repository checks**

`python -m scripts.validate_repository`
`python -m scripts.build_catalog --check`
`python -m scripts.page_metadata --check`
`python -m scripts.coverage_report --check`
`python -m scripts.temporal_graph --check`
`python -m scripts.rag_eval --check`
`python -m scripts.build_knowledge_map --check`

- [ ] **Step 3: Build/verify web and offline sites**

`python -m mkdocs build --strict`
`python -m scripts.verify_site site`
`python -m mkdocs build --strict -f mkdocs.offline.yml -d site-offline`
`python -m scripts.verify_offline_site site-offline`

- [ ] **Step 4: Inspect final diff and PR checks**

Confirm no RGCE annex corpus files changed, no external runtime assets were added, and all required GitHub Actions jobs are green.
