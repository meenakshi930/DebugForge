from .failure import TestFailure


def build_diagnosis_prompt(
    result: TestFailure,
    evidence: dict,
    source_code: str
) -> str:

    return f"""
You are a debugging engineer.

Analyze the following Python test failure.

TEST RESULT:
Status: {evidence["status"]}
Test file: {evidence["test_file"]}
Test name: {evidence["test_name"]}
Error: {evidence["error"]}
Expected: {evidence["expected"]}
Actual: {evidence["actual"]}

COMMAND:
{result.command}

SOURCE CODE:
{source_code}

TASK:
1. Identify the root cause.
2. Identify the exact function responsible.
3. Explain why the current behavior is wrong.
4. Suggest the smallest code change needed.
5. Do not modify the test.

Return your analysis clearly.
""".strip()

def build_repair_prompt(
    result,
    evidence: dict,
    source_code: str
) -> str:

    return f"""
You are an autonomous debugging engineer.

Analyze the failing Python test and propose the smallest safe code change.

TEST RESULT:
Status: {evidence["status"]}
Test file: {evidence["test_file"]}
Test name: {evidence["test_name"]}
Error: {evidence["error"]}
Expected: {evidence["expected"]}
Actual: {evidence["actual"]}

COMMAND:
{result.command}

SOURCE CODE:
{source_code}

Return your response in exactly this format:

DIAGNOSIS:
<short explanation of the root cause>

FILE:
<relative file path>

OLD_CODE:
<exact code that should be replaced>

NEW_CODE:
<replacement code>

RULES:
- Change only the code necessary to fix the bug.
- Do not modify the test.
- OLD_CODE must exactly match the existing source code.
- Do not include markdown code fences.
- Do not include any text outside the required sections.
""".strip()