import pandas as pd
import numpy as np
import matplotlib
import seaborn
import plotly
import sklearn
import xgboost
import lightgbm
import streamlit

print("✅ All libraries loaded successfully!")
print(f"pandas     : {pd.__version__}")
print(f"numpy      : {np.__version__}")
print(f"sklearn    : {sklearn.__version__}")
print(f"xgboost    : {xgboost.__version__}")
print(f"lightgbm   : {lightgbm.__version__}")

df = pd.read_csv('data/raw/superstore_sales.csv', encoding='latin-1')
print(f"\n✅ Dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns")
print(df.head(3))