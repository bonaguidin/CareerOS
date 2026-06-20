#!/usr/bin/env python3
"""
Validates all 5 student JSON files: parses as valid JSON, checks
required top-level keys, and verifies expected record counts.
"""

import json
import sys
import os

STUDENTS_DIR = os.path.dirname(os.path.abspath(__file__))

REQUIRED_KEYS = {"student", "courses", "enrollments", "assignments", "submissions", "examTopicTags"}

EXPECTED = {
    "student_jordanReyes.json":  {"courses": 5, "enrollments": 5, "assignments": 12, "submissions": 10},
    "student_priyaNair.json":    {"courses": 6, "enrollments": 6, "assignments": 19, "submissions": 14},
    "student_ethanBrooks.json":  {"courses": 6, "enrollments": 6, "assignments": 24, "submissions": 17},
    "student_marcusWebb.json":   {"courses": 4, "enrollments": 4, "assignments": 9,  "submissions": 8},
    "student_sofiaRamirez.json": {"courses": 5, "enrollments": 5, "assignments": 17, "submissions": 12},
}

errors = []

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
