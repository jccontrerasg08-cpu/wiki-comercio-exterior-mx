import unittest
import time
from provenance_engine import ProvenanceRecord, SourceAuthority, LegalValidator

class ProvenanceEngineTests(unittest.TestCase):
    def test_record_creates_sha256(self):
        record = ProvenanceRecord("DOF", SourceAuthority.PRIMARY_PUBLICATION, "Texto de prueba")
        self.assertIn("sha256", record.to_dict())
        self.assertEqual(record.content_length, 15)

    def test_validator_fails_closed_on_old_data(self):
        record = ProvenanceRecord("DOF", SourceAuthority.PRIMARY_PUBLICATION, "Texto")
        record.fetched_at = time.time() - (40 * 24 * 3600)  # 40 días atrás
        
        result = LegalValidator.evaluate_record(record)
        self.assertEqual(result["status"], "FAIL_CLOSED")
        
    def test_validator_warns_on_secondary_sources(self):
        record = ProvenanceRecord("SRE", SourceAuthority.INFORMATIVE_REFERENCE, "Texto")
        
        result = LegalValidator.evaluate_record(record)
        self.assertEqual(result["status"], "WARNING")
        
    def test_validator_accepts_fresh_primary_sources(self):
        record = ProvenanceRecord("DOF", SourceAuthority.PRIMARY_PUBLICATION, "Texto")
        
        result = LegalValidator.evaluate_record(record)
        self.assertEqual(result["status"], "OK")

if __name__ == "__main__":
    unittest.main()
