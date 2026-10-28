from pathlib import Path


def read_file(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not path.is_file():
        raise ValueError(f"Not a file: {file_path}")

    return path.read_text(encoding="utf-8")


def read_file_with_lines(file_path: str) -> list[str]:
    content = read_file(file_path)

    return [
        f"{index}: {line}"
        for index, line in enumerate(content.splitlines(), start=1)
    ]