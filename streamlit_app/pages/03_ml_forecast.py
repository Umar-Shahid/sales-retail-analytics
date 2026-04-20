# ─────────────────────────────────────────────────────────────
# pages/03_ml_forecast.py — Prophet Sales Forecasting
# Uses pre-trained model from models/prophet_model.pkl
# ─────────────────────────────────────────────────────────────

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_loader import load_data, load_prophet_model
from utils.styles import apply_styles, page_header, sidebar_brand

st.set_page_config(page_title="ML Forecast", page_icon="📈", layout="wide")
apply_styles()

df            = load_data()
prophet_model = load_prophet_model()

page_header("📈", "Sales Forecasting — Prophet",
            "Pre-trained time-series model · Trend & seasonality decomposition")

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    sidebar_brand()
    st.markdown("""
    <p style='color:#b0c4de; font-size:0.75rem;
              text-transform:uppercase; letter-spacing:0.1em; margin:0;'>
        ⚙️ Forecast Settings
    </p>
    """, unsafe_allow_html=True)
    periods  = st.slider("Forecast Horizon (months)", 3, 24, 12)
    category = st.selectbox("Filter by Category",
                             ["All"] + sorted(df['Category'].unique().tolist()))

# ── Prepare historical data ───────────────────────────────────
plot_df = df.copy()
if category != "All":
    plot_df = plot_df[plot_df['Category'] == category]

monthly = (
    plot_df
    .groupby(plot_df['Order Date'].dt.to_period('M').dt.to_timestamp())['Sales']
    .sum().reset_index()
)
monthly.columns = ['ds', 'y']

# ── KPIs ──────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
col1.metric("Historical Months", f"{len(monthly)}")
col2.metric("Forecast Horizon",  f"{periods} months")
col3.metric("Category Filter",   category)

st.markdown("---")

# ── Generate forecast ─────────────────────────────────────────
st.subheader(f"📅 Sales Forecast — Next {periods} Months")

with st.spinner("⏳ Generating forecast..."):
    future   = prophet_model.make_future_dataframe(periods=periods, freq='MS')
    forecast = prophet_model.predict(future)

forecast_only = forecast[forecast['ds'] > monthly['ds'].max()]

# ── Chart ─────────────────────────────────────────────────────
fig = go.Figure()

fig.add_trace(go.Scatter(
    x    = monthly['ds'], y = monthly['y'],
    name = "Actual Sales",
    mode = "lines+markers",
    line = dict(color="#2e6da4", width=2),
    marker = dict(size=4)
))

fig.add_trace(go.Scatter(
    x    = forecast_only['ds'], y = forecast_only['yhat'],
    name = "Forecast",
    mode = "lines",
    line = dict(color="#e15759", width=2, dash="dash")
))

fig.add_trace(go.Scatter(
    x         = pd.concat([forecast_only['ds'], forecast_only['ds'][::-1]]),
    y         = pd.concat([forecast_only['yhat_upper'],
                           forecast_only['yhat_lower'][::-1]]),
    fill      = "toself",
    fillcolor = "rgba(225,87,89,0.1)",
    line      = dict(color="rgba(255,255,255,0)"),
    name      = "Confidence Interval"
))

fig.update_layout(
    xaxis_title   = "",
    yaxis_title   = "Sales (USD)",
    hovermode     = "x unified",
    plot_bgcolor  = "white",
    paper_bgcolor = "white",
    yaxis  = dict(gridcolor='#e0e8f0'),
    xaxis  = dict(gridcolor='#e0e8f0'),
    legend = dict(orientation="h", y=-0.2)
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ── Components ────────────────────────────────────────────────
st.subheader("🔍 Forecast Components")
st.markdown("Breaks down the forecast into **trend** and **yearly seasonality** components.")
fig2 = prophet_model.plot_components(forecast)
st.pyplot(fig2)

st.markdown("---")

# ── Forecast table ────────────────────────────────────────────
st.subheader("📋 Forecast Values Table")

forecast_table         = forecast_only[['ds','yhat','yhat_lower','yhat_upper']].copy()
forecast_table.columns = ['Month','Forecast','Lower Bound','Upper Bound']
forecast_table['Month'] = forecast_table['Month'].dt.strftime('%b %Y')
for col in ['Forecast','Lower Bound','Upper Bound']:
    forecast_table[col] = forecast_table[col].map('${:,.0f}'.format)

st.dataframe(forecast_table, use_container_width=True)
st.info("💡 Pre-trained Prophet model loaded from `models/prophet_model.pkl` — "
        "no retraining happens here.")