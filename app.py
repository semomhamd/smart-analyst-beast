import streamlit as st
import pandas as pd
import os

# 1. إعدادات الصفحة والذاكرة
st.set_page_config(page_title="Smart Analyst Beast", layout="wide")

if 'main_data' not in st.session_state:
    st.session_state['main_data'] = None

# 2. القائمة الجانبية (Sidebar)
with st.sidebar:
    st.header("🦁 لوحة التحكم")
    # التأكد من وجود اللوجو في نفس الفولدر [cite: 2026-01-28]
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg")
    
    choice = st.radio("اختر الأداة:", ["🏠 الرئيسية", "🧹 التنظيف", "☁️ جوجل شيتس"])
    st.write("---")
    st.write("Verified by: *MIA8444*")

# 3. تشغيل الصفحات
if choice == "🏠 الرئيسية":
    st.title("مرحباً بك")
    uploaded = st.file_uploader("ارفع ملف الإكسيل هنا", type=['xlsx', 'csv'])
    if uploaded:
        df = pd.read_excel(uploaded) if uploaded.name.endswith('xlsx') else pd.read_csv(uploaded)
        st.session_state['main_data'] = df
        st.success("تم رفع البيانات بنجاح! روح لصفحة التنظيف دلوقتي.")

elif choice == "🧹 التنظيف":
    st.title("🧹 محرك التنظيف الذكي")
    if st.session_state['main_data'] is not None:
        df = st.session_state['main_data']
        st.dataframe(df.head(10))
        if st.button("حذف الصفوف الفارغة"):
            st.session_state['main_data'] = df.dropna(how='all')
            st.success("تم التنظيف يا بطل! MIA8444")
            st.rerun()
    else:
        st.warning("ارفع ملف الأول من الصفحة الرئيسية")

elif choice == "☁️ جوجل شيتس":
    st.title("☁️ جوجل شيتس Master")
    url = st.text_input("حط رابط الشيت هنا:")
    if st.button("سحب البيانات"):
        st.info("جاري المزامنة السحابية... (MIA8444)")
