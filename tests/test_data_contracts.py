import unittest
from pathlib import Path

import yaml

from scripts.validate_data_contracts import validate_contract


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data" / "contracts" / "aduanamap.yaml"


class DataContractTests(unittest.TestCase):
    def test_aduanamap_contract_is_valid(self):
        data = yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))
        self.assertEqual(validate_contract(data, ROOT), [])

    def test_world_geometry_is_canonical_in_aduanamap(self):
        data = yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))
        self.assertEqual(data["canonical_repository"], "jccontrerasg08-cpu/aduanamap-mx")
        dataset = data["datasets"][0]
        self.assertEqual(dataset["id"], "world_countries_50m")
        self.assertEqual(dataset["canonical_path"], "data/geojson/countries-50m.geojson")
        self.assertEqual(dataset["generator_path"], "tools/map-build/build-countries.mjs")
        self.assertEqual(dataset["srid"], 4326)
        self.assertEqual(dataset["geometry_type"], "MultiPolygon")
        for field in ("iso2", "iso3", "name_es", "name_en", "region"):
            self.assertIn(field, dataset["schema_fields"])

    def test_contract_uses_immutable_observed_ref_and_text_fallback(self):
        data = yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))
        dataset = data["datasets"][0]
        self.assertRegex(dataset["observed_commit"], r"^[0-9a-f]{40}$")
        self.assertEqual(dataset["consumption"]["fallback"], "text_links")
        self.assertIsNone(dataset["consumption"]["public_artifact"])

    def test_wiki_does_not_vendor_canonical_geojson(self):
        geojson = [path for path in ROOT.rglob("*.geojson") if ".git" not in path.parts]
        self.assertEqual(geojson, [])

    def test_validator_rejects_wiki_owned_path_for_external_canonical_dataset(self):
        data = yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))
        data["datasets"][0]["wiki_local_copy"] = "docs/assets/countries-50m.geojson"
        errors = validate_contract(data, ROOT)
        self.assertTrue(any("wiki_local_copy" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
