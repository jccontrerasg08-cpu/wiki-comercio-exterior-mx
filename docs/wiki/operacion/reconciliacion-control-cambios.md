---
title: Reconciliación y control de cambios
description: Método para contrastar datos comerciales, logísticos y aduaneros, documentar diferencias y preservar la historia de una operación de comercio exterior.
---

# Reconciliación y control de cambios

## La coherencia se revisa entre sistemas, no sólo dentro de un archivo

Una operación de comercio exterior genera datos en distintos momentos: compra o venta, logística, transmisión electrónica, despacho, inventarios, contabilidad y, en ocasiones, rectificaciones o retornos. Cada sistema puede representar la misma mercancía con una clave, unidad, fecha o responsable distinto. El propósito de una reconciliación es identificar dónde existe una diferencia, clasificarla y conservar una explicación verificable; no consiste en forzar que todos los documentos se vean idénticos.

Esta página complementa [Trazabilidad de evidencia por operación](trazabilidad-evidencia.md). Aquella página organiza la evidencia por decisión. Esta describe cómo mantener la **historia de los datos** cuando la información cambia o cuando dos documentos describen la operación desde funciones distintas.

La documentación asociada al despacho debe permitir relacionar valor, transporte, origen, RRNA y demás datos con la operación declarada.[1] Cuando corresponde una transmisión electrónica, el acuse o número de documento contribuye a demostrar el evento de sistema, pero la revisión debe conservar el vínculo hacia el contenido y sus soportes.[2]

## Qué es una diferencia y qué es una contradicción

No toda diferencia es un error. Una unidad comercial puede no ser la unidad estadística; el valor comercial puede requerir análisis adicional para fines aduaneros; un embarque puede dividirse en varios documentos; y una operación puede sufrir un cambio de destinatario o una rectificación. El control falla cuando la diferencia carece de propietario, explicación, fecha o soporte.

| Tipo de hallazgo | Definición operativa | Tratamiento recomendado |
|---|---|---|
| Diferencia esperada | Variación explicable por la función del documento o por la estructura de la operación | Registrar la regla de conversión o la referencia que explica la diferencia y conservarla junto con la operación. |
| Diferencia pendiente | Variación detectada para la que aún no existe evidencia suficiente | Marcar responsable, fecha de apertura, impacto potencial y condición de cierre; no ocultarla con una nota genérica. |
| Corrección previa al despacho | Cambio realizado antes de la declaración o transmisión relevante | Conservar la versión reemplazada, la causa y el responsable; usar la versión final como soporte de la declaración. |
| Cambio posterior | Rectificación, sustitución, complemento, devolución, retorno o ajuste posterior | Conservar la relación entre evento original y posterior; no sustituir el expediente histórico por el archivo más reciente. |
| Contradicción material | Datos incompatibles que pueden afectar clasificación, valor, origen, RRNA, régimen o cantidad | Escalar para validación de la función competente y documentar la decisión tomada. |

La palabra “material” no tiene una única medida para todas las operaciones. En un artículo de bajo riesgo, una diferencia de presentación puede ser menor; en un supuesto sujeto a RRNA, cuota compensatoria, preferencia, IMMEX o garantía, el mismo dato puede cambiar el análisis. La clasificación de criticidad debe responder al hecho y a la norma aplicable, no sólo al importe de una factura.

## Llaves que conectan la operación

La reconciliación no exige que todos los documentos usen el mismo número, pero sí que existan **llaves de enlace**. Estas llaves pueden ser un identificador interno, referencias comerciales, número de guía, contenedor, SKU, partida de factura, folio de transmisión o número de documento aduanero. Una llave debe ser estable, documentada y suficiente para explicar la relación entre documentos.

| Dominio | Llaves frecuentes | Pregunta de diseño |
|---|---|---|
| Comercial | Orden de compra/venta, proveedor, factura, partida, SKU | ¿Puede identificarse cuál partida comercial soporta cada partida o descripción declarada? |
| Logístico | Guía, conocimiento de embarque, contenedor, bulto, lista de empaque | ¿Es posible explicar una consolidación, división o transbordo sin perder la relación con la mercancía? |
| Aduanero | Pedimento o documento aduanero, régimen, clave, fecha de pago o despacho | ¿La llave enlaza la decisión previa con el dato finalmente declarado? |
| Electrónico | Acuse, folio VUCEM, e-documento, sello de tiempo o número de transmisión | ¿El identificador permite recuperar el evento y el archivo o dato asociado? |
| Inventario y posdespacho | Movimiento de inventario, retorno, descargo, rectificación, póliza o asiento | ¿La salida, transformación, transferencia o ajuste conserva el vínculo a la entrada original cuando aplica? |

Las llaves no deben contener información sensible que no sea necesaria para la búsqueda. Si se usan identificadores externos, es conveniente mantener un índice interno de correspondencias y controlar quién puede modificarlo. La trazabilidad también requiere que los enlaces no dependan de rutas locales de una computadora individual.

## Una rutina de conciliación en cinco pasos

La rutina propuesta es deliberadamente neutral respecto del software. Puede aplicarse con un gestor documental, una hoja de control, un ERP o una integración entre sistemas, siempre que el registro de revisión sea recuperable.

| Paso | Resultado verificable | Ejemplo de pregunta |
|---|---|---|
| 1. Delimitar el universo | Lista de operaciones y corte de fecha de la revisión | ¿Se revisarán embarques despachados, pendientes o rectificados durante el periodo definido? |
| 2. Construir el registro maestro | Una fila o ficha por operación con sus llaves de enlace | ¿Qué campo conecta la orden, factura, transporte, acuse y documento aduanero? |
| 3. Comparar campos críticos | Resultado de coincidencias, diferencias y campos faltantes | ¿Descripción, cantidad, unidad, valor, origen, régimen y RRNA son consistentes o tienen explicación? |
| 4. Resolver y aprobar | Evidencia de cierre, responsable y fecha | ¿Quién validó la explicación y qué documento o fuente la respalda? |
| 5. Congelar el corte | Versión del resultado, excepciones abiertas y cambios posteriores | ¿Qué se sabía en la fecha revisada y qué cambio ocurrió después? |

El paso cinco es esencial para una wiki y para una operación real: evita usar una versión nueva de una regla o de un documento para describir artificialmente lo que se decidió antes. El registro no impide corregir; preserva la diferencia entre la **decisión original**, el **motivo de cambio** y el **estado actual**.

## Campos críticos: evaluar función antes de comparar texto

Una comparación literal de texto produce falsos positivos. Por ejemplo, una factura puede agrupar mercancías que el documento aduanero separa, o una lista de empaque puede expresar el peso de forma distinta. Antes de automatizar una regla, define la función de cada campo y el nivel de tolerancia permitido por la política interna.

| Campo | Riesgo de una comparación literal | Regla de análisis más útil |
|---|---|---|
| Descripción de mercancía | Un nombre comercial puede ser demasiado genérico; una ficha técnica puede ser más extensa | Verificar que la descripción declarada se pueda sostener con características técnicas y que los cambios no borren información esencial. |
| Cantidad y unidad | Las unidades comerciales, físicas, estadísticas o de empaque pueden diferir | Documentar la conversión, el factor y la fuente del dato cuando la diferencia sea relevante. |
| Valor y moneda | Precio, valor comercial, cargos y ajustes pueden tener funciones diferentes | Identificar qué dato se compara, bajo qué método y con qué soporte; evitar concluir sólo con una igualdad aritmética. |
| Origen, procedencia y envío | Los tres conceptos pueden corresponder a países distintos | Evaluar cada uno conforme al propósito: preferencia, cuota, marcado u otra medida aplicable. |
| Fechas | Embarque, factura, transmisión, pago y despacho no son sinónimos | Conservar la línea de tiempo y usar la fecha jurídicamente relevante para cada análisis. |
| RRNA | Un permiso puede tener vigencia, titular, cantidad, fracción o alcance específicos | Comparar el alcance de la regulación y el documento, no sólo la existencia de un archivo o un folio. |

## Bitácora de excepciones y cambios

Una bitácora breve y estructurada es más útil que notas dispersas por correo. Debe permitir que otra persona entienda qué cambió y por qué, sin exigir que lea todos los archivos desde cero.

| Campo de bitácora | Contenido mínimo |
|---|---|
| Identificador de operación | Llave que permite abrir el expediente y localizar la partida afectada. |
| Fecha de detección y corte | Cuándo se observó la diferencia y hasta qué información se revisó. |
| Campo o decisión afectada | Descripción, valor, origen, RRNA, transporte, régimen u otro campo crítico. |
| Clasificación | Diferencia esperada, pendiente, corrección previa, cambio posterior o contradicción material. |
| Explicación y soporte | Motivo concreto, documento de apoyo, fuente o referencia a la ficha de decisión. |
| Responsable y aprobación | Quién integra la explicación y quién valida o escala el caso conforme a la política interna. |
| Resultado | Cerrada, escalada, rectificada, reemplazada o pendiente; con fecha de actualización. |

La bitácora no debe convertir una revisión interna en una conclusión legal automática. Su función es hacer visible la información que todavía debe analizarse. Si hay una discrepancia de clasificación, valoración, origen o cumplimiento de RRNA, el cierre requiere el criterio y la fuente que correspondan al caso.

## Paquete de revisión: qué debe poder recuperarse

Un paquete de revisión no necesita duplicar todos los binarios. Debe permitir recuperar el expediente en una secuencia comprensible. Como mínimo, conviene que el índice señale la ficha de decisión, los documentos comerciales y técnicos pertinentes, el transporte, los permisos o evidencia de origen que correspondan, los acuses o folios, el documento aduanero y la bitácora de cambios.

La VUCEM facilita el envío electrónico de información para trámites de RRNA previas al despacho.[3] Por ello, la referencia digital debe incorporarse en el paquete de revisión, pero la plataforma no sustituye el análisis de la autoridad que emite la regulación ni la comprobación de su alcance. La [página de VUCEM](../aduana/vucem.md) profundiza en la distinción entre plataforma, autoridad y acto jurídico.

## Métricas que ayudan sin simular certeza

Una organización puede medir el porcentaje de operaciones con llaves completas, la antigüedad de excepciones, los campos críticos con evidencia enlazada y el tiempo de recuperación de un expediente de muestra. Estas métricas muestran la calidad del control documental; no prueban por sí mismas el cumplimiento legal de una operación. Una métrica útil debe declarar qué mide, cuál es su universo y qué casos quedan fuera.

> Antes de convertir una conciliación en una regla automática, valida la semántica de los campos, los supuestos legales y la fecha de vigencia. Una coincidencia técnica puede ocultar un problema sustantivo; una diferencia técnica puede ser explicable.

## Fuentes oficiales

[1] [Ley Aduanera, Cámara de Diputados](https://www.diputados.gob.mx/LeyesBiblio/pdf/LAdua.pdf), fuente normativa primaria para contrastar obligaciones de documentación y transmisión aplicables.

[2] [ANAM, *Documentos electrónicos o digitales que se deben transmitir como anexos al pedimento de importación*](https://www.anam.gob.mx/documentos-electronicos-o-digitales-que-se-deben-transmitir-como-anexos-al-pedimento-de-importacion/), consulta del 16 de agosto de 2026.

[3] [VUCEM, *Sobre la Ventanilla Única de Comercio Exterior Mexicana*](https://www.ventanillaunica.gob.mx/vucem/ventanillaunica.html), consulta del 16 de agosto de 2026.

## Ver también

[Trazabilidad de evidencia por operación](trazabilidad-evidencia.md) · [Proceso de despacho](../aduana/proceso-despacho.md) · [Documentos de comercio exterior](../aduana/documentos.md) · [Manifestación de Valor](../aduana/manifestacion-valor.md) · [Anexo 24: control de inventarios](../programas/anexo-24-control-inventarios.md)
