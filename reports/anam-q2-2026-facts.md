# Hechos extraídos — Informe Trimestral ANAM Q2 2026

Fuente primaria: <https://www.anam.gob.mx/wp-content/uploads/Informe_trimestral_Q2_2026_f.pdf>

Fecha de extracción: 2026-08-20

## Alcance declarado

El informe cubre el segundo trimestre de 2026 —abril, mayo y junio— y presenta contextos macroeconómicos, recaudación, pedimentos, operaciones y eficiencia de captación. Sus cifras de recaudación están expresadas en **MDP** (millones de pesos); exportaciones, importaciones y balanza comercial de contexto están expresadas en **MDD** (millones de dólares). No se deben mezclar ambas unidades.

## Indicadores destacados publicados

| Indicador | Valor publicado | Periodo o comparación | Nota de interpretación |
|---|---:|---|---|
| Recaudación Q2 | 336,190 MDP | Q2 2026 | 4.0% superior a Q1 según el informe. |
| Recaudación acumulada | 659,393 MDP | Enero-junio 2026 | Acumulado semestral. |
| Recaudación junio | 121,122 MDP | Junio 2026 | Identificado como el monto más alto del año dentro del informe. |
| Pedimentos acumulados | 5,308,502 | Enero-junio 2026 | No equivale a operaciones. |
| Operaciones acumuladas | 10,905,057 | Enero-junio 2026 | No equivale a operaciones gravadas. |
| Recaudación IVA Q2 | 232,775 MDP | Q2 2026 | Variación de +9.8% frente a Q1. |
| Recaudación IGI Q2 | 46,509 MDP | Q2 2026 | Variación de +6.3% frente a Q1. |
| Recaudación IEPS Q2 | 46,327 MDP | Q2 2026 | Variación de -19.5% frente a Q1. |
| Composición por tipo de aduana | 52% marítima, 31% fronteriza, 17% interior | Recaudación Q2 2026 | Participaciones publicadas. |
| Principales aduanas | Nuevo Laredo 50,063; Manzanillo 47,492; Lázaro Cárdenas 31,217 MDP | Recaudación Q2 2026 | Ranking de las 15 principales aduanas. |
| Concentración top 15 | 83% | Recaudación Q2 2026 | Participación nacional publicada. |
| Operaciones Q2 | 5.65 millones | Q2 2026 | +7.5% frente a Q1. |
| Operaciones de importación | 3,161,950 | Q2 2026 | +9.0% frente a Q1. |
| Operaciones de exportación | 2,488,482 | Q2 2026 | +5.7% frente a Q1. |
| Operaciones gravadas | 21.0% | Q2 2026 | El informe distingue el resto como importaciones no gravadas y exportaciones. |
| Costo por 100 recaudados | 0.25 pesos | Acumulado enero-junio 2026 | Indicador de eficiencia de captación reportado por ANAM. |

## Definiciones y límites de transcripción

El informe define «Otros» como DTA, ISAN, cuotas compensatorias, prevalidación, medidas de transición temporal, recargos, sanciones y actualizaciones. Las cifras pueden presentar diferencias por redondeo. Las afirmaciones causales del documento —por ejemplo, el efecto de estímulos fiscales sobre IEPS— se conservan como narrativa de ANAM y no se deben convertir en causalidad demostrada por la wiki.

La fuente también presenta mapas y gráficas con atribuciones GeoNames, Microsoft y TomTom. Para el primer tablero se usarán sólo valores textuales o tabulares confirmados en este registro; no se digitalizarán etiquetas de mapa o puntos visuales sin una segunda comprobación.

## Verificación visual de la implementación

La vista previa local de `wiki/aduana/recaudacion-anam/` cargó correctamente el JSON de datos tras ajustar la ruta relativa desde la página anidada. El estado accesible informó «Mostrando recaudación para Segundo trimestre de 2026 (abril-junio)» y el tablero mostró la métrica de 336,190 MDP, la variación de +4.0% frente a Q1 y los seis valores mensuales transcritos. La navegación incluyó «Recaudación ANAM» dentro de Wiki → Aduana.

La primera vista interactiva confirma mejora progresiva con datos locales; no emplea API remota, animación de cifras ni una capa cartográfica que implique precisión geográfica aún no documentada.

La comprobación con teclado cambió el indicador de Recaudación a Pedimentos mediante el selector nativo. La interfaz actualizó el estado accesible a «Mostrando pedimentos…», mostró 2.72 millones y +5.4% frente a Q1, y presentó el estado vacío previsto para la vista de evolución mensual: no hay serie mensual estructurada transcrita para esa combinación. Esto confirma que una ausencia de granularidad se comunica sin reemplazarla con estimaciones.

La segunda prueba por teclado cambió la vista a «Composición por tipo de aduana». El tablero presentó para pedimentos las participaciones publicadas por ANAM: fronteriza 52.2%, interior 29.9% y marítima 17.9%. La interacción se verificó mediante controles `select` nativos y las barras sólo representan visualmente esos porcentajes; no se ejecutó animación de valores ni cálculo de participación alternativo.
