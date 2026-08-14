# Contributing

This is a public wiki plus an official-URL catalog. Unsourced claims are rejected.

## One official URL per catalog PR

Each pull request that changes `docs/catalog/` or `sources/registry.yaml` adds or updates **one** official URL. Include authority. HTTP 200 is not enough.

Do not scrape [INEGI TIGIE–SCIAN](https://www.inegi.org.mx/app/tigie/) or [SNICE Mi Fracción](https://www.snice.gob.mx/cs/avi/snice/hce.mi.fraccion.arancelaria.html).

## Wiki pages (`docs/wiki/`)

Original explainers only, one topic folder (`fundamentos/`, `aduana/`, `clasificacion/`, `contribuciones/`, `programas/`, `logistica/`). Cite `docs/catalog/` or a SIDOF/Diputados/SAT URL. No LinkedIn, Tec syllabi, LMS dumps, or Incoterms® rule text.

## Originals (`data/originals/`)

Git holds manifests (url, sha256, bytes, `license: official-not-relicensed`). Bytes go in a GitHub Release `originals-YYYY.MM.DD`, not the clone.

## License of contributions

Unless you state otherwise, original markdown and code are Apache-2.0. Do not commit `.env`, `token.txt`, credentials, or personal data.
