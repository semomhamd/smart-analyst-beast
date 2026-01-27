import streamlit as st
import pandas as pd
from PIL import Image

def run_ocr_app():
    st.markdown("<h2 style='text-align:center; color:#D4AF37;'>👁️ استخراج البيانات من الصور (OCR)</h2>", unsafe_allow_html=True)
    
    uploaded = st.file_uploader("ارفع صور الفواتير أو الكشوفات", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
    
    if uploaded:
        for img_file in uploaded:
            st.image(Image.open(img_file), width=300)
            
        if st.button("🪄 استخراج وتحويل لجدول"):
            # محاكاة استخراج بيانات
            mock_data = pd.DataFrame({"التاريخ": ["2026-01-28"], "البيان": ["فاتورة تجريبية"], "المبلغ": [5000]})
            st.write("✅ البيانات المستخرجة:")
            st.table(mock_data)
            
            if st.button("📤 إرسال إلى إكسيل الوحش"):
                st.session_state['main_data'] = mock_data
                st.success("تم الإرسال! افتح أداة الإكسيل الآن.")

st.markdown("<p style='text-align:center; color:#555;'>MIA8444 | Vision Engine</p>", unsafe_allow_html=True)
