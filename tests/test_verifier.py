
from debugforge.verifier import verify_fix


def test_verify_fix(tmp_path):
    test_file = tmp_path / "test_app.py"

    test_file.write_text(
        """
def test_addition():
    assert 2 + 2 == 4
""",
        encoding="utf-8"
    )

    result = verify_fix(
        workspace=tmp_path,
        test_command="pytest test_app.py"
    )

    assert result["verified"] is True
    assert result["status"] == "PASSED"