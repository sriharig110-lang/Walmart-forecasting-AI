import streamlit as st
import pandas as pd
from LLM.gemini_agent import ask_walmart_ai
from Visualization.visualizations import render_visualization

st.set_page_config(
    page_title="Walmart AI ",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 Walmart AI Assistant")
st.caption("AI-powered Walmart sales analysis and forecasting")
with st.sidebar:
    st.header("Example Questions")

    st.write("Try asking:")

    st.markdown("""
    - What is the total sale for Store 5?
    - What is the average sale for Store 7 over the last 10 weeks?
    - Forecast the next 5 weeks for Store 7.
    - Compare Store 5 and Store 20.
    """)
    show_visuals = st.checkbox("📊 Show Visuals")
if "messages" not in st.session_state:
    st.session_state.messages = []
if "tool_results" not in st.session_state:
    st.session_state.tool_results = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_question := st.chat_input("Ask about sales, forecast, or store performance ..."):

    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    with st.chat_message("user"):
        st.markdown(user_question)
    with st.spinner("Analyzing walmart data..."):
        result = ask_walmart_ai(user_question)
    answer=result["answer"]
    tool_results=result["tool_results"]
    st.session_state.tool_results = tool_results
    answer = answer.replace("$",r"\$")
    

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    with st.chat_message("assistant"):
        st.markdown(answer)

# Visualizations
if show_visuals and st.session_state.tool_results:
    for tool_result in st.session_state.tool_results:
        if "error" not in tool_result:
            render_visualization(tool_result)
 