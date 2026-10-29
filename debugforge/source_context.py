import ast


def extract_function(
    source_code: str,
    function_name: str
) -> str | None:

    try:
        tree = ast.parse(source_code)
    except SyntaxError:
        return None

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name == function_name:
                lines = source_code.splitlines()

                start = node.lineno - 1
                end = node.end_lineno

                return "\n".join(lines[start:end])

    return None