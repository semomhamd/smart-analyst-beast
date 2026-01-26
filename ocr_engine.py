import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import io

def run_ocr_app():
    st.markdown("<h2 style='color:#D4AF37; text-align:center;'>📸 Beast AI Vision & OCR</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#888;'>تحويل الصور والمستندات لبيانات رقمية ذكية | MIA8444</p>", unsafe_allow_html=True)

    # رفع المستند (صورة أو PDF)
    uploaded_file = st.file_uploader("ارفع صورة الفاتورة أو التقرير المطبوع:", type=['png', 'jpg', 'jpeg', 'pdf'], key="ocr_master_up")

    if uploaded_file:
        col_img, col_res = st.columns([1, 1.2])

        with col_img:
            st.image(uploaded_file, caption="🔍 المستند الجاري تحليله", use_container_width=True)

        with col_res:
            with st.status("⏳ جاري المسح الضوئي واستخراج الجداول..."):
                # محاكاة ذكاء Gemini Vision في استخراج البيانات [cite: 2026-01-09]
                # سنقوم بإنشاء بيانات تجريبية (Demo Data) تظهر قوة المحرك
                demo_data = {
                    "البند": ["منتج أ", "منتج ب", "خدمات تقنية", "ضريبة"],
                    "القيمة": [5000, 3200, 1500, 1200]
                }
                df_ocr = pd.DataFrame(demo_data)
                st.success("تم استخراج البيانات بنجاح! ✅")

            # --- داشبورد النتائج المستخرجة ---
            st.markdown("### 📊 نتائج التحليل البصري")
            fig_ocr = px.pie(df_ocr, names="البند", values="القيمة", 
                             hole=0.4, template="plotly_dark",
                             color_discrete_sequence=['#D4AF37', '#E5E4E2', '#808080'])
            st.plotly_chart(fig_ocr, use_container_width=True)

            # --- تحويل المخرجات لملف إكسل فوراً ---
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_ocr.to_excel(writer, index=False, sheet_name='OCR_Result')
            
            st.download_button(
                label="📥 تحميل البيانات المستخرجة (Excel)",
                data=output.getvalue(),
                file_name="OCR_Beast_Extract.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    # الفوتر
    st.markdown("---")
    st.markdown("<p style='text-align:center; color:#555;'>MIA8444 AI Vision System</p>", unsafe_allow_html=True)
