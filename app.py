import streamlit as st
import pandas as pd
import numpy as np
import google.generativeai as genai
import hashlib
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="Smart Analyst Ultimate", layout="wide")

# 2. إعداد الذكاء الاصطناعي (تأكد من وضع الكود الصحيح هنا)
genai.configure(api_key="AIzaSyBBiIEEGCzXpv8OcwR9yzLXuQdj_J5n9tA")
model = genai.GenerativeModel('gemini-pro')

# --- وظائف الأمان والنظام العالمي ---
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

# محاكاة قاعدة بيانات (في المستقبل سنربطها بـ Supabase للأبد)
# تعديل الجزء الخاص بقاعدة البيانات المؤقتة
if 'user_db' not in st.session_state:
    st.session_state.user_db = {
        "admin": make_hashes("1234"),
        "semomohamed": make_hashes("123456") # ضفت لك اسمك هنا والباسورد يدوياً
    }
if 'auth' not in st.session_state:
    st.session_state.auth = False
# ----------------------------------

# 3. واجهة الدخول وإنشاء الحساب
if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center; color: #fbbf24;'>🔐 Smart Analyst Ultimate</h1>", unsafe_allow_html=True)
    
    tab_login, tab_signup = st.tabs(["تسجيل الدخول", "إنشاء حساب جديد"])
    
    with tab_login:
        user = st.text_input("اسم المستخدم", key="login_user")
        password = st.text_input("كلمة المرور", type="password", key="login_pass")
        if st.button("دخول للنظام"):
            if user in st.session_state.user_db and check_hashes(password, st.session_state.user_db[user]):
                st.session_state.auth = True
                st.success(f"مرحباً بك يا {user}")
                st.rerun()
            else:
                st.error("بيانات الدخول غير صحيحة")
                
    with tab_signup:
        new_user = st.text_input("اختر اسم مستخدم", key="signup_user")
        new_password = st.text_input("اختر كلمة مرور", type="password", key="signup_pass")
        confirm_password = st.text_input("تأكيد كلمة المرور", type="password")
        if st.button("تسجيل الحساب"):
            if new_password != confirm_password:
                st.warning("كلمات المرور غير متطابقة")
            elif new_user in st.session_state.user_db:
                st.warning("هذا المستخدم موجود بالفعل")
            else:
                st.session_state.user_db[new_user] = make_hashes(new_password)
                st.success("تم إنشاء الحساب بنجاح! انتقل لتبويب الدخول")
    st.stop()

# 4. الستايل والهيدر (بعد تسجيل الدخول)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .header-box { display: flex; align-items: center; justify-content: center; background: #161b22; padding: 15px; border-radius: 15px; border: 2px solid #fbbf24; }
    .footer-bar { position: fixed; bottom: 0; width: 100%; background: #161b22; color: #fbbf24; text-align: center; padding: 10px; border-top: 1px solid #fbbf24; }
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class='header-box'>
    <img src="https://raw.githubusercontent.com/semomhamd/smart-analyst-beast/main/99afc3d2-b6ef-4eda-977f-2fdc4b6621dd.jpg" style="width:60px; border-radius:10px; margin-left: 20px;">
    <h1 style='color: #fbbf24; margin: 0;'>Smart Analyst Ultimate</h1>
</div>
""", unsafe_allow_html=True)

# 5. المساعد الذكي في Sidebar
with st.sidebar:
    st.markdown("### 🤖 مساعد Gemini")
    chat = st.text_input("اسألني عن أي شيء...")
    if chat:
        try:
            res = model.generate_content(chat)
            st.info(res.text)
        except:
            st.error("حدث خطأ في الاتصال بالذكاء الاصطناعي")

# 6. منطقة العمل (Tabs)
t1, t2, t3 = st.tabs(["📊 البيانات", "🛠️ الأدوات", "📈 النتائج"])
with t1:
    up = st.file_uploader("ارفع ملفاتك هنا", accept_multiple_files=True)
    if up: st.success(f"تم استلام {len(up)} ملفات")

with t3:
    if up: st.line_chart(np.random.randn(20, 3))
    else: st.warning("الرجاء رفع الملفات أولاً")

# 7. الفوتر
st.markdown("<div class='footer-bar'>Smart Analyst Ultimate | Certified System by MIA8444 | 2026</div>", unsafe_allow_html=True)
