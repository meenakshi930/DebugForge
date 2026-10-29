from .workspace import create_workspace
from .runner import run_command
from .pytest_parser import parse_failure
from .localizer import read_file
from .diagnosis import build_repair_prompt
from .retry_prompt import build_retry_prompt
from .agent import generate_repair
from .repair_loop import repair_once, MAX_ATTEMPTS
from .job import Job


def debug_repository(
    repo_path: str,
    test_command: str
) -> dict:

    job = Job(
        repo_path=repo_path,
        command=test_command
    )

    workspace = create_workspace(repo_path)

    result = run_command(
        command=test_command,
        workspace=workspace
    )

    evidence = parse_failure(result)

    job.add_evidence(evidence)

    if not result.failed:
        job.status = "PASSED"

        return {
            "status": "PASSED",
            "workspace": str(workspace),
            "evidence": evidence,
            "job": job
        }

    source_code = ""

    if evidence["test_file"]:
        test_file = workspace / evidence["test_file"]

        if test_file.exists():
            source_code = read_file(str(test_file))

    job.status = "REPAIRING"

    repair_prompt = build_repair_prompt(
        result=result,
        evidence=evidence,
        source_code=source_code
    )

    repair = generate_repair(repair_prompt)

    repair_result = repair_once(
        job=job,
        workspace=workspace,
        file_path=repair.file_path,
        diagnosis=repair.diagnosis,
        old_code=repair.old_code,
        new_code=repair.new_code,
        test_command=test_command
    )

    if repair_result["verified"]:
        job.status = "VERIFIED"

        return {
            "status": job.status,
            "workspace": str(workspace),
            "evidence": evidence,
            "repair": repair,
            "repair_result": repair_result,
            "job": job
        }

    for _ in range(1, MAX_ATTEMPTS):

        previous_attempt = job.last_attempt()

        if previous_attempt is None:
            break

        current_result = repair_result.get("result")

        if current_result is None:
            break

        current_evidence = parse_failure(current_result)

        job.add_evidence(current_evidence)

        current_source = ""

        current_file = workspace / previous_attempt.file_path

        if current_file.exists():
            current_source = read_file(str(current_file))

        retry_prompt = build_retry_prompt(
            result=current_result,
            evidence=current_evidence,
            source_code=current_source,
            previous_attempt=previous_attempt
        )

        repair = generate_repair(retry_prompt)

        repair_result = repair_once(
            job=job,
            workspace=workspace,
            file_path=repair.file_path,
            diagnosis=repair.diagnosis,
            old_code=repair.old_code,
            new_code=repair.new_code,
            test_command=test_command
        )

        if repair_result["verified"]:
            job.status = "VERIFIED"

            return {
                "status": job.status,
                "workspace": str(workspace),
                "evidence": current_evidence,
                "repair": repair,
                "repair_result": repair_result,
                "job": job
            }

    job.status = "FAILED"

    return {
        "status": job.status,
        "workspace": str(workspace),
        "evidence": evidence,
        "repair": repair,
        "repair_result": repair_result,
        "job": job
    }
