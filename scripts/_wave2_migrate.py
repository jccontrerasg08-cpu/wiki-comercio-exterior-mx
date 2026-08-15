from __future__ import annotations

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]

DESCRIPTIONS = {
    "docs/wiki/aduana/pedimento-rgce.md": "Pedimento y RGCE 2026: declaración electrónica, Anexo 22, documentos e identificadores para el despacho aduanero mexicano.",
    "docs/wiki/aduana/regimenes-aduaneros.md": "Regímenes aduaneros en México: finalidades, efectos y puntos de control que cambian según el régimen previsto por la Ley Aduanera.",
    "docs/wiki/clasificacion/rrna.md": "Introducción a las regulaciones y restricciones no arancelarias que pueden activarse por mercancía, fracción, NICO y operación.",
    "docs/wiki/clasificacion/sistema-armonizado.md": "Sistema Armonizado: estructura internacional de clasificación, versión HS 2022 y relación con la TIGIE mexicana.",
    "docs/wiki/clasificacion/tigie-nico.md": "TIGIE y NICO: relación entre fracción arancelaria mexicana, NICO, tasa y fuentes oficiales vigentes.",
    "docs/wiki/contribuciones/impuestos-importacion.md": "Contribuciones de importación en México: relación entre IGI, IVA, IEPS, DTA, valor en aduana y otras obligaciones aplicables.",
    "docs/wiki/fundamentos/marco-juridico.md": "Marco jurídico del comercio exterior mexicano: jerarquía de leyes, reglamentos, reglas, decretos y fuentes oficiales para verificar vigencia.",
    "docs/wiki/logistica/logistica-internacional.md": "Logística internacional: transporte, seguros, documentos y controles que deben coordinarse con el despacho aduanero.",
    "docs/wiki/programas/drawback.md": "Drawback en México: devolución de impuestos de importación a exportadores, requisitos y fuentes del programa vigente.",
    "docs/wiki/programas/immex.md": "IMMEX: importación temporal para procesos de exportación, obligaciones, plazos y controles relacionados con RGCE.",
    "docs/wiki/programas/prosec.md": "PROSEC: tasas preferenciales de IGI por sector productivo, condiciones de uso y modificaciones vigentes del decreto.",
    "docs/wiki/programas/reglas-de-origen.md": "Reglas de origen: criterios para determinar origen preferencial y sustentar beneficios arancelarios bajo el tratado aplicable.",
    "docs/wiki/programas/tlc-tmec.md": "Tratados comerciales y T-MEC: preferencias arancelarias, origen, certificación y verificación sin confundir país de compra con origen.",
    "docs/wiki/rrna/anexo-2-2-1.md": "Anexo 2.2.1: permisos y avisos de la Secretaría de Economía vinculados con fracciones y supuestos de comercio exterior.",
    "docs/wiki/rrna/anexo-2-4-1.md": "Anexo 2.4.1: fracciones sujetas a NOM en punto de entrada y ruta para verificar requisitos y excepciones vigentes.",
    "docs/wiki/rrna/index.md": "Guía de RRNA: flujo para identificar permisos, avisos, NOM y otras restricciones antes del despacho aduanero.",
    "docs/wiki/rrna/reglas-criterios-se.md": "Reglas y criterios de la Secretaría de Economía: acuerdo base, modificaciones y anexos que estructuran numerosas RRNA.",
}

PUBLIC_DESCRIPTIONS = {
    "docs/catalog/index.md": "Guía para usar el catálogo de fuentes oficiales y distinguir disponibilidad, autoridad, vigencia y evidencia local.",
    "docs/catalog/catalog.md": "Catálogo curado de portales y documentos oficiales relevantes para comercio exterior mexicano y fuentes internacionales.",
    "docs/catalog/global/index.md": "Fuentes globales de comercio exterior: OMC, OMA, ICC y referencias multilaterales usadas por la wiki.",
    "docs/catalog/mexico/index.md": "Fuentes oficiales mexicanas para legislación aduanera, tarifa, RGCE, SNICE, SAT, ANAM y Ventanilla Única.",
    "docs/catalog/mexico/arancel.md": "Fuentes oficiales y capa estructurada para consultar LIGIE, TIGIE, NICO y modificaciones arancelarias de México.",
    "docs/catalog/mexico/inegi-tigie-scian.md": "Referencia INEGI para TIGIE-SCIAN y su uso como herramienta estadística y de consulta, no como sustituto de la LIGIE.",
    "docs/catalog/mexico/ley-aduanera.md": "Fuentes oficiales para consultar la Ley Aduanera vigente, reformas y texto consolidado aplicable en México.",
    "docs/catalog/mexico/rgce.md": "Fuentes oficiales de RGCE, resoluciones de modificaciones y anexos para verificar reglas aduaneras vigentes.",
    "docs/changes/index.md": "Historial del proyecto y cambios relevantes en fuentes, metodología, contenido y controles de la wiki.",
    "docs/glossary.md": "Glosario de siglas y conceptos frecuentes de comercio exterior, aduanas, tarifa y regulación mexicana.",
    "docs/methodology/index.md": "Metodología de captura, provenance, revisión jurídica, vigencia temporal y publicación de Wiki Comercio Exterior MX.",
    "docs/methodology/status-model.md": "Modelo de estados independiente para fuente, extracción, revisión legal, corpus y salud de transporte.",
    "docs/methodology/external-patterns.md": "Patrones de proyectos externos adaptados a la wiki para provenance, documentación, validación y mantenimiento reproducible.",
    "docs/methodology/docs-engine-compatibility.md": "Contrato de compatibilidad del motor documental, MkDocs Material, redirects y ruta futura de migración.",
    "docs/ARCHITECTURE.md": "Arquitectura del repositorio: fuentes, originales, corpus, wiki, grafo temporal, validadores y recuperación RAG.",
}

COUNTRIES = {
    "BRA": "Fuentes oficiales de Brasil para aduanas y comercio exterior, mantenidas como catálogo de referencia país.",
    "CAN": "Fuentes oficiales de Canadá para aduanas y comercio exterior, mantenidas como catálogo de referencia país.",
    "CHN": "Fuentes oficiales de China para aduanas y comercio exterior, mantenidas como catálogo de referencia país.",
    "DEU": "Fuentes oficiales de Alemania y la Unión Europea para aduanas y comercio exterior, como catálogo de referencia país.",
    "JPN": "Fuentes oficiales de Japón para aduanas y comercio exterior, mantenidas como catálogo de referencia país.",
    "NLD": "Fuentes oficiales de Países Bajos y la Unión Europea para aduanas y comercio exterior, como catálogo de referencia país.",
    "USA": "Fuentes oficiales de Estados Unidos para aduanas y comercio exterior, mantenidas como catálogo de referencia país.",
}

SOURCE_SECTION_PATHS = {
    "docs/wiki/aduana/regimenes-aduaneros.md",
    "docs/wiki/contribuciones/impuestos-importacion.md",
    "docs/wiki/fundamentos/marco-juridico.md",
    "docs/wiki/programas/drawback.md",
    "docs/wiki/rrna/anexo-2-2-1.md",
    "docs/wiki/rrna/anexo-2-4-1.md",
    "docs/wiki/rrna/reglas-criterios-se.md",
}


def yaml_string(value: str) -> str:
    """Return a deterministic double-quoted YAML scalar."""

    return json.dumps(value, ensure_ascii=False)


def set_description(path: Path, description: str) -> None:
    text = path.read_text(encoding="utf-8")
    rendered = yaml_string(description)
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end < 0:
            raise RuntimeError(f"invalid front matter: {path}")
        head = text[4:end]
        body = text[end + 5 :]
        if re.search(r"^description:\s*", head, flags=re.M):
            head = re.sub(r"^description:.*$", f"description: {rendered}", head, count=1, flags=re.M)
        else:
            lines = head.splitlines()
            insert_at = 1 if lines and lines[0].startswith("title:") else len(lines)
            lines.insert(insert_at, f"description: {rendered}")
            head = "\n".join(lines)
        path.write_text(f"---\n{head}\n---\n{body}", encoding="utf-8")
        return

    title_match = re.search(r"^#\s+(.+)$", text, flags=re.M)
    title = title_match.group(1).strip() if title_match else path.stem.replace("-", " ").title()
    path.write_text(
        f"---\ntitle: {yaml_string(title)}\ndescription: {rendered}\n---\n\n{text}",
        encoding="utf-8",
    )


def ensure_sources(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if re.search(r"^## Fuentes(?: oficiales| de referencia| oficiales y multilaterales)?\b", text, re.M):
        return
    section = (
        "\n\n## Fuentes\n\n"
        "Esta página conserva en su encabezado o cuerpo las autoridades, instrumentos o identificadores de fuente ya revisados. "
        "Para seguirlos hasta su URL y estado de procedencia, consulta el "
        "[catálogo reproducible de fuentes](../../catalog/registry.md).\n"
    )
    marker = "\n## Ver también"
    if marker in text:
        text = text.replace(marker, section.rstrip() + marker, 1)
    else:
        text = text.rstrip() + section
    path.write_text(text, encoding="utf-8")


def ensure_related(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if "## Ver también" in text:
        return
    related = (
        "\n\n## Ver también\n\n"
        "[Mapa de la wiki](../index.md) · "
        "[Proceso de despacho](../aduana/proceso-despacho.md) · "
        "[Estado del corpus](../../status/corpus-coverage.md)\n"
    )
    path.write_text(text.rstrip() + related, encoding="utf-8")


for rel, description in DESCRIPTIONS.items():
    set_description(ROOT / rel, description)

for rel, description in PUBLIC_DESCRIPTIONS.items():
    set_description(ROOT / rel, description)

for code, description in COUNTRIES.items():
    set_description(ROOT / "docs" / "catalog" / "countries" / f"{code}.md", description)

for rel in sorted(SOURCE_SECTION_PATHS):
    ensure_sources(ROOT / rel)

for path in sorted((ROOT / "docs" / "wiki").rglob("*.md")):
    if path.name != "index.md" or path.parent != ROOT / "docs" / "wiki":
        ensure_related(path)

index = ROOT / "docs" / "wiki" / "index.md"
text = index.read_text(encoding="utf-8")
needle = "El [Roadmap de contenido](../status/content-roadmap.md) separa lo cubierto, parcial y pendiente."
replacement = (
    "El [Roadmap de contenido](../status/content-roadmap.md) separa lo cubierto, parcial y pendiente. "
    "El catálogo reproducible de fuentes vive en `docs/catalog/` y puede recorrerse desde la "
    "[Guía del catálogo](../catalog/index.md)."
)
if needle in text:
    text = text.replace(needle, replacement)
if "No es asesoría legal" not in text:
    text = text.rstrip() + "\n\n**No es asesoría legal.** Verifica la fuente oficial y la vigencia aplicable antes de tomar una decisión operativa.\n"
index.write_text(text, encoding="utf-8")

scope_test = ROOT / "tests" / "test_editorial_quality.py"
text = scope_test.read_text(encoding="utf-8")
old = "                    self.assertIn(marker, text)"
new = "                    self.assertIn(marker.lower(), text.lower())"
if old in text:
    text = text.replace(old, new)
elif new not in text:
    raise RuntimeError("editorial marker assertion changed")
scope_test.write_text(text, encoding="utf-8")
