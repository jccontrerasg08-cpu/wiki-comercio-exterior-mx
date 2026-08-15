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

```
git clone https://github.com/jccontrerasg08-cpu/wiki-comercio-exterior-mx.git
cd wiki-comercio-exterior-mx
pip install -r requirements-docs.txt
python -m mkdocs serve
python -m unittest discover -s tests -v
python -m scripts.validate_repository
python -m scripts.rag_eval --check
```

## Licencia

Apache-2.0 para notas originales. Las gacetas oficiales no se relicencian. Ver [LICENSE](LICENSE) y [NOTICE](NOTICE).
