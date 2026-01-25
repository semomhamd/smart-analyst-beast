import streamlit as st
import pandas as pd
import ocr_engine as ocr
import cleaner_pro as clean

# إعدادات الصفحة
st.set_page_config(page_title="Smart Analyst Beast", layout="wide")

# تأمين الجلسة (حل خطأ الصورة 5)
if 'auth' not in st.session_state: st.session_state.auth = False

# شاشة الدخول
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center;'>🐉 SMART ANALYST BEAST</h1>", unsafe_allow_html=True)
    with st.form("Login"):
        u = st.text_input("Username")
        if st.form_submit_button("Wake the Beast"):
            if u == "semomohamed":
                st.session_state.auth = True
                st.session_state.user = u
                st.rerun()
    st.stop()

# التطبيق بعد الدخول
st.markdown(f"<h3 style='color:#00C853;'>🐲 Welcome, {st.session_state.user}</h3>", unsafe_allow_html=True)
st.markdown("<p style='font-size:12px; opacity:0.6;'>Engineered by MIA8444</p>", unsafe_allow_html=True)

tabs = st.tabs(["📸 OCR Engine", "🧹 Power Query", "📊 Analytics"])
with tabs[0]: ocr.run_ocr()
with tabs[1]: clean.apply_clean(None)
