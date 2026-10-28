
from .workspace import create_workspace
from .runner import run_command
from .pytest_parser import parse_failure
from .localizer import read_file
from .diagnosis import build_diagnosis_prompt


def debug_repository(
    repo_path: str,
    test_command: str
) -> dict:

    workspace = create_workspace(repo_path)

    result = run_command(
        command=test_command,
        workspace=workspace
    )

    evidence = parse_failure(result)

    if not result.failed:
        return {
            "status": "PASSED",
            "workspace": str(workspace),
            "evidence": evidence
        }

    source_code = ""

    if evidence["test_file"]:
        test_file = workspace / evidence["test_file"]

        if test_file.exists():
            source_code = read_file(str(test_file))

    diagnosis_prompt = build_diagnosis_prompt(
        result=result,
        evidence=evidence,
        source_code=source_code
    )

    return {
        "status": "FAILED",
        "workspace": str(workspace),
        "evidence": evidence,
        "diagnosis_prompt": diagnosis_prompt
    }
