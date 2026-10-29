
from pathlib import Path

from debugforge.workspace import create_workspace


def test_create_workspace(tmp_path):
    repo = tmp_path / "sample_repo"
    repo.mkdir()

    app_file = repo / "app.py"
    app_file.write_text(
        "print('hello')",
        encoding="utf-8"
    )

    workspace = create_workspace(str(repo))

    workspace_file = workspace / "app.py"

    assert workspace.exists()
    assert workspace.is_dir()
    assert workspace_file.exists()
    assert workspace_file.read_text(encoding="utf-8") == "print('hello')"
