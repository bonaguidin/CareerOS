"""Career feature runners for Campus IQ."""

from .base import FeatureResult, FeatureRunner, FeatureStatus
from .fit import FitRunner
from .gap import GapRunner
from .orchestrator import run_career_analysis, run_feature
from .shift import ShiftRunner


RUNNERS = {
    "FIT": FitRunner,
    "GAP": GapRunner,
    "SHIFT": ShiftRunner,
}


def run_career_feature(feature_name, student_profile, client):
    normalized = feature_name.strip().upper()
    try:
        runner_class = RUNNERS[normalized]
    except KeyError as exc:
        supported = ", ".join(sorted(RUNNERS))
        raise ValueError(f"Unsupported career feature '{feature_name}'. Expected one of: {supported}.") from exc
    return runner_class(client=client).run(student_profile)


__all__ = [
    "FeatureResult",
    "FeatureRunner",
    "FeatureStatus",
    "FitRunner",
    "GapRunner",
    "ShiftRunner",
    "run_career_analysis",
    "run_career_feature",
    "run_feature",
]
