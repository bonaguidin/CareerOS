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

---

## Other commands

| Command                                      | What it does                          |
|----------------------------------------------|---------------------------------------|
| `uv run python data/scrape_catalog.py`       | Re-scrape the TAMU course catalog     |
| `uv run python data/build_catalog.py`        | Rebuild catalog JSON from scrape output |
