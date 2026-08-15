---
title: "Status model"
description: "Modelo de estados independiente para fuente, extracción, revisión legal, corpus y salud de transporte."
---

# Status model

This project never treats one green HTTP check as proof that legal content is current. Five independent dimensions prevent that shortcut.

| Dimension | Question | Typical values |
|---|---|---|
| Source status | Is the official source known and applicable? | `current`, `superseded`, `partial`, `unknown` |
| Extraction status | How much was transformed into project content? | `complete`, `partial`, `not_applicable` |
| Legal review | Has a person checked publication, effects, and dates? | `reviewed`, `pending_review` |
| Corpus status | May retrieval present this digest as current? | `current`, `stale`, `partial`, `superseded` |
| Transport health | Did a bounded probe receive plausible content? | `healthy`, `suspicious_response`, `unreachable` |

## Rules

- DOF or SIDOF establishes publication. A consolidated Cámara de Diputados text is useful for reading the incorporated law, but it does not replace the publication event.
- `current_through` is the latest effective event explicitly reviewed into a page. It is not the date on which a URL was fetched.
- `content_valid_from` delimits the observed manifestation behind a mutable consolidated URL. It prevents a PDF marked "vigente" today from being silently used as if it were the text available decades ago.
- `partial` is a positive disclosure: the source family is useful, but one or more amendments, annexes, extraction sections, or review steps remain incomplete.
- `stale` content remains available for historical or diagnostic retrieval but must not be cited as the current answer.
- Project-authored explainers are `non_authoritative` even when every citation is official.

## Examples

A consolidated Ley Aduanera PDF may be available and current while the local digest is `stale`, because the digest has not been fully rebuilt after a reform. Conversely, RGCE 2025 is intentionally `superseded` but remains indexed for questions whose cutoff falls in 2025.

No automated network workflow may promote a record to `current`. That transition requires review of the instrument, publication date, effective provisions, transitory articles, and affected annexes.

When a historical cutoff has no versioned manifestation, retrieval must abstain and disclose the gap. A current consolidated URL is not backdated to the instrument's original effective date.
