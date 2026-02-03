import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
from prophet import Prophet
import speech_recognition as sr

# --- الإعدادات الفخمة (MIA8444) ---
st.set_page_config(page_title="Smart Analyst Beast PRO", layout="wide")

# تصميم الواجهة والألوان
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .radar-alert { background-color: #7f1d1d; color: white; padding: 15px; border-radius: 10px; border-left: 5px solid #ef4444; margin-bottom: 20px; }
    .sidebar-chat { background-color: #1f2937; padding: 10px; border-radius: 8px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. المساعد الصوتي والشات (موقعه: تحت اللوجو) ---
with st.sidebar:
    st.image("8888.jpg", use_container_width=True) # اللوجو الخاص بك
    st.markdown("<h3 style='text-align: center;'>Smart Analyst Assistant</h3>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="sidebar-chat">', unsafe_allow_html=True)
        user_msg = st.text_input("اسأل MIA8444...", placeholder="اكتب أمرك هنا...")
        col_voice, col_send = st.columns([1, 3])
        if col_voice.button("🎤"):
            st.write("🎙️ جارِ الاستماع...")
        if user_msg:
            st.info(f"الوحش: أنا بجهز لك تحليل لـ '{user_msg}' دلوقتي يا صديقي.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("---")
    menu = ["🏠 الرئيسية", "📊 Excel Pro", "📉 التنبؤ المالي", "👁️ العين الرقمية"]
    choice = st.sidebar.selectbox("القائمة التنفيذية:", menu)
    st.write("---")
    st.caption("Signature: MIA8444")

# --- 2. محرك الرادار الذكي (Smart Radar) ---
def run_smart_radar(data):
    if not data.empty and 'المبيعات' in data.columns:
        last_val = data['المبيعات'].iloc[-1]
        avg_val = data['المبيعات'].mean()
        if last_val < avg_val * 0.8:
            st.markdown(f"""
            <div class="radar-alert">
                ⚠️ <b>رادار المخاطر:</b> انخفاض ملحوظ! المبيعات الأخيرة ({last_val:,.0f}) أقل من المتوسط ({avg_val:,.0f}). انتبه للمخزون!
            </div>
            """, unsafe_allow_html=True)

# --- 3. صفحة Excel Pro (المحرر الأبيض) ---
if choice == "📊 Excel Pro":
    st.title("📊 Excel Pro Dashboard")
    st.write("أدوات إدخال البيانات الذكية - Pivot & Tools")
    
    # بيانات تجريبية إذا كان الجدول فارغاً
    if 'main_df' not in st.session_state or st.session_state['main_df'].empty:
        st.session_state['main_df'] = pd.DataFrame({
            'التاريخ': pd.date_range(start='2025-01-01', periods=5),
            'المنتج': ['ساعة', 'موبايل', 'لابتوب', 'ساعة', 'موبايل'],
            'المبيعات': [5000, 7000, 12000, 4500, 8000],
            'التكلفة': [3000, 4000, 8000, 2500, 5000]
        })

    # إعداد الجدول الأبيض الاحترافي (AgGrid)
    gb = GridOptionsBuilder.from_dataframe(st.session_state['main_df'])
    gb.configure_default_column(editable=True, groupable=True, value=True, enableRowGroup=True, aggFunc='sum')
    gb.configure_side_bar() # تفعيل Pivot Table وتصفية البيانات
    gb.configure_selection(selection_mode='multiple', use_checkbox=True)
    grid_options = gb.build()

    # عرض الجدول بثيم أبيض (Balham)
    response = AgGrid(
        st.session_state['main_df'],
        gridOptions=grid_options,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        fit_columns_on_grid_load=True,
        theme='balham', # الثيم الأبيض الاحترافي
        enable_enterprise_modules=True, # تفعيل أدوات الإكسل المتقدمة
        height=400,
        width='100%',
    )
    
    if st.button("حفظ البيانات المحدثة"):
        st.session_state['main_df'] = response['data']
        st.success("تم حفظ التعديلات في ذاكرة الوحش! ✅")

# --- 4. الصفحة الرئيسية والرادار ---
elif choice == "🏠 الرئيسية":
    st.title("🦁 Smart Analyst Beast Home")
    run_smart_radar(st.session_state.get('main_df', pd.DataFrame()))
    
    if 'main_df' in st.session_state:
        st.subheader("لمحة سريعة على البيانات الحالية")
        st.dataframe(st.session_state['main_df'], use_container_width=True)
    else:
        st.info("ارفع ملفاتك أو استخدم Excel Pro لبدء التحليل.")

# تذييل الصفحة
st.write("---")
st.markdown("<center>Proudly Developed by MIA8444 | 2026</center>", unsafe_allow_html=True)
