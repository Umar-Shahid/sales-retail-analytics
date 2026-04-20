# ─────────────────────────────────────────────────────────────
# pages/01_overview.py — Sales Overview
# ─────────────────────────────────────────────────────────────

import streamlit as st
import plotly.express as px
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_loader import load_data, filter_data
from utils.styles import apply_styles, page_header, sidebar_filters

st.set_page_config(page_title="Overview", page_icon="📊", layout="wide")
apply_styles()

df                        = load_data()
segment, region, category = sidebar_filters(df)
filtered                  = filter_data(df, segment, region, category)

page_header("📊", "Sales Overview",
            "KPI metrics · Sales trends · Category & region breakdowns")

# ── KPIs ──────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Orders",      f"{len(filtered):,}")
col2.metric("Total Sales",       f"${filtered['Sales'].sum():,.0f}")
col3.metric("Total Profit",      f"${filtered['Profit'].sum():,.0f}")
col4.metric("Avg Profit Margin", f"{filtered['Profit Margin %'].mean():.1f}%")

st.markdown("---")

# ── Chart 1: Monthly Sales Trend ──────────────────────────────
st.subheader("📅 Monthly Sales Trend")

monthly = (
    filtered
    .groupby(filtered['Order Date'].dt.to_period('M').astype(str))['Sales']
    .sum().reset_index()
)
monthly.columns = ['Month', 'Sales']

fig1 = px.area(
    monthly, x='Month', y='Sales',
    color_discrete_sequence = ["#2e6da4"]
)
fig1.update_traces(fill='tozeroy', fillcolor='rgba(46,109,164,0.15)')
fig1.update_layout(
    xaxis_title   = "",
    yaxis_title   = "Sales (USD)",
    xaxis_tickangle = -45,
    hovermode     = "x unified",
    plot_bgcolor  = "white",
    paper_bgcolor = "white",
    yaxis = dict(gridcolor='#e0e8f0'),
    xaxis = dict(gridcolor='#e0e8f0')
)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# ── Charts 2 & 3 ──────────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🏷️ Sales by Category")
    cat_data = (
        filtered.groupby('Category')['Sales']
        .sum().reset_index()
        .sort_values('Sales', ascending=True)
    )
    fig2 = px.bar(
        cat_data, x='Sales', y='Category',
        orientation = 'h',
        color       = 'Category',
        color_discrete_map = {
            "Furniture"       : "#4e79a7",
            "Office Supplies" : "#f28e2b",
            "Technology"      : "#59a14f"
        },
        text = 'Sales'
    )
    fig2.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    fig2.update_layout(
        showlegend    = False,
        xaxis_title   = "Sales (USD)",
        yaxis_title   = "",
        plot_bgcolor  = "white",
        paper_bgcolor = "white",
        xaxis = dict(gridcolor='#e0e8f0')
    )
    st.plotly_chart(fig2, use_container_width=True)

with col_right:
    st.subheader("🌍 Sales by Region")
    reg_data = (
        filtered.groupby('Region')['Sales']
        .sum().reset_index()
        .sort_values('Sales', ascending=False)
    )
    fig3 = px.bar(
        reg_data, x='Region', y='Sales',
        color  = 'Region',
        color_discrete_map = {
            "Central" : "#4e79a7",
            "East"    : "#59a14f",
            "South"   : "#f28e2b",
            "West"    : "#e15759"
        },
        text = 'Sales'
    )
    fig3.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    fig3.update_layout(
        showlegend    = False,
        xaxis_title   = "",
        yaxis_title   = "Sales (USD)",
        plot_bgcolor  = "white",
        paper_bgcolor = "white",
        yaxis = dict(gridcolor='#e0e8f0')
    )
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# ── Chart 4: Sales by Region & Segment ────────────────────────
st.subheader("👥 Sales by Region and Customer Segment")

seg_data = (
    filtered.groupby(['Region', 'Segment'])['Sales']
    .sum().reset_index()
)
fig4 = px.bar(
    seg_data, x='Region', y='Sales',
    color   = 'Segment',
    barmode = 'group',
    color_discrete_map = {
        "Consumer"    : "#4e79a7",
        "Corporate"   : "#59a14f",
        "Home Office" : "#f28e2b"
    }
)
fig4.update_layout(
    xaxis_title   = "",
    yaxis_title   = "Sales (USD)",
    plot_bgcolor  = "white",
    paper_bgcolor = "white",
    yaxis  = dict(gridcolor='#e0e8f0'),
    legend = dict(orientation="h", y=-0.2)
)
st.plotly_chart(fig4, use_container_width=True)