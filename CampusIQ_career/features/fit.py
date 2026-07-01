"""FIT career feature runner."""

from typing import Any, Mapping

from .base import CareerFeatureRunner


class FitRunner(CareerFeatureRunner):
    feature = "FIT"
    prompt_filename = "campus_iq_prompt_FIT.md"
    required_paths = (
        "student.major_intended",
        "career.target_roles",
        "career.interests",
        "career.skills_self_reported",
    )
    output_contract: Mapping[str, Any] = {
        "role_matches": [
            {
                "role": "string",
                "fit_level": "high|medium|low",
                "rationale": "string",
                "supporting_signals": [],
                "missing_signals": [],
            }
        ],
        "overall_fit_summary": "string",
    }

    def build_student_context(self, student_profile):
        student = student_profile.get("student", {})
        career = student_profile.get("career", {})
        return {
            "major_current": student.get("major_current") or student.get("major"),
            "major_intended": student.get("major_intended") or student.get("major"),
            "classification": student.get("classification"),
            "target_roles": career.get("target_roles", []),
            "interests": career.get("interests", []),
            "career_goals": career.get("career_goals", ""),
            "geographic_preference": career.get("geographic_preference", ""),
            "skills_self_reported": career.get("skills_self_reported", {}),
            "work_experience": career.get("work_experience", []),
            "projects": career.get("projects", []),
        }

    def default_summary(self, data):
        return data.get("overall_fit_summary", "FIT analysis completed.")
