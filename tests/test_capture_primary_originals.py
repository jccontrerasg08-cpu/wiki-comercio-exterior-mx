import unittest

from scripts.capture_primary_originals import (
    build_manifest_document,
    capture_url_for,
    validate_payload,
)


DIPUTADOS = {
    "id": "mx_diputados_constitucion",
    "url": "https://www.diputados.gob.mx/LeyesBiblio/pdf/CPEUM.pdf",
    "authority": "Cámara de Diputados",
    "allowed_hosts": ["www.diputados.gob.mx"],
    "media_types": ["application/pdf"],
}

SIDOF = {
    "id": "mx_sidof_lineamientos_159bis_20260331",
    "url": "https://sidof.segob.gob.mx/notas/5783669",
    "authority": "DOF/SIDOF",
    "note_id": "5783669",
    "allowed_hosts": ["sidof.segob.gob.mx"],
    "media_types": ["text/html", "application/pdf"],
}


class CapturePrimaryOriginalsTests(unittest.TestCase):
    def test_direct_pdf_uses_canonical_url_and_pdf_suffix(self):
        url, suffix = capture_url_for(DIPUTADOS)
        self.assertEqual(url, DIPUTADOS["url"])
        self.assertEqual(suffix, ".pdf")

    def test_sidof_note_uses_official_docfuente_and_html_suffix(self):
        url, suffix = capture_url_for(SIDOF)
        self.assertEqual(url, "https://sidof.segob.gob.mx/notas/docFuente/5783669")
        self.assertEqual(suffix, ".html")

    def test_rejects_capture_url_outside_allowed_hosts(self):
        source = dict(DIPUTADOS)
        source["url"] = "https://example.com/CPEUM.pdf"
        with self.assertRaisesRegex(ValueError, "allowed_hosts"):
            capture_url_for(source)

    def test_rejects_non_pdf_payload_for_pdf_source(self):
        with self.assertRaisesRegex(ValueError, "PDF signature"):
            validate_payload(
                DIPUTADOS,
                DIPUTADOS["url"],
                "application/pdf",
                b"<html>not a pdf</html>" * 100,
            )

    def test_rejects_tiny_or_blocked_html_snapshot(self):
        capture_url, _ = capture_url_for(SIDOF)
        with self.assertRaisesRegex(ValueError, "too small"):
            validate_payload(SIDOF, capture_url, "text/html", b"<html>short</html>")
        with self.assertRaisesRegex(ValueError, "blocked"):
            validate_payload(
                SIDOF,
                capture_url,
                "text/html",
                (b"<html>Access Denied captcha</html>" + b"x" * 600),
            )

    def test_manifest_document_is_deterministic_and_keeps_canonical_url(self):
        payload = b"%PDF-1.7\n" + b"official bytes" * 100
        capture_url, _ = capture_url_for(DIPUTADOS)
        validate_payload(DIPUTADOS, capture_url, "application/pdf", payload)
        first = build_manifest_document(
            DIPUTADOS,
            "mx_diputados_constitucion.pdf",
            capture_url,
            "application/pdf",
            payload,
        )
        second = build_manifest_document(
            DIPUTADOS,
            "mx_diputados_constitucion.pdf",
            capture_url,
            "application/pdf",
            payload,
        )
        self.assertEqual(first, second)
        self.assertEqual(first["id"], DIPUTADOS["id"])
        self.assertEqual(first["url"], DIPUTADOS["url"])
        self.assertEqual(first["file"], "mx_diputados_constitucion.pdf")
        self.assertEqual(first["storage"], "local_git")
        self.assertEqual(first["bytes"], len(payload))
        self.assertEqual(len(first["sha256"]), 64)
        self.assertNotIn("capture_url", first)

    def test_sidof_manifest_records_distinct_capture_url(self):
        payload = b"<html><body>" + b"official sidof source" * 40 + b"</body></html>"
        capture_url, _ = capture_url_for(SIDOF)
        validate_payload(SIDOF, capture_url, "text/html", payload)
        document = build_manifest_document(
            SIDOF,
            "mx_sidof_lineamientos_159bis_20260331.html",
            capture_url,
            "text/html",
            payload,
        )
        self.assertEqual(document["url"], SIDOF["url"])
        self.assertEqual(document["capture_url"], capture_url)


if __name__ == "__main__":
    unittest.main()
