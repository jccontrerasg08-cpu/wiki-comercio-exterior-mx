"""
Motor de Proveniencia y Jerarquía de Fuentes (Provenance Engine).
Inspirado en el diseño para wiki-comercio-exterior-mx.

Implementa `failClosed()` y asignación de autoridad (`source hierarchy`)
para evitar presentar conclusiones legales basadas en datos desactualizados
o de fuentes secundarias sin verificación.
"""

import hashlib
import time
from enum import IntEnum
from typing import Dict, Any, Optional

class SourceAuthority(IntEnum):
    PRIMARY_PUBLICATION = 1       # ej. DOF / SIDOF
    OFFICIAL_CONSOLIDATION = 2    # ej. Diputados
    OFFICIAL_DATASET = 3          # ej. SNICE / Banxico
    INFORMATIVE_REFERENCE = 4     # ej. SRE
    INTERGOVERNMENTAL = 5         # ej. WITS
    DERIVED_CONTENT = 6           # Contenido de la wiki

class ProvenanceRecord:
    def __init__(self, source_name: str, authority: SourceAuthority, content: str, fetched_at: float = None):
        self.source_name = source_name
        self.authority = authority
        self.fetched_at = fetched_at or time.time()
        self.sha256 = hashlib.sha256(content.encode('utf-8')).hexdigest()
        self.content_length = len(content)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_name": self.source_name,
            "authority_level": self.authority.value,
            "authority_name": self.authority.name,
            "fetched_at": self.fetched_at,
            "sha256": self.sha256,
            "content_length": self.content_length
        }

class LegalValidator:
    """Implementa el patrón failClosed() para consultas legales."""
    
    MAX_AGE_SECONDS = 30 * 24 * 3600  # 30 días de vigencia por defecto
    
    @classmethod
    def evaluate_record(cls, record: ProvenanceRecord) -> Dict[str, Any]:
        """
        Evalúa un registro y decide si es seguro mostrarlo como vigente.
        Si falla la comprobación de vigencia o autoridad, aplica failClosed().
        """
        age = time.time() - record.fetched_at
        
        if age > cls.MAX_AGE_SECONDS:
            return {
                "status": "FAIL_CLOSED",
                "reason": "Fuente desactualizada",
                "message": f"⚠️ Resultado no confirmado. El dataset tiene {int(age/86400)} días de antigüedad.",
                "record": record.to_dict()
            }
            
        if record.authority > SourceAuthority.OFFICIAL_DATASET:
            return {
                "status": "WARNING",
                "reason": "Fuente secundaria",
                "message": "⚖ Fuente informativa. Requiere verificación contra DOF.",
                "record": record.to_dict()
            }
            
        return {
            "status": "OK",
            "reason": "Confirmado",
            "message": "✅ Confirmado contra fuente primaria/oficial reciente.",
            "record": record.to_dict()
        }

