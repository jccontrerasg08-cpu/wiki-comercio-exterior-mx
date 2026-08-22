"""
Procedure Engine: Máquina de estados estricta para trámites de comercio exterior.
Inspirado en el patrón ATI Observation Lab para flujos guiados.
Asegura que no se salten pasos y expone un estado público limpio.
"""

from typing import List, Dict, Any, Optional

class ProcedureState:
    def __init__(self, name: str, steps: List[str]):
        if not steps:
            raise ValueError("Un procedimiento debe tener al menos un paso.")
        self.name = name
        self.steps = steps
        self.current_step_index = 0
        self.completed_steps = set()
        self.warnings = []
        self.evidence = {}

    def next_step(self, step_name: str, evidence_data: Any = None) -> bool:
        """Avanza al paso indicado si es el esperado según la secuencia estricta."""
        if self.is_completed():
            self.warnings.append(f"Intento de avanzar en procedimiento '{self.name}' ya completado.")
            return False
            
        expected_step = self.steps[self.current_step_index]
        if step_name != expected_step:
            self.warnings.append(f"Paso incorrecto: se esperaba '{expected_step}', se recibió '{step_name}'.")
            return False
            
        self.completed_steps.add(step_name)
        if evidence_data:
            self.evidence[step_name] = evidence_data
            
        self.current_step_index += 1
        return True

    def is_completed(self) -> bool:
        return self.current_step_index >= len(self.steps)

    def public_state(self) -> Dict[str, Any]:
        """Expone un estado limpio, seguro para el frontend o logs."""
        return {
            "procedure": self.name,
            "status": "completed" if self.is_completed() else "busy",
            "current_step": None if self.is_completed() else self.steps[self.current_step_index],
            "completed": list(self.completed_steps),
            "pending": self.steps[self.current_step_index:],
            "warnings": self.warnings.copy(),
            "evidence_keys": list(self.evidence.keys())
        }

if __name__ == "__main__":
    import json
    # Demo de uso
    proc = ProcedureState("Importar Mercancía", ["clasificacion", "nico", "arancel", "rrna", "despacho"])
    proc.next_step("clasificacion", {"fraccion": "8517.13.01"})
    proc.next_step("nico", {"nico": "00"})
    
    # Intento de salto de paso
    proc.next_step("rrna", {"permiso": "ok"}) 
    
    print(json.dumps(proc.public_state(), indent=2))
