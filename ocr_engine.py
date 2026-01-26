import streamlit as st

def run_ocr_app():
    st.markdown("<h3 style='color:#D4AF37;'>📸 محرك استخراج النصوص (OCR)</h3>", unsafe_allow_html=True)
    st.info("ارفع صورة أو ملف PDF لاستخراج النصوص منها ذكياً")
    
    up_ocr = st.file_uploader("ارفع الصورة هنا", type=['png', 'jpg', 'jpeg', 'pdf'], key="ocr_uploader")
    
    if up_ocr:
        st.success("جاري معالجة الصورة... (هنا سنربط محرك الاستخراج قريباً)")
