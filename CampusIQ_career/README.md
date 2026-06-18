# Campus IQ — Career Features

**Team 6 | Dallas AI Summer Program | SMU | July 2026**

---

## Overview

This folder contains the research foundation, mock data, prompt 
architecture, and working demo for the three career-side features 
of Campus IQ — an AI-powered longitudinal academic and career 
companion launching at Texas A&M University.

The career features answer three questions no current tool answers 
for students:

- **Where do I fit?** → Role Explorer (FIT)
- **What am I missing?** → Readiness Check (GAP)
- **What is changing?** → Trend-Aware Guidance (SHIFT)

---

## Folder Structure
Campus IQ/

├── mock_student_profiles/      # Five fictional A&M students
│   ├── tamu-001-base.json      # Jordan Mitchell — FIT primary
│   ├── tamu-002-gap.json       # Priya Nair — GAP primary
│   ├── tamu-003-shift.json     # Marcus Webb — SHIFT primary
│   ├── tamu-004-fit.json       # Alexis Garza — FIT primary
│   └── tamu-005-gap.json       # Derek Okonkwo — GAP primary
│
├── context_prompts/            # Prompt templates for each feature
│   ├── system_prompt.md        # Shared system prompt for all features
│   ├── fit_prompt.md           # Role Explorer prompt
│   ├── gap_prompt.md           # Readiness Check prompt
│   └── shift_prompt.md        # Trend-Aware Guidance prompt
│
└── demo/                       # Working demo script
|    └── campus_iq_test.py       # Runs any student through any feature
|     ├── demo_outputs/         # demo outputs using demo py script
|         └── tamu-001-FIT.md
|         └── tamu-002-GAP.md
|         └── tamu-003-SHIFT.md
|         └── tamu-004-FIT.md
|         └── tamu-005-GAP.md

---

## How the Demo Works

The demo script reads a student profile, automatically detects 
which feature to run based on the `primary_feature` field in the 
JSON, loads the matching prompt template, and calls the Claude API 
to generate a personalized career report.

**To run it:**

1. Add your Anthropic API key to `campus_iq_test.py`
2. Set `STUDENT_FILE` at the top of the script to the profile 
   you want to test
3. From the `demo` folder, run:

```bash
python campus_iq_test.py
```

**To swap students:** Change the `STUDENT_FILE` variable at the 
top of the script.

**To swap features:** Change the `primary_feature` field in the 
student JSON to `FIT`, `GAP`, or `SHIFT`.

---

## Student Profiles

Each profile is grounded in real Texas A&M enrollment and 
demographic data and designed to represent a realistic A&M 
undergraduate across college, major, year, internship status, 
and career clarity level.

Each profile includes a `primary_feature` field that tells the 
demo script which career feature to run for that student.

---

## Prompt Architecture

Three prompt templates map directly to the three career features:

| Template | Feature | What It Does |
|---|---|---|
| `fit_prompt.md` | Role Explorer | Surfaces 3-5 DFW-anchored career paths with fit reasoning |
| `gap_prompt.md` | Readiness Check | Compares student profile to real posting requirements |
| `shift_prompt.md` | Trend-Aware Guidance | Explains how target roles are evolving and what to learn |

All three share a common system prompt that establishes Campus 
IQ's identity, reasoning rules, tone, and hard constraints.

---

## Research Foundation

The prompt architecture and market context are grounded in:
- BLS OEWS DFW metro employment data
- Texas Workforce Commission 2022-2032 projections
- NACE Job Outlook 2026
- Strada Education Network research
- Handshake Class of 2026 data
- Stanford HAI 2026 AI Index
- Primary field research (two practitioner interviews)

Full research documentation is in `DFW_Market_Research_MVP_Analysis_v3`

---

## Next Steps

- [ ] Connect to live job market API (Lightcast or O*NET)
- [ ] Build front end UI for recruiter showcase
- [ ] Run all five profiles and save demo outputs
- [ ] Integrate with academic side student profile