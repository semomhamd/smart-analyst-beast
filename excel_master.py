import streamlit as st
import pandas as pd

def run_excel_app():
    st.markdown("<h3 style='color:#D4AF37;'>📊 محلل البيانات الذكي (Excel)</h3>", unsafe_allow_html=True)
    
    # رفع الملف
    uploaded_file = st.file_uploader("ارفع ملف الإكسل هنا يا بطل", type=['xlsx', 'csv'], key="excel_tool_uploader")
    
    if uploaded_file:
        try:
            # قراءة الملف
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success("تم رفع الملف بنجاح! ✅")
            
            # عرض البيانات في جدول
            st.write("---")
            st.markdown("#### 📋 معاينة البيانات")
            st.dataframe(df)
            
        except Exception as e:
            st.error(f"حصلت مشكلة وأنا بقرأ الملف: {e}")
