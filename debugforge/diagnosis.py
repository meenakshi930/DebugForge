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