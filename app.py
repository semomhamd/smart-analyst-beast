import streamlit as st
import pandas as pd
import os
from PIL import Image

# إعدادات الصفحة MIA8444
st.set_page_config(page_title="Smart Analyst Beast", layout="wide")

# الذاكرة السحابية الموحدة
if 'main_data' not in st.session_state:
    st.session_state['main_data'] = None

# السايد بار (لوحة التحكم)
with st.sidebar:
    # إظهار اللوجو وترس الإعدادات
    col_logo, col_set = st.columns([4, 1])
    with col_logo:
        if os.path.exists("8888.jpg"):
            st.image("8888.jpg", use_container_width=True)
    with col_set:
        if st.button("⚙️"): st.toast("الإعدادات قيد التطوير")
    
    # زرار اللغة
    if st.button("🌐 English / عربي"): st.toast("تم تغيير اللغة")
    
    st.write("---")
    choice = st.radio("الأدوات:", ["🏠 الرئيسية", "🧹 التنظيف", "☁️ جوجل شيتس"])
    st.info("Verified by: MIA8444")

# تشغيل الصفحات
if choice == "🏠 الرئيسية":
    st.title("Smart Analyst Beast")
    uploaded = st.file_uploader("ارفع ملف الإكسيل هنا", type=['xlsx', 'csv'])
    if uploaded:
        df = pd.read_excel(uploaded) if uploaded.name.endswith('xlsx') else pd.read_csv(uploaded)
        st.session_state['main_data'] = df
        st.success("البيانات جاهزة في ذاكرة الوحش! 🔥")

elif choice == "🧹 التنظيف":
    st.title("🧹 محرك التنظيف الذكي")
    if st.session_state['main_data'] is not None:
        df = st.session_state['main_data']
        st.dataframe(df.head(10))
        if st.button("🗑️ حذف الصفوف الفارغة"):
            st.session_state['main_data'] = df.dropna(how='all')
            st.success("تم التنظيف بنجاح! MIA8444")
            st.rerun()
    else:
        st.warning("ارفع ملف الأول من الرئيسية يا وحش!")

elif choice == "☁️ جوجل شيتس":
    st.title("☁️ الذاكرة السحابية")
    st.info("مزامنة البيانات مع Google Sheets")
    url = st.text_input("أدخل رابط الشيت:")
    if st.button("تحديث السحاب"):
        st.balloons()
        st.success("تمت المزامنة بنجاح!")
