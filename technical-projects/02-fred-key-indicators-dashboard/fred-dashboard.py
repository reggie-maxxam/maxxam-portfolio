"""
Key Economic Indicators Dashboard
A Streamlit dashboard that pulls live data from FRED (Federal Reserve Economic Data)
"""

import plotly.graph_objects as go
import streamlit as st

from fred_client import CATEGORIES, INDICATORS, get_series, indicators_for_category, is_live_mode

st.set_page_config(
    page_title="Key Economic Indicators Dashboard",
    page_icon="🏦",
    layout="wide",
)


def get_theme_css(dark_mode: bool) -> str:
    if dark_mode:
        app_bg, sidebar_bg, text, label = "#0e1117", "#1c1e26", "#fafafa", "#aab0bb"
    else:
        app_bg, sidebar_bg, text, label = "#ffffff", "#f0f2f6", "#1f1f1f", "#666"

    return f"""
    <style>
        .stApp {{
            background-color: {app_bg};
            color: {text};
        }}

        [data-testid="stSidebar"] {{
            background-color: {sidebar_bg};
        }}

        [data-testid="stWidgetLabel"],
        [data-testid="stWidgetLabel"] p,
        [data-testid="stMetricLabel"],
        [data-testid="stMetricLabel"] p,
        [data-testid="stMetricValue"],
        [data-testid="stCaptionContainer"],
        [data-testid="stCaptionContainer"] p,
        [data-testid="stSidebar"] h2,
        label[data-baseweb="radio"],
        label[data-baseweb="radio"] p {{
            color: {text} !important;
        }}

        label[data-baseweb="checkbox"] > div:first-of-type,
        label[data-baseweb="radio"] > div:first-of-type {{
            border: 1px solid {label} !important;
        }}
    </style>
    """


def format_value(value: float, fmt: str) -> str:
    if fmt == "billions":
        return f"${value:,.0f}B"
    if fmt == "percent":
        return f"{value:.2f}%"
    if fmt == "thousands":
        return f"{value:,.0f}K"
    return f"{value:,.1f}"


def create_series_chart(df, label: str, dark_mode: bool) -> go.Figure:
    plot_bg = "#1c1e26" if dark_mode else "white"
    grid_color = "#3d4048" if dark_mode else "#f0f0f0"
    font_color = "#fafafa" if dark_mode else "#1f1f1f"

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["value"],
        mode="lines",
        line=dict(color="#1f77b4", width=3),
    ))
    fig.update_layout(
        title=label,
        plot_bgcolor=plot_bg,
        paper_bgcolor=plot_bg,
        font=dict(color=font_color),
        xaxis=dict(showgrid=True, gridcolor=grid_color),
        yaxis=dict(showgrid=True, gridcolor=grid_color),
        height=320,
        margin=dict(t=50, b=40, l=50, r=30),
    )
    return fig


def render_indicators(series_ids: list, dark_mode: bool):
    cols = st.columns(min(len(series_ids), 4))
    for i, series_id in enumerate(series_ids):
        meta = INDICATORS[series_id]
        df = get_series(series_id)
        latest = df["value"].iloc[-1]
        previous = df["value"].iloc[-2] if len(df) > 1 else latest
        with cols[i % len(cols)]:
            st.metric(
                label=meta["label"],
                value=format_value(latest, meta["format"]),
                delta=format_value(latest - previous, meta["format"]),
            )

    st.markdown("### Trends")
    chart_cols = st.columns(2)
    for i, series_id in enumerate(series_ids):
        meta = INDICATORS[series_id]
        df = get_series(series_id)
        with chart_cols[i % 2]:
            fig = create_series_chart(df, meta["label"], dark_mode)
            st.plotly_chart(fig, use_container_width=True)


def main():
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False

    with st.sidebar:
        st.markdown("## 🏦 FRED Indicators")
        st.caption("Economic Data Dashboard")
        category = st.radio("Category", CATEGORIES, label_visibility="collapsed")
        st.markdown("---")
        st.caption("Data provided by Federal Reserve Economic Data (FRED)")

    header_col, toggle_col = st.columns([5, 1])
    with header_col:
        st.title("📊 Economic Indicators Dashboard")
        st.caption("Real-time economic data from the Federal Reserve Economic Data (FRED) system")
    with toggle_col:
        st.toggle("🌙 Dark Mode", key="dark_mode")

    st.markdown(get_theme_css(st.session_state.dark_mode), unsafe_allow_html=True)

    if not is_live_mode():
        st.warning(
            "**Demo mode** — no `FRED_API_KEY` found, showing synthetic placeholder data. "
            "Add your free key to `.env` to pull real FRED data. See README for setup.",
            icon="⚠️",
        )

    st.markdown(f"#### {category}")
    render_indicators(indicators_for_category(category), st.session_state.dark_mode)


if __name__ == "__main__":
    main()
