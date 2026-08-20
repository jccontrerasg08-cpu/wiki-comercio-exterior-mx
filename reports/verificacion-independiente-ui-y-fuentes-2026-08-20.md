---
title: "Verificación independiente de UI y fuentes primarias"
date: 2026-08-20
scope: "Wiki Comercio Exterior MX, interfaz desplegada y lote prioritario de fuentes oficiales"
---

# Verificación independiente de UI y fuentes primarias

## Propósito y alcance

Esta ejecución contrasta la wiki mediante dos canales independientes: la representación en navegador y las solicitudes HTTP directas. El objetivo es comprobar que la interfaz publicada responde correctamente y que las fuentes prioritarias siguen siendo identificables y accesibles. El resultado **no equivale** a un dictamen de vigencia jurídica: la disponibilidad de una URL, un estado HTTP 200 o la coincidencia de un título no sustituyen la revisión de reformas, transitorios, texto consolidado ni autoridad competente.

## Resumen ejecutivo

| Dimensión | Resultado | Alcance de la conclusión |
|---|---|---|
| Wiki desplegada | Confirmada | La portada y `stylesheets/extra.css` devolvieron HTTP 200; el navegador mostró la jerarquía, ruta operativa y accesos principales. |
| UI y movimiento | Confirmada | El PR #52 fue integrado; el repositorio superó 177 pruebas, build estricto y comprobación de compatibilidad/accesibilidad. |
| Identidad de fuentes | Confirmada por revisión paralela | Doce fuentes primarias se reportaron como HTTP 200 e identificables en una comprobación independiente paralela. |
| Captura HTTP cruda desde sandbox | Parcial | Cámara de Diputados falló por TLS, dos `getDoc` de SIDOF agotaron tiempo y el host DOF presentó un certificado no coincidente. Estos son límites de transporte del entorno, no pruebas de que el documento sea inválido. |
| Hash contra emisor oficial | No concluido en esta ejecución | La descarga completa desde algunos emisores quedó limitada por los errores anteriores. Los hashes publicados por la wiki siguen siendo evidencia de preservación, pero requieren una descarga completa reproducible desde el emisor o un canal alterno para volver a cotejarlos. |
| Vigencia jurídica | No concluida por HTTP | Debe confirmarse mediante el instrumento, sus reformas, transitorios y la fecha del caso consultado. |

## Capturas visuales y evidencia de interfaz

La portada de [Wiki Comercio Exterior MX](https://jccontrerasg08-cpu.github.io/wiki-comercio-exterior-mx/) se abrió en navegador y mostró la cabecera, hero, llamadas a la acción, ruta de cinco pasos, acceso de exportación, rutas por problema y bloques de trazabilidad. La estructura se mantuvo legible en modo oscuro. Las comprobaciones HTTP independientes devolvieron los siguientes resultados:

| Recurso desplegado | HTTP | Tipo | Conclusión |
|---|---:|---|---|
| [Portada de la wiki](https://jccontrerasg08-cpu.github.io/wiki-comercio-exterior-mx/) | 200 | `text/html; charset=utf-8` | El sitio publicado está disponible. |
| [Hoja de estilos propia](https://jccontrerasg08-cpu.github.io/wiki-comercio-exterior-mx/stylesheets/extra.css) | 200 | `text/css; charset=utf-8` | El recurso de UI se sirve desde el despliegue. |

El refinamiento de interfaz integrado en el PR #52 no añadió dependencias ni JavaScript. Limita el hover a dispositivos con puntero fino, conserva el foco sin desplazamiento, añade presión breve a controles activables y desactiva traslación/escala bajo `prefers-reduced-motion`.

> **Límite de captura.** El PDF de LIGIE de Cámara de Diputados se abrió por URL, pero el visor de navegador no entregó imagen ni texto extraíble. Por ello esa acción no se usa como prueba visual del contenido. La identidad de LIGIE se respalda en la comprobación paralela y el manifiesto de la wiki, no en esa captura fallida.

## Captura de asiento SIDOF

El navegador abrió [SIDOF 5777199](https://sidof.segob.gob.mx/notas/5777199) y mostró la identidad **“Reglas Generales de Comercio Exterior para 2026 y Anexo 13”**, el emisor **Poder Ejecutivo / Secretaría de Hacienda y Crédito Público**, publicación **27-12-2025**, y enlaces para `.doc`, imagen digitalizada y versión electrónica del diario.

La fuente advierte expresamente que su conversión HTML puede omitir tablas, caracteres u objetos. La arquitectura actual de la wiki recoge correctamente ese límite: para detalle documental debe consultarse la imagen digitalizada, la edición electrónica o el archivo oficial disponible desde el asiento, sin tratar el HTML como una representación exhaustiva.

## Lote de fuentes prioritarias

La revisión paralela independiente confirmó la disponibilidad e identidad de cuatro documentos de Cámara de Diputados, siete asientos SIDOF y el decreto promulgatorio del T-MEC. El CSV detallado se conserva como artefacto de auditoría entregable; el siguiente cuadro lista la referencia oficial verificada sin depender de una ruta externa al sitio.

| Grupo | Recurso oficial | Identidad confirmada | Resultado paralelo |
|---|---|---|---|
| Marco aduanero | [Ley Aduanera](https://www.diputados.gob.mx/LeyesBiblio/pdf/LAdua.pdf) | Ley Aduanera — Cámara de Diputados | Confirmada |
| Marco aduanero | [Reglamento de la Ley Aduanera](https://www.diputados.gob.mx/LeyesBiblio/regley/Reg_LAdua.pdf) | Reglamento de la Ley Aduanera | Confirmada |
| Clasificación | [LIGIE 2022](https://www.diputados.gob.mx/LeyesBiblio/pdf/LIGIE_2022.pdf) | Ley de los Impuestos Generales de Importación y de Exportación | Confirmada |
| Política comercial | [Ley de Comercio Exterior](https://www.diputados.gob.mx/LeyesBiblio/pdf/LCE.pdf) | Ley de Comercio Exterior | Confirmada |
| RGCE | [SIDOF 5777199](https://sidof.segob.gob.mx/notas/5777199) | RGCE 2026 y Anexo 13 | Confirmada |
| RGCE | [SIDOF 5777997](https://sidof.segob.gob.mx/notas/5777997) | Anexo 1 de RGCE 2026 | Confirmada |
| RGCE | [SIDOF 5778101](https://sidof.segob.gob.mx/notas/5778101) | Anexo 2 de RGCE 2026 | Confirmada |
| RGCE | [SIDOF 5778241](https://sidof.segob.gob.mx/notas/5778241) | Anexos 3–12 y 14–20 de RGCE 2026 | Confirmada |
| RGCE | [SIDOF 5778300](https://sidof.segob.gob.mx/notas/5778300) | Anexos 21–30 de RGCE 2026 | Confirmada |
| RGCE | [SIDOF 5787425](https://sidof.segob.gob.mx/notas/5787425) | Primera modificación a RGCE 2026 | Confirmada |
| Operación digital | [SIDOF 5786598](https://sidof.segob.gob.mx/notas/5786598) | Decreto de Ventanilla Única de Trámites de Comercio Exterior | Confirmada |
| Tratados | [Decreto promulgatorio T-MEC](https://www.dof.gob.mx/2020/SRE/T_MEC_290620.pdf) | T-MEC — DOF, 29-jun-2020 | Confirmada |

## Resultados del transporte HTTP crudo desde sandbox

La prueba de cabeceras HTTP con redirecciones y límite de doce segundos permitió distinguir incidentes de transporte de una afirmación sobre autoridad o vigencia.

| Emisor o ruta | Resultado HTTP crudo | Interpretación correcta |
|---|---|---|
| Cuatro PDFs de Cámara de Diputados | Error TLS `SSL_ERROR_SYSCALL` | El entorno no pudo negociar la conexión en esta ruta; no demuestra que los documentos sean inexistentes o incorrectos. |
| SIDOF `getDoc/5777997`, `5778101`, `5778241`, `5787425`, `5786598` | 200, `application/doc` | Las cabeceras confirmaron una ruta directa de documento disponible. |
| SIDOF `getDoc/5777199`, `5778300` | Límite de doce segundos sin bytes | La respuesta no llegó dentro del umbral de captura; el asiento HTML sí fue confirmado por navegador y revisión paralela. |
| DOF T-MEC | Error de certificado: el nombre no coincidió con `www.dof.gob.mx` | No se desactivó la validación TLS; el resultado se mantiene como atención de transporte, no como falla del tratado. |

## Calidad de parseo y organización en la wiki

La wiki separa correctamente cuatro capas que no deben confundirse: fuente primaria del emisor, copia preservada en release, manifiesto con hash y explicación editorial. Asimismo, las guías nuevas de consulta distinguen publicación jurídica, consolidado, portal operativo y evidencia preservada. Esa taxonomía es apropiada para evitar que una URL disponible se presente indebidamente como texto vigente o que una copia de evidencia se presente como autoría propia.

Para mantener este modelo, toda incorporación futura debe registrar al menos: identificador estable, título oficial, emisor, URL de origen, formato, fecha de publicación o corte, hash si se preservan bytes, estatus de extracción y advertencia temporal. Las tablas de la biblioteca ya exponen estos campos de manera legible; los manifiestos y reportes derivados los mantienen como datos estructurados.

## Recomendaciones de seguimiento

1. Reintentar la comprobación de hash desde un entorno que negocie TLS correctamente con Cámara de Diputados y DOF, sin deshabilitar la validación de certificado.
2. Mantener las advertencias de SIDOF sobre conversión HTML y enlazar siempre a imagen digitalizada o documento oficial cuando tablas, anexos u objetos sean materiales.
3. Conservar `HTTP 200`, identidad de documento, hash preservado y vigencia jurídica como controles separados dentro de cada reporte.
4. Versionar las futuras capturas con fecha, método, entorno de transporte y resultado para que un fallo temporal no se convierta en afirmación sobre el derecho aplicable.

## Referencias

[1] [Biblioteca de publicaciones oficiales preservadas](../catalog/publicaciones-oficiales.md)

[2] [SIDOF 5777199 — RGCE 2026 y Anexo 13](https://sidof.segob.gob.mx/notas/5777199)

[3] [Portada desplegada de Wiki Comercio Exterior MX](https://jccontrerasg08-cpu.github.io/wiki-comercio-exterior-mx/)

[4] [PR #52 — Refinar respuesta de interfaz y movimiento accesible](https://github.com/jccontrerasg08-cpu/wiki-comercio-exterior-mx/pull/52)
