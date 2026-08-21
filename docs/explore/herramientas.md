---
title: "Herramientas verificables"
description: "Catálogo modular de consultas, rutas y dashboards de comercio exterior con estado, fuente y límites explícitos."
---

# Herramientas verificables

Este catálogo organiza las capacidades de la wiki por **tarea**, sin convertir una tarjeta en una conclusión jurídica, fiscal o aduanera. Cada módulo indica qué puede consultar hoy, qué fuente respalda la ruta y qué falta antes de transformarlo en una herramienta de cálculo o verificación más profunda.

> **Regla de uso.** Una herramienta puede ayudarte a recuperar fuentes y ordenar pasos, pero **no clasifica mercancías**, no acredita origen, no determina una tasa preferencial ni genera un pedimento transmisible. Verifica la fuente primaria, la fecha de corte y el contexto de la operación.

## Herramientas disponibles

<div class="grid cards" markdown>

-   :material-barcode-scan:{ .lg .middle } **Buscar fracción y tasa**

    ---

    Consulta la ruta de clasificación, HS, TIGIE, fracción mexicana y NICO; enlaza al dominio estructurado de `arancel-mx` sin duplicar sus tablas.

    **Tipo:** consulta y recuperación · **Fuente principal:** LIGIE/TIGIE, SNICE y release estructurada · **Estado:** disponible como orientación.

    [:octicons-arrow-right-24: Abrir aranceles](aranceles.md)

-   :material-shield-search:{ .lg .middle } **Explorar RRNA y NOM**

    ---

    Recorre regulaciones, restricciones, NOM, reglas y criterios con enlaces a instrumentos y autoridades. Las coincidencias son candidatas de revisión, no una decisión de cumplimiento.

    **Tipo:** descubrimiento regulatorio · **Fuente principal:** DOF/SIDOF, SAT, Secretaría de Economía y autoridades competentes · **Estado:** disponible con límites de cobertura.

    [:octicons-arrow-right-24: Abrir RRNA y NOM](rrna-nom.md)

-   :material-handshake:{ .lg .middle } **Tratados y origen**

    ---

    Conecta instrumentos, partes, reglas de origen, clasificación y fuentes preservadas. Distingue origen preferencial, procedencia, tasa general y programas mexicanos.

    **Tipo:** consulta documental · **Fuente principal:** tratados promulgados, Secretaría de Economía y documentos oficiales · **Estado:** disponible como ruta de evidencia.

    [:octicons-arrow-right-24: Abrir tratados y origen](tratados-origen.md)

-   :material-map-marker-path:{ .lg .middle } **Ruta de importación**

    ---

    Organiza clasificación, RRNA, contribuciones, pedimento, logística y fuentes por etapa. Permite identificar datos faltantes y volver a la evidencia que desbloquea cada paso.

    **Tipo:** recorrido operativo · **Fuente principal:** corpus y metodología de la wiki · **Estado:** disponible; cada mercancía, régimen y fecha requiere revisión propia.

    [:octicons-arrow-right-24: Abrir proceso de despacho](../wiki/aduana/proceso-despacho.md)

-   :material-chart-bar:{ .lg .middle } **Dashboard de recaudación**

    ---

    Explora valores agregados explícitamente publicados por ANAM, con filtros locales, tabla de respaldo y estados vacíos cuando no existe la granularidad solicitada.

    **Tipo:** dashboard de datos · **Fuente principal:** informes de recaudación ANAM · **Estado:** Q2 2026 documentado; no equivale a valor de comercio ni a tasas arancelarias.

    [:octicons-arrow-right-24: Abrir recaudación ANAM](../wiki/aduana/recaudacion-anam.md)

-   :material-earth:{ .lg .middle } **Mundo y fuentes comparables**

    ---

    Filtra guías de país y fuentes internacionales preservando la tabla como ruta primaria. El mapa o globo será una capa opcional sobre datos comparables y geometría verificable.

    **Tipo:** exploración mundial · **Fuente principal:** catálogo global y contratos entre repositorios · **Estado:** disponible en modo texto primero.

    [:octicons-arrow-right-24: Abrir explorador mundial](mundo.md)

</div>

## Módulos en preparación

| Módulo | Qué debe resolver | Dueño del dominio | Condición para activarlo |
|---|---|---|---|
| Simulador de costos de importación | Escenario auditable de valor en aduana, IGI, IVA, IEPS, DTA y cuotas. | `arancel-mx` para tarifa; wiki para fuentes, vigencia y límites. | Reglas y tablas versionadas, supuestos visibles, casos revisados y rechazo de escenarios incompletos. |
| Calculadora de pedimento | Borrador no transmisible de campos y desglose. | Módulo externo futuro; la wiki no transmite ni liquida pedimentos. | Contrato de entrada/salida, Anexo 22 y contribuciones validados, revisión profesional y snapshot de reglas. |
| Verificador T-MEC | Lista de requisitos, evidencia faltante y regla aplicable. | Wiki para fuentes; `arancel-mx` para clasificación. | Datos de clasificación, versión, criterio invocado y documentos; salida siempre “requiere revisión”. |
| Consultor RRNA por producto | Hipótesis de RRNA/NOM por clasificación, operación, autoridad e instrumento. | Wiki, con publicaciones oficiales y corpus controlado. | Corpus versionado, acotaciones/excepciones estructuradas y estado `unknown` cuando no haya evidencia. |
| Comparador de aranceles por país | Mostrar tasas y preferencias comparables para un producto y fecha. | Fuentes internacionales + `arancel-mx`. | Dataset con HS6, versión, tipo de tasa, socio/preferencia, vintage, metodología y licencia de uso. |

## Arquitectura del catálogo

La wiki es la fachada de conocimiento: explica, enlaza, conserva contexto y muestra el estado de evidencia. Los módulos con datos o cómputo propio permanecen en su repositorio canónico y se conectan mediante contratos versionados.

| Capa | Responsabilidad | Ubicación actual | Regla de integración |
|---|---|---|---|
| Conocimiento y evidencia | Fuentes, instrumentos, relaciones, metodología, guías y estados editoriales. | `wiki-comercio-exterior-mx` | La lectura debe funcionar aunque un servicio externo no responda. |
| Aranceles estructurados | LIGIE, TIGIE, fracción, NICO, tasas y releases. | `arancel-mx` | Consumir release/API de sólo lectura con versión, hash y fuente; no copiar tablas. |
| Cambios documentales | Capturas, diffs, evidencia OCR y eventos para revisar. | `dof-diff-lab` | Un cambio detectado no declara vigencia sin revisión humana. |
| Geografía y relaciones | Países, aduanas, puertos, acuerdos y geometría canónica. | `aduanamap-mx` | Consumir un artefacto público e inmutable cuando exista; mientras tanto, usar texto y enlaces. |
| Herramientas con estado | Cálculo, perfiles, cargas o tareas largas. | Módulo externo futuro, sólo si hace falta. | Requiere responsable operativo, contrato de API, monitorización y fallback estático. |

## Cómo elegir una ruta

| Si empiezas con… | Entra primero por… | Antes de seguir, confirma… |
|---|---|---|
| Una descripción o código de mercancía | Aranceles | Versión de clasificación, nivel HS/fracción/NICO y fecha de operación. |
| Un permiso, NOM o requisito sectorial | RRNA y NOM | Clasificación como hipótesis, autoridad, alcance, excepción y publicación aplicable. |
| País de origen o tratado | Tratados y origen | Instrumento, regla de origen, evidencia de certificación, producto y fecha. |
| Una importación concreta | Ruta de importación | Régimen, valor, Incoterm declarado, aduana, documentos y supuestos faltantes. |
| Un dato de desempeño aduanero | Dashboard de recaudación | Periodo, unidad, indicador, fuente y granularidad publicada. |
| Comparar contexto internacional | Mundo y fuentes comparables | Dataset, vintage, reportante, socio, HS6, metodología y comparabilidad real. |

## Ver también

[Explorar comercio exterior](index.md) · [Marco jurídico](marco-juridico.md) · [Arquitectura modular de datos](../about/arquitectura-datos-modular.md) · [Cómo consultar fuentes](../about/como-consultar-fuentes.md) · [Contratos entre repositorios](../methodology/cross-repo-contracts.md)
