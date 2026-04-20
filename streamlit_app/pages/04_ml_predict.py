# ─────────────────────────────────────────────────────────────
# pages/04_ml_predict.py
# Tab 1 — XGBoost: Profit Prediction (regression)
# Tab 2 — LightGBM: Churn Prediction (classification)
# Both use pre-trained models from models/ directory
# ─────────────────────────────────────────────────────────────

import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import sys, os

from sklearn.model_selection import train_test_split
from sklearn.metrics import (mean_absolute_error, mean_squared_error,
                              r2_score)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_loader import load_data, load_xgb_model, load_xgb_encoders, load_lgb_model
from utils.styles import apply_styles, page_header, sidebar_brand

st.set_page_config(page_title="ML Predict", page_icon="🤖", layout="wide")
apply_styles()

df        = load_data()
xgb_model = load_xgb_model()
encoders  = load_xgb_encoders()
lgb_model = load_lgb_model()

page_header("🤖", "ML Predictions — XGBoost & LightGBM",
            "Profit prediction · Customer churn classification · Feature importance")

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    sidebar_brand()
    st.markdown("""
    <p style='color:#b0c4de; font-size:0.75rem;
              text-transform:uppercase; letter-spacing:0.1em; margin:0;'>
        ⚙️ Model Settings
    </p>
    """, unsafe_allow_html=True)
    test_size       = st.slider("Test Set Size (%)", 10, 40, 20)
    churn_threshold = st.slider("Churn Threshold (days)", 90, 365, 180)

tab1, tab2 = st.tabs(["📦 XGBoost — Profit Prediction",
                       "👥 LightGBM — Churn Prediction"])

# ══════════════════════════════════════════════════════════════
# TAB 1 — XGBoost
# ══════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### 📦 Profit Prediction — XGBoost Regressor")
    st.markdown("Predicts **order-level profit** using the pre-trained XGBoost model from Notebook 03.")

    xgb_features = list(xgb_model.feature_names_in_)
    target       = 'Profit'
    model_df     = df.copy()

    for col, encoder in encoders.items():
        if col in model_df.columns:
            known         = set(encoder.classes_)
            model_df[col] = model_df[col].apply(
                lambda x: x if x in known else encoder.classes_[0]
            )
            model_df[col] = encoder.transform(model_df[col].astype(str))

    available = [f for f in xgb_features if f in model_df.columns]
    model_df  = model_df[available + [target]].dropna()

    X = model_df[available]
    y = model_df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size/100, random_state=42
    )

    y_pred = xgb_model.predict(X_test)
    mae    = mean_absolute_error(y_test, y_pred)
    rmse   = np.sqrt(mean_squared_error(y_test, y_pred))
    r2     = r2_score(y_test, y_pred)

    st.markdown("#### Model Performance")
    c1, c2, c3 = st.columns(3)
    c1.metric("MAE",  f"${mae:,.2f}",  help="Average dollar error")
    c2.metric("RMSE", f"${rmse:,.2f}", help="Penalises large errors")
    c3.metric("R²",   f"{r2:.4f}",     help="1.0 = perfect fit")

    st.markdown("---")

    st.markdown("#### Actual vs Predicted Profit")
    fig1 = px.scatter(
        x=y_test, y=y_pred,
        labels  = {'x':'Actual Profit','y':'Predicted Profit'},
        opacity = 0.4,
        color_discrete_sequence = ["#2e6da4"]
    )
    min_val = float(min(y_test.min(), y_pred.min()))
    max_val = float(max(y_test.max(), y_pred.max()))
    fig1.add_shape(type="line",
                   x0=min_val, y0=min_val, x1=max_val, y1=max_val,
                   line=dict(color="#e15759", dash="dash", width=2))
    fig1.add_annotation(text="Perfect prediction line",
                        x=max_val*0.6, y=max_val*0.7,
                        showarrow=False, font=dict(color="#e15759", size=11))
    fig1.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(gridcolor='#e0e8f0'),
        yaxis=dict(gridcolor='#e0e8f0')
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("---")

    st.markdown("#### Feature Importance")
    importance = pd.DataFrame({
        'Feature'    : available,
        'Importance' : xgb_model.feature_importances_
    }).sort_values('Importance', ascending=True)

    fig2 = px.bar(
        importance, x='Importance', y='Feature',
        orientation = 'h',
        color       = 'Importance',
        color_continuous_scale = ["#4e79a7", "#2e6da4", "#1a3a5c"]
    )
    fig2.update_layout(
        xaxis_title="Importance Score", yaxis_title="",
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(gridcolor='#e0e8f0')
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.info("💡 Pre-trained XGBoost model from `models/xgboost_profit_model.pkl`")

# ══════════════════════════════════════════════════════════════
# TAB 2 — LightGBM
# ══════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### 👥 Customer Churn Prediction — LightGBM Classifier")
    st.markdown(f"Customers inactive for more than **{churn_threshold} days** are labelled as churned.")

    reference_date = df['Order Date'].max() + pd.Timedelta(days=1)

    rfm = df.groupby('Customer ID').agg(
        CustomerName = ('Customer Name', 'first'),
        Recency      = ('Order Date',    lambda x: (reference_date - x.max()).days),
        Frequency    = ('Order ID',      'nunique'),
        Monetary     = ('Sales',         'sum')
    ).reset_index()

    rfm['Churned'] = (rfm['Recency'] > churn_threshold).astype(int)

    customer_features = df.groupby('Customer ID').agg(
        Total_Orders      = ('Order ID',       'nunique'),
        Total_Sales       = ('Sales',          'sum'),
        Total_Quantity    = ('Quantity',        'sum'),
        Total_Profit      = ('Profit',          'sum'),
        Avg_Discount      = ('Discount',        'mean'),
        Avg_Order_Value   = ('Sales',           'mean'),
        Avg_Profit        = ('Profit',          'mean'),
        Unique_Products   = ('Product ID',      'nunique'),
        Unique_Categories = ('Category',        'nunique'),
        Avg_Ship_Days     = ('Ship Days',       'mean'),
        First_Order_Month = ('Order Month',     'min'),
        Last_Order_Month  = ('Order Month',     'max'),
        Preferred_Quarter = ('Order Quarter',   lambda x: x.mode()[0]),
    ).reset_index()

    churn_df = customer_features.merge(
        rfm[['Customer ID','Recency','Frequency','Monetary',
             'Churned','CustomerName']],
        on='Customer ID', how='left'
    )

    churn_feature_cols = [
        'Total_Orders',     'Total_Sales',      'Total_Quantity',
        'Total_Profit',     'Avg_Discount',     'Avg_Order_Value',
        'Avg_Profit',       'Unique_Products',  'Unique_Categories',
        'Avg_Ship_Days',    'First_Order_Month','Last_Order_Month',
        'Preferred_Quarter','Recency',          'Frequency',
        'Monetary'
    ]

    X_churn     = churn_df[churn_feature_cols].dropna()
    churn_proba = lgb_model.predict_proba(X_churn)[:, 1]
    churn_pred  = lgb_model.predict(X_churn)

    def assign_risk_tier(prob):
        if prob >= 0.75:   return '🔴 Critical Risk'
        elif prob >= 0.50: return '🟠 High Risk'
        elif prob >= 0.25: return '🟡 Medium Risk'
        else:              return '🟢 Low Risk'

    results_df = churn_df.iloc[:len(X_churn)][
        ['Customer ID','CustomerName','Recency','Frequency','Monetary']
    ].copy()
    results_df['Churn Probability %'] = (churn_proba * 100).round(1)
    results_df['Churned']             = churn_pred
    results_df['Risk Tier']           = [assign_risk_tier(p) for p in churn_proba]
    results_df = results_df.sort_values(
        'Churn Probability %', ascending=False
    ).reset_index(drop=True)

    # ── KPIs ──────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Customers",    f"{len(results_df):,}")
    c2.metric("Predicted Churners", f"{churn_pred.sum():,}")
    c3.metric("Churn Rate",         f"{churn_pred.mean()*100:.1f}%")
    c4.metric("Avg Churn Prob",     f"{churn_proba.mean()*100:.1f}%")

    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### Customer Risk Distribution")
        risk_counts = results_df['Risk Tier'].value_counts().reset_index()
        risk_counts.columns = ['Risk Tier', 'Count']
        fig3 = px.pie(
            risk_counts, names='Risk Tier', values='Count',
            hole  = 0.45,
            color = 'Risk Tier',
            color_discrete_map = {
                '🟢 Low Risk'      : '#59a14f',
                '🟡 Medium Risk'   : '#f28e2b',
                '🟠 High Risk'     : '#e67e22',
                '🔴 Critical Risk' : '#e15759'
            }
        )
        fig3.update_traces(textposition='inside', textinfo='percent+label')
        fig3.update_layout(showlegend=False, paper_bgcolor="white")
        st.plotly_chart(fig3, use_container_width=True)

    with col_right:
        st.markdown("#### Churn Probability Distribution")
        fig4 = px.histogram(
            x      = churn_proba,
            nbins  = 40,
            labels = {'x': 'Churn Probability'},
            color_discrete_sequence = ["#2e6da4"]
        )
        for threshold, color, label in [
            (0.25, '#f28e2b', 'Medium (0.25)'),
            (0.50, '#e67e22', 'High (0.50)'),
            (0.75, '#e15759', 'Critical (0.75)')
        ]:
            fig4.add_vline(x=threshold, line_dash="dash",
                           line_color=color,
                           annotation_text=label,
                           annotation_position="top")
        fig4.update_layout(
            xaxis_title   = "Churn Probability",
            yaxis_title   = "Number of Customers",
            plot_bgcolor  = "white",
            paper_bgcolor = "white",
            xaxis = dict(gridcolor='#e0e8f0'),
            yaxis = dict(gridcolor='#e0e8f0')
        )
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")

    st.markdown("#### Feature Importance")
    lgb_importance = pd.DataFrame({
        'Feature'    : churn_feature_cols,
        'Importance' : lgb_model.feature_importances_
    }).sort_values('Importance', ascending=True)

    fig5 = px.bar(
        lgb_importance, x='Importance', y='Feature',
        orientation = 'h',
        color       = 'Importance',
        color_continuous_scale = ["#4e79a7", "#2e6da4", "#1a3a5c"]
    )
    fig5.update_layout(
        xaxis_title="Importance Score", yaxis_title="",
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(gridcolor='#e0e8f0')
    )
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("---")

    st.markdown("#### 🔴 Top 20 Highest Risk Customers")
    st.dataframe(
        results_df[['Customer ID','CustomerName','Recency',
                    'Frequency','Monetary','Churn Probability %','Risk Tier']]
        .head(20),
        use_container_width=True
    )
    st.info(f"💡 Pre-trained LightGBM model from `models/lightgbm_churn_model.pkl` — "
            f"Churn threshold: {churn_threshold} days.")