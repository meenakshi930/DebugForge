from debugforge.attempt import RepairAttempt
from debugforge.retry_prompt import build_retry_prompt
from debugforge.failure import TestFailure


def test_build_retry_prompt_contains_previous_attempt():
    result = TestFailure(
        command="pytest test_app.py",
        exit_code=1,
        stdout="",
        stderr="AssertionError: assert 6 == 5"
    )

    evidence = {
        "status": "FAILED",
        "test_file": "test_app.py",
        "test_name": "test_add",
        "error": "AssertionError",
        "expected": "5",
        "actual": "6"
    }

    previous_attempt = RepairAttempt(
        attempt_number=1,
        diagnosis="Addition function uses the wrong operator.",
        file_path="app.py",
        old_code="return a - b",
        new_code="return a * b",
        test_status="FAILED",
        verified=False
    )

    prompt = build_retry_prompt(
        result=result,
        evidence=evidence,
        source_code="""def add(a, b):
    return a * b
""",
        previous_attempt=previous_attempt
    )

    assert "Addition function uses the wrong operator." in prompt
    assert "return a - b" in prompt
    assert "return a * b" in prompt
    assert "AssertionError" in prompt
    assert "expected" in prompt.lower()
    assert "actual" in prompt.lower()
    assert "Make the smallest safe change possible." in prompt