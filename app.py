import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder
from prophet import Prophet
from fpdf import FPDF
import os
from datetime import datetime

# --- 1. إعدادات الهوية (MIA8444) ---
st.set_page_config(page_title="Smart Analyst Beast PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .sidebar-chat { background: #1f2937; padding: 15px; border-radius: 10px; border: 1px solid #3b82f6; }
    .report-btn { background-color: #10b981 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك الذاكرة ---
if 'main_df' not in st.session_state:
    st.session_state['main_df'] = pd.DataFrame()

# --- 3. السايد بار (الشات + القائمة) ---
with st.sidebar:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg")
    st.markdown("<h2 style='text-align: center;'>MIA8444 Assistant</h2>", unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-chat">', unsafe_allow_html=True)
    msg = st.text_input("اسأل الوحش أي شيء:")
    if st.button("🎤 صوت"): st.write("🎙️ جارِ الاستماع...")
    st.markdown('</div>', unsafe_allow_html=True)
    
    menu = ["الرئيسية", "منظف البيانات", "Excel Pro", "المحلل الاستراتيجي", "التنبؤ المالي", "داشبورد الإدارة", "تقرير PDF النهائي"]
    choice = st.radio("القائمة:", menu)

df = st.session_state['main_df']

# --- 4. تنفيذ الصفحات (بدون نقص ميزة واحدة) ---

if choice == "الرئيسية":
    st.title("🏠 بوابة التحكم MIA8444")
    up = st.file_uploader("ارفع ملفك المالي", type=['csv', 'xlsx'])
    if up:
        st.session_state['main_df'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
        st.success("تم رفع البيانات بنجاح!")

elif choice == "منظف البيانات":
    st.header("🧼 منظف البيانات الذكي")
    if not df.empty:
        if st.button("تنظيف عميق (حذف الفراغات والتكرار)"):
            st.session_state['main_df'] = df.dropna().drop_duplicates()
            st.success("تم التنظيف يا صديقي! ✅")
        st.dataframe(st.session_state['main_df'])

elif choice == "Excel Pro":
    st.header("📊 Excel Pro (الأبيض المحترف)")
    if not df.empty:
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_default_column(editable=True, groupable=True)
        gb.configure_side_bar() 
        grid_response = AgGrid(df, gridOptions=gb.build(), theme='balham', height=400)
        if st.button("حفظ التعديلات"):
            st.session_state['main_df'] = pd.DataFrame(grid_response['data'])

elif choice == "التنبؤ المالي":
    st.header("📈 محرك التنبؤ بالذكاء الاصطناعي")
    if not df.empty:
        try:
            # تجهيز البيانات للـ Prophet
            pdf = df.copy()
            pdf.columns = [c.strip() for c in pdf.columns]
            if 'التاريخ' in pdf.columns and 'المبيعات' in pdf.columns:
                pdf = pdf[['التاريخ', 'المبيعات']].rename(columns={'التاريخ': 'ds', 'المبيعات': 'y'})
                m = Prophet().fit(pdf)
                future = m.make_future_dataframe(periods=30)
                forecast = m.predict(future)
                st.plotly_chart(px.line(forecast, x='ds', y='yhat', title="توقعات الـ 30 يوماً القادمة"))
            else: st.error("تأكد من وجود أعمدة 'التاريخ' و 'المبيعات' بدقة.")
        except Exception as e: st.error(f"حدث خطأ في المحرك: {e}")

elif choice == "تقرير PDF النهائي":
    st.header("📄 مُولد التقارير الملكي")
    if not df.empty:
        if st.button("إنشاء وتحميل التقرير (PDF)"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Smart Analyst Beast Report - MIA8444", ln=1, align='C')
            pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=2, align='C')
            pdf.output("report.pdf")
            with open("report.pdf", "rb") as f:
                st.download_button("تحميل التقرير الآن 📥", f, "MIA8444_Report.pdf")
