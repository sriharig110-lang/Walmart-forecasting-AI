import pandas as pd

df = pd.read_csv("DATA/Walmart.csv", encoding="latin1")

for store_id in [5, 20]:
    store_data = df[df["Store"] == store_id].copy()
    store_data["Date"] = pd.to_datetime(store_data["Date"],dayfirst=True)
    store_data = store_data.sort_values("Date")

    last_10 = store_data.tail(10)

    average = last_10["Weekly_Sales"].mean()

    print(f"Store {store_id}")
    print(f"Last 10 weeks average: ${average:,.2f}")
    print()





