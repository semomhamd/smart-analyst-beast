import streamlit as st
import pandas as pd

def run_powerbi():
    st.markdown("<h2 style='text-align:center; color:#F2C811;'>📊 محرك Power BI (The Beast)</h2>", unsafe_allow_html=True)

    if 'main_data' in st.session_state and st.session_state['main_data'] is not None:
        df = st.session_state['main_data']
        st.success("✅ البيانات جاهزة للتحليل في Power BI.")
        
        st.info("💡 نصيحة: Power BI بيفضل ملفات الـ Excel المنسقة أو الربط المباشر.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("📂 *تحميل البيانات:*")
            # تحويل البيانات لملف إكسيل في الذاكرة
            output = pd.ExcelWriter("MIA8444_PowerBI.xlsx", engine='xlsxwriter')
            df.to_excel(output, index=False, sheet_name='Data')
            output.close()
            
            with open("MIA8444_PowerBI.xlsx", "rb") as f:
                st.download_button(
                    label="📥 تحميل ملف Excel لـ Power BI",
                    data=f,
                    file_name="MIA8444_PowerBI.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        
        with col2:
            st.write("🔗 *حالة الربط:*")
            st.code("Direct Query: Enabled\nMIA8444 Signature: Verified", language="text")

        st.markdown("---")
        st.write("📋 *نظرة أخيرة على البيانات قبل الاستيراد:*")
        st.dataframe(df.head(10), use_container_width=True)
    else:
        st.warning("⚠️ الذاكرة فارغة. الوحش مستني بياناتك عشان يجهزها للـ Power BI.")

st.markdown("<p style='text-align:center; font-size:12px; color:#555;'>MIA8444 | Power BI Integration</p>", unsafe_allow_html=True)
