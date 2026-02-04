import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
import easyocr
from prophet import Prophet
from st_aggrid import AgGrid, GridOptionsBuilder

# --- 1. الإعدادات الرسمية والهوية ---
st.set_page_config(page_title="Smart Analyst Beast PRO", layout="wide", page_icon="🦁")

# CSS المخصص للهوية MIA8444
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stMetric { background: linear-gradient(135deg, #1f2937 0%, #111827 100%); padding: 25px; border-radius: 15px; border-bottom: 4px solid #3b82f6; }
    .radar-alert { background-color: #450a0a; border: 1px solid #ff4b4b; padding: 15px; border-radius: 10px; color: white; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محركات الذكاء (Caching) ---
@st.cache_resource
def load_ocr_model():
    return easyocr.Reader(['ar', 'en'], gpu=False)

# --- 3. وظائف الصفحات (المعمارية الجديدة) ---

def home_page():
    st.title("🦁 مركز التحكم - MIA8444")
    # رادار المخاطر المؤمن
    df = st.session_state.get('main_df', pd.DataFrame())
    if not df.empty and 'المبيعات' in df.columns:
        sales_series = pd.to_numeric(df['المبيعات'], errors='coerce').dropna()
        if not sales_series.empty:
            avg, last = sales_series.mean(), sales_series.iloc[-1]
            if last < avg * 0.7:
                st.markdown(f'<div class="radar-alert">⚠️ <b>رادار MIA8444:</b> انتباه! المبيعات الأخيرة منخفضة ({last:,.0f}).</div>', unsafe_allow_html=True)
    
    up = st.file_uploader("ارفع ملف البيانات (Excel/CSV)", type=['csv', 'xlsx'])
    if up:
        new_df = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
        st.session_state['main_df'] = new_df
        st.success("تم التحديث!")
        st.rerun()

def dashboard_page(df):
    st.title("🖥️ داشبورد الإدارة")
    if df.empty: return st.warning("الرجاء رفع بيانات أولاً.")
    
    nums = df.select_dtypes(include=[np.number]).columns.tolist()
    if not nums: return st.error("لا توجد أعمدة رقمية للتحليل.")
    
    val_col = st.selectbox("اختر العمود التحليلي الأساسي:", nums) # تحسين احترافي
    
    c1, c2 = st.columns(2)
    c1.metric("إجمالي القيمة", f"{df[val_col].sum():,.0f}")
    c2.metric("عدد القيود", len(df))
    
    st.plotly_chart(px.area(df, y=val_col, title="تحليل الأداء الزمني", color_discrete_sequence=['#3b82f6']))
    
    # زر النسخة الاحتياطية
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 تحميل نسخة احتياطية (Backup)", csv, "MIA8444_backup.csv", "text/csv")

def forecast_page(df):
    st.title("📈 التنبؤ بالذكاء الاصطناعي")
    if df.empty: return st.warning("لا توجد بيانات.")
    
    # البحث الآمن عن الأعمدة
    ds_col = next((c for c in df.columns if 'تاريخ' in c or 'date' in c.lower()), None)
    y_col = next((c for c in df.columns if 'مبيعات' in c or 'sales' in c.lower()), None)
    
    if not ds_col or not y_col:
        return st.error("عذراً.. لم أجد أعمدة 'التاريخ' و 'المبيعات' بشكل تلقائي.")
    
    with st.spinner("جاري قراءة المستقبل..."):
        m_df = df[[ds_col, y_col]].rename(columns={ds_col: 'ds', y_col: 'y'})
        m_df['ds'] = pd.to_datetime(m_df['ds'])
        m_df = m_df.sort_values("ds") # تحسين Prophet
        
        m = Prophet().fit(m_df)
        future = m.make_future_dataframe(periods=30)
        forecast = m.predict(future)
        st.plotly_chart(px.line(forecast, x='ds', y='yhat', title="توقعات الـ 30 يوماً القادمة"))

# --- 4. الهيكل التنفيذي ---
def main():
    if 'main_df' not in st.session_state:
        st.session_state['main_df'] = pd.DataFrame()

    with st.sidebar:
        if os.path.exists("8888.jpg"): st.image("8888.jpg")
        st.markdown("<h2 style='text-align: center;'>Smart Analyst Beast</h2>", unsafe_allow_html=True)
        choice = st.radio("القائمة الإدارية:", ["🏠 الرئيسية", "🖥️ الداشبورد", "📊 Excel Pro", "📈 التنبؤ"])
        st.caption("System Owner: MIA8444")

    # سحب الداتا بشكل ديناميكي
    current_df = st.session_state['main_df']

    if choice == "🏠 الرئيسية": home_page()
    elif choice == "🖥️ الداشبورد": dashboard_page(current_df)
    elif choice == "📈 التنبؤ": forecast_page(current_df)
    elif choice == "📊 Excel Pro":
        st.title("📊 محرر البيانات الأبيض")
        if not current_df.empty:
            gb = GridOptionsBuilder.from_dataframe(current_df)
            gb.configure_default_column(editable=True, groupable=True)
            grid_res = AgGrid(current_df, gridOptions=gb.build(), theme='balham')
            if st.button("تثبيت التعديلات"):
                st.session_state['main_df'] = pd.DataFrame(grid_res['data'])
                st.success("تم الحفظ!")

if _name_ == "_main_":
    main()
