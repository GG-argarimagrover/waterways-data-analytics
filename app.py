import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Waterways | Living Systems",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Visual system: river / glacier / wetland ---
BG = "#071923"
PANEL = "#102B36"
PANEL2 = "#153844"
TEXT = "#EAF7F7"
MUTED = "#A8C4CA"
TEAL = "#52E0C4"
BLUE = "#70C8F2"
MINT = "#A8E6CF"
CORAL = "#FF987A"
GOLD = "#EACB7A"
PALETTE = [TEAL, BLUE, MINT, CORAL, GOLD, "#A9A5FF", "#D7F0EF", "#4EA3A8"]

# CSS: target Streamlit's app canvas and header; hide only the default header
# background, not Streamlit's controls. Header controls remain usable.
st.markdown(f"""
<style>
:root {{
  color-scheme: dark;
}}
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{
  background: {BG};
  color: {TEXT};
}}
[data-testid="stHeader"] {{
  background: rgba(7,25,35,0.96);
}}
[data-testid="stToolbar"] {{
  right: 1rem;
}}
[data-testid="stSidebar"] {{
  background: #0B222D;
  border-right: 1px solid #1C4651;
}}
[data-testid="stSidebar"] * {{
  color: {TEXT};
}}
.block-container {{
  padding-top: 1.4rem;
  padding-bottom: 3rem;
  max-width: 1500px;
}}
h1, h2, h3, p, label, .stMarkdown {{
  color: {TEXT};
}}
.hero {{
  background:
    radial-gradient(ellipse at 80% 15%, rgba(82,224,196,.18), transparent 35%),
    radial-gradient(ellipse at 95% 85%, rgba(112,200,242,.16), transparent 35%),
    linear-gradient(120deg, #102F3B, #0A202C 68%, #123844);
  border: 1px solid #24515B;
  border-radius: 24px;
  padding: 28px 32px 26px 32px;
  margin: 4px 0 22px 0;
  position: relative;
  overflow: hidden;
}}
.eyebrow {{
  color: {TEAL};
  font-size: .78rem;
  font-weight: 750;
  letter-spacing: .16em;
  text-transform: uppercase;
}}
.hero h1 {{
  font-size: clamp(2rem, 4vw, 3.4rem);
  letter-spacing: -.04em;
  line-height: 1.04;
  margin: 10px 0 12px 0;
  color: {TEXT};
}}
.hero p {{
  color: {MUTED};
  max-width: 780px;
  font-size: 1.02rem;
  margin-bottom: 0;
}}
.riverline {{
  height: 5px;
  width: 190px;
  border-radius: 99px;
  margin-top: 22px;
  background: linear-gradient(90deg, {TEAL}, {BLUE}, transparent);
}}
.section-kicker {{
  color: {TEAL};
  font-size: .76rem;
  font-weight: 750;
  letter-spacing: .14em;
  text-transform: uppercase;
  margin-bottom: .3rem;
}}
.section-title {{
  color: {TEXT};
  font-size: 1.45rem;
  font-weight: 720;
  letter-spacing: -.025em;
  margin-bottom: .2rem;
}}
.section-note {{
  color: {MUTED};
  margin-bottom: 1rem;
  font-size: .92rem;
}}
div[data-testid="stMetric"] {{
  background: linear-gradient(145deg, #12323E, #0D2732);
  border: 1px solid #24515B;
  border-radius: 16px;
  padding: 18px 18px 15px 18px;
  min-height: 112px;
}}
div[data-testid="stMetricLabel"] {{
  color: {MUTED} !important;
  font-size: .84rem;
}}
div[data-testid="stMetricValue"] {{
  color: {TEXT} !important;
  font-size: 1.95rem;
  font-weight: 750;
}}
div[data-testid="stMetricDelta"] {{
  color: {TEAL} !important;
}}
div[data-testid="stTabs"] button {{
  color: {MUTED};
  border-radius: 10px 10px 0 0;
}}
div[data-testid="stTabs"] button[aria-selected="true"] {{
  color: {TEAL};
  border-bottom-color: {TEAL};
}}
div[data-testid="stDataFrame"] {{
  border: 1px solid #24515B;
  border-radius: 12px;
  overflow: hidden;
}}
.stButton button, .stDownloadButton button {{
  background: #174451;
  color: {TEXT};
  border: 1px solid #2B6870;
  border-radius: 10px;
}}
.stButton button:hover, .stDownloadButton button:hover {{
  background: #20606A;
  color: white;
  border-color: {TEAL};
}}
hr {{
  border-color: #214652;
}}
div[data-testid="stAlert"] {{
  background: #102B36;
}}
footer {{visibility: hidden;}}
</style>
""", unsafe_allow_html=True)

def plot_theme(fig, height=390):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, Arial, sans-serif", color=TEXT, size=12),
        title=dict(font=dict(size=16, color=TEXT), x=0.02, xanchor="left"),
        margin=dict(l=12, r=12, t=58, b=12),
        height=height,
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=MUTED)),
        xaxis=dict(gridcolor="#23434D", zerolinecolor="#23434D", title_font_color=MUTED, tickfont_color=MUTED),
        yaxis=dict(gridcolor="#23434D", zerolinecolor="#23434D", title_font_color=MUTED, tickfont_color=MUTED),
    )
    return fig

@st.cache_data
def read_csv(file_bytes):
    import io
    return pd.read_csv(io.BytesIO(file_bytes))

@st.cache_data
def read_local(path):
    return pd.read_csv(path)

st.sidebar.markdown("## 🌊 Explore the system")
st.sidebar.caption("Bring a waterways CSV into the studio.")
uploaded = st.sidebar.file_uploader("Upload CSV", type=["csv"])
if uploaded:
    try:
        df = read_csv(uploaded.getvalue())
    except Exception as e:
        st.error(f"Unable to read CSV: {e}")
        st.stop()
else:
    try:
        df = read_local("Waterways.csv")
        st.sidebar.success("Waterways.csv loaded")
    except FileNotFoundError:
        st.markdown("""
        <div class="hero">
          <div class="eyebrow">Waterways intelligence studio</div>
          <h1>Read the patterns<br>within the blue network.</h1>
          <p>Upload a waterways CSV in the sidebar to explore feature composition, naming coverage, data quality and classification patterns.</p>
          <div class="riverline"></div>
        </div>
        """, unsafe_allow_html=True)
        st.info("Upload Waterways.csv using the sidebar to start the dashboard.")
        st.stop()
    except Exception as e:
        st.error(f"Unable to read Waterways.csv: {e}")
        st.stop()

if df.empty:
    st.warning("This CSV contains no records.")
    st.stop()

df.columns = df.columns.astype(str).str.strip()
for c in df.select_dtypes(include=["object", "string"]).columns:
    df[c] = df[c].astype("string").str.strip().replace("", pd.NA)

def find_col(options):
    lookup = {c.lower(): c for c in df.columns}
    return next((lookup[x] for x in options if x in lookup), None)

class_col = find_col(["fclass", "class", "category", "feature_type", "type"])
name_col = find_col(["name", "waterway_name", "feature_name"])
code_col = find_col(["code", "type_code"])
id_col = find_col(["fid", "osm_id", "id", "feature_id"])

st.markdown("""
<div class="hero">
  <div class="eyebrow">Waterways intelligence · Exploratory edition</div>
  <h1>Water is a network.<br>Let's understand its patterns.</h1>
  <p>Explore the composition, information quality and classification of mapped water-related features. Start with the big picture, then move into the details.</p>
  <div class="riverline"></div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### Refine your view")
filtered = df.copy()
if class_col:
    classes = sorted(df[class_col].dropna().astype(str).unique().tolist())
    selected = st.sidebar.multiselect("Feature class", classes, default=classes)
    filtered = filtered[filtered[class_col].astype("string").isin(selected)]
if name_col:
    name_search = st.sidebar.text_input("Find a named feature", placeholder="Type a name…")
    if name_search.strip():
        filtered = filtered[filtered[name_col].astype("string").str.contains(name_search.strip(), case=False, na=False, regex=False)]

st.sidebar.caption(f"{len(filtered):,} of {len(df):,} records in view")
if filtered.empty:
    st.warning("No records match these filters. Adjust the sidebar selections.")
    st.stop()

total = len(filtered)
class_count = filtered[class_col].nunique(dropna=True) if class_col else 0
named = int(filtered[name_col].notna().sum()) if name_col else 0
named_pct = (named / total * 100) if name_col and total else 0
missing_pct = float(filtered.isna().sum().sum() / max(filtered.size, 1) * 100)
dupes = int(filtered.duplicated().sum())

m1, m2, m3, m4 = st.columns(4)
m1.metric("Mapped records", f"{total:,}", help="Number of rows currently included by filters.")
m2.metric("Feature classes", f"{class_count:,}")
m3.metric("Named features", f"{named_pct:.1f}%" if name_col else "N/A", help="Share of records with a name.")
m4.metric("Missing cells", f"{missing_pct:.1f}%", help="Share of empty cells across the filtered table.")

st.markdown('<div class="section-kicker">Explore the evidence</div><div class="section-title">From composition to confidence</div><div class="section-note">Use the tabs to move from an overview into classification, data quality and individual records.</div>', unsafe_allow_html=True)

overview, types, quality, records = st.tabs(["🌊 The overview", "🧩 Feature patterns", "🧪 Data confidence", "📋 Record explorer"])

with overview:
    left, right = st.columns([1.05, 1.15], gap="large")
    if class_col:
        counts = filtered[class_col].fillna("Unknown").astype(str).value_counts().rename_axis("Feature class").reset_index(name="Records")
        counts["Share"] = counts["Records"] / max(total, 1) * 100
        with left:
            st.markdown("#### What makes up this dataset?")
            fig = go.Figure(go.Pie(
                labels=counts["Feature class"], values=counts["Records"],
                hole=.70, sort=False,
                marker=dict(colors=PALETTE, line=dict(color=BG, width=3)),
                textinfo="percent", textposition="inside",
                hovertemplate="<b>%{label}</b><br>%{value:,} records<br>%{percent}<extra></extra>"
            ))
            fig.add_annotation(text=f"<b>{total:,}</b><br><span style='font-size:11px'>records</span>",
                               x=.5, y=.5, showarrow=False,
                               font=dict(size=23, color=TEXT))
            plot_theme(fig, 400)
            fig.update_layout(showlegend=True, legend=dict(orientation="h", y=-.12, x=0, font=dict(size=10, color=MUTED)))
            st.plotly_chart(fig, use_container_width=True)
        with right:
            st.markdown("#### Which classes appear most often?")
            top = counts.head(10).sort_values("Records")
            fig = px.bar(top, x="Records", y="Feature class", orientation="h",
                         text="Records", color="Feature class",
                         color_discrete_sequence=PALETTE)
            fig.update_traces(textposition="outside", cliponaxis=False)
            plot_theme(fig, 400)
            fig.update_layout(showlegend=False, xaxis_title="Mapped records", yaxis_title="")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No feature class field was detected. Check the CSV column names.")
    if name_col:
        named_count = int(filtered[name_col].notna().sum())
        unnamed_count = total - named_count
        a, b = st.columns([1, 1], gap="large")
        with a:
            st.markdown("#### How much is named?")
            fig = go.Figure(go.Pie(labels=["Named", "Unnamed"], values=[named_count, unnamed_count],
                                   hole=.72, marker=dict(colors=[TEAL, "#294651"], line=dict(color=BG, width=3)),
                                   textinfo="percent", hovertemplate="%{label}: %{value:,}<extra></extra>"))
            fig.add_annotation(text=f"<b>{named_pct:.0f}%</b><br><span style='font-size:11px'>named</span>",
                               x=.5, y=.5, showarrow=False, font=dict(size=22, color=TEXT))
            plot_theme(fig, 320)
            fig.update_layout(showlegend=True, legend=dict(orientation="h", y=-.1))
            st.plotly_chart(fig, use_container_width=True)
        with b:
            st.markdown("#### Most common names")
            top_names = filtered[name_col].dropna().astype(str).value_counts().head(8).sort_values()
            if len(top_names):
                named_df = top_names.rename_axis("Name").reset_index(name="Records")
                fig = px.bar(named_df, x="Records", y="Name", orientation="h", text="Records",
                             color_discrete_sequence=[BLUE])
                fig.update_traces(textposition="outside", cliponaxis=False)
                plot_theme(fig, 320)
                fig.update_layout(xaxis_title="Records", yaxis_title="")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.caption("No named records in the current filter.")

    st.markdown("#### A quick reading of the dataset")
    insights = []
    if class_col:
        vc = filtered[class_col].fillna("Unknown").astype(str).value_counts()
        if len(vc):
            insights.append(f"**{vc.index[0]}** is the most common class, accounting for **{vc.iloc[0]/total*100:.1f}%** of the filtered records.")
            insights.append(f"The data includes **{len(vc)} distinct feature classes**.")
    if name_col:
        insights.append(f"**{named_pct:.1f}%** of filtered records have a name; the remainder may need interpretation or enrichment depending on the source.")
    insights.append(f"**{missing_pct:.1f}%** of cells are empty across the current view.")
    for item in insights:
        st.markdown(f"- {item}")

with types:
    st.markdown("#### Compare feature categories")
    if class_col:
        counts = filtered[class_col].fillna("Unknown").astype(str).value_counts().rename_axis("Feature class").reset_index(name="Records")
        counts["Share (%)"] = (counts["Records"] / max(total, 1) * 100).round(2)
        counts["Cumulative (%)"] = counts["Share (%)"].cumsum().round(2)
        st.dataframe(counts, use_container_width=True, hide_index=True)
        if code_col:
            cross = pd.crosstab(filtered[class_col].fillna("Unknown"), filtered[code_col].fillna("Unknown"))
            st.markdown("#### Feature class × code")
            fig = px.imshow(cross, aspect="auto", color_continuous_scale=[[0, PANEL], [1, TEAL]],
                            labels=dict(x="Code", y="Feature class", color="Records"))
            plot_theme(fig, max(350, 28 * len(cross)))
            st.plotly_chart(fig, use_container_width=True)
    numeric = filtered.select_dtypes(include=np.number).columns.tolist()
    numeric = [c for c in numeric if not any(k in c.lower() for k in ["fid", "osm_id", "identifier"])]
    if numeric:
        st.markdown("#### Numeric field distribution")
        chosen = st.selectbox("Choose a numeric field", numeric)
        fig = px.histogram(filtered, x=chosen, marginal="box", color_discrete_sequence=[TEAL])
        plot_theme(fig, 350)
        st.plotly_chart(fig, use_container_width=True)
        if len(numeric) > 1:
            corr = filtered[numeric].corr()
            fig = px.imshow(corr, text_auto=".2f", aspect="auto", color_continuous_scale="RdBu_r", zmin=-1, zmax=1)
            plot_theme(fig, 360)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.caption("No measured numeric fields are available. IDs and classification codes are not treated as physical measurements.")

with quality:
    st.markdown("#### Data completeness")
    q = pd.DataFrame({
        "Field": filtered.columns,
        "Type": filtered.dtypes.astype(str).values,
        "Records filled": filtered.notna().sum().values,
        "Missing": filtered.isna().sum().values,
        "Missing (%)": (filtered.isna().mean().values * 100).round(2),
        "Distinct values": filtered.nunique(dropna=True).values
    }).sort_values("Missing (%)", ascending=False)
    st.dataframe(q, use_container_width=True, hide_index=True)
    missing = q[q["Missing"] > 0].sort_values("Missing (%)")
    if not missing.empty:
        fig = px.bar(missing, x="Missing (%)", y="Field", orientation="h", text="Missing (%)",
                     color="Missing (%)", color_continuous_scale=[[0, "#1D6570"], [1, CORAL]])
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside", cliponaxis=False)
        plot_theme(fig, max(300, 35 * len(missing)))
        fig.update_layout(showlegend=False, xaxis_title="Empty cells (%)", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("No missing cells in the current view.")
    st.markdown("#### Repeated records and identifiers")
    qc1, qc2, qc3 = st.columns(3)
    qc1.metric("Duplicate rows", f"{dupes:,}")
    if id_col:
        qc2.metric("Unique IDs", f"{filtered[id_col].nunique(dropna=True):,}")
        qc3.metric("Repeated ID values", f"{int(filtered[id_col].duplicated().sum()):,}")
    else:
        qc2.metric("Unique IDs", "No ID field")
        qc3.metric("Repeated ID values", "N/A")
    st.markdown("#### Numeric summary")
    num = filtered.select_dtypes(include=np.number)
    if not num.empty:
        st.dataframe(num.describe().T, use_container_width=True)
    else:
        st.caption("No numeric columns to summarise.")

with records:
    st.markdown("#### Find and inspect records")
    search = st.text_input("Search all fields", placeholder="Search class, code, ID or name…")
    view = filtered.copy()
    if search.strip():
        mask = view.astype("string").apply(lambda col: col.str.contains(search.strip(), case=False, na=False, regex=False)).any(axis=1)
        view = view[mask]
    st.caption(f"{len(view):,} records match your search.")
    st.dataframe(view, use_container_width=True, hide_index=True, height=480)
    st.download_button("Download filtered records · CSV", view.to_csv(index=False).encode("utf-8"),
                       "waterways_filtered.csv", "text/csv")
    summary = pd.DataFrame({"Indicator": ["Original records", "Filtered records", "Fields", "Duplicate rows", "Missing cells"],
                            "Value": [len(df), len(filtered), len(df.columns), int(filtered.duplicated().sum()), int(filtered.isna().sum().sum())]})
    st.download_button("Download summary · CSV", summary.to_csv(index=False).encode("utf-8"),
                       "waterways_summary.csv", "text/csv")

st.markdown("---")
st.caption("WATERWAYS INTELLIGENCE STUDIO  /  Attribute analytics only. Counts describe mapped records, not waterway length, water volume, flood risk, ecological health or geographic distribution. Those analyses require verified spatial and environmental data.")
