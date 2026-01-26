# © 2026 MIA8444 | THE BEAST v3.0
import streamlit as st
from auth_system import login_page

# استدعاء ملفاتك اللي تعبت فيها امبارح (كلها محفوظة وموجودة)
import ocr_engine, cleaner_pro, pdf_pro, sql_beast, excel_master
import power_bi_hub, python_analytics, tableau_connect, ai_vision

# 1. إعدادات الصفحة
st.set_page_config(page_title="Smart Analyst Beast v3.0", layout="wide")

# 2. تشغيل واجهة الدخول الذهبية (بصمتك الخاصة)
login_page()

# 3. ملاحظة للوحش: بمجرد تسجيل الدخول، كل الأدوات اللي فوق هتشتغل تلقائياً
