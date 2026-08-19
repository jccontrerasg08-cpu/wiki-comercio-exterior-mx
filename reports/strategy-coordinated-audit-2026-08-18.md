# Síntesis coordinada y arquitectura editorial

**Fecha de corte:** 18 de agosto de 2026  
**Alcance:** estado del repositorio, corpus, fuentes, herramientas, datos, experiencia visual y arquitectura técnica.  
**Método:** diagnóstico local, comprobación de la PR y seis auditorías independientes de contenido, normatividad, operación, herramientas, datos/visualización y calidad técnica.

## Estado de partida

La rama `feat/parser-audit-source-resilience` corresponde al commit `c5e1e00` y la [PR #40](https://github.com/jccontrerasg08-cpu/wiki-comercio-exterior-mx/pull/40) permanece abierta y limpia, con comprobaciones remotas exitosas. El corpus contiene 108 documentos Markdown, 43 páginas bajo `docs/wiki`, 109 fuentes registradas y 10 activos visuales. El tablero de cobertura está actualizado, pero no equivale a una garantía de vigencia: registra 86 páginas, 29 revisadas, 56 pendientes, 40 no actuales, 80 con fuente y 76 instrumentadas.

> **Principio rector.** La wiki puede aspirar a cobertura amplia de temas, pero cada afirmación debe indicar su tipo de evidencia, fuente, fecha de corte y límite. Una interfaz accesible, una URL viva o un resumen local no sustituyen una regla vigente, un trámite aceptado, un acuse ni un expediente de operación.

## Propósito y relato de la wiki

El propósito no es duplicar el Diario Oficial, SNICE, VUCEM, SAT, ANAM, INEGI ni los datos estructurados de repositorios especializados. Es convertir esas fuentes dispersas en un recorrido explicable y verificable. El relato canónico debe responder a la pregunta del lector en este orden.

| Tramo narrativo | Pregunta del lector | Salida que debe producir la wiki | Fuente de verdad principal |
|---|---|---|---|
| Contexto | ¿Qué operación, mercado y objetivo tengo? | Alcance, flujo importar/exportar, régimen y actores | Marco jurídico, política comercial y datos agregados |
| Identidad comercial | ¿Qué es la mercancía y cómo se clasifica? | Hipótesis documentada de fracción/NICO y hechos técnicos | LIGIE/TIGIE, notas, ficha técnica y fuentes estructuradas |
| Aplicabilidad | ¿Qué medida puede alcanzarla hoy? | Matriz fracción–medida–autoridad–fecha–excepción | LCE, reglas, RRNA, NOM, cupos, cuotas y publicaciones vigentes |
| Ejecución | ¿Qué trámite, dato y documento corresponde? | Ruta por plataforma, autoridad, responsable, plazo y acuse | VUCEM, SAT, ANAM, reglas, anexos y manuales técnicos |
| Evento de operación | ¿Qué se declara, mueve o transmite? | Declaración condicionada, documentos comerciales, transporte y eventos | Pedimento/Anexo 22, régimen, contrato, transporte y acuses |
| Evidencia y control | ¿Cómo se reconstruye y corrige después? | Expediente conciliado, control de cambios, conservación, rectificación o respuesta | Documentos, acuses, inventario, conciliación y fuente vigente |

La navegación debe usar estos tramos como historia única. **Explorar** descubre temas y datos; **Wiki** explica decisiones; **Fuentes** prueba procedencia; **Metodología** explica el grado de confianza. Las secciones no deben competir por explicar la misma obligación.

## Hallazgos coordinados

La fortaleza dominante es la trazabilidad: catálogo, manifiestos, estados, pruebas, grafo temporal, evaluaciones RAG y compilaciones estrictas forman una base inusual para una wiki de este dominio. Las debilidades son de conectividad editorial y de completitud relativa, no de falta de enlaces. En particular, el recorrido privilegia la importación y concluye demasiado pronto en logística; varios temas jurídicos y herramientas aparecen desde puertas paralelas; la evidencia primaria de ciertas reformas 2026 sigue incompleta; y los datos, mapas y visualizaciones deben mantenerse claramente separados de una determinación por operación.

| Frente | Hallazgo de mayor impacto | Riesgo si no se corrige | Orden de atención |
|---|---|---|---|
| Narrativa | Falta ruta exportación–salida–prueba–control posterior | Sesgo hacia importación y ciclo incompleto | P0 |
| Operación | Pedimento, documentos, VUCEM y Anexo 22 se explican en piezas separadas | El lector confunde regla, campo, interfaz y acuse | P0 |
| Normatividad | Tratados, LCE, cupos, cuotas y reformas 2026 tienen profundidad desigual | Una fuente parcial puede leerse como aplicación vigente | P0 |
| Herramientas | SIAVI/SIAVI Data, semáforos y manuales requieren límites visibles y entradas/salidas | Uso de una interfaz histórica o técnica como fuente jurídica | P1 |
| Datos y mapas | La nueva página BCMM es una base, pero faltan tarjetas de dataset y mapa público verificable | Sobreinterpretación de contexto agregado o geolocalización | P1 |
| Arquitectura | Varias representaciones de una misma fuente y estados distribuidos | Divergencia de vigencia y costo de mantenimiento | P1 |

## Hoja de ruta por lotes

| Lote | Resultado editorial | Núcleo de evidencia | Criterio de cierre |
|---|---|---|---|
| 1. Exportación verificable | Ruta end-to-end: producto → clasificación → medida → documentos → salida → prueba → control | Ley Aduanera, RGCE/Anexo 22, VUCEM, SNICE, ANAM/SAT cuando proceda | Cada etapa expone decisión, responsable, evidencia y enlace a fuente primaria |
| 2. Expediente y conciliación | Matriz de llaves documentales para importación, exportación y retorno | Pedimento, factura/CFDI, transporte, COVE/e-document, acuses, inventario | Ninguna fila confunde el documento con la autoridad ni el acuse con el cumplimiento |
| 3. Aplicabilidad jurídica | Matriz canónica de RRNA, NOM, cupos y cuotas | Fracción/NICO, acotación, autoridad, fecha efectiva, excepción y trámite | Toda medida muestra vigencia y límite; no se emite “cumple/no cumple” automático |
| 4. Tratados y origen | Fichas comparables de T-MEC, TIPAT y TLCUEM | Partes, entrada en vigor, preferencia, prueba/certificación y fuente oficial | La wiki no asume que el tratado o el origen confieren preferencia sin regla aplicable |
| 5. Herramientas por tarea | Matriz de SNICE, VUCEM, SAT, ANAM, SIAVI/SIAVI Data, calculadoras y consultas | Autoridad, entrada, salida, fecha de verificación, login, límite y evidencia | Cada herramienta se clasifica como orientación, dato, trámite, estado o fuente |
| 6. Datos y mapa | Tarjetas de BCMM/ETEF y mapa con artefacto público o limitación explícita | Dataset, unidad, corte, checksum, script, accesibilidad y metodología | Cada figura incluye tabla, fuente, fecha, estado de cifra y advertencia interpretativa |
| 7. Simplificación técnica | Manifiesto de frescura y generación de vistas derivadas | Registro de fuentes, manifiestos, metadatos, catálogo, vigilancia y CI | Una fuente canónica evita que página, catálogo, RAG y estado discrepen |

## Primer lote recomendado

La siguiente implementación debe ser la **ruta de exportación verificable**. Corrige a la vez el vacío narrativo principal, el sesgo de la portada y la separación entre decisión, trámite, evidencia y control posterior. No requiere una nueva dependencia ni una reescritura de scripts: reutiliza la estructura editorial, fuentes, validadores, diagramas deterministas y navegación existentes.

La página piloto seguirá la plantilla común: **propósito y límite**, **decisiones previas**, **secuencia condicionada**, **matriz de evidencia**, **cambios que obligan a volver atrás**, **fuentes oficiales y referencia temporal**, y **enlaces a páginas canónicas**. La prueba de aceptación será editorial y técnica: fuente directa por afirmación, rutas locales válidas, metadatos, navegación visible, compilación estricta, y comprobación visual en Chrome.

## Decisiones deliberadas de alcance

No se adoptará una “wiki completa” como una única página ni se prometerá automatización jurídica. Tampoco se duplicarán LIGIE/TIGIE, GeoJSON, interfaces VUCEM ni textos legales completos cuando existe una fuente oficial o un repositorio canónico. La ampliación será progresiva: cada lote añadirá una pieza usable y verificable, conservará su procedencia y reducirá un punto específico de ambigüedad.

## Evidencia de la auditoría

Las seis auditorías paralelas se conservaron en `/home/ubuntu/auditar_wiki_comercio_exterior.json` y `.csv` fuera del repositorio de entrega. Sus hallazgos fueron contrastados con el estado local, [PR #40](https://github.com/jccontrerasg08-cpu/wiki-comercio-exterior-mx/pull/40), `docs/status/corpus-coverage.md`, `docs/status/missing-primary-sources.md`, `sources/registry.yaml`, `mkdocs.yml`, documentación de ANAM, SNICE, SAT, VUCEM, Secretaría de Economía e INEGI mencionada en los informes especializados del repositorio.

## Verificación institucional para el lote de exportación

La página institucional **Aprende a Exportar** de SNICE estructura la orientación en siete pasos y, en su etapa documental, pide confirmar fracción arancelaria, regulaciones aplicables y documentos básicos. Señala que el despacho implica presentar mercancía, pedimento de exportación y soportes digitalizados —por ejemplo COVE, permisos, certificados de origen, escritos, avisos y documentos de transporte— previamente tramitados cuando corresponda en VUCEM. La redacción de la wiki debe conservar el carácter orientativo y condicional de esa guía.

La página **Sobre la VUCEM** confirma que es una plataforma integral para enviar información electrónica y efectuar trámites de RRNA antes del despacho emitidos por diversas dependencias. Es una capa de transmisión y gestión; no sustituye a la autoridad competente, la regla aplicable ni la evidencia de una operación. Este límite se incorporará visiblemente a la ruta de exportación.

## Comprobación visual de la ruta de exportación

La nueva página se inspeccionó en Chrome dentro de la navegación real. Aparece bajo **3. Prepara y despacha**, entre el proceso general y los componentes específicos. El panel lateral, la tabla de contenidos y las siete secciones siguen la historia prevista: definición, clasificación/medidas, documentos, transmisión, salida, expediente y control posterior. El diagrama se muestra completo dentro de la columna de lectura, conserva contraste en modo oscuro y queda seguido de una leyenda que limita su uso a orientación. Las tablas se presentan bajo cada decisión y no sustituyen las fuentes jurídicas enlazadas.
