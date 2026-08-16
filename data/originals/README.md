# Originales oficiales y preservación reproducible

Este directorio contiene la capa de manifiestos del archivo de fuentes oficiales. Cada `MANIFEST.yaml` registra el original por documento con URL oficial, SHA-256, tamaño en bytes y metadatos de redistribución. El archivo raíz `manifest.yaml` enumera los fragmentos y `releases.yaml` indexa los bundles de originales publicados como GitHub Release assets.

## Modelo de almacenamiento

El proyecto usa un modelo híbrido:

- los manifiestos, checksums y metadata reproducible viven en Git;
- los originales oficiales grandes —PDF, `.doc`, `.docx`, `.xlsx` y otros binarios— pueden vivir en GitHub Releases `originals-YYYY.MM.DD` para no inflar innecesariamente el historial Git;
- originales pequeños o artefactos que realmente convenga versionar directamente pueden registrarse como `local_git` en la metadata de fuente;
- portales interactivos o copias redundantes pueden permanecer `external_only` cuando existe una razón documentada.

La [biblioteca documental](../../docs/catalog/library.md) expone esta capa de preservación para navegación humana. `SHA256SUMS` y los manifests permiten verificar los bytes sin convertir una respuesta HTTP exitosa en una decisión jurídica.

## Autoridad y vigencia

Preservar una copia mejora reproducibilidad, auditoría y resiliencia frente a enlaces rotos, pero no sustituye la publicación oficial ni determina por sí solo la vigencia. Para efectos jurídicos se conserva la referencia a SIDOF/DOF, Cámara de Diputados, SAT, SE u otra autoridad competente según el instrumento.

La promoción de una fuente o página a estado jurídico vigente sigue siendo un proceso separado y revisado; ni el hash correcto, ni la existencia de un Release asset, ni HTTP 200 bastan para ello.

## Organización

Cada carpeta tiene su `MANIFEST.yaml`. Las áreas actuales incluyen `diputados/`, `sat/`, `se/`, `sidof/`, `snice/`, `tlc/`, `tmec/`, `vucem/`, `wto/` y `tigie/`. `tigie/` conserva la procedencia de la tabla oficial INEGI TIGIE–SCIAN; las tablas arancelarias estructuradas canónicas pertenecen a [`arancel-mx`](https://github.com/jccontrerasg08-cpu/arancel-mx), no a una segunda base duplicada en esta wiki.

Los resúmenes y extracciones de trabajo están en `data/corpus/`; no sustituyen a los originales.

## Derechos y fuentes propietarias

El proyecto no reclama autoría ni relicencia las publicaciones gubernamentales o tratados preservados: los manifests mantienen `license: official-not-relicensed` y la URL oficial correspondiente.

Incoterms® y materiales propietarios como las notas explicativas protegidas de la WCO permanecen como referencias cuando corresponda. No ICC rule text se incorpora al archivo ni se usa la política de preservación para copiar contenido privado protegido.
