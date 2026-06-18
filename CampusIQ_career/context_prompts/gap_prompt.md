FEATURE: Readiness Check (GAP)
PURPOSE: Compare the student's current profile against actual
DFW employer requirements for their target role, distinguish
must-have from nice-to-have gaps, and generate a specific,
actionable readiness plan.

---

STUDENT PROFILE:
{insert student JSON here}

---

MARKET CONTEXT:
DFW employers are actively posting for roles requiring:
SQL, Python, Salesforce, Power BI, Tableau, ERP systems,
data visualization, and process documentation.
85% of employers now use skills-based hiring.
76% use skills assessments as part of the hiring process.
GPA without experience ranks last as a hiring signal.
Internship completion reduces underemployment odds by 48.5%.
Intern-to-hire conversion reached 63.1% in 2024-25 —
highest in five years.

---

INSTRUCTIONS:
Using the student profile and market context above, generate a
Readiness Check report with the following structure:

1. TARGET ROLE SUMMARY
   - Restate the student's target role(s) from their profile.
   - Briefly describe what DFW employers actually require for
     this role at the entry level — skills, experience, tools.
   - Note the student's graduation timeline and how urgency
     affects the plan.

2. READINESS SCORE
   - Rate overall readiness: NOT READY / PARTIALLY READY /
     COMPETITIVE — with a 1-2 sentence rationale.
   - Do not use a numerical score. Use the three-tier rating only.

3. GAP ANALYSIS
   MUST-HAVE GAPS (blocking):
   - List specific skills, tools, or experiences that appear
     in the majority of DFW postings for this role and are
     absent from the student's profile.
   - For each: name the gap, why it is blocking, and what
     closing it looks like concretely.

   NICE-TO-HAVE GAPS (differentiating):
   - List skills or experiences that appear in postings but
     are not universally required.
   - For each: name the gap and note that closing it
     strengthens competitiveness but is not blocking.

4. ACTION PLAN
   For each must-have gap, provide ONE specific next step:
   - A named course (e.g. "MIS 3300 at Texas A&M") OR
   - A specific project type (e.g. "build a Power BI dashboard
     using public DFW labor data") OR
   - A specific certification (e.g. "Google Data Analytics
     Certificate on Coursera") OR
   - A specific experience type (e.g. "target a summer
     operations internship at a logistics or supply chain firm")

5. TIMELINE FLAG
   - If the student is a senior or December grad, flag urgency
     explicitly and front-load the action plan accordingly.
   - Note any employer recruiting cycle deadlines relevant
     to the target role.

---

CONSTRAINTS:
- Only identify gaps relative to the student's stated target
  role. Do not assess readiness for roles they did not name.
- Every gap must be tied to evidence in the student profile
  and the market context — no generic gap lists.
- Every action step must be specific and executable.
  "Improve your SQL skills" is not acceptable output.
  "Complete the SQL for Data Analysis course on Coursera
  and build one query-based project" is acceptable.
- Do not fabricate posting data or employer requirements.
  Use only the market context provided.