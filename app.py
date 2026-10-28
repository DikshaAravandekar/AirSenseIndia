"""AirSense India — Air Quality Analytics Dashboard
Run: streamlit run app.py
"""

from pathlib import Path
import re

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# --------------------------------------------------
# 1. Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="AirSense India | Analytics",
    page_icon="🌏",
    layout="wide",
    initial_sidebar_state="collapsed",
)

DATA_URL = (
    "https://huggingface.co/datasets/AkshayKarthick/"
    "india-weather-air-quality/resolve/main/air_quality_daily.csv"
)

# --------------------------------------------------
# 2. Theme colors
# --------------------------------------------------
BG = "#0E1117"
PANEL = "#161B22"
TEXT = "#F3F4F6"
MUTED = "#B0BAC8"
GRID = "#303844"
TEAL = "#20B2AA"
BLUE = "#82C7F5"

# --------------------------------------------------
# 3. Professional styling
# --------------------------------------------------
st.markdown("""
<style>
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2rem;
        max-width: 1450px;
    }

    .hero {
        padding: 1.5rem 1.7rem;
        border-radius: 16px;
        background: linear-gradient(120deg, #102A43, #176B70);
        color: white;
        margin-bottom: 1.5rem;
    }

    .hero h1 {
        color: #FFFFFF;
        font-size: 2.25rem;
        margin-bottom: 0.35rem;
    }

    .hero p {
        color: #D9E7EF;
        margin-bottom: 0;
        font-size: 1rem;
    }

    div[data-testid="stMetric"] {
        background: #141922;
        border: 1px solid #303844;
        padding: 18px;
        border-radius: 12px;
        min-height: 112px;
    }

    div[data-testid="stMetricLabel"] {
        font-size: 0.9rem;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.65rem;
        color: #F3F4F6;
    }

    .section-note {
        color: #B0BAC8;
        font-size: 0.9rem;
    }

    .insight-card {
        background: #141922;
        padding: 1.2rem;
        border-radius: 12px;
        border: 1px solid #303844;
        min-height: 175px;
        height: 100%;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
    }

    .insight-card h4 {
        color: #F3F4F6;
        margin-top: 0;
        margin-bottom: 0.8rem;
        min-height: 2.5rem;
        font-size: 1.05 rem;
    }

    .insight-card h3 {
        color: #5EEAD4;
        margin-top: 0.2rem;
        margin-bottom: 0.6rem;
        font-size: 1.5rem;
    }

    .insight-card p {
        color: #C5CED8;
        margin-bottom: 0;
        line-height: 1.55;
        font-size: 0.92rem;
    }

    div[data-testid="stPyplot"] {
        width: 100%;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #303844;
        border-radius: 10px;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 4. Chart formatting helper
# --------------------------------------------------
def style_chart(fig, ax):
    """Apply a readable dark theme to Matplotlib charts."""

    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    ax.tick_params(
        axis="both",
        colors=TEXT,
        labelsize=9,
        length=4,
    )

    ax.xaxis.label.set_color(TEXT)
    ax.yaxis.label.set_color(TEXT)

    ax.title.set_color(TEXT)
    ax.title.set_fontsize(14)
    ax.title.set_fontweight("bold")

    ax.grid(
        visible=True,
        color=GRID,
        linestyle="-",
        linewidth=0.8,
        alpha=0.85,
    )

    ax.set_axisbelow(True)

    for side in ["top", "right"]:
        ax.spines[side].set_visible(False)

    for side in ["bottom", "left"]:
        ax.spines[side].set_color("#586474")
        ax.spines[side].set_linewidth(0.8)


def style_legend(ax, location="upper left"):
    """Use readable legend text and a dark legend background."""

    legend = ax.legend(
        loc=location,
        frameon=True,
        fontsize=9,
        labelcolor=TEXT,
        facecolor=PANEL,
        edgecolor=GRID,
        framealpha=0.95,
    )

    if legend:
        for label in legend.get_texts():
            label.set_color(TEXT)

    return legend


# --------------------------------------------------
# 5. Load and clean data
# --------------------------------------------------
@st.cache_data(ttl=3600)
def load_data():
    local_path = Path("data/air_quality_daily.csv")

    if local_path.exists():
        data = pd.read_csv(local_path)
    else:
        data = pd.read_csv(DATA_URL)

    required = {"date", "city", "pm2_5_mean"}
    missing = required - set(data.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {', '.join(sorted(missing))}"
        )

    data["date"] = pd.to_datetime(
        data["date"], errors="coerce"
    )

    data["city"] = (
        data["city"].astype("string").str.strip()
    )

    data["pm2_5_mean"] = pd.to_numeric(
        data["pm2_5_mean"], errors="coerce"
    )

    if "pm10_mean" in data.columns:
        data["pm10_mean"] = pd.to_numeric(
            data["pm10_mean"], errors="coerce"
        )

    data = data.dropna(
        subset=["date", "city", "pm2_5_mean"]
    )

    data = data[
        data["date"].ge(pd.Timestamp("2025-01-01"))
        & data["date"].lt(pd.Timestamp("2026-10-29"))
        & data["pm2_5_mean"].ge(0)
    ]

    data = data.drop_duplicates(
        subset=["city", "date"], keep="last"
    )

    if data.empty:
        raise ValueError(
            "No valid records remain after cleaning."
        )

    return data.sort_values(
        ["city", "date"]
    ).reset_index(drop=True)


try:
    df = load_data()
except Exception as exc:
    st.error(f"Unable to load the dataset: {exc}")
    st.info(
        "Check your internet connection or place "
        "air_quality_daily.csv inside the data/ folder."
    )
    st.stop()


# --------------------------------------------------
# 6. Prepare filter options
# --------------------------------------------------
cities = sorted(df["city"].dropna().unique().tolist())

default_city = (
    cities.index("Mumbai") if "Mumbai" in cities else 0
)


# --------------------------------------------------
# 7. Header
# --------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>🌏 AirSense India</h1>
        <p>
            Air Quality Analytics &nbsp;|&nbsp;
            City-level trends, comparisons and insights
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(
    "Explore modelled PM2.5 estimates across Indian cities. "
    "These are CAMS/Open-Meteo-based estimates, not official "
    "CPCB station observations."
)


# --------------------------------------------------
# 8. Horizontal dashboard filters
# --------------------------------------------------
st.markdown("### Dashboard filters")
st.caption("Choose a city and analysis period.")

filter_col1, filter_col2 = st.columns([1, 2])

with filter_col1:
    city = st.selectbox(
        "Select city",
        cities,
        index=default_city,
        key="dashboard_city",
    )

with filter_col2:
    window = st.slider(
        "Recent days",
        min_value=30,
        max_value=365,
        value=150,
        step=30,
        key="dashboard_window",
    )

st.divider()


# --------------------------------------------------
# 9. Prepare selected-city data
# --------------------------------------------------
city_data = (
    df[df["city"].eq(city)]
    .sort_values("date")
    .reset_index(drop=True)
)

g = city_data.tail(window).copy()

if g.empty:
    st.warning(
        "No observations are available for this selection."
    )
    st.stop()

latest = g.iloc[-1]
latest_value = float(latest["pm2_5_mean"])
latest_date = latest["date"]

avg_seven = float(
    g.tail(7)["pm2_5_mean"].mean()
)

if len(g) >= 2:
    previous_value = float(g.iloc[-2]["pm2_5_mean"])
    daily_change = latest_value - previous_value
else:
    daily_change = None


# --------------------------------------------------
# 10. Overview KPI cards
# --------------------------------------------------
st.subheader(f"Air quality overview — {city}")

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Latest PM2.5",
    f"{latest_value:.1f} µg/m³",
    help="Latest available estimated PM2.5 value.",
)

k2.metric(
    "7-observation average",
    f"{avg_seven:.1f} µg/m³",
    help=(
        "Mean of the latest seven available observations. "
        "These may not represent seven consecutive calendar days."
    ),
)

if daily_change is not None:
    k3.metric(
        "Change from previous observation",
        f"{daily_change:+.1f} µg/m³",
        help=(
            "Absolute difference from the previous available "
            "observation. Positive means an increase."
        ),
    )
else:
    k3.metric(
        "Change from previous observation", "N/A"
    )

k4.metric(
    "Latest available date",
    latest_date.strftime("%d %b %Y"),
)

st.caption(
    f"Showing {len(g):,} available observations from "
    f"{g['date'].min():%d %b %Y} to "
    f"{latest_date:%d %b %Y}."
)

st.divider()


# --------------------------------------------------
# 11. Navigation tabs
# --------------------------------------------------
overview_tab, compare_tab, data_tab = st.tabs(
    ["City overview", "City comparison", "Explore data"]
)


# --------------------------------------------------
# TAB 1: Trend and insights
# --------------------------------------------------
with overview_tab:
    st.subheader(f"{city}: PM2.5 trend")

    st.markdown(
        '<p class="section-note">'
        "Daily estimates compared with a seven-observation "
        "rolling average."
        "</p>",
        unsafe_allow_html=True,
    )

    fig, ax = plt.subplots(figsize=(12, 4.8))
    style_chart(fig, ax)

    # Daily estimates
    ax.plot(
        g["date"],
        g["pm2_5_mean"],
        color=BLUE,
        linewidth=1.6,
        alpha=0.85,
        label="Daily estimate",
        zorder=2,
    )

    # Seven-observation moving average
    rolling_average = (
        g["pm2_5_mean"]
        .rolling(7, min_periods=1)
        .mean()
    )

    ax.plot(
        g["date"],
        rolling_average,
        color=TEAL,
        linewidth=2.8,
        label="7-observation average",
        zorder=3,
    )

    ax.set_ylabel("PM2.5 (µg/m³)")
    ax.set_xlabel("Date")

    ax.xaxis.set_major_formatter(
        mdates.DateFormatter("%b %Y")
    )

    ax.xaxis.set_major_locator(
        mdates.AutoDateLocator(minticks=5, maxticks=8)
    )

    ax.margins(x=0.02, y=0.12)
    style_legend(ax)

    fig.tight_layout(pad=2.0)

    st.pyplot(
        fig,
        use_container_width=True,
        transparent=False,
    )

    plt.close(fig)

    # ------------------------------
    # Key insights
    # ------------------------------
    st.subheader("Key insights")

    period_mean = float(g["pm2_5_mean"].mean())
    peak_idx = g["pm2_5_mean"].idxmax()
    peak_row = g.loc[peak_idx]

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            '<div class="insight-card">'
            "<h4>📊 Period average</h4>"
            f"<h3>{period_mean:.1f} µg/m³</h3>"
            "<p>Mean estimated PM2.5 for the selected period.</p>"
            "</div>",
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            '<div class="insight-card">'
            "<h4>🔎 Highest observation</h4>"
            f"<h3>{peak_row['pm2_5_mean']:.1f} µg/m³</h3>"
            f"<p>Recorded on {peak_row['date']:%d %b %Y} "
            "within the selected period.</p>"
            "</div>",
            unsafe_allow_html=True,
        )

    with c3:
        if daily_change is not None:
            if daily_change > 0:
                change_text = "Increased"
            elif daily_change < 0:
                change_text = "Decreased"
            else:
                change_text = "Unchanged"

            detail = (
                f"{change_text} by {abs(daily_change):.1f} µg/m³ "
                "versus the previous observation."
            )
        else:
            detail = (
                "Not enough observations to calculate a change."
            )

        st.markdown(
            '<div class="insight-card">'
            "<h4>↕️ Recent movement</h4>"
            f"<h3>{'+' if daily_change is not None and daily_change > 0 else ''}"
            f"{daily_change:.1f} µg/m³</h3>"
            f"<p>{detail}</p>"
            "</div>",
            unsafe_allow_html=True,
        )

    st.caption(
        "These insights describe the selected dataset and period. "
        "They do not establish causes or health outcomes."
    )


# --------------------------------------------------
# TAB 2: Compare cities
# --------------------------------------------------
with compare_tab:
    st.subheader(
        "Top 12 Cities by Average PM2.5 Concentration"
    )

    st.caption(
        "Indian cities ranked by mean estimated PM2.5 levels "
        "from 1 January 2025 onward (µg/m³)."
    )

    ranking = (
        df.groupby("city")["pm2_5_mean"]
        .mean()
        .sort_values(ascending=False)
        .head(12)
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(12, 6.5))
    style_chart(fig, ax)

    bars = ax.barh(
        ranking.index,
        ranking.values,
        color=TEAL,
        height=0.68,
        edgecolor="#8CE5DC",
        linewidth=0.4,
        zorder=3,
    )

    ax.set_xlabel("Mean PM2.5 (µg/m³)")
    ax.set_ylabel("")

    # Make room for value labels at the end of each bar.
    max_value = float(ranking.max())
    ax.set_xlim(0, max_value * 1.15)

    for bar, value in zip(bars, ranking.values):
        ax.text(
            value + max_value * 0.012,
            bar.get_y() + bar.get_height() / 2,
            f"{value:.1f}",
            va="center",
            ha="left",
            fontsize=9,
            fontweight="bold",
            color=TEXT,
        )

    ax.tick_params(
        axis="y",
        colors=TEXT,
        labelsize=10,
    )

    ax.tick_params(
        axis="x",
        colors=MUTED,
        labelsize=9,
    )

    ax.grid(
        axis="x",
        color=GRID,
        linestyle="-",
        linewidth=0.8,
        alpha=0.85,
    )

    ax.grid(axis="y", visible=False)
    ax.set_axisbelow(True)

    fig.tight_layout(pad=2.0)

    st.pyplot(
        fig,
        use_container_width=True,
        transparent=False,
    )

    plt.close(fig)

    st.caption(
        "Ranking period: all valid records in the loaded dataset "
        "from 1 January 2025 through 28 October 2026, "
        "subject to data availability. Only the 12 highest-mean "
        "cities are displayed; the selected city may not appear "
        "if it is outside the top 12."
    )

    with st.expander("View city ranking table"):
        rank_table = (
            df.groupby("city")
            .agg(
                Mean_PM25=("pm2_5_mean", "mean"),
                Observations=("pm2_5_mean", "count"),
            )
            .sort_values("Mean_PM25", ascending=False)
            .reset_index()
        )

        rank_table["Mean_PM25"] = (
            rank_table["Mean_PM25"].round(2)
        )

        st.dataframe(
            rank_table.rename(
                columns={
                    "city": "City",
                    "Mean_PM25": "Mean PM2.5 (µg/m³)",
                    "Observations": "Available observations",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )


# --------------------------------------------------
# TAB 3: Data explorer and download
# --------------------------------------------------
with data_tab:
    st.subheader("Explore selected-city data")

    st.write(
        "Preview the most recent observations or download "
        "the selected city's available records."
    )

    display_columns = [
        col
        for col in [
            "date",
            "city",
            "pm2_5_mean",
            "pm10_mean",
        ]
        if col in g.columns
    ]

    preview = g[display_columns].tail(20).copy()

    preview = preview.rename(
        columns={
            "date": "Date",
            "city": "City",
            "pm2_5_mean": "Mean PM2.5 (µg/m³)",
            "pm10_mean": "Mean PM10 (µg/m³)",
        }
    )

    preview["Date"] = preview["Date"].dt.strftime(
        "%d %b %Y"
    )

    st.dataframe(
        preview,
        use_container_width=True,
        hide_index=True,
    )

    safe_city = re.sub(
        r"[^a-z0-9]+",
        "_",
        city.lower(),
    ).strip("_")

    st.download_button(
        label=f"⬇️ Download {city} data (CSV)",
        data=g.to_csv(index=False).encode("utf-8"),
        file_name=f"{safe_city}_air_quality.csv",
        mime="text/csv",
    )

# --------------------------------------------------
# 12. Footer
# --------------------------------------------------
st.divider()

st.caption(
    "Source: AkshayKarthick — India Daily Weather & Air Quality. "
    "Data are modelled CAMS/Open-Meteo estimates, not official "
    "CPCB station observations. Recent records may be provisional. "
    "The PM2.5 values shown are not the official full CPCB AQI."
)
