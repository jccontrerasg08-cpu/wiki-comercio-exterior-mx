from __future__ import annotations

from datetime import date, datetime, timezone
import unittest

from scripts.snice_intelligence import (
    build_series,
    detect_missing_companions,
    detect_size_anomaly,
    diff_rows,
    parse_index_html,
    parse_snice_filename,
)


class SniceFilenameTests(unittest.TestCase):
    def test_parses_modern_snapshot_name(self) -> None:
        parsed = parse_snice_filename(
            "VALIDADOS-ETIQUETADO_20260814-20260814.xlsx"
        )

        self.assertEqual(parsed.family, "VALIDADOS")
        self.assertEqual(parsed.category, "ETIQUETADO")
        self.assertEqual(parsed.filename_date, date(2026, 8, 14))
        self.assertEqual(parsed.source_date, date(2026, 8, 14))
        self.assertEqual(parsed.extension, "xlsx")

    def test_normalizes_known_typo_aliases(self) -> None:
        parsed = parse_snice_filename(
            "TEXITL_MAYO_2026-PERMISO-AUTOMATICO-IMPORTACION_20260625-20260625.xlsx"
        )

        self.assertEqual(parsed.family, "TEXTIL")
        self.assertEqual(parsed.period_year, 2026)
        self.assertEqual(parsed.period_month, 5)

    def test_extracts_business_period_before_upload_date(self) -> None:
        parsed = parse_snice_filename(
            "IMMEX_JUNIO_2026-DIRECTORIO_20260728-20260728.xlsx"
        )

        self.assertEqual(parsed.family, "IMMEX")
        self.assertEqual(parsed.category, "DIRECTORIO")
        self.assertEqual(parsed.period_year, 2026)
        self.assertEqual(parsed.period_month, 6)
        self.assertEqual(parsed.logical_dataset_id, "immex:directorio:2026-06")

    def test_handles_legacy_punctuation_without_losing_family(self) -> None:
        parsed = parse_snice_filename(
            "ACUSE*-1980-ACUSE_20230828-20230828.pdf"
        )

        self.assertEqual(parsed.family, "ACUSE")
        self.assertEqual(parsed.category, "ACUSE")
        self.assertEqual(parsed.extension, "pdf")


class SniceIndexTests(unittest.TestCase):
    def test_parses_apache_autoindex_entries(self) -> None:
        html = """
        <html><body><pre>
        <a href="VALIDADOS-ETIQUETADO_20260814-20260814.xlsx">VALIDADOS-ETIQUETADO_20260814-20260814.xlsx</a> 13-Aug-2026 22:17 1.5M
        <a href="NOVALIDADOS-ETIQUETADO_20260814-20260814.xlsx">NOVALIDADOS-ETIQUETADO_20260814-20260814.xlsx</a> 13-Aug-2026 22:25 183K
        <a href="ACUSE-3617-ACUSE_20260813-20260813.pdf">ACUSE-3617-ACUSE_20260813-20260813.pdf</a> 13-Aug-2026 16:47 289K
        </pre></body></html>
        """

        entries = parse_index_html(
            html,
            base_url="https://www.snice.gob.mx/~oracle/SNICE_DOCS/",
            discovered_at=datetime(2026, 8, 15, 18, 0, tzinfo=timezone.utc),
        )

        self.assertEqual(len(entries), 3)
        self.assertEqual(entries[0].family, "VALIDADOS")
        self.assertEqual(entries[0].bytes, 1_572_864)
        self.assertEqual(entries[1].bytes, 187_392)
        self.assertTrue(entries[2].source_url.endswith("ACUSE-3617-ACUSE_20260813-20260813.pdf"))

    def test_parses_fancyindex_table_entries(self) -> None:
        html = """
        <html><body><table>
          <tr>
            <td><a href="VALIDADOS-ETIQUETADO_20260814-20260814.xlsx">VALIDADOS-ETIQUETADO_20260814-20260814.xlsx</a></td>
            <td>13-Aug-2026 22:17</td>
            <td>1.5M</td>
          </tr>
        </table></body></html>
        """

        entries = parse_index_html(
            html,
            base_url="https://www.snice.gob.mx/~oracle/SNICE_DOCS/",
            discovered_at=datetime(2026, 8, 15, 18, 0, tzinfo=timezone.utc),
        )

        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].family, "VALIDADOS")
        self.assertEqual(entries[0].bytes, 1_572_864)


class SniceSeriesTests(unittest.TestCase):
    def _docs(self):
        html = """
        <pre>
        <a href="IMMEX_MAYO2026-DIRECTORIO_20260622-20260622.xlsx">IMMEX_MAYO2026-DIRECTORIO_20260622-20260622.xlsx</a> 22-Jun-2026 17:34 848K
        <a href="IMMEX_MAYO-2026-DIRECTORIO_20260622-20260622.xlsx">IMMEX_MAYO-2026-DIRECTORIO_20260622-20260622.xlsx</a> 22-Jun-2026 18:04 1.7M
        <a href="PROSEC_MAYO2026-DIRECTORIO_20260622-20260622.xlsx">PROSEC_MAYO2026-DIRECTORIO_20260622-20260622.xlsx</a> 22-Jun-2026 17:35 629K
        <a href="SIDERURGICO_DIC_2016-AVISO-AUTOMATICO-IMPORTACION_20201209-20201209.xlsx">SIDERURGICO_DIC_2016-AVISO-AUTOMATICO-IMPORTACION_20201209-20201209.xlsx</a> 09-Dec-2020 12:03 3.8M
        </pre>
        """
        return parse_index_html(
            html,
            base_url="https://www.snice.gob.mx/~oracle/SNICE_DOCS/",
            discovered_at=datetime(2026, 8, 15, 18, 0, tzinfo=timezone.utc),
        )

    def test_groups_reuploads_into_versions(self) -> None:
        series = build_series(self._docs())
        immex = next(
            item
            for item in series
            if item.logical_dataset_id == "immex:directorio:2026-05"
        )

        self.assertEqual(len(immex.documents), 2)
        self.assertEqual([item.version for item in immex.documents], [1, 2])
        self.assertFalse(immex.documents[0].is_replacement)
        self.assertTrue(immex.documents[1].is_replacement)

    def test_marks_historical_republication_as_backfill(self) -> None:
        series = build_series(self._docs())
        siderurgico = next(item for item in series if item.family == "SIDERURGICO")

        self.assertTrue(siderurgico.documents[0].is_backfill)
        self.assertEqual(siderurgico.period_year, 2016)
        self.assertEqual(siderurgico.period_month, 12)

    def test_detects_missing_expected_companion(self) -> None:
        docs = [doc for doc in self._docs() if doc.family != "PROSEC"]

        missing = detect_missing_companions(docs)

        self.assertIn(
            {
                "family": "IMMEX",
                "missing_family": "PROSEC",
                "period_year": 2026,
                "period_month": 5,
            },
            missing,
        )

    def test_uses_robust_size_anomaly_threshold(self) -> None:
        normal = [5_600_000, 5_700_000, 5_750_000, 5_800_000, 5_900_000]

        self.assertFalse(detect_size_anomaly(5_650_000, normal))
        self.assertTrue(detect_size_anomaly(400_000, normal))


class SniceDiffTests(unittest.TestCase):
    def test_row_diff_reports_added_removed_and_modified(self) -> None:
        previous = [
            {"rfc": "AAA010101AAA", "status": "VALIDADO", "nom": "NOM-050"},
            {"rfc": "BBB010101BBB", "status": "VALIDADO", "nom": "NOM-004"},
        ]
        current = [
            {"rfc": "AAA010101AAA", "status": "NO VALIDADO", "nom": "NOM-050"},
            {"rfc": "CCC010101CCC", "status": "VALIDADO", "nom": "NOM-020"},
        ]

        diff = diff_rows(previous, current, key_fields=("rfc",))

        self.assertEqual(diff.rows_added, 1)
        self.assertEqual(diff.rows_removed, 1)
        self.assertEqual(diff.rows_modified, 1)
        self.assertEqual(diff.modified_keys, (("AAA010101AAA",),))


if __name__ == "__main__":
    unittest.main()
