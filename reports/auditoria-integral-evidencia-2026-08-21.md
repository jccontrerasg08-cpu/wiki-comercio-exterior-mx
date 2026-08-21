# Evidencia de auditoría integral — 21 de agosto de 2026

## Vista previa local: explorador mundial

**URL auditada:** `/explore/mundo/` de la compilación local generada con `mkdocs build --strict`.

La revisión visual en navegador confirmó que el encabezado **“Filtros de guías de país”** es visible antes de los controles Región y Buscar país o código ISO3. Los controles conservan etiquetas legibles y la tabla muestra sus cuatro columnas, encabezados y filas de las siete guías curadas sin un error de carga. La tabla se mantiene como fuente primaria de lectura y el bloque explica que no representa serie estadística, arancel, recaudación ni relación jurídica por sí solo.

La observación corresponde a una vista de escritorio en modo oscuro. Queda pendiente una comprobación manual con viewport móvil real, contraste calculado y lector de pantalla; la corrección aplicada elimina el ancho mínimo móvil fijo y añade agrupación nativa de filtros, pero no constituye una certificación WCAG.

## Vista previa local: tablero de recaudación ANAM

**URL auditada:** `/wiki/aduana/recaudacion-anam/` de la misma compilación local.

El navegador confirmó que el tablero carga los datos locales y muestra el grupo **“Filtros del tablero de recaudación”**, las opciones de Indicador y Vista, el estado en vivo y la métrica de Recaudación Q2 de **336,190 MDP** con su comparación publicada. La serie enero–junio se renderizó con los seis valores ya documentados en el conjunto de datos. No se observó estado de error de carga ni pérdida del bloque editorial que explica el alcance y la fuente primaria.

Esta comprobación acredita presentación y carga en escritorio, no autenticidad jurídica adicional de los valores ni conformidad WCAG formal. Los valores siguen limitados al Informe Trimestral Q2 2026 de ANAM y a los metadatos de procedencia de la wiki.
