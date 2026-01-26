import streamlit as st
import os
import webbrowser
from fpdf import FPDF

# 1. إعدادات الصفحة والدارك مود (الشكل الفخم اللي كان عندك)
st.set_page_config(page_title="Smart Analyst The Beast", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    div.stButton > button {
        background-color: #D4AF37 !important; color: #000 !important;
        font-weight: bold; border-radius: 10px; width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# 2. الهيدر واللوجو 8888.jpg
col_l1, col_l2, col_l3 = st.columns([1, 0.4, 1])
with col_l2:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_container_width=True)

st.markdown("<h1 style='color:#D4AF37; text-align:center;'>Smart Analyst The Beast</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Settings | Dark Mode | MIA8444</p>", unsafe_allow_html=True)

# 3. شريط الأدوات (الأزرار اللي بتنور)
st.markdown("<br>", unsafe_allow_html=True)
cols = st.columns(7)
tools = ["OCR", "Excel", "Power BI", "SQL", "Cleaner Pro", "Python", "Tableau"]
for i, tool in enumerate(tools):
    with cols[i]:
        if st.button(tool):
            st.session_state['active_tool'] = tool

# 4. منطقة العمل (Gemini + الأداة)
st.markdown("---")
col_gem, col_file = st.columns(2)

with col_gem:
    st.markdown("<h4 style='color:#D4AF37;'>🤖 (Gemini AI) المحلل الذكي</h4>", unsafe_allow_html=True)
    st.chat_input("اسأل Gemini عن بياناتك...")
    st.info("الوحش جاهز للتحليل الذكي (Anomaly Detection) 🚨")

with col_file:
    current = st.session_state.get('active_tool', 'Excel')
    st.markdown(f"<h4 style='color:#D4AF37;'>📂 أداة: {current}</h4>", unsafe_allow_html=True)
    
    # محرك الربط اللي شغلناه ونجح في الإكسل
    try:
        if current == "Excel":
            import excel_master
            excel_master.run_excel_app()
        elif current == "OCR":
            import ocr_engine
            ocr_engine.run_ocr_app()
        else:
            st.file_uploader(f"ارفع ملف {current}", type=['csv', 'xlsx', 'pdf'], key=f"up_{current}")
    except:
        st.warning(f"جاري ربط {current}...")

# 5. مركز المخرجات (الـ PDF والواتساب العام)
st.markdown("---")
st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📦 مركز المخرجات</h3>", unsafe_allow_html=True)
c_pdf, c_wa = st.columns(2)

with c_pdf:
    if st.button("📄 تحميل التقرير PDF"):
        pdf = FPDF()
        pdf.add_page(); pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Smart Analyst The Beast Report", ln=1, align='C')
        st.download_button("Download Now", pdf.output(dest='S').encode('latin-1'), "Report.pdf")

with c_wa:
    # هنا شلت رقمي وحطيت مكان يدخله المستخدم عشان الخصوصية [cite: 2026-01-07]
    target_phone = st.text_input("رقم الواتساب المستلم:", placeholder="2010XXXXXXXX")
    if st.button("🟢 إرسال للواتساب"):
        if target_phone:
            webbrowser.open(f"https://wa.me/{target_phone}?text=MIA8444_Analysis_Ready")
        else:
            st.warning("دخل الرقم الأول يا وحش")

st.markdown("<br><p style='text-align:center; color:#555;'>Smart Analyst The Beast | MIA8444</p>", unsafe_allow_html=True)
