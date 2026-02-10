import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression
import os

# ======== 1. الذاكرة المركزية (The Unified Brain) ========
if 'active_df' not in st.session_state:
    st.session_state.active_df = None 

# ======== 2. الهوية والإعدادات (UI/UX) ========
APP_NAME = "Smart Analyst"
AUTHOR_SIGNATURE = "MIA8444"
LOGO_FILE = "8888.jpg"

st.set_page_config(page_title=f"{AUTHOR_SIGNATURE} | {APP_NAME}", layout="wide")

# ستايل "التكنولوجيا المظلمة" الاحترافي
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0d1117; color: white; }}
    .footer {{ position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; padding: 10px; background: #161b22; color: #8b949e; border-top: 1px solid #58a6ff; font-size: 12px; z-index: 100; }}
    </style>
    """, unsafe_allow_html=True)

# ======== 3. القائمة الجانبية (Command Center) ========
with st.sidebar:
    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, use_container_width=True)
    st.markdown(f"<h2 style='text-align:center;'>{APP_NAME}</h2>", unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("القائمة الرئيسية:", [
        "🏠 مركز التحكم والبوابة",
        "📂 ورشة البيانات (رفع وتوليد)",
        "✨ منظف البيانات العالمي",
        "🔮 محرك التنبؤ AI",
        "⚙️ الإعدادات (الترس)"
    ])
    st.markdown("---")
    st.info(f"المستخدم: {AUTHOR_SIGNATURE}")

# ======== 4. تنفيذ الأدوات المربوطة ========

# --- قسم ورشة البيانات (الرفع والتوليد) ---
if menu == "📂 ورشة البيانات (رفع وتوليد)":
    st.header("📂 ورشة عمل البيانات (Data Hub)")
    
    tab1, tab2, tab3 = st.tabs(["📤 رفع ملفات", "🧪 توليد بيانات اختبار", "✍️ Excel Pro (إدخال يدوي)"])
    
    with tab1:
        st.subheader("تحميل ملفاتك الخاصة")
        uploaded_file = st.file_uploader("اختر ملف (Excel/CSV) لربطه بالمنصة", type=['csv', 'xlsx'])
        if uploaded_file:
            df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file)
            st.session_state.active_df = df
            st.success("Successfully uploaded and linked to system!")

    with tab2:
        st.subheader("مولد بيانات الاختبار (Data Generator)")
        rows = st.number_input("عدد الصفوف:", min_value=10, max_value=1000, value=100)
        if st.button("🚀 توليد بيانات اختبار فورية"):
            test_data = pd.DataFrame({
                'Date': pd.date_range(start='2025-01-01', periods=rows),
                'Sales': np.random.randint(1000, 5000, size=rows),
                'Costs': np.random.randint(500, 3000, size=rows),
                'Region': np.random.choice(['Cairo', 'Dubai', 'Riyadh'], size=rows)
            })
            st.session_state.active_df = test_data
            st.success(f"Generated {rows} rows for testing!")

    with tab3:
        st.subheader("Excel Pro: الإدخال اليدوي")
        # إذا كانت الذاكرة فارغة، نبدأ بجدول فارغ
        current_df = st.session_state.active_df if st.session_state.active_df is not None else pd.DataFrame(columns=["Category", "Value", "Note"])
        edited_df = st.data_editor(current_df, num_rows="dynamic", use_container_width=True)
        if st.button("💾 حفظ البيانات اليدوية"):
            st.session_state.active_df = edited_df
            st.success("Data Saved!")

# --- قسم منظف البيانات ---
elif menu == "✨ منظف البيانات العالمي":
    st.header("✨ محرك التنظيف (Beast Cleaner)")
    if st.session_state.active_df is not None:
        df = st.session_state.active_df
        st.write("البيانات الحالية:")
        st.dataframe(df.head())
        
        if st.button("🚀 تشغيل التنظيف التلقائي"):
            df_clean = df.drop_duplicates().dropna(how='all')
            st.session_state.active_df = df_clean
            st.success("Cleaning complete! Database updated.")
    else:
        st.warning("No data found. Please upload or generate data first.")

# --- قسم التنبؤ ---
elif menu == "🔮 محرك التنبؤ AI":
    st.header("🔮 AI Prediction Engine")
    if st.session_state.active_df is not None:
        df = st.session_state.active_df
        # رسم بياني ذكي
        fig = px.line(df, title="Data Trend Analysis")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Please provide data in the Data Hub first.")

# ======== 5. التوقيع (Footer) ========
st.markdown(f"<div class='footer'>Property of {AUTHOR_SIGNATURE} | MIA8444 © 2026</div>", unsafe_allow_html=True)
