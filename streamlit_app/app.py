# ─────────────────────────────────────────────────────────────
# app.py — Main Entry Point
# Run with: streamlit run app.py
# ─────────────────────────────────────────────────────────────

import streamlit as st

st.set_page_config(
    page_title            = "Superstore Analytics",
    page_icon             = "🛒",
    layout                = "wide",
    initial_sidebar_state = "expanded"
)

st.markdown("""
<style>
    .main { background-color: #ffffff; }

    [data-testid="stSidebar"] {
        background-color: #1a3a5c;
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        overflow-y: auto;
        overflow-x: hidden;
        max-height: 100vh;
        padding-bottom: 2rem;
    }

    [data-testid="stMetric"] {
        background-color: #f0f4f8;
        border-left: 4px solid #2e6da4;
        border-radius: 8px;
        padding: 16px 20px;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.85rem;
        color: #4a4a4a;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.6rem;
        font-weight: 700;
        color: #1a3a5c;
    }

    h1 {
        color: #1a3a5c;
        font-weight: 700;
        border-bottom: 3px solid #2e6da4;
        padding-bottom: 10px;
    }
    h2, h3 { color: #2e6da4; font-weight: 600; }

    hr {
        border: none;
        border-top: 1px solid #e0e8f0;
        margin: 1.5rem 0;
    }

    #MainMenu { visibility: hidden; }
    footer    { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:0.4rem 0 0.6rem 0;'>
        <h2 style='color:#ffffff; font-size:1.1rem; margin:0;'>
            🛒 Superstore Analytics
        </h2>
        <p style='color:#b0c4de; font-size:0.72rem; margin:2px 0 0 0;'>
            Muhammad Umar Shahid
        </p>
        <p style='color:#7eb3d8; font-size:0.70rem; margin:2px 0 0 0;'>
            <a href='https://github.com/Umar-Shahid'
               style='color:#7eb3d8;'>github.com/Umar-Shahid</a>
        </p>
    </div>
    <hr style='border-color:#2e6da4; margin:0.3rem 0 0.6rem 0;'>
    """, unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────
st.markdown("""
<div style='background: linear-gradient(135deg, #1a3a5c 0%, #2e6da4 100%);
            padding: 2.5rem 2rem; border-radius: 12px; margin-bottom: 2rem;'>
    <h1 style='color:#ffffff; border:none; padding:0; font-size:2rem;'>
        🛒 Global Superstore Analytics
    </h1>
    <p style='color:#b0c4de; font-size:1rem; margin-top:0.5rem;'>
        End-to-end Sales & Retail Analytics Portfolio —
        8,286 orders · 35 features · 4 years of data
    </p>
</div>
""", unsafe_allow_html=True)

# ── Page cards ────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

cards = [
    ("📊", "Overview",       "KPIs, sales trends, category & region breakdowns",         "#2e6da4"),
    ("💰", "Profitability",  "Discount impact, profit margins, regional analysis",        "#27ae60"),
    ("📈", "ML Forecast",    "Prophet time-series forecasting for future sales",          "#e67e22"),
    ("🤖", "ML Predict",     "XGBoost profit prediction + LightGBM churn scoring",        "#8e44ad"),
]

for col, (icon, title, desc, color) in zip([col1, col2, col3, col4], cards):
    col.markdown(f"""
    <div style='background:#f0f4f8; border-top: 4px solid {color};
                border-radius:10px; padding:1.2rem; height:160px;'>
        <div style='font-size:1.8rem;'>{icon}</div>
        <div style='font-weight:700; color:#1a3a5c; margin:0.4rem 0;'>{title}</div>
        <div style='font-size:0.82rem; color:#4a4a4a;'>{desc}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Tech stack ────────────────────────────────────────────────
st.markdown("### 🛠️ Tech Stack")

tech_cols = st.columns(6)
tools = [
    ("🐍", "Python 3.11"),
    ("📊", "Streamlit"),
    ("📉", "Plotly"),
    ("🔮", "Prophet"),
    ("⚡", "XGBoost"),
    ("💡", "LightGBM"),
]
for col, (icon, name) in zip(tech_cols, tools):
    col.markdown(f"""
    <div style='background:#f0f4f8; border-radius:8px; padding:0.8rem;
                text-align:center; border:1px solid #e0e8f0;'>
        <div style='font-size:1.4rem;'>{icon}</div>
        <div style='font-size:0.8rem; font-weight:600; color:#1a3a5c;'>{name}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.info("👈 Use the sidebar to navigate between pages.")