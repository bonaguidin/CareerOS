import importlib.util
from pathlib import Path


def test_campus_iq_demo_import_has_no_side_effects():
    demo_path = Path(__file__).resolve().parents[1] / "CampusIQ_career" / "demo" / "campus_iq_test.py"
    spec = importlib.util.spec_from_file_location("campus_iq_test", demo_path)
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert module.FEATURE == "gap"
    assert callable(module.run_legacy_anthropic_demo)
