from auth_system import login_pagimport streamlit as st
# استدعاء الترسانة كاملة
import ocr_engine, cleaner_pro, pdf_pro, sql_beast, excel_master
import power_bi_hub, python_analytics, tableau_connect, ai_vision

# 1. إعدادات الصفحة والـ Dark Mode الافتراضي
st.set_page_config(page_title="Smart Analyst Beast v3.0", layout="wide")

# 2. لوحة التحكم الجانبية (Settings & Language)
with st.sidebar:
    st.image("8888.jpg", width=100)
    st.title("⚙️ Settings Control")
    
    # اختيار اللغة
    lang = st.radio("🌐 Select Language / اختر اللغة", ["English", "العربية"])
    
    # رسالة الحالة
    st.write("---")
    st.success(f"Mode: {'Professional' if lang == 'English' else 'احترافي'}")
    st.info("MIA8444 System v3.0")

# 3. الهوية البصرية (تتأثر باللغة المختارة)
title = "🐉 SMART ANALYST BEAST v3.0" if lang == "English" else "🐉 وحش التحليل الذكي v3.0"
subtitle = "The Ultimate Financial Brain | MIA8444" if lang == "English" else "العقل المالي المطلق | تصميم: MIA8444"

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("8888.jpg", width=200)
    st.markdown(f"<h1 style='text-align:center; color:#00C853;'>{title}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; opacity:0.8; font-weight:bold;'>{subtitle}</p>", unsafe_allow_html=True)

st.write("---")

# 4. نظام التبويبات (Tabs) - يتغير اسمه حسب اللغة
if lang == "English":
    tab_titles = ["🔍 OCR", "🧹 Power Query", "📄 PDF Pro", "🗄️ SQL", "📊 Excel", "📈 Power BI", "🐍 Python", "🖼️ Tableau", "🧠 AI in Data"]
else:
    tab_titles = ["🔍 سحب البيانات", "🧹 تنظيف البيانات", "📄 محول PDF", "🗄️ قواعد البيانات", "📊 إكسيل", "📈 باور بي آي", "🐍 بايثون", "🖼️ تابلو", "🧠 ذكاء اصطناعي"]

tabs = st.tabs(tab_titles)

# ربط التبويبات بالملفات (الترتيب ثابت)
with tabs[0]: ocr_engine.run_module()
with tabs[1]: cleaner_pro.run_module()
with tabs[2]: pdf_pro.run_module()
with tabs[3]: sql_beast.run_module()
with tabs[4]: excel_master.run_module()
with tabs[5]: power_bi_hub.run_module()
with tabs[6]: python_analytics.run_module()
with tabs[7]: tableau_connect.run_module()
with tabs[8]: ai_vision.run_module()
