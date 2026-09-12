
import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
# loading the data
df = pd.read_csv('C:/Users/sriha/Walmart-forecasting-AI/DATA/walmart.csv',encoding = "latin1")
# convert the date column
df['Date']= pd.to_datetime(df['Date'],dayfirst=True)
#sort data by date
df = df.sort_values("Date")

# data cleaning and handleing the missing values

# ==========================================
#  CHECK REQUIRED COLUMNS
# ==========================================

required_columns = [
    "Store",
    "Date",
    "Weekly_Sales",
    "Holiday_Flag",
    "Temperature",
    "Fuel_Price",
    "CPI",
    "Unemployment"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )


# ==========================================
#  HANDLE DATE
# ==========================================

df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)

# Handle missing/invalid dates
df["Date"] = df["Date"].ffill().bfill()


# ==========================================
#  CONVERT NUMERIC COLUMNS
# ==========================================

numeric_columns = [
    "Store",
    "Weekly_Sales",
    "Holiday_Flag",
    "Temperature",
    "Fuel_Price",
    "CPI",
    "Unemployment"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# ==========================================
#  HANDLE MISSING WEEKLY SALES
# ==========================================

# Weekly_Sales is the target.
# If it is missing/invalid, drop that row.

df = df.dropna(subset=["Weekly_Sales"])
#===========================================
#  HANDLE MISSING STORE IDs
# ==========================================

# Store ID cannot be reliably guessed.
df = df.dropna(subset=["Store"])
# ==========================================
#  HANDLE MISSING NUMERIC FEATURES
# ==========================================
feature_columns = [
    "Temperature",
    "Fuel_Price",
    "CPI",
    "Unemployment"
]

# Interpolate values between valid observations
df[feature_columns] = df[
    feature_columns
].interpolate(method="linear")

# Handle missing values at the beginning/end
df[feature_columns] = df[
    feature_columns
].ffill().bfill()


# ==========================================
#  HANDLE HOLIDAY FLAG
# ==========================================

# Missing Holiday_Flag → assume non-holiday
df["Holiday_Flag"] = df[
    "Holiday_Flag"
].fillna(0)

df["Holiday_Flag"] = df[
    "Holiday_Flag"
].astype(int)

# Keep only valid values: 0 or 1
df = df[
    df["Holiday_Flag"].isin([0, 1])
]


# ==========================================
#  HANDLE INVALID SALES
# ==========================================

# Weekly sales cannot be negative.

df = df[
    df["Weekly_Sales"] >= 0
]


# ==========================================
#  REMOVE DUPLICATES
# ==========================================

df = df.drop_duplicates()


# ==========================================
#  SORT DATA
# ==========================================

df = df.sort_values(
    ["Store", "Date"]
)


# ==========================================
#  RESET INDEX
# ==========================================

df = df.reset_index(drop=True)

def forecast_sales(weeks, store_id=None):

    # ==========================================
    # OVERALL WALMART FORECAST
    # ==========================================

    if store_id is None:

        sales_data = (
            df.groupby("Date")["Weekly_Sales"]
            .sum()
            .sort_index()
        )

    # ==========================================
    # STORE-SPECIFIC FORECAST
    # ==========================================

    else:

        store_data = df[
            df["Store"] == store_id
        ].copy()

        if store_data.empty:
            return {
                "error": f"Store {store_id} was not found."
            }

        store_data = store_data.sort_values("Date")

        sales_data = (
            store_data
            .set_index("Date")["Weekly_Sales"]
            .sort_index()
        )

    # ==========================================
    # SET WEEKLY FREQUENCY
    # ==========================================

    sales_data.index = pd.DatetimeIndex(
        sales_data.index,
        freq="W-FRI"
    )

    # ==========================================
    # SARIMA MODEL
    # ==========================================

    model = SARIMAX(
        sales_data,
        order=(2, 0, 4),
        seasonal_order=(2, 0, 1, 26),
        enforce_stationarity=False,
        enforce_invertibility=False
    )

    model_fit = model.fit(
        disp=False,
        maxiter=500
    )

    # ==========================================
    # FORECAST
    # ==========================================

    forecast = model_fit.forecast(
        steps=weeks
    )

    return {
        "store_id": store_id,
        "weeks": weeks,
        "forecast": forecast.tolist()
    }

