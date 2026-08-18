from pathlib import Path

import pandas as pd
import pytest

from dashboard_utils import compute_kpis, filter_telemetry, load_telemetry


def test_load_telemetry_validates_and_normalizes(tmp_path: Path):
    source = tmp_path / "telemetry.csv"
    pd.DataFrame(
        {
            "time_tag": ["2024-01-01 00:00:00", "invalid", "2024-01-01 06:00:00"],
            "flux": [1.0e-6, "bad", 2.0e-6],
            "Is_Anomaly": [0, 1, 1],
        }
    ).to_csv(source, index=False)

    frame = load_telemetry(source)

    assert len(frame) == 2
    assert frame["time_tag"].is_monotonic_increasing
    assert frame["Is_Anomaly"].tolist() == [0, 1]


def test_load_telemetry_rejects_missing_columns(tmp_path: Path):
    source = tmp_path / "bad.csv"
    pd.DataFrame({"time_tag": ["2024-01-01"], "flux": [1.0]}).to_csv(source, index=False)

    with pytest.raises(ValueError, match="missing required columns"):
        load_telemetry(source)


def test_filter_and_kpis_are_date_aware():
    frame = pd.DataFrame(
        {
            "time_tag": pd.to_datetime(["2024-01-01 00:00", "2024-01-02 12:00", "2024-01-03 00:00"]),
            "flux": [1.0e-6, 9.0e-6, 3.0e-6],
            "Is_Anomaly": [0, 1, 0],
        }
    )

    filtered = filter_telemetry(frame, "2024-01-02", "2024-01-02")
    kpis = compute_kpis(filtered)

    assert len(filtered) == 1
    assert kpis["peak_flux"] == 9.0e-6
    assert kpis["anomalies"] == 1
    assert kpis["latest_time"] == pd.Timestamp("2024-01-02 12:00")


def test_empty_kpis_are_safe():
    empty = pd.DataFrame(columns=["time_tag", "flux", "Is_Anomaly"])
    result = compute_kpis(empty)

    assert result["observations"] == 0
    assert result["peak_flux"] == 0.0
    assert result["anomalies"] == 0
    assert pd.isna(result["latest_time"])
