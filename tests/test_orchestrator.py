from pathlib import Path

from debugforge.orchestrator import debug_repository


def test_orchestrator_reaches_repair(monkeypatch, tmp_path):

    repo = tmp_path / "repo"
    repo.mkdir()

    app_file = repo / "app.py"

    app_file.write_text(
        """
def calculate_discount(total, discount):
    return total - (total * discount)
""",
        encoding="utf-8"
    )

    test_file = repo / "test_app.py"

    test_file.write_text(
        """
from app import calculate_discount


def test_discount():
    assert calculate_discount(3500, 10) == 3150
""",
        encoding="utf-8"
    )

    fake_repair = """
DIAGNOSIS:
Discount is treated as 10 instead of 10%.

FILE:
app.py

OLD_CODE:
return total - (total * discount)

NEW_CODE:
return total - (total * (discount / 100))
"""

    def fake_generate_repair(prompt):
        assert "def calculate_discount" in prompt
        assert "return total - (total * discount)" in prompt

        from debugforge.repair_parser import parse_repair_response

        return parse_repair_response(fake_repair)

    monkeypatch.setattr(
        "debugforge.orchestrator.generate_repair",
        fake_generate_repair
    )

    result = debug_repository(
        repo_path=str(repo),
        test_command="pytest"
    )

    assert result["status"] == "VERIFIED"
    assert result["repair_result"]["verified"] is True
    assert "source_file" in result["evidence"]
    assert "source_line" in result["evidence"]
    assert "source_function" in result["evidence"]

    repair = result["repair"]

    assert repair.file_path == "app.py"

    assert repair.old_code == (
        "return total - (total * discount)"
    )

    assert repair.new_code == (
        "return total - (total * (discount / 100))"
    )


def test_orchestrator_retries_failed_repair(monkeypatch, tmp_path):

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

    responses = [
        """DIAGNOSIS:
The function uses multiplication instead of addition.

FILE:
app.py

OLD_CODE:
def add(a, b):
    return a - b

NEW_CODE:
def add(a, b):
    return a * b
""",
        """DIAGNOSIS:
The previous repair used multiplication. The function should use addition.

FILE:
app.py

OLD_CODE:
def add(a, b):
    return a * b

NEW_CODE:
def add(a, b):
    return a + b
"""
    ]

    def fake_generate_repair(prompt):

        response = responses.pop(0)

        from debugforge.repair_parser import parse_repair_response

        return parse_repair_response(response)

    monkeypatch.setattr(
        "debugforge.orchestrator.generate_repair",
        fake_generate_repair
    )

    result = debug_repository(
        repo_path=str(tmp_path),
        test_command="pytest test_app.py"
    )

    assert result["status"] == "VERIFIED"

    assert len(result["job"].attempts.attempts) == 2

    assert result["job"].attempts.attempts[0].verified is False
    assert result["job"].attempts.attempts[1].verified is True

    final_code = (
        Path(result["workspace"]) / "app.py"
    ).read_text(encoding="utf-8")

    assert "return a + b" in final_code