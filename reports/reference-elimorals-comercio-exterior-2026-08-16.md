# Comparativo: elimorals/comercio-exterior

Fecha de consulta: 2026-08-16. Repositorio revisado: <https://github.com/elimorals/comercio-exterior>.

## Alcance de la revisión

El repositorio se examinó como referencia de arquitectura, cobertura declarada y prácticas de calidad. No se ejecutó su código, no se importaron dependencias y no se copiará contenido, código, diagramas ni datos. La metadata de GitHub no declara licencia y el archivo `LICENSE` no figura en el inventario superficial clonado, aunque el README muestra un distintivo Apache 2.0; por precaución, se tratará como referencia no reutilizable hasta que su licencia se compruebe explícitamente.

## Hallazgos útiles

| Idea observada | Valor conceptual | Adopción en esta wiki |
|---|---|---|
| Separación por capas entre interfaz, orquestación, skills, conectores y núcleo | Evita que una herramienta, una respuesta o una interfaz suplanten la fuente de verdad | Ya existe un equivalente editorial en la guía de arquitectura: norma, datos, transmisión y evidencia. Puede extenderse a cada flujo de consulta. |
| Parsers puros separados de clientes de red | Facilita pruebas reproducibles y corrección quirúrgica de fuentes cambiantes | El repositorio ya sigue este patrón en `snice_intelligence`, `snice_discovery`, `legal_watch` y sus pruebas. No se añade abstracción nueva. |
| Modo simulado explícito y no conexión accidental a producción | Límite de seguridad útil para integraciones potenciales | La wiki mantiene su frontera actual: no ejecuta trámites, no automatiza portales no contratados y conserva comprobación offline. |
| Evals de groundedness y rutas de herramientas | Refuerza calidad de respuestas y recuperaciones | La wiki ya tiene `rag_eval`, cobertura temporal, fuentes por página y validadores de enlaces; se prioriza profundizar contenido antes de introducir un nuevo framework. |
| Límite explícito de que un agente no firma ni despacha | Buena delimitación de responsabilidad | Se refuerza en páginas operativas: una herramienta, acuse o guía no reemplaza autoridad, instrumento, profesional autorizado ni evidencia. |

## Diferenciación de la wiki

El repositorio de referencia se presenta como infraestructura de automatización y MCP en estado Alpha. Esta wiki debe conservar una finalidad distinta: **orientación documental verificable**, con fuentes oficiales, distinción temporal, catálogo y archivo de procedencia, rutas de lectura y controles estáticos. Su mejora no consiste en replicar agentes o conectores, sino en explicar de forma legible cómo una decisión de comercio exterior se compone de norma, dato técnico, evento de sistema y evidencia.

## Conclusión operativa

No se incorporará código ni dependencias del repositorio de referencia. Se tomarán como principios compatibles: límites explícitos de automatización, trazabilidad de fuente, separación de responsabilidades y validación reproducible. El próximo lote editorial podrá usar una imagen oficial o un diagrama propio para reforzar esos límites en una de las guías operativas de mayor consulta.

## Activos visuales candidatos: VUCEM

La búsqueda de imágenes devolvió piezas atribuidas a VUCEM, cursos y portales de terceros, pero ninguna ruta de imagen directamente verificable desde el portal oficial de VUCEM durante esta consulta. Se descartan los activos de terceros y no se incorporan capturas de interfaz. Para las guías de pedimento, RRNA y logística se priorizará un diagrama propio y reproducible sobre flujos de datos, documentos, transmisión y evidencia. El sitio oficial de VUCEM permanece como referencia de canal: <https://www.ventanillaunica.gob.mx/vucem/index.html>.

## Verificación visual del diagrama documental

En Chrome, el diagrama se integra después de la definición y antes de la tabla de cuatro capas de Pedimento y RGCE. Su escala utiliza el ancho de la columna de lectura, mantiene contraste en modo oscuro y permite seguir la secuencia de decisión, soportes, comprobación, transmisión, evento, expediente y reconciliación. La leyenda queda inmediatamente debajo y evita presentarlo como sustituto de RGCE, Anexo 22, una autorización o el análisis de una operación concreta.
