from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, content: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content.rstrip() + "\n", encoding="utf-8")


def replace_once(path: str, old: str, new: str) -> None:
    text = read(path)
    if text.count(old) != 1:
        raise RuntimeError(f"{path}: expected exactly one replacement target, got {text.count(old)}")
    write(path, text.replace(old, new, 1))


# 1. Register primary IMMEX evidence before the administrative SNICE index.
registry_marker = "  - id: mx_snice_immex\n"
registry_insert = """  - id: mx_sidof_immex_reform_20241219
    jurisdiction: MEX
    title: Decreto de reforma al Programa IMMEX de 19 de diciembre de 2024
    url: https://sidof.segob.gob.mx/notas/5745788
    note_id: "5745788"
    authority: DOF / SIDOF
    evidence_class: primary_legal
    instrument_id: mx_programa_immex
    publication_date: 2024-12-19
    allowed_hosts: [sidof.segob.gob.mx, www.dof.gob.mx, dof.gob.mx]
    media_types: [text/html, application/pdf]
    harvest: true
    cadence_days: 365
    probe: *probe_html

  - id: mx_sidof_immex_reform_20250828
    jurisdiction: MEX
    title: Decreto de reforma al Programa IMMEX de 28 de agosto de 2025
    url: https://sidof.segob.gob.mx/notas/5766797
    note_id: "5766797"
    authority: DOF / SIDOF
    evidence_class: primary_legal
    instrument_id: mx_programa_immex
    publication_date: 2025-08-28
    allowed_hosts: [sidof.segob.gob.mx, www.dof.gob.mx, dof.gob.mx]
    media_types: [text/html, application/pdf]
    harvest: true
    cadence_days: 365
    probe: *probe_html

  - id: mx_sidof_immex_suspension_2026
    jurisdiction: MEX
    title: Aviso IMMEX de programas suspendidos por reporte anual 2025
    url: https://sidof.segob.gob.mx/notas/5792091
    note_id: "5792091"
    authority: DOF / SIDOF
    evidence_class: official_administrative
    instrument_id: mx_programa_immex
    publication_date: 2026-06-30
    allowed_hosts: [sidof.segob.gob.mx, www.dof.gob.mx, dof.gob.mx]
    media_types: [text/html, application/pdf]
    harvest: true
    cadence_days: 365
    probe: *probe_html

"""
registry = read("sources/registry.yaml")
if "mx_sidof_immex_reform_20241219" not in registry:
    replace_once("sources/registry.yaml", registry_marker, registry_insert + registry_marker)

# 2. Version the two latest normative IMMEX reforms without turning the 2026 notice into an amendment.
old_immex_instrument = """  - id: mx_programa_immex
    jurisdiction: MEX
    title: Programa IMMEX
    instrument_type: program
    status: partial
    publication_date: 2006-11-01
    effective_from: 2006-11-13
    effective_to: null
    current_through: 2026-08-15
    consolidated_source_id: mx_snice_immex
    events: []
"""
new_immex_instrument = """  - id: mx_programa_immex
    jurisdiction: MEX
    title: Programa IMMEX
    instrument_type: program
    status: partial
    publication_date: 2006-11-01
    effective_from: 2006-11-13
    effective_to: null
    current_through: 2026-08-15
    consolidated_source_id: mx_snice_immex
    events:
      - source_id: mx_sidof_immex_reform_20241219
        relation: amends
        effective_from: 2024-12-20
      - source_id: mx_sidof_immex_reform_20250828
        relation: amends
        effective_from: 2025-08-29
"""
replace_once("sources/instruments.yaml", old_immex_instrument, new_immex_instrument)

# 3. Reader-first IMMEX hub.
write(
    "docs/wiki/programas/immex.md",
    """---
title: "IMMEX"
description: "Guía operativa del Programa IMMEX: importación temporal, control de inventarios, retornos, Anexo 24, SCCCyG y reporte anual."
---

# IMMEX

El **Programa para el Fomento de la Industria Manufacturera, Maquiladora y de Servicios de Exportación (IMMEX)** permite realizar importaciones temporales vinculadas a procesos de elaboración, transformación, reparación o servicios de exportación, bajo las condiciones del Decreto IMMEX, la Ley Aduanera y las reglas aplicables.

No basta con identificar una empresa como “IMMEX” para concluir qué plazo, beneficio o sistema de control le corresponde. La mercancía, el régimen, el tipo de operación, la certificación de la empresa y la regla aplicable cambian el análisis.

## Ruta operativa

Una operación típica debe poder reconstruirse documentalmente desde la autorización y la entrada temporal hasta su salida o regularización:

1. **Autorización y mercancía.** Verificar que la operación esté dentro del Programa IMMEX autorizado y que la mercancía no caiga en una restricción o condición especial.
2. **Importación temporal.** Declarar correctamente pedimento, fracción arancelaria, NICO cuando corresponda, identificadores y demás datos exigibles.
3. **Control de inventarios.** Vincular la entrada aduanera con materiales, productos, procesos, salidas y saldos conforme al [Anexo 24](anexo-24-control-inventarios.md).
4. **Destino de la mercancía.** Documentar retorno, transferencia, destrucción, donación, cambio de régimen u otro destino jurídicamente procedente.
5. **Plazo.** Computarlo conforme al tipo de mercancía y al fundamento aplicable; no existe un único plazo IMMEX que sustituya el análisis de la Ley Aduanera, el Decreto y las RGCE.

Para el detalle arancelario conviene consultar la fuente oficial y la capa estructurada de `arancel-mx`; esta wiki no duplica listados completos de fracciones.

## Anexo 24: control de inventarios

El artículo 24, fracción IX del Decreto IMMEX obliga a llevar un control automatizado de inventarios conforme a las disposiciones del SAT. El Anexo 24 de las RGCE 2026 desarrolla la información mínima del sistema y distingue **tres apartados con alcances diferentes**.

Por eso, Anexo 24 no debe usarse como sinónimo de SECIIT. El SECIIT corresponde al supuesto específico del apartado B; los apartados A y C tienen estructuras y obligaciones propias. Consulta [Anexo 24: control de inventarios](anexo-24-control-inventarios.md).

## Anexo 30: SCCCyG

El [Anexo 30: SCCCyG](anexo-30-scccyg.md) regula información del **Sistema de Control de Cuentas de Créditos y Garantías**. Su función es distinta del control físico-documental del Anexo 24: se relaciona con cuentas de créditos fiscales y garantías dentro de los supuestos que las RGCE vinculan al sistema.

Ser titular de un Programa IMMEX, por sí solo, **no significa que el SCCCyG aplique a toda operación**. Primero se identifica el esquema fiscal/certificación y la regla que genera la cuenta de cargo o el descargo.

## Reporte anual y aviso 2026

El artículo 25 del Decreto IMMEX prevé un **reporte anual electrónico** respecto del ejercicio inmediato anterior, a más tardar el último día hábil de mayo, conforme a los términos aplicables.

El aviso publicado en el DOF el **30 de junio de 2026** identificó programas suspendidos por no haber presentado el reporte correspondiente al ejercicio 2025. Ese aviso establece, para ese ciclo, que quienes subsanen a más tardar el **último día hábil de agosto de 2026** pueden obtener el levantamiento de la suspensión; si no se regulariza, la cancelación definitiva opera a partir del **1 de septiembre de 2026**. Esta fecha es propia del aviso 2026 y no debe reutilizarse como calendario permanente para otros ejercicios.

## Reformas recientes

El Decreto IMMEX fue reformado el **19 de diciembre de 2024** y nuevamente el **28 de agosto de 2025**. Ambos decretos dispusieron entrada en vigor al día siguiente de su publicación. La reforma de agosto de 2025 modificó, entre otros elementos, el Anexo I del Decreto IMMEX.

Cuando una decisión dependa de una fracción concreta, se debe revisar el texto oficial vigente y su fecha efectiva; una lista copiada en una guía puede quedar desactualizada.

## Cómo verificar una operación

Antes de concluir que una operación cumple, conviene cruzar al menos:

- autorización/programa y modalidad IMMEX;
- fracción arancelaria y NICO aplicables;
- pedimentos de entrada y salida vinculados;
- plazo legal de permanencia;
- registros y descargos del Anexo 24;
- certificación o garantía fiscal cuando pueda activar SCCCyG;
- reformas y reglas vigentes para la fecha de la operación.

## Fuentes

- [SNICE — Programa IMMEX](https://www.snice.gob.mx/cs/avi/snice/immex.html)
- [DOF/SIDOF — reforma IMMEX del 19 de diciembre de 2024](https://sidof.segob.gob.mx/notas/5745788)
- [DOF/SIDOF — reforma IMMEX del 28 de agosto de 2025](https://sidof.segob.gob.mx/notas/5766797)
- [DOF/SIDOF — aviso de programas IMMEX suspendidos, 30 de junio de 2026](https://sidof.segob.gob.mx/notas/5792091)
- [DOF/SIDOF — RGCE 2026](https://sidof.segob.gob.mx/notas/5777199)
- [DOF/SIDOF — Anexos 21 a 30 de las RGCE 2026](https://sidof.segob.gob.mx/notas/5778300)

## Vigencia

Revisión editorial/jurídica efectuada el **15 de agosto de 2026**. El grafo local del Decreto IMMEX sigue marcado como `partial` porque todavía no versiona individualmente todas las reformas históricas; esta página no se usa por sí sola como documento temporal “current” del RAG.

## Ver también

[Anexo 24](anexo-24-control-inventarios.md) · [Anexo 30](anexo-30-scccyg.md) · [Pedimento y RGCE](../aduana/pedimento-rgce.md) · [TIGIE y NICO](../clasificacion/tigie-nico.md) · [PROSEC](prosec.md)
""",
)

# 4. Public Annex 24 guide.
write(
    "docs/wiki/programas/anexo-24-control-inventarios.md",
    """---
title: "Anexo 24: control de inventarios"
description: "Guía del Anexo 24 de las RGCE 2026: apartados A, B y C, SECIIT, PEPS, entradas, salidas, saldos y trazabilidad IMMEX."
---

# Anexo 24: control de inventarios

El **Anexo 24 de las RGCE 2026** establece la información mínima que debe contener el sistema automatizado de control de inventarios en los supuestos que remiten a este anexo. Su objetivo práctico es permitir relacionar las mercancías de comercio exterior con entradas, procesos, salidas y saldos de forma reconstruible.

Su lectura debe hacerse junto con el artículo 59, fracción I de la Ley Aduanera, el artículo 24, fracción IX del Decreto IMMEX y las reglas específicas de las RGCE que remiten a cada apartado.

## Tres apartados, no un solo sistema

| Apartado | Alcance resumido | Punto clave |
|---|---|---|
| **Apartado A** | Información mínima del sistema automatizado de control de inventarios vinculado a la regla 4.3.1. | Catálogos, módulo de aduanas y reportes para entradas, salidas, saldos y materiales utilizados. |
| **Apartado B** | Información que debe contener el **SECIIT** para el supuesto específico de la regla 7.1.4 señalado por el propio anexo. | Integra información electrónica del sistema corporativo, interfaces, conciliación y acceso en línea para la autoridad. |
| **Apartado C** | Información mínima del sistema para empresas con Registro en el Esquema de Certificación de Empresas. | Recibe electrónicamente información del apartado A y establece una ventana propia de actualización. |

La consecuencia importante es metodológica: **SECIIT es un supuesto del Anexo 24, no la definición completa del Anexo 24**.

## Apartado A: mínimo de control

El apartado A exige que el sistema permita cumplir el control de inventarios, comprobar retornos y mercancías pendientes de retorno, y generar información requerida por las disposiciones aduaneras y la autoridad.

Entre sus componentes mínimos aparecen catálogos de datos generales, materiales y productos; módulos de información aduanera de entradas y salidas; materiales utilizados; activo fijo; y reportes de entradas, salidas, saldos por fracción arancelaria y materiales utilizados.

Esto permite responder preguntas operativas básicas: **qué entró, bajo qué pedimento, qué se utilizó, qué salió y qué saldo permanece**.

## Apartado B: SECIIT

El apartado B corresponde al SECIIT en el supuesto que identifica el propio Anexo 24. El sistema recibe electrónicamente información proveniente del sistema corporativo, incluida la interfaz de entradas, salidas y movimientos de manufactura/ajustes.

La publicación 2026 establece que determinada información obtenida electrónicamente del sistema corporativo debe recibirse en el SECIIT en un plazo que **no exceda 24 horas** y que la información restante se incorpore a más tardar en el momento señalado por el propio anexo para el pedimento correspondiente. También prevé acceso en línea de la autoridad al SECIIT.

La inmutabilidad no es universal: el texto identifica **campos concretos** que, al provenir electrónicamente del sistema corporativo, no pueden modificarse dentro del SECIIT, con las excepciones que el mismo anexo señala. No debe convertirse esa regla de campo en la afirmación “todo dato del sistema es inmutable”.

## Apartado C: empresas con RECE

El apartado C se dirige al supuesto de empresas con Registro en el Esquema de Certificación de Empresas. La publicación 2026 exige recibir electrónicamente la información obligatoria y actualizar el sistema en un plazo que **no exceda 48 horas** en los términos definidos por el apartado; también contempla acceso en línea de la autoridad.

Las ventanas de 24 y 48 horas pertenecen a **supuestos distintos**. No deben aplicarse indistintamente a cualquier empresa IMMEX.

## Descargos y PEPS

El Anexo 24 utiliza el método **Primeras Entradas Primeras Salidas (PEPS)** en la mecánica de descargos que describe. En términos operativos, el sistema identifica los pedimentos de importación temporal que deben afectarse por retornos, transferencias, cambios de régimen y, cuando corresponde, mermas o desperdicios, siguiendo el orden y las condiciones del anexo.

Esto no sustituye la revisión del pedimento ni del plazo legal de permanencia. Un descargo informático correcto necesita corresponder con la operación aduanera que realmente ocurrió.

## Qué conviene conciliar

Una revisión útil cruza, como mínimo:

- pedimento y fecha de entrada;
- número de parte/material y unidad de medida;
- proceso o consumo registrado;
- pedimento/documento de salida o destino;
- cantidad descargada y saldo pendiente;
- activo fijo, desperdicios y transferencias cuando sean aplicables;
- evidencia de que los registros electrónicos cumplen el apartado A, B o C que realmente corresponde.

## Lo que no debe inferirse

El Anexo 24 **no prescribe una marca de ERP**, un proveedor de software o una arquitectura tecnológica específica. Tampoco convierte por sí mismo cada diferencia de inventario en una sanción, PAMA o consecuencia penal automática. Esas consecuencias, cuando existan, dependen del hecho concreto y de otras disposiciones legales.

Tampoco debe imponerse una “reconciliación anual” inventada como sustituto de los tiempos y registros que exige la norma. La frecuencia de controles internos adicionales puede ser una buena práctica, pero debe identificarse como práctica de gestión y no como texto del Anexo 24.

## Fuentes

- [DOF/SIDOF — Anexos 21 a 30 de las RGCE 2026](https://sidof.segob.gob.mx/notas/5778300)
- [DOF/SIDOF — RGCE 2026](https://sidof.segob.gob.mx/notas/5777199)
- [SAT — Normatividad RGCE 2026](https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/normatividad_rmf_rgce2026.html)
- [SNICE — Programa IMMEX](https://www.snice.gob.mx/cs/avi/snice/immex.html)

## Vigencia

El Anexo 24 de las RGCE 2026 fue publicado el **15 de enero de 2026**. Al corte de revisión del **15 de agosto de 2026**, el portal oficial del SAT muestra publicada la Primera Resolución de Modificaciones a las RGCE 2026 y modificaciones de los Anexos 5, 22 y 29; no muestra una modificación publicada del Anexo 24. Las versiones anticipadas deben distinguirse de las publicaciones en DOF.

## Ver también

[IMMEX](immex.md) · [Anexo 30: SCCCyG](anexo-30-scccyg.md) · [Pedimento y RGCE](../aduana/pedimento-rgce.md) · [TIGIE y NICO](../clasificacion/tigie-nico.md)
""",
)

# 5. Public Annex 30 guide.
write(
    "docs/wiki/programas/anexo-30-scccyg.md",
    """---
title: "Anexo 30: SCCCyG"
description: "Guía del Anexo 30 de las RGCE 2026 y del SCCCyG: cuentas de créditos y garantías, cargos, descargos, PEPS, plazos y saldos."
---

# Anexo 30: SCCCyG

El **Anexo 30 de las RGCE 2026** se refiere a la información del **Sistema de Control de Cuentas de Créditos y Garantías (SCCCyG)**. Es una capa de control fiscal distinta del inventario aduanero del Anexo 24.

En términos prácticos, el SCCCyG sirve para administrar cuentas relacionadas con **créditos fiscales o montos garantizados** en los esquemas a los que remiten las RGCE. Por ello, ser empresa IMMEX por sí solo **no significa que todo el flujo SCCCyG aplique**: primero debe identificarse la certificación, garantía, régimen y regla que generan la cuenta correspondiente.

## Qué información articula

La estructura del Anexo 30 contempla la información necesaria para integrar y afectar las cuentas del sistema, incluyendo, conforme al supuesto aplicable:

- inventario inicial;
- cuentas o cargos asociados a los montos controlados;
- informes de descargo;
- correcciones y movimientos previstos por el propio sistema;
- determinación del saldo que muestra el SCCCyG.

La guía no convierte estos conceptos en un formato universal fuera de los supuestos que las RGCE vinculan al sistema.

## Descargos y PEPS

La publicación vigente del Anexo 30 utiliza **PEPS** en la mecánica de descargo de las fracciones arancelarias reportadas en las cuentas de cargo. El objetivo es definir qué cargos se afectan primero al procesar los informes de descargo conforme a las disposiciones aplicables.

PEPS en SCCCyG y PEPS en el control de inventarios del Anexo 24 deben entenderse dentro de sus propios objetos de control: uno afecta cuentas fiscales/garantizadas y el otro forma parte de la trazabilidad de mercancías e inventarios.

## Plazos del sistema y plazo legal

El propio Anexo 30 advierte que el SCCCyG puede determinar plazos de retorno **de forma presuntiva**, por lo que el contribuyente debe computar el plazo conforme a las disposiciones legales vigentes que correspondan a su mercancía y operación.

En consecuencia, una fecha mostrada por el sistema sirve como dato de control; no sustituye la revisión de la Ley Aduanera, el Decreto IMMEX, las RGCE y el pedimento concreto.

## Qué significa el saldo

Los saldos reflejados en el SCCCyG **no implican una resolución definitiva** y quedan a salvo las facultades de comprobación de la autoridad. Tampoco debe invertirse esa regla para afirmar que cualquier saldo positivo demuestra por sí solo mercancía no declarada o genera automáticamente un procedimiento sancionador.

Si aparece una diferencia, la respuesta correcta es reconstruir cargos, informes de descargo, correcciones, pedimentos y fundamento antes de asignarle una consecuencia jurídica.

## Anexo 24 vs. Anexo 30

| Tema | Anexo 24 | Anexo 30 / SCCCyG |
|---|---|---|
| Objeto principal | Trazabilidad y control automatizado de inventarios/mercancías. | Control de cuentas de créditos fiscales y garantías en los supuestos aplicables. |
| Unidad operativa | Entradas, materiales, productos, salidas, pedimentos y saldos de inventario. | Cargos, inventario inicial, informes de descargo, correcciones y saldos de cuenta. |
| PEPS | Se usa en la mecánica de descargo prevista por el anexo. | Se usa para aplicar descargos sobre las cuentas/fracciones reportadas. |
| Aplicación | Depende del apartado A, B o C y de la regla que remite al anexo. | Depende del esquema fiscal, certificación/garantía y reglas que remiten al SCCCyG. |

Los dos controles deben poder reconciliarse con la operación aduanera real, pero **no son el mismo sistema ni responden a la misma obligación**.

## Cómo revisar una diferencia

1. Identificar la regla que originó la cuenta SCCCyG.
2. Verificar inventario inicial/cargo y fracción arancelaria.
3. Relacionar cada informe de descargo con pedimentos y operaciones efectivamente realizadas.
4. Comprobar correcciones posteriores.
5. Calcular el plazo legal fuera del simple dato presuntivo del sistema.
6. Comparar el resultado con Anexo 24 y contabilidad sólo en la medida necesaria para reconstruir el hecho.

## Fuentes

- [DOF/SIDOF — Anexos 21 a 30 de las RGCE 2026](https://sidof.segob.gob.mx/notas/5778300)
- [DOF/SIDOF — RGCE 2026](https://sidof.segob.gob.mx/notas/5777199)
- [SAT — Normatividad RGCE 2026](https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/normatividad_rmf_rgce2026.html)

## Vigencia

El Anexo 30 de las RGCE 2026 fue publicado el **15 de enero de 2026**. Al corte de revisión del **15 de agosto de 2026**, el portal oficial del SAT no muestra una modificación publicada del Anexo 30; la Primera Resolución de Modificaciones publicada en mayo modifica los Anexos 5, 22 y 29. Las versiones anticipadas se documentan por separado y no se tratan como si ya fueran una publicación del DOF.

## Ver también

[IMMEX](immex.md) · [Anexo 24: control de inventarios](anexo-24-control-inventarios.md) · [Pedimento y RGCE](../aduana/pedimento-rgce.md) · [Valor en aduana](../contribuciones/valor-en-aduana.md)
""",
)

# 6. Replace the two unsafe explanatory digests with source-bounded summaries.
write(
    "data/corpus/anexo-24-control-inventarios-immex.md",
    """# Anexo 24 RGCE 2026 — control automatizado de inventarios

> Digest explicativo. No sustituye la publicación oficial ni constituye texto normativo consolidado.

## Fuente primaria

- DOF/SIDOF: [Anexos 21 a 30 de las RGCE 2026](https://sidof.segob.gob.mx/notas/5778300), publicado el 15 de enero de 2026.

## Alcance

El Anexo 24 establece la información mínima que debe contener el sistema automatizado de control de inventarios en los supuestos a los que remiten las RGCE. La edición 2026 distingue tres apartados:

- **A:** información mínima del sistema automatizado vinculado a la regla 4.3.1;
- **B:** información del **SECIIT** para el supuesto específico señalado en la regla 7.1.4 y el propio anexo;
- **C:** información mínima para empresas con Registro en el Esquema de Certificación de Empresas.

## Componentes verificables

El apartado A contempla catálogos de datos generales, materiales y productos; información aduanera de entradas y salidas; materiales utilizados; activo fijo; y reportes de entradas, salidas, saldos y materiales utilizados.

El apartado B integra información electrónica proveniente del sistema corporativo. La edición 2026 establece ventanas de recepción de información que incluyen un plazo que no excede **24 horas** para la información señalada por el propio apartado, acceso en línea para la autoridad y restricciones de modificación sobre campos concretos obtenidos electrónicamente del sistema corporativo.

El apartado C prevé una ventana que no excede **48 horas** para la actualización definida por ese apartado y acceso en línea para la autoridad.

## Descargos

El Anexo 24 utiliza **Primeras Entradas Primeras Salidas (PEPS)** en su mecánica de descargos. La aplicación depende del apartado y del tipo de mercancía/operación descritos en la fuente oficial.

## Límites de este digest

Este resumen no afirma que:

- toda empresa IMMEX deba operar SECIIT;
- todo campo sea inmodificable;
- exista una periodicidad anual de conciliación creada por el Anexo 24;
- una diferencia produzca por sí misma PAMA, cancelación, multa o consecuencia penal;
- el anexo obligue a contratar una marca o arquitectura de software concreta.

Las consecuencias jurídicas de una diferencia deben fundarse en la disposición específica aplicable al hecho.
""",
)

write(
    "data/corpus/anexo-30-scccyg.md",
    """# Anexo 30 RGCE 2026 — Sistema de Control de Cuentas de Créditos y Garantías (SCCCyG)

> Digest explicativo. No sustituye la publicación oficial ni constituye texto normativo consolidado.

## Fuente primaria

- DOF/SIDOF: [Anexos 21 a 30 de las RGCE 2026](https://sidof.segob.gob.mx/notas/5778300), publicado el 15 de enero de 2026.

## Alcance

El Anexo 30 se refiere a la información del **Sistema de Control de Cuentas de Créditos y Garantías (SCCCyG)**. El sistema se conecta con los supuestos de créditos fiscales y garantías previstos por las RGCE; la sola existencia de un Programa IMMEX no determina por sí misma que cada operación esté dentro del SCCCyG.

## Mecánica resumida

La estructura oficial contempla información para integrar y afectar las cuentas del sistema, incluyendo inventario inicial, cargos, informes de descargo, correcciones y saldo en los términos del supuesto aplicable.

Los descargos utilizan **PEPS** para afectar las fracciones/cuentas de cargo conforme a la mecánica prevista por el anexo.

El SCCCyG puede mostrar plazos de retorno de forma **presuntiva**; el cómputo legal debe hacerse con las disposiciones vigentes aplicables a la operación.

Los saldos reflejados en el sistema **no implican resolución definitiva** y quedan a salvo las facultades de comprobación de la autoridad.

## Límites de este digest

Este resumen no convierte:

- una merma en cancelación automática de un saldo;
- un saldo positivo en prueba automática de mercancía no declarada;
- una discrepancia en un procedimiento sancionador automático;
- una estructura histórica de archivo o manual técnico en requisito vigente sin verificar su versión aplicable.

Para evaluar una diferencia deben reconstruirse el cargo, los informes de descargo, las correcciones, los pedimentos y la regla que originó la cuenta.
""",
)

# 7. Govern the public pages. The two annex guides are current-answer eligible only because
# the one-time preflight verifies the 2026 primary text and that SAT lists no published
# Annex 24/30 modification as of the review cutoff. The IMMEX hub remains source-partial.
old_immex_metadata = """  - <<: *wiki
    path: docs/wiki/programas/immex.md
    title: Programa IMMEX
    topic: programas
    source_ids: [mx_snice_immex]
    instrument_ids: [mx_programa_immex]
"""
new_immex_metadata = """  - <<: *wiki
    path: docs/wiki/programas/immex.md
    title: Programa IMMEX
    topic: programas
    source_ids: [mx_snice_immex, mx_sidof_immex_reform_20241219, mx_sidof_immex_reform_20250828, mx_sidof_immex_suspension_2026]
    instrument_ids: [mx_programa_immex, mx_rgce_2026]
    effective_from: 2006-11-13
    current_through: 2025-08-29
    source_status: partial
    legal_review_status: reviewed
  - <<: *wiki
    path: docs/wiki/programas/anexo-24-control-inventarios.md
    title: Anexo 24 - control de inventarios
    topic: programas
    source_ids: [mx_sidof_rgce_2026_anexos_21_30]
    instrument_ids: [mx_rgce_2026]
    effective_from: 2026-01-15
    current_through: 2026-01-15
    source_status: current
    legal_review_status: reviewed
  - <<: *wiki
    path: docs/wiki/programas/anexo-30-scccyg.md
    title: Anexo 30 - SCCCyG
    topic: programas
    source_ids: [mx_sidof_rgce_2026_anexos_21_30]
    instrument_ids: [mx_rgce_2026]
    effective_from: 2026-01-15
    current_through: 2026-01-15
    source_status: current
    legal_review_status: reviewed
"""
replace_once("sources/page_metadata.yaml", old_immex_metadata, new_immex_metadata)

# 8. Navigation.
old_nav = """- Programas y tratados:
  - Drawback: wiki/programas/drawback.md
  - IMMEX: wiki/programas/immex.md
  - PROSEC: wiki/programas/prosec.md
  - TLC y T-MEC: wiki/programas/tlc-tmec.md
  - Reglas de origen: wiki/programas/reglas-de-origen.md
"""
new_nav = """- Programas y tratados:
  - Drawback: wiki/programas/drawback.md
  - IMMEX: wiki/programas/immex.md
  - Anexo 24 - control de inventarios: wiki/programas/anexo-24-control-inventarios.md
  - Anexo 30 - SCCCyG: wiki/programas/anexo-30-scccyg.md
  - PROSEC: wiki/programas/prosec.md
  - TLC y T-MEC: wiki/programas/tlc-tmec.md
  - Reglas de origen: wiki/programas/reglas-de-origen.md
"""
replace_once("mkdocs.yml", old_nav, new_nav)

# 9. Roadmap: coverage is now public; legal status remains a separate concern.
replace_once(
    "docs/status/content-roadmap.md",
    "| Anexos 24 y 30 | corpus disponible, guía pendiente | corpus de anexos | RGCE |",
    "| Anexos 24 y 30 | cubierto con guías operativas | [Anexo 24](../wiki/programas/anexo-24-control-inventarios.md) / [Anexo 30](../wiki/programas/anexo-30-scccyg.md) | RGCE 2026 / SAT |",
)
replace_once(
    "docs/status/content-roadmap.md",
    """1. profundizar IMMEX, PROSEC, T-MEC y reglas de origen;
2. crear una guía integrada de Anexos 24 y 30;
3. construir una ruta de exportación equivalente a la ruta de importación;
4. explicar DTA y otros conceptos de contribuciones con ejemplos condicionados;
5. ampliar fuentes-país sólo cuando aporten valor real y no como páginas vacías.
""",
    """1. profundizar PROSEC, T-MEC y reglas de origen;
2. construir una ruta de exportación equivalente a la ruta de importación;
3. explicar DTA y otros conceptos de contribuciones con ejemplos condicionados;
4. ampliar fuentes-país sólo cuando aporten valor real y no como páginas vacías;
5. completar el historial versionado de reformas IMMEX anteriores a 2024 para consultas temporales más profundas.
""",
)

# 10. Retrieval cases: they all expect the 2026 Annex publication event; no fake event is
# created for the 2026 IMMEX suspension notice.
evals = read("evals/questions.yaml")
if "anexo24-seciit-scope" not in evals:
    write(
        "evals/questions.yaml",
        evals
        + """

  - id: anexo24-seciit-scope
    query: Anexo 24 2026 apartado B SECIIT 24 horas sistema corporativo
    cutoff: 2026-08-15
    expected_source_ids: [mx_sidof_rgce_2026_anexos_21_30]

  - id: anexo24-rece-48h
    query: Anexo 24 2026 apartado C RECE 48 horas control inventarios
    cutoff: 2026-08-15
    expected_source_ids: [mx_sidof_rgce_2026_anexos_21_30]

  - id: anexo30-scccyg-scope
    query: Anexo 30 SCCCyG creditos garantias PEPS plazos presuntivos saldo resolucion definitiva
    cutoff: 2026-08-15
    expected_source_ids: [mx_sidof_rgce_2026_anexos_21_30]
""",
    )

print("Wave 3 production edits applied")
