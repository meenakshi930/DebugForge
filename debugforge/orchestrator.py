from .workspace import create_workspace
from .runner import run_command
from .pytest_parser import parse_failure
from .localizer import read_file
from .diagnosis import build_repair_prompt
from .retry_prompt import build_retry_prompt
from .agent import generate_repair
from .repair_loop import repair_once, MAX_ATTEMPTS
from .job import Job
from .source_localizer import find_source_frame
from .source_context import extract_function


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
    source_frame = find_source_frame(
        result=result,
        workspace=workspace,
        test_file=evidence["test_file"]
    )

    if source_frame:
        evidence["source_file"] = source_frame["file_path"]
        evidence["source_line"] = source_frame["line_number"]
        evidence["source_function"] = source_frame["function_name"]

        source_path = workspace / source_frame["file_path"]

        if source_path.exists():
            full_source = read_file(str(source_path))

            source_code = extract_function(
                source_code=full_source,
                function_name=source_frame["function_name"]
            )

            if source_code is None:
                source_code = full_source

    job.status = "REPAIRING"

    repair_prompt = build_repair_prompt(
        result=result,
        evidence=evidence,
        source_code=source_code
    )

    repair = generate_repair(repair_prompt)

    if source_frame and repair.file_path != source_frame["file_path"]:
        repair.file_path = source_frame["file_path"]

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

        source_frame = find_source_frame(
            result=current_result,
            workspace=workspace,
            test_file=current_evidence["test_file"]
        )

        if source_frame:
            current_evidence["source_file"] = source_frame["file_path"]
            current_evidence["source_line"] = source_frame["line_number"]
            current_evidence["source_function"] = source_frame["function_name"]

            source_path = workspace / source_frame["file_path"]

            if source_path.exists():
                full_source = read_file(str(source_path))

                current_source = extract_function(
                    source_code=full_source,
                    function_name=source_frame["function_name"]
                )

                if current_source is None:
                    current_source = full_source

        retry_prompt = build_retry_prompt(
            result=current_result,
            evidence=current_evidence,
            source_code=current_source,
            previous_attempt=previous_attempt
        )

        repair = generate_repair(retry_prompt)

        if source_frame and repair.file_path != source_frame["file_path"]:
            repair.file_path = source_frame["file_path"]

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