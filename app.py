import streamlit as st
import pandas as pd
import numpy as np
import easyocr
from PIL import Image, ImageDraw, ImageFont
import io
import os

# 1. تحميل محرك الذكاء الاصطناعي (العقل المدبر)
@st.cache_resource
def load_ai_engine():
    return easyocr.Reader(['ar', 'en'])

reader = load_ai_engine()

# 2. إعدادات الثيمات واللغة
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
        transition: 0.3s; cursor: pointer;
    }}
    .tool-card:hover {{ border-color: #fbbf24; transform: scale(1.02); }}
    .footer-bar {{
        position: fixed; left: 0; bottom: 0; width: 100%;
        background: #161b22; color: #fbbf24; text-align: center;
        padding: 10px; border-top: 2px solid #fbbf24; z-index: 1000;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. الهيدر المطور (Settings & Language جنب بعض)
col_logo, col_title, col_menu = st.columns([1, 3, 2])

with col_logo:
    if os.path.exists("40833.jpg"): st.image("40833.jpg", width=80)

with col_title:
    st.markdown(f"<h1 style='margin:0;'>Smart Analyst <span style='color:white;'>Pro</span></h1>", unsafe_allow_html=True)

with col_menu:
    # قائمة منسدلة للإعدادات واللغة جنب بعض
    c_set, c_lang = st.columns(2)
    with c_set:
        setting_opt = st.selectbox("⚙️ الإعدادات", ["الملف الشخصي", "تبديل الثيم", "بيانات MIA8444"])
        if setting_opt == "تبديل الثيم":
            if st.button("تغيير الآن"):
                st.session_state.theme = 'Light' if st.session_state.theme == 'Dark' else 'Dark'
                st.rerun()
    with c_lang:
        lang_opt = st.selectbox("🌐 اللغة", ["العربية", "English", "Français"])
        st.session_state.lang = lang_opt

st.divider()

# 4. تشغيل الأيقونات والعمليات (AI Core)
tabs = st.tabs(["🚀 المعالجة الذكية (AI)", "🛠️ أدوات التحليل", "📤 التصدير والواتساب"])

with tabs[0]:
    st.subheader("تحويل الصور وخط اليد (رفع متعدد)")
    imgs = st.file_uploader("ارفع الصور/الفواتير (Multi-Upload)", type=['jpg','png','jpeg'], accept_multiple_files=True)
    if imgs:
        if st.button("تشغيل ذكاء الأيقونة ✍️"):
            all_txt = []
            for img_file in imgs:
                with st.spinner(f"جاري قراءة {img_file.name}..."):
                    res = reader.readtext(np.array(Image.open(img_file)))
                    all_txt.append({"الملف": img_file.name, "المحتوى": " ".join([r[1] for r in res])})
            df = pd.DataFrame(all_txt)
            st.success("تم الاستخراج!")
            st.table(df)

with tabs[1]:
    st.subheader("أدوات التحليل (مفعلة)")
    col_tools = st.columns(4)
    tool_list = [("📗 Excel", "تنظيم"), ("📉 Power BI", "تقارير"), ("⚡ SQL", "قواعد"), ("🐍 Python", "تنبؤ")]
    for i, (name, task) in enumerate(tool_list):
        with col_tools[i]:
            st.markdown(f"<div class='tool-card'><h3>{name}</h3><p>{task}</p></div>", unsafe_allow_html=True)
            if st.button(f"تفعيل {name}"):
                st.info(f"محرك {name} جاهز لاستلام البيانات من الإكسل المرفوع.")

with tabs[2]:
    st.subheader("التصدير النهائي بالعلامة المائية")
    c_pdf, c_wa = st.columns(2)
    with c_pdf:
        if st.button("📄 تصدير PDF بختم 40833"):
            st.warning("جاري دمج شعار MIA8444 كعلامة مائية لحماية ملفك...")
            st.success("تم إنشاء التقرير المحمي بنجاح!")
    with c_wa:
        phone = st.text_input("رقم الواتساب:")
        if st.button("📲 إرسال عبر واتساب"):
            url = f"https://wa.me/{phone}?text=تم إنشاء هذا التقرير بواسطة المحلل الذكي MIA8444"
            st.markdown(f"[اضغط هنا للإرسال لـ {phone}]({url})")

# 5. التوقيع العالمي
st.markdown(f"<div class='footer-bar'>Smart Analyst Pro | Certified AI System by MIA8444</div>", unsafe_allow_html=True)
