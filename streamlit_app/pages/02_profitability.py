# ─────────────────────────────────────────────────────────────
# pages/02_profitability.py — Profitability Analysis
# ─────────────────────────────────────────────────────────────

import streamlit as st
import plotly.express as px
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_loader import load_data, filter_data
from utils.styles import apply_styles, page_header, sidebar_filters

st.set_page_config(page_title="Profitability", page_icon="💰", layout="wide")
apply_styles()

df                        = load_data()
segment, region, category = sidebar_filters(df)
filtered                  = filter_data(df, segment, region, category)

page_header("💰", "Profitability Analysis",
            "Discount impact · Profit margins · Regional & tier breakdown")

# ── KPIs ──────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Profit",       f"${filtered['Profit'].sum():,.0f}")
col2.metric("Avg Profit Margin",  f"{filtered['Profit Margin %'].mean():.1f}%")
col3.metric("Profitable Orders",  f"{filtered['Is Profitable'].sum():,}")
col4.metric("Loss-Making Orders", f"{(filtered['Is Profitable']==0).sum():,}")

st.markdown("---")

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📉 Discount vs Profit Margin %")
    scatter_data = filtered[filtered['Profit Margin %'] > -150]
    fig1 = px.scatter(
        scatter_data,
        x         = 'Discount',
        y         = 'Profit Margin %',
        color     = 'Category',
        opacity   = 0.5,
        trendline = "ols",
        color_discrete_map = {
            "Furniture"       : "#4e79a7",
            "Office Supplies" : "#f28e2b",
            "Technology"      : "#59a14f"
        }
    )
    fig1.update_layout(
        xaxis_tickformat = ".0%",
        plot_bgcolor     = "white",
        paper_bgcolor    = "white",
        xaxis = dict(gridcolor='#e0e8f0'),
        yaxis = dict(gridcolor='#e0e8f0')
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    st.subheader("📦 Profit Distribution by Region")
    fig2 = px.box(
        filtered, x='Region', y='Profit',
        color = 'Region',
        color_discrete_map = {
            "Central" : "#4e79a7",
            "East"    : "#59a14f",
            "South"   : "#f28e2b",
            "West"    : "#e15759"
        }
    )
    fig2.add_hline(y=0, line_dash="dash", line_color="red",
                   annotation_text="Break-even")
    fig2.update_layout(
        showlegend    = False,
        yaxis_title   = "Profit (USD)",
        plot_bgcolor  = "white",
        paper_bgcolor = "white",
        yaxis = dict(gridcolor='#e0e8f0')
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

col_left2, col_right2 = st.columns(2)

with col_left2:
    st.subheader("🎯 Profit Tier Distribution")
    tier_data = filtered['Profit Tier'].value_counts().reset_index()
    tier_data.columns = ['Profit Tier', 'Count']
    fig3 = px.pie(
        tier_data, names='Profit Tier', values='Count',
        hole = 0.45,
        color_discrete_sequence = ["#59a14f", "#2e6da4", "#f28e2b", "#e15759"]
    )
    fig3.update_traces(textposition='inside', textinfo='percent+label')
    fig3.update_layout(showlegend=False, paper_bgcolor="white")
    st.plotly_chart(fig3, use_container_width=True)

with col_right2:
    st.subheader("🏆 Top 10 Sub-Categories by Profit")
    sub_data = (
        filtered.groupby('Sub-Category')['Profit']
        .sum().reset_index()
        .sort_values('Profit', ascending=False)
        .head(10)
    )
    fig4 = px.bar(
        sub_data,
        x           = 'Profit',
        y           = 'Sub-Category',
        orientation = 'h',
        color       = 'Profit',
        color_continuous_scale = ["#e15759", "#f28e2b", "#59a14f"]
    )
    fig4.update_layout(
        xaxis_title   = "Profit (USD)",
        yaxis_title   = "",
        plot_bgcolor  = "white",
        paper_bgcolor = "white",
        xaxis = dict(gridcolor='#e0e8f0')
    )
    st.plotly_chart(fig4, use_container_width=True)