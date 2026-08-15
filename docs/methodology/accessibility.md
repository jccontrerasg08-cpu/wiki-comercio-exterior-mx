---
title: Accesibilidad
description: Objetivo WCAG 2.2 AA y estrategia de pruebas automatizadas y manuales para la documentación pública.
---

# Accesibilidad

El objetivo de la interfaz pública es **WCAG 2.2 AA** en el contenido y componentes que controla el proyecto.

## Controles automatizados

El build debe verificar de forma determinista:

- idioma `es` en las páginas;
- títulos y URL canónica;
- imágenes de contenido con atributo `alt`;
- enlaces internos y fragments existentes;
- HTML válido para los patrones que genera la wiki;
- soporte CSS para `prefers-reduced-motion` cuando existan animaciones.

Estos checks detectan regresiones estructurales, pero no certifican accesibilidad completa.

## Revisión manual

Antes de cambios visuales importantes deben revisarse:

- navegación sólo con **teclado**;
- foco visible y orden lógico;
- zoom 200% y 400%;
- **reflow** sin pérdida de información;
- contraste de texto, controles y estados;
- lectura por landmarks, headings y nombres accesibles;
- comportamiento de tablas en pantallas pequeñas;
- modo claro/oscuro y preferencia de movimiento reducido.

## Contenido

Las tablas necesitan encabezados claros. Los enlaces deben describir su destino. El color no debe ser el único mecanismo para comunicar estado. Las abreviaturas globales ayudan a reducir carga cognitiva, pero una página compleja también debe explicar el concepto al primer uso cuando sea necesario.

## Responsabilidad

Una prueba automatizada verde no equivale a “WCAG certificado”. Los hallazgos manuales se tratan como deuda verificable y deben documentarse cuando no puedan resolverse en el mismo cambio.

## Ver también

[Política editorial](editorial-policy.md) · [Arquitectura](../ARCHITECTURE.md)
