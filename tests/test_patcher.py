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
