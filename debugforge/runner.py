import subprocess
from pathlib import Path

from .failure import TestFailure


def run_command(
    command: str,
    workspace: Path,
    timeout: int = 30
) -> TestFailure:

    try:
        result = subprocess.run(
            command,
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=True
        )

        return TestFailure(
            command=command,
            exit_code=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
            timed_out=False
        )

    except subprocess.TimeoutExpired as error:
        return TestFailure(
            command=command,
            exit_code=None,
            stdout=error.stdout or "",
            stderr=error.stderr or "",
            timed_out=True
        )