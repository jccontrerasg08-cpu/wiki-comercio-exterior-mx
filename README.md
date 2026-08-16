# Wiki Comercio Exterior MX

Conocimiento verificable de comercio exterior **con México al centro**: aduanas, TIGIE/NICO, RGCE, RRNA, tratados y procedimientos, enlazados a fuentes oficiales. Capa internacional hasta **HS6**. No es SAT, ANAM ni el Diario Oficial.

[Explorar el sitio](docs/index.md) · [Fuentes generadas](docs/catalog/registry.md) · [Metodología](docs/methodology/index.md) · [arancel-mx](https://github.com/jccontrerasg08-cpu/arancel-mx)

## Qué encontrarás

**México:** aduanas, TIGIE/NICO, RGCE, RRNA/NOM, contribuciones, tratados, IMMEX/PROSEC, documentos y despacho.

**Internacional (hasta HS6):** Sistema Armonizado, OMA/OMC, tarifas y comercio (WITS, WTO TTD, Comtrade), origen, valoración, portales aduaneros. Las extensiones nacionales (HTS, TARIC, TIGIE 8/10) no son universales.

Las **tablas de tarifa estructuradas** no viven aquí: están en [`arancel-mx`](https://github.com/jccontrerasg08-cpu/arancel-mx).

## Cómo está organizado

```
docs/             Sitio MkDocs integrado
docs/wiki/        Enciclopedia pedagógica
docs/catalog/     Guía y catálogo generado
sources/          registro, instrumentos y metadatos canónicos
data/originals/   MANIFEST + SHA-256; PDF en Releases
data/corpus/      Digest RAG (no es el DOF)
evals/            Preguntas temporales revisadas
```

Cita vinculante: SIDOF, Diputados o SAT. Incoterms®: solo [ICC](https://iccwbo.org/business-solutions/incoterms-rules/), [ICC México](https://iccmex.mx/seccion/incoterms-2020), [ICC 2go](https://2go.iccwbo.org).

## Cómo empezar

```bash
git clone https://github.com/jccontrerasg08-cpu/wiki-comercio-exterior-mx.git
cd wiki-comercio-exterior-mx
pip install -r requirements-docs.txt
python -m mkdocs serve
python -m unittest discover -s tests -v
python -m scripts.validate_repository
python -m scripts.rag_eval --check
```

## Consulta local gobernada

La recuperación local reutiliza los mismos gates temporales y de revisión del repositorio. El corte es obligatorio para evitar asumir implícitamente que una fuente representa la ley vigente hoy.

```bash
python -m scripts.query_knowledge "IMMEX Anexo 24" --cutoff 2026-08-15
python -m scripts.query_knowledge "IMMEX Anexo 24" --cutoff 2026-08-15 --json
```

La salida JSON puede alimentar una capa posterior de LLM para explicación o conexiones adicionales. El LLM no sustituye la selección temporal ni la evidencia oficial.

## Build web y offline

El perfil normal conserva Instant Navigation para GitHub Pages:

```bash
python -m mkdocs build --strict
python -m scripts.verify_site site
```

El perfil offline desactiva funciones dependientes de `fetch`, activa el plugin offline de Material y comprueba que el artefacto no requiera recursos remotos en tiempo de ejecución:

```bash
python -m mkdocs build --strict -f mkdocs.offline.yml -d site-offline
python -m scripts.verify_offline_site site-offline
```

Después del build offline, `site-offline/index.html` está diseñado para abrirse directamente con `file://`.

## Licencia

Apache-2.0 para notas originales. Las gacetas oficiales no se relicencian. Ver [LICENSE](LICENSE) y [NOTICE](NOTICE).
