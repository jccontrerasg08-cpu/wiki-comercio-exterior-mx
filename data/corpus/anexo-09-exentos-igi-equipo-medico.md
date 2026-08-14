# Anexo 9 — Mercancías Exentas de IGI y Equipo Médico sin Obligación de Inscripción al Padrón de Importadores (RGCE 2026)

**URL oficial:** https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/documentos2026/rgce/anexos/Anexo9delasRGCEpara2026.pdf
**Publicado:** 14-01-2026 | **DOF:** 14-01-2026
**Portal de actualizaciones:** https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/normatividad_rmf_rgce2026.html
**Fundamento:** Art. 61 de la Ley Aduanera; regla 3.3.1. de las RGCE 2026

## Cómo actualizar
1. Descargar el PDF desde la URL oficial.
2. Verificar si se agregaron o eliminaron fracciones arancelarias de la lista.
3. Si hay nuevas fracciones en la TIGIE (reformas al LIGIE), verificar si aplican a este Anexo.

## Contenido y uso para el chatbot

Contiene dos listas:

**Lista I — Mercancías exentas de IGI:**
Fracciones arancelarias de la TIGIE por cuya importación definitiva **no se paga el Impuesto General de Importación** (art. 61 de la LA o reglas específicas).

**Lista II — Equipo médico sin obligación de inscripción al Padrón de Importadores:**
Fracciones arancelarias de equipo médico que pueden importarse sin inscripción al Padrón de Importadores cuando el importador es una institución de salud o similar.

**Lógica de uso del motor de cálculo:**
- Verificar primero el Anexo 9 (exención de IGI) antes de calcular el IGI.
- Si la fracción aparece en Lista I → IGI = $0.
- Si la fracción no aparece aquí pero sí en el Anexo 27 → IVA = $0 (son cálculos independientes).
- Puede ser exento de IGI pero pagar IVA, o viceversa, o ninguno de los dos, o ambos.
