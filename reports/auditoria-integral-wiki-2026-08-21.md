---
title: "Auditoría integral de la wiki — 21 de agosto de 2026"
description: "Resultado verificable de una auditoría de arquitectura, contenido, datos, accesibilidad, experiencia, seguridad y mantenibilidad."
---

# Auditoría integral de la wiki

Esta auditoría examinó la arquitectura estática, las rutas de navegación, los contratos de datos, los dashboards, el explorador mundial, los catálogos, las fuentes, los scripts, las pruebas, la superficie de seguridad y los límites de integración entre repositorios. El resultado no es un dictamen jurídico ni una certificación WCAG: separa lo confirmado por ejecución de lo que requiere revisión editorial, jurídica, asistiva o de producto.

## Resultado ejecutivo

| Área | Estado al cierre | Evidencia principal |
|---|---|---|
| Integridad del repositorio | Correcta | `validate_repository`, catálogos, metadatos, originales y grafo temporal superaron sus controles. |
| Pruebas y builds | Correctos | 191 pruebas unitarias correctas; build estricto, sitio normal y sitio offline verificados. |
| Navegación y enlaces | Corregida | La página histórica IMMEX/Anexos 24–30 quedó incorporada a la navegación; los anclajes del catálogo se ajustaron a los IDs generados por MkDocs. |
| Dashboard ANAM | Corregido y comprobado | El renderizado ya no interpreta datos JSON como HTML; navegador local confirmó filtros, métrica y serie publicados. |
| Explorador mundial | Corregido y comprobado | Los filtros ahora usan `fieldset`/`legend`; el ancho mínimo móvil fijo se eliminó y la tabla mantiene una ruta textual primaria. |
| Catálogo editorial | Corregido | El índice visible se unificó al español, conservando sus referencias técnicas y rutas. |
| Seguridad estática | Parcialmente cubierta | Seis reglas Semgrep completaron; tres reglas externas/YAML no completaron por incompatibilidad de reglas. El único hallazgo fusionado fue un falso positivo sobre `_date_yyyymmdd`. |
| Cobertura editorial | Pendiente prioritaria | La política de corpus reporta 80 páginas gobernadas, 17 elegibles y 59 pendientes; no se debe interpretar la navegación como sinónimo de contenido vigente revisado. |

## Correcciones aplicadas

| Hallazgo reproducible | Corrección mínima | Guarda de regresión |
|---|---|---|
| Campos de datos ANAM se interpolaban mediante `innerHTML` | El dashboard construye nodos DOM y usa `textContent`; sólo los números controlados definen el ancho de barras. | `test_dashboard_script_renders_dataset_text_without_html_interpolation`. |
| Filtros sin agrupación semántica explícita | Los filtros de ANAM y del explorador mundial ahora usan `fieldset` con `legend`. | Contratos específicos de dashboard y explorador. |
| Tabla mundial forzaba ancho mínimo en móvil | En el breakpoint móvil usa `width: 100%`, `min-width: 0`, `table-layout: fixed` y división de palabras. | `test_world_explorer_groups_filters_and_reflows_on_mobile`. |
| Índice del catálogo con mezcla editorial de inglés y español | Se tradujeron título, encabezados, explicaciones y etiquetas al español sin cambiar rutas. | Build estricto y verificación de fragmentos locales. |
| Nota de cambios construida pero no descubierta | Se agregó front matter, título y subruta dentro de Cambios. | Build estricto sin aviso de página fuera de navegación. |
| Anclajes con acento no coincidían con MkDocs | Se enlazan los IDs normalizados `#mexico`, `#paises` y `#catalogo`. | `verify_site` sobre el HTML generado. |

## Verificaciones ejecutadas

La batería completa confirmó contratos de datos, catálogo generado, cobertura, mapa de conocimiento, grafo temporal y evaluación de recuperación. El conjunto de evaluación reportó `citation_coverage=1.0`, `recall_at_k=1.0`, `temporal_accuracy=1.0` y MRR de `0.9333` para sus preguntas definidas. Se construyó tanto el sitio convencional como el perfil offline; este último verificó índice de búsqueda y activos de ejecución.

La vista previa local confirmó que el explorador mundial muestra un grupo de filtros legible, una tabla con siete guías y la explicación de que no es una serie estadística. También confirmó que el tablero ANAM carga su conjunto local, muestra el grupo de filtros, la recaudación Q2 de 336,190 MDP y su serie enero–junio. Estas comprobaciones se realizaron en escritorio; no sustituyen pruebas con lector de pantalla, zoom extremo o dispositivos móviles físicos.

## Escaneo estático de seguridad

El análisis Semgrep se ejecutó en modo completo sin telemetría y sin motor Pro. Completaron `p/security-audit`, `p/secrets`, `p/python`, `p/javascript`, `p/github-actions` y las reglas de Apiiro. No completaron `p/yaml` y dos conjuntos externos: Trail of Bits terminó con código 7 y elttam presentó errores de validación de patrones. Por tanto, el resultado es **cobertura parcial**, no una certificación de ausencia de vulnerabilidades.

El SARIF fusionado señaló `_date_yyyymmdd` en `scripts/snice_intelligence.py`; la revisión de contexto confirmó que es un analizador fijo de fecha mediante `datetime.strptime`, no ejecución dinámica ni ofuscación. La corrección de mayor valor fue preventiva: reemplazar la interpolación `innerHTML` del dashboard por renderizado seguro de nodos.

## Deuda priorizada

| Prioridad | Decisión pendiente | Razón y criterio de cierre |
|---|---|---|
| P0 editorial | Hacer visible el estado de fuente/revisión en catálogo y navegación. | Los estados canónicos distinguen contenido vigente, parcial, pendiente y no actual; el lector debe ver esa diferencia antes de usar una página como guía operativa. |
| P1 de integración | Versionar contratos consumibles para `arancel-mx` y `dof-diff-lab`. | Cada adaptador debe declarar dueño, versión, release o commit observado, campos, degradación y prueba de compatibilidad. |
| P1 de accesibilidad | Ejecutar prueba manual con móvil real, teclado, lector de pantalla, zoom 200/400% y contraste claro/oscuro. | Aprobación explícita de criterios de lectura, foco, reflow y contraste; no basta la inspección de CSS. |
| P1 de seguridad | Resolver reglas Semgrep incompatibles y añadir comprobación YAML alternativa; eliminar o justificar fuentes HTTP y exclusiones de enlaces. | El informe de seguridad debe cubrir configuraciones y dependencias con reglas que completen correctamente. |
| P2 de mantenibilidad | Adoptar política reproducible de dependencias y un comando único de validación local/CI. | Dos instalaciones limpias deben resolver las mismas versiones y ejecutar los mismos gates. |
| P2 de cobertura de código | Diferenciar cobertura editorial de corpus y cobertura de pruebas de scripts. | Crear umbral o tests de integración por comando, sin confundirlo con el estado de fuentes. |

## Límites de la auditoría

La auditoría no declara vigencia jurídica de las normas, exactitud económica más allá de los valores ya documentados, licencia de cada documento externo, seguridad del CDN de GitHub Pages, configuración de cabeceras HTTP, ni compatibilidad con APIs privadas. Tampoco completa el backlog editorial; lo hace visible y propone condiciones verificables para cerrarlo.

## Referencias de auditoría

- [Evidencia visual local](auditoria-integral-evidencia-2026-08-21.md).
- [Cobertura de corpus](../status/corpus-coverage.md).
- [Modelo de estados y elegibilidad](../methodology/state-model.md).
- [Metodología de accesibilidad](../methodology/accessibility.md).
- [Contratos entre repositorios](../methodology/cross-repo-contracts.md).
