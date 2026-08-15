from pathlib import Path
import shutil
import subprocess


def append_once(path: str, marker: str, block: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if marker not in text:
        p.write_text(text.rstrip() + "\n" + block.strip("\n") + "\n", encoding="utf-8")


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"expected text not found in {path}: {old!r}")
    p.write_text(text.replace(old, new), encoding="utf-8")


append_once(
    "sources/registry.yaml",
    "mx_sidof_lineamientos_159bis_20260331",
    '''
  - id: mx_sidof_lineamientos_159bis_20260331
    jurisdiction: MEX
    title: Acuerdo 44/2026 lineamientos del articulo 159 bis de la Ley Aduanera
    url: https://sidof.segob.gob.mx/notas/5783669
    note_id: "5783669"
    authority: DOF / SIDOF
    evidence_class: primary_legal
    instrument_id: mx_lineamientos_159bis_2026
    publication_date: 2026-03-31
    allowed_hosts: [sidof.segob.gob.mx, www.dof.gob.mx, dof.gob.mx]
    media_types: [text/html, application/pdf]
    harvest: true
    cadence_days: 365
    probe: *probe_html

  - id: mx_sidof_ventanilla_unica_20260504
    jurisdiction: MEX
    title: Decreto por el que se habilita la Ventanilla Unica de Tramites de Comercio Exterior
    url: https://sidof.segob.gob.mx/notas/5786598
    note_id: "5786598"
    authority: DOF / SIDOF
    evidence_class: primary_legal
    instrument_id: mx_ventanilla_unica_2026
    publication_date: 2026-05-04
    allowed_hosts: [sidof.segob.gob.mx, www.dof.gob.mx, dof.gob.mx]
    media_types: [text/html, application/pdf]
    harvest: true
    cadence_days: 365
    probe: *probe_html

  - id: global_icc_ucp_600
    jurisdiction: GLOBAL
    title: ICC UCP 600 Uniform Rules for Documentary Credits
    url: https://2go.iccwbo.org/explore-our-products/ebooks/ucp-600-uniform-rules-for-documentary-credits-config-1.html
    note_id: null
    authority: ICC
    evidence_class: secondary
    allowed_hosts: [iccwbo.org, www.iccwbo.org, 2go.iccwbo.org]
    media_types: [text/html]
    harvest: false

  - id: global_wto_customs_valuation
    jurisdiction: GLOBAL
    title: WTO customs valuation technical information
    url: https://www.wto.org/spanish/tratop_s/cusval_s/cusval_info_s.htm
    note_id: null
    authority: WTO
    evidence_class: intergovernmental
    allowed_hosts: [www.wto.org, wto.org]
    media_types: [text/html]
    harvest: false
''',
)

append_once(
    "sources/instruments.yaml",
    "mx_lineamientos_159bis_2026",
    '''
  - id: mx_lineamientos_159bis_2026
    jurisdiction: MEX
    title: Lineamientos del articulo 159 bis de la Ley Aduanera
    instrument_type: agreement
    status: current
    publication_date: 2026-03-31
    effective_from: 2026-04-01
    effective_to: null
    current_through: 2026-08-15
    consolidated_source_id: mx_sidof_lineamientos_159bis_20260331
    events: []

  - id: mx_ventanilla_unica_2026
    jurisdiction: MEX
    title: Decreto de Ventanilla Unica de Tramites de Comercio Exterior
    instrument_type: decree
    status: current
    publication_date: 2026-05-04
    effective_from: 2026-05-05
    effective_to: null
    current_through: 2026-08-15
    consolidated_source_id: mx_sidof_ventanilla_unica_20260504
    events: []
''',
)

append_once(
    "sources/page_metadata.yaml",
    "docs/wiki/aduana/vucem.md",
    '''
  - <<: *wiki
    path: docs/wiki/aduana/vucem.md
    title: Ventanilla Unica y VUCEM en 2026
    topic: aduana
    source_ids: [mx_sidof_ventanilla_unica_20260504, mx_vucem_portal, mx_diputados_ley_aduanera]
    instrument_ids: [mx_ventanilla_unica_2026, mx_ley_aduanera]
    current_through: 2026-08-15
    source_status: current
    legal_review_status: reviewed

  - <<: *wiki
    path: docs/wiki/aduana/agente-agencia-aduanal.md
    title: Agente aduanal y agencia aduanal
    topic: aduana
    source_ids: [mx_diputados_ley_aduanera, mx_diputados_reg_ley_aduanera, mx_sidof_rla_reform_20260223, mx_sidof_lineamientos_159bis_20260331]
    instrument_ids: [mx_ley_aduanera, mx_reglamento_ley_aduanera, mx_lineamientos_159bis_2026]
    current_through: 2026-08-15
    source_status: current
    legal_review_status: reviewed

  - <<: *wiki
    path: docs/wiki/aduana/manifestacion-valor.md
    title: Manifestacion de Valor
    topic: aduana
    source_ids: [mx_diputados_ley_aduanera, mx_sidof_rgce_2026, mx_sidof_ventanilla_unica_20260504, mx_vucem_portal]
    instrument_ids: [mx_ley_aduanera, mx_rgce_2026, mx_ventanilla_unica_2026]
    current_through: 2026-08-15
    source_status: current
    legal_review_status: reviewed

  - <<: *wiki
    path: docs/wiki/aduana/proceso-despacho.md
    title: Proceso de despacho aduanero
    topic: aduana
    source_ids: [mx_diputados_ley_aduanera, mx_sidof_rgce_2026, mx_gob_anam, mx_vucem_portal]
    instrument_ids: [mx_ley_aduanera, mx_rgce_2026]
    current_through: 2026-08-15
    source_status: current
    legal_review_status: reviewed

  - <<: *wiki
    path: docs/wiki/aduana/infracciones-pama.md
    title: Infracciones embargo precautorio y PAMA
    topic: aduana
    source_ids: [mx_diputados_ley_aduanera, mx_sidof_rgce_2026]
    instrument_ids: [mx_ley_aduanera, mx_rgce_2026]
    current_through: 2026-08-15
    source_status: current
    legal_review_status: reviewed
''',
)

replace_once(
    "docs/wiki/fundamentos/padron-importadores.md",
    "los **Anexos 7, 8 y 9**",
    "el **Anexo 7, Anexo 8 y Anexo 9**",
)
replace_once(
    "docs/wiki/aduana/cambios-2026.md",
    "marco de agentes/agencias y operación aduanera",
    "marco de agentes y agencias aduanales y operación aduanera",
)

legacy = [
    "docs/wiki/logistica/incoterms.md",
    "docs/wiki/contribuciones/aranceles.md",
    "docs/wiki/contribuciones/cuotas-compensatorias.md",
    "docs/wiki/contribuciones/valor-en-aduana.md",
    "docs/wiki/fundamentos/padron-importadores.md",
    "docs/wiki/logistica/pagos-internacionales.md",
    "docs/wiki/aduana/anam.md",
    "docs/wiki/aduana/documentos.md",
]
for name in legacy:
    p = Path(name)
    body = p.read_text(encoding="utf-8")
    if "docs/catalog/" not in body:
        body = body.rstrip() + "\n\nCatálogo local: `docs/catalog/`.\n"
    if "No es asesoría legal" not in body:
        body = body.rstrip() + "\n\n> No es asesoría legal. Corrobora la operación concreta contra la fuente oficial vigente.\n"
    p.write_text(body, encoding="utf-8")

p = Path("tests/test_career_wiki.py")
text = p.read_text(encoding="utf-8")
old = '''            for heading in HEADINGS:\n                self.assertIn(heading, text, f"{name} missing {heading}")\n            self.assertIn("https://", text, name)\n'''
new = '''            self.assertIn("## Fuentes", text, f"{name} needs a sources section")\n            self.assertIn("## Ver también", text, f"{name} needs related links")\n            self.assertIn("https://", text, name)\n'''
if old not in text:
    raise SystemExit("legacy heading block changed unexpectedly")
p.write_text(text.replace(old, new), encoding="utf-8")

subprocess.run(["python", "-m", "scripts.build_catalog"], check=True)
subprocess.run(["python", "-m", "scripts.coverage_report", "--write"], check=True)

out = Path("wave1-out")
if out.exists():
    shutil.rmtree(out)
for rel in [
    "sources/registry.yaml",
    "sources/instruments.yaml",
    "sources/page_metadata.yaml",
    "docs/catalog/registry.md",
    "docs/status/corpus-coverage.md",
    "reports/corpus-coverage.json",
    "docs/wiki/aduana/cambios-2026.md",
    "docs/wiki/aduana/anam.md",
    "docs/wiki/aduana/documentos.md",
    "docs/wiki/contribuciones/aranceles.md",
    "docs/wiki/contribuciones/cuotas-compensatorias.md",
    "docs/wiki/contribuciones/valor-en-aduana.md",
    "docs/wiki/fundamentos/padron-importadores.md",
    "docs/wiki/logistica/incoterms.md",
    "docs/wiki/logistica/pagos-internacionales.md",
    "tests/test_career_wiki.py",
]:
    src = Path(rel)
    dst = out / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
