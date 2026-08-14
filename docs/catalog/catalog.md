# Catalogo

Static snapshot of `sources/registry.yaml` (must match every id/url/harvest). SHA-256 and last harvest are filled by `build_wiki.py` later.

## Contents

- [Mexico law](#mexico-law)
- [Mexico portals](#mexico-portals)
- [Global](#global)
- [Countries](#countries)
- [Registry snapshot](#registry-snapshot)

## Mexico law

- [LIGIE vigente](https://www.diputados.gob.mx/LeyesBiblio/pdf/LIGIE_2022.pdf) - Cámara de Diputados. Harvest.
- [Decreto LIGIE 29 dic 2025](https://www.diputados.gob.mx/LeyesBiblio/ref/ligie_2022/LIGIE_2022_ref02_29dic25.pdf) - Harvest.
- [Ley Aduanera](https://www.diputados.gob.mx/LeyesBiblio/pdf/LAdua.pdf) - Harvest.
- [Reglamento de la Ley Aduanera](https://www.diputados.gob.mx/LeyesBiblio/regley/Reg_LAdua.pdf) - Harvest.
- [RGCE y anexos 1–30](mexico/rgce.md) - SIDOF 2025, 2026 y modificaciones. Harvest.
- [Decreto TIGIE SIDOF](https://sidof.segob.gob.mx/notas/5777376) - 29 dic 2025. Harvest. Not RGCE.

## Mexico portals

Catalog-only unless noted. Do not scrape interactive classifiers.

- [SNICE LIGIE](https://www.snice.gob.mx/cs/avi/snice/ligie.info22.html) - IMMEX, PROSEC, RRNA lookup.
- [INEGI TIGIE–SCIAN](https://www.inegi.org.mx/app/tigie/) - Classifier. Do not scrape.
- [SNICE Mi Fracción](https://www.snice.gob.mx/cs/avi/snice/hce.mi.fraccion.arancelaria.html) - Empty CMS shell as of 2026-08-13.
- [T-MEC](https://www.gob.mx/t-mec)
- [ANAM](https://anam.gob.mx/)
- [SAT Padrón](https://www.sat.gob.mx/minisitio/PadronImportadoresExportadores/index.html)
- [UPCI](https://www.gob.mx/se/acciones-y-programas/industria-y-comercio-unidad-de-practicas-comerciales-internacionales-upci)
- [SNICE cuotas](https://www.snice.gob.mx/cs/avi/snice/drrnas.cuotascomp.html)

## Global

- [WTO Tariff and Trade Data](https://ttd.wto.org/en)
- [UN Comtrade](https://comtrade.un.org/)
- [WITS/TRAINS](https://wits.worldbank.org/)
- [ITC Market Access Map](https://www.macmap.org/)
- [CEPII BACI](https://www.cepii.fr/cepii/en/bdd_modele/bdd_modele_item.asp?id=37)
- [WCO nomenclature](https://www.wcoomd.org/en/topics/nomenclature.aspx) - HS 2022.
- [ICC Incoterms](https://iccwbo.org/business-solutions/incoterms-rules/) - Incoterms® 2020. Catalog-only. Also https://iccmex.mx/seccion/incoterms-2020 and https://2go.iccwbo.org. Do not vendor rule text.

## Countries

- [USA / USITC HTS](https://hts.usitc.gov/)
- [Canada / CBSA](https://www.cbsa-asfc.gc.ca/)
- [EU / TARIC](https://taxation-customs.ec.europa.eu/customs-4/calculation-customs-duties/customs-tariff/eu-customs-tariff-taric_en)
- [Netherlands / Douane](https://www.douane.nl/)
- [Japan Customs](https://www.customs.go.jp/)
- [China Customs (English)](http://english.customs.gov.cn/)
- [Brazil / Receita Federal](https://www.gov.br/receitafederal/)

## Registry snapshot

| id | url | harvest |
|---|---|---|
| mx_diputados_ligie_current | https://www.diputados.gob.mx/LeyesBiblio/pdf/LIGIE_2022.pdf | true |
| mx_diputados_ligie_reform_2025 | https://www.diputados.gob.mx/LeyesBiblio/ref/ligie_2022/LIGIE_2022_ref02_29dic25.pdf | true |
| mx_diputados_ley_aduanera | https://www.diputados.gob.mx/LeyesBiblio/pdf/LAdua.pdf | true |
| mx_diputados_reg_ley_aduanera | https://www.diputados.gob.mx/LeyesBiblio/regley/Reg_LAdua.pdf | true |
| mx_sidof_rgce_2025_body | https://sidof.segob.gob.mx/notas/5746326 | true |
| mx_sidof_rgce_2025 | https://sidof.segob.gob.mx/notas/5746685 | true |
| mx_sidof_rgce_2025_anexos_10_22_27 | https://sidof.segob.gob.mx/notas/5746745 | true |
| mx_sidof_rgce_2025_anexo_2 | https://sidof.segob.gob.mx/notas/5746846 | true |
| mx_sidof_rgce_2025_anexo_1 | https://sidof.segob.gob.mx/notas/5747310 | true |
| mx_sidof_rgce_2025_mod1 | https://sidof.segob.gob.mx/notas/5754200 | true |
| mx_sidof_rgce_2025_mod2 | https://sidof.segob.gob.mx/notas/5757079 | true |
| mx_sidof_rgce_2025_mod3 | https://sidof.segob.gob.mx/notas/5758614 | true |
| mx_sidof_rgce_2025_mod4 | https://sidof.segob.gob.mx/notas/5763997 | true |
| mx_sidof_rgce_2025_mod5 | https://sidof.segob.gob.mx/notas/5770439 | true |
| mx_sidof_rgce_2025_mod6 | https://sidof.segob.gob.mx/notas/5770661 | true |
| mx_sidof_rgce_2025_mod7 | https://sidof.segob.gob.mx/notas/5776301 | true |
| mx_sidof_decreto_20251229 | https://sidof.segob.gob.mx/notas/5777376 | true |
| mx_sidof_rgce_2026 | https://sidof.segob.gob.mx/notas/5777199 | true |
| mx_sidof_rgce_2026_anexo_1 | https://sidof.segob.gob.mx/notas/5777997 | true |
| mx_sidof_rgce_2026_anexo_2 | https://sidof.segob.gob.mx/notas/5778101 | true |
| mx_sidof_rgce_2026_anexos_3_20 | https://sidof.segob.gob.mx/notas/5778241 | true |
| mx_sidof_rgce_2026_anexos_21_30 | https://sidof.segob.gob.mx/notas/5778300 | true |
| mx_sidof_rgce_2026_mod1 | https://sidof.segob.gob.mx/notas/5787425 | true |
| mx_sidof_rgce_2026_mod1_anexos | https://sidof.segob.gob.mx/notas/5787982 | true |
| mx_inegi_tigie_scian | https://www.inegi.org.mx/app/tigie/ | false |
| mx_snice_mi_fraccion | https://www.snice.gob.mx/cs/avi/snice/hce.mi.fraccion.arancelaria.html | false |
| global_wto_tariff_download | https://ttd.wto.org/en | false |
| global_un_comtrade | https://comtrade.un.org/ | false |
| global_wits | https://wits.worldbank.org/ | false |
| global_itc_macmap | https://www.macmap.org/ | false |
| global_cepii_baci | https://www.cepii.fr/cepii/en/bdd_modele/bdd_modele_item.asp?id=37 | false |
| us_usitc_hts | https://hts.usitc.gov/ | false |
| can_cbsa | https://www.cbsa-asfc.gc.ca/ | false |
| eu_taric | https://taxation-customs.ec.europa.eu/customs-4/calculation-customs-duties/customs-tariff/eu-customs-tariff-taric_en | false |
| nl_douane | https://www.douane.nl/ | false |
| jp_customs | https://www.customs.go.jp/ | false |
| cn_customs | http://english.customs.gov.cn/ | false |
| br_receita | https://www.gov.br/receitafederal/ | false |
| mx_snice_ligie_info | https://www.snice.gob.mx/cs/avi/snice/ligie.info22.html | false |
| mx_gob_tmec | https://www.gob.mx/t-mec | false |
| mx_gob_anam | https://anam.gob.mx/ | false |
| mx_sat_padron | https://www.sat.gob.mx/minisitio/PadronImportadoresExportadores/index.html | false |
| global_wco | https://www.wcoomd.org/en/topics/nomenclature.aspx | false |
| mx_gob_upci | https://www.gob.mx/se/acciones-y-programas/industria-y-comercio-unidad-de-practicas-comerciales-internacionales-upci | false |
| mx_snice_cuotas | https://www.snice.gob.mx/cs/avi/snice/drrnas.cuotascomp.html | false |
| global_icc_incoterms | https://iccwbo.org/business-solutions/incoterms-rules/ | false |
