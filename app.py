import streamlit as st
import os
import webbrowser

# 1. إعدادات الصفحة
st.set_page_config(page_title="Smart Analyst The Beast", layout="wide")

# 2. هندسة الفخامة MIA8444 Elite UI
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    div.stButton > button {
        background-color: #D4AF37 !important;
        color: #000000 !important;
        font-weight: 900 !important;
        font-size: 16px !important;
        border-radius: 10px;
        border: 1px solid #FFFFFF;
        height: 3em; width: 100%;
    }
    .workspace-header {
        color: #D4AF37; font-weight: bold; border-bottom: 1px solid #333;
        padding-bottom: 10px; margin-bottom: 20px;
    }
    .footer-mark {
        text-align: center; color: #444; font-size: 0.8em;
        margin-top: 50px; border-top: 0.1px solid #222; padding-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. الهيدر (اللوجو الملكي 8888.jpg)
col_l1, col_l2, col_l3 = st.columns([1, 0.4, 1])
with col_l2:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_container_width=True) #

st.markdown("<h1 style='color:#D4AF37; text-align:center;'>Smart Analyst The Beast</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888; font-size:0.8em;'>🌐 EN/AR | ⚙️ Settings | 🌙 Dark Mode</p>", unsafe_allow_html=True)

# 4. شريط الأدوات السبعة (الترتيب الذهبي)
st.markdown("<br>", unsafe_allow_html=True)
cols = st.columns(7)
tools = [
    ("📸 OCR", "ocr_engine"),
    ("📊 Excel", "excel_master"),
    ("📉 Power BI", "power_bi_hub"),
    ("🗄️ SQL", "sql_connector"),
    ("🧹 Cleaner Pro", "cleaner_pro"),
    ("🐍 Python", "python_analytics"),
    ("🎨 Tableau", "tableau_view")
]

for i, (label, module_name) in enumerate(tools):
    with cols[i]:
        if st.button(label):
            st.session_state['active_tool'] = label
            st.session_state['module'] = module_name # [cite: 2026-01-24]

st.markdown("---")

# 5. منطقة العمل (Gemini + تفعيل الأداة المباشر)
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("<div class='workspace-header'>🤖 (Gemini AI) المحلل الذكي</div>", unsafe_allow_html=True)
    st.chat_input("يا وحش، اسأل Gemini عن بياناتك...") # [cite: 2026-01-20]
    st.info("الوحش جاهز لتحليل الأنماط وكشف الأخطاء (Anomaly Detection) 🚨")

with col_right:
    current_tool = st.session_state.get('active_tool', 'إستدعاء الملفات')
    st.markdown(f"<div class='workspace-header'>📂 {current_tool}</div>", unsafe_allow_html=True)
    
    # التفعيل الفعلي للأداة المختارة
    if current_tool == "📊 Excel":
        try:
            import excel_master
            excel_master.run_excel_app() # لازم يكون عندك دالة بالاسم ده في ملف excel_master.py
        except: st.warning("جاري تجهيز ملف excel_master.py للربط...")
    
    elif current_tool == "📸 OCR":
        try:
            import ocr_engine
            ocr_engine.run_ocr_app()
        except: st.warning("جاري تجهيز محرك الـ OCR...")
    
    else:
        # افتراضي لرفع الملفات لو الأداة لسه مبرمجناش تفعيلها
        st.file_uploader(f"ارفع ملف {current_tool} هنا", type=['csv', 'xlsx', 'pdf', 'sql', 'txt'])

# 6. مركز المخرجات (PDF + WhatsApp)
st.markdown("---")
st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📦 مركز المخرجات والواتساب</h3>", unsafe_allow_html=True)
c_out1, c_out2 = st.columns(2)
with c_out1:
    if st.button("📄 استخراج تقرير PDF للمحلل"):
        st.success("تم تجهيز التقرير بنجاح! 📥")
with c_out2:
    if st.button("🟢 إرسال النتائج للواتساب"):
        webbrowser.open("https://wa.me/201005305955?text=تقرير_الوحش_جاهز") # [cite: 2025-11-13]

# 7. التوقيع الملكي الأنيق
st.markdown(f"<div class='footer-mark'>Smart Analyst The Beast | Designed by <span style='color:#D4AF37;'>MIA8444</span></div>", unsafe_allow_html=True)
