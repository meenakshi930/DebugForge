from debugforge.failure import TestFailure


def test_failed_result():
    failure = TestFailure(
        command="pytest",
        exit_code=1,
        stdout="",
        stderr="AssertionError",
    )

    assert failure.failed is True
    assert failure.summary() == "Tests failed."


def test_successful_result():
    result = TestFailure(
        command="pytest",
        exit_code=0,
        stdout="1 passed",
        stderr="",
    )

    assert result.failed is False
    assert result.summary() == "Tests passed."