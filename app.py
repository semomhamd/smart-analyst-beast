# © 2026 MIA8444 | THE BEAST v3.0
import streamlit as st
from auth_system import login_page

# إعدادات الصفحة
st.set_page_config(page_title="Smart Analyst Beast v3.0", layout="wide")

# تشغيل واجهة الدخول
login_page()
