from types import SimpleNamespace

from AI_tools.tools import (
    MAX_WEEKS,
    execute_tool,
    get_average_forecast,
    get_average_sales,
    get_historical_sales,
    get_total_sales,
    tools,
)


def test_tool_schema_names_match_registry():
    names = {tool["name"] for tool in tools}
    assert names == {
        "get_average_sales",
        "forecast_sales",
        "compare_stores",
        "get_average_forecast",
        "get_historical_sales",
        "get_total_sales",
    }


def test_total_sales_for_store():
    result = get_total_sales(store_id=1, weeks=4)
    assert "error" not in result
    assert result["store_id"] == 1
    assert result["weeks"] == 4
    assert result["total_sales"] >= 0


def test_total_sales_overall():
    result = get_total_sales(weeks=4)
    assert "error" not in result
    assert result["store_id"] is None
    assert result["total_sales"] >= 0


def test_average_sales():
    result = get_average_sales(store_id=1, weeks=4)
    assert "error" not in result
    assert result["average_sales"] >= 0


def test_historical_sales_returns_aligned_series():
    result = get_historical_sales(store_id=1, weeks=4)
    assert "error" not in result
    assert len(result["dates"]) == len(result["sales"]) == 4


def test_invalid_week_count():
    assert "error" in get_total_sales(weeks=0)
    assert "error" in get_total_sales(weeks=MAX_WEEKS + 1)


def test_missing_store():
    result = get_total_sales(store_id=999999)
    assert result["error"]


def test_forecast_summary_average_and_total():
    forecast = {"forecast": [10, 20, 30]}
    assert get_average_forecast(forecast, "average")["average_predicted_sales"] == 20
    assert get_average_forecast(forecast, "total")["total_predicted_sales"] == 60


def test_invalid_forecast_operation():
    assert "error" in get_average_forecast({"forecast": [10]}, "median")


def test_unknown_tool_is_safe():
    call = SimpleNamespace(name="does_not_exist", args={})
    result = execute_tool(call)
    assert "error" in result


def test_malformed_tool_arguments_are_safe():
    call = SimpleNamespace(name="get_total_sales", args={"weeks": 0})
    result = execute_tool(call)
    assert "error" in result
