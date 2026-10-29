from debugforge.job import Job
from debugforge.attempt import RepairAttempt


def test_job_tracks_attempts():

    job = Job(
        repo_path="demo_target",
        command="pytest demo_target/tests/test_app.py"
    )

    attempt = RepairAttempt(
        attempt_number=1,
        diagnosis="Discount calculation is incorrect.",
        file_path="demo_target/app.py",
        old_code="old",
        new_code="new",
        test_status="PASSED",
        verified=True
    )

    job.add_attempt(attempt)

    assert job.last_attempt() == attempt
    assert job.is_verified() is True