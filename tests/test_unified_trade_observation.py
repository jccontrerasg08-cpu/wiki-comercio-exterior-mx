import json
import unittest
from pathlib import Path

import jsonschema
import yaml


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "unified-trade-observation.schema.json"
MODEL_PATH = ROOT / "data" / "contracts" / "unified-trade-data-model.yaml"


class UnifiedTradeObservationTests(unittest.TestCase):
    def _load_contracts(self):
        if not SCHEMA_PATH.exists() or not MODEL_PATH.exists():
            self.fail("El esquema y el contrato de datos unificado deben existir antes de aceptar observaciones.")
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        model = yaml.safe_load(MODEL_PATH.read_text(encoding="utf-8"))
        return schema, model

    def test_model_keeps_domains_separate_and_declares_logical_key(self):
        _, model = self._load_contracts()
        self.assertEqual(model["model_version"], "1.0")
        self.assertEqual(
            set(model["controlled_vocabularies"]["domain"]),
            {"revenue_anam", "tariff", "trade_flow"},
        )
        self.assertIn("domain", model["logical_key"])
        self.assertIn("source_dataset_id", model["logical_key"])
        self.assertIn("observation_period", model["logical_key"])
        self.assertIn("geometry_mode", model["cross_repo_boundaries"])
        self.assertEqual(model["cross_repo_boundaries"]["geometry_mode"], "contract-only")

    def test_schema_accepts_representative_observations_with_provenance(self):
        schema, model = self._load_contracts()
        validator = jsonschema.Draft202012Validator(schema)
        for observation in model["representative_observations"]:
            errors = list(validator.iter_errors(observation))
            self.assertEqual(errors, [], errors)

    def test_schema_rejects_domain_specific_mixing(self):
        schema, model = self._load_contracts()
        invalid = dict(model["representative_observations"][0])
        invalid["domain"] = "revenue_anam"
        invalid["tariff"] = {"rate_type": "mfn_applied", "rate_value": 5, "rate_unit": "percent"}
        errors = list(jsonschema.Draft202012Validator(schema).iter_errors(invalid))
        self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main()
