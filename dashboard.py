# dashboard.py
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "BI_Dashboard_Telemetry_Data.csv"
SHAP_IMAGE_PATH = BASE_DIR / "shap_explainability_analysis.png"

st.title("Space Weather Intelligence Dashboard")
st.sidebar.header("Filters")

if not DATA_PATH.exists():
    st.error(
        f"Data file not found: `{DATA_PATH.name}`. "
        "Place `BI_Dashboard_Telemetry_Data.csv` in the project folder."
    )
    st.stop()

df = pd.read_csv(DATA_PATH)
df["time_tag"] = pd.to_datetime(df["time_tag"])

min_date = df["time_tag"].min().date()
max_date = df["time_tag"].max().date()
date_range = st.sidebar.date_input("Date Range", [min_date, max_date])

if isinstance(date_range, (list, tuple)):
    start_date, end_date = date_range[0], date_range[-1]
else:
    start_date = end_date = date_range

mask = (df["time_tag"].dt.date >= start_date) & (
    df["time_tag"].dt.date <= end_date
)
filtered = df.loc[mask]

if filtered.empty:
    st.warning("No data in the selected date range.")
    st.stop()

# KPIs in columns for better layout
col1, col2 = st.columns(2)
col1.metric("Max Flux", f"{filtered['flux'].max():.2e}")
col2.metric("Anomaly Count", int(filtered["Is_Anomaly"].sum()))

# Interactive Line Chart
st.subheader("X-Ray Flux Over Time")
st.line_chart(filtered, x="time_tag", y="flux", use_container_width=True)

st.subheader("SHAP Feature Importance")
if SHAP_IMAGE_PATH.exists():
    st.image(str(SHAP_IMAGE_PATH))
else:
    st.info(
        f"`{SHAP_IMAGE_PATH.name}` not found. "
        "Add the image to show SHAP explainability."
    )
