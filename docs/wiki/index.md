# Wiki Comercio Exterior MX

Wiki pedagógica en `docs/wiki/` para entrenamiento: qué es cada figura y cómo aparece en una operación de importación o exportación.

No es SAT/DOF. Manifiestos y SHA-256 viven en `data/originals/`; los PDF oficiales salen en el GitHub Release `originals-*`. [arancel-mx](https://github.com/jccontrerasg08-cpu/arancel-mx) es el paquete público de tarifa.

## Capas de este repositorio

| Capa | Qué es | Qué no es |
|---|---|---|
| `docs/catalog/` | Catálogo de URLs oficiales | El DOF, ni PDFs |
| `data/originals/` | Manifiestos + hashes (bytes en Release) | Resumen para RAG |
| `data/corpus/` | Resúmenes Markdown (`official-not-relicensed`) | Texto vinculante |
| `docs/wiki/` (esta wiki) | Notas pedagógicas | Asesoría legal, curso de negocio |

Cita vinculante: URL de SIDOF, Cámara de Diputados o SAT. `docs/catalog/` no sustituye al DOF.

Incoterms®: citamos a la ICC. No copiamos el libro, el PDF, el wallchart ni las 11 reglas. Catálogo: [ICC](https://iccwbo.org/business-solutions/incoterms-rules/), [ICC México](https://iccmex.mx/seccion/incoterms-2020), [ICC 2go](https://2go.iccwbo.org). Página local: [Incoterms](incoterms.md).

Notas explicativas del SA (OMA) y apps SNICE/INEGI: solo catálogo. No se scrapean ni se versionan aquí.

Fuentes oficiales (no scrapear): [SNICE LIGIE](https://www.snice.gob.mx/cs/avi/snice/ligie.info22.html) (IMMEX, PROSEC, RRNA), [INEGI TIGIE–SCIAN](https://www.inegi.org.mx/app/tigie/). La URL [SNICE Mi Fracción](https://www.snice.gob.mx/cs/avi/snice/hce.mi.fraccion.arancelaria.html) sigue publicada, pero el 13-ago-2026 era un cascarón CMS vacío. Catálogo local: `docs/catalog/catalog.md`.

## Temario vs este repo

Temas que suelen aparecer en cursos comerciales de importación. Aquí solo hay lo que ya existe como URL oficial, bytes o nota pedagógica. El resto se marca hueco. No se inventa consejo de negocio con pinta de SAT.

Estado: **cubierto** hay página o corpus. **solo catálogo** hay URL, sin texto de la obra. **hueco** no hay fuente oficial aquí.

### Cómo importar desde cero

| Tema | En este repo | Fuente oficial | Estado |
|---|---|---|---|
| Tipos de importación | [Pedimento y RGCE](pedimento-rgce.md), [IMMEX](immex.md); corpus `data/corpus/ley-aduanera.md` (art. 90) y `anexo-29-regimenes-prohibidos.md` | [Ley Aduanera](https://www.diputados.gob.mx/LeyesBiblio/pdf/LAdua.pdf), [RGCE 2026](https://sidof.segob.gob.mx/notas/5777199) | cubierto como regímenes legales, no como "estrategia comercial" |
| Estrategias de importación | — | — | hueco |
| Aduana | [ANAM](anam.md); corpus anexos 3, 4, 21 | [ANAM](https://anam.gob.mx/), SIDOF RGCE | cubierto (autoridad y recintos). ANAM no es una agencia aduanal privada |
| Documentos | [Pedimento y RGCE](pedimento-rgce.md); corpus `anexo-01-formatos-modelos.md`, `anexo-22.md`; originales `data/originals/vucem/` (manifestación de valor) | SIDOF anexos 1 y 22, [VUCEM](https://www.ventanillaunica.gob.mx/) | cubierto para documentos aduaneros. Hueco para plantillas de contrato mercantil |
| Cálculo de costos | [Valor en aduana](valor-en-aduana.md), [Aranceles](aranceles.md) | LA arts. 64-78, [LIGIE](https://www.diputados.gob.mx/LeyesBiblio/pdf/LIGIE_2022.pdf) | cubierto para base gravable y arancel. Hueco para costo-beneficio o precio de reventa |
| Contribuciones e impuestos | [Aranceles](aranceles.md), [Cuotas compensatorias](cuotas-compensatorias.md); corpus `anexo-13-multas-cantidades.md`, `anexo-27-fracciones-sin-iva.md`; RMF en `data/originals/sat/rmf-2026/` | LIGIE, RGCE, SAT RMF | cubierto (IGI, IVA en aduana, DTA, cuotas). RMF está en originales, sin página en esta wiki |
| Cómo elegir agencia aduanal | [Pedimento y RGCE](pedimento-rgce.md); corpus LA arts. 54, 159, 167-D y `criterios-anam-sat.md` | [Ley Aduanera](https://www.diputados.gob.mx/LeyesBiblio/pdf/LAdua.pdf) | cubierto como patente, agencia aduanal y responsabilidades. Hueco como directorio de despachadores |
| Transporte y logística | [Logística internacional](logistica-internacional.md); corpus `anexos-riesgo-logistica.md` | ANAM, anexos RGCE de tránsito | cubierto a nivel figura y restricciones de ruta. Hueco para cotizar flete |
| Formas de pago seguras | [Pagos internacionales](pagos-internacionales.md) | — | hueco. No hay guía SAT de "pago seguro". Esa página no es asesoría bancaria |
| Ejemplos de productos: textiles, ropa, maquinaria, juguetes, autos, autopartes, coleccionables | [TIGIE y NICO](tigie-nico.md), [RRNA](rrna.md), [Padrón](padron-importadores.md); corpus `anexo-10-padron-sectorial.md` (textil caps. 50-63, automotriz), `anexo-28-mercancias-certificacion-iva-ieps.md`, `noms-comercio-exterior.md`, `tigie-nico-notas.md` | LIGIE, SNICE, Anexo 10 SIDOF | cubierto como fracción, NOM y padrón sectorial. Hueco como "qué producto conviene importar" |

### Cómo iniciar un negocio de importación

| Tema | En este repo | Fuente oficial | Estado |
|---|---|---|---|
| ¿Es buen negocio? | — | — | hueco |
| Productos buenos o malos | Mismos anexos de producto que arriba; [Cuotas](cuotas-compensatorias.md) | SNICE cuotas, Anexo 10, NOMs | cubierto como restricciones. Hueco como ranking comercial |
| Proveedores confiables | — | — | hueco |
| Investigación previa | [TIGIE y NICO](tigie-nico.md), [RRNA](rrna.md) | SNICE LIGIE, INEGI (solo catálogo) | cubierto para fracción y RRNA. Hueco para estudio de mercado |
| Con cuánto dinero (costos vs ganancia) | — | — | hueco |
| Tipos de negocios | [IMMEX](immex.md), [PROSEC](prosec.md), [Padrón](padron-importadores.md) | SNICE, RGCE | cubierto como programas legales. Hueco como modelos de negocio |
| Aspectos legales al iniciar | [Padrón](padron-importadores.md); corpus LA art. 59, Anexo 1 formato A1 | [SAT Padrón](https://www.sat.gob.mx/minisitio/PadronImportadoresExportadores/index.html) | cubierto para inscripción aduanera. Hueco para constituir sociedad |
| Operación (ventas y administración) | — | — | hueco, salvo despacho: [Pedimento y RGCE](pedimento-rgce.md) |

### Otros cursos

| Tema | En este repo | Fuente oficial | Estado |
|---|---|---|---|
| Logística internacional | [Logística internacional](logistica-internacional.md) | ANAM | cubierto (figura). No es un diplomado de cadena de suministro |
| Clasificación arancelaria | [TIGIE y NICO](tigie-nico.md), [Sistema Armonizado](sistema-armonizado.md); corpus `tigie-nico-notas.md`, `anexo-06-consejo-clasificacion-arancelaria.md` | LIGIE, [OMA nomenclatura](https://www.wcoomd.org/en/topics/nomenclature.aspx) | cubierto en TIGIE. Notas explicativas del SA: solo catálogo |
| Operación aduanera | [Pedimento y RGCE](pedimento-rgce.md), [ANAM](anam.md); originales `data/originals/vucem/` | SIDOF RGCE, VUCEM | cubierto |
| Documentos de comercio exterior | corpus Anexo 1 y Anexo 22; VUCEM manifestación de valor | SIDOF, VUCEM | cubierto |
| Incoterms | [Incoterms](incoterms.md) | ICC (tres URLs arriba) | solo catálogo |

## Contents

- [Clasificación y arancel](#clasificacion-y-arancel)
- [Programas y origen](#programas-y-origen)
- [Despacho](#despacho)
- [Logística y pagos](#logistica-y-pagos)

## Clasificacion y arancel

- [Sistema Armonizado](sistema-armonizado.md) - Nomenclatura WCO (HS 2022).
- [TIGIE y NICO](tigie-nico.md) - Fracción de 8 dígitos y NICO de 10.
- [Aranceles](aranceles.md) - IGI/IGE y cómo leer la tarifa.

## Programas y origen

- [TLC y T-MEC](tlc-tmec.md) - Tratados y preferencia arancelaria.
- [Reglas de origen](reglas-de-origen.md) - Cómo califica una mercancía.
- [PROSEC](prosec.md) - IGI preferencial por sector.
- [IMMEX](immex.md) - Importación temporal para exportar.
- [RRNA](rrna.md) - Regulaciones y restricciones no arancelarias.

## Despacho

- [Pedimento y RGCE](pedimento-rgce.md) - Declaración aduanera y anexos SIDOF.
- [ANAM](anam.md) - Agencia Nacional de Aduanas (autoridad), no agencia aduanal privada.
- [Padrón de importadores](padron-importadores.md) - Inscripción SAT.
- [Valor en aduana](valor-en-aduana.md) - Base gravable (OMC).
- [Cuotas compensatorias](cuotas-compensatorias.md) - Remedios comerciales (UPCI/SNICE).

## Logistica y pagos

- [Incoterms](incoterms.md) - Incoterms® 2020 (ICC). Solo catálogo; no hay texto de las reglas.
- [Logística internacional](logistica-internacional.md) - Transporte, seguros, documentos.
- [Pagos internacionales](pagos-internacionales.md) - Cartas de crédito y transferencias. No es guía de "pago seguro".

> No es asesoría legal. Corrobora contra SIDOF, Diputados o SAT.
