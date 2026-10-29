from .attempt import RepairAttempt
from .diff_generator import generate_diff
from .patcher import apply_patch
from .verifier import verify_fix


MAX_ATTEMPTS = 3


def repair_once(
    job,
    workspace,
    file_path: str,
    diagnosis: str,
    old_code: str,
    new_code: str,
    test_command: str
) -> dict:

    attempt_number = len(job.attempts.attempts) + 1

    if attempt_number > MAX_ATTEMPTS:
        return {
            "status": "MAX_ATTEMPTS_REACHED",
            "verified": False
        }

    diff = generate_diff(
        file_path=file_path,
        old_code=old_code,
        new_code=new_code
    )

    full_path = workspace / file_path

    patched = apply_patch(
        file_path=str(full_path),
        old_code=old_code,
        new_code=new_code
    )

    if not patched:
        attempt = RepairAttempt(
            attempt_number=attempt_number,
            diagnosis=diagnosis,
            file_path=file_path,
            old_code=old_code,
            new_code=new_code,
            test_status="PATCH_FAILED",
            verified=False,
            error="Could not apply patch"
        )

        job.add_attempt(attempt)

        return {
            "status": "PATCH_FAILED",
            "verified": False,
            "diff": diff
        }

    verification = verify_fix(
        workspace=workspace,
        test_command=test_command
    )

    attempt = RepairAttempt(
        attempt_number=attempt_number,
        diagnosis=diagnosis,
        file_path=file_path,
        old_code=old_code,
        new_code=new_code,
        test_status=verification["status"],
        verified=verification["verified"]
    )

    job.add_attempt(attempt)

    return {
        "status": verification["status"],
        "verified": verification["verified"],
        "diff": diff,
        "result": verification["result"]
    }