from debugforge.repair_parser import parse_repair_response


def test_parse_repair_response():

    response = """
DIAGNOSIS:
Discount is treated as 10 instead of 10%.

FILE:
demo_target/app.py

OLD_CODE:
return total - (total * discount)

NEW_CODE:
return total - (total * (discount / 100))
"""

    result = parse_repair_response(response)

    assert result.diagnosis == (
        "Discount is treated as 10 instead of 10%."
    )

    assert result.file_path == "demo_target/app.py"

    assert result.old_code == (
        "return total - (total * discount)"
    )

    assert result.new_code == (
        "return total - (total * (discount / 100))"
    )