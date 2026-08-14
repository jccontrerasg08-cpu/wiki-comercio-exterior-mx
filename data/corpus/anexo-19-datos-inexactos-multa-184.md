# Anexo 19 — Datos Inexactos, Falsos u Omitidos que Actualizan la Infracción del Artículo 184, Fracción III de la Ley Aduanera (RGCE 2026)

**URL oficial:** https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/documentos2026/rgce/anexos/Anexo19delasRGCEpara2026.pdf
**Publicado:** 14-01-2026 | **DOF:** 14-01-2026
**Portal de actualizaciones:** https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/normatividad_rmf_rgce2026.html
**Fundamento:** Art. 184, fracción III y art. 185, fracción II de la Ley Aduanera; regla 3.7.25. segundo párrafo de las RGCE 2026

## Cómo actualizar
1. Descargar el PDF desde la URL oficial.
2. Verificar si se agregaron nuevos datos — es relativamente estable, pero puede cambiar con reformas a la LA.

## Contenido
Lista de **campos específicos del pedimento** que, si son declarados con datos inexactos, falsos u omitidos, activan automáticamente la infracción del art. 184, fracción III y la multa del art. 185, fracción II (porcentaje del valor de las mercancías).

### Datos del pedimento que típicamente activan la multa
Los siguientes datos están en el Anexo 19 (verificar PDF oficial para el texto exacto):
- Valor en aduana de la mercancía
- Descripción de la mercancía
- Fracción arancelaria declarada
- Número de identificación comercial (NICO)
- País de origen
- País de procedencia
- Nombre o razón social del importador/exportador
- RFC del importador/exportador
- Nombre o razón social del proveedor extranjero
- Domicilio del proveedor extranjero
- Número de factura
- Número de bultos / peso bruto
- Número de candado oficial

### Lógica de uso crítica para el chatbot
```
¿El usuario quiere rectificar un dato en el pedimento?
    ↓
¿Está en el Anexo 19?
    SÍ → La rectificación conlleva la multa del art. 185-II
         (no hay corrección espontánea sin sanción para estos datos)
         Excepción: si la rectificación ocurre ANTES de activar
         el mecanismo de selección automatizado (art. 89 LA)
         → en ese caso SÍ es libre de multa.
    NO → Puede rectificarse espontáneamente sin sanción
         (art. 89 LA, rectificación antes o después del despacho
         sin que sea detectada por facultades de comprobación)
```

### Consecuencia práctica (criterio 4/LA/PI — ver `anexo-05-criterios-practicas-indebidas.md`)
El criterio 4/LA/PI sobre calzado hace explícita referencia al Anexo 19: declarar en el pedimento un valor diferente al del CFDI/documento equivalente activa la multa de este Anexo 19 + el posible delito de defraudación fiscal (art. 108 CFF).
