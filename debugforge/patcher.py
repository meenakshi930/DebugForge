from pathlib import Path

from .patch_validator import validate_patch


def apply_patch(
    file_path: str,
    old_code: str,
    new_code: str
) -> bool:

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    content = path.read_text(encoding="utf-8")

    validation = validate_patch(
        source_code=content,
        old_code=old_code,
        new_code=new_code
    )

    if not validation["valid"]:
        return False

    updated_content = content.replace(
        old_code,
        new_code,
        1
    )

    path.write_text(
        updated_content,
        encoding="utf-8"
    )

    return True