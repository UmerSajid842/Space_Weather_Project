from pathlib import Path

import streamlit as st

from dashboard_utils import (
    build_anomaly_figure,
    build_flux_figure,
    compute_kpis,
    filter_telemetry,
    load_telemetry,
)

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "BI_Dashboard_Telemetry_Data.csv"
SHAP_IMAGE_PATH = BASE_DIR / "shap_explainability_analysis (2).png"
SOLAR_TREND_IMAGE_PATH = BASE_DIR / "solar_flux_trend (2).png"

st.set_page_config(page_title="Space Weather Intelligence", page_icon="☀", layout="wide")
st.markdown(
    """
    <style>
    .hero { padding: 1.2rem 1.5rem; border-radius: 0.8rem; background: linear-gradient(120deg, #0f172a, #1e3a8a); color: white; margin-bottom: 1rem; }
    .hero h1 { margin: 0; font-size: 2.2rem; }
    .hero p { margin: 0.45rem 0 0; color: #dbeafe; }
    .section-note { color: #64748b; font-size: 0.95rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hero"><h1>Space Weather Intelligence</h1><p>Explore solar X-ray flux, anomaly flags, and explainability artifacts from the project telemetry pipeline.</p></div>',
    unsafe_allow_html=True,
)

try:
    telemetry = load_telemetry(DATA_PATH)
except (FileNotFoundError, ValueError) as exc:
    st.error(str(exc))
    st.info("Place the committed telemetry CSV in the project directory and refresh the dashboard.")
    st.stop()

with st.sidebar:
    st.header("Monitoring window")
    minimum_date = telemetry["time_tag"].min().date()
    maximum_date = telemetry["time_tag"].max().date()
    date_range = st.date_input(
        "Observation dates",
        value=(minimum_date, maximum_date),
        min_value=minimum_date,
        max_value=maximum_date,
    )
    st.divider()
    st.caption("This dashboard presents project telemetry and saved model artifacts. It is not a live operational alerting system.")

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
elif isinstance(date_range, (tuple, list)) and date_range:
    start_date = end_date = date_range[0]
else:
    start_date = end_date = date_range

filtered = filter_telemetry(telemetry, start_date, end_date)
if filtered.empty:
    st.warning("No observations exist in the selected date range. Choose a wider window.")
    st.stop()

kpis = compute_kpis(filtered)
metric_cols = st.columns(5)
metric_cols[0].metric("Observations", f"{kpis['observations']:,}")
metric_cols[1].metric("Peak flux", f"{kpis['peak_flux']:.2e}")
metric_cols[2].metric("Mean flux", f"{kpis['mean_flux']:.2e}")
metric_cols[3].metric("Flagged anomalies", f"{kpis['anomalies']:,}")
metric_cols[4].metric("Latest observation", kpis["latest_time"].strftime("%Y-%m-%d %H:%M"))

st.subheader("Monitoring overview")
st.markdown('<p class="section-note">The selected period is shown with flagged anomalies highlighted as diamonds.</p>', unsafe_allow_html=True)
st.plotly_chart(build_flux_figure(filtered), use_container_width=True)

st.subheader("Anomaly analysis")
st.markdown('<p class="section-note">The anomaly flag is read from the project telemetry output; the dashboard does not retrain the anomaly model.</p>', unsafe_allow_html=True)
st.plotly_chart(build_anomaly_figure(filtered), use_container_width=True)

artifact_col1, artifact_col2 = st.columns(2)
with artifact_col1:
    st.subheader("Saved solar-flux analysis")
    if SOLAR_TREND_IMAGE_PATH.exists():
        st.image(str(SOLAR_TREND_IMAGE_PATH), use_container_width=True)
        st.caption("Project-generated GOES-18 solar X-ray flux trend with a baseline reference.")
    else:
        st.info("The saved solar-flux artifact is not available in this checkout.")

with artifact_col2:
    st.subheader("Explainability artifact")
    if SHAP_IMAGE_PATH.exists():
        st.image(str(SHAP_IMAGE_PATH), use_container_width=True)
        st.caption("Saved SHAP interaction summary from the notebook analysis.")
    else:
        st.info("The saved SHAP artifact is not available in this checkout.")

with st.expander("About this project"):
    st.write(
        "This portfolio project combines time-series forecasting, anomaly detection, and explainable AI in a space-weather analysis workflow. "
        "The notebook contains the exploratory modeling work; this dashboard presents validated telemetry outputs and saved visual artifacts."
    )
    st.write("**Data columns:** `time_tag`, `flux`, and `Is_Anomaly`.")
    st.write("**Operational note:** This interface is for analysis and demonstration, not for safety-critical decisions.")

st.markdown("---")
st.caption("Built by Umer Sajid · MS Data Science · Explainable AI and time-series forecasting portfolio project")
