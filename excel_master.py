import streamlit as st
import pandas as pd
import plotly.express as px
import io

def run_excel_app():
    st.markdown("<h2 style='color:#D4AF37; text-align:center;'>🏆 Beast Analytics & Report Maker</h2>", unsafe_allow_html=True)
    
    # 1. رفع الملف
    file = st.file_uploader("ارفع ملف البيانات (Excel/CSV)", type=['xlsx', 'csv'], key="pro_master_up")
    
    if file:
        # قراءة البيانات
        df = pd.read_excel(file) if file.name.endswith('xlsx') else pd.read_csv(file)
        
        # 2. منطقة الداشبورد (الرسوم البيانية عالية المستوى)
        num_cols = df.select_dtypes(include=['number']).columns
        if len(num_cols) > 0:
            st.markdown("### 📊 لوحة المؤشرات الذكية")
            k1, k2, k3 = st.columns(3)
            with k1: st.metric("إجمالي القيمة", f"{df[num_cols[0]].sum():,.0f}")
            with k2: st.metric("المتوسط العام", f"{df[num_cols[0]].mean():,.1f}")
            with k3: st.metric("أقصى نمو", f"{df[num_cols[0]].max():,.0f}")
            
            # الرسم البياني التفاعلي
            fig = px.area(df, x=df.columns[0], y=num_cols[0], 
                          title="منحنى الأداء التحليلي", 
                          template="plotly_dark", color_discrete_sequence=['#D4AF37'])
            st.plotly_chart(fig, use_container_width=True)
            
            # 3. منطقة تصنيع ملف الإكسل (The Pro Export)
            st.markdown("---")
            st.markdown("### 🛠️ صناعة تقرير Excel احترافي")
            st.info("سيقوم الوحش بتنسيق الملف وإضافة شيت ملخص إحصائي تلقائياً")
            
            if st.button("🚀 توليد ملف إكسل MIA8444"):
                output = io.BytesIO()
                # استخدام XlsxWriter لتنسيق الملف بشكل احترافي
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df.to_excel(writer, sheet_name='Data_Cleaned', index=False)
                    # إضافة شيت للملخص
                    df.describe().to_excel(writer, sheet_name='Statistical_Summary')
                    
                    # إضافة لمسة جمالية للملف (تلوين العناوين ذهبي)
                    workbook  = writer.book
                    worksheet = writer.sheets['Data_Cleaned']
                    header_fmt = workbook.add_format({'bold': True, 'bg_color': '#D4AF37', 'border': 1})
                    for col_num, value in enumerate(df.columns.values):
                        worksheet.write(0, col_num, value, header_fmt)
                
                st.download_button(
                    label="📥 تحميل ملف الإكسل المطور",
                    data=output.getvalue(),
                    file_name="Beast_Professional_Report.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        
        # عرض الجدول للمعاينة
        with st.expander("🔍 معاينة البيانات المرفوعة"):
            st.dataframe(df.style.background_gradient(cmap='YlOrBr'), use_container_width=True)

# التوقيع
st.markdown("<p style='text-align:center; color:#555;'>MIA8444 Signature | Smart Analyst Beast</p>", unsafe_allow_html=True)
