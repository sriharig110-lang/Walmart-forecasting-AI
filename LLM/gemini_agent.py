import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from AI_tools.tools import tools, execute_tool

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / "api.env")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Gemini _API_KEY is not configured.")
client = genai.Client(api_key=api_key)
gemini_function_declaration = [
    types.FunctionDeclaration(
        name=tool["Name"],
        description=tool["description"],
        parameters_json_schema=tool["parameters"]
    )
    for tool in tools]

gemini_tools = types.Tool(
    function_declarations=gemini_function_declaration
    )
system_instruction = """
You are a Walmart sales analysis assistant.

Use the available tools to answer the user's questions.

1. Use get_average_sales for historical average sales.

2. Use forecast_sales for future sales predictions.

3. If the user specifies a store ID, always provide that store_id
   when calling forecast_sales.

4. If the user does not specify a store ID, forecast overall Walmart sales.

5. Use compare_stores to compare two stores.

6. When the user asks for the average predicted sales,
   first call forecast_sales and then call get_average_forecast
   with operation="average".

7. When the user asks for total predicted sales or total predicted
   revenue, first call forecast_sales and then call
   get_average_forecast with operation="total".

8. Use get_total_sales for historical total sales or revenue.
   If a store ID is specified, provide the store_id.
   If a number of weeks is specified, provide the weeks.

9. If the user does not specify the number of weeks for a forecast,
   ask the user to provide the number of weeks.

10. Do not invent numerical results.
    Use tool results when answering numerical questions.

11. Do not expose tool names, function calls, arguments, raw forecast
    values, or backend processing to the user.
12. Historical sales questions must use historical sales tools.
    Do not use forecast_sales for historical data.

13. Future sales questions must use forecast_sales.
    Do not use historical sales tools to answer future predictions.

14. Words such as "were", "last", "previous", "historical",
    or "past" refer to historical sales.

15. Words such as "will", "next", "future", "predict",
    or "forecast" refer to future sales.

16.If a question does not clearly specify a historical metric
    such as average, total, or a time period, do not assume
    what metric the user wants.
    
17. For ambiguous sales questions, ask the user to clarify.
    For example, if the user asks "Tell me about Store 7 sales",
    ask whether they want total sales, average sales, recent
    sales, or future forecast.
    
18. Use get_historical_sales when the user asks for historical
    sales trends, historical sales data, or wants to visualize
    past sales over time.

19. When the user specifies a store ID, provide that store_id
    when calling get_historical_sales.

20. When the user specifies a number of historical weeks,
    provide that weeks value.

21. If the user asks for historical sales visualization,
    use get_historical_sales to obtain the dates and sales values.

22. Do not use get_historical_sales for future forecasts.
    Future prediction questions must use forecast_sales.
    Give only the final natural-language answer.
"""
def ask_walmart_ai(user_question):
    contents = [user_question]
    max_iterations=5
    tool_results=[]
    
    for _ in range(max_iterations):
        try:
            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=contents,
                config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                tools=[gemini_tools]
                )
            )
        except Exception:
            return "Sorry, i couldn't process your request right now. please try again"

        if not response.function_calls:
            return {"answer":response.text,"tool_results":tool_results}
        contents.append(response.candidates[0].content)

        for function_call in response.function_calls:
            result = execute_tool(function_call)
            tool_results.append(result)
            tool_response= types.Part.from_function_response(name=function_call.name,response={"result":result})

            contents.append(tool_response)

# lets make this interactive
if __name__=="__main__":
    while True:
        user_question = input("\n You: ") 
        if user_question.lower() in ["exit","quit","bye"]:
            print("Walmart AI: Goodbye! 👋")
            break
    answer = ask_walmart_ai(user_question)
    print("walmart_AI :" ,answer)                                    





                                                        


