import streamlit as st
import pandas as pd
import io
import urllib.parse

def run_module():
    st.markdown("### 📊 Excel Master Pro")
    st.write("System Architect: MIA8444")
    
    file = st.file_uploader("Upload Data", type=['csv', 'xlsx'])
    
    if file:
        df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
        st.dataframe(df.head(10))

        # تحويل البيانات لتنسيق إكسيل مرتب ومنسق
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='MIA8444_Report')
        
        processed_data = output.getvalue()

        st.download_button(
            label="📥 تحميل التقرير المنسق (Excel)",
            data=processed_data,
            file_name="MIA8444_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # زرار واتساب برمز الأيقونة الحقيقي
        msg = urllib.parse.quote("يا وحش! تقرير MIA8444 المنسق جاهز للمراجعة.")
        whatsapp_html = f"""
            <a href="https://wa.me/?text={msg}" target="_blank" style="text-decoration: none;">
                <div style="background-color: #25D366; color: white; padding: 10px 20px; border-radius: 25px; display: flex; align-items: center; width: fit-content; font-weight: bold; gap: 10px;">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" width="20px">
                    Share via WhatsApp
                </div>
            </a>
        """
        st.markdown(whatsapp_html, unsafe_allow_html=True)
