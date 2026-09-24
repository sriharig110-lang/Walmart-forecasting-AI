import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

from AI_tools.tools import execute_tool, tools


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / "api.env")

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")
MAX_ITERATIONS = 5


def _get_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")
    return genai.Client(api_key=api_key)


gemini_function_declaration = [
    types.FunctionDeclaration(
        name=tool["name"],
        description=tool["description"],
        parameters_json_schema=tool["parameters"],
    )
    for tool in tools
]

gemini_tools = types.Tool(function_declarations=gemini_function_declaration)

system_instruction = """
You are a Walmart sales analysis assistant.

Use the available tools to answer the user's questions.

1. Use get_average_sales for historical average sales.
2. Use forecast_sales for future sales predictions.
3. If the user specifies a store ID, provide that store_id when calling forecast_sales.
4. If no store ID is specified, forecast overall Walmart sales.
5. Use compare_stores to compare two stores.
6. For average predicted sales, call forecast_sales first and then get_average_forecast with operation="average".
7. For total predicted sales or revenue, call forecast_sales first and then get_average_forecast with operation="total".
8. Use get_total_sales for historical total sales or revenue.
9. If the number of forecast weeks is missing, ask the user to provide it.
10. Never invent numerical results. Use tool results for numerical answers.
11. Do not expose tool names, function calls, arguments, raw forecast values, or backend processing.
12. Historical questions must use historical tools; future questions must use forecast_sales.
13. Words such as last, previous, historical, or past refer to historical sales.
14. Words such as next, future, predict, or forecast refer to future sales.
15. If the requested historical metric is ambiguous, ask for clarification.
16. Use get_historical_sales for historical trends or visualization data.
17. Do not use get_historical_sales for future forecasts.

Give only the final natural-language answer.
"""


def ask_walmart_ai(user_question):
    """Run the bounded Gemini tool-calling workflow for one user question."""
    if not isinstance(user_question, str) or not user_question.strip():
        return {"answer": "Please enter a question about Walmart sales.", "tool_results": []}

    try:
        client = _get_client()
    except RuntimeError as exc:
        return {"answer": "The AI assistant is not configured correctly.", "tool_results": [], "error": str(exc)}

    contents = [user_question.strip()]
    tool_results = []

    for _ in range(MAX_ITERATIONS):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    tools=[gemini_tools],
                ),
            )
        except Exception as exc:
            return {
                "answer": "Sorry, I couldn't process your request right now. Please try again.",
                "tool_results": tool_results,
                "error": str(exc),
            }

        function_calls = response.function_calls or []
        if not function_calls:
            return {
                "answer": response.text or "I couldn't generate an answer.",
                "tool_results": tool_results,
            }

        if not response.candidates:
            return {
                "answer": "The AI assistant returned an incomplete response.",
                "tool_results": tool_results,
                "error": "No response candidates were returned.",
            }

        contents.append(response.candidates[0].content)

        for function_call in function_calls:
            result = execute_tool(function_call)
            tool_results.append(result)
            contents.append(
                types.Part.from_function_response(
                    name=function_call.name,
                    response={"result": result},
                )
            )

    return {
        "answer": "I couldn't complete the request within the allowed processing steps.",
        "tool_results": tool_results,
        "error": "Maximum agent iterations reached.",
    }


if __name__ == "__main__":
    while True:
        user_question = input("\nYou: ").strip()
        if user_question.lower() in {"exit", "quit", "bye"}:
            print("Walmart AI: Goodbye! 👋")
            break
        result = ask_walmart_ai(user_question)
        print("Walmart AI:", result["answer"])
