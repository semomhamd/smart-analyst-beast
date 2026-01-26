import streamlit as st
import os

# 1. إعدادات الشاشة العريضة
st.set_page_config(page_title="Smart Analyst The Beast", layout="wide")

# 2. تصميم الواجهة (MIA8444 Elite UI)
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    
    /* شريط الأدوات العلوي (Data Tools Bar) */
    .tools-container {
        display: flex; justify-content: space-around;
        background-color: #111; padding: 15px;
        border: 1px solid #D4AF37; border-radius: 15px;
        margin-bottom: 25px;
    }
    
    /* تنسيق أزرار الأدوات الـ 7 */
    div.stButton > button {
        background-color: #D4AF37 !important;
        color: #000 !important;
        font-weight: 900 !important;
        border-radius: 8px;
        border: 1px solid #FFF;
        transition: 0.3s;
    }
    
    /* منطقة العمل (Workspace) */
    .workspace-box {
        border: 2px solid #333; padding: 20px;
        border-radius: 15px; background-color: #0a0a0a;
        min-height: 400px;
    }
    
    .footer-text {
        text-align: center; color: #444; font-size: 0.8em; margin-top: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. الهيدر والإعدادات (صغير وأنيق فوق)
col_h1, col_h2, col_h3 = st.columns([1, 2, 1])
with col_h1: st.caption("🌐 EN/AR | ⚙️ | 🌙")
with col_h2: st.markdown("<h2 style='color:#D4AF37; text-align:center; margin-top:-10px;'>Smart Analyst The Beast</h2>", unsafe_allow_html=True)
with col_h3: st.markdown("<p style='text-align:right; color:#D4AF37;'>👑 MIA8444</p>", unsafe_allow_html=True)

# 4. شريط أدوات تحليل البيانات (الترتيب اللي طلبته)
st.markdown("---")
cols = st.columns(7)
tools = [
    ("📸 OCR", "ocr_engine.py"),
    ("📊 Excel", "excel_master.py"),
    ("📉 Power BI", "power_bi_hub.py"),
    ("🗄️ SQL", "sql_connector.py"),
    ("🧹 Cleaner Pro", "cleaner_pro.py"),
    ("🐍 Python", "python_analytics.py"),
    ("🎨 Tableau", "tableau_view.py")
]

for i, (label, file) in enumerate(tools):
    with cols[i]:
        if st.button(label):
            st.session_state['current_tool'] = label
            st.session_state['target_file'] = file

st.markdown("---")

# 5. منطقة العمل (تقسيم الشاشة: Gemini + استدعاء الملفات)
col_work1, col_work2 = st.columns([1, 1])

with col_work1:
    st.markdown("<h4 style='color:#D4AF37;'>🤖 المحلل الذكي (Gemini AI)</h4>", unsafe_allow_html=True)
    with st.container():
        st.chat_input("اسأل Gemini عن بياناتك...")
        st.info("الوحش جاهز لتحليل أي نمط بيانات تطلبه")

with col_work2:
    current = st.session_state.get('current_tool', 'إستدعاء الملفات')
    st.markdown(f"<h4 style='color:#D4AF37;'>📂 {current}</h4>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(f"ارفع ملف الـ {current} هنا", type=['csv', 'xlsx', 'pdf', 'sql', 'txt'])
    if uploaded_file:
        st.success(f"تم استلام ملف {current} بنجاح! جاري المعالجة...")

# 6. التوقيع النهائي
st.markdown(f"<div class='footer-text'>Smart Analyst The Beast | Designed by <span style='color:#D4AF37;'>MIA8444</span></div>", unsafe_allow_html=True)
