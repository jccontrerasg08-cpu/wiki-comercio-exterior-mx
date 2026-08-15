# Contributing

This is a public legal-knowledge repository, not an official gazette. Contributions must make uncertainty and provenance visible.

## Scope a change by source family

A pull request may integrate related laws, regulations, publication events, wiki pages, corpus metadata, tests, and generated catalog output when the result is one reviewable source family. Keep unrelated reforms in separate commits or pull requests.

Every legal change must identify:

- canonical `source_id` and `instrument_id`;
- issuing authority and official URL;
- publication and effective dates, including material transitory rules;
- whether the source is a publication event, consolidated text, administrative portal, data source, or secondary reference;
- affected page status and `current_through` date;
- generated catalog and test evidence.

An HTTP 200 response is transport evidence only. It never proves legal currency.

## Prohibited extraction

Do **not** scrape INEGI TIGIE-SCIAN, SNICE Mi Fracción, ICC Incoterms rule text, WCO explanatory notes, or other interactive/copyrighted material. Catalog the official URL instead.

An exception requires a documented official API or downloadable dataset, terms that permit the intended use, bounded retrieval, a maintainer decision recorded in the pull request, and fixtures that let CI remain offline.

## Content boundaries

- Structured tariff rows belong in [`arancel-mx`](https://github.com/jccontrerasg08-cpu/arancel-mx).
- Official binary files belong in a GitHub Release, not Git history. Commit manifests and SHA-256 values only.
- Project explainers are non-authoritative and must paraphrase, cite official sources, state a review date, and separate facts from operational guidance.
- Superseded material may remain for historical retrieval but must be labeled.

## Required local verification

```bash
python -m unittest discover -s tests -v
python -m scripts.validate_repository
python -m scripts.build_catalog --check
python -m scripts.page_metadata --check
python -m scripts.temporal_graph --check
python -m scripts.rag_eval --check
python -m mkdocs build --strict
git diff --check
```

## License and safety

Unless stated otherwise, original Markdown and code are Apache-2.0. Official material is not relicensed merely because it is cited or summarized here. Never commit credentials, cookies, personal data, taxpayer files, downloaded official PDFs, or proprietary rule text.
