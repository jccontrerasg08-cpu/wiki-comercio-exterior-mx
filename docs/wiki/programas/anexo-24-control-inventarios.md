---
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
- Catálogo interno de fuentes: `docs/catalog/mexico/rgce.md`
- [SNICE — Programa IMMEX](https://www.snice.gob.mx/cs/avi/snice/immex.html)

## Vigencia

El Anexo 24 de las RGCE 2026 fue publicado el **15 de enero de 2026**. Al corte de revisión del **15 de agosto de 2026**, el portal oficial del SAT muestra publicada la Primera Resolución de Modificaciones a las RGCE 2026 y modificaciones de los Anexos 5, 22 y 29; no muestra una modificación publicada del Anexo 24. Las versiones anticipadas deben distinguirse de las publicaciones en DOF.

## Ver también

[IMMEX](immex.md) · [Anexo 30: SCCCyG](anexo-30-scccyg.md) · [Pedimento y RGCE](../aduana/pedimento-rgce.md) · [TIGIE y NICO](../clasificacion/tigie-nico.md)
