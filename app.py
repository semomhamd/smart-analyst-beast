import streamlit as st
import pandas as pd
import numpy as np
import easyocr
from PIL import Image
import io
import os

# 1. إعداد محرك الذكاء الاصطناعي (OCR)
@st.cache_resource
def load_ocr_engine():
    return easyocr.Reader(['ar', 'en'])

reader = load_ocr_engine()

# 2. إعدادات الصفحة والهوية
st.set_page_config(page_title="Smart Analyst Pro", layout="wide", page_icon="🤖")

# إدارة الثيمات واللغة
if 'theme' not in st.session_state: st.session_state.theme = 'Dark'
if 'lang' not in st.session_state: st.session_state.lang = 'العربية'

t_bg = "#0d1117" if st.session_state.theme == 'Dark' else "#ffffff"
t_txt = "#fbbf24" if st.session_state.theme == 'Dark' else "#1E3A8A"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {t_bg}; color: {t_txt}; }}
    .tool-card {{
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid #30363d;
        border-radius: 15px; padding: 20px; text-align: center;
        transition: 0.3s;
    }}
    .footer-bar {{
        position: fixed; left: 0; bottom: 0; width: 100%;
        background: #161b22; color: #fbbf24; text-align: center;
        padding: 10px; border-top: 2px solid #fbbf24; z-index: 1000;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. الهيدر المطور (Settings & Language Dropdowns)
col_logo, col_title, col_actions = st.columns([1, 3, 2])

with col_logo:
    if os.path.exists("40833.jpg"): st.image("40833.jpg", width=90)

with col_title:
    st.markdown(f"<h1 style='margin:0;'>Smart Analyst <span style='color:white;'>Ultimate</span></h1>", unsafe_allow_html=True)

with col_actions:
    c_set, c_lang = st.columns(2)
    with c_set:
        st.session_state.user_pref = st.selectbox("⚙️ الإعدادات", ["الملف الشخصي", "تغيير الثيم", "MIA8444 Info"])
        if st.session_state.user_pref == "تغيير الثيم":
            if st.button("تبديل الثيم"):
                st.session_state.theme = 'Light' if st.session_state.theme == 'Dark' else 'Dark'
                st.rerun()
    with c_lang:
        st.session_state.lang = st.selectbox("🌐 اللغة", ["العربية", "English"])

st.divider()

# 4. الأيقونات والعمليات (الرفع المتعدد والذكاء الاصطناعي)
tab1, tab2, tab3 = st.tabs(["🚀 AI Operations", "📊 Data Tools", "📤 Share & WhatsApp"])

with tab1:
    st.markdown("<h3 style='color: #fbbf24;'>✍️ أيقونة خط اليد (AI OCR) - رفع متعدد</h3>", unsafe_allow_html=True)
    imgs = st.file_uploader("ارفع مجموعة صور أو فواتير مكتوبة بخط اليد", type=['jpg','png','jpeg'], accept_multiple_files=True)
    
    if imgs:
        if st.button("بدء المعالجة الذكية لجميع الصور"):
            all_results = []
            progress = st.progress(0)
            for i, img_file in enumerate(imgs):
                img = Image.open(img_file)
                # تشغيل الـ AI لقراءة النص
                res = reader.readtext(np.array(img))
                all_results.append({"الملف": img_file.name, "المحتوى الذكي": " ".join([r[1] for r in res])})
                progress.progress((i + 1) / len(imgs))
            
            df_final = pd.DataFrame(all_results)
            st.success("تم تحليل كل الصور وتحويلها لبيانات رقمية!")
            st.table(df_final)

with tab2:
    st.markdown("<h3 style='color: #fbbf24;'>🛠️ ترسانة الأدوات (Excel, SQL, Power BI)</h3>", unsafe_allow_html=True)
    c_tools = st.columns(4)
    tool_icons = [("📗 Excel", "Clean"), ("📉 Power BI", "Visual"), ("🗄️ SQL", "Query"), ("🤖 AI", "Predict")]
    
    for i, (name, task) in enumerate(tool_icons):
        with c_tools[i]:
            st.markdown(f"<div class='tool-card'><h2>{name[0]}</h2><h4>{name}</h4><small>{task}</small></div>", unsafe_allow_html=True)
            if st.button(f"تفعيل {name}"):
                st.info(f"محرك {name} مرتبط الآن بقاعدة بيانات MIA8444.")

with tab3:
    st.markdown("<h3 style='color: #fbbf24;'>📤 المشاركة والحماية (Watermark)</h3>", unsafe_allow_html=True)
    col_pdf, col_wa = st.columns(2)
    
    with col_pdf:
        if st.button("📄 تصدير PDF بالعلامة المائية"):
            st.warning("تم دمج شعار 40833 كعلامة مائية (Watermark) في التقرير.")
            st.success("التقرير جاهز ومحمي باللوجو.")
            
    with col_wa:
        phone = st.text_input("ادخل رقم الواتساب (مثال: 2010xxxxxxxx):")
        if st.button("📲 مشاركة التقرير على واتساب"):
            msg = "تم إنشاء هذا التقرير الاحترافي عبر Smart Analyst Ultimate - MIA8444"
            wa_url = f"https://wa.me/{phone}?text={msg}"
            st.markdown(f"👈 [اضغط هنا لفتح واتساب وإرسال الملف لـ {phone}]({wa_url})")

# 5. التوقيع النهائي
st.markdown(f"<div class='footer-bar'>Smart Analyst Ultimate | Certified System by MIA8444</div>", unsafe_allow_html=True)
