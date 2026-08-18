#!/usr/bin/env python3
"""Build a cited BCMM transport-mode chart from INEGI's official CSV ZIP."""

from __future__ import annotations

import csv
import sys
import zipfile
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
ZIP_PATH = ROOT / "data/external/inegi_bcmm/conjunto_de_datos_bcmm_mensual_mtra_csv.zip"
CSV_MEMBER = "conjunto_de_datos/bcmm_mtra_aduana_mensual_tr_cifra_2012_2026.csv"
SUMMARY_PATH = ROOT / "data/external/inegi_bcmm/bcmm_mtra_2026_05_transport_summary.csv"
CHART_PATH = ROOT / "docs/assets/images/bcmm-modo-transporte-2026-05.png"
MODES = ("Aéreo", "Carretero", "Ferroviario", "Marítimo", "Otros modos")


def main() -> int:
    if not ZIP_PATH.is_file():
        raise SystemExit(f"Missing source ZIP: {ZIP_PATH}")

    values: dict[tuple[str, str], float] = {}
    with zipfile.ZipFile(ZIP_PATH) as archive:
        with archive.open(CSV_MEMBER) as raw:
            rows = csv.DictReader((line.decode("utf-8-sig") for line in raw))
            for row in rows:
                if (
                    row["COBERTURA"] == "Nacional"
                    and row["ANIO"] == "2026"
                    and row["MES"] == "05"
                    and row["CONCEPTO"] in MODES
                    and row["TIPO"] in {"Exportación", "Importación"}
                    and row["ESTATUS_CIFRA"] == "Disponible"
                ):
                    values[(row["CONCEPTO"], row["TIPO"])] = float(row["VAL_USD"])

    expected = {(mode, flow) for mode in MODES for flow in ("Exportación", "Importación")}
    missing = expected - values.keys()
    if missing:
        raise SystemExit(f"Missing expected BCMM records: {sorted(missing)}")

    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with SUMMARY_PATH.open("w", newline="", encoding="utf-8") as output:
        writer = csv.writer(output)
        writer.writerow(["modo_transporte", "exportacion_millones_usd", "importacion_millones_usd", "periodo", "estatus"])
        for mode in MODES:
            writer.writerow([mode, f"{values[(mode, 'Exportación')]:.3f}", f"{values[(mode, 'Importación')]:.3f}", "2026-05", "Cifras Revisadas"])

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, axis = plt.subplots(figsize=(11, 6.4), layout="constrained")
    positions = list(range(len(MODES)))
    width = 0.36
    export_values = [values[(mode, "Exportación")] for mode in MODES]
    import_values = [values[(mode, "Importación")] for mode in MODES]
    export = axis.bar([position - width / 2 for position in positions], export_values, width, label="Exportación", color="#0e7490")
    imports = axis.bar([position + width / 2 for position in positions], import_values, width, label="Importación", color="#d97706")

    axis.set_title(
        "Comercio exterior por modo de transporte\nMéxico, mayo de 2026 · valor registrado en millones de USD · cifras revisadas",
        loc="left",
        fontweight="bold",
        fontsize=16,
        pad=16,
    )
    axis.set_ylabel("Millones de USD")
    axis.set_xticks(positions, MODES)
    axis.legend(frameon=False, ncols=2, loc="upper right")
    axis.spines[["top", "right"]].set_visible(False)
    axis.bar_label(export, labels=[f"{value:,.0f}" for value in export_values], padding=3, fontsize=8, rotation=90)
    axis.bar_label(imports, labels=[f"{value:,.0f}" for value in import_values], padding=3, fontsize=8, rotation=90)
    axis.text(
        0,
        -0.22,
        "Fuente: INEGI con base en SAT, SE, BANXICO e INEGI, BCMM; conjunto mensual por modo de transporte, aduana y capítulo (corte mayo de 2026).\n"
        "La visualización describe comercio agregado; no determina requisitos, fracción, origen, autorización ni cumplimiento de una operación individual.",
        transform=axis.transAxes,
        fontsize=8.3,
        color="#475569",
        va="top",
    )
    CHART_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(CHART_PATH, dpi=180, bbox_inches="tight", facecolor="white")
    print(f"Wrote {SUMMARY_PATH.relative_to(ROOT)}")
    print(f"Wrote {CHART_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
