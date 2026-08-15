# Compatibilidad del motor de documentación

Estado evaluado: **15 de agosto de 2026**.

Esta página define el contrato para cambiar el motor que publica la wiki. El objetivo no es migrar por novedad, sino evitar que una actualización de MkDocs, Material o un reemplazo futuro rompa navegación, búsqueda, redirects o reproducibilidad.

## Producción actual

La publicación de GitHub Pages permanece en:

- `mkdocs==1.6.1`
- `mkdocs-material==9.7.7`
- `mkdocs-redirects==1.2.3`

El build de producción debe seguir pasando `mkdocs build --strict` y `python -m scripts.verify_site` antes de subir el artefacto de Pages.

Material for MkDocs 9.7 está en modo de mantenimiento. Su documentación también advierte que MkDocs 2.0 no es compatible con Material for MkDocs, por lo que no se debe permitir una actualización mayor automática de MkDocs mientras esta sea la plataforma de producción.

Fuentes de referencia:

- [Material for MkDocs, changelog](https://squidfunk.github.io/mkdocs-material/changelog/)
- [Material for MkDocs y MkDocs 2.0](https://squidfunk.github.io/mkdocs-material/blog/2026/mkdocs-2/)

## Candidato evaluado: Zensical 0.0.54

Zensical es el sucesor desarrollado por el equipo de Material for MkDocs. La versión **Zensical 0.0.54** fue publicada el 13 de agosto de 2026.

La compatibilidad existente es relevante para esta wiki porque Zensical puede interpretar configuración de proyectos MkDocs/Material y mantiene compatibilidad con Python Markdown y muchas características del tema. Eso permite evaluarlo sin reescribir el corpus.

Sin embargo, **no es el motor de producción de este repositorio**.

Fuentes de referencia:

- [Zensical](https://zensical.org/)
- [Compatibilidad con proyectos existentes](https://zensical.org/compatibility/)
- [Compatibilidad de plugins](https://zensical.org/compatibility/plugins/)
- [Release 0.0.54](https://github.com/zensical/zensical/releases/tag/0.0.54)

## Bloqueador actual: redirects legacy

Esta wiki conserva rutas públicas antiguas con `mkdocs-redirects`. No son un detalle cosmético: enlaces existentes, referencias externas y bookmarks deben continuar resolviendo después de una migración.

Al 15 de agosto de 2026, la compatibilidad con `mkdocs-redirects` sigue registrada por Zensical como trabajo pendiente de prioridad Tier 1 en [`zensical/backlog#23`](https://github.com/zensical/backlog/issues/23).

Por eso, **un build exitoso de Zensical por sí solo no es suficiente para autorizar la migración**. La nueva plataforma debe demostrar paridad de rutas legacy.

## Gates obligatorios antes de cambiar producción

Una migración del motor sólo puede entrar a `main` cuando el candidato demuestre, en CI y sobre el mismo corpus:

1. build estricto sin errores ni warnings que oculten contenido inválido;
2. todas las páginas y anchors internos válidos;
3. las rutas legacy actuales siguen resolviendo al destino esperado;
4. búsqueda local funcional y sin dependencia obligatoria de servicios externos;
5. soporte del CSS y HTML usados por la portada y navegación;
6. ningún cambio en la semántica de provenance, vigencia temporal o RAG;
7. artefacto de Pages reproducible y verificable antes del deploy;
8. rollback sencillo al motor anterior durante la transición.

Hasta que todos esos gates sean verdes, Zensical debe tratarse como **candidato experimental** y no como reemplazo de producción.

## Dependencias que no forman parte del runtime

El paquete independiente `properdocs` no participa en los comandos, workflows ni scripts de publicación de esta wiki. `mkdocs-redirects` es un proyecto separado y se instala directamente. Por eso `properdocs` no debe mantenerse en `requirements-docs.txt` sólo por compartir organización de mantenimiento con el plugin de redirects.

## Política de actualización

- Mantener versiones del motor y plugins fijadas explícitamente en CI.
- Revisar nuevas versiones de Material sólo por correcciones relevantes mientras permanezca en maintenance mode.
- No subir a MkDocs 2.x mientras Material siga siendo el tema de producción.
- Reevaluar Zensical cuando cambie el estado de `zensical/backlog#23` o aparezca soporte equivalente de redirects.
- Hacer la migración real en un PR separado, con comparación de artefactos y rutas, nunca mezclada con cambios jurídicos del corpus.
