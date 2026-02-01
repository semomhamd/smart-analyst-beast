import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
from io import BytesIO

# 1. الهوية وتوقيع MIA8444 (بدون تواريخ مسببة للأخطاء)
st.set_page_config(page_title="Smart Analyst Beast PRO", page_icon="🦁", layout="wide")

if 'db' not in st.session_state: 
    st.session_state['db'] = pd.DataFrame(columns=['البند', 'القيمة'])

# القائمة المطلوبة: المنظف بعد الرئيسية مباشرة
menu_items = [
    "الرئيسية", 
    "منظف البيانات", 
    "الاكسل برو", 
    "المحلل الذكي", 
    "الرسوم البيانيه", 
    "التقرير النهائي"
]

# 2. السايد بار مع اللوجو 8888.jpg
with st.sidebar:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_column_width=True)
    else:
        st.title("🦁 MIA8444 Beast")
    st.write("---")
    choice = st.radio("القائمة الرئيسية:", menu_items)
    st.write("---")
    st.caption("Developed by MIA8444")

# 3. تشغيل الصفحات

if choice == menu_items[0]: # الرئيسية
    st.header("🏠 Smart Analyst Beast")
    st.subheader("You don't have to be a data analyst.. Smart Analyst thinks for you")
    
    up = st.file_uploader("ارفع ملف البيانات (Excel/CSV)", type=["csv", "xlsx"])
    if up: 
        try:
            st.session_state['db'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
            st.success("تم رفع الملف بنجاح يا محمد!")
        except Exception as e:
            st.error(f"خطأ في الرفع: {e}")
            
    if st.button("🚀 شحن ببيانات اختبار"):
        st.session_state['db'] = pd.DataFrame({
            'المنتج': ['موبايل', 'لاب توب', 'ساعة', 'سماعة'] * 5,
            'المبيعات': np.random.randint(500, 5000, 20),
            'الفرع': ['القاهرة', 'الإسكندرية'] * 10
        })

elif choice == menu_items[1]: # منظف البيانات (اليوم الثالث)
    st.header("✨ منظف البيانات (Cleaner Pro)")
    df = st.session_state['db']
    if not df.empty:
        st.info(f"البيانات الحالية: {df.shape[0]} صف.")
        if st.button("🚀 البدء في تنظيف البيانات"):
            # حذف الفراغات والتكرارات وتصفير القيم
            st.session_state['db'] = df.dropna(how='all').drop_duplicates().fillna(0)
            st.success("تم تنظيف البيانات! جاهزة الآن للاكسل برو.")
            st.dataframe(st.session_state['db'].head())
    else: st.warning("ارفع بيانات من الرئيسية أولاً.")

elif choice == menu_items[2]: # الاكسل برو (حل مشكلة الـ ValueError)
    st.header("📊 الاكسل برو (المحرر والدوال)")
    df = st.session_state['db']
    if not df.empty:
        # محرر البيانات التفاعلي
        df_ed = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        st.session_state['db'] = df_ed
        
        st.write("---")
        num_cols = df_ed.select_dtypes(include=[np.number]).columns.tolist()
        if num_cols:
            col1, col2 = st.columns([1, 2])
            with col1:
                target = st.selectbox("اختر العمود:", num_cols)
                st.metric("المجموع (SUM)", f"{df_ed[target].sum():,}")
                st.metric("المتوسط (AVERAGE)", f"{df_ed[target].mean():.2f}")
            with col2:
                st.subheader("📉 ملخص الـ Pivot:")
                p_idx = st.selectbox("تصنيف حسب:", df_ed.columns)
                # حل مشكلة ValueError بمنع تكرار الأسماء
                pivot_data = df_ed.groupby(p_idx)[target].sum().reset_index()
                pivot_data.columns = [p_idx, f"إجمالي {target}"]
                st.dataframe(pivot_data, use_container_width=True)

elif choice == menu_items[3]: # المحلل الذكي
    st.header("🧠 المحلل الذكي")
    df = st.session_state['db']
    if not df.empty:
        st.write("🔍 الملخص الإحصائي:")
        st.dataframe(df.describe())
    else: st.warning("لا توجد بيانات.")

elif choice == menu_items[4]: # الرسوم البيانيه
    st.header("📈 الرسوم البيانيه")
    df = st.session_state['db']
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if not df.empty and num_cols:
        x = st.selectbox("المحور الأفقي:", df.columns)
        y = st.selectbox("المحور الرأسي:", num_cols)
        st.plotly_chart(px.bar(df, x=x, y=y, color=x), use_container_width=True)

elif choice == menu_items[5]: # التقرير النهائي (حل مشكلة ModuleNotFoundError)
    st.header("📄 التقرير النهائي")
    if not st.session_state['db'].empty:
        output = BytesIO()
        # تصدير بدون طلب مكتبات خارجية تسبب الخطأ الأحمر
        st.session_state['db'].to_excel(output, index=False)
        st.download_button("📥 تحميل التقرير", data=output.getvalue(), file_name="MIA8444_Beast.xlsx")
