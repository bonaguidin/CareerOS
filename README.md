# CareerOS — Campus IQ

AI-powered career and academic companion for Texas A&M students.
Dallas AI Group 6 | 2026 Summer Cohort.

---

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/) — Python package manager
- An [Anthropic API key](https://console.anthropic.com/)

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

Campus IQ uses OpenRouter as the AI gateway.

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

OPENROUTER_API_KEY (Created and Confirmed - Remove this note later) 
SUPABASE_URL (NEEDS CONFIRMATION)
SUPABASE_KEY (NEEDS CONFIRMATION)
