# Waterways Data Analytics 🌊

An interactive Google Colab notebook for exploratory data analysis and visualisation of waterways attribute data.

## Features

- Data quality audit: missing values, data types, unique values and duplicate rows
- Descriptive statistics and categorical frequency distributions
- Interactive Plotly bar charts and pie charts
- Feature class versus code cross-tabulation
- Numeric distributions, outlier checks and correlation heatmap when applicable
- Named versus unnamed feature analysis
- Spatial-data readiness check and coordinate map when valid coordinates exist
- Export of cleaned CSV, KPI summaries and an Excel report

## Quick start

1. Open the notebook: [`Waterways_Data_Analytics.ipynb`](Waterways_Data_Analytics.ipynb).
2. Click **Open in Colab** or upload the notebook to Google Colab.
3. Run all cells.
4. Upload `Waterways.csv` when prompted.
5. Review the charts and download the generated Excel report.

[Open Google Colab](https://colab.research.google.com/)

## Dataset

Place `Waterways.csv` in the Colab session when prompted. The repository intentionally does not include the raw dataset by default.

Expected fields in the current example may include `fid`, `osm_id`, `code`, `fclass`, and `name`. The notebook detects columns dynamically where practical.

## Spatial limitations

Attribute-only CSV data does not provide enough information for a geographic map, feature length/area calculation, proximity analysis, or flood-risk assessment. For those workflows, use verified coordinates or spatial geometry (GeoJSON, Shapefile components, or GeoPackage) and appropriate supporting datasets.

## Outputs

The notebook writes analysis outputs to `/content/waterways_analytics/` in Google Colab:

- `waterways_cleaned.csv`
- `data_quality_audit.csv`
- `waterways_kpis.csv`
- `feature_class_summary.csv` (if `fclass` exists)
- `waterways_analytics_report.xlsx`

## Technologies

Python, pandas, NumPy, Plotly, and openpyxl.

## License

MIT License. See [`LICENSE`](LICENSE).
