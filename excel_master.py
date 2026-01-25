import streamlit as st
import pandas as pd
import io

def run_module():
    st.markdown("### 📊 Excel Master - Pro Visual Analytics")
    st.write("Engineered by MIA8444 for High-Impact Reporting.")
    
    file = st.file_uploader("Upload Data", type=['csv', 'xlsx'])
    
    if file:
        df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
        st.success("Data Loaded Successfully!")
        
        # عرض البيانات قبل التنسيق
        st.dataframe(df.head(10))

        # عملية التنسيق الاحترافي
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='MIA8444_Analysis')
            
            workbook  = writer.book
            worksheet = writer.sheets['MIA8444_Analysis']

            # إضافة تنسيق هيدر (Header) شيك
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'vcenter',
                'fg_color': '#00C853', # اللون الأخضر بتاع الوحش
                'font_color': '#FFFFFF',
                'border': 1
            })

            # تطبيق التنسيق على العواميد وتوسيعها تلقائياً
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
                column_len = max(df[value].astype(str).len().max(), len(value)) + 2
                worksheet.set_column(col_num, col_num, column_len)

        processed_data = output.getvalue()

        # زرار التحميل الاحترافي
        st.download_button(
            label="📥 تحميل تقرير إكسيل منسق (Excel Pro)",
            data=processed_data,
            file_name="MIA8444_Final_Report.xlsx", # لاحظ الامتداد الجديد
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        # زرار الواتساب
        import urllib.parse
        msg = urllib.parse.quote("يا وحش! تقرير MIA8444 المنسق جاهز للمراجعة.")
        st.markdown(f'<a href="https://wa.me/?text={msg}" target="_blank">📲 مشاركة عبر واتساب</a>', unsafe_allow_html=True)
