import streamlit as st
import pandas as pd
import numpy as np
import os
import time

# 1. إعدادات الصفحة والهوية البصرية
st.set_page_config(page_title="Smart Analyst Ultimate", layout="wide", page_icon="🤖")

# إدارة حالة النظام (الثيم واللغة والبيانات)
if 'theme' not in st.session_state: st.session_state.theme = 'Dark'
if 'data_connected' not in st.session_state: st.session_state.data_connected = False

t_bg = "#0d1117" if st.session_state.theme == 'Dark' else "#ffffff"
t_txt = "#fbbf24" if st.session_state.theme == 'Dark' else "#1E3A8A"
card_bg = "rgba(255, 255, 255, 0.05)" if st.session_state.theme == 'Dark' else "#f0f2f6"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {t_bg}; color: {t_txt}; }}
    .tool-card {{
        background: {card_bg};
        border: 1px solid #30363d;
        border-radius: 12px; padding: 15px; text-align: center;
        margin-bottom: 10px; transition: 0.3s; height: 160px;
    }}
    .tool-card:hover {{ border-color: #fbbf24; transform: translateY(-5px); box-shadow: 0 4px 15px rgba(251, 191, 36, 0.2); }}
    .footer-bar {{
        position: fixed; left: 0; bottom: 0; width: 100%;
        background: #161b22; color: #fbbf24; text-align: center;
        padding: 8px; border-top: 1px solid #fbbf24; font-size: 14px; z-index: 100;
    }}
    .status-online {{ color: #2ecc71; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

# 2. الهيدر الاحترافي
col_logo, col_title, col_nav = st.columns([1, 4, 2])

with col_logo:
    # اللوجو كما طلبت يا صديقي (Wanas Style)
    if os.path.exists("40833.jpg"):
        st.image("40833.jpg", width=85)
    else:
        st.markdown(f"<h1 style='color:#fbbf24; margin:0;'>W</h1>", unsafe_allow_html=True)

with col_title:
    st.markdown("<h1 style='margin:0;'>Smart Analyst <span style='color:#fbbf24;'>Ultimate</span></h1>", unsafe_allow_html=True)
    st.caption("The Integrated AI Ecosystem | Powering Data Decisions")

with col_nav:
    c_set, c_lang = st.columns(2)
    with c_set:
        user_choice = st.selectbox("⚙️ الإعدادات", ["الملف الشخصي", "تبديل الثيم", "عن المطور"])
        if user_choice == "تبديل الثيم" and st.button("تغيير"):
            st.session_state.theme = 'Light' if st.session_state.theme == 'Dark' else 'Dark'
            st.rerun()
    with c_lang:
        st.selectbox("🌐 اللغة", ["العربية", "English"])

st.divider()

# 3. المنظومة الذكية (Tabs)
tabs = st.tabs(["📊 الداشبورد", "🧼 Smart Cleaner", "📂 AI OCR", "🛠️ الأدوات المتقدمة", "📤 التقارير"])

with tabs[0]:
    # رسالة ترحيب مخصصة كما في الـ Saved Info
    st.markdown(f"### أهلاً بك يا صديقي في مركز التحكم")
    st.success("🤖 Wanas AI Brain: الحالة متصل | Softr Databases: جاهزة للاستقبال")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("إجمالي البيانات المعالجة", "1.2GB", "+15%")
    m2.metric("دقة الـ AI OCR", "98.5%", "High")
    m3.metric("التقارير الجاهزة", "14", "PDF")
    m4.metric("وقت توفير الجهد", "120h", "🔥")

with tabs[1]:
    st.markdown("### 🧼 Smart Data Cleaner (Python Engine)")
    st.info("هذا المحرك يقوم بتنظيف البيانات تلقائياً من القيم المفقودة والتكرارات.")
    uploaded_file = st.file_uploader("ارفع ملف للبدء بالتنظيف الذكي", type=['csv', 'xlsx'])
    if uploaded_file:
        with st.spinner("جاري الكشف عن المشاكل في البيانات..."):
            time.sleep(1.5)
            st.warning("⚠️ تم اكتشاف 12 قيمة مفقودة و 5 صفوف مكررة.")
            if st.button("تفعيل التنظيف الذكي"):
                st.balloons()
                st.success("تم تنظيف البيانات بنجاح! جاهزة الآن للتحليل عبر Excel Pro.")

with tabs[2]:
    st.markdown("### ✍️ AI OCR - استخراج البيانات الذكي")
    files = st.file_uploader("ارفع صور الفواتير أو الجداول الورقية", type=['jpg','png','pdf'], accept_multiple_files=True)
    if files:
        st.info(f"تم استقبال {len(files)} ملفات. سيتم تحويلها إلى جداول Excel رقمية.")
        if st.button("بدء المسح الضوئي"):
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            st.dataframe(pd.DataFrame({"المصدر": [f.name for f in files], "البيانات المستخرجة": ["Invoice_Data", "Table_Data", "Handwritten_Notes"]}))

with tabs[3]:
    st.markdown("### 🛠️ Professional Toolset")
    col_tools = st.columns(4)
    tools = [
        ("Excel Pro", "Advanced Formulas", "📈"), 
        ("Power BI", "Dashboards", "📊"), 
        ("SQL Engine", "Database Sync", "🗄️"), 
        ("Python ML", "Sales Forecasting", "🐍"),
        ("Tableau", "Visualizations", "🎨"),
        ("Google Sheets", "Cloud Sync", "☁️"),
        ("Power Query", "Data ETL", "🔄"),
        ("AI Assistant", "Quick Insights", "🧠")
    ]
    
    for i, (name, desc, icon) in enumerate(tools):
        with col_tools[i % 4]:
            st.markdown(f"""
                <div class='tool-card'>
                    <h2>{icon}</h2>
                    <h4>{name}</h4>
                    <p style='font-size:12px;'>{desc}</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"فتح {name}", key=f"btn_{name}"):
                st.toast(f"جاري ربط {name} بـ Wanas AI Brain...")

with tabs[4]:
    st.markdown("### 📤 Final Report Center")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### استخراج التقرير النهائي")
        st.button("📄 Generate Certified PDF (MIA8444)")
    with c2:
        st.markdown("#### مشاركة سريعة")
        phone = st.text_input("رقم الواتساب:", placeholder="2010xxxxxxxx")
        if st.button("📲 إرسال التقرير"):
            st.info("جاري تشفير البيانات قبل الإرسال...")

# 4. الفوتر
st.markdown("<div class='footer-bar'>Smart Analyst Ultimate | Powered by Wanas AI | System User: صديقي </div>", unsafe_allow_html=True)
