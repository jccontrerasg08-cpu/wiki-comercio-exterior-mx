import json
import unittest
from pathlib import Path

import yaml

from scripts.legal_watch import enrich_sidof_items, known_publications, normalize_candidates


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "http" / "candidates.json"
DAILY_FIXTURE = ROOT / "tests" / "fixtures" / "http" / "sidof-daily.json"
DIARY_FIXTURE = ROOT / "tests" / "fixtures" / "http" / "sidof-diary.json"


class JsonResponse:
    status_code = 200

    def __init__(self, payload):
        self.body = json.dumps(payload).encode("utf-8")

    def iter_content(self, chunk_size):
        yield self.body

    def close(self):
        pass


class DiaryTransport:
    def __init__(self, payload):
        self.payload = payload
        self.urls = []

    def get(self, url, **kwargs):
        self.urls.append(url)
        return JsonResponse(self.payload)


class LegalWatchTests(unittest.TestCase):
    def setUp(self):
        self.payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.config = yaml.safe_load(
            (ROOT / "sources" / "watch.yaml").read_text(encoding="utf-8")
        )

    def test_candidates_are_deduplicated_by_note_id(self):
        known = known_publications(ROOT / "sources" / "registry.yaml")
        candidates = normalize_candidates(self.payload, self.config, known)
        self.assertEqual(candidates, ())

    def test_discovery_never_marks_candidate_current(self):
        payload = [{
            "note_id": "9999999",
            "title": "Nueva modificacion RGCE",
            "publication_date": "2026-08-15",
            "url": "https://sidof.segob.gob.mx/notas/9999999",
        }]
        candidate = normalize_candidates(payload, self.config)[0]
        self.assertEqual(candidate.review_status, "candidate")

    def test_invalid_date_and_insecure_url_are_rejected(self):
        payload = [
            {"note_id": "1", "title": "RGCE", "publication_date": "15-08-2026", "url": "https://sidof.segob.gob.mx/notas/1"},
            {"note_id": "2", "title": "RGCE", "publication_date": "2026-08-15", "url": "http://sidof.segob.gob.mx/notas/2"},
        ]
        self.assertEqual(normalize_candidates(payload, self.config), ())

    def test_candidate_urls_require_canonical_https_authority(self):
        payload = [
            {
                "note_id": "3",
                "title": "RGCE",
                "publication_date": "2026-08-15",
                "url": "https://user@sidof.segob.gob.mx/notas/3",
            },
            {
                "note_id": "4",
                "title": "RGCE",
                "publication_date": "2026-08-15",
                "url": "https://sidof.segob.gob.mx:8443/notas/4",
            },
        ]
        self.assertEqual(normalize_candidates(payload, self.config), ())

    def test_official_daily_shape_is_enriched_from_per_diary_api(self):
        daily = json.loads(DAILY_FIXTURE.read_text(encoding="utf-8"))
        diary = json.loads(DIARY_FIXTURE.read_text(encoding="utf-8"))
        transport = DiaryTransport(diary)
        items = enrich_sidof_items(daily, self.config, transport)
        candidates = normalize_candidates(items, self.config)
        self.assertEqual([item.note_id for item in candidates], ["5999999"])
        self.assertEqual(len(transport.urls), 1)
        self.assertTrue(transport.urls[0].endswith("/399999"))


if __name__ == "__main__":
    unittest.main()
