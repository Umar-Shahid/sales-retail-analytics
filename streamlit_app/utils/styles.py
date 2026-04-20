# ─────────────────────────────────────────────────────────────
# utils/styles.py
# Shared CSS and UI components for all pages
# ─────────────────────────────────────────────────────────────

import streamlit as st


def apply_styles():
    st.markdown("""
    <style>
        .main { background-color: #ffffff; }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #1a3a5c;
        }
        [data-testid="stSidebar"] * {
            color: #ffffff !important;
        }
        [data-testid="stSidebar"] .stSelectbox label,
        [data-testid="stSidebar"] .stSlider label {
            color: #b0c4de !important;
            font-size: 0.85rem;
        }

        /* Make sidebar scrollable without showing scrollbar */
        [data-testid="stSidebar"] > div:first-child {
            overflow-y: auto;
            overflow-x: hidden;
            max-height: 100vh;
            padding-bottom: 2rem;
        }

        /* Reduce spacing between sidebar elements */
        [data-testid="stSidebar"] .stSelectbox {
            margin-bottom: -1rem;
        }
        [data-testid="stSidebar"] .stSlider {
            margin-bottom: -0.5rem;
        }

        /* Metric cards */
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

        [data-testid="stDataFrame"] {
            border: 1px solid #e0e8f0;
            border-radius: 8px;
        }

        #MainMenu { visibility: hidden; }
        footer    { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)


def page_header(icon, title, subtitle):
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #1a3a5c 0%, #2e6da4 100%);
                padding: 1.8rem 2rem; border-radius: 12px; margin-bottom: 1.5rem;'>
        <h1 style='color:#ffffff; border:none; padding:0; font-size:1.7rem;'>
            {icon} {title}
        </h1>
        <p style='color:#b0c4de; font-size:0.9rem; margin:0.3rem 0 0 0;'>
            {subtitle}
        </p>
    </div>
    """, unsafe_allow_html=True)


def sidebar_brand():
    """Compact branding block — used in pages with custom sidebar controls."""
    st.markdown("""
    <div style='text-align:center; padding:0.4rem 0 0.6rem 0;'>
        <h2 style='color:#ffffff; font-size:1.1rem; margin:0;'>
            🛒 Superstore Analytics
        </h2>
        <p style='color:#b0c4de; font-size:0.72rem; margin:2px 0 0 0;'>
            Muhammad Umar Shahid
        </p>
    </div>
    <hr style='border-color:#2e6da4; margin:0.3rem 0 0.6rem 0;'>
    """, unsafe_allow_html=True)


def sidebar_filters(df):
    """Renders compact sidebar filters. Returns segment, region, category."""
    with st.sidebar:
        sidebar_brand()
        st.markdown("""
        <p style='color:#b0c4de; font-size:0.75rem;
                  text-transform:uppercase; letter-spacing:0.1em; margin:0;'>
            🔍 Filters
        </p>
        """, unsafe_allow_html=True)

        segment  = st.selectbox("Segment",
                                 ["All"] + sorted(df['Segment'].unique().tolist()))
        region   = st.selectbox("Region",
                                 ["All"] + sorted(df['Region'].unique().tolist()))
        category = st.selectbox("Category",
                                 ["All"] + sorted(df['Category'].unique().tolist()))

    return segment, region, category