---
title: "Explorar RGCE y anexos"
description: "Entrada temporal y documental a las RGCE 2026, Anexos 1–30, modificaciones y fuentes oficiales."
---

# RGCE y anexos

Las **RGCE 2026** deben leerse como un instrumento temporal compuesto por reglas, Anexos 1–30 y publicaciones modificatorias. Esta vista conecta el contenido operativo con su cronología y con los originales oficiales, sin copiar el texto completo de cada regla.

## Entradas principales

- [Pedimento y RGCE](../wiki/aduana/pedimento-rgce.md)
- [Catálogo oficial de RGCE](../catalog/mexico/rgce.md)
- [Biblioteca de originales](../catalog/library.md)
- [Modelo de estados y vigencia](../methodology/status-model.md)

## Publicación y preservación

Para la cronología jurídica, **SIDOF/DOF** conserva el evento de publicación. Para reproducibilidad, algunos materiales se preservan además mediante PDF oficiales de **SAT**. Cuando el repositorio declara un **equivalente oficial**, eso significa que los bytes oficiales del mismo material acotado ya están archivados; no significa que el PDF alterno sustituya a SIDOF como autoridad del evento.

Ejemplos de equivalencia documentada incluyen el cuerpo de RGCE 2026 y los PDF oficiales de SAT correspondientes a varios anexos publicados por bloques en SIDOF. Las equivalencias están declaradas de forma auditable en `data/originals/equivalents.yaml`.

## Cómo navegar

1. Parte de la regla o procedimiento operativo.
2. Identifica el instrumento y, cuando corresponda, el anexo relacionado.
3. Verifica la publicación/modificación aplicable y su fecha efectiva.
4. Consulta el original preservado o la URL oficial.
5. Usa únicamente páginas revisadas/current cuando la pregunta requiera estado jurídico vigente.

!!! warning "Publicaciones anticipadas"
    Una versión anticipada publicada para consulta no se convierte automáticamente en publicación DOF definitiva. El repositorio mantiene esa distinción en metadata y en el modelo temporal.
