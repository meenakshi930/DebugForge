
import shutil
import tempfile
from pathlib import Path


def create_workspace(repo_path: str) -> Path:
    source = Path(repo_path).resolve()

    if not source.exists():
        raise FileNotFoundError(f"Repository not found: {repo_path}")

    if not source.is_dir():
        raise ValueError(f"Repository path is not a directory: {repo_path}")

    workspace = Path(
        tempfile.mkdtemp(prefix="debugforge_")
    )

    shutil.rmtree(workspace)

    shutil.copytree(
        source,
        workspace,
        ignore=shutil.ignore_patterns(
            ".git",
            ".venv",
            "venv",
            "__pycache__",
            ".pytest_cache"
        )
    )

    return workspace
