import streamlit as st
import pandas as pd
import numpy as np
import google.generativeai as genai
from datetime import datetime
import io

# ================== 1. إعدادات الواجهة والجماليات ==================
st.set_page_config(page_title="Smart Analyst Beast", page_icon="🐉", layout="wide")

# تهيئة حالة الجلسة (Session State)
if 'theme' not in st.session_state: st.session_state.theme = 'dark'
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# تحديد الألوان بناءً على الثيم المختار
if st.session_state.theme == 'dark':
    bg, txt, card = '#0E1117', 'white', '#1E1E1E'
else:
    bg, txt, card = '#F0F2F6', 'black', '#FFFFFF'

# تطبيق الـ CSS المصلح (تم استبدال f-string بطريقة آمنة لتجنب TypeError)
st.markdown(f"""
<style>
    .stApp {{
        background-color: {bg};
        color: {txt};
    }}
    [data-testid="stSidebar"] {{
        background-color: {card} !important;
        border-right: 1px solid #444;
    }}
    .stButton>button {{
        background-color: #00C853;
        color: white;
        border-radius: 12px;
        font-weight: bold;
        width: 100%;
        border: none;
        height: 3em;
    }}
    .signature-box {{
        text-align: center;
        color: #00C853;
        font-family: 'Courier New';
        padding: 10px;
        border: 1px solid #00C853;
        border-radius: 10px;
        margin-top: 20px;
    }}
</style>
""", unsafe_allow_input=True)

# ================== 2. القائمة الجانبية (محمد إسماعيل | mai8444) ==================
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>🐲</h1>", unsafe_allow_input=True)
    st.markdown(f"<div class='signature-box'>Developed by:<br><b>محمد إسماعيل</b><br>mai8444</div>", unsafe_allow_input=True)
    st.markdown("---")
    
    st.title("⚙️ الإعدادات")
    theme_choice = st.radio("وضع الشاشة / Mode", ["Dark", "Light"], horizontal=True)
    if theme_choice.lower() != st.session_state.theme:
        st.session_state.theme = theme_choice.lower()
        st.rerun()
    
    st.markdown("---")
    if st.button("🚪 تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()

# ================== 3. نظام الدخول الآمن ==================
if not st.session_state.logged_in:
    st.title("🐉 Smart Analyst Beast")
    st.info("نظام التحليل الخاص بـ: محمد إسماعيل (mai8444)")
    with st.form("login"):
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.form_submit_button("دخول آمن"):
            if u == "semomohamed" and p == "123456":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("بيانات الدخول غير صحيحة")
    st.stop()

# ================== 4. تهيئة الذكاء الاصطناعي (Gemini) ==================
# ضع مفتاح الـ API الخاص بك هنا
API_KEY = "YOUR_API_KEY_HERE" 

if API_KEY != "YOUR_API_KEY_HERE":
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    model = None

# ================== 5. واجهة العمل الرئيسية ==================
st.title("🚀 Smart Analyst Beast")
st.write(f"مرحباً يا *محمد* | التوقيع المعتمد: *mai8444*")

tab1, tab2, tab3 = st.tabs(["📂 استيراد ودمج", "🧠 عقل الوحش", "📥 تصدير"])

# --- Tab 1: رفع ودمج الملفات ---
with tab1:
    files = st.file_uploader("ارفع ملفات Excel أو CSV", accept_multiple_files=True, type=['csv', 'xlsx'])
    if files:
        all_dfs = []
        for f in files:
            try:
                df = pd.read_excel(f) if f.name.endswith('xlsx') else pd.read_csv(f)
                all_dfs.append(df)
                st.toast(f"✅ تم تحميل: {f.name}")
            except Exception as e: st.error(f"خطأ في الملف: {e}")
        
        if all_dfs:
            st.session_state.master_df = pd.concat(all_dfs, ignore_index=True)
            st.success("تم دمج البيانات بنجاح!")
            st.dataframe(st.session_state.master_df.head(20), use_container_width=True)

# --- Tab 2: تحليل الذكاء الاصطناعي ---
with tab2:
    if "master_df" in st.session_state:
        if st.button("🧠 تشغيل التحليل الذكي"):
            if model:
                with st.spinner("الوحش يحلل البيانات لمحمد إسماعيل..."):
                    summary = st.session_state.master_df.describe().to_string()
                    prompt = f"حلل البيانات التالية وقدم تقريراً لمحمد إسماعيل (mai8444): {summary}"
                    response = model.generate_content(prompt)
                    st.session_state.ai_report = response.text
            else: st.error("⚠️ يرجى إضافة مفتاح API لتشغيل الذكاء الاصطناعي")
        
        if "ai_report" in st.session_state:
            st.markdown("---")
            st.markdown(st.session_state.ai_report)
            st.markdown(f"<p style='text-align: right;'><i>بواسطة: mai8444</i></p>", unsafe_allow_input=True)
    else: st.warning("يرجى رفع الملفات أولاً")

# --- Tab 3: تصدير النتائج ---
with tab3:
    if "master_df" in st.session_state:
        csv = st.session_state.master_df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ تحميل الملف الموحد (CSV)", data=csv, file_name="Beast_Data_mai8444.csv")
