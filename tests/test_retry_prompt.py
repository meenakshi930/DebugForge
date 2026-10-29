from debugforge.retry_prompt import build_retry_prompt
from debugforge.attempt import RepairAttempt
from debugforge.failure import TestFailure


def test_retry_prompt():

    result = TestFailure(
        command="pytest",
        exit_code=1,
        stdout="",
        stderr="AssertionError",
        timed_out=False
    )

    evidence = {
        "status": "FAILED",
        "test_file": "test_app.py",
        "test_name": "test_discount",
        "error": "AssertionError",
        "expected": "3150",
        "actual": "3500"
    }

    previous_attempt = RepairAttempt(
        attempt_number=1,
        diagnosis="Incorrect discount calculation",
        file_path="app.py",
        old_code="return total - discount",
        new_code="return total - (total * discount)",
        test_status="FAILED",
        verified=False
    )

    prompt = build_retry_prompt(
        result=result,
        evidence=evidence,
        source_code="return total - (total * discount)",
        previous_attempt=previous_attempt
    )

    assert "PREVIOUS ATTEMPT:" in prompt
    assert "CURRENT TEST RESULT:" in prompt
    assert "Incorrect discount calculation" in prompt
    assert "Learn from the previous failed attempt" in prompt