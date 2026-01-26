import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="Smart Analyst The Beast", layout="wide")

# 2. التأكد من حالة تسجيل الدخول
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# 3. تصميم الواجهة (MIA8444 Style)
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    h1, h2, h3, p { color: #D4AF37 !important; text-align: center; }
    .stButton>button { 
        background-color: #D4AF37; 
        color: black; 
        border-radius: 15px;
        width: 100%;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 4. منطق التنقل بين الصفحات
if not st.session_state['logged_in']:
    # صفحة تسجيل الدخول
    st.title("🏆 Smart Analyst The Beast")
    st.subheader("نظام التحليل الذكي - النسخة الفخمة")
    
    user_id = st.text_input("الإيميل أو رقم الهاتف")
    user_password = st.text_input("كلمة السر", type="password")

    if st.button("دخول الوحش"):
        if user_id == "01005305955": # رقمك اللي ظهر في الصورة
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("بيانات الدخول غير صحيحة")
else:
    # صفحة الأدوات (هنا تعب امبارح كله هيظهر)
    st.title("🛠️ لوحة تحكم الوحش | MIA8444")
    st.success("تم تسجيل الدخول بنجاح! اختر الأداة التي تريد تشغيلها:")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("تحليل ملفات Excel"):
            st.info("جاري استدعاء excel_master.py...")
        if st.button("استخراج نصوص OCR"):
            st.info("جاري استدعاء ocr_engine.py...")
            
    with col2:
        if st.button("المحلل الذكي AI"):
            st.info("جاري استدعاء ai_analyst.py...")
        if st.button("تسجيل الخروج"):
            st.session_state['logged_in'] = False
            st.rerun()

st.markdown("<br><br><p style='font-size: 0.8em;'>© 2026 Smart Analyst The Beast | MIA8444</p>", unsafe_allow_html=True)
