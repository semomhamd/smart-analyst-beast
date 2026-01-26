import streamlit as st
import os
import webbrowser
from fpdf import FPDF # تأكد من إضافة fpdf في ملف requirements.txt

# 1. إعدادات الصفحة واللوجو
st.set_page_config(page_title="Smart Analyst The Beast", layout="wide")

# 2. الهيدر الملكي (إضافة اللوجو 8888.jpg)
col_logo1, col_logo2, col_logo3 = st.columns([1, 0.4, 1])
with col_logo2:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_container_width=True) #

st.markdown("<h1 style='color:#D4AF37; text-align:center;'>Smart Analyst The Beast</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888;'>EN/AR | Settings | Dark Mode</p>", unsafe_allow_html=True)

# 3. شريط الأدوات السبعة (التفعيل المباشر)
st.markdown("<br>", unsafe_allow_html=True)
cols = st.columns(7)
tools = ["OCR", "Excel", "Power BI", "SQL", "Cleaner Pro", "Python", "Tableau"]
for i, tool in enumerate(tools):
    with cols[i]:
        if st.button(f" {tool}"):
            st.session_state['active_tool'] = tool

# 4. منطقة العمل (Gemini + ملفات)
st.markdown("---")
# --- 4. منطقة العمل (Gemini + ملفات) ---
st.markdown("---")
col_gem, col_file = st.columns(2)

with col_gem:
    st.markdown("<h4 style='color:#D4AF37;'>🤖 (Gemini AI) المحلل الذكي</h4>", unsafe_allow_html=True)
    st.chat_input("اسأل Gemini عن بياناتك...")
    st.info("الوحش جاهز (Anomaly Detection) لكشف أي خلل 🚨")

with col_file:
    # السطر ده لازم يكون تحت with ومزاح لليمين
    current = st.session_state.get('active_tool', 'Excel')
    st.markdown(f"<h4 style='color:#D4AF37;'>📂 أداة: {current}</h4>", unsafe_allow_html=True)
    
    if current == "Excel":
        try:
            import excel_master
            excel_master.run_excel_app()
        except Exception as e:
            st.warning("جاري تجهيز محرك اكسل... ارفع ملفك هنا")
            st.file_uploader("Upload", type=['xlsx', 'csv'], key="excel_up_fallback")
