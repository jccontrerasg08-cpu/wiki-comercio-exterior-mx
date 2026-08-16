# Docs Discovery, Offline, and Retrieval Hardening Design

## Purpose

Improve discovery, offline distribution, repository review ergonomics, and local evidence retrieval without changing legal semantics, source ownership, or the RGCE annex review currently isolated in PR #36.

## Constraints

- `sources/`, page metadata, instrument metadata, and official URLs remain the source of truth.
- No LLM decides legal currentness. Local retrieval consumes only the same reviewed/current gates already enforced by `scripts.rag_eval`.
- The normal GitHub Pages profile keeps fast web navigation. A separate profile provides true `file://` offline compatibility.
- No external fonts, images, JavaScript, analytics, or runtime CDN dependencies are introduced.
- Structured tariff rows remain in `arancel-mx`.
- The open RGCE annex PR is not modified or rebased by this work.

## Architecture

### Web discovery

Enable Material's built-in `meta` and `tags` plugins with a small controlled hierarchical vocabulary inherited through `.meta.yml` files. Add a topic index, footnote tooltips, and instant previews for the web profile. The existing left navigation remains the primary hierarchy, while tags provide a cross-cutting discovery layer.

### Offline profile

Add `mkdocs.offline.yml` inheriting from `mkdocs.yml`. It enables Material's built-in `offline` plugin, removes the repository link, and explicitly replaces fetch-dependent Instant Navigation features. CI builds and validates both web and offline artifacts.

### Knowledge map

Generate `docs/explore/knowledge-map.md` and a machine-readable `docs/assets/data/knowledge-index.json` from canonical page metadata, source registry, and instrument metadata. The generated map exposes relationships and review/currentness metadata, but labels them as repository metadata rather than legal conclusions.

### Local retrieval

Add `scripts.query_knowledge`, a deterministic CLI on top of the existing lexical and temporal retrieval primitives. It requires an explicit cutoff date, returns official source IDs/URLs and temporal intervals, and supports JSON output for future LLM use. An LLM can explain returned evidence later, but cannot bypass the governed retrieval layer.

### Repository hardening

Reapply the useful SNICE FancyIndex parser fix from superseded PR #35 with a regression test. Update contributor guidance with modern GitHub review techniques from `github-cheat-sheet`, while excluding obsolete Travis/Jekyll/hub-era recommendations.

## Error handling and safety

- Offline verification fails on remote runtime assets and missing offline search artifacts.
- Generated knowledge-map checks fail when committed output drifts from canonical metadata.
- Query CLI abstains when no evidence clears lexical and temporal eligibility.
- SNICE parsing skips anchors without an adjacent valid date/time/size tuple and preserves filename parse failures as unparsed entries.
- CI remains deterministic and network-free after dependency installation.

## Testing

Use TDD. First commit tests that fail on current `main`, including a table-style SNICE index fixture and platform invariants. Then implement the smallest changes needed to make them pass. Final verification runs full unit discovery, repository integrity, generated catalog/page/coverage/temporal/RAG checks, knowledge-map check, strict web build, site verification, strict offline build, and offline verification.

## Out of scope

Updating the GitHub `main-protection` ruleset is an administrative repository setting, not a file change. If the connector cannot mutate rulesets, the implementation will document the exact remaining setting: require the unique `repository-ci` status check before merge.
