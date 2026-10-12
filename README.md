# Waterways Intelligence Studio

A river-inspired Streamlit dashboard for exploring waterways CSV attributes.

## Included
- River/glacier visual theme with high-contrast readable text
- KPI overview and feature-class charts
- Named/unnamed coverage and top-name analysis
- Data quality audit and identifier checks
- Searchable records and CSV downloads
- CSV upload from the sidebar

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy
Deploy on Streamlit Community Cloud with branch `main` and main file path `app.py`.

Upload `Waterways.csv` in the app sidebar unless you have permission to publish it in the repository.

## Limitations
This is attribute-based analytics. Spatial analysis requires valid coordinates or GIS geometry. Feature counts are not measurements of river length, flow, flood risk or ecological condition.
