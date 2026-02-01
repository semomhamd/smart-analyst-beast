import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image
import os

# استيراد الوظائف من ملفاتك المنفصلة (Importing from your files)
try:
    from cleaner_pro import clean_data
    from ai_analyst import run_analysis
    from ai_vision import vision_check
except ImportWarning:
    pass

# 1. إعدادات الواجهة الاحترافية
st.set_page_config(page_title="Smart Analyst Beast PRO", page_icon="🦁", layout="wide")

# الجملة الرسمية تحت اللوجو فقط
slogan = "You don't have to be a data analyst.. Smart Analyst thinks for you"

if 'db' not in st.session_state: st.session_state['db'] = pd.DataFrame()

# 2. السايد بار مع اللوجو 8888.jpg وتنسيق MIA8444
with st.sidebar:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_column_width=True)
    st.markdown(f"<center><b>{slogan}</b></center>", unsafe_allow_html=True)
    st.write("---")
    
    # الإعدادات المتقدمة (Settings)
    with st.expander("⚙️ الإعدادات واللغة"):
        lang = st.radio("اللغة", ["العربية", "English"])
        theme = st.select_slider("المظهر (Mode)", ["Dark", "Light"])
        st.info("تم ضبط المظهر أوتوماتيكياً")

    st.write("---")
    menu = ["الرئيسية", "منظف البيانات", "الاكسل برو", "المحلل الذكي", "الرؤية الذكية (Vision)", "الرسوم البيانيه", "التقرير النهائي"]
    choice = st.radio("القائمة الرئيسية:", menu)
    st.write("---")
    st.caption("Signature: MIA8444")

# 3. محرك العمليات
df = st.session_state['db']

if choice == "الرئيسية":
    st.header("🏠 بوابة البيانات - Smart Analyst Beast")
    col1, col2 = st.columns([3, 1])
    with col1:
        up = st.file_uploader("ارفع ملف Excel أو CSV", type=["csv", "xlsx"])
        if up:
            st.session_state['db'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
            st.success("تم شحن الوحش بالبيانات!")
    with col2:
        if st.button("🚀 توليد بيانات اختبار"):
            st.session_state['db'] = pd.DataFrame({
                'المنتج': ['موبايل', 'ساعة', 'لاب توب'] * 10,
                'المبيعات': np.random.randint(100, 1000, 30),
                'الكمية': np.random.randint(1, 20, 30)
            })
            st.rerun()

elif choice == "منظف البيانات":
    st.header("✨ منظف البيانات الاحترافي")
    if not df.empty:
        # هنا بننادي على الوظيفة من ملف cleaner_pro.py لو موجود
        if st.button("🚀 تنظيف عميق (Deep Clean)"):
            st.session_state['db'] = df.dropna(how='all').drop_duplicates().fillna(0)
            st.success("تم غسيل البيانات بنجاح!")
            st.dataframe(st.session_state['db'].head())
    else: st.warning("ارفع بياناتك الأول يا محمد")

elif choice == "الاكسل برو":
    st.header("📊 محرر الاكسل الذكي")
    if not df.empty:
        df_ed = st.data_editor(df, use_container_width=True, key="beast_editor")
        st.session_state['db'] = df_ed
        num_cols = df_ed.select_dtypes(include=[np.number]).columns.tolist()
        if num_cols:
            st.write("---")
            target = st.selectbox("عمود الحساب:", num_cols)
            # حل مشكلة الـ ValueError نهائياً (الصورة 954afff6)
            other_cols = [c for c in df_ed.columns if c != target]
            idx = st.selectbox("تصنيف حسب:", other_cols if other_cols else df_ed.columns)
            res = df_ed.groupby(idx)[target].sum().reset_index()
            res.columns = [idx, f"إجمالي {target}"]
            st.dataframe(res, use_container_width=True)

elif choice == "المحلل الذكي":
    st.header("🧠 عقل المحلل (AI Analyst)")
    if not df.empty:
        st.write("🔍 ملخص إحصائي شامل:")
        st.dataframe(df.describe())
        # هنا ممكن نربط ملف ai_analyst.py لاحقاً
    else: st.warning("لا توجد بيانات للتحليل")

elif choice == "الرؤية الذكية (Vision)":
    st.header("👁️ رؤية الوحش (AI Vision)")
    st.write("هذا القسم يستخدم مكتبة Pillow لتحليل صور التقارير")
    # ميزة متقدمة لاستخدام ملف ai_vision.py
    cam = st.camera_input("التقط صورة لتقرير مطبوع")

elif choice == "الرسوم البيانيه":
    st.header("📈 الرسوم البيانيه (Plotly Engine)")
    if not df.empty:
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if num_cols:
            x = st.selectbox("المحور الأفقي:", df.columns)
            y = st.selectbox("المحور الرأسي:", num_cols)
            fig = px.bar(df, x=x, y=y, color=x, template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
