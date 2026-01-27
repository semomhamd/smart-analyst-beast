import streamlit as st
import pandas as pd

def run_excel_app():
    # --- السطر السحري للربط ---
    if 'main_data' not in st.session_state:
        st.session_state['main_data'] = None

    st.markdown("### 📊 عمليات الإكسيل الذكية")

    # 1. لو فيه بيانات جاية من أداة تانية (OCR مثلاً) أو ارفعت هنا قبل كدة
    if st.session_state['main_data'] is not None:
        df = st.session_state['main_data']
        st.success("✅ البيانات محملة وجاهزة للعمليات!")
        
        # --- هنا تبدأ "العمليات" اللي إنت عايزها ---
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("عدد الصفوف", df.shape[0])
        with col2:
            st.metric("عدد الأعمدة", df.shape[1])
        with col3:
            if st.button("🔄 مسح الذاكرة"):
                st.session_state['main_data'] = None
                st.rerun()

        # إظهار العمليات الحسابية
        st.write("📋 *معاينة وتحليل سريع:*")
        st.dataframe(df)
        
        # عملية حسابية كمثال:
        if st.checkbox("إظهار الوصف الإحصائي (SUM/AVG)"):
            st.write(df.describe())

    else:
        # لو مفيش بيانات، يظهر زرار الرفع أو إنشاء شيت
        st.warning("الذاكرة فارغة، ارفع ملف أو ابدأ شيت جديد")
        uploaded_file = st.file_uploader("ارفع ملفك هنا", type=['xlsx', 'csv'])
        if uploaded_file:
            if uploaded_file.name.endswith('.csv'):
                st.session_state['main_data'] = pd.read_csv(uploaded_file)
            else:
                st.session_state['main_data'] = pd.read_excel(uploaded_file)
            st.rerun()
