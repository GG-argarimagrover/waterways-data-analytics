# Waterways Intelligence Dashboard

Interactive Streamlit dashboard for exploring waterways CSV data.

## Features
- KPI cards and dataset overview
- Interactive feature-class pie and bar charts
- Feature-class/code cross-tabulation
- Data quality and missing-value analysis
- Searchable data explorer and CSV downloads
- Upload CSV from the sidebar

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy
Deploy this repository using Streamlit Community Cloud. Set the main file path to `app.py`.

If `Waterways.csv` is not included in the repository, upload it through the dashboard sidebar. Do not publish datasets unless you have permission to share them.

## Data limitations
Without coordinates or GIS geometry, this dashboard analyses attributes only. It does not calculate waterway length, area, flood risk, or ecological condition.
