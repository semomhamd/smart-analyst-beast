import streamlit as st
# استدعاء الترسانة كاملة
import ocr_engine, cleaner_pro, pdf_pro, sql_beast, excel_master
import power_bi_hub, python_analytics, tableau_connect, ai_vision

st.set_page_config(page_title="Smart Analyst Beast", layout="wide")

# الهوية البصرية
st.markdown("<h1 style='text-align:center; color:#00C853;'>🐉 SMART ANALYST BEAST v3.0</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; opacity:0.6;'>System Architect: MIA8444</p>", unsafe_allow_html=True)

# نظام التبويبات الشامل (الترسانة)
tabs = st.tabs([
    "📸 OCR", "🧹 Power Query", "📄 PDF Pro", "🗄️ SQL", 
    "🟢 Excel", "📊 Power BI", "🐍 Python", "📈 Tableau", "🤖 AI in Data"
])

# ربط كل تبويب بالملف بتاعه
with tabs[0]: ocr_engine.run_module()
with tabs[1]: cleaner_pro.run_module()
with tabs[2]: pdf_pro.run_module()
with tabs[3]: sql_beast.run_module()
with tabs[4]: excel_master.run_module()
with tabs[5]: power_bi_hub.run_module()
with tabs[6]: python_analytics.run_module()
with tabs[7]: tableau_connect.run_module()
with tabs[8]: ai_vision.run_module()
