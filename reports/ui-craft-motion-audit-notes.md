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
