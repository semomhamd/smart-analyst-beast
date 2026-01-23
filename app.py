import streamlit as st
import pandas as pd
import numpy as np
import google.generativeai as genai
import hashlib
import plotly.express as px
from io import BytesIO
from fpdf import FPDF

# 1. الإعدادات الملكية
st.set_page_config(page_title="Smart Analyst Pro", page_icon="📊", layout="wide")

# 2. اللوجو والذكاء الاصطناعي
# استبدلت الرابط برابط لوجو احترافي دائم
LOGO_URL = "https://cdn-icons-png.flaticon.com/512/1541/1541402.png" 

# تنبيه: المفتاح ده لازم يكون صحيح من Google AI Studio
genai.configure(api_key="AIzaSyBBiIEEGCzXpv80cwR9yzLXuQdj_J5n9tA")
model = genai.GenerativeModel('gemini-pro')

# وظائف الأمان
def make_hashes(password): return hashlib.sha256(str.encode(password)).hexdigest()
def check_hashes(password, hashed_text): return make_hashes(password) == hashed_text

if 'auth' not in st.session_state: st.session_state.auth = False

# واجهة الدخول
if not st.session_state.auth:
    st.image(LOGO_URL, width=100)
    st.title("🔐 Smart Analyst Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("دخول"):
        if u == "semomohamed" and p == "123456":
            st.session_state.auth = True
            st.rerun()
        else: st.error("بيانات خطأ")
    st.stop()

# 3. التصميم (CSS) لإظهار اللوجو في الجنب
st.markdown(f"""
    <style>
    [data-testid="stSidebarNav"] {{
        background-image: url({LOGO_URL});
        background-repeat: no-repeat;
        padding-top: 120px;
        background-position: 20px 20px;
        background-size: 80px;
    }}
    </style>
    """, unsafe_allow_html=True)

# 4. المساعد الذكي في الجنب
with st.sidebar:
    st.image(LOGO_URL, width=80)
    st.header("🤖 مساعد Gemini")
    chat = st.text_input("اسأل عن بياناتك...")
    if chat:
        try:
            res = model.generate_content(chat)
            st.info(res.text)
        except: st.error("المفتاح (API Key) فيه مشكلة")

# 5. التبويبات (Tabs) - حل مشكلة NameError
st.markdown("<h1 style='text-align:center; color:#fbbf24;'>Smart Analyst Ultimate Pro</h1>", unsafe_allow_html=True)
t1, t2, t3 = st.tabs(["📑 Excel Pro", "📈 Dashboards", "📥 PDF Export"])

with t1:
    st.subheader("📝 Microsoft Excel Workstation")
    up = st.file_uploader("ارفع ملف Excel أو CSV", type=['xlsx', 'csv'])
    if up:
        df = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
        st.data_editor(df, use_container_width=True)

with t2:
    st.subheader("📊 لوحة التحكم الذكية")
    if up:
        fig = px.bar(df, template="plotly_dark", color_discrete_sequence=['#fbbf24'])
        st.plotly_chart(fig, use_container_width=True)
    else: st.warning("ارفع ملف أولاً")

with t3:
    st.subheader("📥 تحميل التقرير النهائي")
    if st.button("صناعة تقرير PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=15)
        pdf.cell(200, 10, txt="Smart Analyst Ultimate Report", ln=1, align='C')
        pdf_out = pdf.output(dest='S').encode('latin-1')
        st.download_button("تحميل (PDF)", data=pdf_out, file_name="Report.pdf")
        st.success("تم التجهيز!")

st.markdown("<center>Certified System | 2026</center>", unsafe_allow_html=True)
