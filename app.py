import streamlit as st
import os

# 1. إعدادات الصفحة (توسيع الشاشة لأقصى حد)
st.set_page_config(page_title="Smart Analyst The Beast", layout="wide")

# 2. إدارة حالة الدخول
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# 3. هندسة الفخامة والوضوح (MIA8444 Edition)
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    
    /* توهج الاسم الملكي */
    .royal-signature {
        color: #000000 !important;
        background-color: #D4AF37;
        padding: 10px 40px;
        border-radius: 50px;
        font-weight: 900;
        font-size: 1.5em;
        display: inline-block;
        border: 2px solid #FFFFFF;
        box-shadow: 0 0 25px rgba(212, 175, 55, 0.8);
        margin-bottom: 20px;
    }

    /* تنسيق الأزرار: خط عريض جداً وأسود واضح */
    div.stButton > button {
        background-color: #D4AF37 !important;
        color: #000000 !important;
        border-radius: 12px;
        font-weight: 900 !important;
        font-size: 20px !important;
        height: 4em;
        width: 100%;
        border: 3px solid #D4AF37;
        margin-bottom: 10px;
    }
    
    /* تنسيق الرسائل التوضيحية */
    .stInfo { background-color: #1a1a1a !important; color: #D4AF37 !important; border: 1px solid #D4AF37 !important; }
    </style>
""", unsafe_allow_html=True)

# 4. محتوى لوحة التحكم
if not st.session_state['logged_in']:
    # صفحة الدخول باللوجو 8888.jpg
    col_l1, col_l2, col_l3 = st.columns([1, 0.6, 1])
    with col_l2:
        if os.path.exists("8888.jpg"):
            st.image("8888.jpg", use_container_width=True)
    st.markdown("<h1 style='color:#D4AF37; text-align:center;'>Smart Analyst The Beast</h1>", unsafe_allow_html=True)
    
    user_id = st.text_input("رقم الهاتف", value="01005305955")
    user_password = st.text_input("كلمة السر", type="password")
    if st.button("دخول الوحش 🔓"):
        st.session_state['logged_in'] = True
        st.rerun()
else:
    # --- عرض لوحة تحكم المحلل الذكي ---
    col_t1, col_t2, col_t3 = st.columns([1, 0.4, 1])
    with col_t2:
        if os.path.exists("8888.jpg"):
            st.image("8888.jpg", width=140)

    st.markdown("<h1 style='color:#D4AF37; text-align:center;'>🛡️ لوحة تحكم المحلل الذكي</h1>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center;'><div class='royal-signature'>👑 MIA8444 👑</div></div>", unsafe_allow_html=True)
    
    # توزيع كافة الأدوات في 3 أعمدة لتظهر جميعاً
    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        if st.button("📊 تحليل EXCEL"):
            st.info("🚀 تشغيل Excel Master...")
        if st.button("🔍 استخراج OCR"):
            st.info("🚀 تشغيل OCR Engine...")

    with col_b:
        if st.button("🧠 ذكاء AI"):
            st.info("🚀 تشغيل AI Analyst...")
        if st.button("🧹 تنظيف البيانات"):
            st.info("🚀 تشغيل Cleaner Pro...")

    with col_c:
        if st.button("📈 تقارير BI"):
            st.info("🚀 تشغيل BI Hub...")
        if st.button("🚪 خروج"):
            st.session_state['logged_in'] = False
            st.rerun()

st.markdown("<br><hr><p style='text-align: center; color: #555;'>© 2026 Smart Analyst The Beast | MIA8444</p>", unsafe_allow_html=True)
