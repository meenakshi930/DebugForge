
from .ai_agent import ask_model
from .patcher import apply_patch
from .verifier import verify_fix


def generate_diagnosis(prompt: str) -> str:
    return ask_model(prompt)


def apply_and_verify(
    workspace,
    file_path: str,
    old_code: str,
    new_code: str,
    test_command: str
) -> dict:

    patched = apply_patch(
        file_path=file_path,
        old_code=old_code,
        new_code=new_code
    )

    if not patched:
        return {
            "status": "PATCH_FAILED",
            "verified": False
        }

    verification = verify_fix(
        workspace=workspace,
        test_command=test_command
    )

    return {
        "status": verification["status"],
        "verified": verification["verified"],
        "result": verification["result"]
    }
