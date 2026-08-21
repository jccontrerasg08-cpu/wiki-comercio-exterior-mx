---
title: "Recaudación ANAM"
description: "Tablero verificable de recaudación aduanera mexicana con datos publicados por ANAM para Q2 2026."
---

# Recaudación ANAM

Este tablero organiza **indicadores agregados publicados por la Agencia Nacional de Aduanas de México (ANAM)** para el segundo trimestre de 2026. Permite recorrer recaudación, pedimentos y operaciones sin convertir un informe visual en una base de datos inexistente.

> **Alcance.** Esta primera versión cubre **Q2 2026 (abril-junio)** y sólo transcribe valores explícitos del [Informe Trimestral Q2 2026 de ANAM](https://www.anam.gob.mx/wp-content/uploads/Informe_trimestral_Q2_2026_f.pdf). Los datos de recaudación están en **MDP** —millones de pesos—; no son equivalentes al valor total del comercio exterior, que el propio informe presenta en otras unidades y con otro propósito.[^anam-q2]

<div class="anam-dashboard" data-anam-dashboard data-source="../../../assets/data/anam-recaudacion-q2-2026.json">
  <div class="anam-dashboard__heading">
    <div>
      <p class="anam-dashboard__eyebrow">México · datos publicados por ANAM</p>
      <h2>Explora el corte trimestral</h2>
      <p>Selecciona un indicador y una vista. El tablero no recalcula participaciones ni inventa granularidad que el informe no publique.</p>
    </div>
    <a class="md-button" href="https://www.anam.gob.mx/wp-content/uploads/Informe_trimestral_Q2_2026_f.pdf">Fuente primaria</a>
  </div>
  <div class="anam-dashboard__filters" aria-label="Filtros del tablero de recaudación">
    <label>Indicador
      <select data-dashboard-metric>
        <option value="recaudacion">Recaudación</option>
        <option value="pedimentos">Pedimentos</option>
        <option value="operaciones">Operaciones</option>
      </select>
    </label>
    <label>Vista
      <select data-dashboard-view>
        <option value="serie">Evolución mensual</option>
        <option value="composicion">Composición por tipo de aduana</option>
        <option value="ranking">Top 15 aduanas</option>
      </select>
    </label>
  </div>
  <p class="anam-dashboard__status" data-dashboard-status aria-live="polite">Selecciona una vista para cargar los datos documentados.</p>
  <div data-dashboard-output></div>
</div>

<noscript>

### Sin JavaScript

| Indicador publicado | Valor | Periodo |
|---|---:|---|
| Recaudación | 336,190 MDP | Q2 2026 |
| Recaudación acumulada | 659,393 MDP | Enero-junio 2026 |
| Pedimentos | 2.72 millones | Q2 2026 |
| Operaciones | 5.65 millones | Q2 2026 |

La fuente primaria y el resumen completo siguen disponibles sin funciones interactivas.

</noscript>

## Lectura rápida del corte Q2 2026

| Métrica | Valor publicado | Contexto de comparación |
|---|---:|---|
| Recaudación trimestral | 336,190 MDP | +4.0% frente a Q1 2026 |
| Recaudación acumulada | 659,393 MDP | Enero-junio 2026 |
| IVA | 232,775 MDP | +9.8% frente a Q1 |
| IGI | 46,509 MDP | +6.3% frente a Q1 |
| IEPS | 46,327 MDP | -19.5% frente a Q1 |
| Operaciones gravadas | 21.0% | Participación de operaciones de comercio exterior en Q2 |

La ANAM reporta que las aduanas marítimas concentraron 52% de la recaudación de Q2, las fronterizas 31% y las interiores 17%. En el ranking de las quince principales aduanas, Nuevo Laredo, Manzanillo y Lázaro Cárdenas encabezaron la recaudación; las quince sumaron 83% del total nacional publicado.[^anam-q2]

## Cómo leer los filtros

La vista de **evolución mensual** está disponible inicialmente sólo para recaudación porque el informe publica esa serie de enero a junio. La **composición** cambia entre el reparto por tipo de aduana para recaudación, pedimentos u operaciones. El **ranking** está disponible para recaudación, pues es el único ranking de este primer conjunto de datos cuyos valores textuales se verificaron uno por uno.

Si una combinación no aparece, el tablero muestra un estado explícito. No rellena una serie con OCR incompleto, no deduce valores desde una gráfica y no transforma pedimentos u operaciones en pesos.

## Contrato de datos del prototipo

Cada registro que consume este prototipo pertenece al dominio `revenue_anam`: conserva fuente, periodo, medida, unidad, moneda y granularidad publicada. El [modelo unificado de datos](../../about/arquitectura-datos-modular.md) reserva contratos distintos para `tariff` y `trade_flow`; por ello, este tablero no suma ni compara su recaudación con tasas arancelarias o valores de comercio internacional.

| Campo de observación | Uso en este prototipo | Límite actual |
|---|---|---|
| Fuente y release | Informe Trimestral Q2 2026 de ANAM y URL primaria | ANAM publica un catálogo de PDFs, no una API tabular. |
| Periodo y frecuencia | Q2 2026; enero–junio para la serie mensual disponible | No se infieren meses, años o categorías ausentes. |
| Medida y unidad | Recaudación en MDP; pedimentos y operaciones como conteos | Las unidades no se transforman entre sí. |
| Geografía | México y tipos/ranking de aduana cuando el informe lo publica | No se geocodifican aduanas ni se presume cobertura territorial. |
| Estado de granularidad | Agregado, composición o ranking según el indicador | Una combinación sin datos publicados muestra estado vacío. |

## Fuentes, método y límites

La página de [Recaudación ANAM](https://www.anam.gob.mx/recaudacion-anam/) funciona como catálogo de informes PDF mensuales, trimestrales e históricos. No publica en esa página una API, CSV o XLSX estructurado. Por ello, este tablero es una **capa editorial de datos extraídos con procedencia**, no una réplica de un portal de datos abiertos de ANAM.

Cada valor del archivo local conserva fuente, título, periodo, unidad, fecha de consulta y nota metodológica. La recaudación se presenta como flujo de efectivo y el informe advierte que puede haber diferencias por redondeo. «Otros» agrupa DTA, ISAN, cuotas compensatorias, prevalidación, medidas de transición temporal, recargos, sanciones y actualizaciones.[^anam-q2]

> **No extrapoles.** Un mayor número de operaciones no equivale necesariamente a mayor recaudación; las exportaciones y las importaciones no gravadas forman parte de la operación aduanera sin generar el mismo ingreso directo. Este tablero no califica eficiencia, riesgo o desempeño de una aduana fuera de los indicadores que ANAM publica.

## Del tablero nacional al mapa mundial

La prioridad es México: ANAM es una fuente nacional con categorías operativas propias —aduanas marítimas, fronterizas e interiores— y recaudación en MDP. El siguiente paso geográfico debe integrarse con la [capa mundial existente](../../explore/mapa.md), cuya geometría canónica vive en `aduanamap-mx`.

| Capa futura | Fuente necesaria | Regla de comparación |
|---|---|---|
| México por aduana | ANAM, con PDF, periodo y definición | Mantener MDP y nivel de agregación publicados. |
| México por entidad o puerto | Fuente oficial que publique la relación geográfica | No inferir coordenadas ni adscripción desde mapas visuales. |
| Comercio internacional por país | Fuente internacional separada y metodológicamente compatible | Distinguir valor comercial, volumen y recaudación aduanera. |
| Recaudación aduanera mundial | Fuentes nacionales comparables por país | Conservar moneda original, periodo, definición fiscal y cobertura antes de convertir o comparar. |

El mapa será una capa de exploración y nunca una dependencia de verdad jurídica o fiscal. No se mezclarán en un mismo total la recaudación ANAM, el valor global de importaciones/exportaciones o la actividad de aduanas de otros países sin documentar moneda, metodología, fecha y nivel geográfico.

## Ver también

[Catálogo de informes ANAM](../../catalog/mexico/recaudacion-anam.md) · [ANAM](anam.md) · [Aduanas y mapa](../../explore/mapa.md) · [Fuentes oficiales](../../catalog/publicaciones-oficiales.md) · [Cómo consultar fuentes](../../about/como-consultar-fuentes.md)

[^anam-q2]: [ANAM, Informe Trimestral Q2 2026](https://www.anam.gob.mx/wp-content/uploads/Informe_trimestral_Q2_2026_f.pdf), consultado el 20 de agosto de 2026. Las cifras y notas aquí descritas se limitan a lo que el informe publica de forma explícita.
