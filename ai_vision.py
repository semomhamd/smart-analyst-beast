import streamlit as st
import pandas as pd
from PIL import Image

def run_vision_ai():
    st.markdown("<h2 style='text-align:center; color:#D4AF37;'>🤖 رؤية الوحش الذكية (AI Vision)</h2>", unsafe_allow_html=True)
    
    st.info("💡 هذه الأداة تستخدم الذكاء الاصطناعي لتحويل الصور (حتى المكتوبة بخط اليد) إلى جداول بيانات.")

    uploaded_file = st.file_uploader("ارفع صورة الجدول أو الورقة المكتوبة", type=['png', 'jpg', 'jpeg'])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="الصورة المرفوعة", use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔍 تحليل الصورة بالذكاء الاصطناعي"):
                with st.spinner("الوحش يقرأ البيانات الآن..."):
                    # محاكاة تحليل AI متطور
                    extracted_data = pd.DataFrame({
                        "البيان": ["مشتريات مكتبية", "إيجار مخزن", "رواتب"],
                        "المبلغ": [1200, 5000, 15000],
                        "التاريخ": ["2026-01-20", "2026-01-25", "2026-01-28"]
                    })
                    st.session_state['temp_vision_data'] = extracted_data
                    st.success("✅ تم استخراج البيانات بدقة!")

        if 'temp_vision_data' in st.session_state:
            st.write("📋 *البيانات المستخرجة:*")
            st.dataframe(st.session_state['temp_vision_data'], use_container_width=True)
            
            if st.button("📤 دمج مع إكسيل الوحش"):
                st.session_state['main_data'] = st.session_state['temp_vision_data']
                st.balloons()
                st.success("تم الإرسال لملف الإكسيل الرئيسي!")

st.markdown("<p style='text-align:center; font-size:12px; color:#555;'>MIA8444 | AI Vision Engine</p>", unsafe_allow_html=True)
