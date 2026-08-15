# Metodología

El repositorio aplica una cadena de evidencia reproducible:

1. Identificar el acto de publicación en DOF o SIDOF.
2. Relacionarlo con el texto consolidado oficial, cuando exista.
3. Registrar publicación, entrada en vigor y periodo aplicable por separado.
4. Inventariar cada página y digest con sus fuentes, instrumento y estado de revisión.
5. Validar esquemas, referencias, fechas, catálogo y documentación sin red en cada pull request.
6. Ejecutar comprobaciones externas programadas: sondeos por cadencia y descubrimiento diario mediante la API oficial de datos abiertos de SIDOF. El índice diario aporta IDs; el endpoint por diario completa los títulos antes del filtro temático.
7. Comparar cada hallazgo con IDs y URLs ya registrados. Una publicación nueva queda como `candidate`; nunca cambia vigencia automáticamente.

El monitor conserva como estado de ejecución la fecha, clasificación y hash de la última observación. Ordena primero las fuentes nunca observadas o más antiguas, por lo que el límite por ejecución rota de forma justa incluso si varias fallan. Los fallos se reintentan; las respuestas sanas vuelven a comprobarse según `cadence_days`. La selección explícita de un ID desconocido falla para evitar falsos verdes por errores tipográficos.

El [modelo de estados](status-model.md) evita confundir disponibilidad, vigencia, completitud y revisión. [Patrones externos](external-patterns.md) documenta las prácticas adaptadas de estándares y proyectos de código abierto.
