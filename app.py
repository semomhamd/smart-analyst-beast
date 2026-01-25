import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO, StringIO

# ================== 1. إعدادات الهوية ==================
st.set_page_config(page_title="Smart Analyst Beast", page_icon="🐉", layout="wide")

# تهيئة حالة الجلسة
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# ================== 2. محرك الأسلوب (Safe CSS) ==================
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: white; }
    [data-testid="stSidebar"] { background-color: #1E1E1E !important; border-right: 2px solid #00C853; }
    .stButton>button { background-color: #00C853; color: white; border-radius: 12px; font-weight: bold; height: 3em; border: none; }
    .signature-box { text-align: center; color: #00C853; font-family: 'Courier New'; padding: 10px; border: 1px solid #00C853; border-radius: 10px; margin-top: 20px; }
    .beast-title { font-size: 40px; font-weight: 800; color: #00C853; text-align: center; margin-bottom: 0px; }
</style>
""", unsafe_allow_html=True)

# ================== 3. نظام الدخول ==================
if st.session_state.current_user is None:
    st.markdown("<div class='beast-title'>SMART ANALYST BEAST</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; opacity:0.8; font-family:Courier;'>Designed by MIA8444</p>", unsafe_allow_html=True)
    
    with st.form("Login_Form"):
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.form_submit_button("Wake the Beast"):
            if u == "semomohamed" and p == "123456":
                st.session_state.current_user = u
                st.rerun()
            else:
                st.error("Invalid Credentials")
    st.stop()

# ================== 4. القائمة الجانبية ==================
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>🐲 BEAST</h2>", unsafe_allow_html=True)
    st.markdown("<div class='signature-box'>Developed by<br><b>MIA8444</b></div>", unsafe_allow_html=True)
    st.markdown("---")
    if st.button("Logout"):
        st.session_state.current_user = None
        st.rerun()

# ================== 5. الواجهة الرئيسية ==================
st.markdown(f"<h3>🚀 Welcome, {st.session_state.current_user}</h3>", unsafe_allow_html=True)
st.markdown("<div style='color:#00C853; font-style:italic;'>\"You don't have to be a data analyst.. Smart Analyst thinks for you\"</div>", unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["📂 Intake", "🧠 Analysis", "🧹 Cleaning"])

with t1:
    st.subheader("Data Upload")
    files = st.file_uploader("Upload Files", accept_multiple_files=True)
    if files:
        st.success("The Beast is processing your data...")

with t3:
    st.subheader("Manual Input & Clean")
    raw = st.text_area("Paste data here", height=150)
    if st.button("Process"):
        if raw:
            try:
                df = pd.read_csv(StringIO(raw))
                st.dataframe(df)
            except Exception as e:
                st.error(f"Error: {e}")
