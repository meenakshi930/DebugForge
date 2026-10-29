from debugforge.repair_loop import repair_once


def test_repair_attempt_limit(tmp_path):

    workspace = tmp_path

    file_path = workspace / "app.py"

    file_path.write_text(
        "return 1",
        encoding="utf-8"
    )

    class FakeJob:
        def __init__(self):
            self.attempts = type(
                "Attempts",
                (),
                {
                    "attempts": [
                        object(),
                        object(),
                        object()
                    ]
                }
            )()

    job = FakeJob()

    result = repair_once(
        job=job,
        workspace=workspace,
        file_path="app.py",
        diagnosis="test",
        old_code="return 1",
        new_code="return 2",
        test_command="pytest"
    )

    assert result["status"] == "MAX_ATTEMPTS_REACHED"
    assert result["verified"] is False