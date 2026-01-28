import streamlit as st
import os

# 1. إعدادات الهوية الملكية (Architecture First)
st.set_page_config(page_title="Smart Analyst Beast", layout="wide")

# 2. إدارة الثيم (أبيض/أسود) وحفظ الاختيار
if 'theme' not in st.session_state:
    st.session_state.theme = 'Dark'

# تطبيق الألوان بناءً على اختيار المستخدم من الإعدادات
theme_style = """
    <style>
    .main { background-color: %s; color: %s; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%%; text-align: center; font-size: 10px; color: grey; padding: 10px; }
    </style>
""" % ("#000000" if st.session_state.theme == 'Dark' else "#ffffff", 
       "#D4AF37" if st.session_state.theme == 'Dark' else "#000000")
st.markdown(theme_style, unsafe_allow_html=True)

# 3. الهيدر (أعلى اليمين: اللغة والترس)
col_empty, col_lang, col_settings = st.columns([10, 1, 1])
with col_lang:
    st.button("🌐 AR/EN")
with col_settings:
    with st.popover("⚙️"):
        st.write("### الإعدادات")
        st.text_input("التسجيل (إيميل أو رقم)")
        if st.button("تبديل نمط الصفحة (Light/Dark)"):
            st.session_state.theme = 'Light' if st.session_state.theme == 'Dark' else 'Dark'
            st.rerun()

# 4. محتوى التطبيق الرئيسي (اللوجو والترسانة)
if os.path.exists("8888.jpg"):
    st.image("8888.jpg", width=200)
st.title("The Ultimate Financial Brain")

# 5. التوقيع MIA 8444 (Footer بخط صغير في الأسفل)
st.markdown("""
    <div class="footer">
        <span style="float: left; padding-left: 20px;">Smart Analyst Beast - v1.0</span>
        <span>Property of MIA8444 Signature</span>
        <span style="float: right; padding-right: 20px;">2026 © All Rights Reserved</span>
    </div>
""", unsafe_allow_html=True)
