---
title: "Mundo y fuentes comparables"
description: "Explorador accesible de guías de país y fuentes internacionales para comercio exterior, preparado para una futura capa cartográfica verificable."
---

# Mundo y fuentes comparables

Esta ruta organiza las guías de país y las fuentes multilaterales que la wiki ya referencia. Es una entrada para **encontrar fuentes y entender sus límites**, no un ranking mundial ni una serie estadística homogénea.

> **Alcance actual.** La capa geoespacial canónica pertenece a `aduanamap-mx`. Su contrato actual es de consumo futuro con artefacto público verificable; la wiki no mantiene una copia alternativa del GeoJSON de países. Por eso esta página empieza con una lista accesible y no muestra un globo que pueda sugerir una cobertura o precisión inexistentes.[^contrato]

## Explora las guías curadas

<div class="world-explorer" data-world-explorer data-source="../../assets/data/world-explorer-sources.json">
  <div class="world-explorer__intro">
    <p class="eyebrow">COBERTURA EDITORIAL · NO SERIE ESTADÍSTICA</p>
    <h2>Lista accesible de países</h2>
    <p>Filtra las guías por región o nombre. Cada resultado conduce a una ficha de fuente; no representa flujo comercial, arancel, recaudación ni relación jurídica por sí solo.</p>
  </div>
  <fieldset class="world-explorer__controls">
    <legend>Filtros de guías de país</legend>
    <p>
      <label for="world-region">Región</label>
      <select id="world-region" data-world-region>
        <option value="">Todas las regiones</option>
        <option value="América del Norte">América del Norte</option>
        <option value="América del Sur">América del Sur</option>
        <option value="Asia Oriental">Asia Oriental</option>
        <option value="Europa">Europa</option>
      </select>
    </p>
    <p>
      <label for="world-query">Buscar país o código ISO3</label>
      <input id="world-query" data-world-query type="search" autocomplete="off" placeholder="Ejemplo: México, USA o Europa">
    </p>
  </fieldset>
  <p class="world-explorer__status" data-world-status aria-live="polite">Lista accesible: 7 guías de país curadas.</p>
  <p class="world-explorer__empty" data-world-empty hidden aria-live="polite"></p>
  <div class="world-explorer__table-wrap">
    <table>
      <caption>Guías de país actualmente incluidas</caption>
      <thead>
        <tr><th scope="col">País</th><th scope="col">ISO3</th><th scope="col">Región</th><th scope="col">Enfoque de la fuente</th></tr>
      </thead>
      <tbody data-world-table>
        <tr><th scope="row"><a href="../catalog/countries/BRA.md">Brasil</a></th><td>BRA</td><td>América del Sur</td><td>Portal oficial de comercio de Brasil</td></tr>
        <tr><th scope="row"><a href="../catalog/countries/CAN.md">Canadá</a></th><td>CAN</td><td>América del Norte</td><td>Portal oficial de comercio de Canadá</td></tr>
        <tr><th scope="row"><a href="../catalog/countries/CHN.md">China</a></th><td>CHN</td><td>Asia Oriental</td><td>Portal oficial de comercio de China</td></tr>
        <tr><th scope="row"><a href="../catalog/countries/DEU.md">Alemania</a></th><td>DEU</td><td>Europa</td><td>Portal oficial de comercio de Alemania</td></tr>
        <tr><th scope="row"><a href="../catalog/countries/JPN.md">Japón</a></th><td>JPN</td><td>Asia Oriental</td><td>Portal oficial de comercio de Japón</td></tr>
        <tr><th scope="row"><a href="../catalog/countries/NLD.md">Países Bajos</a></th><td>NLD</td><td>Europa</td><td>Portal oficial de comercio de Países Bajos</td></tr>
        <tr><th scope="row"><a href="../catalog/countries/USA.md">Estados Unidos</a></th><td>USA</td><td>América del Norte</td><td>Portal oficial de comercio de Estados Unidos</td></tr>
      </tbody>
    </table>
  </div>
  <p><strong>Sin JavaScript:</strong> la tabla y los enlaces se mantienen disponibles; los filtros sólo reducen visualmente la lista cuando el navegador puede cargar datos locales versionados.</p>
</div>

## Fuentes para una comparación internacional futura

| Fuente | Útil para | Antes de comparar con México |
|---|---|---|
| [UN Comtrade](https://comtrade.un.org/) | Flujos de mercancías por reportante, socio, producto y periodo | Fijar flujo, clasificación, revisión, moneda, valoración y fecha de descarga. |
| [WITS / Banco Mundial](https://wits.worldbank.org/) | Comercio, aranceles y medidas no arancelarias | Evitar sumar categorías y componentes; conservar su fuente y metodología. |
| [WTO Tariff & Trade Data](https://ttd.wto.org/en) | Contexto comercial y arancelario intergubernamental | Separar mercancías, servicios, aranceles y periodicidad antes de visualizar. |
| [CEPII BACI](https://www.cepii.fr/cepii/en/bdd_modele/bdd_modele_item.asp?id=37) | Flujos bilaterales reconciliados | Tratarlo como fuente secundaria metodológica, no como declaración oficial de México. |

ANAM describe operación aduanera y recaudación mexicana. UN Comtrade, WITS, OMC y BACI describen otras construcciones estadísticas con cobertura, unidad, calendario, método y revisión propios. Ninguna tarjeta, país o color de una visualización puede convertirlas automáticamente en una métrica comparable.[^global]

## Hacia un mapa mundial verificable

No hay globo WebGL en esta primera capa. Un mapa sólo se habilitará cuando tenga un conjunto de datos con licencia y versión identificadas, fuente y fecha de descarga, clasificación, cobertura, unidad, moneda, método, tabla equivalente y una geometría pública inmutable que cumpla el contrato de AduanaMap.

| Etapa | Condición de entrada | Resultado esperado |
|---|---|---|
| 1. Catálogo y lista | Guías y fuentes documentadas | La ruta actual: lectura, filtro nativo y tabla accesible. |
| 2. Ficha de indicador | Un conjunto mundial con metadatos completos | Tabla, resumen y descarga versionada por indicador. |
| 3. Mapa opcional | Geometría pública verificable, atribución y presupuesto de rendimiento | Mapa no interactivo o MapLibre como mejora progresiva sobre la misma tabla. |
| 4. Escala | Datos o geometría rebasan el presupuesto de GeoJSON | Evaluar PMTiles y carga diferida; no añadir un backend sólo para el mapa. |

Un mapa complejo necesita una descripción breve y otra larga con valores, relaciones y tendencias; la tabla sigue siendo la ruta primaria de consulta.[^wai] La implementación deberá evitar depender de hover, color como único canal, vuelos o animación no esencial, proveedor de teselas sin atribución y consultas en vivo por visitante.

## Fuentes

- [Contrato Wiki ↔ AduanaMap](../ARCHITECTURE.md) y `data/contracts/aduanamap.yaml` del repositorio.
- [Global: fuentes multilaterales](../catalog/global/index.md).
- [Aduanas y mapa](mapa.md).
- [Recaudación ANAM](../wiki/aduana/recaudacion-anam.md), como capa nacional separada.

## Ver también

[Aduanas y mapa](mapa.md) · [Tratados y origen](tratados-origen.md) · [Catálogo global](../catalog/global/index.md) · [Mapa de conocimiento](knowledge-map.md) · [Cómo consultar fuentes](../about/como-consultar-fuentes.md)

[^contrato]: Contrato `world_countries_50m` entre la wiki y AduanaMap MX, revisado el 15 de agosto de 2026. La geometría se declara canónica en AduanaMap, con `mode: contract_only_until_public_artifact` y `embed_ready: false`.
[^global]: [UN Comtrade](https://comtrade.un.org/), [WITS](https://wits.worldbank.org/), [WTO Stats](https://stats.wto.org/) y [CEPII BACI](https://www.cepii.fr/cepii/en/bdd_modele/bdd_modele_item.asp?id=37), consultados el 20 de agosto de 2026. Revisa la metodología de cada conjunto antes de comparar valores.
[^wai]: [W3C WAI, Complex Images](https://www.w3.org/WAI/tutorials/images/complex/), actualizado el 8 de abril de 2026.
