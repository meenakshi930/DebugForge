import difflib


def generate_diff(
    file_path: str,
    old_code: str,
    new_code: str
) -> str:

    diff = difflib.unified_diff(
        old_code.splitlines(),
        new_code.splitlines(),
        fromfile=f"{file_path} (before)",
        tofile=f"{file_path} (after)",
        lineterm=""
    )

    return "\n".join(diff)