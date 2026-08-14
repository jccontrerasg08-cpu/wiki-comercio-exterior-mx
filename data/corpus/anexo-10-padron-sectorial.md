# Anexo 10 — Padrón de Importadores de Sectores Específicos y Padrón de Exportadores Sectorial (RGCE 2026)

**Fuente oficial:** Anexo 10 de las RGCE para 2026, SAT / DOF 14-01-2026
**Fundamento:** Art. 59, fracción IV de la Ley Aduanera; arts. 82-87 del Reglamento; reglas 1.3.1., 1.3.2., 1.3.4. de las RGCE 2026
**URL oficial:** https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/documentos2026/rgce/anexos/Anexo10delasRGCEpara2026.pdf

> **Nota sobre volumen:** El Anexo 10 lista fracciones arancelarias específicas de la TIGIE para cada sector. Las fracciones completas no se transcriben aquí (son miles de líneas); este archivo documenta la **estructura de sectores**, los requisitos de inscripción, y los sectores de mayor relevancia para detección de riesgo y cumplimiento. Para verificar si una fracción arancelaria específica requiere Padrón Sectorial, consultar directamente el Anexo 10 oficial en la URL de arriba.

---

## ¿Qué es el Padrón de Importadores de Sectores Específicos?

Es un requisito adicional al Padrón General de Importadores (art. 59, fracción IV, Ley Aduanera). Las empresas que importen mercancías de los sectores listados en el Anexo 10 **deben estar inscritas en el sector correspondiente antes de realizar la importación**. Su ausencia impide el despacho aduanero y es causal de embargo precautorio.

**La inscripción se determina por fracción arancelaria** — es fundamental clasificar correctamente la mercancía antes de intentar importar.

---

## Estructura del Anexo 10

El Anexo 10 tiene dos apartados:

**Apartado A — Padrón de Importadores de Sectores Específicos** (16 sectores):

| Sector | Denominación | Nota |
|---|---|---|
| 1 | Productos químicos | Sin documentación adicional a ficha 5/LA |
| 2 | Radiactivos y nucleares | Control estricto SENER/CNSNS |
| 3 | Precursores químicos y químicos esenciales | Sin documentación adicional a ficha 5/LA |
| 4 | Armas de fuego y sus partes, refacciones, accesorios y municiones | Sin documentación adicional a ficha 5/LA |
| 5 | Explosivos y material relacionado con explosivos | Sin documentación adicional a ficha 5/LA |
| 6 | Sustancias químicas, materiales para usos pirotécnicos y artificios relacionados | Sin documentación adicional a ficha 5/LA |
| 7 | Las demás armas y accesorios; armas blancas; explosores | Sin documentación adicional a ficha 5/LA |
| 8 | Máquinas, aparatos, dispositivos y artefactos relacionados con armas y otros | Sin documentación adicional a ficha 5/LA |
| 9 | Cigarros | Requiere licencia sanitaria COFEPRIS y estar en Catálogo de Claves MULTI-IEPS |
| **10** | **Calzado** | **Documentación adicional (RFC de socios/accionistas en txt)** |
| **11** | **Textil y confección** | **Todas las fracciones de los Capítulos 50 a 63 de la TIGIE; documentación adicional** |
| **12** | **Alcohol etílico** | **Licencia sanitaria COFEPRIS; Catálogo MULTI-IEPS** |
| **13** | **Hidrocarburos y combustibles** | **Permiso SENER; documentación adicional** |
| **14** | **Siderúrgico** | **Documentación adicional (socios, instalaciones, procesos productivos)** |
| **15** | **Productos siderúrgicos** | **Documentación adicional** |
| **16** | **Automotriz** | **Documentación adicional** |

**Apartado B — Padrón de Exportadores Sectorial** (sectores con controles de exportación):

| Sector | Denominación |
|---|---|
| 1 | Alcohol, alcohol desnaturalizado y mieles incristalizables |
| 2 | Bebidas alcohólicas fermentadas (vinos) |
| 3 | Bebidas alcohólicas destiladas (licores) |
| 4 | Cigarros y tabacos labrados |
| 5 | Minerales de hierro y sus concentrados |
| 6 | Textil y confección |

---

## Sectores críticos para análisis de riesgo (ML/IA)

### Sector 10 — Calzado
- **Fracciones:** Partidas 64.01 a 64.05 de la TIGIE (calzado completo); la partida 64.06 (partes de calzado) puede ser usada indebidamente para evadir el padrón (ver criterio 4/LA/PI en `criterios-anam-sat.md`).
- **Riesgo:** Subvaluación y clasificación indebida como "partes" (64.06) en lugar de calzado completo; precio estimado SHCP activo sobre estas fracciones.
- **Documentación adicional para inscripción:** RFC válido de socios, accionistas, asociados y representantes legales en archivo txt.

### Sector 11 — Textil y Confección
- **Fracciones:** TODAS las fracciones de los **Capítulos 50 a 63** de la TIGIE.
- **Riesgo:** Uno de los sectores más vigilados por medidas anti-dumping (cuotas compensatorias) y por el uso indebido del Recinto Fiscalizado Estratégico (práctica indebida 5/LA/PI — ver `criterios-anam-sat.md`).
- **Documentación adicional:** RFC de socios en txt, instrumentos protocolizados, documentación de establecimientos.
- **Requisito extra para RFE:** No pueden destinarse mercancías terminadas (con características esenciales de textil/calzado completo) a RFE para "elaboración/transformación" si no van a ser transformadas realmente.

### Sector 12 — Alcohol Etílico
- **Riesgo:** Mezclas con otras sustancias para importar como producto diferente (paralelo al criterio de azúcar, 3/LA/PI).
- **Documentación:** Licencia sanitaria COFEPRIS; inscripción en Catálogo de Claves de Marcas MULTI-IEPS.

### Sector 13 — Hidrocarburos y Combustibles
- **Fracciones:** Petrolíferos, gas natural, butano/propano, aceite diésel y mezclas.
- **Nota:** Los petrolíferos no pueden sujetarse a los regímenes de importación temporal IMMEX, elaboración en recinto fiscalizado ni Recinto Fiscalizado Estratégico (art. 108, art. 135, art. 135-B de la Ley Aduanera).
- **Requiere:** Permiso SENER para importación.

### Sectores 14 y 15 — Siderúrgico y Productos Siderúrgicos
- **Fracciones:** Acero en sus diversas presentaciones (planchas, láminas, tubos, varillas, etc.).
- **Riesgo:** Cuotas compensatorias activas para importaciones provenientes de China; alto riesgo de subvaluación.
- **Documentación adicional:** RFC de socios, accionistas, instalaciones de la empresa, capacidad productiva.

### Sector 16 — Automotriz
- **Fracciones:** Vehículos y partes específicas.
- **Nota:** Se interrelaciona con el criterio 10/LA/N (vehículos armados con autopartes importadas por separado no acreditan legal tenencia del vehículo) en `criterios-anam-sat.md`.

---

## Requisitos generales de inscripción (reglas 1.3.2. y 1.3.4. RGCE 2026)

Para **todos los sectores**:
- Estar inscrito y activo en el Padrón General de Importadores.
- RFC activo con e.firma vigente.
- Constancia de cumplimiento de obligaciones fiscales (art. 32-D CFF).

Para sectores **10, 11, 12, 13, 14, 15 y 16** (más vigilados) — documentación adicional exigida en la ficha de trámite del Anexo 2:
- Archivo de texto plano (txt) con nombre completo y RFC válido de todos los socios, accionistas, asociados y representantes legales actuales.
- Archivos digitalizados de instrumentos protocolizados que comprueben dichas relaciones.
- Si hay socios/accionistas residentes en el extranjero (no obligados a RFC): número de folio de la solicitud presentada en Mi Portal con Forma 96 "Relación de Socios Residentes en el Extranjero".

**Resolución:** 10 días hábiles para que el SAT resuelva la solicitud de inscripción. Cualquier error reinicia el plazo.

---

## Causales de suspensión (art. 84 Reglamento + regla 1.3.3. RGCE 2026)

- Irregularidades o inconsistencias en el RFC.
- Fusión/escisión con desaparición del RFC.
- Cambio de denominación sin actualizar el Padrón.
- Resolución firme por infracción de los arts. 176, 177 o 179 de la Ley Aduanera.
- **Nueva 2026 — Fracción XLIX:** Omisión o error en la cuenta aduanera de garantía o carta de crédito del art. 86-A, fracción III.
- **Nueva 2026 — Fracción L:** Resolución firme por emisión de CFDI falsos (art. 49 Bis del CFF).

---

## Relación con otros archivos de esta base de conocimiento

- **`criterios-anam-sat.md`:** Criterios 4/LA/PI (calzado, Sec. 10) y 5/LA/PI (textil/calzado, Sec. 11) — prácticas indebidas específicas de estos sectores.
- **`tigie-nico-notas.md`:** La fracción arancelaria/NICO determina qué sector del Anexo 10 aplica.
- **`rgce-2026.md`:** Regla 1.3.2. (inscripción al Padrón Sectorial); regla 1.3.3. (causales de suspensión 2026); regla 1.3.4. (procedimiento).
- **`ley-aduanera.md`:** Art. 59, fracción IV (base legal del Padrón Sectorial); art. 151 (embargo precautorio cuando no se cuenta con el padrón requerido).
