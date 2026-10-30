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


def test_repair_once_verifies_successful_patch(tmp_path):
    app_file = tmp_path / "app.py"

    app_file.write_text(
        """def calculate_discount(total, discount):
    return total - (total * discount)
""",
        encoding="utf-8"
    )

    test_file = tmp_path / "test_app.py"

    test_file.write_text(
        """from app import calculate_discount


def test_calculate_discount():
    assert calculate_discount(1000, 10) == 900
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
        diagnosis="Discount percentage was not converted to decimal.",
        old_code="""def calculate_discount(total, discount):
    return total - (total * discount)
""",
        new_code="""def calculate_discount(total, discount):
    discount = discount / 100
    return total - (total * discount)
""",
        test_command="pytest test_app.py"
    )

    assert result["verified"] is True
    assert result["status"] == "PASSED"

    assert len(job.attempts.attempts) == 1
    assert job.attempts.last_attempt().verified is True
def test_repair_once_records_failed_attempt(tmp_path):
    app_file = tmp_path / "app.py"

    app_file.write_text(
        """def add(a, b):
    return a - b
""",
        encoding="utf-8"
    )

    test_file = tmp_path / "test_app.py"

    test_file.write_text(
        """from app import add


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
        diagnosis="Incorrect operator.",
        old_code="def add(a, b):\n    return a - b",
        new_code="def add(a, b):\n    return a * b",
        test_command="pytest test_app.py"
    )

    assert result["verified"] is False
    assert result["status"] == "FAILED"

    assert len(job.attempts.attempts) == 1
    assert job.attempts.last_attempt().verified is False
    assert job.attempts.last_attempt().test_status == "FAILED"

def test_repair_once_stops_after_max_attempts(tmp_path):
    app_file = tmp_path / "app.py"

    app_file.write_text(
        """def add(a, b):
    return a - b
""",
        encoding="utf-8"
    )

    job = Job(
        repo_path=str(tmp_path),
        command="pytest"
    )

    for _ in range(3):
        result = repair_once(
            job=job,
            workspace=tmp_path,
            file_path="app.py",
            diagnosis="Incorrect operator.",
            old_code="def add(a, b):\n    return a - b",
            new_code="def add(a, b):\n    return a * b",
            test_command="pytest"
        )

    result = repair_once(
        job=job,
        workspace=tmp_path,
        file_path="app.py",
        diagnosis="Another repair attempt.",
        old_code="def add(a, b):\n    return a - b",
        new_code="def add(a, b):\n    return a + b",
        test_command="pytest"
    )

    assert result["status"] == "MAX_ATTEMPTS_REACHED"
    assert result["verified"] is False
    assert len(job.attempts.attempts) == 3