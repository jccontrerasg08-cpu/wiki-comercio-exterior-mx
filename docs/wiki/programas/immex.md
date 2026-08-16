---
title: "IMMEX"
description: "Guía operativa del Programa IMMEX: importación temporal, control de inventarios, retornos, Anexo 24, SCCCyG y reporte anual."
---

# IMMEX

El **Programa para el Fomento de la Industria Manufacturera, Maquiladora y de Servicios de Exportación (IMMEX)** permite realizar importaciones temporales vinculadas a procesos de elaboración, transformación, reparación o servicios de exportación, bajo las condiciones del Decreto IMMEX, la Ley Aduanera y las reglas aplicables.

No basta con identificar una empresa como “IMMEX” para concluir qué plazo, beneficio o sistema de control le corresponde. La mercancía, el régimen, el tipo de operación, la certificación de la empresa y la regla aplicable cambian el análisis.

## Ruta operativa

Una operación típica debe poder reconstruirse documentalmente desde la autorización y la entrada temporal hasta su salida o regularización:

1. **Autorización y mercancía.** Verificar que la operación esté dentro del Programa IMMEX autorizado y que la mercancía no caiga en una restricción o condición especial.
2. **Importación temporal.** Declarar correctamente pedimento, fracción arancelaria, NICO cuando corresponda, identificadores y demás datos exigibles.
3. **Control de inventarios.** Vincular la entrada aduanera con materiales, productos, procesos, salidas y saldos conforme al [Anexo 24](anexo-24-control-inventarios.md).
4. **Destino de la mercancía.** Documentar retorno, transferencia, destrucción, donación, cambio de régimen u otro destino jurídicamente procedente.
5. **Plazo.** Computarlo conforme al tipo de mercancía y al fundamento aplicable; no existe un único plazo IMMEX que sustituya el análisis de la Ley Aduanera, el Decreto y las RGCE.

Para el detalle arancelario conviene consultar la fuente oficial y la capa estructurada de `arancel-mx`; esta wiki no duplica listados completos de fracciones.

## Anexo 24: control de inventarios

El artículo 24, fracción IX del Decreto IMMEX obliga a llevar un control automatizado de inventarios conforme a las disposiciones del SAT. El Anexo 24 de las RGCE 2026 desarrolla la información mínima del sistema y distingue **tres apartados con alcances diferentes**.

Por eso, Anexo 24 no debe usarse como sinónimo de SECIIT. El SECIIT corresponde al supuesto específico del apartado B; los apartados A y C tienen estructuras y obligaciones propias. Consulta [Anexo 24: control de inventarios](anexo-24-control-inventarios.md).

## Anexo 30: SCCCyG

El [Anexo 30: SCCCyG](anexo-30-scccyg.md) regula información del **Sistema de Control de Cuentas de Créditos y Garantías**. Su función es distinta del control físico-documental del Anexo 24: se relaciona con cuentas de créditos fiscales y garantías dentro de los supuestos que las RGCE vinculan al sistema.

El SCCCyG **no aplica automáticamente** a toda empresa u operación IMMEX; ser titular de un Programa IMMEX, por sí solo, no determina su aplicación. Primero se identifica el esquema fiscal/certificación y la regla que genera la cuenta de cargo o el descargo.

## Reporte anual y aviso 2026

El artículo 25 del Decreto IMMEX prevé un **reporte anual electrónico** respecto del ejercicio inmediato anterior, a más tardar el último día hábil de mayo, conforme a los términos aplicables.

El aviso publicado en el DOF el **30 de junio de 2026** identificó programas suspendidos por no haber presentado el reporte correspondiente al ejercicio 2025. Ese aviso establece, para ese ciclo, que quienes subsanen a más tardar el **último día hábil de agosto de 2026** pueden obtener el levantamiento de la suspensión; si no se regulariza, la cancelación definitiva opera a partir del **1 de septiembre de 2026**. Esta fecha es propia del aviso 2026 y no debe reutilizarse como calendario permanente para otros ejercicios.

## Reformas recientes

El Decreto IMMEX fue reformado el **19 de diciembre de 2024** y nuevamente el **28 de agosto de 2025**. Ambos decretos dispusieron entrada en vigor al día siguiente de su publicación. La reforma de agosto de 2025 modificó, entre otros elementos, el Anexo I del Decreto IMMEX.

Cuando una decisión dependa de una fracción concreta, se debe revisar el texto oficial vigente y su fecha efectiva; una lista copiada en una guía puede quedar desactualizada.

## Cómo verificar una operación

Antes de concluir que una operación cumple, conviene cruzar al menos:

- autorización/programa y modalidad IMMEX;
- fracción arancelaria y NICO aplicables;
- pedimentos de entrada y salida vinculados;
- plazo legal de permanencia;
- registros y descargos del Anexo 24;
- certificación o garantía fiscal cuando pueda activar SCCCyG;
- reformas y reglas vigentes para la fecha de la operación.

## Fuentes

- Catálogo interno de fuentes: `docs/catalog/mexico/rgce.md`
- [SNICE — Programa IMMEX](https://www.snice.gob.mx/cs/avi/snice/immex.html)
- [DOF/SIDOF — reforma IMMEX del 19 de diciembre de 2024](https://sidof.segob.gob.mx/notas/5745788)
- [DOF/SIDOF — reforma IMMEX del 28 de agosto de 2025](https://sidof.segob.gob.mx/notas/5766797)
- [DOF/SIDOF — aviso de programas IMMEX suspendidos, 30 de junio de 2026](https://sidof.segob.gob.mx/notas/5792091)
- [DOF/SIDOF — RGCE 2026](https://sidof.segob.gob.mx/notas/5777199)
- [DOF/SIDOF — Anexos 21 a 30 de las RGCE 2026](https://sidof.segob.gob.mx/notas/5778300)

## Alcance de la guía

No es asesoría legal. Para una operación concreta deben revisarse los hechos, documentos, fechas y disposiciones vigentes aplicables.

## Vigencia

Revisión editorial/jurídica efectuada el **15 de agosto de 2026**. El grafo local del Decreto IMMEX sigue marcado como `partial` porque todavía no versiona individualmente todas las reformas históricas; esta página no se usa por sí sola como documento temporal “current” del RAG.

## Ver también

[Anexo 24](anexo-24-control-inventarios.md) · [Anexo 30](anexo-30-scccyg.md) · [Pedimento y RGCE](../aduana/pedimento-rgce.md) · [TIGIE y NICO](../clasificacion/tigie-nico.md) · [PROSEC](prosec.md)
