import unittest
from pathlib import Path

import yaml

from scripts.schema_validation import load_local_schema, validate_instance


ROOT = Path(__file__).resolve().parents[1]


class SchemaValidationTests(unittest.TestCase):
    def test_invalid_source_reports_sorted_paths(self):
        schema = load_local_schema(ROOT, "source.schema.json")
        findings = validate_instance(
            {
                "id": "Bad ID",
                "jurisdiction": "MEX",
                "title": "Invalid source",
                "url": "javascript:alert(1)",
                "authority": "DOF",
                "evidence_class": "primary_legal",
                "allowed_hosts": ["sidof.segob.gob.mx"],
                "media_types": ["text/html"],
                "harvest": "yes",
            },
            schema,
            "fixture",
        )
        self.assertEqual(
            [finding.path for finding in findings],
            ["fixture.harvest", "fixture.id", "fixture.url"],
        )

    def test_format_validation_is_explicitly_enabled(self):
        schema = load_local_schema(ROOT, "source.schema.json")
        findings = validate_instance(
            {
                "id": "valid_id",
                "jurisdiction": "MEX",
                "title": "Invalid URI",
                "url": "not-a-uri",
                "authority": "DOF",
                "evidence_class": "primary_legal",
                "allowed_hosts": ["sidof.segob.gob.mx"],
                "media_types": ["text/html"],
                "harvest": False,
            },
            schema,
            "source",
        )
        self.assertEqual([finding.path for finding in findings], ["source.url"])

    def test_fixture_rejects_unknown_fields(self):
        schema = load_local_schema(ROOT, "source.schema.json")
        fixture = yaml.safe_load(
            (ROOT / "tests/fixtures/schema/invalid-source.yaml").read_text(
                encoding="utf-8"
            )
        )
        findings = validate_instance(fixture, schema, "fixture")
        self.assertIn("SCHEMA_ADDITIONAL_PROPERTIES", {f.code for f in findings})

    def test_primary_source_can_reference_multiple_instruments(self):
        schema = load_local_schema(ROOT, "source.schema.json")
        findings = validate_instance(
            {
                "id": "mx_sidof_joint_decree",
                "jurisdiction": "MEX",
                "title": "Joint legal decree",
                "url": "https://sidof.segob.gob.mx/notas/1234567",
                "note_id": "1234567",
                "authority": "DOF / SIDOF",
                "evidence_class": "primary_legal",
                "instrument_ids": ["mx_ligie", "mx_programa_prosec"],
                "publication_date": "2026-04-23",
                "allowed_hosts": ["sidof.segob.gob.mx"],
                "media_types": ["text/html"],
                "harvest": False,
            },
            schema,
            "source",
        )
        self.assertEqual(findings, [])

    def test_instrument_schema_accepts_local_event_relations(self):
        schema = load_local_schema(ROOT, "instrument.schema.json")
        findings = validate_instance(
            {
                "id": "mx_example_law",
                "jurisdiction": "MEX",
                "title": "Example law",
                "instrument_type": "law",
                "status": "current",
                "publication_date": "2026-01-01",
                "effective_from": "2026-01-02",
                "effective_to": None,
                "current_through": "2026-02-01",
                "consolidated_source_id": "mx_example_consolidated",
                "events": [
                    {
                        "source_id": "mx_example_reform",
                        "relation": "amends",
                        "effective_from": "2026-02-01",
                    }
                ],
            },
            schema,
            "instrument",
        )
        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
