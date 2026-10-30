import pytest

from debugforge.ai_agent import ask_model


@pytest.mark.integration
def test_real_nemotron_call():
    response = ask_model(
        "Reply with exactly: DEBUGFORGE_TEST_OK"
    )

    assert response
    assert "DEBUGFORGE_TEST_OK" in response