# Governance

## Authority and roles

The repository owner has final authority over scope, releases, legal-status transitions, and maintainer appointments. Maintainers review provenance, temporal effects, copyright boundaries, tests, and operational safety. Automation may report evidence but may not decide legal status.

## Source hierarchy

1. DOF or SIDOF publication event.
2. Consolidated text from Cámara de Diputados.
3. SAT, ANAM, Secretaría de Economía, SNICE, VUCEM, or another competent authority.
4. Treaty secretariat or intergovernmental official source.
5. Project-authored explanation.
6. Secondary material, used only to locate or contextualize primary sources.

Conflicts are resolved in favor of the legally competent publication and the applicable date. A consolidated text is useful but does not erase the publication trail.

## Status transitions

`candidate` to `pending_review` to `current` requires a person to verify title, authority, publication, effective provisions, transitory rules, affected instruments, and source references. `current` may become `stale`, `superseded`, `withdrawn`, or `unknown` when evidence changes. Transport failures do not trigger those transitions automatically.

## Corrections

Material errors receive a focused correction commit that names the affected source and date, updates temporal/page metadata, adds a regression test when behavior changed, regenerates derived documentation, and explains whether prior answers or releases were affected. Do not rewrite Git history to hide a published legal-knowledge error.

## Releases and evidence

GitHub Releases may carry official original bytes when redistribution and project policy allow it. Git stores only manifests, hashes, metadata, code, and project-authored text. A release must remain reproducible from its manifest and checksum index.
