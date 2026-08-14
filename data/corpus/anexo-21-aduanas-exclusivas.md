# Anexo 21 — Aduanas Exclusivas para Tramitar el Despacho Aduanero de Determinado Tipo de Mercancías (RGCE 2026)

**URL oficial:** https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/documentos2026/rgce/anexos/Anexo21delasRGCEpara2026.pdf
**Publicado:** 15-01-2026 | **DOF:** 15-01-2026
**Portal de actualizaciones:** https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/normatividad_rmf_rgce2026.html
**Fundamento:** Regla 2.4.x. de las RGCE 2026

## Cómo actualizar
1. Descargar el PDF desde la URL oficial.
2. Verificar si se agregaron mercancías o si cambiaron las aduanas exclusivas designadas.

## Contenido y lógica para el chatbot

### Árbol de decisión
```
Usuario quiere importar/exportar una mercancía específica:
    ↓
Obtener fracción arancelaria / NICO
    ↓
¿Aparece en el Anexo 21?
    SÍ → Solo puede despacharse en la aduana exclusiva ahí designada.
         Verificar su horario en el Anexo 4 (`anexo-04-horarios-aduanas.md`)
         No aplica ni siquiera el beneficio de "cualquier aduana" del OEA
    NO → Puede despacharse en la aduana de preferencia del importador
         (o la de adscripción de su agente aduanal)
```

### Categorías típicas y sus aduanas exclusivas (verificar PDF oficial):

| Tipo de mercancía | Aduanas exclusivas habituales |
|---|---|
| Vehículos nuevos (importación definitiva por particular) | Manzanillo, Lázaro Cárdenas, Altamira, Veracruz + aduanas fronterizas designadas según país de origen |
| Cigarros y tabacos labrados | Aduanas fronterizas designadas |
| Bebidas alcohólicas (a granel) | Aduanas con instalaciones de control volumétrico |
| Precursores químicos y químicos esenciales | Aduanas con capacidad de análisis químico (laboratorio SAT) |
| Explosivos y materiales bélicos | Aduanas autorizadas por SEDENA |
| Material radiactivo | Aduanas designadas (control SENER/CNSNS) |
| Retorno de vehículos temporales de residentes en el extranjero | Cualquier aduana con sección habilitada para vehículos |
| Importación de caballos de carrera | Aduanas específicas con instalaciones veterinarias |

### Nota importante para OEA (Operador Económico Autorizado)
El beneficio de "despacho en cualquier aduana" (regla 7.3.3., fracción I) no aplica cuando la fracción arancelaria aparece en el Anexo 21. Las empresas OEA también están obligadas a despachar en la aduana exclusiva designada para esas mercancías.
