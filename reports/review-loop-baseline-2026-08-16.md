# Línea base de revisión iterativa

Fecha: 2026-08-16.

## Criterio operativo de calidad

Cada página debe distinguir claramente entre explicación propia, fuente oficial, herramienta operativa y límite de la afirmación. Las afirmaciones que dependan de una fecha, excepción, cantidad, requisito o condición deben llevar el fundamento cerca del texto o en una sección de fuentes inequívoca. El formato editorial preferido es una cita numérica enlazada en el cuerpo —`[1]`— y una lista de referencias al final con título, autoridad, URL y fecha de consulta cuando la fuente sea mutable.

| Dimensión | Regla de revisión |
|---|---|
| Fuente | Priorizar publicación DOF/SIDOF, texto oficial consolidado o autoridad competente; no usar portal operativo para afirmar vigencia jurídica. |
| Tiempo | Distinguir publicación, entrada en vigor, modificación posterior y `current_through`. |
| Afirmación | Evitar absolutos sin excepción; explicar el supuesto y el límite. |
| Navegación | Toda página sustantiva debe enlazar a fuentes y a páginas relacionadas; cada enlace interno debe resolver en el sitio generado. |
| Presentación | Usar imagen o diagrama sólo cuando mejora comprensión, con texto alternativo, leyenda y procedencia. |
| Código | Todo control nuevo debe tener una prueba de regresión y no relajar validadores existentes. |

## Estado observado

La rama de trabajo está limpia y la PR #40 tiene estado de integración `CLEAN`. Las métricas de cobertura y recuperación están en verde; el único registro de fuente desconocida corresponde de forma intencional al fixture no autoritativo `data/corpus/requisitos-pais-ejemplo.csv`.

La auditoría visible detectó siete páginas públicas que no contienen una URL HTTP directa y numerosas páginas que aún emplean listas de fuentes sin citas numéricas dentro del cuerpo. Esto no significa que carezcan necesariamente de trazabilidad en metadatos, pero sí que son candidatas prioritarias para uniformar el formato de referencia orientado al lector. Las primeras páginas prioritarias son `regimenes-aduaneros.md`, `impuestos-importacion.md`, `marco-juridico.md`, `drawback.md`, `anexo-2-2-1.md`, `anexo-2-4-1.md` e `rrna/index.md`.

## Hallazgo técnico prioritario

El verificador de sitio valida títulos, idioma, canonicals, texto alternativo y fragmentos de enlaces, pero no detecta actualmente un enlace local roto cuando no contiene fragmento. Debe añadirse un control de ruta y una prueba que reproduzca el fallo, porque el usuario pidió que toda la wiki permanezca conectada y enlazada correctamente.

## Inspección visual inicial

La portada renderizada muestra una jerarquía clara: propuesta de valor, recorrido en cinco pasos, accesos por problema y sección de verificabilidad. La navegación expuesta bajo la ruta pública del proyecto resuelve hacia páginas de clasificación, RRNA, contribuciones, despacho, logística y catálogo. La inspección de contenido renderizado confirma que los enlaces absolutos del subdirectorio público se generan como se espera.

La consulta de vista detallada en Chrome recibió un tiempo de espera de la extensión después de una navegación satisfactoria. Se continuará la revisión visual mediante navegación directa de páginas clave y las validaciones de sitio compilado; no se tratará ese error transitorio como fallo del contenido o de la compilación.

La navegación directa de la guía de RRNA confirmó que el diagrama local se sirve correctamente, conserva texto alternativo y aparece antes de la tabla que explica. Las tablas y los vínculos visibles resuelven bajo el subdirectorio público esperado. Se detectó, sin embargo, un problema de presentación: la salida renderizada expande automáticamente siglas de manera repetitiva —por ejemplo, `RRNA (Regulaciones y restricciones no arancelarias)` y `SNICE (Servicio Nacional de Información de Comercio Exterior)` aun cuando el texto ya las definía—. Esta repetición reduce fluidez, alarga tablas y se debe revisar en configuración o marcado antes de editar el texto de cada página.

La captura visual de Chromium descartó que las siglas se expandan de forma intrusiva en la interfaz: se muestran como abreviaturas legibles con subrayado de ayuda, mientras que la expansión repetida provenía de la extracción textual del navegador. El diagrama se presenta con buen contraste y orden semántico antes de la tabla de fuentes; la tabla conserva encabezados, alineación y legibilidad a 1440 px. No se justifica modificar el diccionario de abreviaturas por este hallazgo.

La captura de la biblioteca de instrumentos confirma que el banner institucional mantiene proporción, contraste y anchura apropiada dentro del área de lectura. La leyenda queda inmediatamente debajo y conserva su advertencia de alcance. Las tablas de fichas de disponibilidad se alinean con el ancho de texto, los encabezados son distinguibles y la navegación lateral y la tabla de contenidos conservan jerarquía. No se detectó un ajuste visual prioritario en esta página a 1440 px.
