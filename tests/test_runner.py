from pathlib import Path

from debugforge.runner import run_command


def test_run_command():
    workspace = Path("demo_target")

    result = run_command(
        command="python app.py",
        workspace=workspace
    )

    assert result.exit_code == 0
    assert result.failed is False
    assert "Final total: -3150" in result.stdout