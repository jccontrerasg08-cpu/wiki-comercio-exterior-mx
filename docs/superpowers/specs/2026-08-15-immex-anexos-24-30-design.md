# IMMEX + Anexos 24 y 30 Design

**Fecha:** 2026-08-15

## Objetivo

Convertir el bloque IMMEX de la wiki en una guía jurídico-operativa auditable que conecte el Decreto IMMEX, la Ley Aduanera, las RGCE 2026, el Anexo 24 y el Anexo 30 sin mezclar obligaciones distintas ni presentar inferencias operativas como si fueran norma.

## Principios de fuente y vigencia

1. El DOF/SIDOF es la autoridad primaria para decretos, RGCE y anexos; SAT y SNICE se usan como índices oficiales, guías y material de apoyo.
2. Las compilaciones o páginas de conveniencia no sustituyen el acto publicado en DOF para afirmar vigencia jurídica.
3. Ninguna edición editorial promueve por sí sola una página a `reviewed/current`.
4. Una promoción exige fuente primaria identificada, fecha de revisión y `current_through` correspondiente al último evento efectivo realmente revisado.
5. Las versiones anticipadas de RGCE se documentan como anticipadas y no se confunden con la resolución publicada en DOF.
6. La wiki no reproduce listados arancelarios extensos del Decreto IMMEX. Para clasificación y fracciones se remite a la fuente oficial y a `arancel-mx` cuando corresponda.

## Hallazgos oficiales que condicionan el diseño

- La página oficial de SNICE identifica al Decreto IMMEX de 1 de noviembre de 2006 y sus reformas como fundamento del programa. La biblioteca jurídica de SNICE lista como reformas más recientes las del 19 de diciembre de 2024 y 28 de agosto de 2025.
- El decreto de 28 de agosto de 2025 entró en vigor al día siguiente de su publicación y modificó el Anexo I del Decreto IMMEX, entre otros elementos.
- El aviso de 2026 sobre programas suspendidos confirma que el reporte anual del artículo 25 corresponde al ejercicio inmediato anterior y debe presentarse a más tardar el último día hábil de mayo; para las suspensiones relativas al ejercicio 2025, el plazo de regularización llega al último día hábil de agosto de 2026 y la cancelación opera desde el 1 de septiembre de 2026 si no se subsana.
- SAT lista el Anexo 24 y el Anexo 30 de RGCE 2026 como publicados el 15 de enero de 2026. La Primera Resolución de Modificaciones de 2026 modifica los anexos 5, 22 y 29, no los anexos 24 ni 30.
- El Anexo 24 de 2026 contiene tres apartados distintos: A, control mínimo ligado a la regla 4.3.1; B, SECIIT para el supuesto específico de la regla 7.1.4; C, control mínimo para empresas con Registro en el Esquema de Certificación de Empresas. Por tanto, `Anexo 24 = SECIIT` es una simplificación incorrecta.
- En el apartado B del Anexo 24, ciertos datos deben recibirse electrónicamente en no más de 24 horas y el SECIIT debe permitir acceso en línea a la autoridad. En el apartado C, el sistema debe actualizarse en no más de 48 horas después de concluir actos y formalidades del despacho y también debe permitir acceso en línea a la autoridad.
- El Anexo 24 exige descargos PEPS en los supuestos descritos por el propio anexo, incluidos materiales y desperdicios dentro de la mecánica correspondiente.
- El Anexo 30/SCCCyG es un sistema de cargos, descargos, créditos y garantías para los regímenes y esquemas a los que las RGCE lo vinculan. No es una obligación universal para toda empresa IMMEX.

## Arquitectura editorial

### 1. Página hub IMMEX

`docs/wiki/programas/immex.md` se convierte en la entrada principal y responde, en este orden:

1. qué es el Programa IMMEX y cuál es su fundamento;
2. cuándo una importación temporal entra al flujo IMMEX;
3. qué obliga a controlar el artículo 24, fracción IX del Decreto IMMEX y la regla 4.3.1;
4. cómo se conectan plazos de permanencia, pedimentos, retornos, transferencias, cambios de régimen y desperdicios;
5. cuándo interviene el Anexo 24;
6. cuándo puede intervenir el Anexo 30/SCCCyG y cuándo no;
7. reporte anual y riesgo de suspensión/cancelación;
8. reformas recientes relevantes sin copiar listas arancelarias.

La página debe distinguir siempre entre regla general, supuesto específico y práctica de verificación.

### 2. Guía pública Anexo 24

Crear `docs/wiki/programas/anexo-24-control-inventarios.md` con:

- alcance y fundamento;
- diferencia entre apartados A, B y C;
- catálogos/módulos/reportes mínimos por nivel;
- mecánica de descargos PEPS;
- relación con pedimentos, inventario corporativo, retornos, transferencias, cambios de régimen, mermas y desperdicios;
- plazos de 24 h y 48 h sólo en los apartados donde la norma los establece;
- sección explícita de `Lo que el Anexo 24 no dice` para evitar convertir recomendaciones de software, auditoría o vigilancia en obligaciones legales;
- fuentes, vigencia y verificación.

No se usará `SACI` como nombre normativo del apartado A si la fuente oficial sólo dice `sistema automatizado de control de inventarios`.

### 3. Guía pública Anexo 30

Crear `docs/wiki/programas/anexo-30-scccyg.md` con:

- qué controla el SCCCyG;
- sujetos/esquemas a los que se conecta;
- inventario inicial, cargos, informes de descargo, correcciones y saldo;
- diferencia con Anexo 24;
- advertencia de que el plazo mostrado por SCCCyG no sustituye el cómputo legal aplicable;
- advertencia de que el saldo del sistema no constituye resolución definitiva;
- ninguna afirmación automática de `saldo positivo = incumplimiento` ni de `discrepancia = PAMA` sin fundamento específico.

### 4. Corrección del corpus explicativo

Reescribir:

- `data/corpus/anexo-24-control-inventarios-immex.md`
- `data/corpus/anexo-30-scccyg.md`

Los digests deben conservar sólo afirmaciones rastreables a la fuente primaria, separar texto normativo de explicación y eliminar lenguaje de chatbot, recomendaciones de software, multas aproximadas, consecuencias penales automáticas y otras inferencias no demostradas por el anexo.

## Grafo de fuentes e instrumentos

Agregar al registro, si no existen:

- reforma IMMEX de 19-12-2024, SIDOF 5745788;
- reforma IMMEX de 28-08-2025, SIDOF 5766797;
- aviso IMMEX suspendidas 2026, SIDOF 5792091, como evidencia operativa del artículo 25 y no como reforma del instrumento.

Actualizar `mx_programa_immex` con los eventos de reforma de 2024 y 2025. El aviso de 2026 no se añade como `amends`.

Las páginas nuevas deben vincular, según corresponda, Decreto IMMEX, Ley Aduanera, RGCE 2026, LIVA/LIEPS y fuentes oficiales del Anexo 24/30.

## Metadata y currentness

- `docs/wiki/programas/immex.md`: sólo podrá pasar a `reviewed` cuando sus afirmaciones se hayan cotejado con Decreto IMMEX, reformas, Ley Aduanera/RGCE y aviso anual vigente.
- `docs/wiki/programas/anexo-24-control-inventarios.md`: puede marcarse `reviewed/current` si se coteja el Anexo 24 publicado y se verifica que las modificaciones publicadas de RGCE posteriores no lo hayan reformado.
- `docs/wiki/programas/anexo-30-scccyg.md`: mismo criterio, con especial cuidado de no importar sin verificación reglas históricas que hayan cambiado.
- Los corpus pueden seguir como `partial` si su extracción no representa el texto oficial completo, aunque el digest sea corregido.

## Navegación y roadmap

En `mkdocs.yml`, agrupar las nuevas guías junto a IMMEX sin romper rutas públicas existentes. En `docs/status/content-roadmap.md`, pasar `Anexos 24 y 30` de `guía pendiente` a un estado que refleje la guía implementada, sin confundir cobertura con revisión jurídica.

## Retrieval y evaluación

Agregar evals deterministas para comprobar que el retrieval actual pueda responder, con cita elegible:

1. qué controla el Anexo 24;
2. cuándo aplica PEPS;
3. por qué Anexo 24 no es sinónimo de SECIIT;
4. diferencia entre Anexo 24 y SCCCyG;
5. por qué SCCCyG no aplica automáticamente a todo IMMEX;
6. obligación anual del artículo 25 y estado 2026 de suspensión/regularización.

Las respuestas `current` no pueden depender de páginas `pending_review`, fuentes stale ni corpus partial no elegible.

## Tests y gates

TDD antes de producción:

- tests de presencia/estructura de las dos nuevas páginas;
- tests de frases de riesgo eliminadas de corpus y wiki;
- tests de source/instrument IDs y eventos IMMEX;
- tests de navegación;
- evals RAG temporales.

Gate final obligatorio:

1. suite completa;
2. repository validator;
3. catálogo generado;
4. page metadata;
5. coverage policy/dashboard;
6. temporal graph;
7. RAG eval;
8. MkDocs strict;
9. verificador de sitio/rutas;
10. Dependency Review;
11. CI de PR verde sobre head exacto;
12. squash merge con `expected_head_sha`;
13. CI de `main` y Pages verdes sobre merge SHA.

## Fuera de alcance de esta ola

- reproducir todas las fracciones sensibles/restringidas del Decreto IMMEX;
- construir software Anexo 24/ERP;
- automatizar descargos reales ante SAT;
- asesoría individual sobre saldos o regularización;
- promover automáticamente estados jurídicos;
- PROSEC y T-MEC en profundidad, salvo enlaces necesarios para explicar interacciones.
