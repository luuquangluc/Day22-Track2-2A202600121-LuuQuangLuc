# 📋 Lab Rubric — Day 22: LangSmith + Prompt Versioning

**Total: 100 points**  
**Deliverables:** Public GitHub repo with source code + `evidence/` folder + LangSmith project URL

---

## Scoring Overview

| Task | Max Points | Key Deliverable |
|------|-----------|-----------------|
| Task 1 — LangSmith RAG Pipeline | 25 pts | ≥ 50 LangSmith traces |
| Task 2 — Prompt Hub & A/B Routing | 25 pts | 2 Hub versions + 50 more traces |
| Task 3 — RAGAS Evaluation | 25 pts | JSON report, faithfulness ≥ 0.8 |
| Task 4 — Guardrails Validators | 25 pts | PII blocked, JSON repaired |

---

## Task 1 — LangSmith RAG Pipeline (25 pts)

### Criteria

| # | Criterion | Points |
|---|-----------|--------|
| 1.1 | Knowledge base is split into chunks and indexed with FAISS correctly | 5 pts |
| 1.2 | RAG chain built with LangChain (retriever → prompt → LLM → parser) | 5 pts |
| 1.3 | `@traceable` decorator applied; at least 50 traces visible in LangSmith UI | 10 pts |
| 1.4 | LangSmith traces contain input question, retrieved context, and LLM answer | 5 pts |

### Deductions

| Issue | Penalty |
|-------|---------|
| Fewer than 50 traces in LangSmith | −5 pts |
| Traces missing retrieved context (wrong chain structure) | −3 pts |
| Hard-coded API keys committed to code | −10 pts |
| `LANGCHAIN_TRACING_V2` not enabled → traces absent | −10 pts |

---

## Task 2 — Prompt Hub & A/B Routing (25 pts)

### Criteria

| # | Criterion | Points |
|---|-----------|--------|
| 2.1 | Two semantically different system prompts written | 5 pts |
| 2.2 | Both prompts pushed to LangSmith Prompt Hub (visible in UI) | 8 pts |
| 2.3 | Prompts pulled from Hub (not just used locally) | 4 pts |
| 2.4 | A/B routing is **deterministic** — same `request_id` always maps to same version | 5 pts |
| 2.5 | Both versions receive queries; console log shows version label per query | 3 pts |

### Deductions

| Issue | Penalty |
|-------|---------|
| Only 1 prompt version in Hub | −8 pts |
| Routing is random (non-deterministic) | −5 pts |
| Prompts not pulled from Hub (bypassed) | −4 pts |
| No version label in logs | −3 pts |

---

## Task 3 — RAGAS Evaluation (25 pts)

### Criteria

| # | Criterion | Points |
|---|-----------|--------|
| 3.1 | All 50 QA pairs run through **both** prompt versions | 5 pts |
| 3.2 | `EvaluationDataset` built with correct `SingleTurnSample` fields | 5 pts |
| 3.3 | All 4 metrics computed: `faithfulness`, `answer_relevancy`, `context_recall`, `context_precision` | 8 pts |
| 3.4 | Faithfulness ≥ 0.8 for at least one prompt version | 5 pts |
| 3.5 | `data/ragas_report.json` saved with V1 and V2 scores | 2 pts |

### Deductions

| Issue | Penalty |
|-------|---------|
| Fewer than 50 QA pairs evaluated | −1 pt per 5 missing pairs |
| Only 1 prompt version evaluated | −5 pts |
| Missing any of the 4 RAGAS metrics | −2 pts per missing metric |
| Faithfulness < 0.8 for both versions | −5 pts |
| No saved report file | −2 pts |

### Bonus

| Bonus | Points |
|-------|--------|
| Faithfulness ≥ 0.9 for both prompt versions | +3 pts |
| Analysis comment explaining why V1 or V2 scores higher | +2 pts |

---

## Task 4 — Guardrails Validators (25 pts)

### PII Detector (13 pts)

| # | Criterion | Points |
|---|-----------|--------|
| 4.1 | Custom validator created using `@register_validator` | 3 pts |
| 4.2 | Detects at least 3 PII types (email, phone, SSN, or credit card) | 5 pts |
| 4.3 | `on_fail=OnFailAction.FIX` used; blocked output replaced with safe string | 3 pts |
| 4.4 | Demonstrated on 5+ test cases (including clean and multiple PII types) | 2 pts |

### JSON Formatter (12 pts)

| # | Criterion | Points |
|---|-----------|--------|
| 4.5 | Custom validator created that checks JSON parseability | 3 pts |
| 4.6 | Auto-repair implemented (at least 2 of: strip fences, fix quotes, trailing commas) | 5 pts |
| 4.7 | Fallback error JSON returned when repair fails | 2 pts |
| 4.8 | Demonstrated on 4+ test cases (valid, fenced/malformed, broken) | 2 pts |

### Deductions

| Issue | Penalty |
|-------|---------|
| Using built-in hub validator instead of custom implementation | −5 pts |
| `on_fail` passed to `Guard.use()` instead of validator constructor | −3 pts |
| PII detection uses no regex (only string matching) | −3 pts |

---

## Evidence & Submission Quality (up to +5 pts)

| Criterion | Points |
|-----------|--------|
| All 7 required evidence files present and clearly labelled | +3 pts |
| LangSmith project URL submitted and publicly accessible | +1 pt |
| `evidence/README.md` with a brief analysis of V1 vs V2 results | +1 pt |

---

## Code Quality Bonus (up to +5 pts)

| Criterion | Points |
|-----------|--------|
| Clean, well-structured code with docstrings | +2 pts |
| All steps work via `run_all.py` without modification | +2 pts |
| Error handling and graceful fallbacks implemented | +1 pt |

---

## Submission Checklist

**Code files — all must run without errors:**
- [x] `01_langsmith_rag_pipeline.py`
- [x] `02_prompt_hub_ab_routing.py`
- [x] `03_ragas_evaluation.py`
- [x] `04_guardrails_validator.py`
- [x] `data/ragas_report.json` — exists and contains V1 + V2 scores

**Evidence folder — all required:**
- [x] `evidence/01_langsmith_traces.png` — LangSmith UI with ≥ 50 traces visible
- [x] `evidence/02_prompt_hub.png` — Prompt Hub UI showing 2 named prompt versions
- [x] `evidence/02_ab_routing_log.txt` — console log of A/B routing (50 queries, v1/v2 labels)
- [x] `evidence/03_ragas_scores.png` — terminal output with V1 vs V2 comparison table
- [x] `evidence/03_ragas_report.json` — copy of `data/ragas_report.json`
- [x] `evidence/04_pii_demo_log.txt` — console output of PII test cases
- [x] `evidence/04_json_demo_log.txt` — console output of JSON repair test cases

**Submission:**
- [x] Public GitHub repo URL submitted
- [] LangSmith project URL submitted (visible ≥ 100 total traces)
- [x] No `.env` file committed; no API keys in source code

**Penalty: −10 pts if API keys are found in committed code.**
