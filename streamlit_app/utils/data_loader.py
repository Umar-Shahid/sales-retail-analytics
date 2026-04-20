# ─────────────────────────────────────────────────────────────
# utils/data_loader.py
# Shared data loading + model loading for all pages
# ─────────────────────────────────────────────────────────────

import pandas as pd
import streamlit as st
import pickle
import os

# ── Path helpers ──────────────────────────────────────────────
def get_project_root():
    """Returns absolute path to project root (sales-retail-analytics/)"""
    return os.path.dirname(
               os.path.dirname(
                   os.path.dirname(
                       os.path.abspath(__file__)
                   )
               )
           )

def get_path(*parts):
    """Builds an absolute path from project root. Usage: get_path('models', 'file.pkl')"""
    return os.path.join(get_project_root(), *parts)


# ── Data loader ───────────────────────────────────────────────
@st.cache_data
def load_data():
    """
    Loads and returns the cleaned Global Superstore dataset.
    @st.cache_data caches after first load — CSV is never read twice.
    """
    path = get_path("data", "processed", "superstore_clean.csv")
    print(f"Loading data from: {path}")

    df = pd.read_csv(path)

    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date']  = pd.to_datetime(df['Ship Date'])

    cat_cols = ['Segment', 'Region', 'Category', 'Sub-Category',
                'Ship Mode', 'Profit Tier', 'Sales Segment',
                'Ship Speed', 'Season']
    for col in cat_cols:
        if col in df.columns:
            df[col] = df[col].astype(str)

    return df


# ── Model loaders ─────────────────────────────────────────────
@st.cache_resource
def load_xgb_model():
    """
    Loads the saved XGBoost profit prediction model.
    @st.cache_resource caches the model object itself in memory —
    unlike cache_data which is for data/dataframes.
    """
    path = get_path("models", "xgboost_profit_model.pkl")
    with open(path, 'rb') as f:
        return pickle.load(f)


@st.cache_resource
def load_xgb_encoders():
    """
    Loads the saved LabelEncoders used during XGBoost training.
    Must use same encoders as training — otherwise predictions are wrong.
    """
    path = get_path("models", "xgb_encoders.pkl")
    with open(path, 'rb') as f:
        return pickle.load(f)


@st.cache_resource
def load_lgb_model():
    """
    Loads the saved LightGBM churn classifier.
    Predicts binary churn (0 = retained, 1 = churned) from RFM features.
    """
    path = get_path("models", "lightgbm_churn_model.pkl")
    with open(path, 'rb') as f:
        return pickle.load(f)


@st.cache_resource
def load_prophet_model():
    """
    Loads the saved Prophet forecasting model.
    Already trained on historical monthly sales — no retraining needed.
    """
    path = get_path("models", "prophet_model.pkl")
    with open(path, 'rb') as f:
        return pickle.load(f)


# ── Filter helper ─────────────────────────────────────────────
def filter_data(df, segment="All", region="All", category="All"):
    """
    Applies sidebar filters to dataframe.
    Returns filtered copy — never modifies the original cached dataframe.
    """
    d = df.copy()
    if segment  != "All": d = d[d['Segment']  == segment]
    if region   != "All": d = d[d['Region']   == region]
    if category != "All": d = d[d['Category'] == category]
    return d