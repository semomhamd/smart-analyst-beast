import streamlit as st
import pandas as pd

def run_module():
    st.markdown("### 🟢 Excel Master - Visual Analytics")
    st.write("Engineered by MIA8444 for High-Impact Reporting.")
    
    uploaded_file = st.file_uploader("Upload Data for Excel Enhancement", type=['csv', 'xlsx'])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        
        st.success("Data Loaded! Ready for Beast Visualization.")
        
        # خيارات التحليل البصري
        st.subheader("📊 Data Visualization")
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if numeric_cols:
            selected_col = st.selectbox("Select metric to visualize:", numeric_cols)
            st.bar_chart(df[selected_col])
        else:
            st.warning("No numeric data found for charting.")

        # تصدير الملف كـ Excel احترافي
        st.markdown("---")
        st.subheader("📥 Export Enhanced Report")
        if st.button("Generate Professional Excel"):
            st.info("The Beast is applying styles and formatting...")
          # زرار التحميل المطور لدعم اللغة العربية والواتساب
        data_to_download = df.to_csv(index=False).encode('utf-8-sig')
        
        st.download_button(
            label="📥 تحميل التقرير بالعربي (Excel)",
            data=data_to_download,
            file_name="MIA8444_Report.csv",
            mime="text/csv"
        )
        
        # إضافة زرار الواتساب (اختياري لو حابب)
        import urllib.parse
        msg = urllib.parse.quote("يا وحش! تقرير MIA8444 جاهز للمراجعة.")
        st.markdown(f'<a href="https://wa.me/?text={msg}" target="_blank">📲 مشاركة عبر واتساب</a>', unsafe_allow_html=True)
    st.caption("Excel Engine v1.0 | MIA8444 Ecosystem")
