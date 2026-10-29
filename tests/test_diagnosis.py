from debugforge.failure import TestFailure
from debugforge.diagnosis import build_diagnosis_prompt


def test_build_diagnosis_prompt():
    result = TestFailure(
        command="pytest",
        exit_code=1,
        stdout="",
        stderr="AssertionError"
    )

    evidence = {
        "status": "FAILED",
        "test_file": "demo_target/tests/test_app.py",
        "test_name": "test_checkout_with_discount",
        "error": "AssertionError",
        "expected": "315.0",
        "actual": "-3150"
    }

    source_code = """
def apply_discount(total, discount):
    return total - (total * discount)
"""

    prompt = build_diagnosis_prompt(
        result,
        evidence,
        source_code
    )

    assert "315.0" in prompt
    assert "-3150" in prompt
    assert "apply_discount" in prompt