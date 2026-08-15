# Wiki Editorial, SEO and Quality Wave 2 Implementation Plan

**Goal:** Turn the legal-writing pattern approved in Wave 1 into a repository-wide editorial contract, improve discoverability and accessibility, and simplify the public wiki index without weakening legal provenance.

**Architecture:** Keep legal truth in source/instrument metadata and official publications; keep the public wiki concise and reader-oriented. Add deterministic editorial tests around front matter, descriptions, page structure, dangerous absolutes and public navigation. Do not change legal review status merely because a page receives SEO or copy edits.

## Task 1: Editorial policy and review governance

- [ ] Create `docs/methodology/editorial-policy.md` with the default pattern: regla general → cuándo aplica → condiciones/excepciones → cómo verificar → fuentes → vigencia → ver también.
- [ ] Define useful length ranges by page intent, not keyword stuffing.
- [ ] Define language rules for absolutes such as `siempre`, `nunca`, `automáticamente`, `sin X no procede`, and require explicit source/context when they are truly warranted.
- [ ] Create `docs/methodology/citation-policy.md` defining primary-source priority, event-vs-consolidated-text handling, source dates, ICC/WTO scope and non-authoritative project explainers.
- [ ] Create `docs/methodology/page-review-checklist.md` defining the evidence required before `pending_review -> reviewed`.
- [ ] Create `docs/methodology/accessibility.md` with WCAG 2.2 AA target and automated/manual verification responsibilities.
- [ ] Create `docs/about/scope.md` clarifying boundaries among this wiki, `arancel-mx`, official sources and downstream product layers.

## Task 2: Reader-first information architecture

- [ ] Refactor `docs/wiki/index.md` to roughly 350–650 reader-facing words.
- [ ] Move coverage/gaps/course-style matrices to `docs/status/content-roadmap.md`.
- [ ] Link the roadmap without mixing repository internals into the primary learning path.
- [ ] Keep the operational route and direct entries for Aduana, Clasificación, RRNA, Contribuciones, Programas/Tratados and Logística.
- [ ] Add the new policy/scope/roadmap pages to MkDocs navigation with correct Spanish accents.

## Task 3: Unique page descriptions and SEO hygiene

- [ ] Add meaningful unique `description:` front matter to all public `docs/wiki/**/*.md` pages.
- [ ] Add descriptions to public catalog, methodology, changes, glossary, status and other navigable docs that currently inherit the generic site description.
- [ ] Preserve canonical URLs and sitemap generation.
- [ ] Do not add a project-subpath `robots.txt`; GitHub Pages path hosting means such a file would not act as host-root robots policy.
- [ ] Keep country source cards visible only when they provide actual source/navigation value; improve placeholder descriptions rather than presenting them as legal guidance.

## Task 4: Automated editorial/accessibility regression contract

- [ ] Create `tests/test_editorial_quality.py` before implementing the production edits and confirm RED.
- [ ] Require unique descriptions for substantive public wiki pages.
- [ ] Require `## Fuentes` and `## Ver también` for substantive wiki explainers, allowing explicit index/landing-page exceptions.
- [ ] Reject the exact high-risk absolute phrases already identified by the audit unless intentionally allowlisted.
- [ ] Enforce the reader-first word-count target for `docs/wiki/index.md`.
- [ ] Verify built HTML has `lang=es`, canonical URLs, unique titles, no missing image alt attributes and no broken local fragment links using deterministic static checks.
- [ ] Add an editorial-quality command to CI/Pages through the normal unit-test suite rather than a network-dependent gate.

## Task 5: Repository and supply-chain best practices

- [ ] Add a GitHub Dependency Review workflow using the current official GitHub action, SHA-pinned, after verifying current documentation/version.
- [ ] Keep external link checking scheduled and separate from deterministic PR CI.
- [ ] Evaluate the branch ruleset and require the stable `repository-ci` status check if the connector/API supports it safely without blocking Pages deployment.
- [ ] Preserve existing CodeQL and pull-request conversation-resolution protections.

## Task 6: Verification and merge

- [ ] Confirm RED for the new editorial regression tests.
- [ ] Run all tests, repository integrity, catalog, page metadata, coverage, temporal graph and RAG eval.
- [ ] Run MkDocs strict and legacy route verification.
- [ ] Inspect PR scope and review threads.
- [ ] Merge only after fresh CI is green.
- [ ] Verify `main` CI and Pages on the merge SHA before starting Wave 3.
