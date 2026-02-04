import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
import easyocr
from prophet import Prophet
from st_aggrid import AgGrid, GridOptionsBuilder

# --- 1. الهوية الإدارية (MIA8444) ---
st.set_page_config(page_title="Smart Analyst Beast PRO", layout="wide", page_icon="🦁")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stMetric { background: linear-gradient(135deg, #1f2937 0%, #111827 100%); padding: 25px; border-radius: 15px; border-bottom: 4px solid #3b82f6; }
    .radar-alert { background-color: #450a0a; border: 1px solid #ff4b4b; padding: 15px; border-radius: 10px; color: white; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك الذاكرة ---
if 'main_df' not in st.session_state:
    st.session_state['main_df'] = pd.DataFrame()

@st.cache_resource
def load_ocr_model():
    return easyocr.Reader(['ar', 'en'], gpu=False)

# --- 3. وظائف الصفحات ---
def home_page():
    st.title("🦁 مركز التحكم - MIA8444")
    df = st.session_state['main_df']
    
    # الرادار المؤمن
    if not df.empty and 'المبيعات' in df.columns:
        sales_series = pd.to_numeric(df['المبيعات'], errors='coerce').dropna()
        if not sales_series.empty:
            avg, last = sales_series.mean(), sales_series.iloc[-1]
            if last < avg * 0.7:
                st.markdown(f'<div class="radar-alert">⚠️ رادار المخاطر: انخفاض في المبيعات الأخيرة ({last:,.0f})!</div>', unsafe_allow_html=True)
    
    up = st.file_uploader("ارفع ملف البيانات (Excel/CSV)", type=['csv', 'xlsx'])
    if up:
        st.session_state['main_df'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
        st.success("تم رفع البيانات بنجاح!")
        st.rerun()

def dashboard_page(df):
    st.title("🖥️ داشبورد الإدارة")
    if df.empty: return st.warning("الرجاء رفع ملف بيانات أولاً.")
    
    nums = df.select_dtypes(include=[np.number]).columns.tolist()
    if not nums: return st.error("لا توجد أعمدة رقمية للتحليل.")
    
    val_col = st.selectbox("اختر العمود التحليلي:", nums)
    c1, c2 = st.columns(2)
    c1.metric("إجمالي القيمة", f"{df[val_col].sum():,.0f}")
    c2.metric("عدد القيود", len(df))
    st.plotly_chart(px.area(df, y=val_col, title="منحنى الأداء"))

def excel_pro_page(df):
    st.title("📊 Excel Pro (MIA8444 Edition)")
    if df.empty: return st.warning("لا توجد بيانات.")
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(editable=True, groupable=True, filterable=True)
    gb.configure_side_bar()
    grid_res = AgGrid(df, gridOptions=gb.build(), theme='balham', height=400)
    if st.button("حفظ التعديلات"):
        st.session_state['main_df'] = pd.DataFrame(grid_res['data'])
        st.success("تم الحفظ!")

# --- 4. الهيكل الرئيسي ---
def main():
    with st.sidebar:
        if os.path.exists("8888.jpg"): st.image("8888.jpg")
        st.markdown("<h2 style='text-align: center;'>Smart Analyst Beast</h2>", unsafe_allow_html=True)
        choice = st.radio("القائمة:", ["الرئيسية", "الداشبورد", "Excel Pro"])
        st.caption("Owner: MIA8444")

    df = st.session_state['main_df']
    if choice == "الرئيسية": home_page()
    elif choice == "الداشبورد": dashboard_page(df)
    elif choice == "Excel Pro": excel_pro_page(df)

if __name__ == "__main__":
    main()
