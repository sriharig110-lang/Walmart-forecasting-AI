from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "DATA" / "walmart.csv"

# Load the dataset relative to the project root so the application works
# outside the original developer machine.
df = pd.read_csv(DATA_PATH, encoding="latin1")

# Convert the date column and normalize the dataset.
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")

required_columns = [
    "Store",
    "Date",
    "Weekly_Sales",
    "Holiday_Flag",
    "Temperature",
    "Fuel_Price",
    "CPI",
    "Unemployment",
]

missing_columns = [column for column in required_columns if column not in df.columns]
if missing_columns:
    raise ValueError(f"Missing required columns: {missing_columns}")

numeric_columns = [
    "Store",
    "Weekly_Sales",
    "Holiday_Flag",
    "Temperature",
    "Fuel_Price",
    "CPI",
    "Unemployment",
]
for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

df = df.dropna(subset=["Date", "Weekly_Sales", "Store"])

feature_columns = ["Temperature", "Fuel_Price", "CPI", "Unemployment"]
df[feature_columns] = df[feature_columns].interpolate(method="linear").ffill().bfill()
df["Holiday_Flag"] = df["Holiday_Flag"].fillna(0).astype(int)
df = df[df["Holiday_Flag"].isin([0, 1])]
df = df[df["Weekly_Sales"] >= 0]
df = df.drop_duplicates()
df = df.sort_values(["Store", "Date"]).reset_index(drop=True)


def forecast_sales(weeks, store_id=None):
    """Forecast future weekly sales for one store or Walmart overall."""
    if not isinstance(weeks, int) or weeks <= 0:
        return {"error": "weeks must be a positive integer."}

    if store_id is not None and not isinstance(store_id, int):
        return {"error": "store_id must be an integer."}

    if store_id is None:
        sales_data = df.groupby("Date")["Weekly_Sales"].sum().sort_index()
    else:
        store_data = df[df["Store"] == store_id].copy()
        if store_data.empty:
            return {"error": f"Store {store_id} was not found."}
        sales_data = store_data.set_index("Date")["Weekly_Sales"].sort_index()

    if len(sales_data) < 52:
        return {"error": "At least 52 weeks of historical data are required for forecasting."}

    sales_data.index = pd.DatetimeIndex(sales_data.index, freq="W-FRI")

    model = SARIMAX(
        sales_data,
        order=(2, 0, 4),
        seasonal_order=(2, 0, 1, 26),
        enforce_stationarity=False,
        enforce_invertibility=False,
    )

    model_fit = model.fit(disp=False, maxiter=500)
    forecast = model_fit.forecast(steps=weeks)

    return {
        "store_id": store_id,
        "weeks": weeks,
        "forecast": forecast.tolist(),
    }
