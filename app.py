import streamlit as st
import pandas as pd
import numpy as np
import google.generativeai as genai
import hashlib
import plotly.express as px
from io import BytesIO
from fpdf import FPDF

# 1. الإعدادات الملكية
st.set_page_config(page_title="Smart Analyst Ultimate Pro", layout="wide")

# 2. تفعيل Gemini (تأكد من كتابة المفتاح الصحيح هنا)
# ملحوظة: المفتاح اللي في الصورة كان ناقص، يرجى التأكد منه
genai.configure(api_key="AIzaSyBBiIEEGCzXpv80cwR9yzLXuQdj_J5n9tA")
model = genai.GenerativeModel('gemini-pro')

# وظائف الأمان
def make_hashes(password): return hashlib.sha256(str.encode(password)).hexdigest()
def check_hashes(password, hashed_text): return make_hashes(password) == hashed_text

if 'user_db' not in st.session_state:
    st.session_state.user_db = {"admin": make_hashes("1234"), "semomohamed": make_hashes("123456")} 
if 'auth' not in st.session_state: st.session_state.auth = False

# واجهة الدخول
if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center; color: #fbbf24;'>👑 Smart Analyst Pro Login</h1>", unsafe_allow_html=True)
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("دخول للنظام"):
        if u in st.session_state.user_db and check_hashes(p, st.session_state.user_db[u]):
            st.session_state.auth = True
            st.rerun()
        else: st.error("بيانات الدخول غير صحيحة")
    st.stop()

# 3. ستايل الألوان والتبويبات
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .main-header { background: linear-gradient(90deg, #161b22, #fbbf24); padding: 15px; border-radius: 15px; text-align: center; color: white; border: 2px solid #fbbf24; }
</style>
""", unsafe_allow_html=True)

# الهيدر
st.markdown("<div class='main-header'><h1>Smart Analyst Ultimate Pro</h1></div>", unsafe_allow_html=True)

# 4. المساعد الذكي في Sidebar
with st.sidebar:
    st.header("🤖 مساعدك الذكي Gemini")
    chat = st.text_input("اسأل المساعد...")
    if chat:
        try:
            res = model.generate_content(chat)
            st.info(res.text)
        except Exception as e: 
            st.error("تأكد من صحة الـ API Key في الكود")

# 5. منطقة العمل (التبويبات)
# هنا عرفنا t1, t2, t3 بالترتيب الصحيح
t1, t2, t3 = st.tabs(["📑 Excel Professional", "📊 Dashboards", "📥 PDF Export"])

with t1:
    st.subheader("📝 Microsoft Excel Workstation")
    up = st.file_uploader("ارفع ملف Excel أو CSV", type=['xlsx', 'csv'])
    if up:
        df = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
        st.data_editor(df, use_container_width=True, height=400)

with t2:
    st.subheader("📈 Professional Dashboards")
    if up:
        fig = px.area(df, template="plotly_dark", color_discrete_sequence=['#fbbf24'])
        st.plotly_chart(fig, use_container_width=True)
    else: st.warning("ارفع ملفاً أولاً")

with t3:
    st.subheader("📥 تقارير PDF النهائية")
    if st.button("تجهيز التقرير"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=15)
        pdf.cell(200, 10, txt="Smart Analyst Pro Report", ln=1, align='C')
        pdf_output = pdf.output(dest='S').encode('latin-1')
        st.download_button("تحميل الآن (PDF)", data=pdf_output, file_name="Report.pdf", mime="application/pdf")
        st.success("جاهز للتحميل!")

st.markdown("<p style='text-align: center; padding-top: 20px;'>Certified System | 2026</p>", unsafe_allow_html=True)
