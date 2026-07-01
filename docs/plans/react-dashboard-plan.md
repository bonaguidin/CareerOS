# React + Vite Student Dashboard — Campus IQ
## Implementation Plan (pre-code review draft)

**Date:** 2026-06-22 · **Author:** Claude Code (Sonnet 4.6)  
**Status:** DRAFT — awaiting Deepak review before any code is written

---

## Audit Findings

### What was read
- All 5 student JSON files in `data/students/`
- `data/students/validate_students.py`
- `data/reference/unified_student_schema.md`
- `.env.example`
- `campusiq_workflow_diagram.md`
- `CampusIQ_career/demo/campus_iq_test.py`
- `CampusIQ_career/README.md`, `README.md`
- `pyproject.toml`

### Critical findings

**1. No Supabase exists yet.**  
The workflow diagram shows Supabase as the database layer, but `.env.example` contains only `ANTHROPIC_API_KEY`. There is no Supabase project, schema, or client code anywhere in the repo. Any data-layer recommendation must account for this gap.

**2. No Streamlit frontend exists.**  
The workflow diagram names "Streamlit (MVP)" for Layer 3, but no Streamlit code was written. The React dashboard described in this plan would be the **first** frontend of any kind.

**3. Data currently lives in 5 flat JSON files.**  
`data/students/student_*.json` are the authoritative student records. The Python demo reads them directly from disk. There is no database write path — updates to student data today require editing JSON files manually.

**4. `career.resume` block is documented but absent from all 5 student files.**  
`data/reference/unified_student_schema.md` describes a `career.resume` sub-object, but none of the actual JSON files contain it. The top-level career fields (`work_experience`, `projects`, etc.) serve as the canonical data. This inconsistency needs a resolution before the edit form is built. See Open Decisions #4.

**5. `onboarding_stage` appears in all 5 files (value: 3) but is not validated.**  
It is not covered by `validate_students.py` and is absent from `_schema_notes`. Treat as system-managed; do not expose it as user-editable.

**6. `student.major_intended` is categorized Canvas-derived but is logically onboarding-entered.**  
All freshman profiles have `major_intended` set (e.g., "Computer Engineering"), but freshmen at TAMU haven't formally declared. The value must have come from an onboarding step, not Canvas. The FIT feature gate also requires `major_intended`. This field is flagged as ambiguous. See Open Decisions #3.

---

## 1. Editability Map

This is the spine of the plan. Every field in the student record is marked below. The edit UI must never expose a READ-ONLY field as an input.

### Top-level structure

| Field | Source (per `_schema_notes`) | Editability | Notes |
|-------|------------------------------|-------------|-------|
| `_notes` | — | NOT SHOWN | Dev/meta only, not user-facing |
| `student` | `canvas_derived` | READ-ONLY | See sub-fields below |
| `onboarding_stage` | Not categorized | READ-ONLY | System-managed progress counter |
| `courses[]` | `canvas_derived` | READ-ONLY | Refreshed from Canvas |
| `enrollments[]` | `canvas_derived` | READ-ONLY | Grade/score state |
| `assignments[]` | `canvas_derived` | READ-ONLY | Assignment metadata |
| `submissions[]` | `canvas_derived` | READ-ONLY | Scores + professor comments |
| `examTopicTags{}` | `campus_iq_layer` | READ-ONLY | System-generated topic tags |
| `career` | `student_entered` | EDITABLE | See sub-fields below |
| `profile_completeness` | `ai_written` | READ-ONLY | System-calculated; display only |
| `_schema_notes` | — | NOT SHOWN | Dev/meta only |

### `student.*` sub-fields — all READ-ONLY

| Field | Read-only Reason |
|-------|-----------------|
| `student.id` | Canvas user ID |
| `student.name` | Canvas display name |
| `student.major_current` | Current Canvas enrollment record |
| `student.classification` | Year-in-school from Canvas |
| `student.institution` | Always "Texas A&M University" |
| `student.gpa_current` | Computed from Canvas enrollment data |
| `student.expected_graduation` | From Canvas registration |
| `student.major_intended` | **AMBIGUOUS** — see below |

> **`student.major_intended` flag:** Logically this is set during onboarding (a freshman entering what they plan to declare). However, `_schema_notes` categorizes the entire `student` block as `canvas_derived`. Making it editable in the dashboard would diverge from Canvas authority. Recommended resolution: treat it as an onboarding-only write (set once during onboarding, read-only after). The edit UI should not expose it. See Open Decisions #3.

### `career.*` sub-fields — all EDITABLE

| Field | UI Widget | Validation |
|-------|-----------|------------|
| `career.target_roles[]` | Tag/chip input | Non-empty list; each item non-empty string |
| `career.interests[]` | Tag/chip input | Non-empty list; each item non-empty string |
| `career.career_goals` | Textarea | Non-empty string |
| `career.geographic_preference` | Text input | Non-empty string |
| `career.ai_anxiety_level` | Text or dropdown | Non-empty string |
| `career.skills_self_reported.technical[]` | Tag input | Non-empty list |
| `career.skills_self_reported.soft[]` | Tag input | Non-empty list |
| `career.skills_self_reported.ai_exposure` | Textarea | Non-empty string |
| `career.certifications[]` | Repeatable form | Each entry: `name`, `issuer`, `status` required; `date` optional; list may be empty |
| `career.work_experience[]` | Repeatable form | Each entry: `employer`, `role`, `duration`, `location`, `description`, `skills_gained[]` required; list non-empty |
| `career.projects[]` | Repeatable form | Each entry: `name`, `timeframe`, `description`, `tools[]` required; list non-empty |

### `profile_completeness` — READ-ONLY, display only

| Field | Display |
|-------|---------|
| `profile_completeness.academic` | Progress indicator (0–1 → 0–100%) |
| `profile_completeness.career` | Progress indicator |
| `profile_completeness.overall` | Overall readiness pill |
| `profile_completeness.by_feature.FIT.ready` | Feature gate badge (green/grey) |
| `profile_completeness.by_feature.GAP.ready` | Feature gate badge |
| `profile_completeness.by_feature.SHIFT.ready` | Feature gate badge |

---

## 2. Auth — Two Options for the July 25 Demo

The demo context: 5 known students, controlled presentation environment, no real users.

### Option A — Real Supabase Auth

The app uses `@supabase/supabase-js` `signInWithPassword`. Each student has a row in `auth.users` seeded before the demo. Login redirects to the dashboard filtered to that student's row via RLS.

**Tradeoffs:**

| | |
|---|---|
| Build time | 2–3 days: Supabase project setup, schema migration, RLS policies, seed script, email invite or password pre-set for 5 demo accounts |
| Demo realism | High — looks like a real product login |
| Security | Appropriate — credentials never hardcoded |
| Post-demo carryover | High — auth infrastructure reusable when real students onboard |
| Risk | Supabase project misconfiguration or network issues on demo day could block the login screen entirely |

### Option B — Profile-select / Mock Login

A simple dropdown: "Select student →" shows the 5 names. Clicking "Enter Dashboard" sets a context value and renders the dashboard with that student's data loaded from a static JSON bundle. No real credential check. A `useAuth` hook provides the pattern so it can be swapped for real auth later.

**Tradeoffs:**

| | |
|---|---|
| Build time | 2–3 hours. No Supabase dependency at all. |
| Demo realism | Medium — panel judges understand it's a demo login. The dashboard experience is identical. |
| Security | Acceptable for a closed demo with no real PII |
| Post-demo carryover | Medium — the auth hook pattern carries over; the selector itself is replaced. Static JSON must be migrated to Supabase before real users can be added. |
| Risk | Near-zero. No external dependency on demo day. |

**Recommendation: Option B for July 25.** The demo's value is in the dashboard experience and AI feature outputs — not in the login screen. Spending 2+ days on Supabase auth for 5 pre-selected mock profiles is poor ROI at this stage. If Supabase is also needed for the AI feature data layer (it likely is), set up the Supabase project after the dashboard is working and migrate then. This is an open decision; surface it to the team.

---

## 3. Project Structure

### Recommendation: `frontend/` subdirectory inside the CareerOS monorepo

```
CareerOS/                         ← existing Python repo root
├── CampusIQ_career/              ← existing Python demo
├── data/                         ← existing data layer
├── docs/
│   └── plans/
│       └── react-dashboard-plan.md
├── frontend/                     ← NEW: Vite + React app
│   ├── public/
│   │   └── data/                 ← Option B: copy of the 5 student JSONs (demo only)
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── auth/
│   │   ├── components/
│   │   ├── data/
│   │   ├── hooks/
│   │   ├── pages/
│   │   └── types/
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── .env.example                  ← add VITE_SUPABASE_URL + VITE_SUPABASE_ANON_KEY when ready
├── pyproject.toml
└── README.md
```

**Why this structure, not a true monorepo (Turborepo/nx)?** The Python backend and React frontend share no code. A workspace tool adds overhead with zero benefit at this scale. A single `frontend/` directory in the same git repo gives colocation (one `git clone`, one PR), lets Python scripts and the React app both see `data/students/` at known relative paths, and is the simplest layout for a team that has never shipped a frontend yet.

---

## 4. Data Access Layer

### Phase 1 (Demo — static JSON, no Supabase)

Student records are copied into `frontend/public/data/` at build time. The React app fetches them at `/data/student_jordanReyes.json` etc. (or imports them as static TS modules). Writes update React state in-session only; nothing persists. This is acceptable because the demo is a live walkthrough with 5 known profiles.

```ts
// Example: fetch by student name/ID selected at login
const res = await fetch(`/data/student_${slug}.json`);
const profile: StudentProfile = await res.json();
```

A `src/types/student.ts` file defines TypeScript interfaces that mirror the JSON schema exactly. This is the contract — changes to the student JSON schema require updating these types.

### Phase 2 (Post-demo — Supabase)

- Set up a Supabase project; add `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY` to `.env.example`
- Store each student's unified record as a JSONB column in a `students` table, keyed by `student.id`
- Enable RLS: students can read and update only rows matching their auth UID
- The `updateCareer()` function sends only the `career` object as a PATCH, not the full record, to avoid overwriting Canvas-derived fields with stale data:

```ts
await supabase
  .from('students')
  .update({ career: updatedCareer })
  .eq('id', studentId);
```

Writes must never touch `student`, `courses`, `enrollments`, `assignments`, `submissions`, `examTopicTags`, or `profile_completeness` columns — those are refreshed by the Python Canvas pull script.

### How this mirrors the existing Python update pattern

`campus_iq_test.py` reads the full JSON, uses it as context, and does not write back. There is no existing "update script" in the repo yet — the workflow diagram describes one (`Python · update script / overwrites changed fields only`), but it hasn't been built. The React save logic will be the first write path, and it should be written with the same field boundary the schema doc defines: only `career.*` is writable by the student.

---

## 5. Component Architecture

All components are read-only displays unless noted as EDITABLE.

```
<App>
└── <Router>
    ├── /             → <LoginPage>           (mock selector or Supabase auth form)
    └── /dashboard    → <DashboardPage>       (requires auth)
        ├── <ProfileHeader>                   READ-ONLY: name, major, classification, GPA pill
        ├── <CompletenessGate>                READ-ONLY: by_feature badges (FIT/GAP/SHIFT ready?)
        ├── <AcademicSnapshot>                READ-ONLY section
        │   ├── <CourseGradeTable>            enrollments joined with courses — grade per course
        │   ├── <ProfessorCommentList>        submissions[].submission_comments (grouped by course)
        │   └── <ExamTopicBreakdown>          examTopicTags — score per topic (read-only)
        └── <CareerPanel>                     EDITABLE section
            ├── <CareerSummaryRow>            career_goals, geographic_preference (inline edit)
            ├── <TargetRolesEditor>           tag chips — add/remove strings
            ├── <InterestsEditor>             tag chips — add/remove strings
            ├── <SkillsEditor>               technical[], soft[], ai_exposure
            ├── <ExperienceList>             work_experience items + [Add / Edit / Remove]
            ├── <ProjectsList>              projects items + [Add / Edit / Remove]
            └── <CertificationsList>        certifications items (may be empty) + [Add / Edit / Remove]
```

**Edit interaction pattern:** Inline edit with a Save/Cancel button pair per section. Avoid a single "Edit everything" modal — it overwhelms a freshman with 10+ fields at once. Each section (`<CareerSummaryRow>`, `<SkillsEditor>`, etc.) independently enters and exits edit mode. This also keeps save granular: a failed save in one section doesn't discard changes in another.

**`<CompletenessGate>` logic:**
```
profile_completeness.by_feature.FIT.ready   → show FIT badge as green / grey
profile_completeness.by_feature.GAP.ready   → show GAP badge
profile_completeness.by_feature.SHIFT.ready → show SHIFT badge
```
These badges are informational for now ("AI features become available here"). They do not trigger any AI calls in this plan scope.

---

## 6. Routing and State Management

### Routing: React Router v6

Two routes only:
- `/` — `<LoginPage>`
- `/dashboard` — `<DashboardPage>`, guarded by `<RequireAuth>`

`<RequireAuth>` checks a `useAuth()` hook. In Phase 1 it reads from React Context (set at mock login). In Phase 2 it reads from `supabase.auth.getSession()`. The hook interface is the same in both phases; only the implementation changes.

No additional client-side routing is needed for this plan scope. Do not add nested routes until AI feature output pages are designed.

### State management: React Context + `useState`

No Redux, no Zustand, no Jotai. The student record is a single object loaded at login and passed through context. Edit forms use local `useState`. On save, the context value is updated (Phase 1: in-memory; Phase 2: after a confirmed Supabase write). This is sufficient for one student viewing their own record.

**If the AI feature output pages are added later,** the state needs may grow. Re-evaluate then. Don't add a state library now for hypothetical future needs.

---

## 7. Validation

### Client-side validation (form layer)

Each editable section runs a lightweight JS validator on save that mirrors `validate_students.py`. Required-field checks can be written as a single `validateCareer(career: CareerBlock): string[]` function that returns human-readable error messages. This function should live in `src/data/validateCareer.ts` and be importable in tests.

Minimum checks to port from Python:
- `target_roles`: non-empty array, all strings non-empty
- `interests`: non-empty array, all strings non-empty
- `career_goals`, `geographic_preference`, `ai_anxiety_level`: non-empty string
- `skills_self_reported.technical[]`, `skills_self_reported.soft[]`: non-empty arrays
- `skills_self_reported.ai_exposure`: non-empty string
- `work_experience[]`: each entry has `employer`, `role`, `duration`, `location`, `description`, `skills_gained[]`
- `projects[]`: each entry has `name`, `timeframe`, `description`, `tools[]`
- `certifications[]`: may be empty; if not empty, each entry has `name`, `issuer`, `status`

### Schema-level validation (CI gate)

The canonical Python validator (`data/students/validate_students.py`) remains the ground truth. Any changes to the student JSON files (including those exported/migrated from Supabase) should still pass `uv run python data/students/validate_students.py`. This can be run as a CI step if GitHub Actions is added.

The React validator does NOT replace the Python validator — it supplements it at the UI boundary to give the student immediate feedback before a save is attempted.

---

## 8. Out of Scope (Explicit)

The following are **not** part of this plan and must not be designed for or scaffolded during the dashboard build:

- Rendering of AI feature outputs: FIT Role Explorer results, GAP Readiness Check results, SHIFT Trend-Aware Guidance results
- Professor Comment Analyzer results display
- Exam Gap Analysis results display
- Study Guide Generator
- Course and Cert Recommender outputs
- PDF / DOCX export
- Resume upload and parser integration
- Live job market API (Lightcast, O*NET)
- Multi-student admin view

These are deferred until (a) the AI engine output format is locked and (b) the view/edit dashboard is shipped and stable. The completeness badges in `<CompletenessGate>` serve as placeholders indicating where these features will attach.

---

## 9. Dependency List and Phased Build Order

### Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `vite` | ^6.x | Build tool |
| `react` | ^19.x | UI library |
| `react-dom` | ^19.x | DOM renderer |
| `typescript` | ^5.x | Type safety |
| `react-router-dom` | ^6.x | Client routing (2 routes) |
| `@supabase/supabase-js` | ^2.x | Database client (Phase 2 only; can be added later) |
| CSS framework | **OPEN DECISION #2** | See below |

No testing library is listed — the Python validator is the contract check. Add `vitest` + `@testing-library/react` if unit tests for `validateCareer.ts` are wanted, but that is optional for the demo.

### Phased build order

#### Phase 1 — Static shell (2–3 days)
1. Scaffold `frontend/` with `npm create vite@latest` → React + TypeScript template
2. Define `src/types/student.ts` — TypeScript interfaces matching the JSON schema
3. Copy 5 JSON files to `frontend/public/data/`
4. Build `<LoginPage>` with mock profile selector; store selection in React Context
5. Build `<DashboardPage>` skeleton with `<ProfileHeader>` and `<AcademicSnapshot>` (read-only)
6. Render `<CompletenessGate>` badges from `profile_completeness.by_feature`
7. Add `<CareerPanel>` in read-only display mode

#### Phase 2 — Edit forms (2–3 days)
8. Implement `validateCareer.ts`
9. Add inline edit mode to `<CareerSummaryRow>` and `<SkillsEditor>`
10. Add repeatable-form edit to `<ExperienceList>`, `<ProjectsList>`, `<CertificationsList>`
11. Wire save: Phase 1 → update React Context; Phase 2 → Supabase PATCH

#### Phase 3 — Supabase migration (2–3 days, post-demo or before demo if time allows)
12. Set up Supabase project; run schema migration (single `students` JSONB table)
13. Swap static JSON fetch for Supabase client reads
14. Add Supabase Auth if Option A is chosen
15. Add RLS policy: `student.id = auth.uid()`
16. Seed 5 demo student records from the existing JSON files

---

## Open Decisions for Deepak

These are unresolved choices this plan cannot make unilaterally. Each needs an answer before the corresponding phase begins.

1. **Auth approach for July 25:** Mock profile-selector login (Option B, recommended) or real Supabase Auth (Option A)? Option B is faster and lower-risk for the demo; Option A has better post-demo carryover. Which matters more for the July deadline?

2. **CSS framework:** Tailwind CSS + shadcn/ui (fast component library, requires setup), plain CSS modules (zero config, more hand-rolling), or something else? Tailwind is recommended for speed; shadcn/ui gives usable form inputs, tags, and badges without designing from scratch.

3. **Is `student.major_intended` student-editable or read-only?** It's categorized as Canvas-derived in `_schema_notes`, but freshmen enter it during onboarding, not Canvas. Should the dashboard let students update it (e.g., they change their mind from Computer Engineering to Electrical Engineering)? If yes, it needs to move to the editable career block or get its own edit path — and the validator needs updating.

4. **What should happen with `career.resume`?** The schema doc defines a nested `career.resume` block, but all 5 student files omit it. Should the dashboard populate it as a parallel write whenever `career.work_experience/projects/certifications` are saved? Or is the `resume` block deprecated in favor of the top-level career mirrors? This needs resolution before the save function is written.

5. **Inline edit vs modal edit:** This plan recommends inline per-section edit. If a full-page edit form is preferred (single "Edit Profile" button → form view → save → return to dashboard), that changes the component layout significantly. Confirm before building `<CareerPanel>`.

6. **Is Supabase being set up before the demo?** If yes, Phase 3 should run in parallel with Phase 2. If no, the demo runs entirely on static JSON and Supabase migration happens after July 25. This affects whether `@supabase/supabase-js` is installed now or later.

7. **Client-only validation or server-side check?** This plan proposes JS-only validation in the browser. An alternative is a small Python FastAPI endpoint that runs `validate_students.py` logic on the submitted JSON before writing to Supabase. Recommended default: client-only for the demo, server-side validation before any real student data goes live.
