---
title: Proceso de despacho aduanero
description: Flujo de una operación de importación o exportación desde clasificación y RRNA hasta pedimento, selección automatizada y expediente posterior.
---

# Proceso de despacho aduanero

## Un proceso, no un solo documento

La Ley Aduanera define el **despacho aduanero** como el conjunto de actos y formalidades relativos a la entrada o salida de mercancías que realizan autoridades y participantes conforme a los regímenes y disposiciones aplicables. El pedimento es una pieza central, pero preparar correctamente el despacho comienza antes de transmitirlo.

La secuencia exacta depende de la mercancía, régimen, tráfico, aduana, origen, participantes y beneficios utilizados. El flujo siguiente es una **ruta de control**, no una afirmación de que todas las operaciones tengan exactamente los mismos pasos.

## 1. Definir la operación

Antes de clasificar, identifica qué está ocurriendo jurídicamente:

- importación o exportación;
- definitiva, temporal, depósito fiscal, tránsito u otro régimen;
- vendedor, comprador, importador/exportador y representantes;
- país de origen y procedencia;
- tráfico y punto de entrada/salida;
- programa o tratado que se pretende utilizar.

El artículo 90 de la Ley Aduanera estructura los regímenes. Escoger un régimen no es sólo seleccionar una clave: determina tratamiento jurídico, obligaciones, plazos y forma de conclusión.

## 2. Clasificar mercancía y NICO

La fracción arancelaria conecta la mercancía con la TIGIE y con muchas regulaciones. La descripción comercial debe ser suficientemente técnica para sustentar la clasificación: material, función, composición, presentación, potencia, capacidad o cualquier característica relevante.

Cuando corresponda, el NICO completa la identificación mexicana a diez dígitos. Consulta [TIGIE y NICO](../clasificacion/tigie-nico.md) y la capa estructurada `arancel-mx` para datos reproducibles.

## 3. Revisar RRNA y padrones

Con la clasificación preliminar, revisa permisos, avisos, NOM y demás **regulaciones y restricciones no arancelarias**. Para Secretaría de Economía, las Reglas y criterios y sus Anexos 2.2.1 y 2.4.1 son fuentes centrales, pero otras autoridades pueden imponer requisitos sectoriales.

En paralelo verifica si el importador debe estar inscrito en el Padrón de Importadores y si existe obligación sectorial. Como regla general hay obligación para quienes encuadran, pero RGCE contiene excepciones y autorizaciones específicas. Consulta [Padrón](../fundamentos/padron-importadores.md).

## 4. Determinar valor, origen y trato arancelario

La clasificación por sí sola no determina cuánto pagar. Debes establecer:

- método y **valor en aduana**;
- origen de la mercancía;
- posibilidad de trato preferencial por tratado;
- PROSEC u otro programa, cuando proceda;
- IGI/IGE;
- IVA, IEPS y DTA según el supuesto;
- cuotas compensatorias, si la resolución aplicable alcanza la operación.

Cada beneficio tiene sus requisitos. No declares preferencia sólo porque proveedor o vendedor esté en un país socio.

## 5. Construir el expediente documental

Integra los documentos exigidos por la operación. Puede incluir pedimento, documento equivalente, transporte, datos de valor/comercialización, e-documentos, permisos, certificados/certificaciones de origen, Manifestación de Valor, garantías y otros soportes.

La documentación debe representar una sola operación coherente. Consulta [Documentos](documentos.md) y [Manifestación de Valor](manifestacion-valor.md).

## 6. Preparar y transmitir el pedimento

La Ley Aduanera define al pedimento como una declaración electrónica que contiene información de la mercancía, tráfico, régimen y demás datos requeridos. La preparación debe apoyarse en el expediente anterior, no al revés.

Según la operación, intervienen importador/exportador, agente aduanal o agencia aduanal y otros participantes. La persona que transmite no sustituye las obligaciones que la Ley conserva para cada sujeto.

El **Anexo 22** es fundamental para claves, campos, identificadores y complementos. Una clave técnicamente aceptada por el sistema no prueba que el supuesto jurídico que representa sea correcto.

## 7. Validación, pago y presentación

La secuencia operativa incluye validaciones electrónicas y, cuando corresponda, determinación/pago de contribuciones y demás conceptos antes de presentar las mercancías al mecanismo correspondiente. Los pasos tecnológicos concretos pueden cambiar y deben verificarse en RGCE, manuales y sistemas vigentes.

Desde mayo de 2026 también debe considerarse el marco de la nueva [Ventanilla Única](vucem.md), que organiza la gestión digital de trámites y mantiene a VUCEM como infraestructura tecnológica durante su transición.

## 8. Mecanismo de selección y reconocimiento

La Ley define el **mecanismo de selección automatizado** como el mecanismo que determina si las mercancías se someterán a reconocimiento aduanero. Cuando procede reconocimiento, la autoridad examina las mercancías y/o muestras para allegarse de elementos que permitan verificar la veracidad de lo declarado y el cumplimiento de las disposiciones aplicables.

No debe interpretarse un resultado sin reconocimiento como una “certificación” de que la operación quedó jurídicamente correcta. Las autoridades conservan facultades de comprobación posteriores.

## 9. Incidencias y PAMA

Si durante reconocimiento, verificación u otras facultades se detectan hechos que encuadren en causales de embargo precautorio, puede iniciarse un **Procedimiento Administrativo en Materia Aduanera (PAMA)** conforme a los artículos 150 y 151. Otros supuestos de determinación de contribuciones o sanciones pueden seguir procedimientos distintos cuando no se actualiza el artículo 151.

Consulta [PAMA e infracciones](infracciones-pama.md). No uses “cualquier error genera PAMA” como regla: la consecuencia depende del supuesto legal.

## 10. Liberación y expediente posterior

Después de la salida de la mercancía, la obligación de cumplimiento no termina. Conserva pedimento, anexos, acuses, soportes de valor y origen, permisos, facturas y demás evidencia conforme a los plazos legales.

Para una empresa con operaciones recurrentes conviene ligar cada pedimento con:

- orden de compra/venta;
- SKU y clasificación aprobada;
- expediente de origen;
- expediente de valoración;
- RRNA y permisos;
- pagos y rectificaciones;
- inventarios/regímenes temporales cuando corresponda.

## Checklist resumida

| Fase | Pregunta de control |
|---|---|
| Operación | ¿régimen y participantes están definidos? |
| Clasificación | ¿la descripción técnica soporta la fracción/NICO? |
| RRNA | ¿se verificó contra la fuente vigente? |
| Padrón | ¿aplica obligación general, sector o excepción? |
| Valor | ¿método y ajustes están documentados? |
| Origen | ¿el trato preferencial, si se usa, está acreditado? |
| Pedimento | ¿claves e identificadores corresponden al supuesto real? |
| Despacho | ¿se conservaron acuses y eventos del sistema? |
| Post-despacho | ¿el expediente permite reconstruir la decisión años después? |

## Fuentes oficiales

- [Ley Aduanera](https://www.diputados.gob.mx/LeyesBiblio/pdf/LAdua.pdf)
- [RGCE 2026](https://sidof.segob.gob.mx/notas/5777199)
- [SAT, Normatividad RGCE 2026](https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/normatividad_rmf_rgce2026.html)
- [ANAM](https://anam.gob.mx/)
- [Ventanilla Única](https://www.ventanillaunica.gob.mx/)

> El flujo sirve para investigar y auditar una operación. Los requisitos concretos deben validarse contra el régimen, mercancía, aduana y fecha efectivos.

## Ver también

[Documentos para el despacho](documentos.md) · [Regímenes aduaneros](regimenes-aduaneros.md) · [Pedimento y RGCE](pedimento-rgce.md) · [Valor en aduana](../contribuciones/valor-en-aduana.md)