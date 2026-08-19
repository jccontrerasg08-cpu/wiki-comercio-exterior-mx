# Auditoría de navegación y propuesta de panel lateral

Fecha de revisión: 2026-08-16.

## Hallazgo

La navegación actual conserva todas las áreas temáticas, pero el panel lateral presenta categorías de dominio mezcladas con el orden real en que un lector resuelve una operación. Por ejemplo, clasificación, tarifa, contribuciones y valor aparecen en grupos separados; RRNA aparece tanto como nota dentro de clasificación como como bloque independiente; y evidencia queda al final aunque interviene desde la preparación del despacho. La estructura es correcta como inventario, pero no minimiza decisiones para una consulta operativa.

## Principio de reorganización

Se conservarán **todas las rutas, archivos, metadatos y enlaces internos existentes**. El cambio afectará únicamente títulos y orden dentro de `mkdocs.yml`. El panel se ordenará por el recorrido de una operación, manteniendo las etiquetas temáticas precisas dentro de cada etapa.

| Orden propuesto | Pregunta del lector | Páginas actuales que permanecen accesibles |
|---|---|---|
| **Empieza aquí** | ¿Cómo uso la wiki y qué fuentes debo consultar? | Mapa, Marco jurídico, Biblioteca de instrumentos, Padrón de importadores. |
| **1. Clasifica y determina el tratamiento** | ¿Qué mercancía es y cuál es su tratamiento arancelario? | Sistema Armonizado, TIGIE y NICO, Aranceles, Lectura de tarifa y tratamientos, Valor en aduana, Impuestos de importación, Cuotas compensatorias. |
| **2. Confirma requisitos previos** | ¿Qué RRNA, permisos, avisos o NOM aplican? | Guía RRNA, Ciclo de vida, Reglas y criterios SE, Anexos 2.2.1 y 2.4.1, RRNA como nota de clasificación. |
| **3. Prepara y despacha** | ¿Cómo se documenta, transmite y despacha la operación? | Proceso de despacho, Regímenes, Documentos, Manifestación de Valor, Pedimento y RGCE, VUCEM, Agente/agencia y ANAM. |
| **4. Aplica programas, origen y tratados** | ¿Hay preferencia, programa de fomento u obligación de origen? | T-MEC, Reglas de origen, IMMEX, PROSEC, Drawback, Anexos 24 y 30. |
| **5. Mueve, documenta y controla** | ¿Cómo se coordina logística y se conserva evidencia posterior? | Incoterms, Logística internacional, Pagos, Trazabilidad de evidencia, Reconciliación y control de cambios. |
| **Riesgos y actualización** | ¿Qué ocurre ante infracciones o cambios regulatorios? | PAMA e infracciones, Cambios 2026. |

## Criterios de éxito

La reorganización se acepta sólo si la compilación estricta conserva todas las páginas; las mismas URLs siguen resolviendo; el verificador de enlaces locales no encuentra destinos rotos; el panel sigue siendo comprensible a 1440 px y en vista móvil; y los controles de cobertura, metadatos, calidad editorial y RAG siguen en verde.

## Verificación visual

La captura de escritorio confirma que la portada conserva su recorrido de cinco pasos y que la estructura propuesta usa las mismas palabras de decisión que el lector ya encuentra en el contenido. En la navegación lateral, las etapas numeradas permiten localizar clasificación, requisitos, despacho, programas y evidencia sin saltar entre categorías técnicas aisladas.

La captura móvil mantiene encabezado, contraste, jerarquía tipográfica y llamadas a la acción legibles a 390 px. El menú colapsado evita que el panel lateral consuma el área de lectura; la reorganización no introduce desbordamientos ni altera la composición responsiva de la portada.

La captura de una página interna confirma que el panel izquierdo sí presenta las seis etapas en el orden propuesto: entrada, tratamiento, requisitos, despacho, programas, evidencia y actualización. La ruta de RRNA se muestra bajo **2. Confirma requisitos previos**, y las páginas posteriores permanecen visibles en una secuencia continua. La vista móvil conserva la ruta de migas, contenido y botón de menú sin desbordamiento; el panel permanece accesible bajo demanda, por lo que no se introduce una penalización visual en lectura estrecha.
