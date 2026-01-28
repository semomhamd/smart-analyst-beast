import streamlit as st

# 1. إعدادات الصفحة (تأكد أنها أول أمر في الكود)
st.set_page_config(page_title="Smart Analyst | MIA8444", layout="wide")

# 2. إدارة الثيم (Session State)
if 'theme' not in st.session_state:
    st.session_state.theme = 'Dark'

# 3. القائمة الجانبية بتنسيق احترافي
with st.sidebar:
    st.markdown("<h2 style='text-align:right; color:#D4AF37;'>⚙️ الإعدادات</h2>", unsafe_allow_html=True)
    
    # اختيار اللغة
    st.selectbox("🌐 لغة التطبيق", ["العربية", "English"])
    
    # اختيار النمط
    theme_choice = st.radio("🌓 نمط العرض", ["Dark", "Light"], 
                            index=0 if st.session_state.theme == 'Dark' else 1)
    
    if theme_choice != st.session_state.theme:
        st.session_state.theme = theme_choice
        st.rerun()

    st.markdown("---")
    st.markdown("<h3 style='text-align:right;'>🛠️ الأدوات</h3>", unsafe_allow_html=True)
    
    # قائمة الأدوات
    tool = st.radio("", [
        "📊 إكسيل الوحش", "🤖 AI Vision", "👁️ OCR", 
        "🧹 Cleaner", "🗄️ SQL", "📄 PDF Pro", 
        "☁️ Sheets", "🐍 Python", "📈 Power BI", "🖼️ Tableau"
    ])

# 4. واجهة الهيدر (اللوجو الفخم)
# تم تحسين الـ CSS لضمان الظهور الصحيح للتوقيع MIA8444
st.markdown(f"""
    <div style="background-color: #000000; padding: 30px; border-radius: 15px; border: 3px solid #D4AF37; text-align: center; margin-bottom: 25px;">
        <h1 style="color: #D4AF37; font-size: 50px; margin: 0; font-family: 'Arial Black';">SMART ANALYST</h1>
        <p style="color: #ffffff; font-size: 15px; letter-spacing: 3px; margin: 5px 0;">THE BEAST EDITION - INTELLIGENT DATA ENGINE</p>
        <div style="text-align: right; color: #D4AF37; font-size: 12px; font-weight: bold; margin-top:10px;">MIA8444 Signature</div>
    </div>
""", unsafe_allow_html=True)

# 5. دالة تشغيل المحرك (The Engine)
def start_beast():
    try:
        if tool == "📊 إكسيل الوحش":
            st.info("جاري تشغيل محرك الإكسيل الذكي...")
            # تأكد من وجود ملف excel_master.py في نفس المجلد
            # import excel_master; excel_master.run_excel_app() 
        elif tool == "🤖 AI Vision":
            st.info("جاري تفعيل الرؤية الاصطناعية...")
        elif tool == "📈 Power BI":
            st.info("جاري الربط مع Power BI Dashboard...")
        else:
            st.write(f"أداة *{tool}* قيد التطوير في Sprint الحالي.")
            
    except ModuleNotFoundError as e:
        st.error(f"⚠️ نقص في الملفات: المكتبة أو الملف {e.name} غير متاح.")
    except Exception as e:
        st.error(f"❌ خطأ غير متوقع: {e}")

# تأكد من كتابة الشرط بهذا الشكل الدقيق (Double Underscore)
if _name_ == "_main_":
    start_beast()
