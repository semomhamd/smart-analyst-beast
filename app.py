import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder
from prophet import Prophet
import easyocr
from PIL import Image
import os

# --- 1. الهوية والستايل (MIA8444) ---
st.set_page_config(page_title="Smart Analyst Beast PRO", layout="wide")

# --- 2. محرك الذاكرة ---
if 'main_df' not in st.session_state:
    st.session_state['main_df'] = pd.DataFrame()

# --- 3. تحميل محرك العين الرقمية (مرة واحدة في الذاكرة) ---
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['ar', 'en'], gpu=False)

# --- 4. السايد بار (تحت اللوجو: شات وصوت) ---
with st.sidebar:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg")
    st.markdown("<h3 style='text-align: center;'>MIA8444 Smart Assistant</h3>", unsafe_allow_html=True)
    
    msg = st.text_input("اسأل الوحش أي شيء:")
    if st.button("🎤 تحدث"): st.info("🎙️ جاري الاستماع...")
    
    st.write("---")
    menu = ["🏠 الرئيسية", "👁️ العين الرقمية", "📊 Excel Pro", "📈 التنبؤ المالي", "🧼 المنظف الذكي"]
    choice = st.radio("القائمة التنفيذية:", menu)

# --- 5. منطق الصفحات ---

# [العين الرقمية] - تم إصلاحها
if choice == "👁️ العين الرقمية":
    st.header("👁️ محرك الرؤية الذكي (OCR)")
    reader = load_ocr()
    img_file = st.file_uploader("ارفع صورة البيانات/الفاتورة", type=['jpg', 'jpeg', 'png'])
    if img_file:
        image = Image.open(img_file)
        st.image(image, caption="الصورة قيد التحليل")
        if st.button("تحليل الصورة واستخراج النصوص 🦁"):
            with st.spinner("جاري القراءة بذكاء MIA8444..."):
                results = reader.readtext(np.array(image))
                extracted_text = [res[1] for res in results]
                st.success("تم استخراج البيانات!")
                st.write(extracted_text)
                # تحويل بسيط لجدول
                st.session_state['main_df'] = pd.DataFrame(extracted_text, columns=["البيانات المستخرجة"])

# [التنبؤ المالي] - تم إصلاحه
elif choice == "📈 التنبؤ المالي":
    st.header("📈 محرك التنبؤ MIA8444")
    df = st.session_state['main_df']
    if not df.empty:
        # تأكد إن الأعمدة فيها 'ds' و 'y' للـ Prophet
        try:
            # مثال لبيانات تجريبية إذا لم يتوفر تاريخ
            if 'التاريخ' not in df.columns:
                st.warning("يرجى التأكد من وجود عمود باسم 'التاريخ' وعمود 'المبيعات'.")
                if st.button("توليد بيانات تاريخية للتجربة"):
                    df = pd.DataFrame({
                        'ds': pd.date_range(start='2025-01-01', periods=len(df)),
                        'y': np.random.randint(1000, 5000, len(df))
                    })
            else:
                df = df.rename(columns={'التاريخ': 'ds', 'المبيعات': 'y'})
            
            m = Prophet()
            m.fit(df[['ds', 'y']])
            future = m.make_future_dataframe(periods=30)
            forecast = m.predict(future)
            st.plotly_chart(px.line(forecast, x='ds', y='yhat', title="توقعات الشهر القادم"))
        except Exception as e:
            st.error(f"خطأ في محرك التنبؤ: {e}")
    else:
        st.warning("لا توجد بيانات للتحليل. ارفع ملف أولاً.")

# [الرئيسية وباقي الأدوات]
elif choice == "🏠 الرئيسية":
    st.title("🦁 بوابة التحكم الرئيسية")
    up = st.file_uploader("ارفع ملف Excel/CSV", type=['csv', 'xlsx'])
    if up:
        st.session_state['main_df'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
        st.rerun()
