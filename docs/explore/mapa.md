---
title: "Explorar aduanas y mapa"
description: "Entrada geográfica al comercio exterior que relaciona territorio, autoridad, herramientas oficiales, rutas operativas y fuentes jurídicas sin reemplazarlas."
---

# Aduanas y mapa

Un mapa puede responder “**dónde** ocurre una parte de la operación”; rara vez responde por sí solo “**qué obligación aplica**”. En comercio exterior, la ubicación de una aduana, puerto, aeropuerto, cruce o recinto ayuda a organizar logística, actores y documentación, pero no sustituye la fracción, el régimen, el instrumento, la autoridad competente ni la fecha de vigencia. Esta entrada conecta la exploración geográfica con las páginas que resuelven esas preguntas.

La wiki ofrece una capa cartográfica contextual, mientras [`aduanamap-mx`](https://github.com/jccontrerasg08-cpu/aduanamap-mx) conserva la aplicación geoespacial avanzada y los datasets canónicos. Mantener esa separación evita dos problemas: duplicar geodatos en varios repositorios y presentar un punto en el mapa como evidencia jurídica de competencia, horario, autorización o aplicabilidad normativa.

## Tres capas para leer una ubicación

| Capa | Pregunta que ayuda a responder | Fuente o herramienta útil | Lo que no debe inferirse |
|---|---|---|---|
| Geográfica | ¿Qué país, corredor, puerto, aeropuerto, cruce o aduana parece relevante? | Mapa, rutas logísticas, datos canónicos de AduanaMap | Que el lugar por sí mismo define régimen, fracción o requisito. |
| Operativa e institucional | ¿Qué autoridad, sistema o canal de trámite participa? | [ANAM](https://anam.gob.mx/), [Ventanilla Única](https://www.ventanillaunica.gob.mx/), agente/agencia y documentos del transporte | Que una interfaz común convierte a todas las autoridades en una sola autoridad decisora. |
| Jurídica y temporal | ¿Qué instrumento, supuesto, fecha y evidencia gobiernan la operación? | Leyes, LIGIE/TIGIE, RGCE, DOF/SIDOF, tratados, acuerdos y anexos | Que un mapa o directorio confirme la vigencia o el alcance de una medida. |

La utilidad del mapa aparece cuando las tres capas se recorren juntas. Por ejemplo, si la operación usa un puerto o frontera específica, el componente geográfico orienta la logística y el punto de ingreso; después se confirma el régimen, documentación, transmisión y autoridades aplicables. El lugar puede afectar tiempos, servicios y ruta física, pero una RRNA o una preferencia arancelaria se revisa contra su instrumento, fracción, origen, condiciones y fecha, no contra el color de un marcador.

## Cómo conectar mapa, despacho y evidencia

### 1. Comienza con una pregunta geográfica acotada

Formula la necesidad sin convertirla en conclusión: “¿qué opciones de entrada se relacionan con esta cadena logística?”, “¿qué aduana o corredor aparece en la ruta?” o “¿qué infraestructura debe coordinarse?”. La capa geográfica sirve para ordenar el contexto de transporte, no para seleccionar una estrategia regulatoria.

El sitio de ANAM muestra accesos institucionales a Sistema Electrónico de Aduanas, VUCEM, Módulo Único de Pago Electrónico Aduanero, recintos fiscalizados y programas especiales.[1] Estos accesos ayudan a localizar canales oficiales, pero cada trámite conserva su fundamento, responsable y datos requeridos. Consulta [ANAM y autoridad aduanera](../wiki/aduana/anam.md) para esa distinción.

### 2. Traduce el punto del mapa en un flujo de operación

Una ubicación sólo es útil si se enlaza con la operación que ocurrirá allí. Define al menos mercancía, régimen, medio de transporte, actor responsable, fecha prevista y documentos que deben estar disponibles. Continúa con [Proceso de despacho](../wiki/aduana/proceso-despacho.md), [Regímenes aduaneros](../wiki/aduana/regimenes-aduaneros.md), [Documentos](../wiki/aduana/documentos.md) y [Logística internacional](../wiki/logistica/logistica-internacional.md).

Cuando haya trámite electrónico, recuerda que una plataforma gestiona información, pero no elimina el análisis previo. VUCEM se presenta institucionalmente como un canal para transmitir información y gestionar trámites relacionados con comercio exterior; la autoridad competente y el instrumento aplicable dependen del acto concreto.[2]

### 3. Enlaza la ubicación con el expediente, no sólo con un itinerario

El expediente debe poder relacionar el dato de ubicación con el documento o evento que lo exige: documento de transporte, pedimento, recinto, autorización, acuse, inspección o incidencia. Si la ruta cambia, no asumas que todos los efectos legales cambian con ella; revisa qué campos, plazos, datos transmitidos o soportes sí dependen de ese cambio. La [Arquitectura de decisión y evidencia](../wiki/fundamentos/arquitectura-decision-evidencia.md) describe cómo distinguir el flujo físico, el jurídico, el digital y el probatorio.

## Qué muestra el mapa y qué debe verificarse fuera de él

| Si el mapa ayuda a observar… | La siguiente verificación debe ser… |
|---|---|
| Aduana, puerto, aeropuerto o cruce | Régimen, procedimiento, documentación, horarios y autoridad según fuente oficial aplicable. |
| País de origen, tránsito o destino | Regla de origen, tratado, medida comercial, documentación y fecha de aplicación. |
| Corredor o ruta logística | Incoterm, contrato, transporte, seguro, responsabilidades y evidencia de movimientos. |
| Recinto o infraestructura | Estatus de autorización, operador, formalidades y datos exigibles en la operación. |
| Concentración de puntos o una capa temática | Calidad, fecha, cobertura y fuente del dataset antes de realizar comparaciones. |

## Capa mundial y datos canónicos

La geometría mundial canónica se encuentra en `aduanamap-mx/data/geojson/countries-50m.geojson`. Es un **GeoJSON** derivado de Natural Earth 1:50m, normalizado para el producto y generado de forma determinista. La wiki no mantiene una segunda copia manual de ese archivo. Cuando existan datasets verificados, el mapa puede relacionar países, tratados, aduanas y secciones, puertos, aeropuertos, cruces fronterizos, recintos, RFE y rutas con páginas jurídicas u operativas. La presencia de una capa no implica por sí sola autorización, competencia o aplicabilidad normativa.

> **Criterio visual:** no se incorpora aquí un mapa de terceros sólo porque parezca detallado. Durante la revisión se localizaron imágenes no institucionales y sin procedencia reutilizable confirmada; se prefieren el contrato geoespacial del proyecto y enlaces oficiales antes que una infografía que pueda quedar desactualizada o atribuir erróneamente datos a la autoridad.

## Degradación segura

La información jurídica y documental debe seguir disponible **sin mapa**. Si el GeoJSON, MapLibre o AduanaMap no están disponibles, esta página conserva enlaces textuales hacia aduanas, instrumentos, tratados y fuentes. El mapa es una capa de exploración, no una dependencia de verdad jurídica.

## Fuentes oficiales y de referencia

[1] [ANAM, portal institucional](https://anam.gob.mx/), accesos institucionales verificados en Chrome el 16 de agosto de 2026.

[2] [Ventanilla Única](https://www.ventanillaunica.gob.mx/vucem/index.html), canal institucional para trámites de comercio exterior; confirmar el trámite, autoridad y disponibilidad al momento de uso.

[3] [`aduanamap-mx`](https://github.com/jccontrerasg08-cpu/aduanamap-mx), repositorio canónico de la capa geoespacial relacionada; consultar sus contratos y provenance para los datos disponibles.

## Ver también

[ANAM y aduanas](../wiki/aduana/anam.md) · [Proceso de despacho](../wiki/aduana/proceso-despacho.md) · [Tratados y origen](tratados-origen.md) · [Fuentes oficiales](../catalog/index.md) · [Arquitectura de decisión y evidencia](../wiki/fundamentos/arquitectura-decision-evidencia.md)
