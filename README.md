# CareerOS — Campus IQ

AI-powered career and academic companion for Texas A&M students.
Dallas AI Group 6 | 2026 Summer Cohort.

---

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/) — Python package manager
- An OpenRouter API key for the primary Campus IQ AI path
- Optional: an Anthropic API key for the legacy direct demo script

---

## Setup

```bash
# 1. Install dependencies
uv sync

# 2. Configure your API key
cp .env.example .env
# then edit .env and replace "your-key-here" with your actual key
```

---

## Running the demo

```bash
cd CampusIQ_career/demo && uv run python campus_iq_test.py
```

To swap which student profile runs, edit `STUDENT_FILE` at the top of
`CampusIQ_career/demo/campus_iq_test.py`. The feature (FIT / GAP / SHIFT)
is read automatically from the `primary_feature` field in the student JSON.

---

## Validating data

```bash
uv run python data/validate_catalog.py
uv run python data/students/validate_students.py
```

## Unified student profile

All academic and career features should build on the same JSON record in
`data/students/`. The schema contract lives in
`data/reference/unified_student_schema.md`.

The student validator checks the shared foundation fields, including academic
record counts, career resume fields, profile completeness, and compatibility
mirrors used by future prompts/UI code.

---

## Other commands

| Command                                      | What it does                          |
|----------------------------------------------|---------------------------------------|
| `uv run python data/scrape_catalog.py`       | Re-scrape the TAMU course catalog     |
| `uv run python data/build_catalog.py`        | Rebuild catalog JSON from scrape output |

## AI Architecture

Campus IQ uses OpenRouter as the primary app AI gateway. The direct Anthropic
demo in `CampusIQ_career/demo/campus_iq_test.py` is legacy/dev-only for now.

### Role-Based Model Routing

Model routing is centralized in `CampusIQ_career/ai/model_config.py` and can be
overridden with `CAMPUSIQ_MODEL_*` environment variables.

| Role | Purpose | Default model family |
|---------|---------|---------|
| orchestrator | Workflow orchestration | Gemini 2.5 Pro |
| career | FIT / GAP / SHIFT career analysis | DeepSeek R1 |
| academic | Academic analysis features | Qwen3 235B |
| parsing | JSON normalization and cleanup | Qwen3 32B |
| chat | Student chat responses | Gemini 2.5 Flash |
| report | Report synthesis | Gemini 2.5 Pro |

### Environment Variables

Required for the primary app AI path:

```bash
OPENROUTER_API_KEY=your-openrouter-key-here
```

Optional role overrides:

```bash
CAMPUSIQ_MODEL_ORCHESTRATOR=
CAMPUSIQ_MODEL_CAREER=
CAMPUSIQ_MODEL_ACADEMIC=
CAMPUSIQ_MODEL_PARSING=
CAMPUSIQ_MODEL_CHAT=
CAMPUSIQ_MODEL_REPORT=
```
