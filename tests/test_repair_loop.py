from debugforge.attempt import AttemptHistory
from debugforge.job import Job
from debugforge.repair_loop import repair_once


def test_repair_once(tmp_path):

    app_file = tmp_path / "app.py"

    app_file.write_text(
        """
def add(a, b):
    return a - b
""",
        encoding="utf-8"
    )

    test_file = tmp_path / "test_app.py"

    test_file.write_text(
        """
from app import add


def test_add():
    assert add(2, 3) == 5
""",
        encoding="utf-8"
    )

    job = Job(
        repo_path=str(tmp_path),
        command="pytest test_app.py"
    )

    result = repair_once(
        job=job,
        workspace=tmp_path,
        file_path="app.py",
        diagnosis="Addition function uses subtraction.",
        old_code="def add(a, b):\n    return a - b",
        new_code="def add(a, b):\n    return a + b",
        test_command="pytest test_app.py"
    )

    assert result["verified"] is True
    assert result["status"] == "PASSED"

    assert len(job.attempts.attempts) == 1
    assert job.attempts.last_attempt().verified is True