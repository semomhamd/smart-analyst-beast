import streamlit as st
import os
import importlib

# 1. إعدادات الصفحة والدارك مود (النسخة الفخمة MIA8444)
st.set_page_config(page_title="Smart Analyst The Beast", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    div.stButton > button {
        background-color: #D4AF37 !important; color: #000 !important;
        font-weight: bold; border-radius: 10px; width: 100%; height: 50px;
    }
    .header-style { text-align: center; color: #D4AF37; }
    </style>
""", unsafe_allow_html=True)

# 2. الهيدر واللوجو MIA8444
st.markdown("<div style='text-align:center; color:#888;'>Settings | Dark Mode | MIA8444</div>", unsafe_allow_html=True)

col_l1, col_l2, col_l3 = st.columns([1, 0.4, 1])
with col_l2:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_container_width=True)

st.markdown("<h1 class='header-style'>Smart Analyst The Beast</h1>", unsafe_allow_html=True)

# 3. أزرار الأدوات الثمانية (ربط حقيقي بالملفات)
tools = ["OCR", "Excel", "Google Sheets", "Power BI", "SQL", "Cleaner Pro", "Python", "Tableau"]
cols = st.columns(len(tools))

if 'active_tool' not in st.session_state:
    st.session_state['active_tool'] = "Excel"

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
    current = st.session_state['active_tool']
    st.markdown(f"<h4 style='color:#D4AF37;'>📂 أداة: {current}</h4>", unsafe_allow_html=True)
    
    try:
        # نظام الربط الديناميكي بناءً على أسماء ملفاتك في الصور
        if current == "Excel":
            import excel_master
            importlib.reload(excel_master)
            excel_master.run_excel_app()
        elif current == "OCR":
            import ocr_engine
            importlib.reload(ocr_engine)
            ocr_engine.run_ocr_app()
        elif current == "Cleaner Pro":
            import cleaner_pro
            importlib.reload(cleaner_pro)
            # افترضنا اسم الدالة run_cleaner، لو مختلفة غيرها
            cleaner_pro.run_cleaner() 
        elif current == "SQL":
            import sql_beast
            importlib.reload(sql_beast)
            sql_beast.run_sql_app()
        else:
            # مساحة رفع الملفات العامة (تصحيح خطأ المسافات)
            st.markdown(f"* :ارفع ملف {current} للبدء :*")
            st.file_uploader("", type=['csv', 'xlsx', 'pdf', 'png', 'jpg'], key=f"up_{current}", accept_multiple_files=True)

    except Exception as e:
        # حل مشكلة الـ Backup والفاصلة الناقصة
        st.warning(f"جاري تشغيل محرك {current}...")
        st.file_uploader(f"ارفع ملف {current} يدوياً", type=['csv', 'xlsx', 'pdf', 'png', 'jpg'], key=f"bk_{current}", accept_multiple_files=True)

    # زر المسح (الجوكر) - يظهر دائماً
    if st.button("🗑️ مسح كل الملفات", key="main_reset"):
        st.rerun()

# 5. التوقيع النهائي
st.markdown("<br><p style='text-align:center; color:#555;'>MIA8444 Signature | Smart Analyst Beast</p>", unsafe_allow_html=True)
