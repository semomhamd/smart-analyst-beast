import streamlit as st
import pandas as pd
from PIL import Image

# استيراد موديولات الوحش المخصصة
from cleaner_pro import run_cleaner
from ai_analyst import run_analysis
from excel_master import run_excel_pro
from sql_beast import run_sql_beast
from google_sheets_master import connect_gsheets
from pdf_pro import export_report

# 1. إعدادات الهوية واللوجو MIA8444 [cite: 2026-01-26, 2026-01-28]
st.set_page_config(page_title="Smart Analyst Beast PRO", layout="wide")

# إظهار اللوجو وترس الإعدادات وزر اللغة [cite: 2026-01-15]
with st.sidebar:
    try:
        logo = Image.open("8888.jpg")
        st.image(logo, use_container_width=True)
    except:
        st.title("🦁 Beast Analyst")
    
    col1, col2 = st.columns(2)
    with col1: st.button("🌐 EN/AR")
    with col2: st.button("⚙️ Settings")
    
    st.markdown("---")
    choice = st.radio("الترسانة الذكية:", [
        "🏠 Data Hub (Home)",
        "🧹 Power Query (Cleaner)",
        "📊 Excel Master PRO",
        "🗄️ SQL & Cloud Memory",
        "🧠 AI Data Scientist",
        "📄 Final Report Center"
    ])
    st.info("Verified by: MIA8444")

# 2. الذاكرة الموحدة (The Unified Memory) [cite: 2026-01-16]
if 'main_data' not in st.session_state:
    st.session_state.main_data = pd.DataFrame()

# 3. توجيه الأوامر للملفات المنفصلة
if choice == "🏠 Data Hub (Home)":
    st.subheader("📥 مركز استقبال البيانات")
    uploaded = st.file_uploader("ارفع ملف Excel أو CSV", type=['xlsx', 'csv'])
    if uploaded:
        st.session_state.main_data = pd.read_excel(uploaded) if uploaded.name.endswith('xlsx') else pd.read_csv(uploaded)
        st.success("البيانات الآن في ذاكرة الوحش! 🔥")

elif choice == "🧹 Power Query (Cleaner)":
    run_cleaner() # استدعاء من ملف cleaner_pro.py

elif choice == "📊 Excel Master PRO":
    run_excel_pro() # استدعاء من ملف excel_master.py

elif choice == "🗄️ SQL & Cloud Memory":
    tab1, tab2 = st.tabs(["SQL Connector", "Google Sheets"])
    with tab1: run_sql_beast()
    with tab2: connect_gsheets()

elif choice == "🧠 AI Data Scientist":
    run_analysis(st.session_state.main_data) # استدعاء من ملف ai_analyst.py

elif choice == "📄 Final Report Center":
    export_report()
