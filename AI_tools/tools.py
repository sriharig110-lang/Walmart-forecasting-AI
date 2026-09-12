from Forecasting.forecasting import forecast_sales, df


def get_average_sales(store_id, weeks,operation ="average"):

    store_data = df[
        df["Store"] == store_id
    ].copy()

    if store_data.empty:
        return {
            "error": f"Store {store_id} was not found."
        }

    store_data = store_data.sort_values("Date")

    recent_data = store_data.tail(weeks)

    sales = recent_data["Weekly_Sales"]
    if operation =="total":return {"store_id":store_id,"weeks":weeks,"total_sales":sales.sum()}
    return {"store_id":store_id,"weeks":weeks,"average_sales":sales.mean()}

def compare_stores(store1,store2):
  sales1 = df[df["Store"]==store1]["Weekly_Sales"].sum()
  sales2 = df[df["Store"]==store2]["Weekly_Sales"].sum()
  if sales1 > sales2:
    better_store = store1
  elif sales1 < sales2:
    better_store = store2
  else:
    better_store = "Equal"
  return {"store1":store1,
          "store2":store2,
          "store1_total_sales":sales1,
          "store2_total_sales":sales2,
          "better_store":better_store}

def get_average_forecast(forecast,operation = "average"):

    if isinstance(forecast, dict):
        forecast_values = forecast["forecast"]
    else:
        forecast_values = forecast
    
    if not forecast_values:
        return {
            "error": "No forecast values were provided."
        }
    if operation == "total":
       return{"total_predicted_sales":sum(forecast_values)}
    return {"average_predicted_sales":sum(forecast_values) / len(forecast_values)}

def get_total_sales(store_id=None,weeks=None):
   if weeks is not None and  weeks <= 0:
    return {"error": "Weeks must be greater than 0."}
   if store_id is not None:
      store_data =df[df["Store"]==store_id].copy()
      if store_data.empty:
         return{"error":f"Store{store_id} was not found."}
      store_data = store_data.sort_values("Date")
      
      if weeks is not None:
        store_data = store_data.tail(weeks)

      total_sales = store_data["Weekly_Sales"].sum()    
   else:
      sales_data = (df.groupby("Date")["Weekly_Sales"].sum().sort_index())
      if weeks is not None:
         sales_data = sales_data.tail(weeks)
      total_sales=sales_data.sum()
   return{"Store_id":store_id,
          "weeks":weeks,
          "total_sales": total_sales}

tools = [{
    "type": "function",
    "Name": "get_average_sales",
    "description": """
    Calculate historical Walmart sales for a specific store.

    Use operation="average" when the user asks for average sales.

    Use operation="total" when the user asks for total sales
    or total revenue.
    """,
    "parameters": {
        "type": "object",
        "properties": {
            "store_id": {
                "type": "integer",
                "description": "Walmart store ID."
            },
            "weeks": {
                "type": "integer",
                "description": "Number of most recent historical weeks."
            },
            "operation": {
                "type": "string",
                "enum": ["average", "total"],
                "description": "Calculate either average or total sales."
            }
        },
        "required": ["store_id", "weeks", "operation"]
    }
},
         {
    "type": "function",
    "Name": "forecast_sales",
    "description": """
    Forecast future Walmart weekly sales.

    If store_id is provided, forecast sales specifically
    for that Walmart store.

    If store_id is not provided, forecast overall Walmart sales.

    The weeks parameter specifies the number of future weeks
    to forecast.
    """,
    "parameters": {
        "type": "object",
        "properties": {
            "weeks": {
                "type": "integer",
                "description": "Number of future weeks to forecast."
            },
            "store_id": {
                "type": "integer",
                "description": "Walmart store ID. Optional. If not provided, forecast overall Walmart sales."
            }
        },
        "required": ["weeks"]
    }
},
         {"type":"function",
          "Name":"compare_stores",
          "description":"Compare the total historical sales of two walmart stores.",
          "parameters":{"type":"object",
                        "properties":{"store1":{"type":"integer","description":"First walmart store ID"},"store2":{"type":"integer","description":"Second walmart store ID."}},"required":["store1","store2"]}},
         {
    "type": "function",
    "Name": "get_average_forecast",
    "description": """
    Perform an operation on forecasted Walmart sales.

    Use this tool after forecast_sales when the user asks
    for an average or total of predicted sales.

    operation="average" calculates the average predicted
    weekly sales.

    operation="total" calculates the total predicted sales
    across the forecast period.
    """,
    "parameters": {
        "type": "object",
        "properties": {
            "forecast": {
                "type": "object",
                "description": "The forecast result returned by forecast_sales."
            },
            "operation": {
                "type": "string",
                "enum": ["average", "total"],
                "description": "Whether to calculate the average or total predicted sales."
            }
        },
        "required": ["forecast", "operation"]
    }
},
        {"type":"function",
         "Name":"get_total_sales",
         "description":""" Calculate the total historical walmart sales accross all stores.and
                use this  tool when the user ask for total, overall, or historical walmart sales/revenue.
                this tool does NOT forecast future sales""",
         "parameters":{"type":"object","properties":{"store_id":{"type":"integer","description":"walmart store ID. Optional."},"weeks":{"type":"integer","description":"Number of most historical weeks. Optional."}},"required":[]}}]
        
        
        
        
        

tool_registry = {
    "get_average_sales": get_average_sales,
    "forecast_sales": forecast_sales,
    "compare_stores": compare_stores,
    "get_average_forecast": get_average_forecast,
    "get_total_sales":get_total_sales
}



def execute_tool(function_call):
  tool_name = function_call.name
  arguments = function_call.args
  tool_function = tool_registry.get(tool_name)
  if tool_function is None:
     return{"error":"The requested operation is not available"}
  result = tool_function(**arguments)
  return result
