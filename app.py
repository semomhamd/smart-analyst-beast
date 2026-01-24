import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime

# --- 1️⃣ إعدادات الصفحة ---
st.set_page_config(page_title="Smart Analyst Beast", layout="wide", page_icon="🐉")

# --- 2️⃣ بيانات الدخول Production (Environment Variables) ---
ADMIN_USER = os.getenv("SA_USER", "semomohamed")
ADMIN_PASS = os.getenv("SA_PASS", "123456")  # للـ MVP التجريبي فقط

# --- 3️⃣ اللوجو من GitHub ---
LOGO_URL = "https://raw.githubusercontent.com/username/repo/main/99afc3d2-b6ef-4eda-977f-2fdc4b6621dd.jpg"
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image(LOGO_URL, width=160)

# --- 4️⃣ نظام الدخول ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🐉 Smart Analyst")
    st.subheader("نظام التحليل المشفر – Production MVP")
    
    with st.form("login_form"):
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        submit = st.form_submit_button("دخول آمن")
        
        if submit:
            if user == ADMIN_USER and pw == ADMIN_PASS:
                st.session_state.logged_in = True
                st.success("تم تسجيل الدخول! 🚀")
                st.experimental_rerun()
            else:
                st.error("بيانات الدخول غير صحيحة")
    st.stop()

# --- 5️⃣ Smart Data Cleaner ---
def smart_analyst_cleaner(df):
    logs = []

    # حذف الأعمدة الفارغة
    initial_cols = df.shape[1]
    df = df.dropna(how='all', axis=1)
    if df.shape[1] < initial_cols:
        logs.append(f"🗑️ حذف {initial_cols - df.shape[1]} عمود فارغ.")

    # توحيد التواريخ تلقائيًا
    for col in df.columns:
        if 'date' in col.lower() or 'تاريخ' in col:
            original_sample = str(df[col].iloc[0]) if not df[col].empty else ""
            df[col] = pd.to_datetime(df[col], errors='coerce')
            logs.append(f"📅 توحيد التاريخ في '{col}' (مثال: {original_sample} -> ISO)")

    # تمييز القيم الشاذة بدون حذف
    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5*IQR
        upper = Q3 + 1.5*IQR
        outliers = ((df[col] < lower) | (df[col] > upper)).sum()
        if outliers > 0:
            logs.append(f"⚠️ اكتشاف {outliers} قيمة شاذة في '{col}'")

    return df, logs

# --- 6️⃣ Tabs / Main Interface ---
st.title("🚀 Smart Analyst Beast – Production MVP")
st.write(f"مرحباً بك يا صديقي | {datetime.now().strftime('%Y-%m-%d')}")

tab1, tab2 = st.tabs(["📂 رفع وإدارة البيانات", "📊 عقل الوحش (AI Explainer)"])

# --- Tab 1: رفع البيانات ---
with tab1:
    st.subheader("إدارة الملفات المتعددة")
    uploaded_files = st.file_uploader("ارفع ملفات Excel أو CSV", accept_multiple_files=True)

    if uploaded_files:
        all_dfs = []
        for file in uploaded_files:
            try:
                if file.name.endswith(('xlsx', 'xls')):
                    df = pd.read_excel(file)
                else:
                    df = pd.read_csv(file)
                
                df, logs = smart_analyst_cleaner(df)
                
                with st.expander(f"⚙️ معالجة: {file.name}"):
                    for log in logs:
                        st.info(log)
                    st.success("جاهز للدمج")
                
                all_dfs.append(df)
            except Exception as e:
                st.error(f"خطأ في {file.name}: {e}")

        if all_dfs:
            st.session_state.master_df = pd.concat(all_dfs, ignore_index=True)
            st.balloons()
            st.subheader("📋 قاعدة بيانات الوحش الموحدة")
            st.data_editor(st.session_state.master_df, use_container_width=True)

# --- Tab 2: AI Explainer ---
with tab2:
    st.subheader("عقل الوحش 🧠")
    if 'master_df' in st.session_state:
        st.write("البيانات جاهزة للتحليل… اضغط على الزر لتفعيل العقل")
        if st.button("شغل عقل الوحش 🧠"):
            st.info("🟢 Gemini AI Analyzer متصل – جاري التشغيل…")
            try:
                from openai import OpenAI  # أو Gemini SDK لو متاح
                client = OpenAI(api_key=os.getenv("GEN_API_KEY"))
                
                df = st.session_state.master_df
                num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                sample_analysis = []
                
                for col in num_cols:
                    mean_val = df[col].mean()
                    max_val = df[col].max()
                    min_val = df[col].min()
                    sample_analysis.append(f"📊 العمود '{col}': متوسط={mean_val:.2f}, أقصى={max_val}, أدنى={min_val}")
                
                prompt = f"""
                أنا محلل بيانات ذكي وصديق خبير. عندي تحليل للأعمدة الرقمية كالتالي:
                {chr(10).join(sample_analysis)}
                إشرح النتائج بطريقة بسيطة وودودة للمستخدم، مع نصائح عملية.
                """
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role":"user","content":prompt}],
                    temperature=0.7
                )
                
                st.success("✅ عقل الوحش أتم التحليل!")
                st.write(response.choices[0].message.content)
                
            except Exception as e:
                st.error(f"حصل خطأ في تشغيل AI: {e}")
    else:
        st.warning("من فضلك ارفع الملفات أولاً في التبويب الأول.")

# --- PDF Export (MVP Template) ---
if 'master_df' in st.session_state:
    if st.button("💾 تصدير PDF (MVP)"):
        st.info("جاري تجهيز التقرير… (في النسخة القادمة PDF حقيقي مع Logo)")

# --- Sidebar ---
st.sidebar.markdown("---")
st.sidebar.write("Powered by Gemini 1.5 | 2026")
st.sidebar.write("Developed by Smart Analyst")
