---
title: Mapa de la wiki
description: Ruta de consulta por clasificación, RRNA, contribuciones, despacho, programas y logística en el comercio exterior mexicano.
---

# Wiki Comercio Exterior MX

Esta wiki está organizada para resolver una operación, no para memorizar un índice legal. Empieza por identificar **qué mercancía es, qué régimen se pretende utilizar, quién interviene y qué fecha gobierna la operación**. Después sigue la ruta de clasificación, regulaciones, contribuciones y despacho. Si necesitas primero entender cómo se conectan norma, datos, transmisión y expediente, consulta [Arquitectura de decisión y evidencia](fundamentos/arquitectura-decision-evidencia.md).

## Empieza por la decisión

### 1. Clasificar la mercancía

La clasificación conecta el Sistema Armonizado con la fracción mexicana de ocho dígitos y, cuando corresponde, el NICO. Consulta [Sistema Armonizado](clasificacion/sistema-armonizado.md) y [TIGIE y NICO](clasificacion/tigie-nico.md).

La wiki explica el contexto; la capa estructurada de fracciones pertenece a [`arancel-mx`](https://github.com/jccontrerasg08-cpu/arancel-mx).

### 2. Revisar RRNA y padrones

Una tasa arancelaria no prueba que la mercancía pueda entrar o salir sin otras condiciones. Usa la [Guía de RRNA](rrna/index.md), [Ciclo de vida de una RRNA](rrna/ciclo-de-vida-rrna.md), [Anexo 2.2.1](rrna/anexo-2-2-1.md), [Anexo 2.4.1](rrna/anexo-2-4-1.md) y [Padrón de Importadores](fundamentos/padron-importadores.md).

Como regla general, determina primero si la operación cae en la obligación y después revisa excepciones, autorizaciones y vigencia del instrumento.

### 3. Determinar valor y contribuciones

Para importación, separa la tasa de IGI del **valor en aduana** y de obligaciones distintas como cuotas compensatorias. Recorre [Valor en aduana](contribuciones/valor-en-aduana.md), [Aranceles](contribuciones/aranceles.md), [Lectura de la tarifa y tratamientos](contribuciones/lectura-tarifa-y-tratos.md), [Impuestos de importación](contribuciones/impuestos-importacion.md) y [Cuotas compensatorias](contribuciones/cuotas-compensatorias.md).

### 4. Preparar el despacho

[Proceso de despacho](aduana/proceso-despacho.md) integra clasificación, RRNA, valor, documentos, pedimento, validación y eventos posteriores. Para piezas específicas consulta [Documentos](aduana/documentos.md), [Manifestación de Valor](aduana/manifestacion-valor.md), [Pedimento y RGCE](aduana/pedimento-rgce.md) y [Ventanilla Única y VUCEM](aduana/vucem.md).

Si una incidencia activa una causal legal, [PAMA e infracciones](aduana/infracciones-pama.md) explica cómo distinguir una irregularidad de un supuesto de embargo precautorio.

### 5. Conservar evidencia y reconciliar cambios

Después del despacho, enlaza cada decisión con sus soportes, acuses y cambios posteriores. Consulta [Trazabilidad de evidencia](operacion/trazabilidad-evidencia.md) y [Reconciliación y control de cambios](operacion/reconciliacion-control-cambios.md) para estructurar esa revisión sin confundir un acuse con la comprobación sustantiva del requisito.

### 6. Aplicar programas, origen y logística

Cuando la operación utilice un programa o preferencia, revisa [IMMEX](programas/immex.md), [PROSEC](programas/prosec.md), [Drawback](programas/drawback.md), [TLC y T-MEC](programas/tlc-tmec.md) y [Reglas de origen](programas/reglas-de-origen.md).

Para la capa comercial/logística consulta [Incoterms®](logistica/incoterms.md), [Logística internacional](logistica/logistica-internacional.md) y [Pagos internacionales](logistica/pagos-internacionales.md), recordando que esas figuras no sustituyen las obligaciones aduaneras mexicanas.

## Consulta los documentos prioritarios

La [Biblioteca de instrumentos prioritarios](fundamentos/biblioteca-instrumentos-prioritarios.md) reúne rutas oficiales a LIGIE/TIGIE, Ley Aduanera, RGCE y Anexo 22, Ley y Reglamento de Comercio Exterior, Reglas y criterios SE, anexos de RRNA, T-MEC, IMMEX, PROSEC y Drawback. La biblioteca explica el propósito de cada documento y la diferencia entre publicación jurídica, texto consolidado y herramienta operativa.

## Revisa la fecha

El comercio exterior cambia por decretos, resoluciones, anexos y modificaciones. [Cambios 2026](aduana/cambios-2026.md) resume eventos recientes, pero cada operación debe verificarse contra la publicación y sus transitorios.

## ¿Qué falta?

El [Roadmap de contenido](../status/content-roadmap.md) separa lo cubierto, parcial y pendiente. El catálogo reproducible de fuentes vive en `docs/catalog/` y puede recorrerse desde la [Guía del catálogo](../catalog/index.md). El [Estado del corpus](../status/corpus-coverage.md) muestra gobernanza y preparación para recuperación; **no es un porcentaje de certeza jurídica**.

> La wiki organiza conocimiento para consulta y estudio. Cuando una afirmación cambie una decisión real, sigue el enlace hasta la **fuente oficial** y verifica la vigencia aplicable.

**No es asesoría legal.** Verifica la fuente oficial y la vigencia aplicable antes de tomar una decisión operativa.
