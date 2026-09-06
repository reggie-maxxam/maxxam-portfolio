"""
FRED (Federal Reserve Economic Data) client
Pulls live series when FRED_API_KEY is configured; falls back to a clearly
labeled synthetic demo series otherwise, so the dashboard is runnable
out of the box before a key is added.
"""

import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# Curated indicator set, keyed by FRED series ID, grouped by category.
# "primary": True marks the series shown for its category in the Key Indicators overview.
INDICATORS = {
    "GDPC1": {"label": "Real GDP", "units": "Billions of Chained 2017 Dollars", "format": "billions",
              "category": "Economic Growth", "primary": True},
    "UNRATE": {"label": "Unemployment Rate", "units": "Percent", "format": "percent",
               "category": "Employment", "primary": True},
    "CPIAUCSL": {"label": "CPI (Inflation)", "units": "Index 1982-1984=100", "format": "index",
                 "category": "Inflation", "primary": True},
    "FEDFUNDS": {"label": "Federal Funds Rate", "units": "Percent", "format": "percent",
                 "category": "Interest Rates", "primary": True},
    "DGS10": {"label": "10-Year Treasury Yield", "units": "Percent", "format": "percent",
              "category": "Interest Rates", "primary": False},
    "TB3MS": {"label": "3-Month Treasury Rate", "units": "Percent", "format": "percent",
              "category": "Interest Rates", "primary": False},
    "HOUST": {"label": "Housing Starts", "units": "Thousands of Units, Annualized", "format": "thousands",
              "category": "Housing", "primary": True},
    "DTWEXBGS": {"label": "Trade-Weighted Dollar Index", "units": "Index Jan 2006=100", "format": "index",
                 "category": "Exchange Rates", "primary": True},
    "PCE": {"label": "Personal Consumption Expenditures", "units": "Billions of Dollars", "format": "billions",
            "category": "Consumer Spending", "primary": True},
}

# Sidebar nav order, matching the categories in the reference dashboard
CATEGORIES = [
    "Key Indicators", "Inflation", "Employment", "Interest Rates",
    "Economic Growth", "Exchange Rates", "Housing", "Consumer Spending",
]


def indicators_for_category(category: str) -> list:
    """Series IDs to show for a given sidebar category.
    'Key Indicators' returns the primary series from every category."""
    if category == "Key Indicators":
        return [sid for sid, meta in INDICATORS.items() if meta["primary"]]
    return [sid for sid, meta in INDICATORS.items() if meta["category"] == category]


def is_live_mode() -> bool:
    """True if a FRED API key is configured"""
    return bool(os.getenv("FRED_API_KEY"))


def _demo_series(series_id: str, periods: int = 60) -> pd.DataFrame:
    """Deterministic synthetic series used when no API key is configured"""
    rng = np.random.default_rng(seed=abs(hash(series_id)) % (2**32))
    dates = pd.date_range(end=datetime.today().replace(day=1), periods=periods, freq="MS")

    baselines = {
        "GDPC1": 22000, "UNRATE": 4.0, "CPIAUCSL": 300, "FEDFUNDS": 4.5,
        "DGS10": 4.2, "TB3MS": 4.8, "HOUST": 1350, "DTWEXBGS": 122, "PCE": 19500,
    }
    drifts = {
        "GDPC1": 25, "UNRATE": 0.0, "CPIAUCSL": 0.6, "FEDFUNDS": 0.0,
        "DGS10": 0.0, "TB3MS": 0.0, "HOUST": 0.0, "DTWEXBGS": 0.0, "PCE": 30,
    }
    noise_scale = {
        "GDPC1": 40, "UNRATE": 0.15, "CPIAUCSL": 0.3, "FEDFUNDS": 0.1,
        "DGS10": 0.08, "TB3MS": 0.08, "HOUST": 40, "DTWEXBGS": 1.2, "PCE": 60,
    }

    base = baselines.get(series_id, 100)
    drift = drifts.get(series_id, 1)
    noise = noise_scale.get(series_id, 1)

    trend = base + np.arange(periods) * drift
    values = trend + rng.normal(0, noise, periods).cumsum() * 0.2

    if series_id in ("UNRATE", "FEDFUNDS", "DGS10", "TB3MS"):
        values = np.clip(values, 0, None)

    return pd.DataFrame({"date": dates, "value": values})


def get_series(series_id: str, periods: int = 60) -> pd.DataFrame:
    """
    Returns a DataFrame with columns [date, value] for the given FRED series.
    Uses the live FRED API if FRED_API_KEY is set, otherwise synthetic demo data.
    """
    if is_live_mode():
        from fredapi import Fred

        fred = Fred(api_key=os.getenv("FRED_API_KEY"))
        start_date = datetime.today() - timedelta(days=periods * 31)
        raw = fred.get_series(series_id, observation_start=start_date)
        df = raw.reset_index()
        df.columns = ["date", "value"]
        return df.dropna()

    return _demo_series(series_id, periods)


def get_all_indicators(periods: int = 60) -> dict:
    """Returns {series_id: DataFrame} for every indicator in INDICATORS"""
    return {series_id: get_series(series_id, periods) for series_id in INDICATORS}
