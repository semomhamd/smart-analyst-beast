import streamlit as st
import os
import webbrowser
import importlib

# 1. إعدادات الصفحة والدارك مود
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

# 2. الهيدر (الإعدادات واللوجو)
st.markdown("<div style='text-align:center; color:#888;'>EN/AR | ⚙️ Settings | 🌙 Dark Mode</div>", unsafe_allow_html=True)

col_l1, col_l2, col_l3 = st.columns([1, 0.4, 1])
with col_l2:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_container_width=True)

st.markdown("<h1 style='color:#D4AF37; text-align:center;'>Smart Analyst The Beast</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888;'>MIA8444 Signature</p>", unsafe_allow_html=True)

# 3. شريط الأدوات الثمانية
st.markdown("<br>", unsafe_allow_html=True)
cols = st.columns(8)
tools = ["OCR", "Excel", "Google Sheets", "Power BI", "SQL", "Cleaner Pro", "Python", "Tableau"]

for i, tool in enumerate(tools):
    with cols[i]:
        if st.button(tool, key=f"btn_{tool}"):
            st.session_state['active_tool'] = tool

# 4. منطقة العمل المترابطة (The Smart Linker)
st.markdown("---")
col_gem, col_tool = st.columns(2)

with col_gem:
    st.markdown("<h4 style='color:#D4AF37;'>🤖 (Gemini AI) المحلل الذكي</h4>")
    st.chat_input("اسأل Gemini عن بياناتك...")
    st.info("الوحش جاهز للتحليل الذكي وكشف الأنماط 🚨")

with col_tool:
    current = st.session_state.get('active_tool', 'Excel')
    st.markdown(f"<h4 style='color:#D4AF37;'>📂 أداة: {current}</h4>", unsafe_allow_html=True)
    
    try:
        if current == "Excel":
            import excel_master
            importlib.reload(excel_master)
            excel_master.run_excel_app()
        elif current == "Google Sheets":
            import google_sheets_master
            importlib.reload(google_sheets_master)
            google_sheets_master.run_sheets_app()
        elif current == "OCR":
            import ocr_engine
            importlib.reload(ocr_engine)
            ocr_engine.run_ocr_app()
        else:
            st.info(f"جاري برمجة محرك {current} الاحترافي...")
    except Exception as e:
        st.warning(f"تأكد من وجود ملف {current.lower().replace(' ', '_')}_master.py")

# 5. مركز المخرجات والواتساب والـ PDF
st.markdown("---")
st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📦 مركز المخرجات</h3>", unsafe_allow_html=True)
c_pdf, c_wa = st.columns(2)

with c_pdf:
    if st.button("📄 تحميل التقرير PDF"):
        st.write("تم تجهيز التقرير بنجاح!")

with c_wa:
    phone = st.text_input("رقم الواتساب المستلم:", placeholder="2010XXXXXXXX")
    if st.button("🟢 إرسال للواتساب"):
        if phone:
            webbrowser.open(f"https://wa.me/{phone}?text=MIA8444_Analysis_Ready")

st.markdown("<br><p style='text-align:center; color:#444;'>Smart Analyst The Beast | MIA8444</p>", unsafe_allow_html=True)
