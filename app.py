import streamlit as st
import pandas as pd
import os

# 1. إعدادات الصفحة الأساسية (أول سطر في البرمجة)
st.set_page_config(page_title="Smart Analyst Beast", layout="wide")

# 2. إدارة الثيم (أبيض/أسود) وحفظها في الذاكرة
if 'theme' not in st.session_state:
    st.session_state.theme = 'Dark'

# تطبيق الألوان بناءً على اختيارك من ترس الإعدادات
bg_color = "#0e1117" if st.session_state.theme == 'Dark' else "#ffffff"
text_color = "#D4AF37" if st.session_state.theme == 'Dark' else "#000000"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; color: {text_color}; }}
    .footer {{ position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; font-size: 12px; color: #888; padding: 5px; background: transparent; }}
    </style>
. . ., unsaf…
