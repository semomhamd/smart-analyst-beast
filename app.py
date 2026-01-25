import streamlit as st
# استدعاء الملفات اللي لسه عاملينها
import ocr_engine as ocr
import cleaner_pro as clean

st.set_page_config(page_title="Smart Analyst Beast", layout="wide")

st.markdown("<h1 style='text-align:center; color:#00C853;'>🐉 SMART ANALYST BEAST</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; opacity:0.6;'>Engineered by MIA8444</p>", unsafe_allow_html=True)

# نظام التبويبات
tabs = st.tabs(["📸 OCR Engine", "🧹 Power Query", "🤖 AI & Analytics"])

with tabs[0]:
    ocr.run_ocr() # نداء على أداة الـ OCR من ملفها المنفصل

with tabs[1]:
    # نداء على أداة التنظيف
    if 'master_df' in st.session_state:
        clean.apply_power_query(st.session_state.master_df)
    else:
        st.info("Waiting for data source...")
