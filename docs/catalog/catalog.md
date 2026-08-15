# Source catalog guide

The canonical records live in `sources/registry.yaml`; the temporal instrument model lives in `sources/instruments.yaml`. The complete Markdown registry is generated from both files and must not be edited by hand.

## How to read a record

- **Evidence** distinguishes publication events, consolidated official texts, operational portals, official data, intergovernmental references, and secondary material.
- **Instrument/status** links a source to the temporal graph. `partial` means the family is useful but not yet represented with every modifying event.
- **Harvest** is permission for the repository's bounded downloader, not a statement that redistribution is allowed.
- **Cadence** is a monitoring interval. It never determines whether an instrument is legally current.

See the [generated registry](registry.md) for every source and the [status model](../methodology/status-model.md) for legal-review semantics.

## Boundaries

Structured tariff rows belong in [`arancel-mx`](https://github.com/jccontrerasg08-cpu/arancel-mx). Interactive INEGI and SNICE classifiers, ICC Incoterms rule text, and WCO explanatory notes are catalog-only unless an official reusable download or API is documented and approved.
