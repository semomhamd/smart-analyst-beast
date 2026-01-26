import streamlit as st
import os

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="Smart Analyst The Beast", layout="wide")

# 2. إدارة حالة الدخول واللغة
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'lang' not in st.session_state: st.session_state['lang'] = 'Arabic'

# 3. CSS الفخامة (الدارك مود والوضوح والتوقيع الأنيق)
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    
    /* شريط الأدوات العلوي (Header) */
    .top-bar {
        display: flex; justify-content: space-between; align-items: center;
        padding: 10px; border-bottom: 1px solid #D4AF37; margin-bottom: 20px;
    }

    /* أزرار الأدوات: وضوح جبار وأسود صريح */
    div.stButton > button {
        background-color: #D4AF37 !important;
        color: #000000 !important;
        font-weight: 900 !important;
        font-size: 18px !important;
        border-radius: 10px;
        height: 3.5em; width: 100%; border: none;
    }

    /* التوقيع الأنيق MIA8444 */
    .footer-signature {
        text-align: center; color: #555; font-size: 0.9em;
        margin-top: 50px; border-top: 0.5px solid #222; padding-top: 10px;
    }
    .mia-mark { color: #D4AF37; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 4. شريط الإعدادات العلوي
with st.container():
    col_set1, col_set2, col_set3 = st.columns([1, 1, 1])
    with col_set1:
        if st.button("🌐 English/عربي"):
            st.session_state['lang'] = 'English' if st.session_state['lang'] == 'Arabic' else 'Arabic'
    with col_set2:
        st.button("⚙️ Settings")
    with col_set3:
        st.button("🌙 Dark Mode")

# 5. منطق المحتوى
if not st.session_state['logged_in']:
    # صفحة الدخول باللوجو
    c1, c2, c3 = st.columns([1, 0.6, 1])
    with c2:
        if os.path.exists("8888.jpg"): st.image("8888.jpg", use_container_width=True)
    st.markdown("<h2 style='color:#D4AF37; text-align:center;'>Smart Analyst The Beast</h2>", unsafe_allow_html=True)
    
    user_id = st.text_input("رقم الهاتف", value="01005305955")
    user_password = st.text_input("كلمة السر", type="password")
    if st.button("🔓 دخول"):
        st.session_state['logged_in'] = True
        st.rerun()
else:
    # --- لوحة تحكم المحلل الذكي (الربط الفعلي) ---
    st.markdown("<h2 style='color:#D4AF37; text-align:center;'>🛡️ لوحة تحكم المحلل الذكي</h2>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        # ربط فعلي بملفات GitHub اللي عملناها
        if st.button("📊 تحليل EXCEL"):
            os.system("streamlit run excel_master.py") # أمر تشغيل الملف
        if st.button("📸 استخراج OCR"):
            os.system("streamlit run ocr_engine.py")
            
    with col_b:
        if st.button("🧠 ذكاء AI"):
            os.system("streamlit run ai_analyst.py")
        if st.button("🚪 خروج"):
            st.session_state['logged_in'] = False
            st.rerun()

# 6. التوقيع الأنيق (MIA8444)
st.markdown(f"""
    <div class='footer-signature'>
        Smart Analyst The Beast | <span class='mia-mark'>MIA8444</span>
    </div>
""", unsafe_allow_html=True)
