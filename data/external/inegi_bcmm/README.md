# BCMM INEGI: modo de transporte, aduana y capítulo

Este directorio conserva el insumo estadístico utilizado por la visualización `docs/assets/images/bcmm-modo-transporte-2026-05.png` y su tabla derivada. No es una fuente jurídica ni un sustituto de los instrumentos, permisos, pedimentos o expedientes por operación.

| Elemento | Valor |
|---|---|
| Fuente institucional | [INEGI, ficha BCMM mensual por modo de transporte, aduana y capítulo](https://www.inegi.org.mx/app/descarga/ficha.html?tit=83071&ag=0&f=csv) |
| Publicador | INEGI con base en SAT, SE, BANXICO e INEGI |
| Archivo original | `conjunto_de_datos_bcmm_mensual_mtra_csv.zip` |
| URL de descarga | `https://www.inegi.org.mx/contenidos/programas/comext/datosabiertos/conjunto_de_datos_bcmm_mensual_mtra_csv.zip` |
| Última modificación declarada por INEGI | 2026-07-22 |
| Cobertura temporal declarada | 2012-01 a 2026-05 |
| Unidad | Millones de dólares estadounidenses; valoración FOB según la ficha |
| SHA-256 del ZIP | `91e3a73c72c195a280143319dd6e2009101ea2ae3f38730e1e9cc55ba5681907` |
| Transformación | `scripts/build_bcmm_transport_chart.py` |

El script lee únicamente las filas nacionales disponibles de mayo de 2026 para `Aéreo`, `Carretero`, `Ferroviario`, `Marítimo` y `Otros modos`, separadas en exportación e importación. Rechaza una ejecución si falta una de las diez combinaciones esperadas. La salida `bcmm_mtra_2026_05_transport_summary.csv` permite inspeccionar los valores usados en el gráfico.

La ficha de INEGI identifica cifras revisadas para los datos utilizados y señala reglas de confidencialidad. La visualización describe comercio agregado por modo de transporte; no prueba una ruta física específica, una fracción, un requisito, un origen, una autorización ni el cumplimiento de una operación individual.
