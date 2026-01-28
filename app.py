import streamlit as st

# 1. إعداد الصفحة الأساسي
st.set_page_config(page_title="Smart Analyst | MIA8444", layout="wide")

# 2. إضافة منطق الدارك واللايت في الواجهة
if 'theme' not in st.session_state:
    st.session_state.theme = 'Dark'

# 3. القائمة الجانبية (Sidebar) على اليمين
with st.sidebar:
    st.markdown("<h2 style='text-align:right; color:#D4AF37;'>⚙️ الإعدادات</h2>", unsafe_allow_html=True)
    
    # زرار اللغة
    st.selectbox("🌐 لغة التطبيق", ["العربية", "English"])
    
    # زرار الدارك واللايت (تعديل مباشر)
    theme_choice = st.radio("🌓 نمط العرض", ["Dark", "Light"], index=0 if st.session_state.theme == 'Dark' else 1)
    st.session_state.theme = theme_choice

    st.markdown("---")
    st.markdown("<h3 style='text-align:right;'>🛠️ الأدوات</h3>", unsafe_allow_html=True)
    tool = st.radio("", [
        "📊 إكسيل الوحش", "🤖 AI Vision", "👁️ OCR", 
        "🧹 Cleaner", "🗄️ SQL", "📄 PDF Pro", 
        "☁️ Sheets", "🐍 Python", "📈 Power BI", "🖼️ Tableau"
    ])
    
    st.markdown("---")
    with st.expander("ℹ️ حول التطبيق"):
        st.write("Smart Analyst Beast v2.0")
        st.write("Signature: MIA8444")
        if st.button("🚪 تسجيل الخروج"):
            st.session_state['logged_in'] = False
            st.rerun()

# 4. تنسيق اللوجو والواجهة بناءً على الثيم المختار
theme_bg = "#000000" if st.session_state.theme == "Dark" else "#ffffff"
theme_text = "#ffffff" if st.session_state.theme == "Dark" else "#000000"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {theme_bg}; }}
    .main-header {{
        background: linear-gradient(90deg, #000000 0%, #1a1a1a 100%);
        padding: 30px;
        border-radius: 15px;
        border: 3px solid #D4AF37;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0px 10px 20px rgba(212, 175, 55, 0.3);
    }}
    .logo-title {{ color: #D4AF37; font-size: 55px; font-weight: bold; margin: 0; font-family: sans-serif; }}
    .logo-sub {{ color: #ffffff; font-size: 18px; letter-spacing: 4px; text-transform: uppercase; }}
    .sig-text {{ color: #D4AF37; text-align: right; font-weight: bold; font-size: 14px; margin-top: 10px; }}
    </style>
    
    <div class="main-header">
        <h1 class="logo-title">SMART ANALYST</h1>
        <p class="logo-sub">The Beast Edition - Intelligent Data Engine</p>
        <div class="sig-text">MIA8444 Signature</div>
    </div>
""", unsafe_allow_html=True)

# 5. تشغيل الأدوات
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
    st.error(f"⚠️ تأكد من رفع ملف الأداة: {e}")

if _name_ == "_main_":
    pass
