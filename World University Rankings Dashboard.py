# ==========================================================
#        WORLD UNIVERSITY RANKINGS ANALYSIS
# ==========================================================
# Project Title : WORLD UNIVERSITY RANKINGS DASHBOARD
#
# Student Name : Hassan Abbas
# Batch        : 315
#
# Technology Used:
# • Python
# • Pandas
# • Plotly
# • Streamlit
#
# Dashboard Name:
# WORLD UNIVERSITY RANKINGS DASHBOARD (Interactive - Plotly Edition)
#
# Developed By:
# Your Name
#
# Description:
# This dashboard analyzes the cleaned 2018-2019 world university
# rankings dataset. It provides interactive KPIs, filters, charts,
# ranking analysis, quality-metric insights, country comparisons,
# and a "Global Competitiveness" health-check (analogous to a
# ratio/decision panel) with automated Elite / Strong / Developing
# verdicts. All charts are fully interactive (hover, zoom, pan)
# using Plotly instead of static Matplotlib charts.
# ==========================================================


# ==========================================================
# STEP 1 - IMPORT LIBRARIES
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ==========================================================
# STEP 2 - PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="WORLD UNIVERSITY RANKINGS DASHBOARD",
    page_icon="🎓",
    layout="wide"
)


# ==========================================================
# STEP 3 - AESTHETICS (CUSTOM CSS + COLOR PALETTE)
# ==========================================================

PRIMARY_COLOR = "#2563EB"     # blue accent
PALETTE = px.colors.qualitative.Set2

st.markdown(
    """
    <style>
    /* Overall page padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* KPI metric cards */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-top: 4px solid #2563EB;
        border-radius: 10px;
        padding: 14px 18px 10px 18px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    div[data-testid="stMetricLabel"] {
        font-weight: 600;
        color: #6B7280;
    }
    div[data-testid="stMetricValue"] {
        color: #111827;
    }

    /* Section headers */
    h1, h2, h3 {
        color: #111827;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #F9FAFB;
    }

    /* Verdict badges */
    .ratio-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 700;
        color: white;
    }
    .badge-healthy { background-color: #16A34A; }
    .badge-caution { background-color: #F59E0B; }
    .badge-emerging { background-color: #DC2626; }
    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================================
# STEP 4 - DASHBOARD TITLE
# ==========================================================

st.title("🎓 WORLD UNIVERSITY RANKINGS DASHBOARD")

st.markdown("### Developed By : Hassan Abbas")

st.markdown(
    """
This interactive dashboard presents the 2018-2019 world university
rankings analysis using Python, Pandas, Plotly and Streamlit, along
with a Global Competitiveness health-check that scores countries and
institutions against benchmark thresholds.
"""
)

st.markdown("---")


# ==========================================================
# STEP 5 - LOAD CLEANED DATASET
# ==========================================================

try:

    df = pd.read_csv("cleaned_university_dataset.csv")

    st.success("✅ Clean Dataset Loaded Successfully")

except Exception as e:

    st.error("❌ Unable to Load Dataset")

    st.write(e)

    st.stop()


# ==========================================================
# STEP 6 - DATASET OVERVIEW
# ==========================================================

st.header("📊 Dataset Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Total Rows",
        value=df.shape[0]
    )

with col2:
    st.metric(
        label="Total Columns",
        value=df.shape[1]
    )

with col3:
    st.metric(
        label="Missing Values",
        value=int(df.isnull().sum().sum())
    )

st.markdown("---")


# ==========================================================
# STEP 7 - DATASET PREVIEW
# ==========================================================

st.header("📋 Dataset Preview")

rows = st.slider(
    "Select Number of Rows",
    min_value=5,
    max_value=50,
    value=10
)

st.dataframe(
    df.head(rows),
    use_container_width=True
)

st.markdown("---")


# ==========================================================
# STEP 8 - SIDEBAR FILTER PANEL
# ==========================================================

st.sidebar.title("🔍 Dashboard Filters")

st.sidebar.markdown("Filter the dataset below.")

country_list = sorted(df["location"].dropna().unique())

selected_countries = st.sidebar.multiselect(
    "Select Country",
    options=country_list,
    default=country_list
)

rank_bucket_list = sorted(
    df["rank_category"].dropna().unique(),
    key=lambda x: ["1-10", "11-50", "51-100", "101-500", "501+"].index(x)
)

selected_rank_buckets = st.sidebar.multiselect(
    "Select Rank Category",
    options=rank_bucket_list,
    default=rank_bucket_list
)

score_min, score_max = st.sidebar.slider(
    "Score Range",
    min_value=float(df["score"].min()),
    max_value=float(df["score"].max()),
    value=(float(df["score"].min()), float(df["score"].max()))
)

filtered_df = df[
    df["location"].isin(selected_countries) &
    df["rank_category"].isin(selected_rank_buckets) &
    df["score"].between(score_min, score_max)
]

st.sidebar.markdown("---")
st.sidebar.info(f"Showing **{len(filtered_df)}** of **{len(df)}** universities")


# ==========================================================
# STEP 8B - SIDEBAR: COMPOSITE INDEX TIER THRESHOLDS
# ==========================================================
# The Global Competitiveness Index blends score, citations,
# research output, and faculty quality into one 0-100 number.
# The tier cutoffs (Elite / Globally Competitive / Emerging)
# aren't fixed in the data, so they're adjustable here.
# ==========================================================

st.sidebar.markdown("---")
st.sidebar.title("🎯 Index Tier Thresholds")
st.sidebar.caption(
    "Set the cutoffs used by the Global Competitiveness Index below."
)

elite_threshold = st.sidebar.slider("Elite Tier Threshold", min_value=50, max_value=100, value=85, step=1)
competitive_threshold = st.sidebar.slider("Globally Competitive Threshold", min_value=0, max_value=elite_threshold - 1, value=min(70, elite_threshold - 1), step=1)


# ==========================================================
# STEP 9 - KPI CARDS (SINGLE COMBINED SET)
# ==========================================================

st.header("📈 Rankings Dashboard KPIs")

st.subheader("🎓 Institution KPIs")

col_total_universities, col_countries_represented, col_top_ranked = st.columns(3)

with col_total_universities:
    st.metric("🎓 Total Universities", len(filtered_df))

with col_countries_represented:
    st.metric("🌍 Countries Represented", filtered_df["location"].nunique())

with col_top_ranked:
    top_uni = filtered_df.sort_values("world_rank").iloc[0] if len(filtered_df) else None
    st.metric("🏆 Top Ranked", top_uni["institution"] if top_uni is not None else "N/A")

st.subheader("💯 Score KPIs")

col_average_score, col_highest_score, col_lowest_score = st.columns(3)

with col_average_score:
    st.metric("📊 Average Score", f"{filtered_df['score'].mean():,.1f}" if len(filtered_df) else "N/A")

with col_highest_score:
    st.metric("🔼 Highest Score", f"{filtered_df['score'].max():,.1f}" if len(filtered_df) else "N/A")

with col_lowest_score:
    st.metric("🔽 Lowest Score", f"{filtered_df['score'].min():,.1f}" if len(filtered_df) else "N/A")

st.divider()


# ==========================================================
# STEP 9B - GLOBAL COMPETITIVENESS INDEX
# ==========================================================

st.header("🌍 Global Competitiveness Index")
st.caption(
    "A single 0-100 composite score blending Score (50%), Citation Impact "
    "(20%), Research Output (15%), and Faculty Quality (15%). Ranking-based "
    "inputs are converted so higher always means better before blending."
)


def normalize_rank(rank_series, worst_possible=1001):
    """
    Converts a 'lower is better' rank (1 = best, worst_possible = worst)
    into a 0-100 'higher is better' score, so it can be blended with
    metrics like Score that are already 0-100 and higher-is-better.
    """
    return 100 * (worst_possible - rank_series) / (worst_possible - 1)


def compute_composite_index(data):
    score_component = data["score"]
    citation_component = normalize_rank(data["citations"])
    research_component = normalize_rank(data["research_output"])
    faculty_component = normalize_rank(data["quality_of_faculty"])

    return (
        0.50 * score_component +
        0.20 * citation_component +
        0.15 * research_component +
        0.15 * faculty_component
    ).clip(lower=0, upper=100)


def get_tier(index_value, elite_min, competitive_min):
    if index_value >= elite_min:
        return "Elite Tier", "badge-healthy", "success"
    elif index_value >= competitive_min:
        return "Globally Competitive", "badge-caution", "warning"
    else:
        return "Emerging", "badge-emerging", "error"


if len(filtered_df) > 0:

    filtered_df = filtered_df.copy()
    filtered_df["composite_index"] = compute_composite_index(filtered_df)

    avg_index = filtered_df["composite_index"].mean()
    tier_label, tier_badge_class, tier_alert = get_tier(avg_index, elite_threshold, competitive_threshold)

    idx_col1, idx_col2 = st.columns([1, 2])

    with idx_col1:
        st.metric("Global Competitiveness Index", f"{avg_index:.1f} / 100")
        st.markdown(
            f'<span class="ratio-badge {tier_badge_class}">{tier_label}</span>',
            unsafe_allow_html=True
        )
        st.caption(
            f"Elite ≥ {elite_threshold}  |  Globally Competitive ≥ {competitive_threshold}  |  "
            f"below {competitive_threshold} = Emerging"
        )

    with idx_col2:
        needle_color = {"badge-healthy": "#16A34A", "badge-caution": "#F59E0B", "badge-emerging": "#DC2626"}[tier_badge_class]

        fig_index_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_index,
            number={"font": {"size": 26}},
            title={"text": "Composite Index (Filtered Selection)", "font": {"size": 14}},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": needle_color, "thickness": 0.3},
                "steps": [
                    {"range": [0, competitive_threshold], "color": "#FEE2E2"},
                    {"range": [competitive_threshold, elite_threshold], "color": "#FEF3C7"},
                    {"range": [elite_threshold, 100], "color": "#DCFCE7"},
                ],
            }
        ))
        fig_index_gauge.update_layout(height=230, margin=dict(l=20, r=20, t=40, b=10), template="plotly_white")
        st.plotly_chart(fig_index_gauge, use_container_width=True)

    getattr(st, tier_alert)(
        f"**Overall Verdict: {tier_label}** — composite index of {avg_index:.1f}/100 across "
        f"{len(filtered_df)} filtered universities."
    )

    st.markdown("##### 📊 Composite Index by Country (Top 10)")
    index_by_country = (
        filtered_df.groupby("location")["composite_index"]
        .mean()
        .sort_values(ascending=True)
        .tail(10)
        .reset_index()
    )
    index_by_country.columns = ["country", "composite_index"]

    fig_index_bar = px.bar(
        index_by_country,
        x="composite_index",
        y="country",
        orientation="h",
        title="Average Composite Index by Country (Top 10)",
        color="composite_index",
        color_continuous_scale="RdYlGn",
        range_color=[0, 100],
        template="plotly_white"
    )
    fig_index_bar.update_layout(xaxis_title="Composite Index (0-100)", yaxis_title="", coloraxis_showscale=False)
    st.plotly_chart(fig_index_bar, use_container_width=True)

else:
    st.warning("⚠️ No universities match the current filters — adjust the sidebar filters to see the Competitiveness Index.")

st.divider()


# ==========================================================
# STEP 10 - ALL CHARTS (INTERACTIVE - PLOTLY, TABBED LAYOUT)
# ==========================================================

st.header("📊 Interactive Charts")

tab_top, tab_category, tab_country, tab_heatmap, tab_trend, tab_map = st.tabs(
    [
        "🏆 Top Universities & Countries",
        "📁 Rank Category, Performance & Score",
        "🌍 Country Comparison",
        "🔥 Top Universities & Heatmap",
        "📈 Quality Metric Trends",
        "🗺️ World Map & Highlights",
    ]
)


# ----------------------------------------------------------
# COUNTRY NAME -> ISO-3 CODE MAP (for the choropleth map)
# ----------------------------------------------------------
COUNTRY_ISO3 = {
    "ARGENTINA": "ARG", "AUSTRALIA": "AUS", "AUSTRIA": "AUT", "BELGIUM": "BEL",
    "BRAZIL": "BRA", "BULGARIA": "BGR", "CANADA": "CAN", "CHILE": "CHL",
    "CHINA": "CHN", "COLOMBIA": "COL", "CROATIA": "HRV", "CYPRUS": "CYP",
    "CZECH REPUBLIC": "CZE", "DENMARK": "DNK", "EGYPT": "EGY", "ESTONIA": "EST",
    "FINLAND": "FIN", "FRANCE": "FRA", "GERMANY": "DEU", "GREECE": "GRC",
    "HONG KONG": "HKG", "HUNGARY": "HUN", "ICELAND": "ISL", "INDIA": "IND",
    "IRAN": "IRN", "IRELAND": "IRL", "ISRAEL": "ISR", "ITALY": "ITA",
    "JAPAN": "JPN", "LEBANON": "LBN", "LITHUANIA": "LTU", "MACAU": "MAC",
    "MALAYSIA": "MYS", "MEXICO": "MEX", "NETHERLANDS": "NLD", "NEW ZEALAND": "NZL",
    "NIGERIA": "NGA", "NORWAY": "NOR", "PAKISTAN": "PAK", "POLAND": "POL",
    "PORTUGAL": "PRT", "ROMANIA": "ROU", "RUSSIA": "RUS", "SAUDI ARABIA": "SAU",
    "SERBIA": "SRB", "SINGAPORE": "SGP", "SLOVAK REPUBLIC": "SVK", "SLOVENIA": "SVN",
    "SOUTH AFRICA": "ZAF", "SOUTH KOREA": "KOR", "SPAIN": "ESP", "SWEDEN": "SWE",
    "SWITZERLAND": "CHE", "TAIWAN": "TWN", "THAILAND": "THA", "TUNISIA": "TUN",
    "TURKEY": "TUR", "UGANDA": "UGA", "UNITED KINGDOM": "GBR", "URUGUAY": "URY",
    "USA": "USA",
}


# ----------------------------------------------------------
# TAB 1 - TOP UNIVERSITIES & COUNTRIES
# ----------------------------------------------------------
with tab_top:

    t1_col1, t1_col2 = st.columns(2)

    # Top 10 Universities (Bar Chart)
    with t1_col1:
        top10_df = filtered_df.sort_values("world_rank").head(10)

        fig_top = px.bar(
            top10_df,
            x="institution",
            y="score",
            title="Top 10 Universities",
            color="institution",
            color_discrete_sequence=PALETTE,
            template="plotly_white"
        )
        fig_top.update_layout(xaxis_title="", yaxis_title="Score", showlegend=False, xaxis_tickangle=-30)
        st.plotly_chart(fig_top, use_container_width=True)

    # Countries by University Count (Pie Chart)
    with t1_col2:
        country_counts = (
            filtered_df["location"]
            .value_counts()
            .head(10)
            .reset_index()
        )
        country_counts.columns = ["country", "count"]

        fig_country = px.pie(
            country_counts,
            names="country",
            values="count",
            title="Top Countries by University Count",
            hole=0.4,
            color_discrete_sequence=PALETTE
        )
        fig_country.update_layout(template="plotly_white")
        st.plotly_chart(fig_country, use_container_width=True)


# ----------------------------------------------------------
# TAB 2 - RANK CATEGORY, PERFORMANCE & SCORE
# ----------------------------------------------------------
with tab_category:

    t2_col1, t2_col2, t2_col3 = st.columns(3)

    # Rank Category Distribution (Bar Chart)
    with t2_col1:
        rank_counts = (
            filtered_df["rank_category"]
            .value_counts()
            .reindex(["1-10", "11-50", "51-100", "101-500", "501+"])
            .dropna()
            .reset_index()
        )
        rank_counts.columns = ["rank_category", "count"]

        fig_rank = px.bar(
            rank_counts,
            x="rank_category",
            y="count",
            title="Rank Category Distribution",
            color="count",
            color_continuous_scale="Blues",
            template="plotly_white"
        )
        fig_rank.update_layout(xaxis_title="", yaxis_title="Universities", coloraxis_showscale=False)
        st.plotly_chart(fig_rank, use_container_width=True)

    # Performance Category Breakdown (Donut Chart)
    with t2_col2:
        perf_counts = (
            filtered_df["performance_category"]
            .value_counts()
            .reset_index()
        )
        perf_counts.columns = ["performance_category", "count"]

        fig_perf_donut = px.pie(
            perf_counts,
            names="performance_category",
            values="count",
            title="Performance Category Breakdown",
            hole=0.45,
            color_discrete_sequence=PALETTE
        )
        fig_perf_donut.update_layout(template="plotly_white")
        st.plotly_chart(fig_perf_donut, use_container_width=True)

    # Score by Rank Category (Boxplot)
    with t2_col3:
        fig_box = px.box(
            filtered_df,
            x="rank_category",
            y="score",
            color="rank_category",
            title="Score Spread by Rank Category",
            color_discrete_sequence=PALETTE,
            template="plotly_white",
            category_orders={"rank_category": ["1-10", "11-50", "51-100", "101-500", "501+"]}
        )
        fig_box.update_layout(xaxis_title="", yaxis_title="Score", showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("##### 💯 Score Distribution")
    fig_score_hist = px.histogram(
        filtered_df,
        x="score",
        nbins=20,
        title="Score Distribution",
        color_discrete_sequence=[PRIMARY_COLOR],
        template="plotly_white"
    )
    st.plotly_chart(fig_score_hist, use_container_width=True)


# ----------------------------------------------------------
# TAB 3 - COUNTRY COMPARISON
# ----------------------------------------------------------
with tab_country:

    t3_col1, t3_col2 = st.columns(2)

    # Average Score by Country (Horizontal Bar Chart)
    with t3_col1:
        avg_score_by_country = (
            filtered_df.groupby("location")["score"]
            .mean()
            .sort_values(ascending=True)
            .tail(10)
            .reset_index()
        )
        avg_score_by_country.columns = ["country", "avg_score"]

        fig_hbar = px.bar(
            avg_score_by_country,
            x="avg_score",
            y="country",
            orientation="h",
            title="Average Score by Country (Top 10)",
            color="avg_score",
            color_continuous_scale="Tealgrn",
            template="plotly_white"
        )
        fig_hbar.update_layout(xaxis_title="Average Score", yaxis_title="", coloraxis_showscale=False)
        st.plotly_chart(fig_hbar, use_container_width=True)

    # Country → Rank Category Treemap
    with t3_col2:
        treemap_df = (
            filtered_df
            .groupby(["location", "rank_category"])
            .size()
            .reset_index(name="count")
        )

        fig_treemap = px.treemap(
            treemap_df,
            path=["location", "rank_category"],
            values="count",
            title="University Mix: Country → Rank Category",
            color="count",
            color_continuous_scale="Blues",
            template="plotly_white"
        )
        fig_treemap.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_treemap, use_container_width=True)

    st.markdown("##### 📦 Score Spread by Country")
    top10_countries_box = (
        filtered_df["location"]
        .value_counts()
        .head(10)
        .index
    )

    box_country_df = filtered_df[filtered_df["location"].isin(top10_countries_box)]

    fig_box_country = px.box(
        box_country_df,
        x="location",
        y="score",
        color="location",
        points="outliers",
        title="Score Spread by Country (Top 10 by Count)",
        color_discrete_sequence=PALETTE,
        template="plotly_white"
    )
    fig_box_country.update_layout(
        xaxis_title="",
        yaxis_title="Score",
        showlegend=False,
        xaxis_tickangle=-30
    )
    fig_box_country.update_traces(boxmean=True)
    st.plotly_chart(fig_box_country, use_container_width=True)


# ----------------------------------------------------------
# TAB 4 - TOP UNIVERSITIES & HEATMAP
# ----------------------------------------------------------
with tab_heatmap:

    st.markdown("##### 🏆 Top 10 Universities by Score")

    t4_col1, t4_col2 = st.columns(2)

    with t4_col1:
        top10_score_df = filtered_df.sort_values("score", ascending=False).head(10)

        fig_top_score = px.bar(
            top10_score_df.sort_values("score"),
            x="score",
            y="institution",
            orientation="h",
            title="Top 10 Universities by Score",
            color="score",
            color_continuous_scale="Blues",
            template="plotly_white"
        )
        fig_top_score.update_layout(xaxis_title="Score", yaxis_title="", coloraxis_showscale=False)
        st.plotly_chart(fig_top_score, use_container_width=True)

    with t4_col2:
        metric_cols = [
            "world_rank", "quality_of_education", "alumni_employment",
            "quality_of_faculty", "research_output", "quality_publications",
            "influence", "citations", "score"
        ]
        corr_matrix = filtered_df[metric_cols].corr()

        fig_heatmap = px.imshow(
            corr_matrix,
            text_auto=".2f",
            title="Correlation Between Ranking Metrics",
            color_continuous_scale="RdBu_r",
            zmin=-1, zmax=1,
            template="plotly_white"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)


# ----------------------------------------------------------
# TAB 5 - QUALITY METRIC TRENDS
# ----------------------------------------------------------
with tab_trend:

    # World Rank vs Score (Scatter)
    fig_scatter = px.scatter(
        filtered_df,
        x="world_rank",
        y="score",
        color="rank_category",
        title="World Rank vs Score",
        color_discrete_sequence=PALETTE,
        template="plotly_white",
        opacity=0.75,
        hover_data=["institution", "location"]
    )
    fig_scatter.update_layout(xaxis_title="World Rank", yaxis_title="Score")
    st.plotly_chart(fig_scatter, use_container_width=True)

    # Quality of Faculty vs Research Output (Scatter Chart)
    fig_quality_scatter = px.scatter(
        filtered_df,
        x="research_output",
        y="quality_of_faculty",
        color="rank_category",
        title="Research Output Rank vs Quality of Faculty Rank",
        color_discrete_sequence=PALETTE,
        template="plotly_white",
        opacity=0.75,
        hover_data=["institution", "location"]
    )
    fig_quality_scatter.update_layout(
        xaxis_title="Research Output Rank (lower = better)",
        yaxis_title="Quality of Faculty Rank (lower = better)"
    )
    st.plotly_chart(fig_quality_scatter, use_container_width=True)


# ----------------------------------------------------------
# TAB 6 - WORLD MAP & HIGHLIGHTS
# ----------------------------------------------------------
with tab_map:

    st.markdown("##### 🗺️ Average Score by Country (World Map)")

    map_df = filtered_df.copy()
    map_df["iso3"] = map_df["location"].map(COUNTRY_ISO3)

    country_map_data = (
        map_df.dropna(subset=["iso3"])
        .groupby(["location", "iso3"])
        .agg(avg_score=("score", "mean"), universities=("institution", "count"))
        .reset_index()
    )

    if len(country_map_data) > 0:
        fig_choropleth = px.choropleth(
            country_map_data,
            locations="iso3",
            color="avg_score",
            hover_name="location",
            hover_data={"iso3": False, "avg_score": ":.1f", "universities": True},
            color_continuous_scale="Viridis",
            range_color=[country_map_data["avg_score"].min(), country_map_data["avg_score"].max()],
            title="Average Score by Country",
            template="plotly_white"
        )
        fig_choropleth.update_layout(
            geo=dict(showframe=False, showcoastlines=True, projection_type="natural earth"),
            margin=dict(l=0, r=0, t=40, b=0),
            coloraxis_colorbar=dict(title="Avg Score")
        )
        st.plotly_chart(fig_choropleth, use_container_width=True)
    else:
        st.info("No mappable countries in the current filter selection.")

    map_col1, map_col2 = st.columns(2)

    # Bubble Chart: Score vs Citation Rank, sized by Influence
    with map_col1:
        st.markdown("##### 🫧 Score vs Citation Impact (Bubble Size = Influence)")

        bubble_df = filtered_df.copy()
        # Convert influence rank (lower = better) into a bubble size (higher = bigger bubble)
        bubble_df["influence_strength"] = 1002 - bubble_df["influence"]

        fig_bubble = px.scatter(
            bubble_df,
            x="citations",
            y="score",
            size="influence_strength",
            color="rank_category",
            hover_name="institution",
            hover_data={"location": True, "influence_strength": False},
            title="Score vs Citation Rank (bubble size = Influence strength)",
            color_discrete_sequence=PALETTE,
            template="plotly_white",
            opacity=0.7,
            size_max=32
        )
        fig_bubble.update_layout(
            xaxis_title="Citation Rank (lower = better)",
            yaxis_title="Score"
        )
        st.plotly_chart(fig_bubble, use_container_width=True)

    # Radar Chart: Top 5 Countries across normalized quality metrics
    with map_col2:
        st.markdown("##### 🕸️ Top 5 Countries — Quality Metric Profile")

        radar_metrics = {
            "Score": filtered_df["score"],
            "Faculty Quality": normalize_rank(filtered_df["quality_of_faculty"]),
            "Research Output": normalize_rank(filtered_df["research_output"]),
            "Citations": normalize_rank(filtered_df["citations"]),
            "Influence": normalize_rank(filtered_df["influence"]),
        }
        radar_df = filtered_df[["location"]].copy()
        for metric_name, values in radar_metrics.items():
            radar_df[metric_name] = values

        top5_countries_radar = (
            filtered_df["location"]
            .value_counts()
            .head(5)
            .index
        )

        radar_avg = (
            radar_df[radar_df["location"].isin(top5_countries_radar)]
            .groupby("location")[list(radar_metrics.keys())]
            .mean()
            .reset_index()
        )

        fig_radar = go.Figure()
        categories = list(radar_metrics.keys())

        for i, row in radar_avg.iterrows():
            values = [row[c] for c in categories]
            values.append(values[0])  # close the loop
            fig_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=categories + [categories[0]],
                fill="toself",
                name=row["location"].title(),
                opacity=0.6,
                line_color=PALETTE[i % len(PALETTE)]
            ))

        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            template="plotly_white",
            showlegend=True,
            margin=dict(l=30, r=30, t=20, b=20)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

st.divider()


# ==========================================================
# STEP 11 - TOP & LOWEST UNIVERSITIES
# ==========================================================

col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Top 10 Highest Scoring Universities")
    st.dataframe(
        filtered_df.nlargest(10, "score")[
            ["institution", "location", "world_rank", "score"]
        ],
        use_container_width=True
    )

with col2:
    st.subheader("📉 Top 10 Lowest Scoring Universities")
    st.dataframe(
        filtered_df.nsmallest(10, "score")[
            ["institution", "location", "world_rank", "score"]
        ],
        use_container_width=True
    )


# ==========================================================
# STEP 12 - FILTERED DATASET
# ==========================================================

st.divider()
st.subheader("📄 Filtered Dataset")

st.dataframe(filtered_df, use_container_width=True)


# ==========================================================
# STEP 13 - DOWNLOAD FILTERED DATA
# ==========================================================

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download Filtered Data",
    data=csv,
    file_name="University_Rankings_Filtered_Data.csv",
    mime="text/csv"
)


# ==========================================================
# STEP 14 - RANKINGS SUMMARY
# ==========================================================

st.divider()
st.subheader("📈 Rankings Summary")

if len(filtered_df) > 0:
    summary = pd.DataFrame({
        "Total Universities": [len(filtered_df)],
        "Countries Represented": [filtered_df["location"].nunique()],
        "Average Score": [filtered_df["score"].mean()],
        "Highest Score": [filtered_df["score"].max()],
        "Lowest Score": [filtered_df["score"].min()]
    })

    st.dataframe(summary, use_container_width=True)
else:
    st.info("No data to summarize — adjust filters.")


# ==========================================================
# STEP 15 - BUSINESS INSIGHTS
# ==========================================================

st.divider()
st.subheader("💡 Key Insights")

if len(filtered_df) > 0:
    best_row = filtered_df.sort_values("world_rank").iloc[0]

    st.success(
        f"""
✔ Total Universities Shown : {len(filtered_df)}

✔ Top Ranked University : {best_row['institution']} ({best_row['location']}, Rank #{int(best_row['world_rank'])})

✔ Most Represented Country : {filtered_df['location'].mode()[0]}

✔ Average Score : {filtered_df['score'].mean():,.1f}

✔ Highest Score : {filtered_df['score'].max():,.1f}
"""
    )
else:
    st.info("No universities match the current filters.")


# ==========================================================
# STEP 16 - FOOTER
# ==========================================================

st.divider()

st.markdown(
"""
### 🎓 WORLD UNIVERSITY RANKINGS DASHBOARD

**Developed By:** Hassan Abbas  
**Batch:** 315

Python • Pandas • Plotly • Streamlit • Global Competitiveness Analysis
"""
)
