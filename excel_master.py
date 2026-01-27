import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import urllib.parse

def export_to_pdf(df):
    # إنشاء ملف PDF في الذاكرة
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica", 12)
    
    p.drawString(100, 750, "Smart Analyst Beast - Report (MIA8444)")
    p.drawString(100, 735, "------------------------------------------")
    
    y = 700
    for index, row in df.head(20).iterrows(): # طباعة أول 20 صف كمثال
        line = " | ".join([str(item) for item in row.values])
        p.drawString(50, y, f"{index}: {line}")
        y -= 20
        if y < 50: # فتح صفحة جديدة لو الجدول طويل
            p.showPage()
            y = 750
            
    p.save()
    buffer.seek(0)
    return buffer

# --- داخل دالة run_excel_app تحت قسم الرسوم البيانية ---

st.markdown("---")
st.write("📤 *مشاركة النتائج (MIA8444):*")
col_pdf, col_wa = st.columns(2)

with col_pdf:
    # 1. زرار توليد وتحميل PDF
    pdf_file = export_to_pdf(st.session_state['main_data'])
    st.download_button(
        label="📄 تحميل الشيت كـ PDF",
        data=pdf_file,
        file_name="MIA8444_Beast_Report.pdf",
        mime="application/pdf"
    )

with col_wa:
    # 2. زرار المشاركة على الواتساب
    phone_number = st.text_input("رقم الواتساب (بالكود الدولي)", placeholder="2010xxxxxx")
    message = f"يا صديقي، إليك تقرير 'الوحش' المستخرج بواسطة تطبيق Smart Analyst. توقيع: MIA8444"
    
    # تجهيز اللينك
    if st.button("📱 مشاركة عبر واتساب"):
        if phone_number:
            encoded_msg = urllib.parse.quote(message)
            wa_url = f"https://wa.me/{phone_number}?text={encoded_msg}"
            st.markdown(f'<a href="{wa_url}" target="_blank">اضغط هنا لفتح الواتساب وإرسال التقرير ✅</a>', unsafe_allow_html=True)
        else:
            st.error("يرجى إدخال رقم الهاتف أولاً!")

# التوقيع النهائي
st.markdown("<p style='text-align:center; color:#555;'>MIA8444 Signature | Global Sharing Enabled</p>", unsafe_allow_html=True)
