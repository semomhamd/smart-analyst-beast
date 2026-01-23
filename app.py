import streamlit as st
import pandas as pd
import numpy as np
import google.generativeai as genai
import hashlib
import plotly.express as px
from io import BytesIO
from fpdf import FPDF

# 1. الإعدادات الأساسية واللوجو
st.set_page_config(page_title="Smart Analyst Ultimate Pro", page_icon="📊", layout="wide")

LOGO_URL = "https://raw.githubusercontent.com/semomhamd/smart-analyst-beast/main/99afc3d2-b6ef-4eda-977f-2fdc4b6621dd.jpg"

# 2. إعداد Gemini (حل مشكلة الرسالة الوردية في صورة 33)
# تنبيه: إذا استمر الخطأ، تأكد من نسخ الكود البرمجي للمفتاح من Google AI Studio بدقة
genai.configure(api_key="AIzaSyBBiIEEGCzXpv80cwR9yzLXuQdj_J5n9tA")
model = genai.GenerativeModel('gemini-pro')

# 3. نظام الأمان
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image(LOGO_URL, width=150)
        st.title("🔐 تسجيل الدخول")
        u = st.text_input("اسم المستخدم")
        p = st.text_input("كلمة المرور", type="password")
        if st.button("دخول"):
            if u == "semomohamed" and p == "123456":
                st.session_state.auth = True
                st.rerun()
            else: st.error("بيانات غير صحيحة")
    st.stop()

# 4. الواجهة الجانبية (Sidebar)
st.sidebar.image(LOGO_URL, use_container_width=True)
with st.sidebar:
    st.header("🤖 مساعدك الذكي")
    chat = st.text_input("اسأل Gemini عن بياناتك...")
    if chat:
        try:
            res = model.generate_content(chat)
            st.info(res.text)
        except:
            st.warning("⚠️ محتاج يتغير من الإعدادات API Key الـ")

# 5. منطقة العمل الرئيسية (حل مشكلة NameError و ValueError)
st.markdown("<h1 style='text-align: center; color: #fbbf24;'>Smart Analyst Ultimate Pro</h1>", unsafe_allow_html=True)

# تعريف التبويبات قبل استخدامها (حل صورة 31)
t1, t2, t3 = st.tabs(["📑 Excel Pro", "📊 Dashboards", "📥 PDF Export"])

with t1:
    st.subheader("📝 إدارة ملفات الإكسيل")
    up = st.file_uploader("ارفع ملف Excel أو CSV", type=['xlsx', 'csv'])
    if up:
        # قراءة البيانات وتخزينها في session_state لضمان ثباتها
        if up.name.endswith('xlsx'):
            st.session_state.df = pd.read_excel(up)
        else:
            st.session_state.df = pd.read_csv(up)
        st.data_editor(st.session_state.df, use_container_width=True)
        st.success("✅ تم تحميل البيانات بنجاح")

with t2:
    st.subheader("📊 الرسوم البيانية الذكية")
    if 'df' in st.session_state:
        df = st.session_state.df
        # حل مشكلة الصورة 37 (اختيار الأعمدة الرقمية فقط للرسم)
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(num_cols) > 0:
            selected_col = st.selectbox("اختر العمود المراد رسمه:", num_cols)
            fig = px.area(df, y=selected_col, template="plotly_dark", color_discrete_sequence=['#fbbf24'])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("❌ الملف لا يحتوي على أعمدة رقمية لرسمها!")
    else:
        st.warning("الرجاء رفع ملف أولاً")

with t3:
    st.subheader("📥 التقارير النهائية")
    if st.button("توليد ملف PDF"):
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt="Smart Analyst Pro - Final Report", ln=1, align='C')
            
            # تصدير الملف كبايتات (حل مشكلة الصورة 26)
            pdf_output = pdf.output(dest='S').encode('latin-1')
            st.download_button(label="تحميل التقرير (PDF)", data=pdf_output, file_name="Report.pdf", mime="application/pdf")
            st.success("✅ الملف جاهز!")
        except Exception as e:
            st.error(f"حدث خطأ: {e}")

st.markdown("<hr><center>Certified System | 2026</center>", unsafe_allow_html=True)
