# Wiki Editorial, SEO and Quality Wave 2 Implementation Plan

**Goal:** Turn the legal-writing pattern approved in Wave 1 into a repository-wide editorial contract, improve discoverability and accessibility, and simplify the public wiki index without weakening legal provenance.

**Architecture:** Keep legal truth in source/instrument metadata and official publications; keep the public wiki concise and reader-oriented. Add deterministic editorial tests around front matter, descriptions, page structure, dangerous absolutes and public navigation. Do not change legal review status merely because a page receives SEO or copy edits.

## Task 1: Editorial policy and review governance

- [x] Create `docs/methodology/editorial-policy.md` with the default pattern: regla general → cuándo aplica → condiciones/excepciones → cómo verificar → fuentes → vigencia → ver también.
- [x] Define useful length ranges by page intent, not keyword stuffing.
- [x] Define language rules for absolutes such as `siempre`, `nunca`, `automáticamente`, `sin X no procede`, and require explicit source/context when they are truly warranted.
- [x] Create `docs/methodology/citation-policy.md` defining primary-source priority, event-vs-consolidated-text handling, source dates, ICC/WTO scope and non-authoritative project explainers.
- [x] Create `docs/methodology/page-review-checklist.md` defining the evidence required before `pending_review -> reviewed`.
- [x] Create `docs/methodology/accessibility.md` with WCAG 2.2 AA target and automated/manual verification responsibilities.
- [x] Create `docs/about/scope.md` clarifying boundaries among this wiki, `arancel-mx`, official sources and downstream product layers.

## Task 2: Reader-first information architecture

- [x] Refactor `docs/wiki/index.md` to roughly 350–650 reader-facing words.
- [x] Move coverage/gaps/course-style matrices to `docs/status/content-roadmap.md`.
- [x] Link the roadmap without mixing repository internals into the primary learning path.
- [x] Keep the operational route and direct entries for Aduana, Clasificación, RRNA, Contribuciones, Programas/Tratados and Logística.
- [x] Add the new policy/scope/roadmap pages to MkDocs navigation with correct Spanish accents.

## Task 3: Unique page descriptions and SEO hygiene

- [x] Add meaningful unique `description:` front matter to all public `docs/wiki/**/*.md` pages.
- [x] Add descriptions to public catalog, methodology, changes, glossary, status and other navigable docs that currently inherit the generic site description.
- [x] Preserve canonical URLs and sitemap generation.
- [x] Do not add a project-subpath `robots.txt`; GitHub Pages path hosting means such a file would not act as host-root robots policy.
- [x] Keep country source cards visible only when they provide actual source/navigation value; improve placeholder descriptions rather than presenting them as legal guidance.

## Task 4: Automated editorial/accessibility regression contract

- [x] Create `tests/test_editorial_quality.py` before implementing the production edits and confirm RED.
- [x] Require unique descriptions for substantive public wiki pages.
- [x] Require `## Fuentes` and `## Ver también` for substantive wiki explainers, allowing explicit index/landing-page exceptions.
- [x] Reject the exact high-risk absolute phrases already identified by the audit unless intentionally allowlisted.
- [x] Enforce the reader-first word-count target for `docs/wiki/index.md`.
- [x] Verify built HTML has `lang=es`, canonical URLs, unique titles, no missing image alt attributes and no broken local fragment links using deterministic static checks. Generated redirect pages and `404.html` are treated according to their non-indexable semantics.
- [x] Add an editorial-quality command to CI/Pages through the normal unit-test suite rather than a network-dependent gate.

## Task 5: Repository and supply-chain best practices

- [x] Add a GitHub Dependency Review workflow using the current official GitHub action, SHA-pinned, after verifying current documentation/version. `actions/dependency-review-action` v5.0.0 is pinned to `a1d282b36b6f3519aa1f3fc636f609c47dddb294`; the workflow passed on PR #33.
- [x] Keep external link checking scheduled and separate from deterministic PR CI.
- [x] Evaluate the branch ruleset and require the stable `repository-ci` status check if the connector/API supports it safely without blocking Pages deployment. The active `main-protection` ruleset already requires PRs, resolved review conversations and CodeQL; it does not yet require a status check, and the available GitHub connector exposes no safe ruleset write mutation, so no administrative protection was changed from this implementation session.
- [x] Preserve existing CodeQL and pull-request conversation-resolution protections.

## Task 6: Verification and merge

- [x] Confirm RED for the new editorial regression tests.
- [x] Run all tests, repository integrity, catalog, page metadata, coverage, temporal graph and RAG eval.
- [x] Run MkDocs strict and legacy route verification.
- [x] Inspect PR scope and review threads. The final pre-merge scope contains only editorial/methodology documentation, navigation/frontmatter/link improvements, static site verification/tests and the pinned Dependency Review workflow; no unresolved review threads are present.
- [ ] Merge only after fresh CI is green.
- [ ] Verify `main` CI and Pages on the merge SHA before starting Wave 3.

## Verification evidence

The clean migrated workspace was verified on GitHub Actions run `31914613648` before its final commit. It completed **117 unit tests** plus repository integrity, generated catalog, page metadata, coverage policy, temporal graph, RAG evaluation, MkDocs strict build, legacy-route compatibility and static SEO/accessibility checks. RAG metrics were `1.0` for citation coverage, MRR, recall@k and temporal accuracy. Coverage remained at 75 governed pages, 15 reviewed, 15 retrieval-eligible, 69 sourced and 66 instrumented; editorial/SEO edits did not promote legal review status.

The migration-only workflow and script were deleted from the committed branch state. On commit `5e50cc667b8bbdccb52356701430b00a1c0c412a`, both the normal `ci` workflow and the new `Dependency Review` workflow completed successfully. A final fresh run on the checklist-closing head is still required before merge.
