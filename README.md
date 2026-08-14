# Wiki Comercio Exterior MX

Public wiki and official-source catalog for Mexican foreign trade: pedagogical notes, official URLs, hashed manifests, and RAG summaries.

This is not SAT, ANAM, or the Diario Oficial. The workshop/app stays private at [`comercio-exterior-mexico`](https://github.com/jccontrerasg08-cpu/comercio-exterior-mexico). Tariff tables live in [`arancel-mx`](https://github.com/jccontrerasg08-cpu/arancel-mx).

Binding cite: SIDOF, Cámara de Diputados, or SAT. Incoterms®: [ICC](https://iccwbo.org/business-solutions/incoterms-rules/), [ICC México](https://iccmex.mx/seccion/incoterms-2020), [ICC 2go](https://2go.iccwbo.org) only. This repo does not ship Incoterms rule text.

Official PDF/DOC/XLSX bytes are **GitHub Release** assets (`originals-YYYY.MM.DD`), not clone blobs. Git holds `MANIFEST.yaml` + SHA-256.

## Contents

- [What this is](#what-this-is)
- [Clone](#clone)
- [Folder map](#folder-map)
- [How to cite](#how-to-cite)
- [Tests](#tests)
- [License](#license)

## What this is

| Path | What it is | What it is not |
|---|---|---|
| [`docs/wiki/`](docs/wiki/index.md) | Wiki Comercio Exterior MX | Legal advice, SAT, a Tec syllabus |
| [`docs/catalog/`](docs/catalog/index.md) | Official URL catalog | The DOF |
| [`data/originals/`](data/originals/README.md) | Manifests, hashes, redistribution notes | A license grant over gazettes |
| [`data/corpus/`](data/corpus/README.md) | RAG summaries (`official-not-relicensed`) | Binding law |

Original markdown and tests are Apache-2.0. Official gazettes remain government/treaty publications; see [NOTICE](NOTICE).

## Clone

```
git clone https://github.com/jccontrerasg08-cpu/wiki-comercio-exterior-mx.git
cd wiki-comercio-exterior-mx
```

Optional wiki preview:

```
pip install -r requirements-docs.txt
mkdocs serve
```

## Folder map

```
docs/wiki/       Wiki Comercio Exterior MX
docs/catalog/    Official URLs (Mexico deep, global thin)
sources/         registry.yaml (one official URL per PR)
data/originals/  MANIFEST.yaml + SHA-256; bytes in Releases
data/corpus/     RAG summaries (not the DOF)
tests/           wiki citation checks
```

## How to cite

1. Prefer the official URL in `docs/catalog/` or the `url` field in `data/originals/**/MANIFEST.yaml`.
2. If you use a Release PDF, keep the SHA-256 from the manifest and say it is a copy of the gazette.
3. Do not treat `data/corpus/` as SIDOF.

## Tests

```
python -m unittest tests.test_career_wiki
```

## License

Apache-2.0 for original notes, catalog markdown, tests, and community files. Official publications are not re-licensed. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
