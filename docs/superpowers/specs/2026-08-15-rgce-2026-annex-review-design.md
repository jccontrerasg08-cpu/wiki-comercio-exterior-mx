# RGCE 2026 Annex Review Design

**Fecha de revisión:** 2026-08-15

## Objetivo

Remediar los 32 digests locales relacionados con los Anexos 1–30 de las RGCE 2026 para que el repositorio pueda distinguir correctamente entre:

- vigencia de la fuente oficial;
- cobertura de extracción;
- revisión jurídica del contenido incluido;
- elegibilidad del digest para respuestas actuales.

El resultado debe mejorar el corpus sin convertir una extracción parcial en una falsa afirmación de exhaustividad.

## Decisión de diseño

Se eligió **reescritura conservadora + manifest por anexo + revisión humana documentada**.

### Alternativa descartada A: actualizar sólo metadata

Ventaja: menor diff. Desventaja: mantendría afirmaciones incorrectas ya detectadas, por ejemplo una supuesta modificación anticipada del Anexo 1 y referencias a una “segunda modificación” de Anexos 5/29 que en realidad fueron versiones anticipadas de la primera modificación. Cambiar estados sin corregir texto violaría el modelo de gobernanza.

### Alternativa descartada B: importar el texto completo de los anexos

Ventaja: máxima cobertura literal. Desventajas: duplicaría grandes tablas del DOF/SAT, aumentaría considerablemente el repositorio, complicaría consolidaciones posteriores y difuminaría la función de la wiki como capa explicativa verificable.

### Alternativa seleccionada

Cada digest será un resumen actual, breve y source-bounded. Debe declarar que no reproduce el anexo completo, explicar qué pregunta operativa responde, indicar publicación/modificaciones aplicables y remitir al DOF/SAT para listas, tablas, apéndices o formatos exhaustivos.

## Fuentes oficiales y mapa de publicación

El portal oficial de Normatividad SAT 2026 se usa como índice de estado y DOF/SIDOF como autoridad primaria.

| Anexo | Publicación primaria | Fuente registrada |
|---|---|---|
| 1 | 2026-01-08 | `mx_sidof_rgce_2026_anexo_1` |
| 2 | 2026-01-12 | `mx_sidof_rgce_2026_anexo_2` |
| 3–12, 14–20 | 2026-01-14 | `mx_sidof_rgce_2026_anexos_3_20` |
| 13 | RGCE publicada 2025-12-27, efectiva 2026 | `mx_sidof_rgce_2026` |
| 21–30 | 2026-01-15 | `mx_sidof_rgce_2026_anexos_21_30` |
| 5, 22, 29 — 1ra modificación | publicación 2026-05-20 | `mx_sidof_rgce_2026_mod1_anexos` |

La Primera Resolución de Modificaciones a las RGCE 2026 fue publicada el 2026-05-14. Sus transitorios establecen reglas de entrada en vigor diferenciadas; las modificaciones de Anexos 5 y 29 se vinculan a la publicación de la modificación del Anexo 29, realizada el 2026-05-20. La clave AL del Apéndice 9 del Anexo 22 tiene una regla especial ligada al acuerdo de Secretaría de Economía del 2026-04-02.

## Versiones anticipadas

Una versión anticipada no se modela como publicación DOF ni promueve currentness jurídica.

Al corte del 2026-08-15:

- SAT muestra una versión anticipada asociada a la futura modificación del Anexo 2 dentro de la 2da RMRGCE 2026;
- las versiones anticipadas que precedieron la 1ra modificación de Anexos 5 y 29 no son una “segunda modificación”; la publicación jurídica relevante es la primera modificación de 2026-05-20;
- no se afirmará una modificación publicada para anexos que el índice SAT sólo presente en la sección de anticipadas.

## Manifest de anexos

Crear `sources/rgce_2026_annexes.yaml` como inventario editorial, no como fuente jurídica independiente. Tendrá exactamente 30 registros con:

- `annex`;
- `title` oficial;
- `publication_source_id`;
- `publication_date`;
- `modification_source_ids` cuando existan;
- `reviewed_through`;
- `corpus_path`.

El manifest no cambia por sí mismo `legal_review_status`. Su función es hacer visibles inconsistencias y evitar que un archivo apunte al bundle incorrecto o omita una modificación publicada.

## Estados tras la revisión

Para los 30 digests individuales y los dos digests compuestos:

- `source_status: current`: sólo si se verificó que las fuentes oficiales registradas son las aplicables al corte;
- `extraction_status: partial`: se mantiene, porque el digest no reproduce todas las tablas/listados/texto;
- `legal_review_status: reviewed`: permitido porque un humano revisó todas las afirmaciones conservadas en el resumen contra el estado oficial;
- `corpus_status: current`: permitido aunque la extracción sea parcial, ya que “current” significa que el contenido incluido puede citarse como actual, no que sea exhaustivo;
- `current_through`: 2026-05-20 para reflejar que se revisó el alcance completo de la primera modificación y se confirmó qué anexos fueron o no afectados.

Esta combinación es coherente con el modelo de estados: una extracción parcial puede ser jurídicamente revisada y actual si su alcance está claramente delimitado.

## Reescritura de los digests

Cada anexo tendrá esta estructura:

1. título oficial;
2. estado al corte y fuente primaria;
3. objeto/alcance, limitado a lo verificable por el título y texto oficial;
4. uso operativo: qué pregunta ayuda a resolver;
5. modificaciones 2026, si aplica;
6. límites: no reemplaza tablas/listados/apéndices/formatos oficiales;
7. relación con otras páginas de la wiki cuando sea útil.

### Reglas de redacción

- no usar “chatbot logic”, árboles de decisión absolutos ni consecuencias automáticas;
- no inventar multas, PAMA, sanciones o prohibiciones más amplias que el texto;
- no copiar listas arancelarias extensas; remitir a la fuente y a `arancel-mx` cuando corresponda;
- no transformar una versión anticipada en derecho vigente;
- no decir “sin cambios” basándose sólo en que el archivo PDF tenga el mismo nombre; la comprobación se hace contra el índice SAT y los actos DOF publicados;
- no usar un compilado SAT como sustituto de la publicación DOF para establecer vigencia.

## Corrección temporal del grafo

Cambiar el evento `mx_sidof_rgce_2026_mod1_anexos` de `2026-05-22` a `2026-05-20`, fecha de publicación DOF de las modificaciones a Anexos 5, 22 y 29.

El evento sigue siendo `has_annex`: representa la nueva manifestación publicada de esos anexos. Las reglas de entrada en vigor específicas del contenido se documentan en los digests y no se reducen a una única fecha genérica cuando el transitorio distingue supuestos.

## Digests compuestos

### `anexos-formatos-tramites.md`

Debe explicar que sintetiza Anexos 1 y 2, que ambos tienen publicaciones separadas y que la versión anticipada del Anexo 2 no se trata como una modificación publicada.

### `anexos-riesgo-logistica.md`

Debe funcionar como mapa temático de los Anexos 3–30 que se relacionan con despacho, tránsito, padrones, mercancías sensibles, restricciones de régimen y controles; no debe crear obligaciones nuevas ni sustituir los anexos individuales.

## Validación automatizada

Crear `scripts/rgce_annexes.py` y tests que verifiquen:

- exactamente 30 anexos, sin duplicados ni huecos;
- título y `corpus_path` únicos;
- source IDs existentes;
- sólo 5, 22 y 29 tienen `mx_sidof_rgce_2026_mod1_anexos` como modificación publicada al corte;
- Anexo 2 no tiene una modificación publicada en el manifest;
- todos los digests gobernados tienen metadata;
- los 32 registros de metadata quedan `current/reviewed/current` con extracción `partial` y `current_through: 2026-05-20`;
- no reaparecen frases de riesgo conocidas como “2da Modificación” aplicada a anticipadas, “puede destinarse” de forma absoluta, o consecuencias sancionadoras automáticas.

## Cobertura y RAG

Al promover los digests revisados a `corpus_status: current`, el RAG puede incorporar su texto. La mejora de grouped-source retrieval de Wave 3 permite que una fuente bundle como “Anexos 21–30” se recupere por títulos individuales sin cambiar la cita oficial.

Se añadirán evals representativas, no una pregunta por cada anexo. Deben cubrir al menos:

- Anexo 1 formatos;
- Anexo 2 trámites y anticipada no publicada;
- Anexo 5 criterio modificado;
- Anexo 13 multas/cantidades;
- Anexo 22 pedimento;
- Anexo 29 regímenes;
- Anexo 30 SCCCyG.

## Gates de finalización

1. tests completos;
2. validator;
3. catálogo generado;
4. page metadata;
5. coverage policy/dashboard, sólo ratchet positivo;
6. temporal graph;
7. RAG eval;
8. MkDocs strict;
9. route/site verifier;
10. Dependency Review;
11. CI de PR verde en el SHA final;
12. squash merge;
13. CI de `main` y Pages verdes sobre el merge SHA.

## Fuera de alcance

Esta ola no reescribe todavía los otros corpus (`ley-aduanera`, `noms-comercio-exterior`, etc.) ni las 19 páginas wiki pendientes. Esos elementos se integrarán en la siguiente PR desde `main` actualizado, junto con los fixes útiles rescatados de la PR #35 cerrada.
