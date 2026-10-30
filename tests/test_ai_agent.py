from debugforge.ai_agent import ask_model


class FakeMessage:
    content = "test response"


class FakeChoice:
    message = FakeMessage()


class FakeResponse:
    choices = [FakeChoice()]


def test_ask_model(monkeypatch):
    def fake_create(**kwargs):
        assert kwargs["model"]
        assert len(kwargs["messages"]) == 1
        assert kwargs["messages"][0]["role"] == "user"
        assert kwargs["messages"][0]["content"] == "hello"

        return FakeResponse()

    monkeypatch.setattr(
        "debugforge.ai_agent.client.chat.completions.create",
        fake_create
    )

    result = ask_model("hello")

    assert result == "test response"