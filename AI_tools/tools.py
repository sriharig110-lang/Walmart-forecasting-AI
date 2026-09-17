from Forecasting.forecasting import df, forecast_sales

MAX_WEEKS = 52


def _validate_weeks(weeks):
    if not isinstance(weeks, int) or weeks <= 0:
        return {"error": "weeks must be a positive integer."}
    if weeks > MAX_WEEKS:
        return {"error": f"weeks cannot exceed {MAX_WEEKS}."}
    return None


def _validate_store(store_id):
    if store_id is not None and not isinstance(store_id, int):
        return {"error": "store_id must be an integer."}
    return None


def get_average_sales(store_id, weeks, operation="average"):
    error = _validate_store(store_id) or _validate_weeks(weeks)
    if error:
        return error
    if operation not in {"average", "total"}:
        return {"error": "operation must be 'average' or 'total'."}

    store_data = df[df["Store"] == store_id].copy()
    if store_data.empty:
        return {"error": f"Store {store_id} was not found."}

    recent_data = store_data.sort_values("Date").tail(weeks)
    sales = recent_data["Weekly_Sales"]

    if operation == "total":
        return {"store_id": store_id, "weeks": weeks, "total_sales": float(sales.sum())}
    return {"store_id": store_id, "weeks": weeks, "average_sales": float(sales.mean())}


def compare_stores(store1, store2):
    if not isinstance(store1, int) or not isinstance(store2, int):
        return {"error": "store IDs must be integers."}
    if store1 == store2:
        return {"error": "store1 and store2 must be different stores."}

    data1 = df[df["Store"] == store1]
    data2 = df[df["Store"] == store2]
    if data1.empty:
        return {"error": f"Store {store1} was not found."}
    if data2.empty:
        return {"error": f"Store {store2} was not found."}

    sales1 = float(data1["Weekly_Sales"].sum())
    sales2 = float(data2["Weekly_Sales"].sum())
    better_store = store1 if sales1 > sales2 else store2 if sales2 > sales1 else "Equal"
    return {
        "store1": store1,
        "store2": store2,
        "store1_total_sales": sales1,
        "store2_total_sales": sales2,
        "better_store": better_store,
    }


def get_average_forecast(forecast, operation="average"):
    if isinstance(forecast, dict):
        forecast_values = forecast.get("forecast", [])
    else:
        forecast_values = forecast or []

    if not forecast_values:
        return {"error": "No forecast values were provided."}
    if operation not in {"average", "total"}:
        return {"error": "operation must be 'average' or 'total'."}

    values = [float(value) for value in forecast_values]
    if operation == "total":
        return {"total_predicted_sales": sum(values)}
    return {"average_predicted_sales": sum(values) / len(values)}


def get_total_sales(store_id=None, weeks=None):
    error = _validate_store(store_id)
    if error:
        return error
    if weeks is not None:
        error = _validate_weeks(weeks)
        if error:
            return error

    if store_id is not None:
        data = df[df["Store"] == store_id].sort_values("Date")
        if data.empty:
            return {"error": f"Store {store_id} was not found."}
        if weeks is not None:
            data = data.tail(weeks)
        total_sales = float(data["Weekly_Sales"].sum())
    else:
        data = df.groupby("Date")["Weekly_Sales"].sum().sort_index()
        if weeks is not None:
            data = data.tail(weeks)
        total_sales = float(data.sum())

    return {"store_id": store_id, "weeks": weeks, "total_sales": total_sales}


def get_historical_sales(store_id=None, weeks=None):
    error = _validate_store(store_id)
    if error:
        return error
    if weeks is not None:
        error = _validate_weeks(weeks)
        if error:
            return error

    if store_id is not None:
        data = df[df["Store"] == store_id].sort_values("Date")
        if data.empty:
            return {"error": f"Store {store_id} was not found."}
        if weeks is not None:
            data = data.tail(weeks)
        return {
            "store_id": store_id,
            "dates": data["Date"].dt.strftime("%Y-%m-%d").tolist(),
            "sales": data["Weekly_Sales"].astype(float).tolist(),
        }

    data = df.groupby("Date")["Weekly_Sales"].sum().sort_index()
    if weeks is not None:
        data = data.tail(weeks)
    return {
        "store_id": None,
        "dates": data.index.strftime("%Y-%m-%d").tolist(),
        "sales": data.astype(float).tolist(),
    }


tools = [
    {
        "type": "function",
        "name": "get_average_sales",
        "description": "Calculate average or total historical sales for a specific Walmart store.",
        "parameters": {
            "type": "object",
            "properties": {
                "store_id": {"type": "integer", "description": "Walmart store ID."},
                "weeks": {"type": "integer", "description": "Number of most recent historical weeks."},
                "operation": {"type": "string", "enum": ["average", "total"]},
            },
            "required": ["store_id", "weeks", "operation"],
        },
    },
    {
        "type": "function",
        "name": "forecast_sales",
        "description": "Forecast future Walmart weekly sales for one store or overall Walmart.",
        "parameters": {
            "type": "object",
            "properties": {
                "weeks": {"type": "integer", "description": "Number of future weeks to forecast."},
                "store_id": {"type": "integer", "description": "Optional Walmart store ID."},
            },
            "required": ["weeks"],
        },
    },
    {
        "type": "function",
        "name": "compare_stores",
        "description": "Compare total historical sales of two Walmart stores.",
        "parameters": {
            "type": "object",
            "properties": {
                "store1": {"type": "integer", "description": "First Walmart store ID."},
                "store2": {"type": "integer", "description": "Second Walmart store ID."},
            },
            "required": ["store1", "store2"],
        },
    },
    {
        "type": "function",
        "name": "get_average_forecast",
        "description": "Calculate the average or total of forecast values returned by forecast_sales.",
        "parameters": {
            "type": "object",
            "properties": {
                "forecast": {"type": "object", "description": "Forecast result returned by forecast_sales."},
                "operation": {"type": "string", "enum": ["average", "total"]},
            },
            "required": ["forecast", "operation"],
        },
    },
    {
        "type": "function",
        "name": "get_historical_sales",
        "description": "Get historical weekly sales values and dates for a store or overall Walmart.",
        "parameters": {
            "type": "object",
            "properties": {
                "store_id": {"type": ["integer", "null"], "description": "Walmart store ID, or null for overall sales."},
                "weeks": {"type": ["integer", "null"], "description": "Recent historical weeks, or null for all available data."},
            },
            "required": ["store_id", "weeks"],
        },
    },
    {
        "type": "function",
        "name": "get_total_sales",
        "description": "Calculate total historical Walmart sales for a store or overall Walmart.",
        "parameters": {
            "type": "object",
            "properties": {
                "store_id": {"type": ["integer", "null"], "description": "Optional Walmart store ID."},
                "weeks": {"type": ["integer", "null"], "description": "Optional number of recent historical weeks."},
            },
            "required": ["store_id", "weeks"],
        },
    },
]


tool_registry = {
    "get_average_sales": get_average_sales,
    "forecast_sales": forecast_sales,
    "compare_stores": compare_stores,
    "get_average_forecast": get_average_forecast,
    "get_total_sales": get_total_sales,
    "get_historical_sales": get_historical_sales,
}


def execute_tool(function_call):
    tool_name = getattr(function_call, "name", None)
    arguments = getattr(function_call, "args", {}) or {}
    tool_function = tool_registry.get(tool_name)
    if tool_function is None:
        return {"error": "The requested operation is not available."}
    try:
        return tool_function(**arguments)
    except (TypeError, ValueError) as exc:
        return {"error": f"Invalid arguments for {tool_name}: {exc}"}
    except Exception:
        return {"error": f"The {tool_name} operation could not be completed."}
