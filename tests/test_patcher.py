from debugforge.patcher import apply_patch


def test_apply_patch(tmp_path):
    file_path = tmp_path / "app.py"

    old_code = """def apply_discount(total, discount):
    return total - (total * discount)
"""

    new_code = """def apply_discount(total, discount):
    discount = discount / 100
    return total - (total * discount)
"""

    file_path.write_text(old_code, encoding="utf-8")

    result = apply_patch(
        str(file_path),
        old_code,
        new_code
    )

    updated_code = file_path.read_text(encoding="utf-8")

    assert result is True
    assert updated_code == new_code

def test_apply_patch_rejects_multiple_matches(tmp_path):
    file_path = tmp_path / "app.py"

    file_path.write_text(
        """
def first():
    return 10

def second():
    return 10
""",
        encoding="utf-8"
    )

    from debugforge.patcher import apply_patch

    result = apply_patch(
        file_path=str(file_path),
        old_code="return 10",
        new_code="return 20"
    )

    assert result is False

    content = file_path.read_text(encoding="utf-8")

    assert "return 10" in content
    assert "return 20" not in content

def test_apply_patch_rejects_missing_old_code(tmp_path):
    file_path = tmp_path / "app.py"

    original_code = """def calculate_discount(total, discount):
    return total - (total * discount)
"""

    file_path.write_text(
        original_code,
        encoding="utf-8"
    )

    result = apply_patch(
        str(file_path),
        "return total + discount",
        "return total - discount"
    )

    content = file_path.read_text(encoding="utf-8")

    assert result is False
    assert content == original_code
