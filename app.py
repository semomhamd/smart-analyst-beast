import streamlit as st
import pandas as pd
import numpy as np
import os
import google.generativeai as genai
from datetime import datetime
import io

# ================== 1. إعدادات الواجهة (محمد إسماعيل) ==================
st.set_page_config(page_title="Smart Analyst Beast", page_icon="🐉", layout="wide")

# تهيئة حالة الجلسة
if 'theme' not in st.session_state: st.session_state.theme = 'dark'
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# الألوان بناءً على الثيم (Dark/Light)
if st.session_state.theme == 'dark':
    bg, txt, sidebar = '#0E1117', 'white', '#1E1E1E'
else:
    bg, txt, sidebar = '#F0F2F6', 'black', '#FFFFFF'

# تطبيق الـ CSS المصلح لتجنب أخطاء SyntaxError في الصور
st.markdown(f"""
<style>
    .stApp {{ background-color: {bg}; color: {txt}; }}
    [data-testid="stSidebar"] {{ background-color: {sidebar} !important; border-right: 1px solid #444; }}
    .stButton>button {{ background-color: #00C853; color: white; border-radius: 12px; font-weight: bold; width: 100%; border: none; height: 3em; }}
    .signature-box {{ text-align: center; color: #00C853; font-family: 'Courier New'; padding: 10px; border: 1px solid #00C853; border-radius: 10px; }}
</style>
""", unsafe_allow_input=True)

# ================== 2. القائمة الجانبية (Signature: mai8444) ==================
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>🐲</h1>", unsafe_allow_input=True)
    st.markdown(f"<div class='signature-box'>Developed by:<br><b>محمد إسماعيل</b><br>mai8444</div>", unsafe_allow_input=True)
    st.markdown("---")
    
    st.title("⚙️ الإعدادات")
    theme_choice = st.radio("وضع الشاشة / Mode", ["Dark", "Light"], horizontal=True)
    st.session_state.theme = theme_choice.lower()
    
    st.markdown("---")
    if st.button("🚪 تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()

# ================== 3. شاشة الدخول الآمن ==================
if not st.session_state.logged_in:
    st.title("🐉 Smart Analyst Beast")
    st.info("Authorized System for: محمد إسماعيل (mai8444)")
    with st.form("login_form"):
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.form_submit_button("دخول آمن"):
            if u == "semomohamed" and p == "123456":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("بيانات الدخول غير صحيحة")
    st.stop()

# ================== 4. تفعيل عقل الوحش (AI) ==================
# استبدل YOUR_API_KEY_HERE بمفتاحك الحقيقي من Google AI Studio
API_KEY = "YOUR_API_KEY_HERE" 

if API_KEY != "YOUR_API_KEY_HERE":
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    model = None

# ================== 5. المنصة الرئيسية ==================
st.title("🚀 Smart Analyst Beast")
st.write(f"مرحباً يا *محمد* | التوقيع المعتمد: *mai8444*")

tab1, tab2, tab3 = st.tabs(["📂 استيراد البيانات", "🧠 عقل الوحش", "📥 تصدير"])

# --- Tab 1: الرفع والدمج ---
with tab1:
    st.subheader("📥 رفع الملفات")
    uploaded_files = st.file_uploader("ارفع ملفات Excel أو CSV", accept_multiple_files=True, type=['csv', 'xlsx'])
    if uploaded_files:
        all_dfs = []
        for f in uploaded_files:
            try:
                df = pd.read_excel(f) if f.name.endswith('xlsx') else pd.read_csv(f)
                all_dfs.append(df)
                st.toast(f"✅ تم تحميل: {f.name}")
            except Exception as e: st.error(f"خطأ في ملف {f.name}: {e}")
        
        if all_dfs:
            st.session_state.master_df = pd.concat(all_dfs, ignore_index=True)
            st.success("تم دمج البيانات بنجاح!")
            st.dataframe(st.session_state.master_df.head(20), use_container_width=True)

# --- Tab 2: التحليل الذكي ---
with tab2:
    if "master_df" in st.session_state:
        if st.button("🧠 تشغيل عقل الوحش"):
            if model:
                with st.spinner("الوحش يحلل البيانات لمحمد إسماعيل..."):
                    summary = st.session_state.master_df.describe().to_string()
                    prompt = f"حلل هذه البيانات لمحمد إسماعيل (mai8444) وقدم تقرير بالعربية: {summary}"
                    response = model.generate_content(prompt)
                    st.session_state.ai_report = response.text
            else: st.error("⚠️ يرجى إضافة مفتاح API لتفعيل الذكاء الاصطناعي")
        
        if "ai_report" in st.session_state:
            st.markdown("---")
            st.markdown(st.session_state.ai_report)
            st.markdown(f"<p style='text-align: right;'><i>توقيع: mai8444</i></p>", unsafe_allow_input=True)
    else: st.warning("يرجى رفع البيانات أولاً")

# --- Tab 3: التصدير ---
with tab3:
    if "master_df" in st.session_state:
        csv = st.session_state.master_df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ تحميل الملف الموحد (CSV)", data=csv, file_name=f"mai8444_Beast_Report.csv")
