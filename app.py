import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Waterways Intelligence",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(145deg, #0b1220, #101c2c);
    color: #f0f5fa;
}
[data-testid="stSidebar"] { background-color: #101a29; }
[data-testid="stMetric"] {
    background: #152438;
    border: 1px solid #263d55;
    padding: 18px;
    border-radius: 12px;
}
h1, h2, h3 { color: #e7f5ff; }
</style>
""", unsafe_allow_html=True)

COLORS = ["#42d6c5", "#53a8ff", "#a78bfa", "#f6bd60",
          "#f28482", "#8bd17c", "#f7a8d8", "#b8c0ff"]

st.title("🌊 WATERWAYS INTELLIGENCE")
st.caption("Interactive data analytics • Feature classification • Data quality • Exploratory insights")

st.sidebar.header("📂 Data source")
uploaded_file = st.sidebar.file_uploader("Upload a CSV dataset", type=["csv"])

@st.cache_data
def load_csv(file_bytes):
    import io
    return pd.read_csv(io.BytesIO(file_bytes))

@st.cache_data
def load_local_csv(path):
    return pd.read_csv(path)

df = None
if uploaded_file is not None:
    try:
        df = load_csv(uploaded_file.getvalue())
    except Exception as e:
        st.error(f"Could not read CSV: {e}")
        st.stop()
else:
    try:
        df = load_local_csv("Waterways.csv")
        st.sidebar.success("Loaded Waterways.csv")
    except FileNotFoundError:
        st.info("Upload Waterways.csv using the sidebar to start exploring. For a hosted dashboard, add the CSV to the repository only if you have permission to publish it.")
        st.stop()
    except Exception as e:
        st.error(f"Could not read Waterways.csv: {e}")
        st.stop()

if df.empty:
    st.warning("The uploaded dataset contains no records.")
    st.stop()

df.columns = df.columns.astype(str).str.strip()
for col in df.select_dtypes(include=["object", "string"]).columns:
    df[col] = df[col].astype("string").str.strip().replace("", pd.NA)

def find_col(candidates):
    lookup = {c.lower(): c for c in df.columns}
    for candidate in candidates:
        if candidate in lookup:
            return lookup[candidate]
    return None

class_col = find_col(["fclass", "class", "category", "feature_type", "type"])
name_col = find_col(["name", "waterway_name", "feature_name"])
code_col = find_col(["code", "type_code"])
id_col = find_col(["fid", "osm_id", "id", "feature_id"])

st.sidebar.divider()
st.sidebar.header("🔎 Dashboard filters")
filtered = df.copy()

if class_col:
    classes = sorted(df[class_col].dropna().astype(str).unique().tolist())
    selected_classes = st.sidebar.multiselect("Feature classes", options=classes, default=classes)
    filtered = filtered[filtered[class_col].astype("string").isin(selected_classes)]

if name_col:
    search_name = st.sidebar.text_input("Search feature names", placeholder="Enter a name...")
    if search_name.strip():
        filtered = filtered[filtered[name_col].astype("string").str.contains(search_name.strip(), case=False, na=False, regex=False)]

st.sidebar.caption(f"Showing {len(filtered):,} of {len(df):,} records")
if filtered.empty:
    st.warning("No records match the current filters.")
    st.stop()

total = len(filtered)
classes_count = filtered[class_col].nunique(dropna=True) if class_col else 0
named_count = int(filtered[name_col].notna().sum()) if name_col else 0
missing_cells = int(filtered.isna().sum().sum())
duplicate_rows = int(filtered.duplicated().sum())

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total features", f"{total:,}")
k2.metric("Feature classes", f"{classes_count:,}")
k3.metric("Named features", f"{named_count:,}" if name_col else "N/A")
k4.metric("Missing cells", f"{missing_cells:,}")
k5.metric("Duplicate rows", f"{duplicate_rows:,}")

st.divider()
overview_tab, class_tab, quality_tab, explorer_tab = st.tabs([
    "📊 Overview", "🧩 Feature Intelligence", "🧪 Data Quality", "📋 Data Explorer"
])

with overview_tab:
    st.subheader("Dataset overview")
    left, right = st.columns(2)
    with left:
        if class_col:
            counts = filtered[class_col].fillna("Unknown").astype(str).value_counts().rename_axis("Feature class").reset_index(name="Records")
            fig = px.pie(counts, names="Feature class", values="Records", hole=0.58, color_discrete_sequence=COLORS, title="Composition by feature class")
            fig.update_traces(textposition="inside", textinfo="percent+label")
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No feature-class column was detected.")
    with right:
        if class_col:
            counts = filtered[class_col].fillna("Unknown").astype(str).value_counts().head(15).sort_values().rename_axis("Feature class").reset_index(name="Records")
            fig = px.bar(counts, x="Records", y="Feature class", orientation="h", text="Records", color="Records", color_continuous_scale="Teal", title="Most frequent feature classes")
            fig.update_layout(template="plotly_dark", coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)
    if name_col:
        named = int(filtered[name_col].notna().sum())
        unnamed = total - named
        fig = go.Figure(data=[go.Pie(labels=["Named", "Unnamed"], values=[named, unnamed], hole=0.62, marker_colors=["#42d6c5", "#53657a"])])
        fig.update_layout(title="Named vs unnamed records", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    st.subheader("Dataset structure")
    structure = pd.DataFrame({
        "Column": filtered.columns,
        "Data type": filtered.dtypes.astype(str).values,
        "Non-null records": filtered.notna().sum().values,
        "Missing records": filtered.isna().sum().values,
        "Unique values": filtered.nunique(dropna=True).values
    })
    st.dataframe(structure, use_container_width=True, hide_index=True)

with class_tab:
    st.subheader("Feature classification")
    if class_col:
        counts = filtered[class_col].fillna("Unknown").astype(str).value_counts().rename_axis("Feature class").reset_index(name="Records")
        counts["Share (%)"] = (counts["Records"] / len(filtered) * 100).round(2)
        st.dataframe(counts, use_container_width=True, hide_index=True)
        if code_col:
            cross = pd.crosstab(filtered[class_col].fillna("Unknown"), filtered[code_col].fillna("Unknown"))
            st.subheader("Feature class versus code")
            fig = px.imshow(cross, aspect="auto", color_continuous_scale="Teal", title="Classification and code matrix")
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
    if id_col:
        st.subheader("Identifier checks")
        st.write(f"Unique values in `{id_col}`: {filtered[id_col].nunique(dropna=True):,}")
        st.write(f"Repeated values in `{id_col}`: {int(filtered[id_col].duplicated().sum()):,}")
    st.subheader("Numeric field distributions")
    numeric_cols = filtered.select_dtypes(include=np.number).columns.tolist()
    id_like = [c for c in numeric_cols if any(k in c.lower() for k in ["fid", "osm_id", "identifier"])]
    measure_cols = [c for c in numeric_cols if c not in id_like]
    if measure_cols:
        selected_numeric = st.selectbox("Choose a numeric field", measure_cols)
        fig = px.histogram(filtered, x=selected_numeric, marginal="box", title=f"Distribution: {selected_numeric}", color_discrete_sequence=["#42d6c5"])
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
        if len(measure_cols) > 1:
            corr = filtered[measure_cols].corr()
            fig = px.imshow(corr, text_auto=".2f", aspect="auto", color_continuous_scale="RdBu_r", title="Numeric correlations")
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No measured numeric variables are available. Identifier fields and category codes should not automatically be interpreted as physical measurements.")

with quality_tab:
    st.subheader("Data quality assessment")
    quality = pd.DataFrame({
        "Column": filtered.columns,
        "Missing": filtered.isna().sum().values,
        "Missing (%)": (filtered.isna().mean().values * 100).round(2),
        "Unique values": filtered.nunique(dropna=True).values,
        "Data type": filtered.dtypes.astype(str).values
    })
    st.dataframe(quality, use_container_width=True, hide_index=True)
    missing = quality[quality["Missing"] > 0].sort_values("Missing", ascending=True)
    if not missing.empty:
        fig = px.bar(missing, x="Missing", y="Column", orientation="h", text="Missing", color="Missing", color_continuous_scale="OrRd", title="Missing values by field")
        fig.update_layout(template="plotly_dark", coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("No missing values in the filtered records.")
    st.write(f"Duplicate rows: {filtered.duplicated().sum():,}")
    st.subheader("Statistical summary")
    numeric = filtered.select_dtypes(include=np.number)
    if not numeric.empty:
        st.dataframe(numeric.describe().T, use_container_width=True)
    else:
        st.info("No numeric fields available for statistical summary.")

with explorer_tab:
    st.subheader("Search and inspect records")
    search_all = st.text_input("Search across all fields", placeholder="Search for a class, ID, code or name...")
    view = filtered.copy()
    if search_all.strip():
        mask = view.astype("string").apply(lambda col: col.str.contains(search_all.strip(), case=False, na=False, regex=False)).any(axis=1)
        view = view[mask]
    st.caption(f"{len(view):,} matching records")
    st.dataframe(view, use_container_width=True, hide_index=True, height=500)
    st.download_button("⬇️ Download filtered data (CSV)", data=view.to_csv(index=False).encode("utf-8"), file_name="waterways_filtered.csv", mime="text/csv")
    report = pd.DataFrame({
        "Metric": ["Total records in original dataset", "Records after dashboard filters", "Columns", "Duplicate rows after filters", "Missing cells after filters"],
        "Value": [len(df), len(filtered), len(df.columns), int(filtered.duplicated().sum()), int(filtered.isna().sum().sum())]
    })
    st.download_button("⬇️ Download dashboard summary (CSV)", data=report.to_csv(index=False).encode("utf-8"), file_name="waterways_dashboard_summary.csv", mime="text/csv")

st.divider()
st.caption("WATERWAYS INTELLIGENCE | Exploratory analytics dashboard. Record counts do not represent waterway length, area, flow, flood risk, or ecological condition. Geographic analysis requires verified spatial data.")
