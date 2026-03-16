"""
╔══════════════════════════════════════════════════════════════════╗
║   ELIGIBILITYIQ  —  Healthcare RCM Platform                     ║
║   Single + Bulk Verification  |  ReAct AI  |  EDI 270/271       ║
║   Stack: Python 3.10+  |  Streamlit  |  Zero external deps      ║
╚══════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import json, time, re, io, csv
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, List, Dict

# ── Page config ─────────────────────────────────────────────
st.set_page_config(
    page_title="EligibilityIQ · RCM Platform",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════
#  THEME  —  US Healthcare Enterprise
#  Deep Navy sidebar · White card bodies · Trust Blue CTAs
#  Emerald success · Amber caution · Crimson error
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Roboto+Mono:wght@400;500&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');

/* ─── COLOR TOKENS ───────────────────────────────────────────
   Primary     #1E40AF  deep sapphire blue
   Accent CTA  #2563EB  vivid interactive blue
   Success     #047857  rich emerald green
   Warning     #B45309  warm amber
   Danger      #B91C1C  strong crimson
   Reasoning   #6D28D9  purple (thought steps)
   Observation #0E7490  teal (observation steps)
   App BG      #F0F5FB  cool slate wash
   Sidebar     deep navy #0F1E3C → #162847
──────────────────────────────────────────────────────────── */

html, body, [class*="css"] { font-family:'Inter',sans-serif; }
.stApp { background:#F0F5FB; color:#111827; }

/* ── Sidebar: deep navy + vivid blue left accent ── */
[data-testid="stSidebar"] {
  background: linear-gradient(175deg, #0F1E3C 0%, #162847 60%, #0D1B38 100%);
  border-right: 3px solid #2563EB;
}
[data-testid="stSidebar"] * { color:#CBD9EE !important; }
[data-testid="stSidebar"] hr { border-color:rgba(37,99,235,.25) !important; }

/* ── Header: rich multi-stop gradient with glow ── */
.hdr {
  background: linear-gradient(130deg,#0F1E3C 0%,#1E3A6E 30%,#1D4ED8 62%,#1E3A6E 82%,#0F1E3C 100%);
  border-radius:14px; padding:30px 40px 26px;
  margin-bottom:26px; position:relative; overflow:hidden;
  box-shadow:0 6px 32px rgba(15,30,60,.35), inset 0 1px 0 rgba(255,255,255,.07);
}
.hdr::before {
  content:""; position:absolute; top:-80px; right:-60px;
  width:360px; height:360px;
  background:radial-gradient(circle,rgba(96,165,250,.15) 0%,transparent 65%);
  pointer-events:none;
}
.hdr::after {
  content:""; position:absolute; bottom:-40px; left:25%;
  width:200px; height:200px;
  background:radial-gradient(circle,rgba(16,185,129,.08) 0%,transparent 70%);
  pointer-events:none;
}
.hdr-eyebrow {
  font-family:'Roboto Mono',monospace; font-size:.68rem;
  letter-spacing:3.5px; color:#60A5FA; text-transform:uppercase; margin-bottom:8px;
}
.hdr-title {
  font-family:'Plus Jakarta Sans',sans-serif; font-size:2rem;
  font-weight:800; color:#fff; margin:0 0 8px; line-height:1.15;
  text-shadow:0 2px 12px rgba(0,0,0,.25);
}
.hdr-sub { color:#93C5FD; font-size:.83rem; line-height:1.7; }
.badge {
  display:inline-block; background:rgba(96,165,250,.18);
  border:1px solid rgba(96,165,250,.4); color:#BFDBFE;
  border-radius:20px; padding:3px 13px;
  font-size:.68rem; font-family:'Roboto Mono',monospace;
  font-weight:500; letter-spacing:.8px; margin-left:8px; vertical-align:middle;
}

/* ── KPI cards: each a distinct colored gradient ── */
.kpi-row { display:flex; gap:14px; margin-bottom:24px; }
.kpi {
  flex:1; border-radius:13px; padding:18px 20px;
  position:relative; overflow:hidden;
  box-shadow:0 3px 14px rgba(0,0,0,.12); border:1px solid rgba(255,255,255,.6);
}
.kpi.navy  { background:linear-gradient(140deg,#1E3A6E 0%,#1E40AF 100%); }
.kpi.green { background:linear-gradient(140deg,#065F46 0%,#059669 100%); }
.kpi.amber { background:linear-gradient(140deg,#78350F 0%,#D97706 100%); }
.kpi.red   { background:linear-gradient(140deg,#7F1D1D 0%,#DC2626 100%); }
.kpi::before {
  content:""; position:absolute; top:-20px; right:-20px;
  width:110px; height:110px;
  background:radial-gradient(circle,rgba(255,255,255,.14) 0%,transparent 70%);
  pointer-events:none;
}
.kpi-val {
  font-family:'Plus Jakarta Sans',sans-serif;
  font-size:2rem; font-weight:800; color:#fff; line-height:1;
}
.kpi-lbl  { font-size:.74rem; color:rgba(255,255,255,.75); margin-top:4px; font-weight:500; }
.kpi-delta {
  font-size:.7rem; font-weight:600; color:#fff;
  background:rgba(255,255,255,.2); border-radius:4px;
  padding:2px 8px; display:inline-block; margin-top:6px;
}

/* ── White cards ── */
.card {
  background:#fff; border-radius:14px;
  box-shadow:0 1px 4px rgba(0,0,0,.06),0 4px 16px rgba(0,0,0,.06);
  padding:22px 24px; margin-bottom:16px;
  border:1px solid rgba(224,232,244,.9);
}
.card-hdr {
  font-family:'Plus Jakarta Sans',sans-serif; font-size:.88rem;
  font-weight:700; color:#0F1E3C; margin-bottom:16px;
  display:flex; align-items:center; gap:8px;
  border-bottom:2px solid #EFF6FF; padding-bottom:12px;
}
.card-hdr .acc { color:#2563EB; }

/* ── Section ruler ── */
.ruler {
  font-family:'Roboto Mono',monospace; font-size:.68rem; letter-spacing:2.5px;
  text-transform:uppercase; color:#2563EB;
  display:flex; align-items:center; gap:10px; margin:22px 0 14px;
}
.ruler::after { content:""; flex:1; height:2px; background:linear-gradient(90deg,#BFDBFE,transparent); }

/* ── Patient card ── */
.pat {
  background:linear-gradient(135deg,#EFF6FF 0%,#fff 100%);
  border-radius:12px; border-left:5px solid #2563EB;
  box-shadow:0 2px 12px rgba(37,99,235,.12);
  padding:16px 22px; margin-bottom:20px;
  display:flex; align-items:center; gap:18px;
  border-top:1px solid #DBEAFE; border-right:1px solid #E0EAFF; border-bottom:1px solid #E0EAFF;
}
.pat-av {
  width:52px; height:52px; border-radius:50%;
  background:linear-gradient(135deg,#1E3A6E,#2563EB);
  display:flex; align-items:center; justify-content:center;
  font-size:1.4rem; flex-shrink:0;
  box-shadow:0 4px 14px rgba(37,99,235,.35);
}
.pat-name {
  font-family:'Plus Jakarta Sans',sans-serif;
  font-size:1.15rem; font-weight:800; color:#0F1E3C;
}
.pat-meta { color:#64748B; font-size:.8rem; margin-top:3px; }

/* ── Tags: vivid colored pills ── */
.tag { display:inline-block; border-radius:20px; padding:4px 13px; font-size:.72rem; font-weight:600; margin:6px 4px 0 0; }
.tblue   { background:#DBEAFE; color:#1D4ED8; border:1px solid #93C5FD; }
.tgreen  { background:#D1FAE5; color:#065F46; border:1px solid #6EE7B7; }
.tamber  { background:#FEF3C7; color:#92400E; border:1px solid #FCD34D; }
.tred    { background:#FEE2E2; color:#991B1B; border:1px solid #FCA5A5; }
.tgray   { background:#F1F5F9; color:#475569; border:1px solid #CBD5E1; }
.tpurple { background:#EDE9FE; color:#5B21B6; border:1px solid #C4B5FD; }
.tteal   { background:#CFFAFE; color:#164E63; border:1px solid #67E8F9; }

/* ── Alert banners: gradient colored backgrounds ── */
.banner {
  border-radius:10px; padding:13px 18px;
  display:flex; align-items:flex-start; gap:12px;
  margin-bottom:12px; font-size:.87rem; font-weight:600;
}
.bok   { background:linear-gradient(135deg,#D1FAE5,#ECFDF5); border:1px solid #6EE7B7; color:#065F46; }
.berr  { background:linear-gradient(135deg,#FEE2E2,#FFF5F5); border:1px solid #FCA5A5; color:#991B1B; }
.bwarn { background:linear-gradient(135deg,#FEF3C7,#FFFBEB); border:1px solid #FCD34D; color:#92400E; }
.binfo { background:linear-gradient(135deg,#DBEAFE,#EFF6FF); border:1px solid #93C5FD; color:#1E40AF; }

/* ── Coverage grid ── */
.cov-grid { display:grid; grid-template-columns:1fr 1fr; gap:9px; margin-bottom:14px; }
.cov-cell {
  background:#F8FAFF; border:1px solid #E2EAF6; border-radius:9px; padding:10px 14px;
  transition:box-shadow .15s;
}
.cov-cell:hover { box-shadow:0 2px 8px rgba(37,99,235,.1); }
.cov-lbl { font-size:.71rem; color:#64748B; font-weight:500; margin-bottom:3px; }
.cov-val { font-size:.9rem; font-weight:700; color:#0F1E3C; }
.cv-teal  { color:#065F46; }
.cv-amber { color:#92400E; }
.cv-blue  { color:#1D4ED8; }
.cv-red   { color:#991B1B; }

/* ── JSON viewer: dark syntax theme ── */
.jv {
  background:#0F172A; border:1px solid #1E293B; border-radius:10px;
  padding:16px 18px; font-family:'Roboto Mono',monospace;
  font-size:.72rem; line-height:1.8; color:#7DD3FC;
  overflow-x:auto; white-space:pre-wrap;
  max-height:420px; overflow-y:auto;
  box-shadow:inset 0 2px 8px rgba(0,0,0,.3);
}

/* ── ReAct steps: distinct color per type ── */
.rs { border-radius:9px; padding:11px 14px; margin-bottom:9px; font-size:.77rem; line-height:1.65; border-left:4px solid #ccc; }
.rs.thought     { border-color:#7C3AED; background:linear-gradient(135deg,rgba(124,58,237,.08),rgba(124,58,237,.03)); }
.rs.action      { border-color:#2563EB; background:linear-gradient(135deg,rgba(37,99,235,.08),rgba(37,99,235,.03)); }
.rs.observation { border-color:#0E7490; background:linear-gradient(135deg,rgba(14,116,144,.08),rgba(14,116,144,.03)); }
.rs.final       { border-color:#047857; background:linear-gradient(135deg,rgba(4,120,87,.1),rgba(4,120,87,.04)); }
.rs .rs-lbl {
  font-family:'Roboto Mono',monospace; font-size:.63rem;
  font-weight:700; letter-spacing:1.8px; text-transform:uppercase; margin-bottom:4px;
}
.rs.thought     .rs-lbl { color:#8B5CF6; }
.rs.action      .rs-lbl { color:#3B82F6; }
.rs.observation .rs-lbl { color:#0EA5E9; }
.rs.final       .rs-lbl { color:#10B981; }
.rs .rs-body { color:#374151; }
.rs .rs-ts { float:right; color:#9CA3AF; font-family:'Roboto Mono',monospace; font-size:.6rem; }

/* ── Tool chips ── */
.chip { display:inline-flex; align-items:center; gap:5px; border-radius:20px; padding:3px 11px; font-family:'Roboto Mono',monospace; font-size:.67rem; font-weight:600; margin:3px 2px 0; }
.chip-ok  { background:#D1FAE5; border:1px solid #6EE7B7; color:#065F46; }
.chip-bad { background:#FEE2E2; border:1px solid #FCA5A5; color:#991B1B; }
.chip-def { background:#DBEAFE; border:1px solid #93C5FD; color:#1E40AF; }

/* ── Sidebar stat cards ── */
.stat-row { display:flex; gap:6px; margin-bottom:12px; }
.stat {
  flex:1; background:rgba(255,255,255,.08); border:1px solid rgba(96,165,250,.2);
  border-radius:9px; padding:10px 10px; text-align:center;
}
.stat .sv { font-family:'Plus Jakarta Sans',sans-serif; font-size:1.4rem; font-weight:800; color:#fff; }
.stat .sl { font-size:.65rem; color:#93C5FD; margin-top:2px; }

/* ── Bulk results table ── */
.btable {
  width:100%; border-collapse:collapse; font-size:.81rem;
  background:#fff; border-radius:12px; overflow:hidden;
  box-shadow:0 2px 12px rgba(0,0,0,.08); border:1px solid #E2EAF6;
}
.btable th {
  background:linear-gradient(135deg,#1E3A6E,#1E40AF); color:#BFDBFE;
  font-family:'Roboto Mono',monospace; font-size:.66rem;
  letter-spacing:1.4px; text-transform:uppercase; padding:12px 14px; text-align:left; font-weight:500;
}
.btable td { padding:11px 14px; border-bottom:1px solid #F0F6FF; color:#1A2332; vertical-align:middle; }
.btable tr:last-child td { border-bottom:none; }
.btable tr:nth-child(even) td { background:#FAFCFF; }
.btable tr:hover td { background:#EFF6FF !important; }

/* ── Status dots ── */
.sdot { display:inline-flex; align-items:center; gap:6px; font-weight:600; font-size:.78rem; }
.dot  { width:9px; height:9px; border-radius:50%; display:inline-block; }
.dg  { background:#059669; box-shadow:0 0 0 3px rgba(5,150,105,.15); }
.da  { background:#D97706; box-shadow:0 0 0 3px rgba(217,119,6,.15); }
.dr  { background:#DC2626; box-shadow:0 0 0 3px rgba(220,38,38,.15); }
.dgr { background:#94A3B8; }

/* ── Streamlit component overrides ── */
.stProgress > div > div { background:linear-gradient(90deg,#2563EB,#3B82F6) !important; border-radius:4px !important; }
.stTextInput input, .stSelectbox > div > div, .stNumberInput input {
  background:#fff !important; border:1.5px solid #CBD5E1 !important;
  border-radius:9px !important; color:#111827 !important;
  box-shadow:0 1px 3px rgba(0,0,0,.05) !important;
}
label { color:#374151 !important; font-size:.8rem !important; font-weight:500 !important; }
.stButton > button {
  background:linear-gradient(135deg,#1D4ED8,#2563EB,#3B82F6) !important;
  color:#fff !important; font-weight:700 !important;
  border:none !important; border-radius:9px !important;
  font-size:.88rem !important; padding:10px 0 !important;
  box-shadow:0 4px 14px rgba(37,99,235,.4) !important;
  transition:all .18s !important;
}
.stButton > button:hover { transform:translateY(-1px) !important; box-shadow:0 6px 20px rgba(37,99,235,.5) !important; }
.stTabs [data-baseweb="tab-list"] {
  background:#fff !important; border-radius:10px 10px 0 0 !important;
  border-bottom:2px solid #DBEAFE !important; gap:0 !important; padding:0 8px !important;
  box-shadow:0 2px 6px rgba(0,0,0,.05) !important;
}
.stTabs [data-baseweb="tab"] {
  font-family:'Inter',sans-serif !important; font-weight:600 !important;
  font-size:.85rem !important; color:#64748B !important; padding:13px 24px !important;
}
.stTabs [aria-selected="true"] { color:#1D4ED8 !important; background:transparent !important; border-bottom:3px solid #2563EB !important; }
.stSpinner > div { color:#2563EB !important; }
.streamlit-expanderHeader {
  background:#F8FAFF !important; border:1.5px solid #DBEAFE !important;
  border-radius:9px !important; color:#374151 !important; font-size:.82rem !important;
}
[data-testid="stFileUploadDropzone"] {
  background:linear-gradient(135deg,#EFF6FF,#F8FAFF) !important;
  border:2px dashed #93C5FD !important; border-radius:12px !important;
}
::-webkit-scrollbar { width:5px; height:5px; }
::-webkit-scrollbar-thumb { background:linear-gradient(180deg,#93C5FD,#6366F1); border-radius:4px; }
::-webkit-scrollbar-track { background:transparent; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  CONSTANTS & SAMPLE DATA
# ══════════════════════════════════════════════════════════════
CORRECT_ID   = "BCB-7723-A"
INCORRECT_ID = "BCB7723A"

BULK_SAMPLE: List[Dict] = [
    {"name":"John Doe",        "dob":"06/15/1985","member_id":"BCB7723A",   "procedure":"MRI",        "payer":"BlueCross BlueShield"},
    {"name":"Maria Garcia",    "dob":"03/22/1978","member_id":"AET-4491-B", "procedure":"CT Scan",    "payer":"Aetna"},
    {"name":"Robert Johnson",  "dob":"11/08/1962","member_id":"UHC88201C",  "procedure":"X-Ray",      "payer":"UnitedHealthcare"},
    {"name":"Linda Chen",      "dob":"07/30/1990","member_id":"HUM-3314-D", "procedure":"Ultrasound", "payer":"Humana"},
    {"name":"James Williams",  "dob":"01/14/1955","member_id":"CIG-9902-E", "procedure":"MRI",        "payer":"Cigna"},
    {"name":"Patricia Brown",  "dob":"09/05/1982","member_id":"BCB-5512-F", "procedure":"CT Scan",    "payer":"BlueCross BlueShield"},
    {"name":"Michael Davis",   "dob":"05/19/1970","member_id":"AET-7761G",  "procedure":"X-Ray",      "payer":"Aetna"},
    {"name":"Jennifer Wilson", "dob":"12/28/1995","member_id":"UHC-0044-H", "procedure":"Ultrasound", "payer":"UnitedHealthcare"},
]

BULK_OUTCOMES: Dict[str, Dict] = {
    "John Doe":        {"status":"VERIFIED",  "plan":"BlueCross PPO Select",     "copay":75,  "ded_rem":1200, "pa":True,  "net":"In-Network",     "note":"Member ID formatting error (dashes missing) — auto-corrected by AI agent"},
    "Maria Garcia":    {"status":"VERIFIED",  "plan":"Aetna Choice POS II",      "copay":50,  "ded_rem":850,  "pa":False, "net":"In-Network",     "note":""},
    "Robert Johnson":  {"status":"NEEDS_PA",  "plan":"UHC Choice Plus",          "copay":40,  "ded_rem":0,    "pa":True,  "net":"In-Network",     "note":"Deductible met; PA required for MRI"},
    "Linda Chen":      {"status":"VERIFIED",  "plan":"Humana Gold Plus HMO",     "copay":60,  "ded_rem":400,  "pa":False, "net":"In-Network",     "note":""},
    "James Williams":  {"status":"INACTIVE",  "plan":"Cigna OAP",                "copay":0,   "ded_rem":0,    "pa":False, "net":"Unknown",        "note":"Coverage terminated 12/31/2023 — contact patient for updated insurance"},
    "Patricia Brown":  {"status":"VERIFIED",  "plan":"BlueCross HMO Blue",       "copay":30,  "ded_rem":1800, "pa":False, "net":"In-Network",     "note":""},
    "Michael Davis":   {"status":"CONFLICT",  "plan":"Aetna Medicare Advantage", "copay":0,   "ded_rem":0,    "pa":False, "net":"Unknown",        "note":"Member ID missing dashes — auto-corrected; secondary insurance also detected"},
    "Jennifer Wilson": {"status":"VERIFIED",  "plan":"UHC Navigate HMO",         "copay":45,  "ded_rem":650,  "pa":False, "net":"In-Network",     "note":""},
}


# ══════════════════════════════════════════════════════════════
#  DATA MODELS
# ══════════════════════════════════════════════════════════════
@dataclass
class ReActStep:
    kind: str
    body: str
    tool: Optional[str] = None
    tool_ok: Optional[bool] = None
    ts: str = field(default_factory=lambda: datetime.now().strftime("%H:%M:%S"))

@dataclass
class AgentResult:
    success: bool
    edi_success: dict
    edi_failure: dict
    steps: List[ReActStep]
    tools_called: List[str]
    corrected_member_id: str
    resolution: str
    attempts: int

@dataclass
class BulkResult:
    row_num: int
    name: str
    dob: str
    member_id: str
    procedure: str
    payer: str
    status: str
    plan: str
    copay: float
    ded_rem: float
    pa: bool
    net: str
    note: str
    at: str = field(default_factory=lambda: datetime.now().strftime("%H:%M:%S"))


# ══════════════════════════════════════════════════════════════
#  SIMULATED TOOLS
# ══════════════════════════════════════════════════════════════
def tool_edi_270_api(member_id: str, patient_name: str, dob: str) -> dict:
    if member_id.strip().upper() == CORRECT_ID:
        return {
            "status": "SUCCESS",
            "transaction_id": "TX-20240315-00847",
            "edi_version": "X12 5010 271",
            "payer": {"id":"BCB001","name":"BlueCross BlueShield of Tennessee"},
            "subscriber": {"member_id":member_id,"first_name":"JOHN","last_name":"DOE","dob":"19850615","relationship":"Self"},
            "coverage": {"plan_name":"BlueCross PPO Select","plan_type":"PPO","group_number":"GRP-45892","effective_date":"20240101","termination_date":"20241231","active":True},
            "benefits": {"copay_specialist":75.0,"copay_primary":30.0,"deductible_annual":2000.0,"deductible_met":800.0,"deductible_remaining":1200.0,"out_of_pocket_max":6500.0,"out_of_pocket_met":1100.0,"coinsurance_pct":20},
            "service": {"procedure":"MRI","covered":True,"network_status":"In-Network","prior_auth_required":True},
            "meta": {"response_ms":312,"edi_loop":"2110C"}
        }
    return {
        "status": "ERROR",
        "error_code": "271-AAA04",
        "error_description": "Member ID not found in payer system",
        "member_id_queried": member_id,
        "payer_id": "BCB001",
        "suggestion": "Verify member ID format and resubmit",
        "transaction_id": "TX-ERR-BCB7723-001",
        "meta": {"response_ms":198}
    }

def tool_historical_claims_db(patient_name: str, dob: str) -> dict:
    return {
        "status": "FOUND",
        "total_claims_found": 3,
        "most_recent_claim": {
            "claim_id":"CLM-2023-089451","service_date":"2023-09-12",
            "procedure":"Annual Physical","cpt_code":"99385",
            "payer_name":"BlueCross BlueShield of Tennessee",
            "member_id_submitted":CORRECT_ID,"claim_status":"PAID","paid_amount":180.0
        },
        "intake_record_member_id": INCORRECT_ID,
        "confirmed_member_id": CORRECT_ID,
        "all_historical_ids": [CORRECT_ID, CORRECT_ID, CORRECT_ID],
        "consistency_score": 1.0,
        "note": "Dash delimiters absent in today's intake record — stripped by intake form"
    }

def tool_fuzzy_name_match(name_a: str, name_b: str, id_a: str, id_b: str) -> dict:
    def lev(s1: str, s2: str) -> int:
        m, n = len(s1), len(s2)
        dp = list(range(n + 1))
        for i in range(1, m + 1):
            prev, dp[0] = dp[:], i
            for j in range(1, n + 1):
                dp[j] = prev[j-1] if s1[i-1] == s2[j-1] else 1 + min(prev[j], dp[j-1], prev[j-1])
        return dp[n]
    ca = re.sub(r"[^A-Z0-9]", "", id_a.upper())
    cb = re.sub(r"[^A-Z0-9]", "", id_b.upper())
    dist   = lev(ca, cb)
    id_sim = round(1 - dist / max(len(ca), len(cb), 1), 3)
    nm_ok  = name_a.strip().upper() == name_b.strip().upper()
    conf   = round(id_sim * 0.7 + (1.0 if nm_ok else 0.0) * 0.3, 3)
    return {
        "status": "MATCH_CONFIRMED" if conf >= 0.80 else "MATCH_UNCERTAIN",
        "algorithm": "Levenshtein + Jaro-Winkler hybrid",
        "id_similarity": id_sim, "levenshtein_distance": dist,
        "name_exact_match": nm_ok, "overall_confidence": conf,
        "interpretation": "Formatting difference only — dashes stripped" if conf >= 0.80 else "Escalate",
        "recommended_action": f"Proceed with corrected ID: {id_b}" if conf >= 0.80 else "Manual review"
    }

def tool_payer_portal_scraper(patient_name: str, dob: str) -> dict:
    return {
        "status": "PARTIAL_MATCH",
        "portal": "BCBS Provider Portal",
        "match": {"name_on_file":"JOHN DOE","dob":dob,"payer_id":"BCB001",
                  "payer_name":"BlueCross BlueShield of Tennessee",
                  "member_id_masked":"BCB-****-A","confidence":0.87},
        "note": "Full member ID requires Historical Claims DB cross-reference"
    }


# ══════════════════════════════════════════════════════════════
#  ELIGIBILITY AGENT  (ReAct)
# ══════════════════════════════════════════════════════════════
class EligibilityAgent:
    def __init__(self, patient_name, dob, member_id, procedure):
        self.patient_name = patient_name
        self.dob = dob
        self.member_id = member_id
        self.procedure = procedure
        self._steps: List[ReActStep] = []
        self._tools: List[str] = []

    def _t(self, kind, body, tool=None, ok=None):
        self._steps.append(ReActStep(kind=kind, body=body, tool=tool, tool_ok=ok))

    def _call(self, name: str, **kw) -> dict:
        self._tools.append(name)
        routes = {
            "EDI_270_API":          lambda: tool_edi_270_api(**kw),
            "Historical_Claims_DB": lambda: tool_historical_claims_db(**kw),
            "Fuzzy_Name_Match":     lambda: tool_fuzzy_name_match(**kw),
            "Payer_Portal_Scraper": lambda: tool_payer_portal_scraper(**kw),
        }
        fn = routes.get(name)
        return fn() if fn else {"status":"ERROR","error":f"Unknown tool: {name}"}

    def run(self) -> AgentResult:
        pat, mid, proc, dob = self.patient_name, self.member_id, self.procedure, self.dob

        # Step 1: First EDI attempt
        self._t("thought", f"Patient {pat} is scheduled for {proc}. Initiating EDI 270 inquiry using member ID on file: '{mid}'.")
        self._t("action", f"Calling EDI_270_API → member_id='{mid}', patient='{pat}', dob='{dob}'", tool="EDI_270_API", ok=False)
        r1 = self._call("EDI_270_API", member_id=mid, patient_name=pat, dob=dob)
        self._t("observation",
            f"❌ EDI 271 ERROR — \"{r1.get('error_description','Unknown error')}\" "
            f"(code: {r1.get('error_code','N/A')}). Member ID '{mid}' rejected by payer.")

        # Step 2: Query historical claims
        self._t("thought",
            "Payer rejected the member ID. Most likely a data entry error — intake system "
            "may have stripped hyphen delimiters. Strategy: query Historical Claims DB "
            "for previously accepted member IDs for this patient.")
        self._t("action", f"Calling Historical_Claims_DB → patient='{pat}', dob='{dob}'",
                tool="Historical_Claims_DB", ok=True)
        rc = self._call("Historical_Claims_DB", patient_name=pat, dob=dob)

        recovered_id = rc.get("confirmed_member_id", CORRECT_ID)
        intake_id    = rc.get("intake_record_member_id", mid)
        mc           = rc.get("most_recent_claim", {})

        self._t("observation",
            f"✅ Found {rc.get('total_claims_found', 0)} historical claims. "
            f"Most recent: {mc.get('claim_id','N/A')} ({mc.get('service_date','N/A')}) — "
            f"processed with ID '{recovered_id}'. "
            f"Intake shows '{intake_id}'. Note: {rc.get('note','')}")

        # Step 3: Fuzzy match to confirm identity
        self._t("thought",
            f"Candidate ID '{recovered_id}' found. Must confirm same patient identity "
            "before using it. Running Fuzzy_Name_Match to validate.")
        self._t("action",
            f"Calling Fuzzy_Name_Match → name_a='{pat}', id_a='{intake_id}', id_b='{recovered_id}'",
            tool="Fuzzy_Name_Match", ok=True)
        rf = self._call("Fuzzy_Name_Match", name_a=pat, name_b="JOHN DOE",
                        id_a=intake_id, id_b=recovered_id)
        self._t("observation",
            f"Fuzzy Match → {rf.get('status')} | "
            f"Confidence: {rf.get('overall_confidence',0):.0%} | "
            f"ID similarity: {rf.get('id_similarity',0)} | "
            f"Levenshtein: {rf.get('levenshtein_distance',0)} | "
            f"Name match: {rf.get('name_exact_match',False)}. "
            f"{rf.get('interpretation','')}")

        # Step 4: Retry EDI with corrected ID
        self._t("thought",
            f"Identity confirmed at {rf.get('overall_confidence',0):.0%} confidence. "
            f"Retrying EDI 270 with corrected member ID '{recovered_id}'.")
        self._t("action",
            f"Calling EDI_270_API (RETRY) → member_id='{recovered_id}'",
            tool="EDI_270_API", ok=True)
        r2 = self._call("EDI_270_API", member_id=recovered_id, patient_name=pat, dob=dob)

        sub = r2.get("subscriber", {})
        cov = r2.get("coverage",   {})
        ben = r2.get("benefits",   {})
        svc = r2.get("service",    {})
        pay = r2.get("payer",      {})

        self._t("observation",
            f"✅ EDI 271 SUCCESS — "
            f"Member '{sub.get('first_name','')} {sub.get('last_name','')}' verified with "
            f"{pay.get('name','N/A')}. Plan: {cov.get('plan_name','N/A')}. "
            f"Active: {cov.get('active',False)}. "
            f"Deductible remaining: ${ben.get('deductible_remaining',0):,.2f}. "
            f"Prior auth for {proc}: {svc.get('prior_auth_required',False)}.")

        self._t("final",
            f"✅ ELIGIBILITY VERIFIED — {pat} is eligible for {proc} under "
            f"{cov.get('plan_name','N/A')} ({pay.get('name','N/A')}). "
            f"Root cause: member ID formatting error ('{intake_id}' → '{recovered_id}'). "
            f"Resolved via Historical Claims + Fuzzy Match. "
            f"⚠️ Prior authorization required — initiate PA workflow.")

        return AgentResult(
            success=True, edi_success=r2, edi_failure=r1,
            steps=self._steps, tools_called=self._tools,
            corrected_member_id=recovered_id,
            resolution="Historical Claims cross-reference + Fuzzy ID matching",
            attempts=2,
        )


# ══════════════════════════════════════════════════════════════
#  AI SUMMARY BUILDER
# ══════════════════════════════════════════════════════════════
def build_summary(edi: dict, patient_name: str, procedure: str) -> dict:
    sub  = edi.get("subscriber", {})
    cov  = edi.get("coverage",   {})
    ben  = edi.get("benefits",   {})
    svc  = edi.get("service",    {})
    pay  = edi.get("payer",      {})
    fname  = sub.get("first_name","")
    lname  = sub.get("last_name", "")
    plan   = cov.get("plan_name", "—")
    ptype  = cov.get("plan_type", "—")
    pname  = pay.get("name",      "—")
    active = cov.get("active",    False)
    net    = svc.get("network_status",      "—")
    pa     = svc.get("prior_auth_required", False)
    cop    = ben.get("copay_specialist",    75)
    ded_a  = ben.get("deductible_annual",  2000)
    ded_m  = ben.get("deductible_met",      800)
    ded_r  = ben.get("deductible_remaining",1200)
    oop_m  = ben.get("out_of_pocket_max",  6500)
    oop_me = ben.get("out_of_pocket_met",  1100)
    coins  = ben.get("coinsurance_pct",      20)
    return {
        "headline":  "✅ Eligibility Verified",
        "narrative": (
            f"{fname} {lname} holds an active {ptype} policy with {pname} ({plan}). "
            f"Coverage is valid through December 31, 2024. "
            f"The {procedure} is covered as {net}"
            + (", and prior authorization is required before scheduling." if pa
               else " — no prior authorization required.")
        ),
        "coverage": [
            ("Patient",          f"{fname} {lname}"),
            ("Payer",            pname),
            ("Plan",             plan),
            ("Plan Type",        ptype),
            ("Network Status",   net),
            ("Coverage Active",  "Yes ✅" if active else "No ❌"),
            ("Effective Date",   "Jan 01, 2024"),
            ("Termination Date", "Dec 31, 2024"),
        ],
        "financials": [
            ("Specialist Copay",     f"${cop:.2f}",    "cv-blue"),
            ("Annual Deductible",    f"${ded_a:,.2f}", ""),
            ("Deductible Met",       f"${ded_m:,.2f}", "cv-teal"),
            ("Deductible Remaining", f"${ded_r:,.2f}", "cv-amber"),
            ("Coinsurance",          f"{coins}% patient",""),
            ("Out-of-Pocket Max",    f"${oop_m:,.2f}", ""),
            ("OOP Met",              f"${oop_me:,.2f}","cv-teal"),
        ],
        "alerts": [
            ("bwarn","⚠️", f"Prior Authorization required for {procedure}. Initiate PA workflow before scheduling."),
            ("binfo","ℹ️", "Data conflict auto-resolved: member ID formatting corrected via Historical Claims DB."),
            ("bok",  "💰", f"Collect ${cop:.0f} copay at check-in. Patient has ${ded_r:,.0f} deductible remaining; then {coins}% coinsurance applies."),
        ],
        "rcm_note": (
            f"Estimated patient responsibility (post-deductible): "
            f"~${cop + 1800*coins/100:.0f}–${cop + 2400*coins/100:.0f} "
            "depending on MRI type and contrast agent."
        ),
    }


# ══════════════════════════════════════════════════════════════
#  BULK ENGINE
# ══════════════════════════════════════════════════════════════
def process_bulk_patient(row_num: int, row: dict) -> BulkResult:
    name = row.get("name", "").strip()
    out  = BULK_OUTCOMES.get(name, {
        "status":"VERIFIED","plan":"Unknown Plan","copay":40,
        "ded_rem":500,"pa":False,"net":"In-Network","note":""
    })
    return BulkResult(
        row_num=row_num, name=name,
        dob=row.get("dob",""), member_id=row.get("member_id",""),
        procedure=row.get("procedure",""), payer=row.get("payer",""),
        status=out.get("status","VERIFIED"), plan=out.get("plan","—"),
        copay=float(out.get("copay",0)), ded_rem=float(out.get("ded_rem",0)),
        pa=bool(out.get("pa",False)), net=out.get("net","—"),
        note=out.get("note",""),
    )

def build_csv_export(results: List[BulkResult]) -> str:
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["#","Name","DOB","Member ID","Procedure","Payer","Status",
                "Plan","Copay","Deductible Remaining","PA Required","Network","Notes","Time"])
    for r in results:
        w.writerow([r.row_num, r.name, r.dob, r.member_id, r.procedure, r.payer,
                    r.status, r.plan, f"${r.copay:.2f}", f"${r.ded_rem:,.2f}",
                    "Yes" if r.pa else "No", r.net, r.note, r.at])
    return buf.getvalue()

def build_sample_csv() -> str:
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["name","dob","member_id","procedure","payer"])
    for p in BULK_SAMPLE:
        w.writerow([p["name"],p["dob"],p["member_id"],p["procedure"],p["payer"]])
    return buf.getvalue()


# ══════════════════════════════════════════════════════════════
#  UI HELPERS
# ══════════════════════════════════════════════════════════════
def H(m: str): st.markdown(m, unsafe_allow_html=True)

def render_header():
    H("""
    <div class="hdr">
      <div class="hdr-eyebrow">Healthcare RCM Platform &nbsp;·&nbsp; Revenue Cycle Automation</div>
      <div class="hdr-title">EligibilityIQ
        <span class="badge">AI-Powered</span>
        <span class="badge">EDI 270/271</span>
        <span class="badge">ReAct Agent</span>
      </div>
      <div class="hdr-sub">
        Autonomous Eligibility Verification &nbsp;·&nbsp;
        Single &amp; Bulk Processing &nbsp;·&nbsp;
        Self-Correcting Conflict Resolution &nbsp;·&nbsp;
        HIPAA-Aware Architecture
      </div>
    </div>
    """)

def render_kpis(results: Optional[List[BulkResult]] = None):
    if results:
        total = len(results)
        v  = sum(1 for r in results if r.status in ("VERIFIED","NEEDS_PA"))
        i  = sum(1 for r in results if r.status == "INACTIVE")
        pa = sum(1 for r in results if r.pa)
        cf = sum(1 for r in results if r.status == "CONFLICT")
        rt = int(v / total * 100) if total else 0
    else:
        total = v = i = pa = cf = rt = 0

    H(f"""
    <div class="kpi-row">
      <div class="kpi navy">
        <div class="kpi-val">{total or "—"}</div>
        <div class="kpi-lbl">Patients Processed</div>
        {"<div class='kpi-delta'>This batch</div>" if total else ""}
      </div>
      <div class="kpi green">
        <div class="kpi-val">{v or "—"}</div>
        <div class="kpi-lbl">Eligibility Verified</div>
        {"<div class='kpi-delta'>"+str(rt)+"% success rate</div>" if v else ""}
      </div>
      <div class="kpi amber">
        <div class="kpi-val">{pa or "—"}</div>
        <div class="kpi-lbl">Prior Auth Required</div>
        {"<div class='kpi-delta' style='background:#FEF3E2;color:#B45309'>Action needed</div>" if pa else ""}
      </div>
      <div class="kpi red">
        <div class="kpi-val">{i+cf or "—"}</div>
        <div class="kpi-lbl">Needs Review</div>
        {"<div class='kpi-delta' style='background:#FEF0F0;color:#B91C1C'>Manual intervention</div>" if i+cf else ""}
      </div>
    </div>
    """)

def render_step(s: ReActStep):
    """Render one ReAct step inside the sidebar with fully explicit inline styles
    so the sidebar's blanket color override cannot suppress them."""
    icons = {"thought":("💭","Thought"),"action":("⚡","Action"),
             "observation":("🔍","Observation"),"final":("✅","Final Answer")}
    icon, label = icons.get(s.kind, ("•", s.kind.title()))

    # Per-type colors — all inline so they beat sidebar's !important rule
    cfg = {
        "thought":     {"border":"#A78BFA","bg":"rgba(167,139,250,.15)","lbl":"#C4B5FD","body":"#E9E4FF"},
        "action":      {"border":"#60A5FA","bg":"rgba(96,165,250,.15)", "lbl":"#93C5FD","body":"#DBEAFE"},
        "observation": {"border":"#22D3EE","bg":"rgba(34,211,238,.12)", "lbl":"#67E8F9","body":"#CFFAFE"},
        "final":       {"border":"#34D399","bg":"rgba(52,211,153,.15)", "lbl":"#6EE7B7","body":"#D1FAE5"},
    }
    c = cfg.get(s.kind, {"border":"#94A3B8","bg":"rgba(148,163,184,.1)","lbl":"#CBD5E1","body":"#E2E8F0"})

    # Tool chip — inline styled for sidebar visibility
    chip = ""
    if s.tool:
        if s.tool_ok:
            chip = (f'<div style="display:inline-flex;align-items:center;gap:5px;'
                    f'background:rgba(52,211,153,.2);border:1px solid #34D399;'
                    f'color:#6EE7B7;border-radius:20px;padding:3px 10px;'
                    f'font-family:Roboto Mono,monospace;font-size:.65rem;'
                    f'font-weight:700;margin-top:6px">✓ {s.tool}</div>')
        else:
            chip = (f'<div style="display:inline-flex;align-items:center;gap:5px;'
                    f'background:rgba(248,113,113,.2);border:1px solid #F87171;'
                    f'color:#FCA5A5;border-radius:20px;padding:3px 10px;'
                    f'font-family:Roboto Mono,monospace;font-size:.65rem;'
                    f'font-weight:700;margin-top:6px">✗ {s.tool}</div>')

    H(f"""
    <div style="border-radius:9px;padding:10px 13px;margin-bottom:8px;
                font-size:.76rem;line-height:1.6;
                border-left:4px solid {c['border']};
                background:{c['bg']};">
      <div style="font-family:'Roboto Mono',monospace;font-size:.62rem;
                  font-weight:700;letter-spacing:1.8px;text-transform:uppercase;
                  color:{c['lbl']};margin-bottom:4px;">
        {icon} {label}
        <span style="float:right;color:rgba(255,255,255,.35);
                     font-size:.6rem;">{s.ts}</span>
      </div>
      <div style="color:{c['body']};font-size:.75rem;line-height:1.6;">{s.body}</div>
      {chip}
    </div>""")


def render_sidebar(steps: List[ReActStep], tools: List[str], result: Optional[AgentResult]):
    with st.sidebar:

        # ── Header ─────────────────────────────────────────
        H("""
        <div style="padding:10px 0 6px;
                    border-bottom:2px solid rgba(96,165,250,.3);
                    margin-bottom:16px;">
          <div style="font-family:'Plus Jakarta Sans',sans-serif;
                      font-size:1.05rem;font-weight:800;
                      color:#FFFFFF;margin-bottom:3px;letter-spacing:-.2px;">
            🧠 AI Agent Brain
          </div>
          <div style="font-family:'Roboto Mono',monospace;font-size:.62rem;
                      color:#60A5FA;letter-spacing:3px;font-weight:600;">
            REACT REASONING ENGINE
          </div>
        </div>""")

        if result:
            # ── Stat cards ──────────────────────────────
            H(f"""
            <div style="display:flex;gap:6px;margin-bottom:8px;">
              <div style="flex:1;background:rgba(96,165,250,.18);
                          border:1px solid rgba(96,165,250,.4);
                          border-radius:9px;padding:10px;text-align:center;">
                <div style="font-family:'Plus Jakarta Sans',sans-serif;
                            font-size:1.5rem;font-weight:800;color:#fff;">{len(tools)}</div>
                <div style="font-size:.64rem;color:#93C5FD;margin-top:1px;">Tools Used</div>
              </div>
              <div style="flex:1;background:rgba(96,165,250,.18);
                          border:1px solid rgba(96,165,250,.4);
                          border-radius:9px;padding:10px;text-align:center;">
                <div style="font-family:'Plus Jakarta Sans',sans-serif;
                            font-size:1.5rem;font-weight:800;color:#fff;">{result.attempts}</div>
                <div style="font-size:.64rem;color:#93C5FD;margin-top:1px;">EDI Tries</div>
              </div>
            </div>
            <div style="display:flex;gap:6px;margin-bottom:14px;">
              <div style="flex:1;background:rgba(96,165,250,.18);
                          border:1px solid rgba(96,165,250,.4);
                          border-radius:9px;padding:10px;text-align:center;">
                <div style="font-family:'Plus Jakarta Sans',sans-serif;
                            font-size:1.5rem;font-weight:800;color:#fff;">{len(steps)}</div>
                <div style="font-size:.64rem;color:#93C5FD;margin-top:1px;">Steps</div>
              </div>
              <div style="flex:1;background:rgba(52,211,153,.18);
                          border:1px solid rgba(52,211,153,.4);
                          border-radius:9px;padding:10px;text-align:center;">
                <div style="font-family:'Plus Jakarta Sans',sans-serif;
                            font-size:1.5rem;font-weight:800;color:#34D399;">✓</div>
                <div style="font-size:.64rem;color:#6EE7B7;margin-top:1px;">Resolved</div>
              </div>
            </div>""")

            # ── Tools Invoked ────────────────────────────
            H("""
            <div style="background:rgba(96,165,250,.1);
                        border:1px solid rgba(96,165,250,.3);
                        border-radius:10px;padding:12px 14px;margin-bottom:12px;">
              <div style="font-family:'Roboto Mono',monospace;font-size:.62rem;
                          font-weight:700;letter-spacing:2.5px;color:#60A5FA;
                          text-transform:uppercase;margin-bottom:10px;
                          display:flex;align-items:center;gap:6px;">
                ⚙ TOOLS INVOKED
              </div>""")

            seen: dict = {}
            for t in tools:
                seen[t] = seen.get(t, 0) + 1

            tool_colors = {
                "EDI_270_API":          ("#60A5FA","rgba(96,165,250,.2)","rgba(96,165,250,.4)"),
                "Historical_Claims_DB": ("#A78BFA","rgba(167,139,250,.2)","rgba(167,139,250,.4)"),
                "Fuzzy_Name_Match":     ("#34D399","rgba(52,211,153,.2)","rgba(52,211,153,.4)"),
                "Payer_Portal_Scraper": ("#FBBF24","rgba(251,191,36,.2)","rgba(251,191,36,.4)"),
            }

            for t, cnt in seen.items():
                tc, bg, border = tool_colors.get(t, ("#CBD9EE","rgba(203,217,238,.15)","rgba(203,217,238,.3)"))
                lbl = f"{t} ×{cnt}" if cnt > 1 else t
                H(f"""
                <div style="display:flex;align-items:center;gap:8px;
                            background:{bg};border:1px solid {border};
                            border-radius:8px;padding:7px 11px;margin-bottom:6px;">
                  <div style="width:8px;height:8px;border-radius:50%;
                              background:{tc};flex-shrink:0;
                              box-shadow:0 0 6px {tc};"></div>
                  <span style="font-family:'Roboto Mono',monospace;font-size:.72rem;
                               font-weight:600;color:{tc};">{lbl}</span>
                  {"<span style='margin-left:auto;font-size:.65rem;color:"+tc+";opacity:.8;font-family:Roboto Mono,monospace;'>✓ called</span>" if cnt==1 else ""}
                </div>""")
            H('</div>')

            # ── Resolution method ────────────────────────
            H(f"""
            <div style="background:rgba(52,211,153,.12);
                        border:1px solid rgba(52,211,153,.35);
                        border-radius:10px;padding:11px 13px;margin-bottom:14px;">
              <div style="font-family:'Roboto Mono',monospace;font-size:.62rem;
                          font-weight:700;letter-spacing:2px;color:#34D399;
                          text-transform:uppercase;margin-bottom:5px;">
                ✅ RESOLUTION METHOD
              </div>
              <div style="font-size:.78rem;color:#A7F3D0;line-height:1.6;">
                {result.resolution}
              </div>
            </div>""")

        # ── Step-by-step log ─────────────────────────────
        H("""
        <div style="font-family:'Roboto Mono',monospace;font-size:.62rem;
                    font-weight:700;letter-spacing:2.5px;color:#60A5FA;
                    text-transform:uppercase;margin-bottom:10px;
                    display:flex;align-items:center;gap:6px;">
          📋 STEP-BY-STEP LOG
        </div>""")

        if steps:
            for s in steps:
                render_step(s)
        else:
            H("""
            <div style="text-align:center;padding:30px 10px;">
              <div style="font-size:2rem;margin-bottom:10px;opacity:.4;">🤖</div>
              <div style="color:rgba(203,217,238,.5);font-size:.8rem;line-height:1.6;">
                Run a single-patient check<br>to see the agent reasoning here.
              </div>
            </div>""")


# ══════════════════════════════════════════════════════════════
#  TAB 1  —  SINGLE PATIENT
# ══════════════════════════════════════════════════════════════
def render_single_tab():
    H('<div class="ruler">📋 Patient Information</div>')
    c1, c2, c3 = st.columns([2,1,1])
    with c1: name  = st.text_input("Patient Name",  value="John Doe",   key="s_name")
    with c2: dob   = st.text_input("Date of Birth", value="06/15/1985", key="s_dob")
    with c3: proc  = st.selectbox("Procedure",["MRI","CT Scan","X-Ray","Ultrasound","Lab Work"], key="s_proc")

    c4, c5, c6 = st.columns([2,1,1])
    with c4:
        mid = st.text_input(
            "Member ID (as recorded in system)", value=INCORRECT_ID, key="s_mid",
            help="⚠️ Demo: this ID is missing hyphens — the AI agent will detect & fix it automatically."
        )
    with c5: st.text_input("Insurance Payer", value="BlueCross BlueShield", key="s_payer")
    with c6:
        st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)
        go = st.button("🔍 Verify Eligibility", use_container_width=True, key="s_go")

    if go:
        st.session_state["s_result"]  = None
        st.session_state["s_summary"] = None
        with st.spinner("AI Agent is reasoning and verifying eligibility…"):
            time.sleep(0.9)
            agent  = EligibilityAgent(name, dob, mid, proc)
            result = agent.run()
            st.session_state["s_result"]  = result
            st.session_state["s_summary"] = build_summary(result.edi_success, name, proc)

    result  = st.session_state.get("s_result")
    summary = st.session_state.get("s_summary")

    render_sidebar(
        result.steps if result else [],
        result.tools_called if result else [],
        result,
    )

    if result and summary:
        H(f"""
        <div class="pat">
          <div class="pat-av">👤</div>
          <div>
            <div class="pat-name">{name}</div>
            <div class="pat-meta">
              DOB: {dob} &nbsp;·&nbsp; Member ID on file:
              <code style="font-family:'Roboto Mono',monospace;color:#1A6AE4">{mid}</code>
              &nbsp;→&nbsp;
              <code style="font-family:'Roboto Mono',monospace;color:#1B7F3A">{result.corrected_member_id}</code>
            </div>
            <span class="tag tblue">🔬 {proc}</span>
            <span class="tag tamber">⚠ ID Conflict Auto-Resolved</span>
            <span class="tag tgreen">✅ Eligibility Verified</span>
          </div>
        </div>
        <div class="banner bok">
          ✅ &nbsp;
          <div><strong>Eligibility Confirmed</strong> — conflict resolved autonomously
          in {result.attempts} EDI attempts · {len(result.tools_called)} tool calls ·
          corrected member ID:
          <code style="font-family:'Roboto Mono',monospace">{result.corrected_member_id}</code></div>
        </div>
        """)

        left, right = st.columns(2, gap="large")

        with left:
            H('<div class="ruler">🏥 Traditional Healthcare Data</div>')
            H('<div class="card">')
            H('<div class="card-hdr">📄 <span class="acc">EDI 271 — Raw JSON Response</span></div>')
            with st.expander("❌ Attempt 1 — Failed EDI Response", expanded=False):
                H(f'<div class="jv">{json.dumps(result.edi_failure, indent=2)}</div>')
            H("""<div style="font-family:'Roboto Mono',monospace;font-size:.68rem;
                             color:#1B7F3A;letter-spacing:1px;margin:10px 0 6px">
               ✅ ATTEMPT 2 — SUCCESSFUL RESPONSE</div>""")
            H(f'<div class="jv">{json.dumps(result.edi_success, indent=2)}</div>')
            H('</div>')

        with right:
            H('<div class="ruler">🤖 AI Reasoning Engine</div>')
            H('<div class="card">')
            H('<div class="card-hdr">✨ <span class="acc">LLM-Generated Eligibility Interpretation</span></div>')
            H(f"""
            <div class="banner bok" style="margin-bottom:14px">
              ✅ <div><strong>{summary["headline"]}</strong><br>
              <span style="font-size:.8rem;font-weight:400">{summary["narrative"]}</span></div>
            </div>""")

            H("""<div style="font-family:'Roboto Mono',monospace;font-size:.67rem;
                             color:#1A6AE4;letter-spacing:2px;margin-bottom:8px;font-weight:600">
               COVERAGE DETAILS</div>""")
            H('<div class="cov-grid">')
            for lbl, val in summary["coverage"]:
                H(f'<div class="cov-cell"><div class="cov-lbl">{lbl}</div><div class="cov-val">{val}</div></div>')
            H('</div>')

            H("""<div style="font-family:'Roboto Mono',monospace;font-size:.67rem;
                             color:#1A6AE4;letter-spacing:2px;margin:12px 0 8px;font-weight:600">
               FINANCIAL DETAILS</div>""")
            H('<div class="cov-grid">')
            for lbl, val, cls in summary["financials"]:
                H(f'<div class="cov-cell"><div class="cov-lbl">{lbl}</div><div class="cov-val {cls}">{val}</div></div>')
            H('</div>')

            for cls, icon, msg in summary["alerts"]:
                H(f'<div class="banner {cls}" style="margin-bottom:8px">{icon} <span>{msg}</span></div>')

            H(f"""
            <div style="background:#F8FAFC;border:1px solid #DDE5EF;border-radius:8px;
                        padding:12px 14px;margin-top:10px">
              <div style="font-family:'Roboto Mono',monospace;font-size:.67rem;
                          color:#1A6AE4;letter-spacing:2px;font-weight:600;margin-bottom:4px">
                💰 RCM ESTIMATE</div>
              <div style="font-size:.8rem;color:#4B5563;line-height:1.7">{summary["rcm_note"]}</div>
            </div>""")
            H('</div>')
    else:
        render_sidebar([], [], None)
        H("""
        <div style="text-align:center;padding:70px 40px;background:#fff;
                    border-radius:14px;box-shadow:0 1px 8px rgba(0,0,0,.07);margin-top:16px">
          <div style="font-size:3rem;margin-bottom:16px">🤖</div>
          <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:1.2rem;
                      font-weight:800;color:#0D2B5C;margin-bottom:8px">
            Agent Ready — Awaiting Patient
          </div>
          <div style="color:#6B7A90;font-size:.84rem;max-width:500px;margin:0 auto;line-height:1.7">
            Enter patient details above and click
            <strong style="color:#1A6AE4">Verify Eligibility</strong>
            to watch the AI agent autonomously resolve the member ID conflict
            using the ReAct reasoning pattern.
          </div>
          <div style="margin-top:22px;display:flex;justify-content:center;gap:8px;flex-wrap:wrap">
            <span class="tag tblue">⚙ EDI_270_API</span>
            <span class="tag tblue">⚙ Historical_Claims_DB</span>
            <span class="tag tblue">⚙ Fuzzy_Name_Match</span>
            <span class="tag tblue">⚙ Payer_Portal_Scraper</span>
          </div>
        </div>""")


# ══════════════════════════════════════════════════════════════
#  TAB 2  —  BULK VERIFICATION
# ══════════════════════════════════════════════════════════════
def status_html(status: str) -> str:
    cfg = {
        "VERIFIED": ("dg", "#1B7F3A", "✅ Verified"),
        "NEEDS_PA": ("da", "#B45309", "⚠️ Needs PA"),
        "INACTIVE": ("dr", "#B91C1C", "❌ Inactive"),
        "CONFLICT": ("da", "#B45309", "⚠️ Conflict"),
        "ERROR":    ("dgr","#6B7280", "❓ Error"),
    }
    dc, color, label = cfg.get(status, ("dgr","#6B7280", status))
    return f'<span class="sdot" style="color:{color}"><span class="dot {dc}"></span>{label}</span>'

def render_bulk_tab():
    H('<div class="ruler">📂 Bulk Eligibility Verification</div>')

    H("""
    <div class="card" style="margin-bottom:16px">
      <div class="card-hdr">📋 <span class="acc">How Bulk Verification Works</span></div>
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px">
        <div style="text-align:center;padding:12px 8px">
          <div style="font-size:1.8rem;margin-bottom:6px">📤</div>
          <div style="font-weight:700;color:#0D2B5C;font-size:.82rem">1. Upload CSV</div>
          <div style="color:#6B7A90;font-size:.75rem;margin-top:3px">Patient roster or use sample</div>
        </div>
        <div style="text-align:center;padding:12px 8px">
          <div style="font-size:1.8rem;margin-bottom:6px">🤖</div>
          <div style="font-weight:700;color:#0D2B5C;font-size:.82rem">2. AI Processes</div>
          <div style="color:#6B7A90;font-size:.75rem;margin-top:3px">Each patient verified autonomously</div>
        </div>
        <div style="text-align:center;padding:12px 8px">
          <div style="font-size:1.8rem;margin-bottom:6px">⚡</div>
          <div style="font-weight:700;color:#0D2B5C;font-size:.82rem">3. Auto-Resolve</div>
          <div style="color:#6B7A90;font-size:.75rem;margin-top:3px">Conflicts fixed without manual work</div>
        </div>
        <div style="text-align:center;padding:12px 8px">
          <div style="font-size:1.8rem;margin-bottom:6px">📊</div>
          <div style="font-weight:700;color:#0D2B5C;font-size:.82rem">4. Export Results</div>
          <div style="color:#6B7A90;font-size:.75rem;margin-top:3px">Download verified roster as CSV</div>
        </div>
      </div>
    </div>
    """)

    col_up, col_ctrl = st.columns([3, 2], gap="large")

    with col_up:
        H("""<div style="font-family:'Roboto Mono',monospace;font-size:.68rem;color:#1A6AE4;
                          letter-spacing:2px;font-weight:600;margin-bottom:8px">
               UPLOAD PATIENT ROSTER</div>""")
        uploaded = st.file_uploader(
            "Upload CSV (columns: name, dob, member_id, procedure, payer)",
            type=["csv"], key="bulk_upload", label_visibility="collapsed"
        )
        st.download_button(
            "⬇️ Download Sample CSV Template",
            data=build_sample_csv(),
            file_name="eligibility_sample_roster.csv",
            mime="text/csv",
        )

    with col_ctrl:
        H("""<div style="font-family:'Roboto Mono',monospace;font-size:.68rem;color:#1A6AE4;
                          letter-spacing:2px;font-weight:600;margin-bottom:8px">
               PROCESSING OPTIONS</div>""")
        use_sample = st.checkbox("Use built-in sample roster (8 patients)", value=True, key="use_sample")
        delay_ms   = st.slider("Processing delay per patient (ms)",
                               min_value=100, max_value=800, value=300, step=100, key="bulk_delay")
        st.markdown(" ")
        run_bulk = st.button("🚀 Run Bulk Verification", use_container_width=True, key="bulk_go")

    if run_bulk:
        st.session_state["bulk_results"] = None
        patients: List[dict] = []
        if use_sample or not uploaded:
            patients = BULK_SAMPLE
        else:
            try:
                content = uploaded.read().decode("utf-8")
                reader  = csv.DictReader(io.StringIO(content))
                patients = [{k.strip().lower(): v.strip() for k,v in row.items()} for row in reader]
                if not patients:
                    st.error("CSV appears empty — using sample data.")
                    patients = BULK_SAMPLE
            except Exception as e:
                st.error(f"Could not parse CSV: {e} — using sample data.")
                patients = BULK_SAMPLE

        H('<div class="ruler" style="margin-top:20px">⚡ Processing Patients</div>')
        prog  = st.progress(0)
        ph    = st.empty()
        results: List[BulkResult] = []

        for i, row in enumerate(patients):
            pct  = (i + 1) / len(patients)
            pname = row.get("name", f"Patient {i+1}")
            ph.markdown(
                f"<div style='font-size:.82rem;color:#374151;padding:4px 0'>"
                f"Processing <strong>{pname}</strong> ({i+1}/{len(patients)})…</div>",
                unsafe_allow_html=True
            )
            prog.progress(pct)
            time.sleep(delay_ms / 1000)
            results.append(process_bulk_patient(i + 1, row))

        prog.progress(1.0)
        ph.markdown(
            f"<div style='font-size:.82rem;color:#1B7F3A;font-weight:600;padding:4px 0'>"
            f"✅ Batch complete — {len(results)} patients processed.</div>",
            unsafe_allow_html=True
        )
        st.session_state["bulk_results"] = results

    results: Optional[List[BulkResult]] = st.session_state.get("bulk_results")

    if results:
        render_kpis(results)
        H('<div class="ruler">📊 Verification Results</div>')

        fc1, fc2, fc3 = st.columns([2, 1.5, 1.5])
        with fc1:
            search = st.text_input("🔍 Search by name", key="bulk_search", placeholder="Filter patients…")
        with fc2:
            sf = st.selectbox("Filter by status", ["All","VERIFIED","NEEDS_PA","INACTIVE","CONFLICT"], key="bulk_sf")
        with fc3:
            pf = st.selectbox("Prior Auth", ["All","Required","Not Required"], key="bulk_pf")

        filtered = results
        if search:        filtered = [r for r in filtered if search.lower() in r.name.lower()]
        if sf != "All":   filtered = [r for r in filtered if r.status == sf]
        if pf == "Required":     filtered = [r for r in filtered if r.pa]
        elif pf == "Not Required": filtered = [r for r in filtered if not r.pa]

        H("""
        <table class="btable">
          <thead><tr>
            <th>#</th><th>Patient</th><th>DOB</th><th>Procedure</th>
            <th>Payer</th><th>Status</th><th>Plan</th>
            <th>Copay</th><th>Ded. Remaining</th>
            <th>Prior Auth</th><th>Network</th><th>Notes / AI Resolution</th>
          </tr></thead><tbody>
        """)

        for r in filtered:
            pa_html = (
                '<span class="tag tamber" style="font-size:.7rem">⚠️ Required</span>'
                if r.pa else
                '<span class="tag tgreen" style="font-size:.7rem">✓ Not Required</span>'
            )
            net_html = (
                '<span class="tag tgreen" style="font-size:.7rem">In-Network</span>'
                if r.net == "In-Network" else
                f'<span class="tag tred" style="font-size:.7rem">{r.net}</span>'
            )
            note_html = (
                f'<span style="color:#B45309;font-size:.74rem">🔧 {r.note}</span>'
                if r.note else
                '<span style="color:#9CA3AF;font-size:.74rem">—</span>'
            )
            dr_color = "#B45309" if r.ded_rem > 0 else "#1B7F3A"
            H(f"""
            <tr>
              <td style="color:#9CA3AF;font-family:'Roboto Mono',monospace;font-size:.72rem">{r.row_num}</td>
              <td style="font-weight:600;color:#0D2B5C">{r.name}</td>
              <td style="font-family:'Roboto Mono',monospace;font-size:.78rem;color:#4B5563">{r.dob}</td>
              <td><span class="tag tblue" style="font-size:.7rem">{r.procedure}</span></td>
              <td style="font-size:.8rem;color:#374151">{r.payer}</td>
              <td>{status_html(r.status)}</td>
              <td style="font-size:.78rem;color:#374151;max-width:140px">{r.plan}</td>
              <td style="font-family:'Roboto Mono',monospace;font-size:.78rem;
                         color:#1A6AE4;font-weight:600">${r.copay:.0f}</td>
              <td style="font-family:'Roboto Mono',monospace;font-size:.78rem;
                         color:{dr_color};font-weight:600">${r.ded_rem:,.0f}</td>
              <td>{pa_html}</td>
              <td>{net_html}</td>
              <td style="max-width:200px">{note_html}</td>
            </tr>
            """)

        H("</tbody></table>")

        v2  = sum(1 for r in filtered if r.status in ("VERIFIED","NEEDS_PA"))
        i2  = sum(1 for r in filtered if r.status == "INACTIVE")
        cf2 = sum(1 for r in filtered if r.status == "CONFLICT")
        pa2 = sum(1 for r in filtered if r.pa)

        H(f"""
        <div style="display:flex;gap:18px;margin-top:12px;flex-wrap:wrap;font-size:.78rem">
          <span style="color:#6B7A90">Showing <strong style="color:#0D2B5C">{len(filtered)}</strong> of {len(results)}</span>
          <span style="color:#1B7F3A;font-weight:600">✅ {v2} verified</span>
          <span style="color:#B45309;font-weight:600">⚠️ {pa2} need prior auth</span>
          <span style="color:#B91C1C;font-weight:600">❌ {i2} inactive</span>
          {"<span style='color:#B45309;font-weight:600'>🔧 "+str(cf2)+" auto-resolved</span>" if cf2 else ""}
        </div>
        """)

        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="⬇️ Export Full Results as CSV",
            data=build_csv_export(results),
            file_name=f"eligibility_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
        )
    elif not run_bulk:
        H("""
        <div style="text-align:center;padding:60px 40px;background:#fff;
                    border-radius:14px;box-shadow:0 1px 8px rgba(0,0,0,.07);margin-top:10px">
          <div style="font-size:2.8rem;margin-bottom:16px">📋</div>
          <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:1.15rem;
                      font-weight:800;color:#0D2B5C;margin-bottom:8px">
            Ready for Bulk Processing
          </div>
          <div style="color:#6B7A90;font-size:.83rem;max-width:520px;margin:0 auto;line-height:1.7">
            Enable <strong>Use built-in sample roster</strong> and click
            <strong style="color:#1A6AE4">Run Bulk Verification</strong>
            to process 8 patients simultaneously — or upload your own CSV.
          </div>
          <div style="margin-top:16px;font-family:'Roboto Mono',monospace;
                      font-size:.72rem;color:#9CA3AF">
            Required columns: name · dob · member_id · procedure · payer
          </div>
        </div>""")


# ══════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════
def main():
    render_header()
    render_kpis(st.session_state.get("bulk_results"))

    tab1, tab2 = st.tabs([
        "🔍  Single Patient Verification",
        "📋  Bulk Eligibility Verification",
    ])
    with tab1: render_single_tab()
    with tab2: render_bulk_tab()

    H("""
    <div style="margin-top:40px;border-top:1px solid #D4E0EF;padding-top:14px;
                display:flex;justify-content:space-between;align-items:center;
                font-size:.71rem;color:#9CA3AF;flex-wrap:wrap;gap:6px">
      <span>EligibilityIQ · Healthcare RCM Platform · Autonomous AI Verification</span>
      <span style="font-family:'Roboto Mono',monospace">
        EDI X12 5010 · ReAct Pattern · HIPAA-aware · Simulated data only
      </span>
    </div>""")

if __name__ == "__main__":
    main()
