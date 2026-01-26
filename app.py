import streamlit as st
from auth_system import login_page

# ضبط إعدادات الصفحة الأساسية
st.set_page_config(page_title="Smart Analyst Beast v3.0", layout="wide")

# تشغيل واجهة الدخول الذهبية الخاصة بـ MIA8444
login_page()
