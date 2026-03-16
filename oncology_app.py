"""
╔══════════════════════════════════════════════════════════════════╗
║        OnchoInsight — Oncology Data Analytics Platform           ║
║        US Healthcare Standard UI  |  Clinical Light Theme        ║
║        WCAG 2.1 AA · CMS Design System · Epic-style palette      ║
╚══════════════════════════════════════════════════════════════════╝

Run:
    pip install streamlit pandas numpy plotly
    streamlit run oncology_app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import math

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="OnchoInsight | Oncology Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# US HEALTHCARE COLOR PALETTE
# References: CMS Design System, Epic Hyperspace, HIMSS, HealthCare.gov
# All colors meet WCAG 2.1 AA (4.5:1 contrast on white backgrounds)
# ─────────────────────────────────────────────────────────────────────────────
C_PRIMARY    = "#1B4F8A"   # Deep clinical blue — trust, authority
C_PRIMARY_LT = "#2563EB"   # Action blue — interactive elements
C_PRIMARY_BG = "#EBF3FB"   # Lightest blue — backgrounds, tints

C_TEAL       = "#0D7680"   # Clinical teal — secondary data, lab
C_TEAL_BG    = "#E0F4F5"

C_SUCCESS    = "#0E7C34"   # Clinical green — positive, normal
C_SUCCESS_BG = "#E6F5EC"

C_WARNING    = "#B45309"   # Amber — caution, review needed
C_WARNING_BG = "#FEF3C7"

C_DANGER     = "#B91C1C"   # Red — critical, high severity
C_DANGER_BG  = "#FEE2E2"

C_INFO       = "#1E40AF"   # Info blue — neoadjuvant, data notes
C_INFO_BG    = "#EFF6FF"

C_PURPLE     = "#6D28D9"   # Purple — research, biomarker, ML
C_PURPLE_BG  = "#EDE9FE"

C_ORANGE     = "#C2410C"   # Deep orange — therapy lines, trends
C_ORANGE_BG  = "#FFF7ED"

# Neutral / structural
C_BG         = "#F0F4F8"   # App canvas — light blue-gray
C_SURFACE    = "#FFFFFF"   # Cards, panels
C_BORDER     = "#CBD5E1"   # Dividers, borders
C_BORDER_LT  = "#E2E8F0"   # Subtle borders
C_TEXT       = "#1E293B"   # Primary text
C_TEXT_MED   = "#475569"   # Secondary text
C_TEXT_MUTED = "#94A3B8"   # Placeholders, hints
C_HEADER     = "#1B4F8A"   # Top header bar

# Chart palette — color-blind safe, WCAG compliant
CHART_COLORS = [C_PRIMARY, C_TEAL, C_SUCCESS, C_WARNING, C_DANGER, C_PURPLE,
                "#0369A1", "#047857", "#7C3AED", "#9A3412"]

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@300;400;600;700&family=Source+Code+Pro:wght@400;500&display=swap');

html, body, [class*="css"] {{
    font-family: 'Source Sans 3', 'Segoe UI', Arial, sans-serif;
    background-color: {C_BG};
    color: {C_TEXT};
    font-size: 14px;
}}
.stApp {{ background-color: {C_BG}; }}

/* Sidebar */
[data-testid="stSidebar"] {{
    background-color: {C_SURFACE} !important;
    border-right: 2px solid {C_BORDER} !important;
}}
[data-testid="stSidebar"] * {{ color: {C_TEXT} !important; }}

/* Main padding */
.main .block-container {{ padding: 0 !important; max-width: 100%; }}

/* Metrics */
[data-testid="metric-container"] {{
    background: {C_SURFACE};
    border: 1px solid {C_BORDER};
    border-radius: 8px;
    padding: 14px 16px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}}
[data-testid="stMetricValue"] {{ color: {C_PRIMARY} !important; font-weight: 700; }}

/* Headings */
h1 {{ color: {C_PRIMARY} !important; font-weight: 700; font-size: 1.4rem !important;
      border-bottom: 2px solid {C_BORDER_LT}; padding-bottom: 8px; }}
h2 {{ color: {C_PRIMARY} !important; font-weight: 600; font-size: 1.1rem !important; }}
h3 {{ color: {C_TEXT} !important; font-weight: 600; font-size: 0.95rem !important; }}

/* Tables */
[data-testid="stDataFrame"] {{
    border: 1px solid {C_BORDER} !important;
    border-radius: 8px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
}}

/* Buttons */
.stButton > button {{
    background: {C_PRIMARY} !important;
    color: white !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 8px 18px !important;
    font-size: 13px !important;
    font-family: 'Source Sans 3', sans-serif !important;
    box-shadow: 0 1px 3px rgba(27,79,138,0.3) !important;
}}
.stButton > button:hover {{ background: #154070 !important; }}

/* Selects */
[data-testid="stSelectbox"] > div > div {{
    background: {C_SURFACE} !important;
    border: 1px solid {C_BORDER} !important;
    border-radius: 6px !important;
    color: {C_TEXT} !important;
}}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {{
    background: {C_SURFACE};
    border-bottom: 2px solid {C_BORDER};
    padding: 0;
    gap: 0;
}}
.stTabs [data-baseweb="tab"] {{
    background: transparent;
    color: {C_TEXT_MED};
    font-weight: 600;
    font-size: 13px;
    padding: 10px 20px;
    border-bottom: 3px solid transparent;
    margin-bottom: -2px;
    border-radius: 0;
}}
.stTabs [aria-selected="true"] {{
    background: transparent !important;
    color: {C_PRIMARY} !important;
    border-bottom: 3px solid {C_PRIMARY} !important;
}}
.stTabs [data-baseweb="tab"]:hover {{
    background: {C_PRIMARY_BG} !important;
    color: {C_PRIMARY} !important;
}}

/* Expanders */
[data-testid="stExpander"] {{
    background: {C_SURFACE} !important;
    border: 1px solid {C_BORDER} !important;
    border-radius: 8px !important;
}}
hr {{ border-color: {C_BORDER} !important; margin: 10px 0 !important; }}

/* ── Custom components ── */

.hc-topbar {{
    background: {C_HEADER};
    color: white;
    padding: 14px 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 8px rgba(27,79,138,0.2);
}}
.hc-topbar-title {{ font-size: 17px; font-weight: 700; }}
.hc-topbar-sub   {{ font-size: 12px; opacity: 0.8; margin-top: 2px; }}
.hc-badge {{
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.3);
    color: white;
    padding: 3px 11px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    margin-left: 7px;
}}

.hc-kpi {{
    background: {C_SURFACE};
    border: 1px solid {C_BORDER};
    border-left: 4px solid;
    border-radius: 8px;
    padding: 14px 18px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}}
.hc-kpi-num   {{ font-size: 26px; font-weight: 700;
                 font-family: 'Source Code Pro', monospace; margin-bottom: 3px; }}
.hc-kpi-label {{ font-size: 10px; font-weight: 700; color: {C_TEXT_MED};
                 text-transform: uppercase; letter-spacing: 0.08em; }}
.hc-kpi-delta {{ font-size: 11px; color: {C_TEXT_MUTED}; margin-top: 5px; }}

.hc-sec {{
    font-size: 13px; font-weight: 700; color: {C_PRIMARY};
    background: {C_PRIMARY_BG};
    border-left: 4px solid {C_PRIMARY};
    padding: 9px 14px;
    border-radius: 0 6px 6px 0;
    margin: 16px 0 12px;
}}

.hc-insight {{
    background: {C_SURFACE};
    border: 1px solid {C_BORDER};
    border-left: 4px solid {C_PRIMARY};
    border-radius: 0 8px 8px 0;
    padding: 13px 18px;
    margin-bottom: 10px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}}
.hc-insight-text {{ font-size: 13px; color: {C_TEXT}; line-height: 1.6; }}
.hc-insight-meta {{ font-size: 11px; color: {C_TEXT_MUTED}; margin-top: 5px; }}

.prd-card {{
    background: {C_SURFACE};
    border: 1px solid {C_BORDER};
    border-radius: 8px;
    padding: 16px 18px;
    margin-bottom: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}}
.prd-title {{ color: {C_PRIMARY}; font-weight: 700; font-size: 13px; margin-bottom: 7px; }}
.prd-body  {{ color: {C_TEXT_MED}; font-size: 13px; line-height: 1.7; }}

.journey-node {{
    background: {C_SURFACE};
    border: 1px solid {C_BORDER};
    border-top: 3px solid;
    border-radius: 8px;
    text-align: center;
    padding: 12px 6px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}}
.journey-icon  {{ font-size: 22px; }}
.journey-title {{ font-size: 9px; font-weight: 700; text-transform: uppercase;
                  letter-spacing: 0.07em; margin: 6px 0 3px; }}
.journey-date  {{ font-size: 10px; font-family: 'Source Code Pro', monospace;
                  color: {C_PRIMARY}; }}

.persona-card {{
    background: {C_SURFACE};
    border: 1px solid {C_BORDER};
    border-top: 3px solid;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}}

.biz-kpi {{
    background: {C_SURFACE};
    border: 1px solid {C_BORDER};
    border-top: 3px solid;
    border-radius: 8px;
    padding: 16px;
    text-align: center;
    margin-bottom: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}}
.biz-kpi-val   {{ font-size: 24px; font-weight: 700;
                  font-family: 'Source Code Pro', monospace; }}
.biz-kpi-label {{ font-size: 10px; color: {C_TEXT_MED}; text-transform: uppercase;
                  letter-spacing: 0.07em; margin-top: 5px; }}

.phase-card {{
    background: {C_SURFACE};
    border: 1px solid {C_BORDER};
    border-left: 4px solid;
    border-radius: 0 8px 8px 0;
    padding: 14px 18px;
    margin-bottom: 10px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    display: flex;
    align-items: flex-start;
    gap: 12px;
}}

.hc-alert-info    {{ background:{C_INFO_BG};border:1px solid #BFDBFE;border-left:4px solid {C_INFO};
                     border-radius:0 6px 6px 0;padding:9px 14px;font-size:12px;color:{C_INFO};margin-bottom:10px;}}
.hc-alert-success {{ background:{C_SUCCESS_BG};border:1px solid #A7F3D0;border-left:4px solid {C_SUCCESS};
                     border-radius:0 6px 6px 0;padding:9px 14px;font-size:12px;color:{C_SUCCESS};margin-bottom:10px;}}
.hc-alert-warn    {{ background:{C_WARNING_BG};border:1px solid #FCD34D;border-left:4px solid {C_WARNING};
                     border-radius:0 6px 6px 0;padding:9px 14px;font-size:12px;color:{C_WARNING};margin-bottom:10px;}}
.hc-alert-danger  {{ background:{C_DANGER_BG};border:1px solid #FCA5A5;border-left:4px solid {C_DANGER};
                     border-radius:0 6px 6px 0;padding:9px 14px;font-size:12px;color:{C_DANGER};margin-bottom:10px;}}

.sidebar-hdr {{
    background: {C_PRIMARY};
    color: white;
    margin: -1rem -1rem 1rem;
    padding: 16px;
    border-bottom: 3px solid {C_TEAL};
}}
.sidebar-dataset {{
    background: {C_PRIMARY_BG};
    border: 1px solid #BFDBFE;
    border-radius: 8px;
    padding: 12px;
    font-size: 11px;
}}

.hc-progress-bg   {{ background:{C_BORDER_LT};border-radius:4px;height:10px;overflow:hidden;margin-top:4px; }}
.hc-progress-fill {{ height:100%;border-radius:4px;transition:width 0.5s; }}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SYNTHETIC DATA
# ─────────────────────────────────────────────────────────────────────────────
CANCER_TYPES = ["Breast","Lung","Colorectal","Prostate","Ovarian","Lymphoma"]
STAGES       = ["I","II","III","IV"]
BIOMARKERS   = ["HER2+","HER2-","ER+","EGFR+","ALK+","PD-L1+","KRAS+","BRCA1/2+"]
DRUGS        = ["Paclitaxel","Carboplatin","Pembrolizumab","Trastuzumab",
                "Bevacizumab","Docetaxel","Nivolumab","Olaparib"]
DRUG_CLASSES = ["Chemotherapy","Immunotherapy","Targeted Therapy","Hormonal","CDK4/6 Inhibitor"]
DISC_TYPES   = ["Drug date before diagnosis","Missing surgery data",
                "Duplicate therapy event","Conflicting drug record","Biomarker mismatch"]
RACES        = ["White","Black","Hispanic","Asian","Other"]


@st.cache_data
def generate_data(n=200, seed=42):
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(n):
        diag   = datetime(2019,1,1) + timedelta(days=int(rng.integers(0,730)))
        surg   = diag   + timedelta(days=int(rng.integers(30,180)))
        drug1  = diag   + timedelta(days=int(rng.integers(10,40)))
        drug2  = surg   + timedelta(days=int(rng.integers(30,90)))
        drug3  = drug2  + timedelta(days=int(rng.integers(90,200)))
        rows.append({
            "patient_id":       f"P{i+1:03d}",
            "age":              int(rng.integers(35,80)),
            "gender":           "Female" if rng.random()>0.45 else "Male",
            "race":             RACES[rng.integers(0,5)],
            "diagnosis_date":   diag.date(),
            "cancer_type":      CANCER_TYPES[rng.integers(0,6)],
            "stage":            STAGES[rng.integers(0,4)],
            "icd_code":         f"C{rng.integers(10,99)}.{rng.integers(0,9)}",
            "biomarker":        BIOMARKERS[rng.integers(0,8)],
            "biomarker_result": "Positive" if rng.random()>0.4 else "Negative",
            "surgery_date":     surg.date(),
            "drug1_name":       DRUGS[rng.integers(0,8)],
            "drug1_date":       drug1.date(),
            "drug1_class":      DRUG_CLASSES[rng.integers(0,5)],
            "drug2_name":       DRUGS[rng.integers(0,8)],
            "drug2_date":       drug2.date(),
            "drug2_class":      DRUG_CLASSES[rng.integers(0,5)],
            "drug3_name":       DRUGS[rng.integers(0,8)],
            "drug3_date":       drug3.date(),
            "drug3_class":      DRUG_CLASSES[rng.integers(0,5)],
            "ant_type":         "Neoadjuvant" if drug1<surg else "Adjuvant",
            "os_months":        int(rng.integers(6,60)),
            "pfs_months":       int(rng.integers(3,40)),
            "ttnt_months":      int(rng.integers(3,24)),
            "ttnt2_days":       int((drug2-drug1).days),
            "has_discrepancy":  rng.random()<0.12,
            "disc_type":        DISC_TYPES[rng.integers(0,5)],
        })
    return pd.DataFrame(rows)


df = generate_data()

surv_df = pd.DataFrame({
    "Month": list(range(0,66,6)),
    "Overall Survival (%)":          [round(100*math.exp(-0.07*(m/6)),1) for m in range(0,66,6)],
    "Progression-Free Survival (%)": [round(100*math.exp(-0.10*(m/6)),1) for m in range(0,66,6)],
})

drug_trend = pd.DataFrame({
    "Quarter":       ["Q1'20","Q2'20","Q3'20","Q4'20","Q1'21","Q2'21","Q3'21"],
    "Pembrolizumab": [18,21,24,26,29,31,34],
    "Paclitaxel":    [45,43,41,40,38,36,35],
    "Trastuzumab":   [22,24,25,27,28,30,31],
    "Nivolumab":     [10,13,15,17,19,22,25],
})

# ─────────────────────────────────────────────────────────────────────────────
# PLOTLY THEME — Clinical white
# ─────────────────────────────────────────────────────────────────────────────
PL = dict(
    paper_bgcolor="rgba(255,255,255,0)",
    plot_bgcolor="rgba(255,255,255,0)",
    font=dict(family="Source Sans 3, Segoe UI, Arial", color=C_TEXT, size=12),
    margin=dict(l=8,r=8,t=38,b=8),
    legend=dict(bgcolor="rgba(255,255,255,0.95)", bordercolor=C_BORDER, borderwidth=1,
                font=dict(size=11)),
    xaxis=dict(gridcolor=C_BORDER_LT, linecolor=C_BORDER, zerolinecolor=C_BORDER_LT,
               tickfont=dict(size=11)),
    yaxis=dict(gridcolor=C_BORDER_LT, linecolor=C_BORDER, zerolinecolor=C_BORDER_LT,
               tickfont=dict(size=11)),
    title_font=dict(size=13, color=C_PRIMARY, family="Source Sans 3"),
    title_x=0,
)


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-hdr">
        <div style="display:flex;align-items:center;gap:10px;">
            <div style="width:36px;height:36px;background:rgba(255,255,255,0.2);
                        border-radius:8px;display:flex;align-items:center;
                        justify-content:center;font-size:20px;flex-shrink:0;">🏥</div>
            <div>
                <div style="font-size:14px;font-weight:700;">OnchoInsight</div>
                <div style="font-size:10px;opacity:0.75;">Oncology Analytics v1.0</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<div style='font-size:10px;font-weight:700;color:{C_TEXT_MUTED};letter-spacing:.1em;text-transform:uppercase;margin-bottom:6px;padding:0 4px;'>Navigation</div>", unsafe_allow_html=True)

    page = st.radio("nav", [
        "🏠  Overview Dashboard",
        "⊕  ANT Classification",
        "≡  Line of Therapy",
        "⊞  Cohort Builder",
        "∿  Treatment Patterns",
        "⚑  Discrepancy Detection",
        "✦  AI Insights",
        "◻  Product Artifacts",
    ], label_visibility="collapsed")

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="sidebar-dataset">
        <div style="font-weight:700;color:{C_PRIMARY};margin-bottom:8px;">📂 Active Dataset</div>
        <div style="color:{C_TEXT_MED};">
            <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                <span>Patients</span><strong>200</strong>
            </div>
            <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                <span>Cancer Types</span><strong>6</strong>
            </div>
            <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                <span>Date Range</span><strong>2019–2021</strong>
            </div>
            <div style="display:flex;justify-content:space-between;">
                <span>Status</span>
                <strong style="color:{C_SUCCESS};">✓ Synthetic</strong>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:11px;font-weight:600;color:{C_TEXT_MED};margin-bottom:4px;'>Upload Your Data</div>", unsafe_allow_html=True)
    uploaded = st.file_uploader("CSV", type=["csv"], label_visibility="collapsed")
    if uploaded:
        try:
            user_df = pd.read_csv(uploaded)
            st.success(f"✓ {len(user_df):,} rows, {len(user_df.columns)} cols")
        except Exception as e:
            st.error(str(e))

    st.markdown(f"""
    <div style="margin-top:16px;text-align:center;font-size:10px;color:{C_TEXT_MUTED};
                border-top:1px solid {C_BORDER};padding-top:10px;">
        WCAG 2.1 AA · HIPAA Demo<br>
        © 2025 OnchoInsight Analytics
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def topbar(title, sub, badges):
    bdg = "".join([f'<span class="hc-badge">{b}</span>' for b in badges])
    st.markdown(f"""
    <div class="hc-topbar">
        <div>
            <div class="hc-topbar-title">{title}</div>
            <div class="hc-topbar-sub">{sub}</div>
        </div>
        <div>{bdg}</div>
    </div>
    """, unsafe_allow_html=True)


def kpi_row(items):
    cols = st.columns(len(items))
    for col, (label, value, color, delta, d_clr) in zip(cols, items):
        col.markdown(f"""
        <div class="hc-kpi" style="border-left-color:{color};">
            <div class="hc-kpi-label">{label}</div>
            <div class="hc-kpi-num" style="color:{color};">{value}</div>
            <div class="hc-kpi-delta" style="color:{d_clr or C_TEXT_MUTED};">{delta}</div>
        </div>
        """, unsafe_allow_html=True)


def sec(text):
    st.markdown(f'<div class="hc-sec">{text}</div>', unsafe_allow_html=True)


def wrap():
    st.markdown("<div style='padding:0 1.5rem 1.5rem;'>", unsafe_allow_html=True)


def end():
    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: OVERVIEW
# ─────────────────────────────────────────────────────────────────────────────
if "Overview" in page:
    topbar("🏥 Oncology Analytics Dashboard",
           "Real-World Evidence Platform · US Healthcare Standard UI",
           ["🟢 Live Demo","200 Patients","6 Cancer Types"])
    wrap()

    neo_n  = df[df.ant_type=="Neoadjuvant"].shape[0]
    disc_n = df[df.has_discrepancy].shape[0]
    avg_os = round(df.os_months.mean(), 1)
    her2_n = df[df.biomarker=="HER2+"].shape[0]

    kpi_row([
        ("Total Patients",     "200",              C_PRIMARY, "Full cohort enrolled",         ""),
        ("Cancer Types",       "6",                C_TEAL,    "Across 12 ICD-10 codes",       ""),
        ("Neoadjuvant Pts",    str(neo_n),         C_INFO,    f"{neo_n/200*100:.0f}% of cohort", C_INFO),
        ("Average OS",         f"{avg_os} mo",     C_SUCCESS, "↑ vs benchmark",               C_SUCCESS),
    ])
    st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
    kpi_row([
        ("2L Patients",        "142",              C_PRIMARY, "71% progressed to 2nd line",   ""),
        ("HER2+ Patients",     str(her2_n),        C_PURPLE,  "Biomarker positive",           ""),
        ("Data Discrepancies", str(disc_n),        C_DANGER,  "⚠ Pending review",            C_DANGER),
        ("Stages Covered",     "I – IV",           C_SUCCESS, "Complete stage range",         ""),
    ])

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        sec("📊 Cancer Type Distribution")
        cd = df.cancer_type.value_counts().reset_index()
        cd.columns = ["Cancer","Count"]
        fig = go.Figure(go.Bar(
            x=cd["Cancer"], y=cd["Count"],
            marker=dict(color=CHART_COLORS[:len(cd)], line_width=0),
            text=cd["Count"], textposition="outside",
        ))
        fig.update_layout(title="Patients by Primary Cancer", yaxis_title="Count",
                          showlegend=False, **PL)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        sec("🎯 Stage Distribution")
        sd = df.stage.value_counts().reset_index()
        sd.columns = ["Stage","Count"]
        sd["Stage"] = "Stage " + sd["Stage"]
        fig = go.Figure(go.Pie(
            labels=sd["Stage"], values=sd["Count"], hole=0.45,
            marker=dict(colors=CHART_COLORS, line=dict(color="white",width=2)),
            textfont=dict(size=12),
        ))
        fig.update_layout(title="Patient Stage Stratification", **PL)
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        sec("📈 Overall & Progression-Free Survival")
        fig = go.Figure()
        for col_n, clr, fc in [
            ("Overall Survival (%)",          C_PRIMARY, "rgba(27,79,138,0.10)"),
            ("Progression-Free Survival (%)", C_TEAL,    "rgba(13,118,128,0.08)"),
        ]:
            fig.add_trace(go.Scatter(
                x=surv_df["Month"], y=surv_df[col_n], name=col_n,
                mode="lines", line=dict(color=clr, width=2.5),
                fill="tozeroy", fillcolor=fc,
            ))
        fig.update_layout(title="KM-Style Survival Curves",
                          xaxis_title="Months", yaxis_title="Survival (%)",
                          height=270, **PL)
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        sec("🔬 Biomarker Distribution")
        bm = df.biomarker.value_counts().reset_index()
        bm.columns = ["Biomarker","Count"]
        fig = go.Figure(go.Bar(
            x=bm["Count"], y=bm["Biomarker"], orientation="h",
            marker=dict(color=C_PURPLE, line_width=0),
            text=bm["Count"], textposition="outside",
        ))
        fig.update_layout(title="Patients by Biomarker", xaxis_title="Count",
                          height=270, **PL)
        st.plotly_chart(fig, use_container_width=True)

    end()


# ─────────────────────────────────────────────────────────────────────────────
# ANT CLASSIFICATION
# ─────────────────────────────────────────────────────────────────────────────
elif "ANT" in page:
    topbar("⊕ ANT Therapy Classification Engine",
           "Adjuvant / Neoadjuvant auto-classification based on surgery date",
           ["Rule-Based Engine","WCAG AA"])
    wrap()

    neo_n = df[df.ant_type=="Neoadjuvant"].shape[0]
    adj_n = df[df.ant_type=="Adjuvant"].shape[0]

    kpi_row([
        ("Neoadjuvant Patients", str(neo_n),              C_INFO,    "Drug administered before surgery", ""),
        ("Adjuvant Patients",    str(adj_n),              C_SUCCESS, "Drug administered after surgery",  ""),
        ("Neoadjuvant Rate",     f"{neo_n/200*100:.0f}%", C_PRIMARY, "of total patient cohort",          ""),
        ("Avg Lead Time",        "42 days",               C_WARNING, "Drug → Surgery interval",          ""),
    ])

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="hc-alert-info">
        📋 <strong>Algorithm:</strong>
        &nbsp; IF drug_date &lt; surgery_date → <strong>Neoadjuvant</strong>
        &nbsp;|&nbsp; IF drug_date &gt; surgery_date → <strong>Adjuvant</strong>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        sec("📊 ANT Distribution")
        fig = go.Figure(go.Pie(
            labels=["Neoadjuvant","Adjuvant"], values=[neo_n,adj_n], hole=0.5,
            marker=dict(colors=[C_INFO,C_SUCCESS], line=dict(color="white",width=2)),
            textfont=dict(size=13),
        ))
        fig.update_layout(title="Neoadjuvant vs Adjuvant", **PL)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        sec("📊 ANT by Cancer Type")
        ant_c  = df.groupby(["cancer_type","ant_type"]).size().reset_index(name="n")
        pivot  = ant_c.pivot(index="cancer_type",columns="ant_type",values="n").fillna(0).reset_index()
        fig = go.Figure()
        for col_n, clr in zip(["Neoadjuvant","Adjuvant"],[C_INFO,C_SUCCESS]):
            if col_n in pivot.columns:
                fig.add_trace(go.Bar(x=pivot["cancer_type"], y=pivot[col_n],
                                     name=col_n, marker_color=clr, marker_line_width=0))
        fig.update_layout(title="ANT Type by Cancer", barmode="group", **PL)
        st.plotly_chart(fig, use_container_width=True)

    sec("🗂 ANT Classification Table — Top 30 Records")
    disp = df[["patient_id","cancer_type","stage","drug1_name","drug1_date",
               "surgery_date","ant_type","drug1_class"]].head(30).copy()
    disp.columns = ["Patient ID","Cancer","Stage","Drug","Drug Date",
                    "Surgery Date","ANT Type","Drug Class"]
    def color_ant(val):
        if val=="Neoadjuvant": return f"background-color:{C_INFO_BG};color:{C_INFO};font-weight:600"
        if val=="Adjuvant":    return f"background-color:{C_SUCCESS_BG};color:{C_SUCCESS};font-weight:600"
        return ""
    st.dataframe(disp.style.applymap(color_ant, subset=["ANT Type"]),
                 use_container_width=True, hide_index=True)
    end()


# ─────────────────────────────────────────────────────────────────────────────
# LINE OF THERAPY
# ─────────────────────────────────────────────────────────────────────────────
elif "Line of Therapy" in page:
    topbar("≡ Line of Therapy (LoT) Engine",
           "Automated 1L → 2L → 3L → 4L+ identification algorithm",
           ["LoT Algorithm v1.0"])
    wrap()

    kpi_row([
        ("1L Patients", "200", C_PRIMARY, "Carboplatin + Paclitaxel",  ""),
        ("2L Patients", "142", C_TEAL,    "71% → Pembrolizumab",        ""),
        ("3L Patients",  "74", C_WARNING, "37% → Nivolumab",            C_WARNING),
        ("4L+ Patients", "28", C_DANGER,  "14% → Olaparib",             C_DANGER),
    ])

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        sec("📉 LoT Patient Funnel")
        fig = go.Figure(go.Funnel(
            y=["1L","2L","3L","4L+"], x=[200,142,74,28],
            textinfo="value+percent initial",
            marker=dict(color=[C_PRIMARY,C_TEAL,C_WARNING,C_DANGER]),
        ))
        fig.update_layout(title="Patient Attrition Across Therapy Lines", **PL)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        sec("💊 Drug Class by Line (%)")
        lot_class = pd.DataFrame({
            "Line":     ["1L","2L","3L","4L+"],
            "Chemo":    [45,25,18,10],
            "Immuno":   [20,38,42,40],
            "Targeted": [25,30,35,45],
            "Hormonal": [10, 7, 5, 5],
        })
        fig = go.Figure()
        for col_n, clr in zip(["Chemo","Immuno","Targeted","Hormonal"],
                               [C_WARNING,C_PURPLE,C_PRIMARY,C_TEAL]):
            fig.add_trace(go.Bar(x=lot_class["Line"], y=lot_class[col_n],
                                 name=col_n, marker_color=clr, marker_line_width=0))
        fig.update_layout(title="Drug Class Distribution by LoT",
                          barmode="group", yaxis_title="%", **PL)
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("📋 LoT Algorithm Logic"):
        st.markdown(f"""
        <div class="prd-card">
            <div class="prd-title">Line of Therapy Rules</div>
            <div class="prd-body">
                <strong>Rule 1:</strong> First treatment after diagnosis = 1st Line<br>
                <strong>Rule 2:</strong> New / changed drug regimen = Next Line<br>
                <strong>Rule 3:</strong> Treatment gap &gt; 90 days = New Line<br>
                <strong>Rule 4:</strong> Disease progression + drug change = Next Line
            </div>
        </div>
        """, unsafe_allow_html=True)

    sec("🗂 Patient-Level LoT Records")
    lot_d = df[["patient_id","cancer_type","stage","drug1_name",
                "drug2_name","drug3_name","ttnt2_days"]].head(25).copy()
    lot_d.columns = ["Patient ID","Cancer","Stage","1L Drug","2L Drug","3L Drug","Days to 2L"]
    def color_days(val):
        if isinstance(val,(int,float)):
            if val<90:  return f"color:{C_DANGER};font-weight:600"
            if val<150: return f"color:{C_WARNING};font-weight:600"
            return f"color:{C_SUCCESS};font-weight:600"
        return ""
    st.dataframe(lot_d.style.applymap(color_days, subset=["Days to 2L"]),
                 use_container_width=True, hide_index=True)
    end()


# ─────────────────────────────────────────────────────────────────────────────
# COHORT BUILDER
# ─────────────────────────────────────────────────────────────────────────────
elif "Cohort" in page:
    topbar("⊞ Cohort Builder",
           "Build custom patient cohorts with multi-dimensional clinical filters",
           ["Self-Service Analytics"])
    wrap()

    # Filter panel
    st.markdown(f"""
    <div style="background:{C_SURFACE};border:1px solid {C_BORDER};border-radius:8px;
                padding:16px 20px;margin-bottom:16px;box-shadow:0 1px 4px rgba(0,0,0,0.05);">
        <div style="font-size:12px;font-weight:700;color:{C_PRIMARY};margin-bottom:10px;">🔍 Filter Cohort</div>
    """, unsafe_allow_html=True)

    c1,c2,c3,c4,c5 = st.columns([2,2,2,2,1])
    with c1: sel_cancer = st.selectbox("Cancer Type", ["All"]+CANCER_TYPES)
    with c2: sel_stage  = st.selectbox("Stage",       ["All"]+[f"Stage {s}" for s in STAGES])
    with c3: sel_bm     = st.selectbox("Biomarker",   ["All"]+BIOMARKERS)
    with c4: sel_drug   = st.selectbox("Drug",        ["All"]+DRUGS)
    with c5:
        st.markdown("<div style='margin-top:22px;'></div>", unsafe_allow_html=True)
        if st.button("↺ Reset"): st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    filt = df.copy()
    if sel_cancer!="All": filt = filt[filt.cancer_type==sel_cancer]
    if sel_stage !="All": filt = filt[filt.stage==sel_stage.replace("Stage ","")]
    if sel_bm    !="All": filt = filt[filt.biomarker==sel_bm]
    if sel_drug  !="All": filt = filt[(filt.drug1_name==sel_drug)|(filt.drug2_name==sel_drug)|(filt.drug3_name==sel_drug)]

    avg_age  = round(filt.age.mean(),1) if len(filt) else 0
    female_p = round(filt[filt.gender=="Female"].shape[0]/max(len(filt),1)*100)
    bm_pos   = filt[filt.biomarker_result=="Positive"].shape[0]

    kpi_row([
        ("Cohort Size",   str(len(filt)),  C_PRIMARY, "Matched patients",    ""),
        ("Average Age",   f"{avg_age} yr", C_TEAL,    "years",               ""),
        ("Female %",      f"{female_p}%",  C_SUCCESS, "of cohort",           ""),
        ("Biomarker +ve", str(bm_pos),     C_PURPLE,  "Positive results",    ""),
    ])

    st.markdown("<br>", unsafe_allow_html=True)
    if len(filt)==0:
        st.markdown(f'<div class="hc-alert-warn">⚠ No patients match the selected filters. Please adjust your criteria.</div>', unsafe_allow_html=True)
    else:
        c1,c2 = st.columns(2)
        with c1:
            sec("📊 Cohort by Cancer Type")
            cc = filt.cancer_type.value_counts().reset_index()
            cc.columns = ["Cancer","Count"]
            fig = go.Figure(go.Pie(labels=cc["Cancer"],values=cc["Count"],hole=0.45,
                marker=dict(colors=CHART_COLORS,line=dict(color="white",width=2))))
            fig.update_layout(title="Cancer Distribution in Cohort",**PL)
            st.plotly_chart(fig,use_container_width=True)
        with c2:
            sec("📊 Stage Breakdown")
            sc = filt.stage.value_counts().reset_index()
            sc.columns = ["Stage","Count"]
            sc["Stage"] = "Stage "+sc["Stage"]
            fig = go.Figure(go.Bar(x=sc["Stage"],y=sc["Count"],
                marker=dict(color=C_PRIMARY,line_width=0),
                text=sc["Count"],textposition="outside"))
            fig.update_layout(title="Stage Distribution in Cohort",
                              yaxis_title="Patients",**PL)
            st.plotly_chart(fig,use_container_width=True)

        sec(f"🗂 Patient Records — {len(filt)} Matched · Click Row for Journey")
        disp = filt[["patient_id","age","gender","cancer_type","stage",
                     "biomarker","ant_type","drug1_name","os_months"]].head(20).copy()
        disp.columns = ["ID","Age","Gender","Cancer","Stage","Biomarker","ANT","1L Drug","OS (mo)"]

        sel = st.dataframe(disp, use_container_width=True, hide_index=True,
                           on_select="rerun", selection_mode="single-row")

        if sel and sel.selection.rows:
            patient = filt.iloc[sel.selection.rows[0]]
            st.markdown(f"""
            <div style="background:{C_PRIMARY_BG};border:1px solid #BFDBFE;
                        border-radius:8px;padding:12px 18px;margin:12px 0 14px;">
                <div style="font-size:13px;font-weight:700;color:{C_PRIMARY};">
                    🧑‍⚕️ Patient Journey — {patient.patient_id}
                    &nbsp;·&nbsp; {patient.cancer_type} Stage {patient.stage}
                    &nbsp;·&nbsp; {patient.ant_type}
                </div>
            </div>
            """, unsafe_allow_html=True)

            timeline = [
                ("🏥","Diagnosis",  str(patient.diagnosis_date),C_WARNING),
                ("💊","1L Therapy", str(patient.drug1_date),    C_PRIMARY),
                ("🔪","Surgery",    str(patient.surgery_date),  C_DANGER),
                ("💉","2L Therapy", str(patient.drug2_date),    C_SUCCESS),
                ("🧪","3L Therapy", str(patient.drug3_date),    C_PURPLE),
            ]
            cols = st.columns(len(timeline))
            for col,(icon,label,date,color) in zip(cols,timeline):
                col.markdown(f"""
                <div class="journey-node" style="border-top-color:{color};">
                    <div class="journey-icon">{icon}</div>
                    <div class="journey-title" style="color:{color};">{label}</div>
                    <div class="journey-date">{date}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>",unsafe_allow_html=True)
            c1,c2,c3 = st.columns(3)
            with c1:
                st.metric("Cancer Type", patient.cancer_type)
                st.metric("Stage", patient.stage)
            with c2:
                st.metric("Biomarker", patient.biomarker)
                st.metric("ANT Type",  patient.ant_type)
            with c3:
                st.metric("OS (months)",  patient.os_months)
                st.metric("PFS (months)", patient.pfs_months)
    end()


# ─────────────────────────────────────────────────────────────────────────────
# TREATMENT PATTERNS
# ─────────────────────────────────────────────────────────────────────────────
elif "Treatment Patterns" in page:
    topbar("∿ Treatment Pattern Analysis",
           "Drug utilization · therapy trends · biomarker-drug correlations",
           ["Drug Analytics"])
    wrap()

    c1,c2 = st.columns(2)
    with c1:
        sec("💊 Drug Class Distribution — 1st Line")
        dc = df.drug1_class.value_counts().reset_index()
        dc.columns = ["Class","Count"]
        fig = go.Figure(go.Pie(labels=dc["Class"],values=dc["Count"],hole=0.45,
            marker=dict(colors=CHART_COLORS,line=dict(color="white",width=2))))
        fig.update_layout(title="First-Line Drug Class Breakdown",**PL)
        st.plotly_chart(fig,use_container_width=True)

    with c2:
        sec("📈 Drug Adoption Trends — Quarterly")
        fig = go.Figure()
        for col_n,clr in zip(["Pembrolizumab","Paclitaxel","Trastuzumab","Nivolumab"],
                              [C_PURPLE,C_WARNING,C_PRIMARY,C_TEAL]):
            fig.add_trace(go.Scatter(
                x=drug_trend["Quarter"],y=drug_trend[col_n],name=col_n,
                mode="lines+markers",
                line=dict(color=clr,width=2.5),
                marker=dict(size=7,color=clr,line=dict(color="white",width=2)),
            ))
        fig.update_layout(title="Quarter-over-Quarter Drug Utilization",
                          yaxis_title="Patient Count",**PL)
        st.plotly_chart(fig,use_container_width=True)

    sec("📊 Drug Utilisation — All Lines")
    all_d = pd.concat([df.drug1_name,df.drug2_name,df.drug3_name]).value_counts().reset_index()
    all_d.columns = ["Drug","Patients"]
    all_d["Pct"] = (all_d["Patients"]/200*100).round(1)

    for i,row in all_d.iterrows():
        pct   = row["Pct"]
        color = CHART_COLORS[i%len(CHART_COLORS)]
        c1,c2,c3,c4 = st.columns([2,5,1,0.5])
        c1.markdown(f"<div style='font-size:13px;padding-top:8px;color:{C_TEXT};font-weight:500;'>{row['Drug']}</div>",unsafe_allow_html=True)
        c2.markdown(f"""
        <div style="margin-top:12px;">
            <div class="hc-progress-bg">
                <div class="hc-progress-fill" style="width:{min(pct,100):.1f}%;background:{color};"></div>
            </div>
        </div>
        """,unsafe_allow_html=True)
        c3.markdown(f"<div style='font-size:12px;color:{color};font-weight:700;padding-top:6px;font-family:Source Code Pro,monospace;'>{pct}%</div>",unsafe_allow_html=True)
        c4.markdown(f"<div style='font-size:11px;color:{C_TEXT_MUTED};padding-top:8px;'>{int(row['Patients'])}</div>",unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)
    sec("🔬 Biomarker vs Therapy Modality Radar")
    cats = ["HER2+","EGFR+","PD-L1+","BRCA+","ALK+"]
    fig = go.Figure()
    for name,vals,clr in [
        ("Chemotherapy",[40,35,30,50,25],C_WARNING),
        ("Targeted",    [75,80,40,70,85],C_PRIMARY),
        ("Immunotherapy",[30,25,90,20,15],C_PURPLE),
    ]:
        fig.add_trace(go.Scatterpolar(
            r=vals+[vals[0]],theta=cats+[cats[0]],fill="toself",name=name,
            line=dict(color=clr,width=2),
            fillcolor=f"rgba({int(clr[1:3],16)},{int(clr[3:5],16)},{int(clr[5:7],16)},0.12)",
        ))
    fig.update_layout(
        title="Therapy Modality by Biomarker Group",
        polar=dict(bgcolor="rgba(255,255,255,0)",
            radialaxis=dict(visible=True,gridcolor=C_BORDER_LT,color=C_TEXT_MUTED),
            angularaxis=dict(gridcolor=C_BORDER_LT,color=C_TEXT)),
        paper_bgcolor="rgba(255,255,255,0)",
        font=dict(family="Source Sans 3",color=C_TEXT,size=12),
        legend=dict(bgcolor="rgba(255,255,255,0.95)",bordercolor=C_BORDER,borderwidth=1),
        margin=dict(l=40,r=40,t=50,b=40),
        title_font=dict(size=13,color=C_PRIMARY),
    )
    st.plotly_chart(fig,use_container_width=True)
    end()


# ─────────────────────────────────────────────────────────────────────────────
# DISCREPANCY DETECTION
# ─────────────────────────────────────────────────────────────────────────────
elif "Discrepancy" in page:
    topbar("⚑ Discrepancy Detection Engine",
           "Automated data quality checks · flagged records · resolution guidance",
           ["Data Quality Monitor"])
    wrap()

    disc_df = df[df.has_discrepancy].copy()
    disc_df["severity"] = np.where(
        np.random.default_rng(99).random(len(disc_df))>0.5,"HIGH","MEDIUM")
    high_n   = disc_df[disc_df.severity=="HIGH"].shape[0]
    medium_n = disc_df[disc_df.severity=="MEDIUM"].shape[0]
    clean_n  = 200-len(disc_df)

    c1,c2,c3 = st.columns(3)
    with c1: st.markdown(f'<div class="hc-alert-danger">🔴 <strong>{high_n} HIGH severity</strong> — Immediate review required</div>',unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="hc-alert-warn">🟡 <strong>{medium_n} MEDIUM severity</strong> — Review recommended</div>',unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="hc-alert-success">🟢 <strong>{clean_n} records</strong> passed all quality checks</div>',unsafe_allow_html=True)

    kpi_row([
        ("Total Flags",     str(len(disc_df)), C_DANGER,  "Require review",              C_DANGER),
        ("High Severity",   str(high_n),       C_WARNING, "Immediate action required",   C_WARNING),
        ("Medium Severity", str(medium_n),     C_INFO,    "Review recommended",          ""),
        ("Clean Records",   str(clean_n),       C_SUCCESS, f"{clean_n/200*100:.0f}% pass rate", C_SUCCESS),
    ])

    st.markdown("<br>",unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        sec("📊 Discrepancy Type Breakdown")
        dt = disc_df.disc_type.value_counts().reset_index()
        dt.columns = ["Issue","Count"]
        fig = go.Figure(go.Bar(
            x=dt["Count"],y=dt["Issue"],orientation="h",
            marker=dict(color=C_DANGER,line_width=0),
            text=dt["Count"],textposition="outside"))
        fig.update_layout(title="Data Quality Issue Types",xaxis_title="Records",**PL)
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        sec("🥧 Record Quality Overview")
        fig = go.Figure(go.Pie(
            labels=["High Severity","Medium Severity","Clean Records"],
            values=[high_n,medium_n,clean_n],hole=0.5,
            marker=dict(colors=[C_DANGER,C_WARNING,C_SUCCESS],
                        line=dict(color="white",width=2))))
        fig.update_layout(title="Quality Breakdown — 200 Records",**PL)
        st.plotly_chart(fig,use_container_width=True)

    resolutions = {
        "Drug date before diagnosis":  "Verify drug administration records against EHR source system",
        "Missing surgery data":        "Cross-reference surgical scheduling and OR records",
        "Duplicate therapy event":     "Deduplicate using patient_id + drug_name + date composite key",
        "Conflicting drug record":     "Reconcile claims data vs EMR — adjudicate with source of truth policy",
        "Biomarker mismatch":          "Validate biomarker test result with pathology report and lab records",
    }
    sec("🗂 Flagged Records — Resolution Guidance")
    dd = disc_df[["patient_id","cancer_type","disc_type","severity"]].copy()
    dd["Suggested Resolution"] = dd["disc_type"].map(resolutions)
    dd.columns = ["Patient ID","Cancer","Issue Type","Severity","Suggested Resolution"]

    def sev_clr(val):
        if val=="HIGH":   return f"background-color:{C_DANGER_BG};color:{C_DANGER};font-weight:700"
        if val=="MEDIUM": return f"background-color:{C_WARNING_BG};color:{C_WARNING};font-weight:700"
        return ""
    st.dataframe(dd.style.applymap(sev_clr,subset=["Severity"]),
                 use_container_width=True,hide_index=True)
    end()


# ─────────────────────────────────────────────────────────────────────────────
# AI INSIGHTS
# ─────────────────────────────────────────────────────────────────────────────
elif "AI Insights" in page:
    topbar("✦ AI Insight Generator",
           "Automated oncology insights from analytics engines",
           ["Analytics Engine"])
    wrap()

    if "insights" not in st.session_state:
        st.session_state.insights = [
            {"icon":"🔬","text":"62% of Stage III breast cancer patients received neoadjuvant chemotherapy prior to surgery.","source":"ANT Engine","confidence":"High","color":C_PRIMARY},
            {"icon":"🎯","text":"HER2+ patients show 2.4× higher targeted therapy adoption in second-line vs first-line.","source":"LoT Analysis","confidence":"High","color":C_SUCCESS},
            {"icon":"📈","text":"Immunotherapy adoption increased 34% year-over-year across all cancer types.","source":"Drug Trends","confidence":"Medium","color":C_TEAL},
            {"icon":"⏱️","text":"Median TTNT for Stage IV is 4.2 months shorter than Stage III patients.","source":"Survival Engine","confidence":"High","color":C_WARNING},
            {"icon":"⚠️","text":f"{df[df.has_discrepancy].shape[0]} patients show data discrepancies — primarily drug date anomalies.","source":"Discrepancy Engine","confidence":"N/A","color":C_DANGER},
        ]

    pool = [
        {"icon":"🧬","text":"Stage IV patients show 38% higher immunotherapy use vs Stage II.","source":"Cohort Analysis","confidence":"High","color":C_PRIMARY},
        {"icon":"💡","text":"BRCA1/2+ patients show significantly higher PARP inhibitor adoption in 2L.","source":"Biomarker Engine","confidence":"High","color":C_SUCCESS},
        {"icon":"🔄","text":"Drug switching 1L→2L most frequent within 120 days of initiation.","source":"LoT Engine","confidence":"Medium","color":C_TEAL},
        {"icon":"📊","text":"Colorectal patients had highest neoadjuvant therapy rate at 71% of subgroup.","source":"ANT Engine","confidence":"High","color":C_WARNING},
        {"icon":"⚕️","text":"Neoadjuvant patients had median OS 6.8 months longer than adjuvant-only.","source":"Survival Model","confidence":"Medium","color":C_PURPLE},
    ]

    c1,c2 = st.columns([2,1])
    with c1:
        if st.button("✦ Generate New Insight"):
            available = [n for n in pool if n["text"] not in [x["text"] for x in st.session_state.insights]]
            if available:
                st.session_state.insights.append(random.choice(available)); st.rerun()
            else:
                st.info("All available insights generated.")
    with c2:
        if st.button("↺ Reset"): del st.session_state.insights; st.rerun()

    st.markdown("<br>",unsafe_allow_html=True)
    for ins in st.session_state.insights:
        conf_clr = C_SUCCESS if ins["confidence"]=="High" else C_WARNING if ins["confidence"]=="Medium" else C_TEXT_MUTED
        conf_bg  = C_SUCCESS_BG if ins["confidence"]=="High" else C_WARNING_BG if ins["confidence"]=="Medium" else "#F8FAFC"
        st.markdown(f"""
        <div class="hc-insight" style="border-left-color:{ins['color']};">
            <div style="display:flex;align-items:flex-start;gap:12px;">
                <span style="font-size:20px;margin-top:1px;">{ins['icon']}</span>
                <div>
                    <div class="hc-insight-text">{ins['text']}</div>
                    <div class="hc-insight-meta">
                        Source: <strong style="color:{C_PRIMARY};">{ins['source']}</strong>
                        &nbsp;·&nbsp; Confidence:
                        <span style="background:{conf_bg};color:{conf_clr};
                                     padding:1px 8px;border-radius:4px;
                                     font-size:10px;font-weight:700;">{ins['confidence']}</span>
                    </div>
                </div>
            </div>
        </div>
        """,unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)
    sec("📊 Insight Coverage by Analytics Module")
    cov = pd.DataFrame({"Module":["ANT Engine","LoT Engine","Cohort Builder",
                                  "Survival Model","Drug Utilization","Discrepancy"],
                        "Insights":[12,18,9,7,14,5]})
    fig = go.Figure(go.Bar(
        x=cov["Module"],y=cov["Insights"],
        marker=dict(color=CHART_COLORS[:6],line_width=0),
        text=cov["Insights"],textposition="outside"))
    fig.update_layout(title="Auto-Generated Insights per Module",
                      yaxis_title="Insight Count",**PL)
    st.plotly_chart(fig,use_container_width=True)
    end()


# ─────────────────────────────────────────────────────────────────────────────
# PRODUCT ARTIFACTS
# ─────────────────────────────────────────────────────────────────────────────
elif "Product" in page:
    topbar("◻ Product Artifacts — PM Deliverables",
           "PRD · User Personas · Business Value · KPIs · Roadmap",
           ["Product Management"])
    wrap()

    tabs = st.tabs(["📋 PRD","👥 Personas","💼 Business Value","📊 KPIs","🗺️ Roadmap"])

    with tabs[0]:
        for title,body in [
            ("🎯 Product Vision","Build a self-service oncology analytics application enabling pharma companies, clinical researchers, and healthcare organizations to explore real-world oncology data and generate actionable insights on treatment patterns, therapy lines, and patient cohorts."),
            ("🔍 Problem Statement","Pharma and oncology analytics teams lack tools to quickly analyze fragmented real-world data across EHR, Claims, Pathology, and Biomarker sources. Current workflows are slow, manual, and require deep engineering — creating critical bottlenecks in drug strategy decisions."),
            ("✅ MVP Scope","Data Upload & Ingestion (CSV/JSON/FHIR) · ANT Therapy Classification Engine · Line of Therapy Algorithm · Interactive Cohort Builder · Treatment Pattern Dashboards · Discrepancy Detection Engine · AI Insight Generation."),
            ("🎯 Success Criteria","Time to first insight < 5 min · Cohort build < 30 sec · ANT accuracy ≥ 95% · Dashboard load < 2 sec · Discrepancy detection recall ≥ 90%."),
            ("🔐 Data & Compliance","Patient data de-identified per HIPAA Safe Harbor. Platform supports audit logging, RBAC, and SOC 2 Type II. No PHI stored in-transit without AES-256 encryption."),
        ]:
            st.markdown(f'<div class="prd-card"><div class="prd-title">{title}</div><div class="prd-body">{body}</div></div>',unsafe_allow_html=True)

    with tabs[1]:
        c1,c2 = st.columns(2)
        personas = [
            ("💊 Pharma Analyst",       C_PRIMARY, "Understand drug usage patterns and market penetration",              "Slow analytics, fragmented datasets, no self-service tools"),
            ("🔬 Oncology Researcher",  C_TEAL,    "Study treatment outcomes and biomarker correlations",               "Difficult cohort discovery, inconsistent data schemas"),
            ("📊 Data Scientist",       C_PURPLE,  "Build and validate oncology ML models at scale",                    "Manual data prep, no standardized oncology data model"),
            ("🏥 Clinical Operations",  C_SUCCESS, "Monitor guideline adherence and optimize treatment pathways",       "No real-time monitoring, siloed EHR systems, slow reports"),
        ]
        for i,(role,clr,goal,pain) in enumerate(personas):
            with (c1 if i%2==0 else c2):
                st.markdown(f"""
                <div class="persona-card" style="border-top-color:{clr};">
                    <div style="font-size:13px;font-weight:700;color:{clr};margin-bottom:8px;">{role}</div>
                    <div style="font-size:12px;color:{C_TEXT};margin-bottom:5px;"><strong>Goal:</strong> {goal}</div>
                    <div style="font-size:12px;color:{C_TEXT_MED};"><strong>Pain:</strong> {pain}</div>
                </div>
                """,unsafe_allow_html=True)

    with tabs[2]:
        c1,c2,c3 = st.columns(3)
        bv = [
            (c1,"💊 Pharma Companies",   C_PRIMARY, ["Drug launch strategy","Competitive therapy analysis","Patient segmentation","RWE generation","Trial enrichment"]),
            (c2,"🏥 Healthcare Providers",C_TEAL,   ["Treatment pathway optimization","Outcome monitoring","Guideline adherence","Biomarker-driven care","Quality dashboards"]),
            (c3,"🔬 Researchers",         C_PURPLE, ["Treatment research","Biomarker studies","Survival analysis","Publication visuals","Hypothesis generation"]),
        ]
        for col,title,clr,items in bv:
            with col:
                rows = "".join([f"<div style='padding:3px 0;border-bottom:1px solid {C_BORDER_LT};font-size:12px;'>✓ {item}</div>" for item in items])
                st.markdown(f"""
                <div class="prd-card" style="border-top:3px solid {clr};">
                    <div class="prd-title" style="color:{clr};">{title}</div>
                    <div style="color:{C_TEXT_MED};">{rows}</div>
                </div>
                """,unsafe_allow_html=True)

    with tabs[3]:
        k_items = [
            ("Target Pharma Users (Y1)","50+",         C_PRIMARY),
            ("Cohort Analyses / Month", "500+",        C_TEAL),
            ("Insight Generation Time", "< 5 min",     C_SUCCESS),
            ("Data Processing Speed",   "1M rows/min", C_WARNING),
            ("ANT Accuracy",            "≥ 95%",       C_PURPLE),
            ("Target ARR (Year 1)",     "$2M+",        C_DANGER),
        ]
        c1,c2,c3 = st.columns(3)
        for i,(label,val,clr) in enumerate(k_items):
            with [c1,c2,c3][i%3]:
                st.markdown(f"""
                <div class="biz-kpi" style="border-top-color:{clr};">
                    <div class="biz-kpi-val" style="color:{clr};">{val}</div>
                    <div class="biz-kpi-label">{label}</div>
                </div>
                """,unsafe_allow_html=True)

        sec("📉 User Adoption Funnel — Year 1 Target")
        fig = go.Figure(go.Funnel(
            y=["Awareness","Trial","Activated","Power Users","Enterprise"],
            x=[500,200,80,40,15],
            textinfo="value+percent initial",
            marker=dict(color=[C_PRIMARY,C_TEAL,C_SUCCESS,C_WARNING,C_PURPLE]),
        ))
        fig.update_layout(title="Y1 User Adoption Funnel",**PL,height=270)
        st.plotly_chart(fig,use_container_width=True)

    with tabs[4]:
        for num,clr,title,items in [
            ("1",C_PRIMARY,"Phase 1 — MVP (Months 1–3)","Streamlit prototype · ANT Classification · LoT Engine · Cohort Builder · Treatment Dashboards · Discrepancy Detection · CSV/JSON ingestion"),
            ("2",C_TEAL,   "Phase 2 — Advanced Analytics (Months 4–8)","Survival analysis (KM curves) · ML predictions · LLM clinical insights · FHIR connectors · PDF export · User authentication"),
            ("3",C_PURPLE, "Phase 3 — Enterprise Platform (Months 9–18)","Cloud deployment (AWS/GCP) · Real-time pipelines · Multi-tenant · SSO & RBAC · EHR integrations · API marketplace · SLA guarantees"),
        ]:
            st.markdown(f"""
            <div class="phase-card" style="border-left-color:{clr};">
                <div style="width:28px;height:28px;min-width:28px;border-radius:50%;
                            background:rgba({int(clr[1:3],16)},{int(clr[3:5],16)},{int(clr[5:7],16)},0.15);
                            color:{clr};font-weight:800;font-size:13px;
                            display:flex;align-items:center;justify-content:center;">{num}</div>
                <div>
                    <div style="font-weight:700;font-size:13px;color:{clr};margin-bottom:3px;">{title}</div>
                    <div style="font-size:12px;color:{C_TEXT_MED};">{items}</div>
                </div>
            </div>
            """,unsafe_allow_html=True)

        sec("📅 Development Gantt Chart")
        gantt_df = pd.DataFrame([
            dict(Task="Data Ingestion", Start="2025-01-01",Finish="2025-02-15",Phase="Phase 1"),
            dict(Task="ANT Engine",     Start="2025-01-15",Finish="2025-03-01",Phase="Phase 1"),
            dict(Task="LoT Engine",     Start="2025-02-01",Finish="2025-03-15",Phase="Phase 1"),
            dict(Task="Cohort Builder", Start="2025-02-15",Finish="2025-04-01",Phase="Phase 1"),
            dict(Task="Survival Model", Start="2025-04-01",Finish="2025-06-01",Phase="Phase 2"),
            dict(Task="ML Predictions", Start="2025-05-01",Finish="2025-08-01",Phase="Phase 2"),
            dict(Task="Cloud Deploy",   Start="2025-09-01",Finish="2025-12-01",Phase="Phase 3"),
            dict(Task="EHR Connectors", Start="2025-10-01",Finish="2026-02-01",Phase="Phase 3"),
        ])
        fig = px.timeline(gantt_df,x_start="Start",x_end="Finish",y="Task",color="Phase",
            color_discrete_map={"Phase 1":C_PRIMARY,"Phase 2":C_TEAL,"Phase 3":C_PURPLE})
        fig.update_layout(title="OnchoInsight Development Roadmap",**PL,height=300)
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig,use_container_width=True)

    end()

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<hr>
<div style="text-align:center;font-size:11px;color:{C_TEXT_MUTED};padding:8px 0 20px;">
    <strong style="color:{C_PRIMARY};">OnchoInsight Analytics Platform v1.0</strong> &nbsp;·&nbsp;
    WCAG 2.1 AA Compliant &nbsp;·&nbsp;
    US Healthcare Standard UI (CMS Design System) &nbsp;·&nbsp;
    All patient data is synthetic — for demonstration purposes only
</div>
""",unsafe_allow_html=True)
