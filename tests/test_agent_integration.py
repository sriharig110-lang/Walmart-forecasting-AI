from types import SimpleNamespace

from LLM import gemini_agent


class FakeClient:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.calls = []
        self.models = self

    def generate_content(self, **kwargs):
        self.calls.append(kwargs)
        return next(self.responses)


def _function_response(name, args):
    return SimpleNamespace(
        function_calls=[SimpleNamespace(name=name, args=args)],
        candidates=[SimpleNamespace(content=SimpleNamespace(role="model", parts=[]))],
        text=None,
    )


def _final_response(text):
    return SimpleNamespace(function_calls=[], candidates=[], text=text)


def test_agent_orchestrates_multi_tool_forecast(monkeypatch):
    client = FakeClient(
        [
            _function_response("forecast_sales", {"store_id": 7, "weeks": 3}),
            _function_response(
                "get_average_forecast",
                {"forecast": {"forecast": [100.0, 120.0, 140.0]}, "operation": "average"},
            ),
            _final_response("The average predicted weekly sales are $120."),
        ]
    )

    executed = []

    def fake_execute_tool(function_call):
        executed.append((function_call.name, function_call.args))
        if function_call.name == "forecast_sales":
            return {"forecast": [100.0, 120.0, 140.0], "store_id": 7}
        return {"average_predicted_sales": 120.0}

    monkeypatch.setattr(gemini_agent, "_get_client", lambda: client)
    monkeypatch.setattr(gemini_agent, "execute_tool", fake_execute_tool)

    result = gemini_agent.ask_walmart_ai("What is the average predicted sales for Store 7 over 3 weeks?")

    assert result["answer"] == "The average predicted weekly sales are $120."
    assert result["error"] if "error" in result else None is None
    assert [name for name, _ in executed] == ["forecast_sales", "get_average_forecast"]
    assert len(client.calls) == 3


def test_agent_returns_controlled_error_when_model_fails(monkeypatch):
    class FailingClient:
        def __init__(self):
            self.models = self

        def generate_content(self, **kwargs):
            raise RuntimeError("temporary model failure")

    monkeypatch.setattr(gemini_agent, "_get_client", FailingClient)

    result = gemini_agent.ask_walmart_ai("Forecast Store 7 for 3 weeks")

    assert result["answer"].startswith("Sorry, I couldn't process")
    assert result["tool_results"] == []
    assert result["error"] == "temporary model failure"


def test_agent_stops_after_max_iterations(monkeypatch):
    response = _function_response("forecast_sales", {"store_id": 7, "weeks": 1})
    client = FakeClient([response] * gemini_agent.MAX_ITERATIONS)

    monkeypatch.setattr(gemini_agent, "_get_client", lambda: client)
    monkeypatch.setattr(
        gemini_agent,
        "execute_tool",
        lambda function_call: {"forecast": [123.0], "store_id": 7},
    )

    result = gemini_agent.ask_walmart_ai("Forecast Store 7")

    assert result["error"] == "Maximum agent iterations reached."
    assert len(client.calls) == gemini_agent.MAX_ITERATIONS
    assert len(result["tool_results"]) == gemini_agent.MAX_ITERATIONS
