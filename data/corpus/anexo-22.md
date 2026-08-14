# Anexo 22 — Instructivo para el Llenado del Pedimento (RGCE 2026)

**Fuente oficial:** SAT / DOF 15-01-2026
**Fundamento:** Arts. 2o. fracc. XVI, 6o., 36, 36-A, 37, 37-A y 39 de la Ley Aduanera; art. 6o. del Reglamento; regla 3.1.41. RGCE 2026
**URL oficial (PDF completo):** https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/documentos2026/rgce/anexos/Anexo22delasRGCEpara2026.pdf
**Vigencia diferida (Transitorio Segundo RGCE 2026):** El **Apéndice 1 (Aduana-Sección)** y el **Apéndice 6 (Recintos Fiscalizados)** del Anexo 22 entraron en vigor el **2 de febrero de 2026** (no el 01-01-2026), por la reestructura de secciones aduaneras (Dos Bocas, Tijuana, etc.).

## Estructura del Anexo 22

**Sección I — Campos del pedimento** (más de 60 campos)
**Sección II — Apéndices** (catálogos de claves)

## Apéndices del Anexo 22

| Apéndice | Contenido |
|---|---|
| 1 | Aduana-Sección (claves de 3 posiciones) |
| 2 | Claves de pedimento (tipo de operación) |
| 3 | Medios de transporte |
| 4 | Claves de países |
| 5 | Claves de monedas |
| 6 | Recintos fiscalizados |
| 7 | Unidades de medida |
| 8 | Identificadores (claves que activan obligaciones específicas: RRNA, NOMs, permisos, etc.) |
| 13 | Pagos (referenciado en rectificaciones que generan pago de lo indebido) |
| 15 | Destino/Origen |
| (otros) | Numerados según la sección del pedimento |

**Apéndice 8 — "clave de constancia" (nueva 2026):** pendiente de publicar para el régimen RFE (regla 1.6.37. RGCE 2026).

## Campos principales del pedimento

| Campo | Descripción |
|---|---|
| NÚM. PEDIMENTO | 15 dígitos: 2 (año) + 2 (aduana) + 1 (tipo) + 4 (agente/importador) + 6 (consecutivo). Numeración inicia en 000001 por año. |
| CVE. PEDIMENTO | Clave del tipo de operación (Apéndice 2): importación definitiva, temporal, tránsito, etc. |
| TIPO DE OPERACIÓN | Leyenda: "Importación", "Exportación", etc. No se llena en pedimentos complementarios ni tránsito internacional. |
| DESTINO/ORIGEN | Clave que identifica destino (importación/tránsito interno) u origen (exportación) — Apéndice 15. |
| TIPO CAMBIO | Tipo de cambio peso-dólar vigente a la fecha del art. 56 LA (fondeo/cruce/arribo aeronave). No se llena en pedimentos complementarios, tránsitos internos a la importación ni tránsitos internacionales ferroviarios. |
| CLAVE SECCIÓN ADUANERA DE DESPACHO | 3 posiciones (Apéndice 1). En tránsitos = aduana/sección de inicio. No se llena en pedimentos complementarios. |
| MARCAS, NÚMEROS Y TOTAL DE BULTOS | Identificación física del embarque. No se llena en pedimentos complementarios. |
| RFC / RAZÓN SOCIAL / DOMICILIO | De importador, exportador, agente/agencia aduanal. Para extranjeros sin RFC: EXTR920901TS4. |
| FECHA DE ENTRADA | Fecha real de cruce/fondeo/arribo, conforme al art. 56 LA. |
| FRACCIÓN ARANCELARIA | 8 dígitos de la TIGIE. |
| NICO | 2 dígitos adicionales (10 en total). Obligatorio conforme a la Regla Complementaria 10a. de la LIGIE. |
| IDENTIFICADORES (Apéndice 8) | Claves alfanuméricas que activan obligaciones específicas (NOM, permiso previo, certificado de origen, precio estimado, etc.) |
| VALOR EN ADUANA | En USD o en la moneda de la transacción con el tipo de cambio declarado. |
| NÚMERO DE PEDIMENTO | De importación/exportación relacionado (para rectificaciones, desistimientos, cambios de régimen). |

## Cambios al Anexo 22 en 2026

- **Nuevas claves de aduanas** por reestructura: secciones de Tijuana (Mesa de Otay, El Chaparral, Puerta México Este) documentadas explícitamente; creación de la Aduana 83 Dos Bocas con sus secciones (Villahermosa, El Ceibo, Nuevo Orizaba-Ingenieros).
- **Pendiente (Apéndice 8):** La clave de constancia para el RFE (regla 1.6.37.) aún no ha sido publicada en el Apéndice 8 al momento de la publicación del Anexo 22 (enero 2026).
- El **formato del pedimento** en sí no cambió — solo se actualizaron los catálogos de claves.

## Lógica para el chatbot

Para responder preguntas sobre llenado del pedimento:
1. Identificar si es pregunta sobre un **campo** (Sección I) o una **clave de catálogo** (Sección II, apéndices).
2. El Apéndice 2 (claves de pedimento) y el Apéndice 8 (identificadores) son los más consultados operativamente.
3. El Apéndice 1 (aduana-sección) es crítico para verificar la clave de 3 posiciones — especialmente relevante para las nuevas secciones de Tijuana y la aduana Dos Bocas (2026).
4. Para clave de fracción arancelaria/NICO → cruzar con `tigie-nico-notas.md`.
5. Para identificadores que activan NOMs/permisos → cruzar con `noms-comercio-exterior.md`.
