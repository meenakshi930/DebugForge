from debugforge.orchestrator import debug_repository


def test_real_repair(monkeypatch, tmp_path):

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

    assert len(result["job"].attempts.attempts) == 1

    attempt = result["job"].attempts.last_attempt()

    assert attempt.verified is True