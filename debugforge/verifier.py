
from pathlib import Path

from .runner import run_command


def verify_fix(
    workspace: Path,
    test_command: str
) -> dict:

    result = run_command(
        command=test_command,
        workspace=workspace
    )

    if result.failed:
        return {
            "verified": False,
            "status": "FAILED",
            "result": result
        }

    return {
        "verified": True,
        "status": "PASSED",
        "result": result
    }
