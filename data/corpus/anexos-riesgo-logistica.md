# Anexos 17, 19, 21, 27 y 29 — Riesgo, Restricciones y Cálculo de Contribuciones (RGCE 2026)

**Fuente oficial:** SAT / DOF 14-01-2026 (publicación de Anexos 3-20) y DOF 15-01-2026 (Anexos 21-30)
**URLs base de descarga:**
- Anexo 17: https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/documentos2026/rgce/anexos/Anexo17delasRGCEpara2026.pdf
- Anexo 19: https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/documentos2026/rgce/anexos/Anexo19delasRGCEpara2026.pdf
- Anexo 21: https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/documentos2026/rgce/anexos/Anexo21delasRGCEpara2026.pdf
- Anexo 27: https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/documentos2026/rgce/anexos/Anexo27delasRGCEpara2026.pdf
- Anexo 29: https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/documentos2026/rgce/anexos/Anexo29delasRGCEpara2026.pdf

> **Nota de estructura:** Este archivo reúne cinco anexos que son catálogos de fracciones arancelarias. No se transcriben las fracciones completas (son cientos a miles de entradas); en su lugar se documenta la lógica operativa y los casos de uso del chatbot para cada uno.

---

## ANEXO 17 — Mercancías por las que NO procederá el tránsito internacional por territorio nacional

**Propósito:** Lista las fracciones arancelarias de la TIGIE cuya mercancía **no puede circular en tránsito internacional** a través de México (art. 131 de la Ley Aduanera + regla 4.6.1. de las RGCE 2026).

**Lógica de uso para el chatbot:**
- Si un usuario pregunta si puede hacer tránsito internacional de una mercancía específica, verificar su fracción arancelaria contra el Anexo 17.
- Si la fracción aparece en el Anexo 17 → **NO procede el tránsito internacional**. La mercancía debe despacharse definitivamente o destinarse a otro régimen, pero no puede transitar entre la frontera norte y la frontera sur (o viceversa) sin importarse.
- Típicamente incluye mercancías de alto riesgo para la seguridad pública, controladas, o sujetas a cuotas compensatorias que se evitarían con el tránsito.

**Caso típico de uso:**
> Usuario: "¿Puedo hacer tránsito internacional de [descripción de mercancía con fracción 6309.00.01 — ropa usada] de Laredo a Guatemala?"
> → Verificar Anexo 17. Las fracciones de ropa usada generalmente aparecen en este Anexo (alto riesgo de evasión de cuotas compensatorias y NOM). Si aparece → No procede.

**Complementario:** Anexo 11 (rutas fiscales para tránsito internacional Ensenada/Guaymas–EUA) y Anexo 15 (plazos máximos de traslado en tránsitos).

---

## ANEXO 19 — Datos inexactos, falsos u omitidos que actualizan la infracción del artículo 184, fracción III de la Ley

**Propósito:** Lista exhaustiva de los **datos específicos del pedimento** que, al ser declarados de forma inexacta, falsa u omitida, activan automáticamente la multa del art. 185, fracción II de la Ley (porcentaje del valor de las mercancías).

**Fundamento:** Art. 184, fracción III de la Ley Aduanera (infracción por datos inexactos o falsos); regla 3.7.25., segundo párrafo de las RGCE 2026.

**Datos que típicamente aparecen en el Anexo 19 (basado en versiones anteriores y criterios vigentes):**
- Valor en aduana de la mercancía.
- Descripción de la mercancía.
- País de origen.
- Fracción arancelaria declarada.
- Número de identificación comercial (NICO).
- Nombre o razón social del importador/exportador.
- RFC del importador/exportador.
- Nombre o razón social del proveedor extranjero.
- Domicilio del proveedor extranjero.
- Número de factura.

**Lógica de uso para el chatbot:**
- El Anexo 19 define qué errores en el pedimento **no se benefician** de la corrección espontánea sin multa (rectificación espontánea sin sanción aplica para datos **no** listados en el Anexo 19).
- La práctica indebida 4/LA/PI (calzado con valor diferente al CFDI — ver `criterios-anam-sat.md`) explícitamente activa la multa del art. 185-II porque el valor en aduana aparece en el Anexo 19.

**Caso típico de uso:**
> Usuario: "¿Puedo rectificar el pedimento si me equivoqué en el valor declarado?"
> → Si el valor en aduana aparece en el Anexo 19, la rectificación conlleva la multa del art. 185-II (no hay corrección sin sanción). Solo si la rectificación se hace ANTES de activar el mecanismo de selección automatizado aplica la corrección libre (art. 89 de la Ley).

---

## ANEXO 21 — Aduanas exclusivas para tramitar el despacho aduanero de determinado tipo de mercancías

**Propósito:** Lista las aduanas que son las **únicas autorizadas** para despachar ciertos tipos de mercancías. Implica que aunque una empresa tenga autorización para despachar en cualquier aduana (beneficio OEA — regla 7.3.3.), para las mercancías del Anexo 21 está obligada a usar la aduana exclusiva designada.

**Fundamento:** Regla 2.4.x. de las RGCE 2026.

**Tipos de mercancías que típicamente tienen aduana exclusiva (basado en versiones anteriores):**

| Tipo de mercancía | Aduana(s) exclusiva(s) habituales |
|---|---|
| Vehículos automotores nuevos (importación definitiva particular) | Aduana de Manzanillo, Lázaro Cárdenas, Altamira, Veracruz; aduanas fronterizas designadas según origen |
| Cigarros y tabacos labrados | Aduanas fronterizas específicas |
| Precursores químicos y sustancias controladas | Aduanas interiores o específicas según autorización |
| Sustancias peligrosas / explosivos | Aduanas con instalaciones especiales |
| Mercancías siderúrgicas en ciertos tráficos | Aduanas marítimas (Manzanillo, Veracruz, Lázaro Cárdenas, Altamira) |
| Pirotecnia y artificios | Aduanas designadas por SEDENA |

**Lógica de uso para el chatbot:**
- Cuando un usuario planifica importar/exportar mercancías de los sectores del Anexo 10 o mercancías de alto riesgo, verificar primero el Anexo 21.
- Si la fracción arancelaria aparece en el Anexo 21 → el despacho debe hacerse en la aduana ahí designada, no en la aduana del importador ni en la más cercana.
- Cruzar con el Anexo 4 (horarios) para saber en qué horario opera esa aduana específica.

---

## ANEXO 27 — Fracciones arancelarias de la TIGIE y NICO por cuya importación NO se está obligado al pago del IVA

**Propósito:** Catálogo de fracciones arancelarias exentas de IVA a la importación, conforme al art. 25 de la Ley del IVA y art. 2-A de la misma.

**Fundamento:** Arts. 25 y 2-A de la Ley del Impuesto al Valor Agregado; regla 5.2.x de las RGCE 2026; art. 52, párrafo final de la Ley Aduanera (las NOMs son RRNA).

**Categorías habituales de mercancías exentas de IVA a la importación (basado en el art. 25 de la Ley del IVA y versiones anteriores del Anexo 27):**

| Categoría | Lógica legal |
|---|---|
| Alimentos en estado natural (frutas, verduras, cárnicos, leche) | Art. 2-A Ley IVA (tasa 0%); en importación = exención |
| Medicamentos en general (fracciones específicas) | Art. 2-A Ley IVA (tasa 0%) |
| Maquinaria y equipo de cierto tipo para producción | Exenciones específicas |
| Libros, periódicos y revistas | Art. 9, fracción II Ley IVA / exención |
| Oro, plata y platino en ciertas presentaciones | Exenciones específicas |
| Equipo médico hospitalario | Regla RGCE específica + art. 9 Ley IVA |
| Semillas y animales en estado natural (agropecuario) | Art. 2-A Ley IVA |

**Lógica de uso para el chatbot (motor de cálculo de contribuciones):**
```
Para calcular las contribuciones de una importación:
1. Obtener la fracción arancelaria / NICO
2. Verificar si aparece en el Anexo 27 → si SÍ: IVA = $0
3. Si NO aparece en el Anexo 27 → IVA = 16% sobre (valor en aduana + IGI + DTA)
4. Verificar si la fracción está en el Anexo 9 (exenta de IGI también)
5. Verificar si aplica algún trato preferencial de TLC (T-MEC, UE, etc.)
```

**Nota importante para la modalidad IMMEX/IVA-IEPS:**
Las empresas con Registro en el Esquema de Certificación, modalidad IVA e IEPS, pueden importar temporalmente sin pagar el IVA (beneficio de flujo de caja). Las mercancías que pueden hacerlo bajo ese esquema están listadas en el **Anexo 28** (no en el Anexo 27 — el 27 es para exenciones permanentes por naturaleza de la mercancía; el 28 es para el esquema de certificación).

---

## ANEXO 29 — Mercancías que NO pueden destinarse a regímenes especiales

**Propósito:** Lista las fracciones arancelarias que están **prohibidas** de destinarse a cualquiera de estos regímenes:
1. Importación temporal para elaboración, transformación o reparación en programas de maquila o de exportación (IMMEX).
2. Depósito fiscal.
3. Elaboración, transformación o reparación en recinto fiscalizado.
4. Recinto fiscalizado estratégico (RFE).

**Fundamento:** Art. 123 de la Ley Aduanera (mercancías que no pueden ser objeto del régimen de depósito fiscal); reglas de los Capítulos 4.3., 4.5., 4.7. y 4.8. de las RGCE 2026.

**Tipos de mercancías que típicamente aparecen en el Anexo 29:**

| Tipo | Razón |
|---|---|
| Petrolíferos (gasolinas, diésel, gas LP, combustóleo) | Art. 108, último párrafo + art. 135 + art. 135-B de la Ley Aduanera: los petrolíferos no pueden sujetarse a ninguno de estos regímenes |
| Ciertos aditivos para aceites lubricantes a granel | Se incorporó la fracción 3811.21.07 (aditivos para aceites lubricantes a granel) en la nueva sección F.II del Anexo 29 para 2026 (cambio respecto a 2025) — restricción específica para el régimen de depósito fiscal |
| Mercancías sujetas a cuotas compensatorias muy altas (ciertos textiles, calzado, azúcar) | Política de protección; se evita que usen los regímenes especiales como bypass |
| Materias primas de importación restringida | Control de insumos sensibles |
| Residuos peligrosos | Por razones ambientales y de seguridad |

**Lógica de uso para el chatbot:**
- Antes de recomendar o confirmar que una empresa puede importar temporalmente bajo IMMEX o destinar a depósito fiscal / RFE, verificar el Anexo 29.
- Si la fracción aparece en el Anexo 29 para el régimen que el usuario quiere usar → **no puede destinarse a ese régimen**; debe importarse definitivamente (con pago de IGI y cuotas compensatorias).
- Los petrolíferos son el caso más claro: están explícitamente excluidos por Ley (no solo por el Anexo 29).

**Caso típico de uso:**
> Usuario IMMEX: "¿Puedo importar temporalmente gasoil para usar en mis procesos productivos?"
> → NO. Los petrolíferos están excluidos del régimen IMMEX por el art. 108, último párrafo de la Ley Aduanera y aparecen en el Anexo 29. Deben importarse definitivamente.

---

## Cómo usar estos anexos en arquitectura de IA

Para un motor de decisiones de comercio exterior, la lógica de árbol es:

```
FRACCIÓN ARANCELARIA / NICO
        │
        ├─► ¿Aparece en Anexo 17? → SÍ: No procede tránsito internacional
        │
        ├─► ¿Aparece en Anexo 10? → SÍ: Requiere Padrón Sectorial específico
        │                                (ver `anexo-10-padron-sectorial.md`)
        │
        ├─► ¿Aparece en Anexo 29 para el régimen solicitado?
        │      → SÍ: No puede destinarse a ese régimen especial
        │
        ├─► ¿Aparece en Anexo 21? → SÍ: Solo puede despacharse en aduana exclusiva
        │
        ├─► ¿Aparece en Anexo 27? → SÍ: IVA = $0 a la importación
        │      → NO: IVA = 16% sobre (VA + IGI + DTA)
        │
        └─► Si hay error en pedimento con datos del Anexo 19 → multa art. 185-II
```

---

## Relación con otros archivos de esta base de conocimiento

- **`tigie-nico-notas.md`:** El punto de partida es siempre la fracción arancelaria/NICO.
- **`ley-aduanera.md`:** Art. 108 (petrolíferos excluidos de IMMEX); art. 123 (mercancías excluidas del depósito fiscal); art. 131 (tránsito internacional — base del Anexo 17); art. 184-III (infracción por datos inexactos — base del Anexo 19).
- **`rgce-2026.md`:** Regla 4.6.1. (tránsito internacional — remite al Anexo 17); regla 3.7.25. (datos inexactos — remite al Anexo 19); regla 5.2. (IVA — remite al Anexo 27).
- **`criterios-anam-sat.md`:** Criterio 4/LA/PI explícitamente menciona el Anexo 19 y los precios estimados; criterio 5/LA/PI menciona el uso indebido del RFE para mercancías que deberían despacharse definitivamente.
- **`noms-comercio-exterior.md`:** El Anexo 2.4.1 del Acuerdo de Reglas de la SE (NOMs) es otro catálogo por fracción arancelaria que debe cruzarse.
