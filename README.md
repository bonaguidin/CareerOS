# CareerOS — Campus IQ

AI-powered career and academic companion for Texas A&M students.
Dallas AI Group 6 | 2026 Summer Cohort.

---

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/) — Python package manager
- Node.js 20+ for the React/Vite frontend
- An [Anthropic API key](https://console.anthropic.com/) for the legacy demo
- An OpenRouter API key for the OpenRouter agent helper

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
is currently selected by the hardcoded `FEATURE` value in that same file.

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
record counts, career fields, and profile completeness gates used by the
dashboard and future prompt/UI code.

---

## Other commands

| Command                                      | What it does                          |
|----------------------------------------------|---------------------------------------|
| `uv run python data/scrape_catalog.py`       | Re-scrape the TAMU course catalog     |
| `uv run python data/build_catalog.py`        | Rebuild catalog JSON from scrape output |

## AI Architecture

Campus IQ is moving toward OpenRouter as the AI gateway. The current repo has
two explicit paths:

- `CampusIQ_career/ai_services.py`: OpenRouter preset helper.
- `CampusIQ_career/demo/campus_iq_test.py`: legacy direct-Anthropic demo.

These should be unified before production use.

### Agent Presets

| Agent | Purpose | Model |
|---------|---------|---------|
| career-os-orchestrator | Workflow orchestration | DeepSeek R1 |
| career-os-fit | Career fit analysis | Qwen3 235B |
| career-os-gap | Skill gap analysis | Qwen3 235B |
| career-os-shift | Trend analysis | DeepSeek R1 |
| career-os-academic | Academic analysis | Qwen3 235B |
| career-os-report | Report synthesis | Gemini Flash |
| career-os-parser | JSON normalization | Qwen3 32B |

### Environment Variables

- `ANTHROPIC_API_KEY`: required by the legacy direct-Anthropic demo.
- `OPENROUTER_API_KEY`: required by `CampusIQ_career/ai_services.py`.

Supabase is documented in the workflow architecture, but no Supabase client,
schema, or runtime path is implemented in the current code.
