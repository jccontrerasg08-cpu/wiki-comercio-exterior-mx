---
title: "Explorar aduanas y mapa"
description: "Entrada geográfica al comercio exterior con datos canónicos de AduanaMap y navegación jurídica de respaldo."
---

# Aduanas y mapa

La wiki ofrece una entrada cartográfica contextual, mientras [`aduanamap-mx`](https://github.com/jccontrerasg08-cpu/aduanamap-mx) conserva la aplicación geoespacial avanzada y los datasets canónicos.

## Capa mundial existente

La geometría mundial canónica se encuentra en `aduanamap-mx/data/geojson/countries-50m.geojson`. Es un **GeoJSON** derivado de Natural Earth 1:50m, normalizado para el producto y generado de forma determinista. La wiki no mantiene una segunda copia manual de ese archivo.

## Capas y relaciones

Conforme existan datasets verificados, el mapa puede relacionar países, tratados, aduanas y secciones, puertos, aeropuertos, cruces fronterizos, recintos, RFE y rutas con sus páginas jurídicas u operativas. La presencia de una capa no implica por sí sola autorización, competencia o aplicabilidad normativa.

- [ANAM y aduanas](../wiki/aduana/anam.md)
- [Regímenes aduaneros](../wiki/aduana/regimenes-aduaneros.md)
- [Proceso de despacho](../wiki/aduana/proceso-despacho.md)
- [Tratados y origen](tratados-origen.md)
- [Fuentes oficiales](../catalog/index.md)

## Degradación segura

La información jurídica y documental debe seguir disponible **sin mapa**. Si el GeoJSON, MapLibre o AduanaMap no están disponibles, esta página conserva enlaces textuales hacia aduanas, instrumentos, tratados y fuentes. El mapa es una capa de exploración, no una dependencia de verdad jurídica.

!!! info "Fuente canónica"
    Los geodatos se consumen mediante un contrato versionado y verificable. No se corrigen manualmente en la wiki; cualquier cambio de geometría debe originarse en AduanaMap y conservar su provenance.
