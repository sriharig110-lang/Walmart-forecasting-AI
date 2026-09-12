import streamlit as st
import pandas as pd
from LLM.gemini_agent import ask_walmart_ai

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

    tool_results = st.session_state.tool_results

    # Forecast visualization
    for tool_result in tool_results:
        if "forecast" in tool_result:
            st.subheader("📈 Sales Forecast")
            st.line_chart(tool_result["forecast"])

    # Average sales comparison
    average_results = [
        result
        for result in tool_results
        if "average_sales" in result
    ]

    if len(average_results) >= 2:

        comparison_data = pd.DataFrame({
            "Store": [
                f"Store {result['store_id']}"
                for result in average_results
            ],
            "Average Sales": [
                result["average_sales"]
                for result in average_results
            ]
        })

        st.subheader("📊 Average Sales Comparison")

        st.bar_chart(
            comparison_data.set_index("Store")
        )

    # Total sales comparison
    total_results = [
        result
        for result in tool_results
        if "total_sales" in result and "Store_id" in result
    ]

    if len(total_results) >= 2:

        total_comparison = pd.DataFrame({
            "Store": [
                f"Store {result['Store_id']}"
                for result in total_results
            ],
            "Total Sales": [
                result["total_sales"]
                for result in total_results
            ]
        })

        st.subheader("📊 Total Sales Comparison")

        st.bar_chart(
            total_comparison.set_index("Store")
        )
    

    
    
    
    
    

    
    
    
 
    
 
    
    
    
    
    
    
    
    
    
    
 
    
    
    
    
    
    
    
    
    
    
 
    
 
    
    
    
    
    
    
    
    
    
    
 
    
 
    
    
    
    
    

    
    
    
    
    
    

    

    
    
    
    