import streamlit as st
import os

# 1. إعدادات الصفحة
st.set_page_config(page_title="Smart Analyst The Beast", layout="wide")

# 2. التأكد من حالة تسجيل الدخول
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# 3. تصميم الواجهة الاحترافي (MIA8444 Edition)
st.markdown("""
    <style>
    /* خلفية سوداء للتطبيق بالكامل */
    .stApp { background-color: #000000; }
    
    /* عناوين باللون الذهبي الملكي */
    h1, h2, h3, p { color: #D4AF37 !important; text-align: center; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* تنسيق أزرار الأدوات: خلفية ذهبية وكلام أسود عريض وواضح */
    div.stButton > button {
        background-color: #D4AF37 !important;
        color: #000000 !important; /* لون النص أسود صريح */
        border-radius: 10px;
        border: 2px solid #D4AF37;
        font-weight: 900 !important; /* أقصى درجة ثقل للخط */
        font-size: 20px !important; /* تكبير الخط للوضوح */
        height: 3.5em;
        width: 100%;
        margin-top: 10px;
        box-shadow: 2px 2px 5px rgba(212, 175, 55, 0.3);
    }

    /* تغيير لون الزرار عند الوقوف عليه */
    div.stButton > button:hover {
        background-color: #FFD700 !important;
        border: 2px solid #FFFFFF;
    }
    
    /* حقول الإدخال */
    .stTextInput>div>div>input {
        background-color: #1a1a1a;
        color: #D4AF37;
        border: 1px solid #D4AF37;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# 4. منطق عرض اللوجو والمحتوى
if not st.session_state['logged_in']:
    # --- صفحة الدخول ---
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        # استدعاء اللوجو 8888.jpg
        if os.path.exists("8888.jpg"):
            st.image("8888.jpg", use_container_width=True)
        else:
            st.markdown("<h1 style='font-size: 80px;'>🏆</h1>", unsafe_allow_html=True)
            
    st.title("Smart Analyst The Beast")
    
    user_id = st.text_input("الإيميل أو رقم الهاتف")
    user_password = st.text_input("كلمة السر", type="password")

    if st.button("دخول الوحش"):
        if user_id == "01005305955" or user_id == "admin": 
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("بيانات الدخول غير صحيحة")
else:
    # --- لوحة تحكم المحلل الذكي ---
    # وضع اللوجو في أعلى اللوحة
    c_logo1, c_logo2, c_logo3 = st.columns([1, 0.4, 1])
    with c_logo2:
        if os.path.exists("8888.jpg"):
            st.image("8888.jpg", width=120)

    st.title("🛡️ لوحة تحكم المحلل الذكي")
    st.markdown("<h3 style='margin-top: -20px;'>مرحباً بك يا وحش MIA8444</h3>", unsafe_allow_html=True)
    
    # شبكة الأدوات
    col_a, col_b = st.columns(2)
    
    with col_a:
        if st.button("📊 تحليل بيانات EXCEL"):
            st.info("بدء تشغيل excel_master.py...")
        if st.button("📝 استخراج نصوص OCR"):
            st.info("بدء تشغيل ocr_engine.py...")
        if st.button("🤖 المحلل الذكي AI"):
            st.info("بدء تشغيل ai_analyst.py...")

    with col_b:
        if st.button("🧹 منظف البيانات PRO"):
            st.info("بدء تشغيل cleaner_pro.py...")
        if st.button("📈 لوحة POWER BI"):
            st.info("بدء تشغيل power_bi_hub.py...")
        if st.button("🚪 تسجيل الخروج"):
            st.session_state['logged_in'] = False
            st.rerun()

st.markdown("<br><hr><p style='color: #444;'>© 2026 Smart Analyst The Beast | MIA8444</p>", unsafe_allow_html=True)
