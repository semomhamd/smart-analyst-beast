import streamlit as st
import pandas as pd
import numpy as np
import os
import google.generativeai as genai
from datetime import datetime

# إعداد الصفحة والستايل المظلم
st.set_page_config(page_title="Smart Analyst Beast", page_icon="🐉", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #121212; color: white; }
    [data-testid="stSidebar"] { background-color: #1E1E1E !important; }
    .stButton>button { background-color: #00C853; color: white; border-radius: 8px; border: none; height: 3em; font-weight: bold; }
    .stTabs [data-baseweb="tab-list"] { background-color: #121212; }
    .stTabs [data-baseweb="tab"] { color: white; background-color: #1E1E1E; border-radius: 5px; margin: 2px; }
    </style>
    """, unsafe_allow_input=True)

# القائمة الجانبية (Sidebar)
with st.sidebar:
    st.title("⚙️ Settings")
    lang = st.selectbox("Language", ["العربية", "English"])
    st.markdown("---")
    st.write("👤 User: MIA8444")
    st.write("🚀 Version: 2.5.0")
# نظام الدخول
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🐉 Smart Analyst Beast")
    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")
    if st.button("Login"):
        if user == "semomohamed" and pw == "123456":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Wrong Data!")
    st.stop()

# تفعيل AI (Gemini)
# حط مفتاح الـ API بتاعك مكان الكلمة دي
API_KEY = "YOUR_API_KEY_HERE"
if API_KEY != "YOUR_API_KEY_HERE":
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    model = None
# الواجهة الرئيسية
st.title("🚀 الوحش الذكي")
t1, t2 = st.tabs(["📂 رفع البيانات", "🧠 عقل الوحش"])

with t1:
    files = st.file_uploader("ارفع ملفاتك", accept_multiple_files=True)
    if files:
        all_dfs = [pd.read_excel(f) if f.name.endswith('xlsx') else pd.read_csv(f) for f in files]
        st.session_state.master_df = pd.concat(all_dfs, ignore_index=True)
        st.success("تم الدمج بنجاح!")
        st.dataframe(st.session_state.master_df.head(10))

with t2:
    if "master_df" in st.session_state:
        if st.button("🧠 ابدأ تحليل الذكاء الاصطناعي"):
            if model:
                with st.spinner("بيفكر..."):
                    summary = st.session_state.master_df.describe().to_string()
                    resp = model.generate_content(f"حلل البيانات دي بالعربي: {summary}")
                    st.write(resp.text)
            else:
                st.error("مفتاح الـ API ناقص!")
    else:
        st.warning("ارفع داتا الأول")
