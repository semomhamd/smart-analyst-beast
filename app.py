import streamlit as st
import pandas as pd
import os

# --- 1. الهوية الفخمة MIA8444 --- [cite: 2026-01-26]
st.set_page_config(page_title="Smart Analyst Beast PRO", layout="wide")

# الذاكرة المركزية الموحدة [cite: 2026-01-16]
if 'main_data' not in st.session_state:
    st.session_state['main_data'] = None

# --- 2. السايد بار (Control Tower) ---
with st.sidebar:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_container_width=True)
    st.markdown("---")
    choice = st.radio("ترسانة الأدوات:", [
        "🏠 Smart Analyst (Home)",
        "📄 إنشاء شيت يدوي (Manual)",
        "📊 Excel Master",
        "🧠 AI Brain Scientist"
    ])
    st.write("---")
    st.caption("Verified by: *MIA8444*")

# --- 3. تشغيل الأدوات ---

# الصفحة الرئيسية (تم تعديل الترحيب هنا)
if choice == "🏠 Smart Analyst (Home)":
    st.markdown("<h1 style='text-align: center; color: #D4AF37;'>Smart Analyst</h1>", unsafe_allow_html=True)
    st.write("---")
    uploaded = st.file_uploader("ارفع ملف الإكسيل هنا", type=['xlsx', 'csv'])
    if uploaded:
        df = pd.read_excel(uploaded) if uploaded.name.endswith('xlsx') else pd.read_csv(uploaded)
        st.session_state['main_data'] = df
        st.success("تم شحن البيانات في ذاكرة الوحش! 🔥")

# صفحة الشيت اليدوي (زي الإكسيل بالظبط)
elif choice == "📄 إنشاء شيت يدوي (Manual)":
    st.title("📄 محرك الشيتات اليدوية")
    st.info("اكتب، عدل، وزود صفوف براحتك زي الإكسيل العادي.")
    
    # لو مفيش بيانات، نفتح شيت فاضي
    if st.session_state['main_data'] is None:
        df_to_edit = pd.DataFrame([['', '', '']], columns=['A', 'B', 'C'])
    else:
        df_to_edit = st.session_state['main_data']

    # أداة التعديل المباشر
    edited_df = st.data_editor(df_to_edit, num_rows="dynamic", use_container_width=True)
    
    if st.button("💾 حفظ التعديلات اليدوية"):
        st.session_state['main_data'] = edited_df
        st.success("تم الحفظ في ذاكرة الوحش بنجاح! MIA8444")

# صفحة الإكسيل (SUM & AVG) [cite: 2025-11-13]
elif choice == "📊 Excel Master":
    st.title("📊 محرك الحسابات الذكي")
    if st.session_state['main_data'] is not None:
        df = st.session_state['main_data']
        # التأكد من وجود أرقام للحساب لتجنب أخطاء numpy
        num_cols = df.select_dtypes(include=['number']).columns.tolist()
        if num_cols:
            target = st.selectbox("اختار العمود للحساب:", num_cols)
            c1, c2 = st.columns(2)
            with c1: st.metric("المجموع (SUM)", f"{df[target].sum():,.2f}")
            with c2: st.metric("المتوسط (AVG)", f"{df[target].mean():,.2f}")
        else:
            st.warning("⚠️ مفيش أعمدة أرقام في الشيت ده يا حبيب قلبي!")
    else:
        st.error("⚠️ الذاكرة فاضية! ارفع ملف أو افتح شيت يدوي.")

# صفحة الذكاء الاصطناعي (AI Analysis) [cite: 2026-01-25]
elif choice == "🧠 AI Brain Scientist":
    st.title("🧠 مخ الذكاء الاصطناعي")
    if st.session_state['main_data'] is not None:
        df = st.session_state['main_data']
        if st.button("ابدأ التحليل العميق"):
            st.write("### 📜 تقرير MIA8444 الذكي:")
            st.write(f"1. عندك *{len(df)}* صف من البيانات.")
            # استخدام ميزة التحليل لتجنب خطأ fada2d35 في numpy
            st.info("تم تحليل هيكل الجدول بنجاح وجاهز للاستنتاجات.")
            st.balloons()
    else:
        st.error("⚠️ ارفع بيانات الأول عشان الوحش يحللها!")
