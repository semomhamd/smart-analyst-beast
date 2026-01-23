import streamlit as st
import pandas as pd
import numpy as np
import google.generativeai as genai
import hashlib
import plotly.express as px
from io import BytesIO
from fpdf import FPDF

# 1. الإعدادات الملكية (عشان نصلح العربي واللوجو)
st.set_page_config(page_title="Smart Analyst Pro", page_icon="📊", layout="wide")

# 2. اللوجو والذكاء الاصطناعي
# استخدمت اللوجو اللي ظهر معاك في آخر صورة (رقم 36)
LOGO_URL = "https://raw.githubusercontent.com/semomhamd/smart-analyst-beast/main/99afc3d2-b6ef-4eda-977f-2fdc4b6621dd.jpg"

# تصحيح الـ API Key (رسالة الخطأ 400 في صورة 33 كانت بسببه)
# اتأكد يا بطل إن المفتاح ده هو اللي نسخته من Google AI Studio
genai.configure(api_key="AIzaSyC9Vk1CHJ2DPiZoGCyFKJB1GAflQcB1FOU")
model = genai.GenerativeModel('gemini-pro')

# وظائف الأمان (Login)
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image(LOGO_URL, width=150)
        st.title("🔐 دخول المحلل الذكي")
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("دخول"):
            if u == "semomohamed" and p == "123456":
                st.session_state.auth = True
                st.rerun()
            else: st.error("بيانات الدخول غير صحيحة")
    st.stop()

# 3. ستايل الواجهة (عشان اللوجو يفضل ثابت في الجنب)
st.sidebar.image(LOGO_URL, use_column_width=True)
with st.sidebar:
    st.header("🤖 مساعدك Gemini")
    chat = st.text_input("اسأل عن بياناتك هنا...")
    if chat:
        try:
            res = model.generate_content(chat)
            st.info(res.text)
        except Exception as e:
            st.error("الـ API Key محتاج يتغير من الإعدادات")

# 4. منطقة التبويبات (حل مشكلة NameError في صورة 31)
st.markdown("<h1 style='text-align: center; color: #fbbf24;'>Smart Analyst Ultimate Pro</h1>", unsafe_allow_html=True)

# ترتيب التبويبات بالظبط زي ما البرنامج متوقعهم
t1, t2, t3 = st.tabs(["📑 Excel Pro", "📊 Dashboards", "📥 PDF Export"])

with t1:
    st.subheader("📝 محطة عمل إكسيل")
    up = st.file_uploader("ارفع ملف Excel أو CSV", type=['xlsx', 'csv'])
    if up:
        df = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
        st.data_editor(df, use_container_width=True)
        st.success("تم تحميل البيانات بنجاح")

with t2:
    st.subheader("📊 لوحة البيانات الاحترافية")
    if up:
        # رسم بياني تفاعلي (Plotly)
        fig = px.area(df, template="plotly_dark", color_discrete_sequence=['#fbbf24'])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("الرجاء رفع ملف في التبويب الأول أولاً")

with t3:
    st.subheader("📥 استخراج التقرير النهائي")
    if st.button("توليد ملف PDF"):
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt="Final Analysis Report", ln=1, align='C')
            
            # تحويل الملف لبايتات عشان يفتح صح (حل صورة 26)
            pdf_output = pdf.output(dest='S').encode('latin-1')
            st.download_button("تحميل التقرير (PDF)", data=pdf_output, file_name="Report.pdf", mime="application/pdf")
            st.success("✅ التقرير جاهز للتحميل!")
        except Exception as e:
            st.error(f"خطأ في التقرير: {e}")

st.markdown("<hr><center>Certified System | Designed for semomohamed | 2026</center>", unsafe_allow_html=True)
