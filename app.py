import streamlit as st
import os

# 1. إعدادات الصفحة
st.set_page_config(page_title="Smart Analyst The Beast", layout="wide")

# 2. إدارة الدخول
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# 3. هندسة الفخامة والوضوح (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    
    /* تنسيق التاج والاسم الملكي */
    .royal-header {
        text-align: center;
        color: #D4AF37;
        font-family: 'Georgia', serif;
        font-size: 2.5em;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(212, 175, 55, 0.5);
        margin-bottom: 5px;
    }
    
    .signature-box {
        text-align: center;
        background: linear-gradient(45deg, #1a1a1a, #000);
        border: 2px solid #D4AF37;
        color: #D4AF37 !important;
        padding: 10px 30px;
        border-radius: 50px;
        display: inline-block;
        font-weight: 900;
        font-size: 1.2em;
        box-shadow: 0 0 15px #D4AF37;
    }

    /* تنسيق أزرار الأدوات: وضوح جبار وأيقونات واضحة */
    div.stButton > button {
        background-color: #D4AF37 !important;
        color: #000000 !important; /* أسود صريح للكتابة */
        border-radius: 15px;
        font-weight: 900 !important;
        font-size: 24px !important; /* تكبير الخط لأقصى درجة */
        height: 4.5em;
        width: 100%;
        border: 4px solid #D4AF37;
        margin-bottom: 15px;
        box-shadow: 0 5px 15px rgba(212, 175, 55, 0.3);
    }

    div.stButton > button:hover {
        background-color: #FFD700 !important;
        transform: scale(1.02);
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

# 4. منطق التشغيل
if not st.session_state['logged_in']:
    # صفحة الدخول باللوجو 8888.jpg
    col1, col2, col3 = st.columns([1, 0.8, 1])
    with col2:
        if os.path.exists("8888.jpg"):
            st.image("8888.jpg", use_container_width=True)
    st.markdown("<h1 class='royal-header'>Smart Analyst The Beast</h1>", unsafe_allow_html=True)
    
    user_id = st.text_input("رقم الهاتف", value="01005305955")
    user_password = st.text_input("كلمة السر", type="password")
    if st.button("🔓 دخول الوحش"):
        st.session_state['logged_in'] = True
        st.rerun()
else:
    # --- لوحة تحكم المحلل الذكي الفخمة ---
    c_logo1, c_logo2, c_logo3 = st.columns([1, 0.4, 1])
    with c_logo2:
        if os.path.exists("8888.jpg"):
            st.image("8888.jpg", width=140)

    st.markdown("<h1 class='royal-header'>🛡️ لوحة تحكم المحلل الذكي</h1>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center;'><div class='signature-box'>👑 MIA8444 👑</div></div>", unsafe_allow_html=True)
    
    # شبكة الأدوات بأيقونات معبرة
    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("📊 تحليل ملفات EXCEL"):
            st.info("🚀 جاري فتح محرك Excel Master...")
        if st.button("🔍 استخراج نصوص OCR"):
            st.info("🚀 جاري تشغيل Beast OCR Engine...")
            
    with col_b:
        if st.button("🧠 المحلل الذكي AI"):
            st.info("🚀 جاري الاتصال بـ Brain Engine...")
        if st.button("🚪 تسجيل الخروج"):
            st.session_state['logged_in'] = False
            st.rerun()

st.markdown("<br><hr><p style='text-align: center; color: #555;'>© 2026 Smart Analyst The Beast | Engineered by MIA8444</p>", unsafe_allow_html=True)
