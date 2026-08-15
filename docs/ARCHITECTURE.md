---
title: "Architecture"
description: "Arquitectura del repositorio: fuentes, originales, corpus, wiki, grafo temporal, validadores y recuperación RAG."
---

# Architecture

The repository is a Mexico-first, provenance-first legal knowledge system. It is not SAT, ANAM, Secretaría de Economía, Cámara de Diputados, or DOF. Structured tariff rows remain in [`arancel-mx`](https://github.com/jccontrerasg08-cpu/arancel-mx).

## Responsibility boundaries

| Layer | Canonical location | Responsibility |
|---|---|---|
| Source registry | `sources/registry.yaml` | Stable official URLs, authority, evidence class, probe policy |
| Instrument graph | `sources/instruments.yaml` | Publication/effective dates, status, amendments, annexes, consolidation |
| Page sidecar | `sources/page_metadata.yaml` | Provenance and independent status dimensions for wiki/corpus content |
| Original evidence | `data/originals/` | Manifests and SHA-256; official binary bytes live in Releases |
| Derived corpus | `data/corpus/` | Retrieval-oriented digests, never the binding text |
| Wiki/site | `docs/` | Human explanations, catalog, methodology, and changes |
| Retrieval evaluation | `evals/questions.yaml` | Hand-checked source expectations at temporal cutoffs |

## Contracts and generation

JSON Schemas in `schemas/` close the accepted metadata vocabulary. Local validation uses Draft 2020-12 with explicit format checking and no remote schema retrieval. `scripts/build_catalog.py` generates `docs/catalog/registry.md`; drift fails CI. The page inventory requires one sidecar record for every governed wiki and corpus page.

## Temporal model

An instrument has one stable ID, a consolidated source, coverage status, effective range, and a sequence of source-backed events. Event records are cross-checked against the registry's instrument and publication date. Mutable consolidations also declare a content-validity interval. Queries select only manifestations valid at their cutoff. Publication, consolidation, extraction, legal review, corpus currency, and transport availability remain separate facts.

Cycles, unknown references, impossible date ranges, events later than `current_through`, duplicate IDs, and page metadata that trails a known event are rejected offline.

## Automation boundary

Pull-request CI is deterministic and network-free after dependency installation. It runs unit tests, composed validation, generated-file checks, temporal RAG evaluation, and MkDocs strict build. Pages repeats that complete deterministic gate before uploading a deployable artifact. CodeQL scans Python and GitHub Actions with a pinned action and restricted permissions.

Scheduled workflows perform bounded external probes, official SIDOF discovery, and link checks. Redirects are followed manually: HTTPS and the allowlist are checked before each next request, hop count, bytes, and time are capped, and bodies are never logged. Identity checks use the expected final path, title, or SIDOF note ID. Transport success cannot promote legal status. Suspect probes and new candidates create or update one deduplicated review issue.

## Retrieval baseline

The baseline is dependency-free lexical ranking over governed wiki/corpus text with Unicode normalization, manifestation-aware temporal filtering, forbidden-source assertions, abstention cases, and deterministic tie-breaking. Evaluation inspects the concrete retrieval result: ranked records, emitted source citations, and the emitted abstention disclaimer. Metrics include recall@k, mean reciprocal rank, temporal accuracy, and citation coverage. It proves infrastructure behavior, not substantive completeness or legal correctness.

Legacy wiki routes are generated with pinned `mkdocs-redirects` mappings so the move from `docs/wiki` to the integrated `docs` site does not break representative public URLs.

## Content and copyright limits

HS6 is the international ceiling. TIGIE eight-digit and NICO ten-digit classification are Mexico-specific. Do not scrape interactive INEGI/SNICE classifiers, reproduce ICC Incoterms rule text, vendor WCO explanatory notes, or commit official PDFs. Catalog-only references are a deliberate supported state.
