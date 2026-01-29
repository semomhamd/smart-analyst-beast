import streamlit as st
import pandas as pd
import os

# --- 1. الهوية الفخمة MIA8444 --- [cite: 2026-01-26]
st.set_page_config(page_title="Smart Analyst Beast PRO", layout="wide")

# الذاكرة المركزية [cite: 2026-01-16]
if 'main_data' not in st.session_state:
    st.session_state['main_data'] = None

# --- 2. السايد بار (مركز التحكم) ---
with st.sidebar:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_container_width=True)
    st.markdown("---")
    choice = st.sidebar.selectbox("الترسانة التقنية:", [
        "🏠 Smart Analyst (Home)",
        "📄 إنشاء شيت يدوي (Excel-Style)",
        "📊 Excel Master (Calculations)",
        "🧠 AI Brain Scientist (Analysis)"
    ])
    st.write("---")
    st.caption("Signature: *MIA8444*")

# --- 3. تشغيل الأدوات ---

# صفحة البداية
if choice == "🏠 Smart Analyst (Home)":
    st.markdown("<h1 style='text-align: center; color: #D4AF37;'>Smart Analyst</h1>", unsafe_allow_html=True)
    uploaded = st.file_uploader("ارفع ملف الإكسيل هنا", type=['xlsx', 'csv'])
    if uploaded:
        df = pd.read_excel(uploaded) if uploaded.name.endswith('xlsx') else pd.read_csv(uploaded)
        st.session_state['main_data'] = df
        st.success("تم شحن البيانات! 🔥")

# صفحة الشيت اليدوي (زي الإكسيل بالظبط)
elif choice == "📄 إنشاء شيت يدوي (Excel-Style)":
    st.title("📄 محرك الشيتات اليدوية")
    st.info("اكتب، عدل، وزود صفوف براحتك زي الإكسيل.")
    
    # لو مفيش بيانات، نفتح شيت فاضي
    if st.session_state['main_data'] is None:
        df_to_edit = pd.DataFrame([['', '', '']], columns=['A', 'B', 'C'])
    else:
        df_to_edit = st.session_state['main_data']

    # أداة التعديل المباشر
    edited_df = st.data_editor(df_to_edit, num_rows="dynamic", use_container_width=True)
    
    if st.button("💾 حفظ التعديلات اليدوية"):
        st.session_state['main_data'] = edited_df
        st.success("تم الحفظ في ذاكرة الوحش! MIA8444")

# صفحة الإكسيل (SUM & AVG) [cite: 2025-11-13]
elif choice == "📊 Excel Master (Calculations)":
    st.title("📊 محرك الحسابات (Excel Master)")
    if st.session_state['main_data'] is not None:
        df = st.session_state['main_data']
        num_cols = df.select_dtypes(include=['number']).columns.tolist()
        if num_cols:
            target = st.selectbox("اختار العمود للحساب:", num_cols)
            col1, col2 = st.columns(2)
            with col1: st.metric("المجموع (SUM)", f"{df[target].sum():,.2f}")
            with col2: st.metric("المتوسط (AVG)", f"{df[target].mean():,.2f}")
        else:
            st.warning("⚠️ مفيش أعمدة أرقام في الشيت ده!")
    else:
        st.error("⚠️ الذاكرة فاضية! ارفع ملف أو افتح شيت يدوي.")

# صفحة الذكاء الاصطناعي (AI Analysis) [cite: 2026-01-25]
elif choice == "🧠 AI Brain Scientist (Analysis)":
    st.title("🧠 مخ الذكاء الاصطناعي")
    if st.session_state['main_data'] is not None:
        df = st.session_state['main_data']
        if st.button("ابدأ التحليل العميق"):
            st.write("### 📜 تقرير MIA8444 الذكي:")
            st.write(f"1. عندك *{len(df)}* صف من البيانات.")
            st.info(f"2. أكبر قيمة موجودة في الجدول هي: *{df.max().max()}*")
            st.balloons()
    else:
        st.error("⚠️ ارفع بيانات الأول عشان الوحش يحللها!")
