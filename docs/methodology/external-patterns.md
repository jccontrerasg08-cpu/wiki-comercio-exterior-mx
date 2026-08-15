---
title: "Patrones externos revisados"
description: "Patrones de proyectos externos adaptados a la wiki para provenance, documentación, validación y mantenimiento reproducible."
---

# Patrones externos revisados

No se copió una implementación completa. Se adaptaron ideas pequeñas, con tests locales y contratos propios.

| Proyecto | Licencia upstream | Patrón adoptado | Patrón descartado |
|---|---|---|---|
| [OASIS LegalDocML Akoma Ntoso](https://github.com/oasis-open/legaldocml-akomantoso) | CC BY 2.0 para el repositorio abierto | Separar instrumento, evento, versión temporal y manifestación | XML legislativo completo, innecesario para este repositorio |
| [python-jsonschema](https://github.com/python-jsonschema/jsonschema) | MIT | Draft 2020-12, `check_schema`, errores iterables y `FormatChecker` explícito | Resolver referencias remotas durante CI |
| [MkDocs Material](https://github.com/squidfunk/mkdocs-material) | MIT | Sitio estático reproducible y búsqueda local | Plugins no fijados o generación con red |
| [mkdocs-redirects](https://github.com/ProperDocs/mkdocs-redirects) | MIT | Compatibilidad explícita de rutas públicas movidas | Redirecciones implícitas o dependientes del servidor |
| [lychee-action](https://github.com/lycheeverse/lychee-action) | MIT o Apache-2.0 | Revisión de enlaces programada y cacheada | Bloquear PR por disponibilidad externa transitoria |
| [GitHub CodeQL Action](https://github.com/github/codeql-action) | MIT | Análisis de Python con permisos mínimos | Escritura desde eventos de pull request |
| [OpenSSF Scorecard](https://github.com/ossf/scorecard) | Apache-2.0 | Dependencias fijadas, permisos explícitos y política de seguridad | Publicar una puntuación sin contexto como garantía absoluta |

La evaluación de recuperación adopta métricas comunes de recuperación de información: recall@k, reciprocal rank, exactitud temporal y cobertura de cita. Se usa una línea base léxica local para que CI no dependa de modelos, claves o servicios externos.
