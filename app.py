import streamlit as st
import os
import webbrowser
from fpdf import FPDF # تأكد من إضافة fpdf في ملف requirements.txt

# 1. إعدادات الصفحة واللوجو
st.set_page_config(page_title="Smart Analyst The Beast", layout="wide")

# 2. الهيدر الملكي (إضافة اللوجو 8888.jpg)
col_logo1, col_logo2, col_logo3 = st.columns([1, 0.4, 1])
with col_logo2:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_container_width=True) #

st.markdown("<h1 style='color:#D4AF37; text-align:center;'>Smart Analyst The Beast</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888;'>EN/AR | Settings | Dark Mode</p>", unsafe_allow_html=True)

# 3. شريط الأدوات السبعة (التفعيل المباشر)
st.markdown("<br>", unsafe_allow_html=True)
cols = st.columns(7)
tools = ["OCR", "Excel", "Power BI", "SQL", "Cleaner Pro", "Python", "Tableau"]
for i, tool in enumerate(tools):
    with cols[i]:
        if st.button(f" {tool}"):
            st.session_state['active_tool'] = tool

# 4. منطقة العمل (Gemini + ملفات)
st.markdown("---")
with col_file:
current = st.session_state.get('active_tool', 'Excel')
    st.markdown(f"<div class='workspace-header'>📂 أداة: {current}</div>", unsafe_allow_html=True)
    
    # الربط الفعلي بين الزرار والملف
    if current == "Excel":
        try:
            import excel_master
            # استدعاء الدالة اللي برمجناها في الملف التاني
            excel_master.run_excel_app() 
        except Exception as e:
            st.info("جاري تجهيز محرك اكسل... ارفع ملفك هنا مؤقتاً")
            st.file_uploader("Upload File", type=['xlsx', 'csv'])
            
    elif current == "OCR":
        st.info("أداة الـ OCR جاري ربطها بنفس الطريقة...")
with col_gem:
    st.markdown("<h4 style='color:#D4AF37;'>🤖 (Gemini AI) المحلل الذكي</h4>", unsafe_allow_html=True)
    st.chat_input("اسأل Gemini عن بياناتك...")
    st.info("الوحش جاهز لتحليل الأنماط وكشف الأخطاء (Anomaly Detection) 🚨")

with col_file:
    tool_name = st.session_state.get('active_tool', 'إستدعاء الملفات')
    st.markdown(f"<h4 style='color:#D4AF37;'>📂 {tool_name}</h4>", unsafe_allow_html=True)
    uploaded = st.file_uploader(f"ارفع ملف {tool_name} هنا", type=['csv', 'xlsx', 'pdf', 'sql', 'txt'])

# 5. تفعيل PDF والواتساب (مركز المخرجات)
st.markdown("---")
st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📦 مركز المخرجات والواتساب</h3>", unsafe_allow_html=True)

col_pdf, col_wa = st.columns(2)

with col_pdf:
    if st.button("📄 تحميل التقرير النهائي PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Smart Analyst The Beast - Report", ln=1, align='C')
        pdf.cell(200, 10, txt=f"Analysis for: {tool_name}", ln=2, align='L')
        pdf_output = pdf.output(dest='S').encode('latin-1')
        st.download_button(label="Click to Download PDF", data=pdf_output, file_name="Beast_Report.pdf", mime="application/pdf")

with col_wa:
    phone = st.text_input("رقم الواتساب (بالكود الدولي)", value="201005305955")
    if st.button("🟢 إرسال النتائج للواتساب"):
        msg = f"تم تحليل بياناتك بنجاح بواسطة الوحش MIA8444 للأداة {tool_name}"
        webbrowser.open(f"https://wa.me/{phone}?text={msg}") #

# 6. التوقيع الأنيق (تحت خالص)
st.markdown(f"<div style='text-align:center; color:#444; margin-top:50px;'>Smart Analyst The Beast | Designed by <span style='color:#D4AF37;'>MIA8444</span></div>", unsafe_allow_html=True)
