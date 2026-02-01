import streamlit as st
import pandas as pd
import numpy as np
import os
from PIL import Image

# تأكد إن السطور اللي تحت دي مفيش قبلها أي مسافات (Indentation Fix)
try:
    from cleaner_pro import clean_data
    from excel_master import process_excel
    from ai_analyst import run_analysis
    from power_bi_hub import show_charts
except ImportError as e:
    st.error(f"فيه ملف ناقص يا صديقي: {e}")

# إعدادات الصفحة
st.set_page_config(page_title="Smart Analyst Beast", layout="wide")

# السايد بار واللوجو
with st.sidebar:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg")
    st.write("---")
    menu = ["الرئيسية", "منظف البيانات", "الاكسل برو", "المحلل الذكي", "الرسوم البيانيه", "المستشار المالي"]
    choice = st.radio("اختر الأداة:", menu)
    st.info("Signature: MIA8444")

# تشغيل الصفحات بناءً على الاختيار
if choice == "الرئيسية":
    st.title("🏠 بوابة البيانات الذكية")
    uploaded_file = st.file_uploader("ارفع ملفك هنا", type=['csv', 'xlsx'])
    if uploaded_file:
        st.session_state['data'] = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('csv') else pd.read_excel(uploaded_file)
        st.success("تم رفع البيانات بنجاح!")

elif choice == "منظف البيانات":
    st.title("🧼 منظف البيانات الاحترافي")
    if 'data' in st.session_state:
        # هنا بنادي على وظيفة التنظيف
        st.write("جاري تجهيز أدوات التنظيف...")
    else:
        st.warning("ارفع ملف الأول من الصفحة الرئيسية يا صديقي.")

# وباقي الصفحات بنفس الطريقة...
