import streamlit as st
import pandas as pd
import numpy as np
import os
import google.generativeai as genai
from datetime import datetime
import io

# ================== 1. إعدادات الثيم والجماليات ==================
st.set_page_config(page_title="Smart Analyst Beast", page_icon="🐉", layout="wide")

# نظام تبديل الدارك واللايت مود في الإعدادات
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

theme_css = {
    'dark': {"bg": "#0E1117", "text": "white", "card": "#1E1E1E", "btn": "#00C853"},
    'light': {"bg": "#F0F2F6", "text": "black", "card": "white", "btn": "#00A36C"}
}

curr = theme_css[st.session_state.theme]

st.markdown(f"""
    <style>
    .stApp {{ background-color: {curr['bg']}; color: {curr['text']}; }}
    [data-testid="stSidebar"] {{ background-color: {curr['card']} !important; }}
    .stButton>button {{ background-color: {curr['btn']}; color: white; border-radius: 10px; font-weight: bold; border: none; height: 3em; }}
    .stExpander {{ background-color: {curr['card']}; border-radius: 10px; border: 1px solid #333; }}
    </style>
    """, unsafe_allow_input=True)

# ================== 2. القائمة الجانبية (الإعدادات واللغة) ==================
with st.sidebar:
    # تعديل اللوجو ليكون أيقونة وحش جذابة
    st.markdown("<h1 style='text-align: center;'>🐲</h1>", unsafe_allow_input=True)
    st.title("Settings | الإعدادات")
    
    # اختيار اللغة والثيم
    lang = st.radio("🌍 اختر اللغة / Language", ["العربية", "English"], horizontal=True)
    theme_choice = st.radio("🌗 وضع الشاشة / Mode", ["Dark", "Light"], horizontal=True)
    st.session_state.theme = theme_choice.lower()
    
    st.markdown("---")
    st.write(f"👤 المستخدم: محمد")
    st.write(f"🚀 النسخة: 3.0.0 (Turbo)")
    if st.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()

# ================== 3. نظام الدخول ==================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🐉 Smart Analyst Beast")
    with st.container():
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        if st.button("دخول آمن"):
            if user == "semomohamed" and pw == "123456":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("خطأ في البيانات!")
    st.stop()

# ================== 4. تصليح تفعيل AI (Gemini) ==================
# تأكد من وضع مفتاح الـ API هنا أو في Secrets
# للحصول عليه: https://aistudio.google.com/app/apikey
API_KEY = "YOUR_API_KEY_HERE" 

if API_KEY != "YOUR_API_KEY_HERE":
    genai.configure(api_key=API_KEY)
    # استخدام فلاش للسرعة القصوى
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    model = None

# ================== 5. الواجهة الرئيسية (التطوير الجديد) ==================
st.title("🚀 Smart Analyst Beast")
st.caption("AI-Powered Data Intelligence Suite")

tab1, tab2, tab3 = st.tabs(["📂 استيراد ودمج", "🧠 عقل الوحش", "📥 تصدير"])

# --- Tab 1: الاستيراد والدمج ---
with tab1:
    st.subheader("📥 استيراد ملفات Excel/CSV")
    files = st.file_uploader("ارفع ملفاتك هنا", accept_multiple_files=True, type=['csv', 'xlsx'])
    
    if files:
        all_dfs = []
        for f in files:
            try:
                df = pd.read_excel(f) if f.name.endswith('xlsx') else pd.read_csv(f)
                # تنظيف سريع
                df = df.dropna(how='all', axis=1)
                all_dfs.append(df)
                st.toast(f"✅ تم تحميل {f.name}")
            except Exception as e:
                st.error(f"خطأ في {f.name}: {e}")
        
        if all_dfs:
            st.session_state.master_df = pd.concat(all_dfs, ignore_index=True)
            st.success("🔥 تم دمج البيانات وتجهيز الوحش!")
            st.dataframe(st.session_state.master_df.head(50), use_container_width=True)

# --- Tab 2: عقل الوحش (AI) - تصليح كامل ---
with tab2:
    if "master_df" in st.session_state:
        st.subheader("🤖 تحليل الذكاء الاصطناعي")
        if st.button("🧠 ابدأ استنتاج عقل الوحش"):
            if model:
                with st.spinner("الوحش يقوم بقراءة الأرقام الآن..."):
                    try:
                        # نرسل ملخص البيانات للـ AI (Head + Info)
                        buffer = io.StringIO()
                        st.session_state.master_df.info(buf=buffer)
                        info_str = buffer.getvalue()
                        
                        prompt = f"""
                        أنت خبير مالي ومحلل بيانات محترف. حلل هذه البيانات:
                        - هيكل البيانات: {info_str}
                        - ملخص إحصائي: {st.session_state.master_df.describe().to_string()}
                        
                        المطلوب بالعربية:
                        1. ملخص سريع للوضع الحالي.
                        2. 3 ملاحظات جوهرية.
                        3. توصية واحدة لزيادة الأرباح أو الكفاءة.
                        """
                        response = model.generate_content(prompt)
                        st.session_state.ai_report = response.text
                        st.success("✅ اكتمل التحليل!")
                    except Exception as e:
                        st.error(f"حدث خطأ أثناء التحليل: {e}")
            else:
                st.error("⚠️ خطأ: مفتاح الـ API غير مضبوط (API_KEY missing)")

        if "ai_report" in st.session_state:
            st.markdown("---")
            st.markdown(st.session_state.ai_report)
    else:
        st.warning("ارفع البيانات أولاً في التبويب الأول")

# --- Tab 3: التصدير ---
with tab3:
    if "master_df" in st.session_state:
        st.subheader("📥 تصدير الملف النهائي")
        
        # تصدير كـ CSV
        csv = st.session_state.master_df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ تحميل الملف الموحد (CSV)", data=csv, file_name="Beast_Data.csv")
        
        # تصدير كـ Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            st.session_state.master_df.to_excel(writer, index=False)
        st.download_button("⬇️ تحميل الملف الموحد (Excel)", data=output.getvalue(), file_name="Beast_Data.xlsx")
    else:
        st.info("لا توجد بيانات لتصديرها")

# --- تذييل الصفحة ---
st.markdown("---")
st.markdown("<p style='text-align: center;'>Powered by Gemini AI | Designed for Mohamed 🐲</p>", unsafe_allow_input=True)
