# Anexo 24 — Sistema Automatizado de Control de Inventarios (SACI / SECIIT) — IMMEX y Regímenes Especiales

**Fuente oficial:** Anexo 24 de las RGCE para 2026, SAT / DOF 15-01-2026
**Fundamento legal:**
- Art. 59, fracción I de la Ley Aduanera (control de inventarios automatizado en forma continua)
- Art. 24, fracción IX del Decreto IMMEX
- Regla 4.3.1. de las RGCE 2026
**URL oficial:** https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/documentos2026/rgce/anexos/Anexo24delasRGCEpara2026.pdf

> **Contexto 2026:** El Anexo 24 pasó de ser una obligación de auditoría ocasional a un **sistema de vigilancia continua**. El SAT puede acceder al sistema de la empresa en tiempo real bajo el Plan Maestro 2026. La pregunta que el sistema debe responder en todo momento: *¿dónde está, o en qué se convirtió, cada unidad de mercancía importada temporalmente?*

---

## ¿Quiénes están obligados?

El sistema automatizado de control de inventarios es obligatorio para:
1. **Empresas con Programa IMMEX** (Decreto IMMEX) — la obligación principal.
2. Empresas que operen bajo **régimen de depósito fiscal**.
3. Empresas bajo **régimen de recinto fiscalizado estratégico (RFE)**.
4. Empresas que realicen **elaboración, transformación o reparación en recinto fiscalizado**.
5. Empresas con **Registro en el Esquema de Certificación (OEA / IVA-IEPS)** — en su modalidad SECIIT (Sistema Electrónico de Control de Inventarios para Importaciones Temporales), que es una versión más estricta.

---

## Nombres del sistema según el tipo de empresa

| Tipo de empresa | Sistema | Características |
|---|---|---|
| IMMEX sin certificación especial | **SACI** (Sistema Automatizado de Control de Inventarios) | Control interno, auditable por el SAT |
| IMMEX con Registro OEA / IVA-IEPS (Esquema de Certificación) | **SECIIT** (Sistema Electrónico de Control de Inventarios para Importaciones Temporales) | El SAT puede jalar datos directamente; no editable manualmente una vez registrado |

---

## Estructura del sistema — Catálogos y Módulos mínimos requeridos

### APARTADO A — Datos del contribuyente y Catálogos básicos
- **Datos generales:** Número de Programa IMMEX expedido por la SE, RFC, razón social, domicilio.
- **Catálogo de Materiales:** Descripción comercial del material importado temporalmente (insumos, materias primas, partes, componentes, empaques, etiquetas, envases, herramientas, maquinaria).
- **Catálogo de Productos:** Descripción comercial del producto terminado o semiterminado que resulta del proceso productivo.

### APARTADO B — Módulos operativos

**I. Módulo de información aduanera de entradas (importaciones temporales)**
- Clave del pedimento (tipo de operación).
- Fecha declarada en el pedimento.
- Fecha del pedimento.
- Fracción arancelaria / NICO.
- Cantidades importadas por unidad de medida.
- Número de serie, parte, marca y modelo (cuando aplique).
- Vinculación automática con el pedimento.

**II. Módulo de información sobre materiales utilizados (descarga / consumo)**
Este módulo descarga automáticamente la cantidad de cada mercancía **usando el método PEPS (Primeras Entradas, Primeras Salidas)**, descontando del pedimento de importación temporal más antiguo que contenga la mercancía a descargar. Registra:
- Fecha de descarga / consumo.
- Clave del pedimento origen.
- Cantidad consumida / descargada.
- Relación con el producto terminado (lista de materiales / bill of materials).

**III. Módulo de activo fijo (maquinaria y equipo)**
- Maquinaria, equipo, herramientas, instrumentos y moldes importados temporalmente.
- Período de depreciación conforme a la LISR.
- Seguimiento por activo individual.

**IV. Módulo de procesos**
- Descripción de los procesos productivos en los que se utilizan los materiales importados.
- Porcentajes de consumo / desperdicio / merma por proceso.
- Vinculación con los catálogos de materiales y productos.

**V. Módulo de reportes**
Debe permitir generar, como mínimo:
- Reporte de entrada de mercancías de importación temporal.
- Reporte de materiales utilizados en producción.
- Reporte de saldos pendientes de retorno/cambio de régimen.
- Reporte de activo fijo con estado de depreciación.
- Reportes que comprueben el cumplimiento de los requerimientos de información de las disposiciones aduaneras y de la propia autoridad (incluyendo declaración anual del art. 109 de la Ley Aduanera).

---

## Diferencias críticas SACI vs. SECIIT

| Característica | SACI (IMMEX sin certificación) | SECIIT (Empresas certificadas IVA/IEPS) |
|---|---|---|
| Edición posterior de registros | Posible con controles | **No posible** — datos inmutables |
| Acceso del SAT | Por requerimiento de auditoría | **Acceso en línea continuo** |
| Integración con SEA | Recomendada | **Obligatoria** |
| Nivel de detalle | Mínimo del Anexo 24 | Mayor granularidad; marcas, series, etc. |
| Consecuencia de fallas | Presunción de mercancía ilegal en México | Pérdida de la certificación + presunción de ilegalidad |

---

## Consecuencias de incumplimiento

La **falta o desactualización** del sistema de control de inventarios activa la presunción del art. 59, fracción I, último párrafo de la Ley Aduanera:

> *"En caso de incumplimiento a lo dispuesto en esta fracción se presumirá que las mercancías que sean propiedad del contribuyente o que se encuentren bajo su posesión o custodia y las que sean enajenadas por el contribuyente a partir de la fecha de la importación, análogas o iguales a las importadas, son de procedencia extranjera."*

Lo que implica:
- Determinación de créditos fiscales por IGI, IVA y DTA sobre todas las mercancías análogas.
- **Multas de $20,660.00 a $41,350.00** por no llevar el control automatizado (montos aproximados, verificar Anexo 13 RGCE 2026 para monto exacto actualizado 2026).
- Suspensión del Programa IMMEX.
- Inicio de PAMA con embargo precautorio.
- En casos graves, proceso penal por contrabando equiparado.

---

## Consideraciones prácticas para el chatbot

1. **El Anexo 24 no es una hoja de cálculo** — el SAT exige software especializado con trazabilidad de base de datos.
2. **PEPS es obligatorio** — no puede elegirse UEPS ni promedio ponderado para el control de inventarios aduaneros.
3. **Vigencia del programa** — el plazo de permanencia de la mercancía se computa desde la activación del mecanismo de selección automatizado (art. 173 del Reglamento; criterio 6/LA/N derogado pero incorporado en la Ley).
4. **Transferencias IMMEX** — cuando una empresa IMMEX transfiere mercancías a otra (art. 112 Ley Aduanera), ambas deben registrar la operación en sus sistemas Anexo 24.
5. **Maquinaria y equipo** — tiene su propio módulo porque su plazo de permanencia está vinculado a la vigencia del programa IMMEX (no al plazo de 18 meses de los insumos).
6. **Revisión recomendada** — efectuar una reconciliación del SACI vs. el sistema del SAT cada 12 meses, o inmediatamente después de migraciones de ERP, expansiones IMMEX, fusiones o cambio de agente aduanal.

---

## Relación con otros archivos de esta base de conocimiento

- **`ley-aduanera.md`:** Art. 59-I (obligación base); art. 109 (declaración anual de mermas/desperdicios IMMEX); art. 108 (plazos de permanencia de mercancías IMMEX).
- **`reglamento-ley-aduanera.md`:** Art. 79 (opción de control mediante registro de detallistas para ciertas operaciones); art. 173 (cómputo del plazo de permanencia).
- **`criterios-anam-sat.md`:** Criterio 4/LA/N (mermas no sujetas a régimen aduanero — distinción con desperdicios que sí deben registrarse y destruirse); criterio 6/LA/N (contenedores IMMEX solo para mercancías del mismo programa).
- **`rgce-2026.md`:** Regla 4.3.1. (obligación de Anexo 24 para IMMEX); Título 7 / regla 7.2.x (SECIIT para empresas certificadas); Anexo 30 (SCCCyG — el sistema complementario que lleva el estado de cuenta de créditos y garantías del IVA/IEPS diferido).
