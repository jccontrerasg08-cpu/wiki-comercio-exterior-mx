# Notas de auditoría visual — portada MkDocs

Fecha de revisión: 2026-08-20

## Observaciones verificadas en la interfaz desplegada

La portada presenta una identidad clara de comercio exterior con cabecera azul, hero editorial, dos llamadas a la acción y una ruta de cinco pasos. En escritorio, la jerarquía de hero es legible y la navegación principal expone muchas secciones, por lo que el contenido de la portada necesita ofrecer orientación inmediata sin aumentar densidad visual.

La ruta operativa se transforma de cinco columnas a tres y luego una según el ancho. Su línea discontinua animada ya desaparece en el breakpoint medio, evitando una conexión visual engañosa cuando la secuencia deja de ser lineal. Las tarjetas de la ruta son enlaces grandes y muestran elevación por `transform` en hover/foco. La interfaz contiene foco visible y una alternativa global para `prefers-reduced-motion`.

## Riesgos y oportunidades

| Área | Hallazgo | Oportunidad de bajo riesgo |
|---|---|---|
| Hero | Las llamadas a la acción son correctas, pero no tienen respuesta de presión propia. | Añadir retroalimentación activa breve sólo a botones reales. |
| Tarjetas de ruta | La elevación sirve para comunicar que son enlaces, pero se aplica el mismo comportamiento a hover y foco. | Conservar foco estable y limitar el desplazamiento a dispositivos con hover/puntero fino; el foco debe usar borde y sombra sin movimiento. |
| Tarjetas generales | Sólo el contenedor de lista recibe hover; el enlace interno puede no transmitir con claridad la activación. | Aplicar realce de tarjeta mediante `:focus-within` y una respuesta táctil/activa sutil en el enlace real. |
| Movimiento continuo | La línea de ruta es decorativa y ya tiene reducción de movimiento. | Mantenerla decorativa, ralentizarla ligeramente o no añadir más movimiento continuo. |
| Navegación | La cantidad de opciones de navegación es alta; la mejora principal debe ser orientación, no animación. | Reforzar estados de foco, hover y presión; no introducir paneles ni menús custom. |

## Decisión provisional

Se recomienda un ajuste CSS acotado, sin dependencias ni JavaScript: tokens de movimiento, feedback de presión para botones y enlaces de ruta, hover condicionado a hardware adecuado, foco sin desplazamiento y respeto de movimiento reducido. No se recomienda añadir animaciones decorativas adicionales ni modificar la navegación de Material for MkDocs.

## Nota de compatibilidad

La interfaz pública observada muestra la versión desplegada disponible al momento de revisión. Los cambios futuros deben verificarse localmente con build estricto, reglas existentes de accesibilidad y visualización responsive.

## Captura posterior a la integración

La portada desplegada siguió mostrando la jerarquía de hero, la ruta de cinco pasos, los accesos por tema y el acceso a la ruta de exportación sin errores de presentación visibles. La navegación y los llamados a la acción permanecieron legibles en modo oscuro.

Se intentó abrir el PDF oficial LIGIE 2022 de Cámara de Diputados directamente en el visor del navegador. El navegador navegó a la URL, pero no entregó una captura visual ni texto extraíble del PDF. Este resultado **no invalida** el recurso ni confirma visualmente su contenido; se registra como límite del visor. La identidad documental de esa fuente queda respaldada por la revisión HTTP paralela y por el manifiesto/registro de evidencia, no por esta captura visual.

La siguiente verificación visual debe concentrarse en páginas HTML oficiales de SIDOF y en la portada desplegada, que sí proporcionan una representación visual interpretable.

## Captura de fuente oficial HTML

El asiento oficial SIDOF 5777199 fue accesible como HTML y mostró: título **“Reglas Generales de Comercio Exterior para 2026 y Anexo 13”**, emisor **Poder Ejecutivo / Secretaría de Hacienda y Crédito Público**, publicación **27-12-2025**, y las opciones oficiales para descargar el documento `.doc`, ver la imagen digitalizada y descargar la edición electrónica del diario. La propia fuente advierte que la conversión HTML puede omitir tablas, caracteres u objetos; por ese motivo, la wiki debe conservar la advertencia de usar la imagen digitalizada o el archivo de la edición para detalle documental. Esta captura confirma identidad y disponibilidad del asiento, no una conclusión autónoma de vigencia jurídica.

## Observación visual directa — Recaudación ANAM

La página oficial `recaudacion-anam` se abrió en navegador y muestra la navegación institucional de ANAM, el encabezado «Reporte segundo trimestre 2026 (abril, mayo, junio)» y una tarjeta visual central para «Informe Trimestral Q2» con una llamada a la acción «Más información». La extracción textual identifica además los bloques «Informe Mensual 2026», «Históricos 2026», «Históricos 2025» e «Históricos 2024».

La página actúa como **catálogo de informes visuales en PDF**, no como tablero de datos: no se observaron filtros, tabla navegable, exportación estructurada ni indicadores interactivos en el contenido extraído. La experiencia propuesta para la wiki debe por tanto declarar que sus datos estructurados son una transcripción o extracción verificable de informes ANAM, conservar enlace al PDF y evitar sugerir que ANAM publica una API o CSV.
