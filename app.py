import streamlit as st
import pandas as pd
import numpy as np
import os
from PIL import Image

# تأكد أن السطور التالية تبدأ من أول السطر تماماً بدون أي مسافات
try:
    from cleaner_pro import clean_data
    from excel_master import process_excel
    from ai_analyst import run_analysis
    from power_bi_hub import show_charts
    from ai_vision import run_ocr
except Exception as e:
    st.error(f"مشكلة في استدعاء الملفات يا صديقي: {e}")

# إعدادات الهوية الفخمة
st.set_page_config(page_title="Smart Analyst Beast PRO", layout="wide")

# السايد بار (اللوجو والشات والمايك)
with st.sidebar:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg")
    st.markdown("<center><b>Smart Analyst thinks for you</b></center>", unsafe_allow_html=True)
    
    st.write("---")
    # خانة الشات الثابتة
    chat_val = st.text_input("💬 اسأل MIA8444:", placeholder="اكتب هنا...")
    
    menu = ["الرئيسية", "منظف البيانات", "الاكسل برو", "المحلل الذكي", "الرؤية الذكية (OCR)", "الرسوم البيانيه", "المستشار المالي"]
    choice = st.radio("القائمة:", menu)
    st.info("Signature: MIA8444")

# منطق عمل الصفحات
if 'data' not in st.session_state:
    st.session_state['data'] = pd.DataFrame()

df = st.session_state['data']

if choice == "الرئيسية":
    st.header("🏠 بوابة البيانات الذكية")
    up = st.file_uploader("ارفع ملف Excel/CSV", type=['csv', 'xlsx'])
    if up:
        st.session_state['data'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
        st.success("تم رفع البيانات بنجاح!")

elif choice == "منظف البيانات":
    st.header("🧼 منظف البيانات الاحترافي")
    if not df.empty:
        if st.button("Deep Clean ✨"):
            st.session_state['data'] = clean_data(df) # استدعاء من ملفك
            st.success("تم التنظيف!")
    else: st.warning("ارفع بيانات أولاً")

elif choice == "الاكسل برو":
    st.header("📊 محرر الاكسل الذكي")
    if not df.empty:
        process_excel(df) # استدعاء من ملفك

elif choice == "المحلل الذكي":
    st.header("🧠 المحلل الذكي (AI Analysis)")
    if not df.empty:
        run_analysis(df) # استدعاء من ملفك

elif choice == "الرؤية الذكية (OCR)":
    st.header("👁️ رؤية الوحش (OCR Vision)")
    run_ocr() # تفعيل الكاميرا والمسح

elif choice == "الرسوم البيانيه":
    st.header("📈 الرسوم البيانيه")
    if not df.empty:
        show_charts(df) # استدعاء من ملفك
