# ============================================================
# Smart Analyst – Foundation Core
# Designed & Engineered by MIA8444
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="Smart Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------
# Session Defaults
# ---------------------------
if "auth" not in st.session_state:
    st.session_state.auth = {
        "logged_in": False,
        "user": None,
        "lang": "ar",
        "theme": "dark"
    }

if "users_db" not in st.session_state:
    # Demo in-memory users DB (قابل للاستبدال بقاعدة بيانات لاحقًا)
    st.session_state.users_db = {}

if "data" not in st.session_state:
    st.session_state.data = None

# ---------------------------
# Theme (Dark / Light)
# ---------------------------
def apply_theme(theme="dark"):
    if theme == "dark":
        st.markdown("""
        <style>
        .stApp { background-color: #0E1117; color: #EAEAEA; }
        [data-testid="stSidebar"] { background-color: #161A22; border-right: 1px solid #2A2F3A; }
        .stButton>button { background: linear-gradient(135deg,#22c55e,#16a34a); color:#0b1220; border-radius:12px; font-weight:700; border:none; height:3em; }
        .card { background:#0b1220; border:1px solid #1f2937; border-radius:16px; padding:16px; }
        .badge { background:#0ea5e9; color:#001018; padding:6px 10px; border-radius:999px; font-weight:700; }
        .sig { color:#22c55e; border:1px dashed #22c55e; border-radius:12px; padding:10px; text-align:center; }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .stApp { background-color: #F7F7FB; color: #0b1220; }
        [data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #E5E7EB; }
        .stButton>button { background: linear-gradient(135deg,#22c55e,#16a34a); color:#ffffff; border-radius:12px; font-weight:700; border:none; height:3em; }
        .card { background:#ffffff; border:1px solid #E5E7EB; border-radius:16px; padding:16px; }
        .badge { background:#0ea5e9; color:#ffffff; padding:6px 10px; border-radius:999px; font-weight:700; }
        .sig { color:#16a34a; border:1px dashed #16a34a; border-radius:12px; padding:10px; text-align:center; }
        </style>
        """, unsafe_allow_html=True)

apply_theme(st.session_state.auth["theme"])

# ---------------------------
# i18n (Arabic / English)
# ---------------------------
TXT = {
    "ar": {
        "app": "Smart Analyst",
        "login": "تسجيل الدخول",
        "signup": "إنشاء حساب",
        "email": "البريد الإلكتروني",
        "password": "كلمة المرور",
        "enter": "دخول",
        "logout": "تسجيل الخروج",
        "settings": "الإعدادات",
        "language": "اللغة",
        "theme": "المظهر",
        "dark": "داكن",
        "light": "فاتح",
        "upload": "رفع البيانات",
        "clean": "تنظيف البيانات",
        "analysis": "التحليل",
        "dashboard": "الداشبورد",
        "export": "التصدير",
        "welcome": "مرحباً",
        "nodata": "لا توجد بيانات — عرض افتراضي",
        "designed": "Designed & Engineered by MIA8444"
    },
    "en": {
        "app": "Smart Analyst",
        "login": "Login",
        "signup": "Sign up",
        "email": "Email",
        "password": "Password",
        "enter": "Enter",
        "logout": "Logout",
        "settings": "Settings",
        "language": "Language",
        "theme": "Theme",
        "dark": "Dark",
        "light": "Light",
        "upload": "Upload Data",
        "clean": "Data Cleaning",
        "analysis": "Analysis",
        "dashboard": "Dashboard",
        "export": "Export",
        "welcome": "Welcome",
        "nodata": "No data — showing demo",
        "designed": "Designed & Engineered by MIA8444"
    }
}

L = TXT[st.session_state.auth["lang"]]

# ---------------------------
# Auth Helpers
# ---------------------------
def signup(email, password):
    if email in st.session_state.users_db:
        return False, "User exists"
    st.session_state.users_db[email] = {
        "password": password,
        "created_at": datetime.utcnow().isoformat(),
        "prefs": {"lang": "ar", "theme": "dark"}
    }
    return True, "Created"

def login(email, password):
    user = st.session_state.users_db.get(email)
    if not user or user["password"] != password:
        return False
    st.session_state.auth["logged_in"] = True
    st.session_state.auth["user"] = email
    st.session_state.auth["lang"] = user["prefs"]["lang"]
    st.session_state.auth["theme"] = user["prefs"]["theme"]
    apply_theme(st.session_state.auth["theme"])
    return True

def save_prefs():
    u = st.session_state.auth["user"]
    if u:
        st.session_state.users_db[u]["prefs"] = {
            "lang": st.session_state.auth["lang"],
            "theme": st.session_state.auth["theme"]
        }

# ---------------------------
# Sidebar
# ---------------------------
with st.sidebar:
    st.markdown(f"## 📊 {L['app']}")
    st.markdown(f"<div class='sig'>{L['designed']}</div>", unsafe_allow_html=True)
    st.markdown("---")

    if st.session_state.auth["logged_in"]:
        st.write(f"*{L['welcome']}*: {st.session_state.auth['user']}")
  if st.button(f"🚪 {L['logout']}"):
    st.session_state.auth["logged_in"] = False
    st.session_state.auth["user"] = None
    st.session_state.auth["lang"] = "ar"
    st.session_state.auth["theme"] = "dark"
    st.rerun()      
    else:
        with st.form("auth"):
            email = st.text_input(L["email"])
            password = st.text_input(L["password"], type="password")
            c1, c2 = st.columns(2)
            if c1.form_submit_button(L["login"]):
                if login(email, password):
                    st.rerun()
                else:
                    st.error("Auth failed")
            if c2.form_submit_button(L["signup"]):
                ok, msg = signup(email, password)
                st.success(msg) if ok else st.error(msg)

    st.markdown("---")
    # Settings
    st.subheader(L["settings"])
    lang = st.selectbox(L["language"], ["ar", "en"], index=0 if st.session_state.auth["lang"]=="ar" else 1)
    theme = st.selectbox(L["theme"], ["dark", "light"], index=0 if st.session_state.auth["theme"]=="dark" else 1)
    if lang != st.session_state.auth["lang"] or theme != st.session_state.auth["theme"]:
        st.session_state.auth["lang"] = lang
        st.session_state.auth["theme"] = theme
        save_prefs()
        apply_theme(theme)
        st.rerun()

# ---------------------------
# Guard
# ---------------------------
if not st.session_state.auth["logged_in"]:
    st.stop()

# ---------------------------
# Main Tabs
# ---------------------------
tabs = st.tabs([
    f"📂 {L['upload']}",
    f"🧹 {L['clean']}",
    f"📈 {L['analysis']}",
    f"🧩 {L['dashboard']}",
    f"📤 {L['export']}",
])

# ---------------------------
# Upload
# ---------------------------
with tabs[0]:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    files = st.file_uploader("Upload files (xlsx, csv)", accept_multiple_files=True)
    if files:
        dfs = []
        for f in files:
            if f.name.lower().endswith(".xlsx"):
                dfs.append(pd.read_excel(f))
            elif f.name.lower().endswith(".csv"):
                dfs.append(pd.read_csv(f))
        if dfs:
            st.session_state.data = pd.concat(dfs, ignore_index=True)
            st.success("Loaded")
            st.dataframe(st.session_state.data.head())
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# Cleaning (Power Query-like)
# ---------------------------
with tabs[1]:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    if st.session_state.data is None:
        st.info(L["nodata"])
    else:
        df = st.session_state.data.copy()
        if st.checkbox("Remove duplicates"):
            df = df.drop_duplicates()
        if st.checkbox("Fill missing (numeric=0, text='')"):
            for c in df.columns:
                if pd.api.types.is_numeric_dtype(df[c]):
                    df[c] = df[c].fillna(0)
                else:
                    df[c] = df[c].fillna("")
        st.session_state.data = df
        st.dataframe(df.head())
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# Analysis (Demo)
# ---------------------------
with tabs[2]:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    if st.session_state.data is None:
        st.info(L["nodata"])
    else:
        st.write("Basic describe:")
        st.write(st.session_state.data.describe(include="all"))
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# Dashboard (Auto demo charts)
# ---------------------------
with tabs[3]:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    if st.session_state.data is None:
        demo = pd.DataFrame({
            "Month": ["Jan","Feb","Mar","Apr","May","Jun"],
            "Value": np.random.randint(50, 200, 6)
        })
        st.line_chart(demo.set_index("Month"))
        st.bar_chart(demo.set_index("Month"))
    else:
        df = st.session_state.data.select_dtypes(include=np.number)
        if not df.empty:
            st.line_chart(df)
            st.bar_chart(df)
        else:
            st.info("No numeric columns")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# Export
# ---------------------------
with tabs[4]:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    if st.session_state.data is not None:
        st.download_button(
            "Download CSV",
            st.session_state.data.to_csv(index=False).encode("utf-8"),
            file_name="smart_analyst_export.csv",
            mime="text/csv"
        )
    else:
        st.info(L["nodata"])
    st.markdown("</div>", unsafe_allow_html=True)
