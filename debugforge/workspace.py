import shutil
import tempfile
from pathlib import Path


def create_workspace(repo_path: str) -> Path:
    source = Path(repo_path)

    if not source.exists():
        raise FileNotFoundError(f"Repository not found: {repo_path}")

    if not source.is_dir():
        raise ValueError(f"Repository path is not a directory: {repo_path}")

    temp_dir = Path(tempfile.mkdtemp(prefix="bugpilot_"))
    workspace = temp_dir / source.name

    shutil.copytree(source, workspace)

    return workspace