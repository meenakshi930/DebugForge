from .attempt import RepairAttempt


def build_retry_prompt(
    result,
    evidence: dict,
    source_code: str,
    previous_attempt: RepairAttempt
) -> str:

    return f"""
You are an autonomous debugging engineer.

A previous repair attempt failed.

PREVIOUS ATTEMPT:
Diagnosis:
{previous_attempt.diagnosis}

File:
{previous_attempt.file_path}

OLD CODE:
{previous_attempt.old_code}

NEW CODE:
{previous_attempt.new_code}

PREVIOUS TEST STATUS:
{previous_attempt.test_status}

CURRENT TEST RESULT:
Status: {evidence["status"]}
Test file: {evidence["test_file"]}
Test name: {evidence["test_name"]}
Error: {evidence["error"]}
Expected: {evidence["expected"]}
Actual: {evidence["actual"]}

COMMAND:
{result.command}

CURRENT SOURCE CODE:
{source_code}

TASK:
Analyze why the previous repair failed and propose a better repair.

Return your response in exactly this format:

DIAGNOSIS:
<short explanation of the root cause>

FILE:
<relative file path>

OLD_CODE:
<exact code currently present in the source file>

NEW_CODE:
<replacement code>

RULES:
- Do not modify the test.
- Learn from the previous failed attempt.
- OLD_CODE must exactly match the current source code.
- Make the smallest safe change possible.
- Do not include markdown code fences.
- Do not include any text outside the required sections.
""".strip()