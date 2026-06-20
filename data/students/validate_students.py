#!/usr/bin/env python3
"""
Validates all 5 student JSON files: parses valid JSON, checks the
unified student profile contract, and verifies expected record counts.
"""

import json
import sys
import os

STUDENTS_DIR = os.path.dirname(os.path.abspath(__file__))

REQUIRED_KEYS = {
    "student",
    "courses",
    "enrollments",
    "assignments",
    "submissions",
    "career",
    "profile_completeness",
    "examTopicTags",
}

REQUIRED_STUDENT_KEYS = {
    "id",
    "name",
    "major",
    "classification",
    "institution",
    "gpa_current",
}

REQUIRED_CAREER_KEYS = {
    "target_roles",
    "interests",
    "career_goals",
    "geographic_preference",
    "ai_anxiety_level",
    "skills_self_reported",
    "certifications",
    "work_experience",
    "projects",
    "resume",
}

REQUIRED_RESUME_KEYS = {"skills", "work_experience", "projects", "certifications"}
REQUIRED_SKILL_KEYS = {"technical", "soft", "ai_exposure"}
REQUIRED_COMPLETENESS_KEYS = {"academic", "career", "overall"}

EXPECTED = {
    "student_jordanReyes.json":  {"courses": 5, "enrollments": 5, "assignments": 12, "submissions": 10},
    "student_priyaNair.json":    {"courses": 6, "enrollments": 6, "assignments": 19, "submissions": 14},
    "student_ethanBrooks.json":  {"courses": 6, "enrollments": 6, "assignments": 24, "submissions": 17},
    "student_marcusWebb.json":   {"courses": 4, "enrollments": 4, "assignments": 9,  "submissions": 8},
    "student_sofiaRamirez.json": {"courses": 5, "enrollments": 5, "assignments": 17, "submissions": 12},
}

errors = []


def is_non_empty_string(value):
    return isinstance(value, str) and bool(value.strip())


def validate_string_list(value, field_name, issues, allow_empty=False):
    if not isinstance(value, list):
        issues.append(f"{field_name}: expected list")
        return
    if not allow_empty and not value:
        issues.append(f"{field_name}: expected non-empty list")
        return
    bad_items = [item for item in value if not is_non_empty_string(item)]
    if bad_items:
        issues.append(f"{field_name}: all items must be non-empty strings")


def validate_resume_items(items, required_fields, field_name, issues, allow_empty=False):
    if not isinstance(items, list):
        issues.append(f"{field_name}: expected list")
        return
    if not allow_empty and not items:
        issues.append(f"{field_name}: expected non-empty list")
        return
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            issues.append(f"{field_name}[{index}]: expected object")
            continue
        missing = required_fields - set(item.keys())
        if missing:
            issues.append(f"{field_name}[{index}]: missing keys {sorted(missing)}")


def validate_unified_profile(data, issues):
    student = data.get("student")
    if not isinstance(student, dict):
        issues.append("student: expected object")
    else:
        missing_student = REQUIRED_STUDENT_KEYS - set(student.keys())
        if missing_student:
            issues.append(f"student: missing keys {sorted(missing_student)}")
        if not isinstance(student.get("id"), int):
            issues.append("student.id: expected integer")
        for key in ["name", "major", "classification", "institution"]:
            if not is_non_empty_string(student.get(key)):
                issues.append(f"student.{key}: expected non-empty string")
        if not isinstance(student.get("gpa_current"), (int, float)):
            issues.append("student.gpa_current: expected number")

    career = data.get("career")
    if not isinstance(career, dict):
        issues.append("career: expected object")
        return

    missing_career = REQUIRED_CAREER_KEYS - set(career.keys())
    if missing_career:
        issues.append(f"career: missing keys {sorted(missing_career)}")

    validate_string_list(career.get("target_roles"), "career.target_roles", issues)
    validate_string_list(career.get("interests"), "career.interests", issues)
    for key in ["career_goals", "geographic_preference", "ai_anxiety_level"]:
        if not is_non_empty_string(career.get(key)):
            issues.append(f"career.{key}: expected non-empty string")

    resume = career.get("resume")
    if not isinstance(resume, dict):
        issues.append("career.resume: expected object")
        return

    missing_resume = REQUIRED_RESUME_KEYS - set(resume.keys())
    if missing_resume:
        issues.append(f"career.resume: missing keys {sorted(missing_resume)}")

    skills = resume.get("skills")
    if not isinstance(skills, dict):
        issues.append("career.resume.skills: expected object")
    else:
        missing_skills = REQUIRED_SKILL_KEYS - set(skills.keys())
        if missing_skills:
            issues.append(f"career.resume.skills: missing keys {sorted(missing_skills)}")
        validate_string_list(skills.get("technical"), "career.resume.skills.technical", issues)
        validate_string_list(skills.get("soft"), "career.resume.skills.soft", issues)
        if not is_non_empty_string(skills.get("ai_exposure")):
            issues.append("career.resume.skills.ai_exposure: expected non-empty string")

    if career.get("skills_self_reported") != resume.get("skills"):
        issues.append("career.skills_self_reported must mirror career.resume.skills")
    if career.get("work_experience") != resume.get("work_experience"):
        issues.append("career.work_experience must mirror career.resume.work_experience")
    if career.get("projects") != resume.get("projects"):
        issues.append("career.projects must mirror career.resume.projects")
    if career.get("certifications") != resume.get("certifications"):
        issues.append("career.certifications must mirror career.resume.certifications")

    validate_resume_items(
        resume.get("work_experience"),
        {"employer", "role", "duration", "location", "description", "skills_gained"},
        "career.resume.work_experience",
        issues,
    )
    validate_resume_items(
        resume.get("projects"),
        {"name", "timeframe", "description", "tools"},
        "career.resume.projects",
        issues,
    )
    validate_resume_items(
        resume.get("certifications"),
        {"name", "issuer", "status"},
        "career.resume.certifications",
        issues,
        allow_empty=True,
    )

    completeness = data.get("profile_completeness")
    if not isinstance(completeness, dict):
        issues.append("profile_completeness: expected object")
    else:
        missing_completeness = REQUIRED_COMPLETENESS_KEYS - set(completeness.keys())
        if missing_completeness:
            issues.append(f"profile_completeness: missing keys {sorted(missing_completeness)}")
        for key in REQUIRED_COMPLETENESS_KEYS:
            value = completeness.get(key)
            if not isinstance(value, (int, float)) or value < 0 or value > 1:
                issues.append(f"profile_completeness.{key}: expected number from 0 to 1")

print(f"{'File':<30} {'Keys':>5}  {'Courses':>7}  {'Enroll':>6}  {'Assign':>6}  {'Subs':>5}  Status")
print("-" * 80)

for fname, expected_counts in sorted(EXPECTED.items()):
    path = os.path.join(STUDENTS_DIR, fname)

    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"{fname:<30}  FILE NOT FOUND")
        errors.append(f"{fname}: file not found")
        continue
    except json.JSONDecodeError as e:
        print(f"{fname:<30}  INVALID JSON: {e}")
        errors.append(f"{fname}: invalid JSON")
        continue

    missing_keys = REQUIRED_KEYS - set(data.keys())
    has_notes = "_notes" in data

    actual = {
        "courses":     len(data.get("courses", [])),
        "enrollments": len(data.get("enrollments", [])),
        "assignments": len(data.get("assignments", [])),
        "submissions": len(data.get("submissions", [])),
    }

    count_ok = all(actual[k] == expected_counts[k] for k in expected_counts)
    keys_ok = len(missing_keys) == 0

    issues = []
    if missing_keys:
        issues.append(f"missing keys: {missing_keys}")
    for k, v in expected_counts.items():
        if actual[k] != v:
            issues.append(f"{k}: expected {v} got {actual[k]}")
    validate_unified_profile(data, issues)

    status = "OK" + (" +_notes" if has_notes else "") if not issues else "FAIL: " + "; ".join(issues)

    print(
        f"{fname:<30} {len(REQUIRED_KEYS - missing_keys):>5}  "
        f"{actual['courses']:>7}  {actual['enrollments']:>6}  "
        f"{actual['assignments']:>6}  {actual['submissions']:>5}  {status}"
    )
    if issues:
        errors.extend([f"{fname}: {i}" for i in issues])

print("-" * 80)
print()
if errors:
    print(f"RESULT: FAILED ({len(errors)} error(s))")
    for e in errors:
        print(f"  {e}")
    sys.exit(1)
else:
    print("RESULT: All 5 student JSON files valid.")
