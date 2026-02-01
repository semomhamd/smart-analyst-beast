import streamlit as st
import pandas as pd
import os

# محاولة استيراد الملفات بحذر
try:
    from cleaner_pro import clean_data
    # لو الملفات التانية لسه فيها أخطاء، البرنامج مش هيقف
except Exception as e:
    st.sidebar.error(f"خطأ في ملفات الربط: {e}")

st.set_page_config(page_title="Smart Analyst Beast PRO", layout="wide")

# السايد بار الفخم
with st.sidebar:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg")
    st.write("### MIA8444 Control Center")
    menu = ["الرئيسية", "منظف البيانات", "الاكسل برو", "المحلل الذكي", "الرؤية الذكية (OCR)", "الرسوم البيانيه", "التقرير النهائي"]
    choice = st.radio("القائمة:", menu)

# إدارة البيانات
if 'data' not in st.session_state:
    st.session_state['data'] = pd.DataFrame()

# تشغيل الصفحات
if choice == "الرئيسية":
    st.header("🏠 بوابة البيانات الذكية")
    up = st.file_uploader("ارفع ملف Excel/CSV", type=['csv', 'xlsx'])
    if up:
        st.session_state['data'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
        st.success("تم شحن الوحش بالبيانات!")

elif choice == "منظف البيانات":
    st.header("🧼 منظف البيانات الاحترافي")
    if not st.session_state['data'].empty:
        if st.button("Deep Clean ✨"):
            st.session_state['data'] = clean_data(st.session_state['data'])
            st.success("تم التنظيف بنجاح!")
            st.dataframe(st.session_state['data'].head())
    else: st.warning("ارفع ملف من الرئيسية الأول")

elif choice == "الرسوم البيانيه":
    st.header("📈 الرسوم البيانيه")
    if not st.session_state['data'].empty:
        st.bar_chart(st.session_state['data'].select_dtypes(include='number'))
    else: st.warning("مفيش بيانات للرسم")
