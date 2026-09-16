import pandas as pd
import streamlit as st

def render_historical_sales(result):
    dates = result.get("dates",[])
    sales = result.get("sales",[])
    if not dates or not sales:
        return 
    data = pd.DataFrame({"Date":pd.to_datetime(dates),"Weekly Sales":sales})
    data = data.set_index("Date")
    store_id = result.get("store_id")
    if store_id is not None :
        title = f"📈 Historical Sales — Store {store_id}"
    else:
        title = "📈 Historical Walmart Sales"

    st.subheader(title)
    st.line_chart(data)

def render_forecast(result):
    forecast = result.get("forecast", [])

    if not forecast:
        return

    data = pd.DataFrame({
        "Forecast": forecast
    })

    store_id = result.get("store_id")

    if store_id is not None:
        title = f"🔮 Sales Forecast — Store {store_id}"
    else:
        title = "🔮 Walmart Sales Forecast"

    st.subheader(title)
    st.line_chart(data)

def render_store_comparison(result):
    store1 = result.get("store1")
    store2 = result.get("store2")

    sales1 = result.get("store1_total_sales")
    sales2 = result.get("store2_total_sales")

    if store1 is None or store2 is None:
        return

    if sales1 is None or sales2 is None:
        return

    data = pd.DataFrame({
        "Store": [f"Store {store1}", f"Store {store2}"],
        "Total Sales": [sales1, sales2]
    })

    st.subheader(f"🏪 Store Comparison — Store {store1} vs Store {store2}")
    st.bar_chart(data.set_index("Store"))

def render_sales_summary(result):

    store_id = result.get("store_id", result.get("Store_id"))

    if "average_sales" in result:
        average_sales = result["average_sales"]

        if store_id is None:
            title = "📊 Average Walmart Sales"
            label = "Overall Walmart"
        else:
            title = f"📊 Average Sales — Store {store_id}"
            label = f"Store {store_id}"

        data = pd.DataFrame({
            "Store": [label],
            "Average Sales": [average_sales]
        })

        st.subheader(title)
        st.bar_chart(data.set_index("Store"))

    elif "total_sales" in result:
        total_sales = result["total_sales"]

        if store_id is None:
            title = "📊 Total Walmart Sales"
            label = "Overall Walmart"
        else:
            title = f"📊 Total Sales — Store {store_id}"
            label = f"Store {store_id}"

        data = pd.DataFrame({
            "Store": [label],
            "Total Sales": [total_sales]
        })

        st.subheader(title)
        st.bar_chart(data.set_index("Store"))


def render_forecast_summary(result):
    average_predicted = result.get("average_predicted_sales")
    total_predicted = result.get("total_predicted_sales")

    if average_predicted is not None:
        data = pd.DataFrame({
            "Metric": ["Average Predicted Sales"],
            "Sales": [average_predicted]
        })

        st.subheader("📊 Average Predicted Sales")
        st.bar_chart(data.set_index("Metric"))

    if total_predicted is not None:
        data = pd.DataFrame({
            "Metric": ["Total Predicted Sales"],
            "Sales": [total_predicted]
        })

        st.subheader("📊 Total Predicted Sales")
        st.bar_chart(data.set_index("Metric"))

def render_visualization(result):
    if "average_predicted_sales"in result or "total_predicted_sales" in result:
        render_forecast_summary(result)

    elif "dates" in result and "sales" in result:
        render_historical_sales(result)

    elif "forecast" in result:
        render_forecast(result)

    elif "store1_total_sales" in result:
        render_store_comparison(result)

    elif "average_sales" in result or "total_sales" in result:
        render_sales_summary(result)