# Legal Currentness Regression Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert already-verified Mexican legal-currentness facts into deterministic regression tests and correct the remaining confirmed false attribution in the RGCE 2026 / Anexo 13 corpus.

**Architecture:** Keep legal-currentness tests small and explicit. They do not attempt to prove every legal statement in the corpus. Instead, they protect a short set of high-risk facts that were independently verified against primary sources: the current Ley Aduanera reform date, the LIC/LFMN framework for NOMs, and the origin of the 2026 prevalidation payment in RGCE rule 1.8.3. The tests run offline against committed Markdown and fail when stale or false claims reappear.

**Tech Stack:** Python 3.12 standard library, `unittest`, existing deterministic `repository-ci`, Markdown corpus.

## Global Constraints

- Use primary official sources to establish each protected fact before encoding it in a test.
- Do not fetch the web from required PR CI.
- Do not pretend these tests certify the entire corpus as legally correct.
- Preserve `authority: derived_non_authoritative` for corpus summaries.
- Do not mix the broader NOM/Anexo 2.4.1 content audit into this PR.
- Do not rewrite the Ley Aduanera digest as if it were already a full rebuild; its current `digest_status: stale_pending_full_rebuild` warning remains truthful.
- Keep tests readable enough that a reviewer can understand the legal invariant without reverse engineering a framework.

## Verified Primary-Source Facts Protected by This Plan

1. Cámara de Diputados lists the current Ley Aduanera last reform as DOF 19-11-2025 and quantities updated by RGCE/Anexo 13 DOF 27-12-2025.
2. The Ley Federal sobre Metrología y Normalización was abrogated effective 30-08-2020 by the decree that issued the Ley de Infraestructura de la Calidad.
3. Original RGCE 2026 published 27-12-2025 already contains rule 1.8.3 with a $350.00 prevalidation payment.
4. The First Resolution modifying RGCE 2026, published 14-05-2026, reforms rules 1.4.14 and 1.5.1, adds to 1.5.1 and 4.8.4, and derogates part of 4.8.2. It does not reform rule 1.8.3.

---

## File Structure

- Create `tests/test_legal_currentness.py`: high-risk legal-currentness regression tests over committed corpus files.
- Modify `data/corpus/anexo-13-multas-cantidades.md`: correct the false attribution of the $350 amount to the First RMRGCE 2026 and tighten the annual-update wording.
- Modify `.github/workflows/ci.yml`: include `tests.test_legal_currentness` in the deterministic unit-test command.
- No changes to official snapshots, manifests, registry identities, or RAG architecture in this PR.

---

### Task 1: Protect the current Ley Aduanera reform date

**Files:**
- Create: `tests/test_legal_currentness.py`

**Interfaces:**
- Consumes: `data/corpus/ley-aduanera.md`.
- Produces: an offline regression that prevents the old 2021 currentness claim from returning.

- [ ] **Step 1: Write the test**

Create:

```python
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data" / "corpus"


class LegalCurrentnessTests(unittest.TestCase):
    def test_ley_aduanera_currentness_metadata(self):
        text = (CORPUS / "ley-aduanera.md").read_text(encoding="utf-8")
        self.assertIn("**Última reforma:** DOF 19-11-2025", text)
        self.assertIn(
            "**Cantidades actualizadas por:** RGCE y Anexo 13 DOF 27-12-2025",
            text,
        )
        self.assertNotIn("**Última reforma:** DOF 12-11-2021", text)
        self.assertIn("digest_status: stale_pending_full_rebuild", text)
```

- [ ] **Step 2: Run and verify the existing corrected file is GREEN**

Run:

```bash
python -m unittest tests.test_legal_currentness
```

Expected: PASS. This test captures an already-corrected fact as a non-regression contract.

- [ ] **Step 3: Commit the protected currentness contract**

```bash
git add tests/test_legal_currentness.py
git commit -m "test: protect Ley Aduanera currentness"
```

---

### Task 2: Protect the current NOM legal framework

**Files:**
- Modify: `tests/test_legal_currentness.py`

**Interfaces:**
- Consumes: `data/corpus/noms-comercio-exterior.md` and `data/corpus/noms-maestro-anexo-241.md`.
- Produces: a regression preventing the abrogated LFMN from being reintroduced as the current legal framework.

- [ ] **Step 1: Add NOM framework tests**

Add:

```python
    def test_nom_documents_use_ley_infraestructura_calidad_as_current_framework(self):
        for filename in (
            "noms-comercio-exterior.md",
            "noms-maestro-anexo-241.md",
        ):
            with self.subTest(filename=filename):
                text = (CORPUS / filename).read_text(encoding="utf-8")
                self.assertIn("Ley de Infraestructura de la Calidad", text)
                self.assertIn("LFMN", text)
                self.assertIn("abrogada", text.lower())
                self.assertNotIn("**Marco legal:** Ley Federal sobre Metrología", text)
```

- [ ] **Step 2: Run and verify GREEN against the current corrected documents**

```bash
python -m unittest tests.test_legal_currentness
```

Expected: PASS.

- [ ] **Step 3: Commit**

```bash
git add tests/test_legal_currentness.py
git commit -m "test: protect current NOM legal framework"
```

---

### Task 3: Encode the confirmed RGCE 1.8.3 false attribution as RED

**Files:**
- Modify: `tests/test_legal_currentness.py`
- Later modify: `data/corpus/anexo-13-multas-cantidades.md`

**Interfaces:**
- Consumes: `data/corpus/anexo-13-multas-cantidades.md`.
- Produces: a test that fails on the current false statement before the content is corrected.

- [ ] **Step 1: Add a test for the legal invariant**

Add:

```python
    def test_rgce_2026_prevalidation_amount_is_not_attributed_to_first_modification(self):
        text = (CORPUS / "anexo-13-multas-cantidades.md").read_text(encoding="utf-8")
        false_attribution = (
            "la 1a. Resolución de Modificaciones a las RGCE 2026, DOF 14-05-2026, "
            "reformó la regla 1.8.3. para establecer este nuevo monto"
        )
        self.assertNotIn(false_attribution, text)
        self.assertIn("$350.00 por pedimento prevalidado", text)
        self.assertIn("RGCE 2026 original", text)
        self.assertIn("no reformó la regla 1.8.3", text)
```

- [ ] **Step 2: Run and verify RED before editing the corpus**

Run:

```bash
python -m unittest tests.test_legal_currentness
```

Expected: FAIL because the current corpus still contains the false First-RMRGCE attribution and does not yet contain the correction language.

- [ ] **Step 3: Record the RED evidence in the PR workflow history**

Do not edit the corpus until the failing CI/test result is visible on the implementation PR.

---

### Task 4: Correct the Anexo 13 / rule 1.8.3 statement minimally

**Files:**
- Modify: `data/corpus/anexo-13-multas-cantidades.md`

**Interfaces:**
- Consumes: verified primary-source facts above.
- Produces: a corrected derived explanation that no longer invents a modifying resolution.

- [ ] **Step 1: Replace only the false Art. 16-A explanation**

Replace:

```markdown
**$350.00 por pedimento prevalidado** (antes $310.00 en 2025; la 1a. Resolución de Modificaciones a las RGCE 2026, DOF 14-05-2026, reformó la regla 1.8.3. para establecer este nuevo monto)
```

with:

```markdown
**$350.00 por pedimento prevalidado.** La regla 1.8.3 de las **RGCE 2026 originales, publicadas en el DOF el 27-12-2025**, ya establecía este monto. En las RGCE 2025 la regla 1.8.3 señalaba $310.00. La **Primera Resolución de Modificaciones a las RGCE 2026, DOF 14-05-2026, no reformó la regla 1.8.3**; modificó otras reglas, por lo que no debe atribuirse a esa resolución el cambio $310 → $350.
```

- [ ] **Step 2: Tighten the broad percentage wording**

Replace the broad metadata claim:

```markdown
**Incremento 2026 vs. 2025:** Aproximadamente **+13%** en la mayoría de los conceptos.
```

with a narrower statement tied to the official update factor:

```markdown
**Factor oficial de actualización publicado para 2026:** **1.1245**. Equivale a un ajuste de **12.45%** sobre las cantidades base a las que aplica el factor; no implica que cada concepto de este digest tenga exactamente el mismo cambio interanual.
```

Do not infer changes for individual articles that have not been checked directly.

- [ ] **Step 3: Remove any downstream sentence that repeats the blanket `~13%` claim**

If the file says that all Article 176-related amounts or all published amounts changed by `~13%`, rewrite that sentence to direct the reader to the official Anexo 13 without claiming a uniform percentage.

- [ ] **Step 4: Run the legal regression test and verify GREEN**

```bash
python -m unittest tests.test_legal_currentness
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add data/corpus/anexo-13-multas-cantidades.md tests/test_legal_currentness.py
git commit -m "fix: correct RGCE prevalidation attribution"
```

---

### Task 5: Put legal-currentness regressions in deterministic CI

**Files:**
- Modify: `.github/workflows/ci.yml`

**Interfaces:**
- Consumes: `tests.test_legal_currentness`.
- Produces: existing stable `repository-ci` now blocks merges that reintroduce these verified stale/false claims.

- [ ] **Step 1: Extend the unit-test command**

Change:

```yaml
run: python -m unittest tests.test_career_wiki tests.test_repository_validator
```

into:

```yaml
run: >-
  python -m unittest
  tests.test_career_wiki
  tests.test_repository_validator
  tests.test_legal_currentness
```

- [ ] **Step 2: Verify the CI remains offline**

The test file must use only local `Path.read_text`. It must not import `requests`, `urllib.request`, or invoke any network command.

- [ ] **Step 3: Run the complete deterministic sequence**

Expected CI steps:

```text
repository tests including legal currentness  PASS
repository validator                          PASS
mkdocs build --strict                         PASS
```

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/ci.yml
git commit -m "ci: enforce legal currentness regressions"
```

---

## Verification Checklist

Before merge:

- [ ] Ley Aduanera test requires DOF 19-11-2025.
- [ ] Ley Aduanera test requires quantities update DOF 27-12-2025.
- [ ] Ley Aduanera digest still warns that a full rebuild remains pending.
- [ ] NOM tests require the Ley de Infraestructura de la Calidad.
- [ ] NOM tests require the LFMN to be described as abrogated.
- [ ] A RED run was observed for the current false rule-1.8.3 attribution before editing the corpus.
- [ ] The corrected Anexo 13 text says original RGCE 2026 already contained $350.
- [ ] The corrected text says First RMRGCE 2026 did not reform rule 1.8.3.
- [ ] Broad `~13%` language is replaced by the official factor 1.1245 / 12.45% with scope caveat.
- [ ] `python -m unittest tests.test_legal_currentness` passes.
- [ ] `repository-ci` passes.
- [ ] `python -m scripts.validate_repository` passes.
- [ ] `mkdocs build --strict` passes.
- [ ] CodeQL underlying Actions/Python jobs do not regress.

## Deferred Deliberately

- full legal rebuild of `ley-aduanera.md`
- comprehensive verification of every amount in Anexo 13
- comprehensive NOM title/applicability audit
- verification of every 2026 operational claim in `noms-comercio-exterior.md`
- Anexo 2.4.1 29-05-2026 line-by-line audit
- claim-level provenance locators and corpus-wide front matter migration
