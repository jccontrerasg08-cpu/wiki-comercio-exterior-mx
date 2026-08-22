"""
Regulatory Diff Engine: Comparador de versiones para documentos legales.
Detecta adiciones, modificaciones y derogaciones entre dos versiones de un texto normativo.
"""

import difflib
from typing import List, Dict, Any

class RegulatoryDiffEngine:
    @staticmethod
    def compare_versions(old_text: str, new_text: str) -> Dict[str, Any]:
        """
        Compara dos textos (separados por líneas) y clasifica los cambios.
        Ideal para mostrar: '+ 3 adiciones, ~ 7 modificaciones, - 2 derogaciones'.
        """
        old_lines = [line.strip() for line in old_text.splitlines() if line.strip()]
        new_lines = [line.strip() for line in new_text.splitlines() if line.strip()]
        
        additions = 0
        deletions = 0
        modifications = 0
        
        changes = []
        
        matcher = difflib.SequenceMatcher(None, old_lines, new_lines)
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'replace':
                modifications += (i2 - i1)
                for line in new_lines[j1:j2]:
                    changes.append({"type": "modification", "content": line})
            elif tag == 'delete':
                deletions += (i2 - i1)
                for line in old_lines[i1:i2]:
                    changes.append({"type": "deletion", "content": line})
            elif tag == 'insert':
                additions += (j2 - j1)
                for line in new_lines[j1:j2]:
                    changes.append({"type": "addition", "content": line})
                    
        return {
            "summary": {
                "additions": additions,
                "modifications": modifications,
                "deletions": deletions,
                "total_changes": additions + modifications + deletions
            },
            "details": changes
        }

if __name__ == "__main__":
    import json
    v1 = "Artículo 1. Esta ley regula la entrada.\nArtículo 2. Derogado."
    v2 = "Artículo 1. Esta ley regula la entrada y salida.\nArtículo 3. Nuevo."
    
    diff = RegulatoryDiffEngine.compare_versions(v1, v2)
    print(json.dumps(diff, indent=2))
