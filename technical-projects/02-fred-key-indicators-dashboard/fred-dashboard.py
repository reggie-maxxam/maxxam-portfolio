"""
Key Economic Indicators Dashboard
A Streamlit dashboard that pulls live data from FRED (Federal Reserve Economic Data)
"""

import plotly.graph_objects as go
import streamlit as st

from fred_client import INDICATORS, get_all_indicators, is_live_mode

st.set_page_config(
    page_title="Key Economic Indicators Dashboard",
    page_icon="🏦",
    layout="wide",
)


def format_value(value: float, fmt: str) -> str:
    if fmt == "billions":
        return f"${value:,.0f}B"
    if fmt == "percent":
        return f"{value:.2f}%"
    return f"{value:,.1f}"


def create_series_chart(df, label: str) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["value"],
        mode="lines",
        line=dict(color="#1f77b4", width=3),
    ))
    fig.update_layout(
        title=label,
        plot_bgcolor="white",
        xaxis=dict(showgrid=True, gridcolor="#f0f0f0"),
        yaxis=dict(showgrid=True, gridcolor="#f0f0f0"),
        height=320,
        margin=dict(t=50, b=40, l=50, r=30),
    )
    return fig


def main():
    st.title("🏦 Key Economic Indicators Dashboard")
    st.caption("Real GDP · Unemployment · CPI · Federal Funds Rate — sourced from FRED")

    if not is_live_mode():
        st.warning(
            "**Demo mode** — no `FRED_API_KEY` found, showing synthetic placeholder data. "
            "Add your free key to `.env` to pull real FRED data. See README for setup.",
            icon="⚠️",
        )

    data = get_all_indicators()

    cols = st.columns(len(INDICATORS))
    for col, (series_id, meta) in zip(cols, INDICATORS.items()):
        df = data[series_id]
        latest = df["value"].iloc[-1]
        previous = df["value"].iloc[-2] if len(df) > 1 else latest
        delta = latest - previous
        with col:
            st.metric(
                label=meta["label"],
                value=format_value(latest, meta["format"]),
                delta=format_value(delta, meta["format"]),
            )

    st.markdown("### Trends")
    chart_cols = st.columns(2)
    for i, (series_id, meta) in enumerate(INDICATORS.items()):
        with chart_cols[i % 2]:
            fig = create_series_chart(data[series_id], meta["label"])
            st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
