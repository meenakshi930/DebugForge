from pathlib import Path
import re

from .failure import TestFailure


def find_source_frame(
    result: TestFailure,
    workspace: Path,
    test_file: str | None = None
) -> dict | None:

    output = result.stdout + "\n" + result.stderr

    pattern = re.compile(
        r"([A-Za-z0-9_./\\-]+\.py):(\d+):\s+in\s+([A-Za-z_][A-Za-z0-9_]*)"
    )

    matches = pattern.findall(output)

    for file_path, line_number, function_name in matches:
        path = Path(file_path)

        if test_file and path.as_posix() == Path(test_file).as_posix():
            continue

        full_path = workspace / path

        if full_path.exists():
            return {
                "file_path": str(path),
                "line_number": int(line_number),
                "function_name": function_name
            }

    if not test_file:
        return None

    test_path = workspace / test_file

    if not test_path.exists():
        return None

    test_code = test_path.read_text(encoding="utf-8")

    from_import_match = re.search(
        r"from\s+([\w.]+)\s+import\s+([A-Za-z_][A-Za-z0-9_]*)",
        test_code
    )

    import_match = re.search(
        r"import\s+([A-Za-z_][A-Za-z0-9_]*)",
        test_code
    )

    if from_import_match:
        module_name = from_import_match.group(1)
        function_name = from_import_match.group(2)

    elif import_match:
        module_name = import_match.group(1)

        function_match = re.search(
            rf"{re.escape(module_name)}\.([A-Za-z_][A-Za-z0-9_]*)",
            test_code
        )

        if not function_match:
            return None

        function_name = function_match.group(1)

    else:
        return None

    module_path = workspace / Path(
        module_name.replace(".", "/") + ".py"
    )

    if not module_path.exists():
        return None

    return {
        "file_path": str(module_path.relative_to(workspace)),
        "line_number": None,
        "function_name": function_name
    }