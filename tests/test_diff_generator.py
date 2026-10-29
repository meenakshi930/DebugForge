from debugforge.diff_generator import generate_diff


def test_generate_diff():
    old_code = """def add(a, b):
    return a - b
"""

    new_code = """def add(a, b):
    return a + b
"""

    diff = generate_diff(
        file_path="app.py",
        old_code=old_code,
        new_code=new_code
    )

    assert "-    return a - b" in diff
    assert "+    return a + b" in diff