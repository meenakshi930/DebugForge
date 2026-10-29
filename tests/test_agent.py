from debugforge.agent import generate_repair


def test_generate_repair(monkeypatch):

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

    def fake_ask_model(prompt):
        return response

    monkeypatch.setattr(
        "debugforge.agent.ask_model",
        fake_ask_model
    )

    result = generate_repair("test prompt")

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