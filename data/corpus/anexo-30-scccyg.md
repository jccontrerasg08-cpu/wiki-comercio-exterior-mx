# Anexo 30 — Sistema de Control de Cuentas de Créditos y Garantías (SCCCyG) (RGCE 2026)

**URL oficial:** https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/documentos2026/rgce/anexos/Anexo30delasRGCEpara2026.pdf
**Publicado:** 15-01-2026 | **DOF:** 15-01-2026
**Portal de actualizaciones:** https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/normatividad_rmf_rgce2026.html
**Fundamento:** Arts. 28-A Ley del IVA; arts. 15-A Ley del IEPS; reglas del Título 7 (RECE) de las RGCE 2026

## Cómo actualizar
1. Descargar el PDF desde la URL oficial.
2. El Anexo 30 define el sistema de contabilidad; los cambios relevantes son en el Título 7 de las RGCE (reglas RECE/OEA), no necesariamente en el Anexo 30 mismo.
3. Verificar si se modificaron los formatos de transmisión de datos al SAT o las tasas de garantía.

## ¿Qué es el SCCCyG?
El Sistema de Control de Cuentas de Créditos y Garantías es el **mecanismo contable digital** mediante el cual el SAT registra y controla:

1. **Los saldos de IVA e IEPS diferidos** por las empresas con Registro en el Esquema de Certificación (RECE) modalidad IVA-IEPS al importar temporalmente (Título 7 RGCE 2026).
2. **Las garantías** constituidas para respaldar los créditos fiscales contingentes derivados del diferimiento del IVA e IEPS.

## ¿Cómo funciona?

```
EMPRESA INMEX CON CERTIFICACIÓN IVA-IEPS:

IMPORTA TEMPORALMENTE (sin pagar IVA/IEPS)
    ↓
El SAT registra en el SCCCyG:
  + Crédito = IVA+IEPS que "debía" haberse pagado
  + Garantía vinculada (carta de crédito bancaria o monto suficiente)
    ↓
DURANTE LA PERMANENCIA DE LA MERCANCÍA EN MEXICO:
  - La empresa puede transferir a otra IMMEX → se traspasa el saldo en SCCCyG
  - La mercancía se consume/merma → se cancela la parte correspondiente del saldo
    ↓
AL RETORNAR o CAMBIAR A IMPORTACIÓN DEFINITIVA:
  → Se descarga el saldo del SCCCyG
  → Si es importación definitiva: se paga el IVA/IEPS real
  → El saldo en SCCCyG = $0 para esa mercancía
```

## Estructura del Anexo 30
Define los requisitos técnicos de la plataforma del SCCCyG:
- **Catálogos de cuentas** (importador, proveedor extranjero, fracción arancelaria, pedimento)
- **Movimientos de cargo** (importaciones temporales que generan crédito diferido)
- **Movimientos de abono** (retornos, destrucciones, mermas, cambios de régimen)
- **Formato de transmisión de información** al SAT (XML, periodicidad, plazos)
- **Consulta de saldos** por la empresa y por la autoridad

## Relación con el SECIIT (Anexo 24) y el SCCCyG (Anexo 30)
Son sistemas complementarios pero distintos:

| Sistema | Qué controla | Quién lo lleva |
|---|---|---|
| **SACI / SECIIT (Anexo 24)** | Inventario físico de mercancías importadas temporalmente (unidades, lotes, pedimentos) | La empresa IMMEX |
| **SCCCyG (Anexo 30)** | Saldo contable de IVA/IEPS diferido y garantías | El SAT (la empresa lo alimenta con sus reportes) |

Ambos deben estar **reconciliados** en todo momento. Una discrepancia entre el SECIIT y el SCCCyG es señal de alerta para el SAT y puede derivar en una revisión de gabinete o visita domiciliaria.

## Implicación práctica para el chatbot
Cuando una empresa certificada IVA-IEPS pregunta sobre su saldo diferido:
- El saldo lo gestiona el SAT en el SCCCyG — la empresa puede consultarlo en el Portal del SAT.
- Si la empresa tiene un saldo positivo inesperado (más IVA diferido del que debería), es señal de que tiene mercancías temporales no retornadas o no declaradas → riesgo de PAMA.
- La garantía asociada al SCCCyG debe mantenerse vigente en todo momento; su vencimiento sin renovación puede derivar en la cancelación del RECE.
