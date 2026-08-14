# Arquitectura

Wiki Comercio Exterior MX es un repositorio **público, Mexico-first**, de conocimiento verificable sobre comercio exterior. No es SAT ni el DOF. Las tablas de tarifa viven en [arancel-mx](https://github.com/jccontrerasg08-cpu/arancel-mx).

## Cuatro capas (no mezclar)

| Capa | Pregunta que responde | Dónde |
|---|---|---|
| Wiki | ¿Qué es, cómo funciona, qué documento, qué sistema? | `docs/wiki/` → MkDocs |
| Catálogo | ¿Cuál es la URL oficial? | `docs/catalog/` + `sources/registry.yaml` |
| Originales | ¿Qué bytes, qué SHA, qué Release? | `data/originals/` + GitHub Release |
| Corpus | ¿Qué dice el digest RAG? (no es el DOF) | `data/corpus/` |

HS6 es el techo internacional. TIGIE 8 y NICO 10 son México. No duplicar una base arancelaria mundial en este git.

## Jerarquía de autoridad

1. DOF / SIDOF  
2. Texto consolidado Diputados  
3. SAT / ANAM / SE / SNICE / VUCEM  
4. OMA / OMC / UNCTAD  
5. Esta wiki  
6. Corpus derivado (paráfrasis)

## Roadmap (PRs)

1. P0 jurídico: Ley Aduanera vigente, NOMs bajo LIC (no LFMN), Anexo 13  
2. `source_id` canónico  
3. Front matter en corpus  
4. Sacar del corpus lo que es guía/RAG policy  
5. Validators  
6. MkDocs: México / global / tratados / procedimientos (el catálogo entra al sitio)  
7. Separar tratados de programas; páginas por TLC con el material ya capturado  

No borrar anexos RGCE 1–30. No meter PDF en el clone.
