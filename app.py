import streamlit as st
import pandas as pd

# استيراد جيش الملفات (تأكد أن الملفات الـ 10 في نفس المجلد)
try:
    import auth_system, excel_master, ocr_engine, cleaner_pro, sql_beast, pdf_pro, google_sheets_master, python_beast, power_bi_pro, ai_vision, tableau_expert
except:
    pass

# 1. إعدادات الصفحة
st.set_page_config(page_title="WANAS | MIA8444", layout="wide", initial_sidebar_state="expanded")

# 2. الواجهة واللوجو (التصميم الفخم)
def display_header():
    st.markdown("""
        <style>
        .header-box {
            background: linear-gradient(90deg, #000000 0%, #1a1a1a 100%);
            padding: 25px;
            border-bottom: 4px solid #D4AF37;
            text-align: center;
            border-radius: 15px;
            box-shadow: 0px 5px 15px rgba(212, 175, 55, 0.4);
        }
        .logo-main { color: #D4AF37; font-size: 50px; font-weight: bold; margin-bottom: 0px; }
        .logo-sub { color: #ffffff; font-size: 18px; letter-spacing: 2px; }
        .sig { color: #D4AF37; font-size: 12px; text-align: right; }
        [data-testid="stSidebar"] { direction: rtl; text-align: right; }
        </style>
        <div class="header-box">
            <div class="logo-main">WANAS | ونس</div>
            <div class="logo-sub">SMART ANALYST BEAST - THE LUXURY EDITION</div>
            <div class="sig">MIA8444</div>
        </div>
    """, unsafe_allow_html=True)

# 3. منطق التشغيل
def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        auth_system.run_auth()
    else:
        # عرض اللوجو والواجهة
        display_header()

        # القائمة الجانبية (الإعدادات على اليمين)
        with st.sidebar:
            st.markdown("<h2 style='color:#D4AF37;'>⚙️ الإعدادات</h2>", unsafe_allow_html=True)
            
            with st.expander("🌐 اللغة والمظهر", expanded=True):
                st.selectbox("اختر اللغة", ["العربية", "English"])
                st.select_slider("النمط", ["Dark", "Light"])
            
            st.markdown("---")
            st.markdown("<h3 style='color:#D4AF37;'>🛠️ الأدوات</h3>", unsafe_allow_html=True)
            tool = st.radio("", [
                "📊 إكسيل الوحش", "🤖 رؤية الوحش (AI Vision)", "👁️ ماسح OCR", 
                "🧹 منظف البيانات", "🗄️ محرك SQL", "📄 مستخرج PDF", 
                "☁️ Google Sheets", "🐍 بايثون", "📈 Power BI", "🖼️ Tableau"
            ])

            st.markdown("---")
            with st.expander("⚙️ حول التطبيق"):
                st.write("MIA8444 Signature")
                st.write("النسخة الفخمة النهائية")
                if st.button("🚪 تسجيل الخروج"):
                    st.session_state['logged_in'] = False
                    st.rerun()

        # تشغيل الأداة المختارة
        if tool == "📊 إكسيل الوحش": excel_master.run_excel_app()
        elif tool == "🤖 رؤية الوحش (AI Vision)": ai_vision.run_vision_ai()
        elif tool == "👁️ ماسح OCR": ocr_engine.run_ocr_app()
        elif tool == "🧹 منظف البيانات": cleaner_pro.run_cleaner()
        elif tool == "🗄️ محرك SQL": sql_beast.run_sql_app()
        elif tool == "📄 مستخرج PDF": pdf_pro.run_pdf_app()
        elif tool == "☁️ Google Sheets": google_sheets_master.run_sheets_app()
        elif tool == "🐍 بايثون": python_beast.run_python_app()
        elif tool == "📈 Power BI": power_bi_pro.run_powerbi()
        elif tool == "🖼️ Tableau": tableau_expert.run_tableau()

if _name_ == "_main_":
    main()
