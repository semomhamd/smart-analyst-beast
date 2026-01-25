import streamlit as st
import pandas as pd

def run_module():
    st.markdown("### 🧹 Power Query - Data Cleaner")
    st.write("Engineered by MIA8444 for Data Integrity.")
    
    # تحميل ملف للتنظيف
    file = st.file_uploader("Upload Excel/CSV to Clean", type=['csv', 'xlsx'])
    
    if file:
        df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
        
        st.write("📊 *Original Data Preview:*")
        st.dataframe(df.head())
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✨ Remove Duplicates"):
                df = df.drop_duplicates()
                st.success("Duplicates Removed!")
        with col2:
            if st.button("🗑️ Drop Empty Rows"):
                df = df.dropna()
                st.success("Empty Rows Cleaned!")
        
        st.write("✅ *Cleaned Data:*")
        st.dataframe(df)
        
        # تحميل الملف النظيف
        st.download_button("Download Cleaned Data", df.to_csv(index=False), "cleaned_beast_data.csv")
