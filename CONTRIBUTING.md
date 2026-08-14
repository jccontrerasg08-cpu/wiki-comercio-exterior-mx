# Contributing

This is a public wiki plus an official-URL catalog. Unsourced claims are rejected.

## One coherent legal/source event per PR

A pull request may touch wiki + catalog + corpus + manifest together when they describe **the same** legal or source event (one SIDOF/DOF/SAT publication). Do not mix unrelated reforms.

Catalog-only PRs still need the official URL, authority, and `source_id`. HTTP 200 is not enough.

Scrape [INEGI TIGIE–SCIAN](https://www.inegi.org.mx/app/tigie/) or [SNICE Mi Fracción](https://www.snice.gob.mx/cs/avi/snice/hce.mi.fraccion.arancelaria.html).

## Wiki pages (`docs/wiki/`)

Original explainers only, one topic folder (`fundamentos/`, `aduana/`, `clasificacion/`, `contribuciones/`, `programas/`, `logistica/`). Cite `docs/catalog/` or a SIDOF/Diputados/SAT URL. No LinkedIn, Tec syllabi, LMS dumps, or Incoterms® rule text.

## Originals (`data/originals/`)

Git holds manifests (url, sha256, bytes, `license: official-not-relicensed`). Bytes go in a GitHub Release `originals-YYYY.MM.DD`, not the clone.

## License of contributions

Unless you state otherwise, original markdown and code are Apache-2.0. Do not commit `.env`, `token.txt`, credentials, or personal data.
