import unittest
from procedure_engine import ProcedureState

class ProcedureEngineTests(unittest.TestCase):
    def test_initial_state_is_busy_and_has_first_step_pending(self):
        proc = ProcedureState("Test", ["paso1", "paso2"])
        state = proc.public_state()
        
        self.assertEqual(state["status"], "busy")
        self.assertEqual(state["current_step"], "paso1")
        
    def test_next_step_advances_only_on_correct_sequence(self):
        proc = ProcedureState("Test", ["paso1", "paso2"])
        
        # Intento de salto falla
        self.assertFalse(proc.next_step("paso2"))
        self.assertEqual(proc.public_state()["current_step"], "paso1")
        
        # Secuencia correcta avanza
        self.assertTrue(proc.next_step("paso1", {"data": "ok"}))
        self.assertEqual(proc.public_state()["current_step"], "paso2")
        self.assertIn("paso1", proc.public_state()["completed"])
        
    def test_procedure_completes_after_last_step(self):
        proc = ProcedureState("Test", ["paso1"])
        proc.next_step("paso1")
        
        state = proc.public_state()
        self.assertEqual(state["status"], "completed")
        self.assertIsNone(state["current_step"])

if __name__ == "__main__":
    unittest.main()
