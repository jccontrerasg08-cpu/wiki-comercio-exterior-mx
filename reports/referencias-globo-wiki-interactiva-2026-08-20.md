# Referencias y decisión preliminar — globo y wiki interactiva

Fecha de investigación: 20 de agosto de 2026.

## Principios adoptables

| Principio | Base comprobada | Decisión para la wiki |
|---|---|---|
| HTML antes que JavaScript | GOV.UK recomienda que la función principal exista en HTML y que JavaScript sólo mejore la experiencia. | La tabla, resumen y enlaces a fuente serán siempre la experiencia base; el mapa/globo será opcional. |
| Equivalente textual de un mapa | W3C WAI caracteriza los mapas como imágenes complejas que requieren descripción breve y descripción larga estructurada. | Todo mapa tendrá resumen, tabla/lista de entidades, unidad, periodo, fuente y nota metodológica visibles. |
| No usar globo 3D como punto de partida | Cesium, Globe.gl y MapLibre usan WebGL; su exploración visual no asegura operación accesible ni buen rendimiento en hardware limitado. | No se incorporará un globo WebGL todavía. Primero se añadirá una ficha geoespacial textual/HTML y una integración visual opcional bajo presupuesto explícito. |
| GeoJSON reducido y bajo demanda | MapLibre documenta eliminar propiedades, reducir precisión, simplificar geometría, dividir datos, cargar por URL y teselar si hay grandes volúmenes. | Reutilizar la geometría canónica de `aduanamap-mx`, no duplicarla; cargar sólo un resumen de países cuando exista una fuente mundial validada. |
| PMTiles sólo al crecer | PMTiles permite un archivo de teselas en almacenamiento estático y no requiere backend de teselas propio. | PMTiles es una vía futura cuando la capa mundial supere el presupuesto de GeoJSON; no es dependencia del MVP. |
| Metadatos internacionales | SDMX y fuentes de comercio distinguen unidad, moneda, clasificación, revisión, cobertura, valoración y transformaciones. | ANAM y datos globales permanecerán en capas separadas con sus propios metadatos; nunca se compararán automáticamente. |

## Proyectos revisados

| Proyecto o guía | Función principal | Aplicabilidad |
|---|---|---|
| [MapLibre GL JS](https://github.com/maplibre/maplibre-gl-js) | Mapas WebGL, globo, GeoJSON y vector tiles; licencia BSD-3-Clause. | Opción futura si el mapa necesita capas vectoriales o gran volumen de datos. |
| [Globe.gl](https://github.com/vasturiano/globe.gl) y [three-globe](https://github.com/vasturiano/three-globe) | Globo WebGL narrativo con arcos, puntos y coropletas; licencia MIT. | Sólo para una visualización editorial posterior y nunca como única interfaz. |
| [CesiumJS](https://github.com/CesiumGS/cesium) | Globo geoespacial 3D avanzado; licencia Apache-2.0. | Excesivo para el alcance actual; reservar para 3D Tiles, terreno o precisión especializada. |
| [PMTiles](https://github.com/protomaps/PMTiles) | Archivo único de teselas para hosting estático; implementaciones BSD-3-Clause. | Ruta de escala sin backend cuando datos y geometrías validadas lo justifiquen. |
| [WTO Stats](https://stats.wto.org/), [OEC](https://oec.world/en/) y [CBP Public Data Portal](https://www.cbp.gov/newsroom/stats/cbp-public-data-portal) | Patrones de filtro, descarga, metadatos y contexto. | Adoptar ficha de indicador, periodo, unidad, fuente, revisión y tabla equivalente, no su arquitectura completa. |

## Criterios de implementación

1. El primer cambio geoespacial debe conservar el sitio estático y no añadir una dependencia de WebGL o un proveedor de teselas.
2. La información debe funcionar sin JavaScript, con teclado y con `prefers-reduced-motion`.
3. La capa visual no puede ocultar fuente, moneda, unidad, periodo, cobertura, clasificación ni metodología.
4. Los datos ANAM de recaudación no se mezclan con valor internacional de comercio, estadísticas de flujo ni recaudación de otros países.
5. Antes de usar datos internacionales se requiere un conjunto con licencia, versión/vintage, clasificación, flujo, socio, valoración, moneda y tabla equivalente documentados.
6. Toda cartografía futura requerirá atribución de geometría, mapa base y datos; la licencia del componente no cubre los datos o teselas.

## Fuentes primarias de recomendación

- [GOV.UK — Building a robust frontend using progressive enhancement](https://www.gov.uk/service-manual/technology/using-progressive-enhancement)
- [W3C WAI — Complex Images](https://www.w3.org/WAI/tutorials/images/complex/)
- [MapLibre — Optimising performance for large GeoJSON](https://maplibre.org/maplibre-gl-js/docs/guides/large-data/)
- [PMTiles](https://github.com/protomaps/PMTiles)
- [W3C — WCAG focus visible](https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html)
- [W3C — WCAG non-text contrast](https://www.w3.org/WAI/WCAG21/Understanding/non-text-contrast.html)
- [UN Comtrade](https://comtrade.un.org/)
- [WITS, Banco Mundial](https://wits.worldbank.org/)
- [WTO Stats](https://stats.wto.org/)
- [SDMX Guidelines](https://sdmx.org/guidelines/)

## Verificación visual de la primera mejora

La vista previa local de `explore/mundo/` confirmó que la página carga el conjunto local y anuncia «Mostrando 7 guías de país curadas». La tabla es visible sin depender de interacción y presenta país, ISO3, región y enfoque de fuente. La corrección de la ruta del JSON fue necesaria porque `../assets` se resolvía bajo `/explore/`; `../../assets` resuelve correctamente desde la URL publicada `/explore/mundo/`.

La prueba visual también confirmó que los controles nativos de región y búsqueda son visibles, están etiquetados y conservan foco perceptible. La siguiente comprobación manual reduce la lista mediante filtro regional; no se ha incorporado WebGL, proveedor de teselas, globo ni geometría mundial dentro de la wiki.

La prueba manual por teclado seleccionó «América del Norte» en el control nativo de región. El estado accesible cambió a «Mostrando 2 guías de país curadas» y la tabla se redujo a Canadá (CAN) y Estados Unidos (USA). La navegación, el foco visible y la tabla permanecieron disponibles; esta interacción no usa hover, globo, WebGL ni una fuente de datos remota.
