import re

from .failure import TestFailure


def parse_failure(result: TestFailure) -> dict:
    output = result.stdout + "\n" + result.stderr

    if not result.failed:
        return {
            "status": "PASSED",
            "test_file": None,
            "test_name": None,
            "error": None,
            "expected": None,
            "actual": None
        }

    test_file = None
    test_name = None
    error = None
    expected = None
    actual = None

    match = re.search(
        r"([\w\\/.-]+\.py):(\d+):\s+(\w+Error)",
        output
    )

    if match:
        test_file = match.group(1)
        error = match.group(3)

    match = re.search(
        r"([\w\\/.-]+\.py)::([\w_]+)",
        output
    )

    if match:
        test_file = match.group(1)
        test_name = match.group(2)

    match = re.search(
        r"assert\s+(.+?)\s+==\s+(.+)",
        output
    )

    if match:
        actual = match.group(1).strip()
        expected = match.group(2).strip()

    return {
        "status": "FAILED",
        "test_file": test_file,
        "test_name": test_name,
        "error": error,
        "expected": expected,
        "actual": actual
    }