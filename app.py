import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="Smart Analyst | MIA8444", layout="wide")

# 2. منطق الدارك واللايت (عشان يشتغل فوراً)
if 'theme' not in st.session_state:
    st.session_state.theme = 'Dark'

# 3. القائمة الجانبية (الإعدادات على اليمين)
with st.sidebar:
    st.markdown("<h2 style='text-align:right; color:#D4AF37;'>⚙️ الإعدادات</h2>", unsafe_allow_html=True)
    
    # تغيير اللغة
    st.selectbox("🌐 لغة التطبيق", ["العربية", "English"])
    
    # زرار الدارك واللايت (تصليح العطل)
    theme_choice = st.radio("🌓 نمط العرض", ["Dark", "Light"], 
                            index=0 if st.session_state.theme == 'Dark' else 1)
    
    if theme_choice != st.session_state.theme:
        st.session_state.theme = theme_choice
        st.rerun()

    st.markdown("---")
    st.markdown("<h3 style='text-align:right;'>🛠️ الأدوات</h3>", unsafe_allow_html=True)
    tool = st.radio("", [
        "📊 إكسيل الوحش", "🤖 AI Vision", "👁️ OCR", 
        "🧹 Cleaner", "🗄️ SQL", "📄 PDF Pro", 
        "☁️ Sheets", "🐍 Python", "📈 Power BI", "🖼️ Tableau"
    ])

# 4. اللوجو الفخم (تصليح الاختفاء)
theme_bg = "#0e1117" if st.session_state.theme == "Dark" else "#ffffff"
theme_text = "#D4AF37"

st.markdown(f"""
    <div style="background-color: #000000; padding: 30px; border-radius: 15px; border: 3px solid #D4AF37; text-align: center; margin-bottom: 25px;">
        <h1 style="color: #D4AF37; font-size: 50px; margin: 0; font-family: 'Arial';">SMART ANALYST</h1>
        <p style="color: #ffffff; font-size: 15px; letter-spacing: 3px; margin: 5px 0;">THE BEAST EDITION - INTELLIGENT DATA ENGINE</p>
        <div style="text-align: right; color: #D4AF37; font-size: 12px; font-weight: bold;">MIA8444 Signature</div>
    </div>
""", unsafe_allow_html=True)

# 5. تشغيل الأدوات مع حماية من الأخطاء (عشان الـ Power BI ميعملش Crash)
def start_beast():
    try:
        if tool == "📊 إكسيل الوحش":
            import excel_master; excel_master.run_excel_app()
        elif tool == "🤖 AI Vision":
            import ai_vision; ai_vision.run_vision_ai()
        elif tool == "👁️ OCR":
            import ocr_engine; ocr_engine.run_ocr_app()
        elif tool == "📈 Power BI":
            import power_bi_pro; power_bi_pro.run_powerbi()
        # إضافة باقي الأدوات هنا بنفس الطريقة...
    except ModuleNotFoundError as e:
        st.warning(f"⚠️ تنبيه: الملف {e.name} غير مرفوع حالياً. برجاء رفعه لتفعيل الأداة.")
    except Exception as e:
        st.error(f"❌ حدث خطأ: {e}")

# تصليح غلطة الصور (الشرطتين _name_)
if _name_ == "_main_":
    start_beast()
