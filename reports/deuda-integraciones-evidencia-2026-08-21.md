# Evidencia para contratos de integración — 21 de agosto de 2026

## arancel-mx

**Repositorio canónico:** `jccontrerasg08-cpu/arancel-mx`.

La guía de consumo externo de arancel-mx declara que GitHub Releases mantiene la identidad canónica del dataset y que la capa de Vercel/Neon es de servicio, no la fuente de verdad. Para integraciones de datos recomienda fijar una release `data-YYYY.MM.DD`, verificar `manifest.json`, `SHA256SUMS` y la estructura del bundle, y conservar el tag, manifest, checksums, momento de ingesta y transformaciones downstream.

**Release observada:** `data-2026.08.17`, publicada el 17 de agosto de 2026. El bundle documentado contiene exactamente `arancel_mx.duckdb`, `arancel_mx.csv`, `arancel_mx.json`, `manifest.json`, `SHA256SUMS` y `official-sources.tar.gz`; el manifiesto usa schema v2. Los campos de consumo declarados incluyen `fraccion8`, `nico10`, `igi_text`, `ige_text` y procedencia. La guía establece que una consulta, sugerencia o comparación no es clasificación ni determinación jurídica.

## dof-diff-lab

**Repositorio canónico:** `jccontrerasg08-cpu/dof-diff-lab`.

Su README define el proyecto como monitor diario, informativo y trazable del DOF. La fuente primaria sigue siendo la publicación oficial; catálogos, etiquetas, hashes y resúmenes son derivados técnicos que no certifican autenticidad jurídica, vigencia ni efectos regulatorios. Conserva URL oficial, SHA-256, tamaño y metadatos mínimos, sin republicar contenido fuente.

**Estado observado:** `data/state/latest.json` del 20 de agosto de 2026, edición `matutina`, con `status: changed`, manifest de captura, `normalized_sha256` y `updated_at`. El repositorio documenta que `changed` es un estado de monitorización y que etiquetas o coincidencias de regla invitan a revisar la publicación, no confirman efectos jurídicos. La fecha de publicación se trata como fecha del índice oficial y las marcas de captura se guardan en UTC.
