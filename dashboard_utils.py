from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

REQUIRED_COLUMNS = {"time_tag", "flux", "Is_Anomaly"}


def load_telemetry(path: str | Path) -> pd.DataFrame:
    """Load and validate the dashboard telemetry file."""
    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(f"Telemetry file not found: {source.name}")

    frame = pd.read_csv(source)
    missing = REQUIRED_COLUMNS.difference(frame.columns)
    if missing:
        raise ValueError(f"Telemetry file is missing required columns: {sorted(missing)}")

    normalized = frame.copy()
    normalized["time_tag"] = pd.to_datetime(normalized["time_tag"], errors="coerce")
    normalized["flux"] = pd.to_numeric(normalized["flux"], errors="coerce")
    normalized["Is_Anomaly"] = pd.to_numeric(normalized["Is_Anomaly"], errors="coerce").fillna(0).astype(int)
    normalized = normalized.dropna(subset=["time_tag", "flux"]).sort_values("time_tag")
    if normalized.empty:
        raise ValueError("Telemetry file contains no valid time and flux observations")
    return normalized.reset_index(drop=True)


def filter_telemetry(frame: pd.DataFrame, start_date, end_date) -> pd.DataFrame:
    """Filter observations inclusively by calendar date without mutating the source."""
    start = pd.Timestamp(start_date).normalize()
    end = pd.Timestamp(end_date).normalize() + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1)
    return frame.loc[frame["time_tag"].between(start, end)].copy().reset_index(drop=True)


def compute_kpis(frame: pd.DataFrame) -> dict[str, float | int | pd.Timestamp]:
    """Return dashboard KPIs for a validated telemetry frame."""
    if frame.empty:
        return {"observations": 0, "peak_flux": 0.0, "mean_flux": 0.0, "anomalies": 0, "latest_time": pd.NaT}
    return {
        "observations": int(len(frame)),
        "peak_flux": float(frame["flux"].max()),
        "mean_flux": float(frame["flux"].mean()),
        "anomalies": int(frame["Is_Anomaly"].sum()),
        "latest_time": frame["time_tag"].max(),
    }


def build_flux_figure(frame: pd.DataFrame) -> go.Figure:
    """Create the primary flux trend figure with anomaly markers."""
    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=frame["time_tag"],
            y=frame["flux"],
            mode="lines+markers",
            name="X-ray flux",
            line={"color": "#f59e0b", "width": 3},
            marker={"size": 8},
            hovertemplate="%{x|%Y-%m-%d %H:%M}<br>Flux: %{y:.2e}<extra></extra>",
        )
    )
    anomalies = frame[frame["Is_Anomaly"] == 1]
    if not anomalies.empty:
        figure.add_trace(
            go.Scatter(
                x=anomalies["time_tag"],
                y=anomalies["flux"],
                mode="markers",
                name="Flagged anomaly",
                marker={"color": "#dc2626", "size": 13, "symbol": "diamond"},
                hovertemplate="%{x|%Y-%m-%d %H:%M}<br>Anomaly flux: %{y:.2e}<extra></extra>",
            )
        )
    figure.update_layout(
        title="Solar X-ray flux over time",
        xaxis_title="Observation time",
        yaxis_title="Flux (W/m²)",
        hovermode="x unified",
        template="plotly_white",
        height=430,
        legend={"orientation": "h", "y": 1.08, "x": 0},
        margin={"l": 20, "r": 20, "t": 75, "b": 20},
    )
    return figure


def build_anomaly_figure(frame: pd.DataFrame) -> go.Figure:
    """Create a compact anomaly timeline for the selected period."""
    figure = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08, row_heights=[0.75, 0.25])
    figure.add_trace(
        go.Scatter(x=frame["time_tag"], y=frame["flux"], mode="lines", name="Flux", line={"color": "#2563eb"}),
        row=1,
        col=1,
    )
    figure.add_trace(
        go.Bar(
            x=frame["time_tag"],
            y=frame["Is_Anomaly"],
            name="Anomaly flag",
            marker_color="#dc2626",
            hovertemplate="%{x|%Y-%m-%d %H:%M}<br>Flag: %{y}<extra></extra>",
        ),
        row=2,
        col=1,
    )
    figure.update_yaxes(title_text="Flux", row=1, col=1)
    figure.update_yaxes(title_text="Flag", range=[0, 1.2], row=2, col=1)
    figure.update_layout(title="Flux and anomaly timeline", template="plotly_white", height=480, margin={"l": 20, "r": 20, "t": 60, "b": 20})
    return figure
