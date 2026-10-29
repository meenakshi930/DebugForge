from debugforge.attempt import RepairAttempt, AttemptHistory


def test_attempt_history():
    history = AttemptHistory()

    attempt = RepairAttempt(
        attempt_number=1,
        diagnosis="Discount is treated as a multiplier.",
        file_path="demo_target/app.py",
        old_code="return total - (total * discount)",
        new_code="return total - (total * (discount / 100))",
        test_status="PASSED",
        verified=True
    )

    history.add_attempt(attempt)

    assert len(history.attempts) == 1
    assert history.last_attempt() == attempt
    assert history.successful() is True