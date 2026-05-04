# 🛒 Sales & Retail Analytics — End-to-End Portfolio Project

## Overview
This repository contains a complete retail analytics portfolio built on the Global Superstore dataset. The project includes data cleaning, exploratory data analysis, forecasting, customer behavior modeling, churn prediction, and dashboard deployment.

The solution is designed around:
- 8,286 orders and 35 feature columns
- 4 years of historical sales data
- Python, R, SQL, and dashboard tooling

## 📊 Core Capabilities
- Data engineering and cleaning of the Superstore dataset
- Exploratory and statistical analysis with Python and R
- Sales forecasting using Prophet
- Profit prediction using XGBoost
- Customer churn scoring using LightGBM
- Dashboarding with Streamlit, R Shiny, Power BI, and an Excel dashboard
- Model artifacts and reusable datasets for analytics delivery

## 📁 Repository Contents
- [data/raw/superstore_sales.csv](data/raw/superstore_sales.csv) — original dataset
- [data/processed/superstore_clean.csv](data/processed/superstore_clean.csv) — cleaned sales data
- [data/processed/churn_risk_scores.csv](data/processed/churn_risk_scores.csv) — churn scoring outputs
- [data/processed/prophet_forecast.csv](data/processed/prophet_forecast.csv) — sales forecast dataset
- [data/processed/rfm_segments.csv](data/processed/rfm_segments.csv) — RFM segmentation results
- [database/](database/) — database artifacts and schema support
- [excel-dashboard/](excel-dashboard/) — Excel dashboard files
- [models/lightgbm_churn_model.txt](models/lightgbm_churn_model.txt) — churn model artifact
- [models/xgboost_profit_model.json](models/xgboost_profit_model.json) — profit prediction model artifact
- [notebooks/](notebooks/) — analysis and modeling notebooks
- [sql/](sql/) — SQL analysis and SQLite queries
- [power_bi/](power_bi/) — Power BI dashboard files
- [r_analysis/](r_analysis/) — R analysis and Shiny app
- [spss/](spss/) — SPSS analysis files
- [streamlit_app/](streamlit_app/) — deployed Streamlit analytics app
- [reports/](reports/) — exported deliverables and reports
- [requirements.txt](requirements.txt) — Python package dependencies

## 📚 Notebooks
- [notebooks/00_setup_check.py](notebooks/00_setup_check.py)
- [notebooks/01_data_cleaning.ipynb](notebooks/01_data_cleaning.ipynb)
- [notebooks/02_eda.ipynb](notebooks/02_eda.ipynb)
- [notebooks/02_eda_upload.ipynb](notebooks/02_eda_upload.ipynb)
- [notebooks/03_ml_models.ipynb](notebooks/03_ml_models.ipynb)
- [notebooks/03_ml_models_upload.ipynb](notebooks/03_ml_models_upload.ipynb)
- [notebooks/04_sql_sqlite.ipynb](notebooks/04_sql_sqlite.ipynb)
- [notebooks/05_powerbi.ipynb](notebooks/05_powerbi.ipynb)
- [notebooks/06_spss_analysis.ipynb](notebooks/06_spss_analysis.ipynb)
- [notebooks/08_streamlit_app.ipynb](notebooks/08_streamlit_app.ipynb)

## 🧠 Dashboards and Apps
- Streamlit app: [streamlit_app/app.py](streamlit_app/app.py)
- Streamlit pages:
  - [streamlit_app/pages/01_overview.py](streamlit_app/pages/01_overview.py)
  - [streamlit_app/pages/02_profitability.py](streamlit_app/pages/02_profitability.py)
  - [streamlit_app/pages/03_ml_forecast.py](streamlit_app/pages/03_ml_forecast.py)
  - [streamlit_app/pages/04_ml_predict.py](streamlit_app/pages/04_ml_predict.py)
- R Shiny app: [r_analysis/shiny_app/app.R](r_analysis/shiny_app/app.R)
- Power BI assets: [power_bi/](power_bi/)
- Excel dashboard: [excel-dashboard/](excel-dashboard/)

## 🚀 Setup & Run
1. Create or activate your Python environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Launch the Streamlit dashboard:
   ```bash
   streamlit run streamlit_app/app.py
   ```

## 🔧 Notes
- The project uses `Streamlit 1.56.0`, `Prophet 1.3.0`, `XGBoost 3.2.0`, and `LightGBM 4.6.0`.
- SQL analysis and schema design are available in [sql/](sql/).
- R-based visualization and Shiny deployment are available in [r_analysis/](r_analysis/).
- SPSS deliverables are stored in [spss/](spss/).

## 📌 Author
- Muhammad Umar Shahid — [github.com/Umar-Shahid](https://github.com/Umar-Shahid)

## 📄 License
This project can be adapted for analytics portfolio review, dashboard delivery, and retail sales forecasting demonstrations.
