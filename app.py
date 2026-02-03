import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
from io import BytesIO
from PIL import Image
import easyocr
from prophet import Prophet
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
from fpdf import FPDF
from datetime import datetime

# --- 1. الإعدادات الفخمة (MIA8444) ---
st.set_page_config(page_title="Smart Analyst Beast PRO", layout="wide", page_icon="🦁")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    [data-testid="stSidebar"] { background-color: #161b22; }
    .stMetric { background-color: #1f2937; padding: 20px; border-radius: 12px; border-top: 4px solid #3b82f6; }
    .radar-alert { background-color: #450a0a; border: 1px solid #ff4b4b; padding: 15px; border-radius: 10px; color: white; margin-bottom: 20px; }
    .sidebar-chat { background-color: #1f2937; padding: 15px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #3b82f6; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محركات الذكاء الاصطناعي (Caching) ---
if 'main_df' not in st.session_state:
    st.session_state['main_df'] = pd.DataFrame()

@st.cache_resource
def load_ocr_model():
    return easyocr.Reader(['ar', 'en'], gpu=False)

# --- 3. السايد بار (اللوجو + الشات + القائمة) ---
with st.sidebar:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_container_width=True)
    st.markdown("<h2 style='text-align: center;'>Smart Analyst Beast</h2>", unsafe_allow_html=True)
    
    # قسم الشات والمساعد الصوتي
    st.markdown('<div class="sidebar-chat">', unsafe_allow_html=True)
    st.markdown("💬 *مساعد MIA8444 الذكي*")
    user_msg = st.text_input("اسأل الوحش أو اكتب أمرك:", key="voice_chat_input")
    if st.button("🎤 تحدث (صوت)"):
        st.info("🎙️ جاري الاستماع للأمر الصوتي...")
    if user_msg:
        st.write(f"🤖: جاري تحليل طلبك يا صديقي...")
    st.markdown('</div>', unsafe_allow_html=True)
    
    menu = {
        "🏠 الرئيسية": "Home",
        "👁️ العين الرقمية (OCR)": "OCR",
        "🧼 منظف البيانات": "Clean",
        "📊 Excel Pro (الأبيض)": "Excel",
        "🧠 المحلل الاستراتيجي": "Analysis",
        "📈 التنبؤ المالي (AI)": "Forecast",
        "🖥️ داشبورد الإدارة": "Dashboard",
        "📄 تقرير PDF": "PDF"
    }
    choice = st.radio("القائمة التنفيذية:", list(menu.keys()))
    st.write("---")
    st.caption("MIA8444 Signature")

df = st.session_state['main_df']

# --- 4. منطق الصفحات (كامل بدون نقص) ---

# [الرئيسية والرادار]
if choice == "🏠 الرئيسية":
    st.title("🦁 بوابة التحكم الرئيسية")
    if not df.empty and 'المبيعات' in df.columns:
        avg = df['المبيعات'].mean()
        last = df['المبيعات'].iloc[-1]
        if last < avg * 0.7:
            st.markdown(f'<div class="radar-alert">⚠️ <b>رادار المخاطر:</b> المبيعات الأخيرة ({last}) منخفضة جداً عن المتوسط!</div>', unsafe_allow_html=True)
    
    up = st.file_uploader("ارفع ملف (Excel/CSV)", type=['csv', 'xlsx'])
    if up:
        st.session_state['main_df'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
        st.rerun()

# [العين الرقمية]
elif choice == "👁️ العين الرقمية (OCR)":
    st.header("👁️ محرك الرؤية MIA8444")
    reader = load_ocr_model()
    img_file = st.file_uploader("ارفع صورة جدول أو فاتورة", type=['jpg', 'png', 'jpeg'])
    if img_file:
        img = Image.open(img_file)
        st.image(img)
        if st.button("تحليل الصورة 🦁"):
            res = reader.readtext(np.array(img))
            texts = [r[1] for r in res]
            st.session_state['main_df'] = pd.DataFrame(texts, columns=["البيانات المستخرجة"])
            st.success("تم استخراج البيانات بنجاح!")

# [منظف البيانات]
elif choice == "🧼 منظف البيانات":
    st.header("🧼 وحدة التنظيف العميق")
    if not df.empty:
        if st.button("حذف القيم الفارغة والتكرارات"):
            st.session_state['main_df'] = df.dropna().drop_duplicates()
            st.success("تم التنظيف! ✅")
        st.dataframe(df)

# [Excel Pro الأبيض]
elif choice == "📊 Excel Pro (الأبيض)":
    st.header("📊 Excel Pro Dashboard")
    if not df.empty:
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_default_column(editable=True, groupable=True)
        gb.configure_side_bar() 
        grid_res = AgGrid(df, gridOptions=gb.build(), theme='balham', height=500)
        if st.button("حفظ التعديلات"):
            st.session_state['main_df'] = grid_res['data']

# [المحلل الاستراتيجي]
elif choice == "🧠 المحلل الاستراتيجي":
    st.header("🧠 التحليل العميق")
    if not df.empty:
        st.write(df.describe())
        if 'المبيعات' in df.columns:
            st.plotly_chart(px.box(df, y="المبيعات"))

# [التنبؤ المالي]
elif choice == "📈 التنبؤ المالي (AI)":
    st.header("📈 محرك التنبؤ بالذكاء الاصطناعي")
    if not df.empty:
        try:
            pdf = df.copy()
            # محاولة العثور على أعمدة التاريخ والمبيعات
            pdf.columns = [c.strip() for c in pdf.columns]
            ds_col = 'التاريخ' if 'التاريخ' in pdf.columns else pdf.columns[0]
            y_col = 'المبيعات' if 'المبيعات' in pdf.columns else pdf.columns[1]
            
            m_df = pdf[[ds_col, y_col]].rename(columns={ds_col: 'ds', y_col: 'y'})
            m_df['ds'] = pd.to_datetime(m_df['ds'])
            
            m = Prophet().fit(m_df)
            future = m.make_future_dataframe(periods=30)
            forecast = m.predict(future)
            st.plotly_chart(px.line(forecast, x='ds', y='yhat', title="توقعات المستقبل"))
        except: st.error("تأكد من وجود عمود 'التاريخ' وعمود 'المبيعات'.")

# [الداشبورد والتقارير]
elif choice == "🖥️ داشبورد الإدارة":
    if not df.empty and 'المبيعات' in df.columns:
        st.metric("إجمالي المبيعات", f"{df['المبيعات'].sum():,.0f}")
        st.plotly_chart(px.pie(df, values='المبيعات', names=df.columns[1]))

elif choice == "📄 تقرير PDF":
    if st.button("توليد تقرير MIA8444"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=15)
        pdf.cell(200, 10, txt="Smart Analyst Beast Report", ln=1, align='C')
        pdf.output("report.pdf")
        with open("report.pdf", "rb") as f:
            st.download_button("تحميل التقرير", f, "MIA8444_Report.pdf")
