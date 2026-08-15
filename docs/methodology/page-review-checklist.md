---
title: Checklist de revisión jurídica
description: Evidencia mínima necesaria antes de promover una página de pending_review a reviewed en la wiki.
---

# Checklist de revisión jurídica

Una edición puede mejorar una página sin convertirla en jurídicamente revisada. El cambio de `pending_review` a `reviewed` requiere una revisión explícita.

## Antes de promover a `reviewed`

- [ ] Se identificó el instrumento jurídico correcto.
- [ ] Se consultó la publicación oficial o una manifestación oficial adecuada.
- [ ] Se verificó la fecha de publicación.
- [ ] Se revisaron transitorios y fecha efectiva.
- [ ] Se buscaron reformas o modificaciones posteriores hasta `current_through`.
- [ ] Se distinguió texto consolidado de eventos modificatorios.
- [ ] Se revisaron excepciones materialmente relevantes.
- [ ] Las afirmaciones absolutas están justificadas o fueron convertidas en lenguaje condicional.
- [ ] `source_ids` apunta a fuentes registradas.
- [ ] `instrument_ids` apunta a instrumentos conocidos cuando la página trata una norma.
- [ ] La sección de fuentes permite al lector llegar a la evidencia oficial.
- [ ] La página indica límites cuando una herramienta o portal no prueba vigencia jurídica.
- [ ] Se ejecutaron los validadores temporal, provenance y RAG correspondientes.

## `current_through`

`current_through` registra hasta qué fecha efectiva se revisaron eventos conocidos para la página. **No es** la fecha de descarga, el último commit ni el día en que un endpoint respondió correctamente.

## Qué no basta

No es suficiente para marcar `reviewed`:

- cambiar ortografía;
- agregar una metadescripción;
- comprobar que un enlace devuelve 200;
- copiar una explicación de otra página;
- encontrar un documento sin revisar sus transitorios;
- hacer que una prueba sintáctica pase.

## Regresiones

Si aparece un nuevo evento jurídico posterior al `current_through`, la página puede requerir revisión o degradación de su elegibilidad para respuestas actuales. El sistema debe preferir abstenerse a presentar como vigente una síntesis que quedó atrás.

## Ver también

[Política editorial](editorial-policy.md) · [Política de citas](citation-policy.md) · [Estado del corpus](../status/corpus-coverage.md)
