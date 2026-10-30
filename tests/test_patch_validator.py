from debugforge.patch_validator import validate_patch


def test_validate_patch_accepts_exact_match():
    source = """
def calculate_discount(total, discount):
    return total - (total * discount)
"""

    result = validate_patch(
        source_code=source,
        old_code="return total - (total * discount)",
        new_code="return total - (total * (discount / 100))"
    )

    assert result["valid"] is True


def test_validate_patch_rejects_missing_old_code():
    source = """
def calculate_discount(total, discount):
    return total - (total * discount)
"""

    result = validate_patch(
        source_code=source,
        old_code="return total + discount",
        new_code="return total - discount"
    )

    assert result["valid"] is False