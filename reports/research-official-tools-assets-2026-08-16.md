# Investigación de herramientas oficiales y activos visuales

Fecha de consulta: 2026-08-16.

## SNICE: LIGIE, NICO y materiales visuales

La búsqueda de activos devuelve infografías de **LIGIE: Acerca de** atribuidas a SNICE. Las piezas identificadas explican las Notas Nacionales, el Decreto General, los Números de Identificación Comercial (NICO) y su metodología. Estas imágenes tienen función editorial directa para la guía de TIGIE/NICO porque resumen relaciones que el lector suele confundir: la fracción de ocho dígitos, el NICO, el decreto, las notas y la publicación.

Sólo se considerarán los activos cuyo resultado identifica a SNICE como fuente. Se conservará la advertencia de que una infografía institucional sirve para orientación; la LIGIE vigente, decretos y publicaciones posteriores siguen siendo las fuentes que deben confirmar el tratamiento aplicable.

## ANAM: herramientas y mapa

La portada oficial de ANAM presenta accesos a **Sistema Electrónico de Aduanas**, **VUCEM**, **Módulo Único de Pago Electrónico Aduanero**, recintos fiscalizados y programas especiales. El sitio institucional no expuso durante esta consulta un mapa o directorio geográfico reutilizable de aduanas. Por ello no se incorporará el mapa de terceros visto en la búsqueda de imágenes: la entrada cartográfica de la wiki conservará su vínculo con `aduanamap-mx` y su advertencia de que el mapa no sustituye la fuente jurídica.

## INEGI: TIGIE–SCIAN

La búsqueda devuelve gráficos del catálogo TIGIE–SCIAN que explican su correspondencia con clasificación económica. La aplicación oficial de INEGI no respondió en Chrome durante esta consulta (`ERR_CONNECTION_TIMED_OUT`), por lo que esos activos no se incorporarán hasta validar su ruta y procedencia directamente. La wiki mantendrá el enlace oficial y seguirá distinguiendo una herramienta de correspondencia estadística de la determinación arancelaria jurídica.

## Conclusión operativa

El lote visual prioritario será SNICE/LIGIE/NICO. Para ANAM y el mapa, se añadirá contexto y enlaces oficiales, pero no una imagen de mapa sin una fuente institucional verificable. Para INEGI, se documenta la ruta y se pospone el uso del material visual hasta que el portal sea accesible y verificable.

## Evaluación de soluciones abiertas

Se revisó el catálogo comunitario de MkDocs y proyectos de validación de enlaces. `mkdocs/catalog` es útil como directorio de plugins, pero no sustituye la validación específica que ya hace este repositorio sobre rutas de GitHub Pages, anclas, fuentes directas y políticas editoriales. `markdownlint` es un proyecto consolidado, pero añadirlo no resolvería el requisito principal de esta iteración —explicar herramientas oficiales y verificar sus fuentes— y duplicaría reglas ya cubiertas por controles propios. No se añadirá dependencia ni abstracción nueva en este lote.

## Evaluación de los activos SNICE seleccionados

La infografía de **NICO** es legible a tamaño editorial y explica que el identificador corresponde al quinto par de dígitos añadido a la fracción de ocho dígitos. También comunica que no supone por sí solo una carga regulatoria. Se incorporará a la guía TIGIE/NICO, con una leyenda que preserve ese límite.

La infografía de **Decreto General** es legible y es útil para separar un decreto de armonización de una tasa o medida vigente. Contiene referencias históricas explícitas a TIGIE 2022 y al 18 de noviembre de 2022, por lo que se incorporará únicamente junto con una advertencia visible: ilustra un mecanismo y un contexto de publicación; no acredita tasas ni medidas vigentes en la fecha actual.

## Comprobación visual en Chrome

La guía TIGIE/NICO presenta la infografía institucional al inicio, antes de la tabla que separa mercancía, LIGIE/TIGIE, NICO, herramienta y declaración. La jerarquía mantiene legibles la leyenda, la advertencia de fuentes y la navegación lateral en modo oscuro.

La guía de lectura tarifaria conserva la tabla de capas antes de la infografía histórica. La leyenda temporal aparece inmediatamente después del activo, de modo que la imagen no se presenta como evidencia de tasa vigente. Ambas integraciones mantienen texto alternativo y rutas de profundización dentro de la wiki.
