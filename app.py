import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
import easyocr
from prophet import Prophet
from st_aggrid import AgGrid, GridOptionsBuilder

# --- 1. الهوية الرسمية (MIA8444) ---
st.set_page_config(page_title="Smart Analyst Beast PRO", layout="wide", page_icon="🦁")

# --- 2. محرك الذاكرة ---
if 'main_df' not in st.session_state:
    st.session_state['main_df'] = pd.DataFrame()

@st.cache_resource
def load_ocr_model():
    return easyocr.Reader(['ar', 'en'], gpu=False)

# --- 3. بناء القائمة الجانبية الكاملة ---
with st.sidebar:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_container_width=True)
    st.markdown("<h2 style='text-align: center;'>Smart Analyst Beast</h2>", unsafe_allow_html=True)
    
    # القائمة الكاملة التي طلبتها يا صديقي
    menu = {
        "🏠 الرئيسية وبوابة التحكم": "Home",
        "👁️ العين الرقمية (OCR)": "OCR",
        "🧼 منظف البيانات الذكي": "Clean",
        "📊 Excel Pro (المحرر الأبيض)": "Excel",
        "🧠 المحلل الاستراتيجي": "Analysis",
        "📈 التنبؤ المالي (AI)": "Forecast",
        "🖥️ داشبورد الإدارة": "Dashboard"
    }
    choice = st.radio("انتقل بين أدواتك بدقة:", list(menu.keys()))
    st.write("---")
    st.caption("Owner: MIA8444")

df = st.session_state['main_df']

# --- 4. تشغيل الأدوات ---

if menu[choice] == "Home":
    st.title("🦁 مركز التحكم - MIA8444")
    up = st.file_uploader("ارفع ملف البيانات (Excel/CSV)", type=['csv', 'xlsx'])
    if up:
        st.session_state['main_df'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
        st.success("تم رفع البيانات!")
        st.rerun()

elif menu[choice] == "OCR":
    st.header("👁️ استخراج النصوص من الصور")
    reader = load_ocr_model()
    img = st.file_uploader("ارفع صورة جدول أو فاتورة", type=['jpg', 'png', 'jpeg'])
    if img:
        st.image(img)
        if st.button("تحويل الصورة لبيانات"):
            res = reader.readtext(np.array(Image.open(img)))
            st.write([r[1] for r in res])

elif menu[choice] == "Clean":
    st.header("🧼 تنظيف البيانات")
    if not df.empty:
        if st.button("إزالة الصفوف الفارغة والمكررة"):
            st.session_state['main_df'] = df.dropna().drop_duplicates()
            st.success("تم التنظيف!")
            st.dataframe(st.session_state['main_df'])
    else: st.warning("ارفع ملف أولاً.")

elif menu[choice] == "Excel":
    st.header("📊 Excel Pro المحرر")
    if not df.empty:
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_default_column(editable=True, groupable=True)
        grid_res = AgGrid(df, gridOptions=gb.build(), theme='balham')
        if st.button("حفظ التعديلات"):
            st.session_state['main_df'] = pd.DataFrame(grid_res['data'])
    else: st.warning("لا توجد بيانات للعرض.")

elif menu[choice] == "Dashboard":
    st.header("🖥️ داشبورد الإدارة")
    if not df.empty:
        nums = df.select_dtypes(include=[np.number]).columns.tolist()
        if nums:
            col = st.selectbox("اختر العمود للرسم:", nums)
            st.plotly_chart(px.area(df, y=col, title=f"تحليل {col}"))
    else: st.warning("ارفع البيانات لتفعيل الشاشة.")

# السطر السحري المصحح بشرطتين (__) لمنع الـ NameError
if __name__ == "__main__":
    pass
