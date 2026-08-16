# Exploradores, archivo de originales e integración cartográfica

Fecha: 2026-08-15
Estado: aprobado conceptualmente por el propietario del proyecto

## Objetivo

Convertir `wiki-comercio-exterior-mx` en una combinación coherente de enciclopedia, biblioteca jurídica verificable y conjunto de exploradores especializados, sin duplicar las responsabilidades canónicas de `arancel-mx` ni `aduanamap-mx`.

La experiencia final debe permitir navegar por documentos, temas operativos, instrumentos jurídicos, aranceles, tratados, RGCE, programas, RRNA/NOM y geografía, con trazabilidad hacia fuentes oficiales y originales reproducibles.

## Decisiones aprobadas

### 1. Archivo híbrido de fuentes oficiales

El repositorio sí conservará originales oficiales cuando sean necesarios para reproducir o auditar la wiki. Se elimina la política previa implícita de que este repositorio no guarda PDF oficiales.

Se archivarán localmente en Git los originales normativos y datasets oficiales de tamaño razonable que sean críticos para el conocimiento publicado. Los archivos grandes, históricos o de actualización frecuente podrán almacenarse como assets de GitHub Releases, pero siempre deberán estar representados en el catálogo mediante metadata verificable.

Cada original archivado debe registrar, como mínimo:

- `source_id` estable;
- autoridad emisora;
- título oficial;
- URL oficial de origen;
- fecha de publicación;
- fecha de captura;
- fecha de entrada en vigor cuando aplique;
- estado de fuente;
- tipo MIME;
- tamaño;
- SHA256;
- ubicación local o asset de Release;
- relación con instrumento(s), evento(s) y página(s) de la wiki;
- notas de sustitución o supersesión cuando existan.

Un enlace HTTP disponible nunca será suficiente por sí solo para promover una fuente a evidencia vigente.

### 2. Política para originales grandes

Los binarios grandes no se incorporarán necesariamente al historial Git. Podrán publicarse como GitHub Release assets con checksums e identidad estable. La navegación pública no deberá distinguir artificialmente entre un original versionado en Git y un original almacenado como asset: ambos pertenecen a la misma biblioteca documental.

### 3. Navegación dual y múltiples exploradores

La wiki mantendrá navegación documental tradicional y añadirá exploradores de primer nivel generados desde metadata común.

Entradas de primer nivel:

- Aranceles
- Marco jurídico
- RGCE y anexos
- Tratados y origen
- Programas
- RRNA y NOM
- Aduanas y mapa
- Fuentes oficiales

Las vistas no duplicarán los documentos. Un mismo objeto fuente o instrumento podrá aparecer por autoridad, tipo documental, tema operativo, vigencia o relación jurídica.

### 4. Separación canónica entre repositorios

Las responsabilidades canónicas quedan separadas por dominio:

- `wiki-comercio-exterior-mx`: fuente canónica jurídica, documental y de provenance. Conserva originales, leyes, reglamentos, RGCE, tratados, NOM, manifests, eventos y relaciones jurídicas.
- `arancel-mx`: fuente canónica arancelaria estructurada. Conserva HS, TIGIE, fracción mexicana, NICO, tasas y artefactos de datos reproducibles.
- `aduanamap-mx`: fuente canónica geoespacial y aplicación cartográfica. Conserva GeoJSON y otras capas de aduanas, puertos, aeropuertos, cruces, rutas, países y relaciones geográficas.

Los repositorios compartirán IDs y metadatos estables cuando una entidad atraviese dominios. No se mantendrán copias manuales divergentes de los mismos datasets estructurados.

### 5. Integración cartográfica

La wiki tendrá una experiencia híbrida:

- un explorador cartográfico central de comercio exterior;
- mapas contextuales embebidos y filtrados dentro de páginas relevantes;
- AduanaMap conserva la experiencia cartográfica avanzada, comparadores y cruces de datos.

Los mapas de la wiki deberán funcionar con datasets versionados y sin requerir una API comercial para la información esencial. Servicios externos pueden ser mejoras opcionales, no dependencias de verdad.

El GeoJSON mundial ya existente en `aduanamap-mx/data/geojson/countries-50m.geojson` se considera candidato canónico para países y no debe duplicarse manualmente en la wiki.

### 6. Exploradores previstos

#### Aranceles

La wiki explica la estructura y enlaza a la capa estructurada de `arancel-mx`:

HS -> capítulo -> partida -> subpartida -> fracción MX -> NICO -> tasa -> RRNA -> preferencias/tratados relacionados.

La wiki no mantiene una segunda tabla arancelaria completa.

#### Marco jurídico

Navegación por:

instrumento -> artículo/regla -> reforma/evento -> disposición relacionada -> original -> páginas operativas.

Debe soportar temporalidad y distinguir texto consolidado, decreto modificatorio, publicación anticipada y fuente secundaria.

#### RGCE y anexos

Navegación por año, título, capítulo, regla, anexo y modificaciones. Las publicaciones anticipadas deben distinguirse de las publicaciones DOF definitivas.

#### Tratados y origen

Vista lista + mapa. Cada tratado debe relacionar:

- partes;
- vigencia;
- capítulos relevantes;
- reglas de origen;
- documentos originales;
- instrumentos de implementación mexicanos;
- páginas operativas relacionadas.

#### Programas

IMMEX, PROSEC, Drawback, certificaciones y otros programas se navegarán como objetos relacionados con instrumentos, trámites, anexos, requisitos y páginas operativas.

#### RRNA y NOM

Explorador por autoridad, instrumento, NOM, fracción relacionada cuando exista enlace estructurado, excepción y evidencia oficial. No se inferirá aplicabilidad sólo por NICO de referencia.

#### Aduanas y mapa

Vista central con capas que, conforme existan datasets confiables, podrá incluir:

- países;
- aduanas y secciones;
- puertos;
- aeropuertos;
- cruces fronterizos;
- recintos y RFE;
- rutas fiscales y de tránsito;
- países parte de tratados;
- otras capas de comercio exterior.

Las páginas específicas podrán embeber vistas filtradas del mismo origen de datos.

#### Fuentes oficiales

Navegación por:

autoridad -> instrumento -> versión/publicación -> original -> checksum -> vigencia -> páginas relacionadas.

Debe mostrar claramente si el original está en Git, GitHub Releases o sólo referenciado externamente.

## Modelo de metadata

El diseño debe reutilizar `sources/registry.yaml`, `sources/instruments.yaml`, `sources/page_metadata.yaml` y los manifests existentes en lugar de crear catálogos paralelos. Si faltan campos, se ampliará el esquema de forma compatible.

Se añadirá una representación explícita de almacenamiento del original, por ejemplo:

```yaml
archive:
  status: local_git | release_asset | external_only
  path: data/originals/...
  release_tag: null
  asset_name: null
  sha256: ...
  size_bytes: ...
  mime_type: application/pdf
  captured_at: 2026-08-15
```

`external_only` sólo será válido cuando conservar una copia no sea necesario, sea redundante, no sea técnicamente razonable o exista una limitación clara. La razón deberá quedar documentada.

## Auditoría de contradicciones

La implementación debe buscar y corregir frases o políticas que contradigan este diseño, incluyendo expresiones equivalentes a:

- `does not ship official PDF bytes`;
- `this tree is not a DOF dump` cuando se use para prohibir el archivo de originales;
- `catalog-only; do not scrape` cuando la intención real deba ser una política más precisa de captura, archivo o consumo;
- cualquier afirmación que implique que la wiki depende únicamente de enlaces externos.

No se reemplazarán por una política de scraping indiscriminado. Cada fuente seguirá una estrategia apropiada según autoridad, formato, estabilidad, licenciamiento, reproducibilidad y valor probatorio.

## Fuentes solicitadas al propietario

Antes de pedir un documento nuevo se debe comprobar:

1. `data/originals/` y sus manifests;
2. `sources/registry.yaml` e instrumentos relacionados;
3. corpus y páginas existentes;
4. archivos ya subidos en la conversación/proyecto;
5. versiones equivalentes o más recientes.

Sólo se pedirá un documento si realmente falta, existe únicamente una copia incompleta, se necesita una versión oficial más reciente o un formato estructurado aporta información no presente.

## Integración con `aduanamap-mx`

No se copiará manualmente el GeoJSON mundial a la wiki como una segunda fuente canónica.

La primera integración debe definir un contrato estable de consumo que pueda usar uno de estos mecanismos, por orden de preferencia:

1. artefacto versionado/release de `aduanamap-mx` con checksum;
2. URL raw versionada por commit/tag;
3. copia generada durante build con metadata de procedencia y hash, nunca mantenida manualmente.

La wiki debe degradar correctamente cuando el mapa no pueda cargar: el contenido jurídico y documental seguirá siendo navegable.

## UX

La portada y navegación principal deben ofrecer rutas claras tanto a usuarios que saben qué instrumento buscan como a usuarios que parten de una operación de comercio exterior.

Cada explorador deberá privilegiar:

- búsqueda;
- filtros relevantes;
- estado de vigencia;
- fuente oficial;
- relaciones con otras páginas;
- enlaces al original;
- navegación por contexto, no sólo listas de URLs.

El diseño visual seguirá MkDocs Material y los patrones existentes del proyecto. No se introducirá un SPA paralela dentro de la wiki si el mismo resultado puede obtenerse con componentes ligeros y datos estáticos.

## Fases de implementación

### Fase A: archivo y catálogo verificable

- corregir contradicciones documentales;
- ampliar metadata de archivo;
- crear validadores/tests para originales y checksums;
- crear vista navegable de biblioteca de fuentes;
- registrar los originales críticos ya presentes y los nuevos documentos oficiales aportados.

### Fase B: exploradores de conocimiento

- crear portada `Explorar`;
- crear vistas por marco jurídico, RGCE, tratados, programas, RRNA/NOM y fuentes;
- generar índices desde metadata común;
- mantener compatibilidad con URLs existentes.

### Fase C: mapa contextual

- definir contrato de datos con `aduanamap-mx`;
- reutilizar capas canónicas existentes;
- añadir explorador cartográfico central ligero;
- añadir componentes embebibles filtrables;
- añadir enlaces hacia AduanaMap para análisis avanzado.

### Fase D: interoperabilidad entre repositorios

- documentar IDs compartidos;
- publicar manifests/artefactos consumibles;
- añadir checks que detecten referencias rotas o versiones incompatibles;
- evitar divergencia entre wiki, `arancel-mx` y `aduanamap-mx`.

## Límites de alcance

- La wiki no reemplaza `arancel-mx` como base arancelaria estructurada.
- La wiki no reemplaza AduanaMap como aplicación geoespacial avanzada.
- No se copiarán textos protegidos de fuentes privadas como ICC Incoterms; se conservarán sólo referencias y explicaciones compatibles con derechos aplicables.
- No se promoverá automáticamente contenido jurídico a vigente sólo porque una descarga o endpoint responda.
- Los originales archivados son evidencia y respaldo, no sustituyen la publicación oficial para determinar vigencia cuando el ordenamiento exige consulta al DOF u otra autoridad.

## Criterios de aceptación

1. No quedan contradicciones de política que prohíban genéricamente conservar originales oficiales.
2. Los documentos críticos pueden identificarse por autoridad, instrumento, fecha, vigencia, checksum y ubicación de archivo.
3. La wiki ofrece navegación documental y operativa sin duplicar archivos.
4. Existe una ruta de primer nivel a Aranceles, Marco jurídico, RGCE, Tratados, Programas, RRNA/NOM, Mapa y Fuentes.
5. Las páginas pueden relacionarse con originales y fuentes desde metadata común.
6. El mapa usa geodatos canónicos de AduanaMap o artefactos derivados reproducibles, no una copia manual divergente.
7. La ausencia del mapa o de una fuente externa no rompe el contenido jurídico principal.
8. Tests de integridad detectan hashes faltantes, rutas inválidas, referencias a assets inexistentes y contradicciones básicas de esquema.
9. `mkdocs build --strict` y la suite existente permanecen verdes.
10. El número de PRs abiertos del proyecto se mantiene pequeño y cada PR conserva un alcance coherente.
