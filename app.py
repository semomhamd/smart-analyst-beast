import streamlit as st
import os
import webbrowser
import importlib

# 1. إعدادات الصفحة
st.set_page_config(page_title="Smart Analyst The Beast", layout="wide")
st.markdown("<style>.stApp { background-color: #0e1117; color: #ffffff; }</style>", unsafe_allow_html=True)

# 2. الهيدر واللوجو
st.markdown("<div style='text-align:center; color:#888;'>EN/AR | ⚙️ Settings | 🌙 Dark Mode</div>", unsafe_allow_html=True)
col_l1, col_l2, col_l3 = st.columns([1, 0.4, 1])
with col_l2:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_container_width=True)

st.markdown("<h1 style='color:#D4AF37; text-align:center;'>Smart Analyst The Beast</h1>", unsafe_allow_html=True)

# 3. شريط الأدوات (الزراير)
cols = st.columns(8)
tools = ["OCR", "Excel", "Google Sheets", "Power BI", "SQL", "Cleaner Pro", "Python", "Tableau"]
for i, tool in enumerate(tools):
    with cols[i]:
        if st.button(tool, key=f"btn_{tool}"):
            st.session_state['active_tool'] = tool

# 4. منطقة العمل (الرجوع للرفع التلقائي لو الملف ناقص)
st.markdown("---")
col_gem, col_tool = st.columns(2)

with col_gem:
    st.markdown("<h4 style='color:#D4AF37;'>🤖 (Gemini AI) المحلل الذكي</h4>")
    st.chat_input("اسأل Gemini عن بياناتك...")

with col_tool:
    current = st.session_state.get('active_tool', 'Excel')
    st.markdown(f"<h4 style='color:#D4AF37;'>📂 أداة: {current}</h4>", unsafe_allow_html=True)
    
    # محاولة تشغيل الأداة الاحترافية
    try:
        if current == "Excel":
            import excel_master
            importlib.reload(excel_master)
            excel_master.run_excel_app()
        elif current == "OCR":
            import ocr_engine
            importlib.reload(ocr_engine)
            ocr_engine.run_ocr_app()
        elif current == "Google Sheets":
            import google_sheets_master
            importlib.reload(google_sheets_master)
            google_sheets_master.run_sheets_app()
        else:
            # المساحة اللي كانت مختفية رجعتها لك هنا للأدوات الباقية
            st.file_uploader(f"ارفع ملف {current}", type=['csv', 'xlsx', 'pdf'], key=f"up_{current}")
    
    except Exception as e:
        # لو فيه ملف ناقص، هيظهر مكان الرفع فوراً بدل الرسالة
        st.error(f"⚠️ محرك {current} غير مفعل (تأكد من وجود الملف البرمجي)")
        st.file_uploader(f"ارفع ملف {current} يدوياً الآن:", type=['csv', 'xlsx', 'pdf'], key=f"emergency_up_{current}")

# التوقيع MIA8444 [cite: 2026-01-26]
st.markdown("<br><p style='text-align:center; color:#555;'>MIA8444 Signature | Smart Analyst Beast</p>", unsafe_allow_html=True)
