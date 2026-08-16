---
title: "Contratos entre repositorios"
description: "Responsabilidades canónicas, identificadores compartidos y reglas de consumo entre la wiki, arancel-mx y aduanamap-mx."
---

# Contratos entre repositorios

El proyecto separa responsabilidades para evitar tres copias divergentes de la misma información. Cada dominio tiene una fuente canónica y los demás repositorios la consumen mediante identificadores y contratos explícitos.

## Responsabilidades canónicas

| Dominio | Repositorio canónico | Identificador principal |
|---|---|---|
| Fuentes jurídicas, instrumentos, eventos, originales y provenance | `wiki-comercio-exterior-mx` | `source_id`, `instrument_id` |
| HS, TIGIE, fracción mexicana, NICO, tasas y artefactos arancelarios | `arancel-mx` | código HS / fracción / NICO |
| Países, geometrías, aduanas, puertos, cruces, rutas y capas cartográficas | `aduanamap-mx` | ISO2/ISO3 y IDs geoespaciales propios |

## Países

Para relaciones entre tratados, estadísticas y mapa se prefieren **ISO 3166-1 alpha-2 (`iso2`)** e **ISO 3166-1 alpha-3 (`iso3`)**. AduanaMap normaliza ambos campos en su geometría mundial. Los nombres en español/inglés son atributos de presentación y no sustituyen el identificador estable.

## Clasificación arancelaria

`arancel-mx` es la fuente estructurada para la jerarquía **HS → capítulo → partida → subpartida → fracción MX → NICO**. La wiki puede enlazar una fracción o explicar su contexto jurídico, pero no mantiene una tabla paralela de tasas.

## Fuentes e instrumentos legales

`source_id` e `instrument_id` se definen en esta wiki. Una aplicación externa puede guardar esos IDs para regresar al documento o evento jurídico correspondiente. La copia de los textos o la inferencia independiente de vigencia no forman parte del contrato.

## Geodatos

El contrato actual está en `data/contracts/aduanamap.yaml`. La geometría mundial `world_countries_50m` pertenece a AduanaMap y se observó en un commit inmutable. Mientras no exista un artefacto público inmutable o verificable por checksum, la wiki usa únicamente enlaces y navegación textual; no copia el GeoJSON de forma manual.

## Versionado y compatibilidad

Un consumidor reproducible debe preferir, en este orden:

1. artefacto de release inmutable con checksum;
2. URL fijada a tag o commit;
3. copia derivada durante build con provenance/hash, si el contrato lo permite;
4. enlace textual de fallback cuando no exista un artefacto consumible.

Nunca se debe sustituir silenciosamente una referencia inmutable por `main`. Si cambia el esquema esperado, el contrato debe actualizarse y la validación debe fallar hasta que el consumidor sea compatible.

## Degradación

Los contratos entre repositorios mejoran navegación e interoperabilidad, pero no son dependencias de vigencia jurídica. Si AduanaMap, `arancel-mx` o un artefacto externo no están disponibles, las páginas jurídicas y la biblioteca documental de la wiki deben seguir funcionando.
