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
    .header-style { text-align: center; color: #D4AF37; }
    </style>
""", unsafe_allow_html=True)

# 2. الهيدر واللوجو
st.markdown("<div style='text-align:center; color:#888;'>Settings | Dark Mode | MIA8444</div>", unsafe_allow_html=True)

col_l1, col_l2, col_l3 = st.columns([1, 0.4, 1])
with col_l2:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_container_width=True)

st.markdown("<h1 class='header-style'>Smart Analyst The Beast</h1>", unsafe_allow_html=True)

# 3. أزرار الأدوات الثمانية
cols = st.columns(8)
tools = ["OCR", "Excel", "Google Sheets", "Power BI", "SQL", "Cleaner Pro", "Python", "Tableau"]

for i, tool in enumerate(tools):
    with cols[i]:
        if st.button(tool, key=f"btn_{tool}"):
            st.session_state['active_tool'] = tool

# 4. منطقة العمل المزدوجة
st.markdown("---")
col_gem, col_tool = st.columns(2)

with col_gem:
    st.markdown("<h4 style='color:#D4AF37;'>🤖 (Gemini AI) المحلل الذكي</h4>", unsafe_allow_html=True)
    st.chat_input("...اسأل Gemini عن بياناتك")

with col_tool:
    current = st.session_state.get('active_tool', 'Excel')
    st.markdown(f"<h4 style='color:#D4AF37;'>📂 أداة: {current}</h4>", unsafe_allow_html=True)
    
    # محرك الربط الذكي
    try:
        if current == "Excel":
            import excel_master
            importlib.reload(excel_master)
            excel_master.run_excel_app()
        elif current == "OCR":
            import ocr_engine
            importlib.reload(ocr_engine)
            ocr_engine.run_ocr_app()
        elif current == "Google Sheets":
            import google_sheets_master
            importlib.reload(google_sheets_master)
            google_sheets_master.run_sheets_app()
        else:
            # هنا مساحة الرفع اللي كانت مختفية
            st.markdown(f"*ارفع ملف {current} للبدء:*")
            st.file_uploader("", type=['csv', 'xlsx', 'pdf'], key=f"up_{current}", accept_multiple_files=True)
            if st.button("🗑️ مسح كل الملفات"):
                st.rerun()
    except Exception:
        # لو الملف مش موجود، افتح خانة الرفع فوراً كـ Backup
        st.file_uploader(f"ارفع ملف {current} يدوياً (المحرك جاري تفعيله):", type=['csv', 'xlsx', 'pdf'], key=f"bk_{current}"accept_multiple_files=True)

# 5.التوقيع النهائي
st.markdown("<br><p style='text-align:center; color:#555;'>MIA8444 Signature | Smart Analyst Beast</p>", unsafe_allow_html=True)
