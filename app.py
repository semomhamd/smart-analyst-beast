import streamlit as st

# إعداد الصفحة
st.set_page_config(page_title="Smart Analyst | MIA8444", layout="wide")

# الواجهة واللوجو (Smart Analyst Beast)
st.markdown("""
    <div style="background-color: #000; padding: 20px; border-radius: 15px; border: 2px solid #D4AF37; text-align: center; margin-bottom: 20px;">
        <h1 style="color: #D4AF37; font-size: 45px; margin: 0;">SMART ANALYST</h1>
        <p style="color: #fff; font-size: 15px; letter-spacing: 3px;">THE BEAST EDITION</p>
        <p style="color: #D4AF37; text-align: right; font-weight: bold; margin: 0;">MIA8444</p>
    </div>
""", unsafe_allow_html=True)

# الإعدادات على اليمين (Sidebar)
with st.sidebar:
    st.markdown("<h2 style='text-align:right;'>⚙️ الإعدادات</h2>", unsafe_allow_html=True)
    st.selectbox("🌐 اللغة", ["العربية", "English"])
    st.radio("🌓 المظهر", ["Dark", "Light"])
    st.markdown("---")
    st.markdown("### 🛠️ الأدوات")
    tool = st.radio("", [
        "📊 إكسيل الوحش", "🤖 AI Vision", "👁️ OCR", 
        "🧹 Cleaner", "🗄️ SQL", "📄 PDF Pro", 
        "☁️ Sheets", "🐍 Python", "📈 Power BI", "🖼️ Tableau"
    ])
    st.markdown("---")
    if st.button("🚪 تسجيل الخروج"):
        st.session_state['logged_in'] = False
        st.rerun()

# الربط بالملفات
try:
    if tool == "📊 إكسيل الوحش":
        import excel_master; excel_master.run_excel_app()
    elif tool == "🤖 AI Vision":
        import ai_vision; ai_vision.run_vision_ai()
    elif tool == "👁️ OCR":
        import ocr_engine; ocr_engine.run_ocr_app()
    elif tool == "🧹 Cleaner":
        import cleaner_pro; cleaner_pro.run_cleaner()
    elif tool == "🗄️ SQL":
        import sql_beast; sql_beast.run_sql_app()
    elif tool == "📄 PDF Pro":
        import pdf_pro; pdf_pro.run_pdf_app()
    elif tool == "☁️ Sheets":
        import google_sheets_master; google_sheets_master.run_sheets_app()
    elif tool == "🐍 Python":
        import python_beast; python_beast.run_python_app()
    elif tool == "📈 Power BI":
        import power_bi_pro; power_bi_pro.run_powerbi()
    elif tool == "🖼️ Tableau":
        import tableau_expert; tableau_expert.run_tableau()
except Exception as e:
    st.error(f"تأكد من وجود جميع ملفات الأدوات في المجلد: {e}")
