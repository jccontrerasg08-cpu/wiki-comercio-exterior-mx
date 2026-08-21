# Lectura visual de referencias SDV

## Captura 1: catálogo de herramientas — recortes 1 y 2

La cuadrícula emplea tarjetas de utilidad con cuatro señales repetibles: icono de categoría en bloque de color, etiqueta opcional «Nuevo», título orientado a tarea, descripción de alcance y CTA uniforme «Abrir herramienta →». Los módulos legibles, sin reconstruir el texto cortado de los bordes, son:

| Módulo visible | Promesa legible | Patrón transferible |
|---|---|---|
| Buscador de Fracciones Arancelarias | Buscar fracción LIGIE por producto o código; relacionar aranceles, RRNA y tratados. | Consulta de dominio con fuentes y vínculos relacionados. |
| Simulador de Costos de Importación | Calcular costo total con CIF, arancel, DTA, IVA e IEPS por país/tratado. | Herramienta de cálculo, sólo con datos/versiones explícitos. |
| Calculadora de Aranceles por País | Consultar tasa por país y tratado; comparar orígenes. | Comparador de escenarios que exige preferencia, producto y vigencia. |
| Verificador T-MEC (USMCA) | Revisar reglas de origen y contenido regional para tasa preferencial. | Flujo guiado con límites y evidencia documental. |
| Consultor RRNA | Consultar NOMs, permisos, entidades y certificaciones. | Matriz de requisitos por producto/operación. |
| Guía de Importación Paso a Paso | Wizard desde producto hasta despacho, requisitos y costos. | Recorrido por situación, no sustituto de determinación individual. |

La captura confirma una separación útil entre herramientas de búsqueda, cálculo, verificación, consulta regulatoria y guía de proceso. La adaptación a la wiki debe conservar tarjetas con tipo, estado, fuente y límites, pero no reutilizar identidad gráfica ni asumir que los cálculos de referencia son exactos para un caso individual.

## Captura 1 y 2: cierre de herramientas e inicio legal — recortes 3 y 1

El cierre del catálogo añade dos categorías transferibles:

| Módulo visible | Promesa legible | Condición de adopción en la wiki |
|---|---|---|
| Calculadora de Pedimento Aduanero | Campos de IGI, DTA, IVA, prevalidación y formato oficial. | Debe vivir sobre datos/reglas versionadas de `arancel-mx`; no se publica como cálculo definitivo sin supuestos, fecha y fuente. |
| Dashboard Comercio Exterior | Socios comerciales de México, cobertura de TLCs e indicadores. | Debe usar el contrato unificado: `trade_flow` separado de `tariff` y `revenue_anam`. |

La captura legal inicia con un encabezado de módulo «Legislación y Compendio Legal», subtítulo «Leyes clave para comercio exterior — artículo por artículo» y tarjetas de consulta. Las tarjetas legibles son Ley Aduanera («Marco legal del despacho aduanero, regímenes y operaciones») y T-MEC («Tratado comercial con EE.UU. y Canadá — reglas de origen»). El patrón transferible es un índice de fuentes profundas por dominio y propósito; la wiki ya cuenta con documentos/fuentes y debe añadir una capa de descubribilidad, no copiar contenido ni prometer texto artículo por artículo sin fuente verificable.

## Captura 2: compendio legal — recortes 2 y 3

Las tarjetas restantes completan un compendio de seis entradas: LIGIE («Clasificación arancelaria y tasas de importación/exportación»), CPTPP («Tratado Transpacífico — 11 países de la Cuenca del Pacífico»), Ley de Comercio Exterior («Aranceles, cuotas compensatorias y medidas de regulación») y Reglas de Comercio Exterior («RGCE vigentes — procedimientos y requisitos operativos»). Todas mantienen un CTA de «Consultar →» y un icono semántico.

La organización transferible para la wiki es una capa `Compendio` con seis núcleos de navegación: Ley Aduanera, LIGIE, Ley de Comercio Exterior, RGCE, tratados y reglas de origen. Cada tarjeta debe llevar tipo de recurso, fuente primaria, estado de revisión y un enlace a la página ya existente. La etiqueta «vigentes» no debe usarse sin un proceso reproducible de verificación temporal; para RGCE se prefiere mostrar «corte de fuente» y fecha de revisión.

## Captura 3: tratados comerciales — recortes 1 y 2

El encabezado presenta «Tratados Comerciales de México» y una red de acuerdos. Las tarjetas muestran icono, clave corta, año, nombre normalizado y contrapartes/cobertura. Los acuerdos legibles son T-MEC / USMCA (clave T-MEC, 2020, EE.UU. y Canadá), TLC México-UE (TLCUEM, 2000, Unión Europea — 27 países), TLC México-Chile (TLC-CL, 1999, Chile), TLC México-Israel (TLC-IL, 2000, Israel), CPTPP / TIPAT (CPTPP, 2018, incluye Japón, Vietnam, Australia y más) y TLC México-EFTA (AELC, 2001, Suiza, Noruega, Islandia y Liechtenstein).

El patrón transferible es una ficha de tratado con `instrument_id`, nombre, estado editorial, fecha/hito indicado por la fuente, países ISO3/agrupaciones, documentos de promulgación y relación hacia reglas de origen/arancel preferencial. El texto «vigentes» de una interfaz de referencia no debe copiarse ni convertirse en verificación jurídica propia; la wiki debe enlazar a su fuente primaria, fecha de corte y nota de estado.

## Captura 3: tratados comerciales — recorte 3 y reconciliación

El extremo derecho completa la red con Alianza del Pacífico (AP, 2016, Colombia, Chile y Perú) y TLC México-Corea del Sur (TLC-KR, 2022, Corea del Sur). Las superposiciones entre recortes confirman que los campos de cada tarjeta son consistentes: icono, código, año, nombre y contraparte/cobertura.

No se infiere de estas capturas la vigencia jurídica, los capítulos, tasas, reglas de origen ni documentos aplicables de cada instrumento. Para la wiki, cada tarjeta debe ser una puerta de descubrimiento hacia sus fuentes preservadas, catálogo de tratados, reglas de origen y estado de revisión fechado.

