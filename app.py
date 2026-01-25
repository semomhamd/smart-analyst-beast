import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# ================== 1. إعدادات الصفحة والهوية ==================
st.set_page_config(page_title="Smart Analyst Beast", page_icon="🐉", layout="wide")

# تهيئة الحالة
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'theme' not in st.session_state: st.session_state.theme = "Dark"

# ================== 2. محرك الأسلوب (CSS) مع التوقيع الصغير ==================
def apply_custom_style():
    bg = "#0E1117" if st.session_state.theme == "Dark" else "#F0F2F6"
    txt = "white" if st.session_state.theme == "Dark" else "black"
    accent = "#00C853"
    
    st.markdown(f"""
    <style>
        .stApp {{ background-color: {bg}; color: {txt}; }}
        .app-title {{ font-size: 45px; font-weight: 800; color: {accent}; margin-bottom: 0px; text-align: center; }}
        .app-signature {{ font-size: 14px; font-family: 'Courier New'; color: {txt}; opacity: 0.7; text-align: center; margin-top: -10px; letter-spacing: 2px; }}
        .welcome-msg {{ color: {accent}; font-size: 18px; font-weight: bold; text-align: center; margin-top: 20px; border: 1px dashed {accent}; padding: 10px; border-radius: 10px; }}
        [data-testid="stSidebar"] {{ border-right: 1px solid {accent}; }}
        .stButton>button {{ background-color: {accent}; color: white; border-radius: 12px; font-weight: bold; width: 100%; border: none; }}
    </style>
    """, unsafe_allow_input=True)

apply_custom_style()

# ================== 3. نظام الدخول ==================
if not st.session_state.logged_in:
    # اللوجو والعناوين في صفحة الدخول
    st.markdown("<div class='app-title'>SMART ANALYST BEAST</div>", unsafe_allow_html=True)
    st.markdown("<div class='app-signature'>by MIA8444</div>", unsafe_allow_html=True)
    
    st.image("https://raw.githubusercontent.com/username/repo/branch/99afc3d2-b6ef-4eda-977f-2fdc4b6621dd.jpg", width=180)
    
    with st.form("Login Form"):
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.form_submit_button("Wake the Beast"):
            if u == "semomohamed" and p == "123456":
                st.session_state.logged_in = True
                st.session_state.current_user = u
                st.rerun()
            else: st.error("Access Denied")
    st.stop()

# ================== 4. Sidebar مع التوقيع الصغير ==================
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>🐉 BEAST</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:12px; opacity:0.6;'>Eng. MIA8444 Signature</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.session_state.theme = st.radio("🌗 Mode", ["Dark", "Light"])
    st.markdown("---")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# ================== 5. الواجهة الرئيسية والجملة الديناميكية ==================
st.markdown("<div class='app-title'>SMART ANALYST BEAST</div>", unsafe_allow_html=True)
st.markdown("<div class='app-signature'>Designed & Engineered by MIA8444</div>", unsafe_allow_html=True)

st.markdown(f"<div class='welcome-msg'>\"You don't have to be a data analyst.. Smart Analyst thinks for you\"</div>", unsafe_allow_html=True)

tabs = st.tabs(["📂 Intake", "🧹 Cleaning", "📊 Analysis", "⭐ Dashboard", "📤 Export"])

# مثال بسيط للداشبورد الملون تلقائياً
with tabs[3]:
    st.subheader("Smart Visualization")
    df = pd.DataFrame({"Tool": ["Python", "PowerBI", "Excel", "Tableau"], "Power": [95, 85, 80, 75]})
    fig, ax = plt.subplots()
    sns.barplot(data=df, x="Tool", y="Power", palette="magma", ax=ax) # باليتة ألوان تلقائية
    st.pyplot(fig)
