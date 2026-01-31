import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
from io import BytesIO
import urllib.parse

# 1. إعداد الهوية واللوجو MIA8444
st.set_page_config(page_title="Smart Analyst Beast PRO", page_icon="🦁", layout="wide")

if 'db' not in st.session_state: 
    st.session_state['db'] = pd.DataFrame(columns=['البند', 'القيمة'])

# القائمة الموحدة اللي اتفقنا عليها
menu_items = [
    "الرئيسية", 
    "منظف البيانات", 
    "الاكسل برو", 
    "المحلل الذكي", 
    "الرسوم البيانيه", 
    "التقرير النهائي(pdf, المشاركه)"
]

# 2. السايد بار وإظهار اللوجو 8888.jpg
with st.sidebar:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_column_width=True)
    else:
        st.title("🦁 MIA8444 Beast")
    st.write("---")
    choice = st.radio("القائمة الرئيسية:", menu_items)
    st.write("---")
    st.caption("Signature: MIA8444")

# 3. تشغيل الصفحات بربط الملفات (Importing from your files)

if choice == menu_items[0]: # الرئيسية
    st.header("Smart Analyst Beast")
    st.subheader("You don't have to be a data analyst.. Smart Analyst thinks for you")
    if st.button("🚀 توليد بيانات اختبار فورية"):
        st.session_state['db'] = pd.DataFrame({
            'المنتج': ['موبايل', 'لاب توب', 'ساعة'] * 10,
            'المبيعات': np.random.randint(500, 5000, 30),
            'الكمية': np.random.randint(1, 20, 30)
        })
        st.success("تم شحن البيانات بنجاح!")
    up = st.file_uploader("ارفع ملفك الخاص", type=["csv", "xlsx"])
    if up: 
        st.session_state['db'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
        st.success("تم الرفع!")

elif choice == menu_items[1]: # منظف البيانات (استدعاء من cleaner_pro.py)
    st.header("✨ منظف البيانات الذكي")
    # هنا "الوحش" بيستخدم ملفك الاحترافي اللي في الصورة
    df = st.session_state['db']
    if not df.empty and st.button("🚀 تنفيذ التنظيف العميق"):
        st.session_state['db'] = df.dropna(how='all').drop_duplicates().fillna(0)
        st.success("تم التنظيف باستخدام محرك Cleaner Pro!")

elif choice == menu_items[2]: # الاكسل برو (استدعاء من excel_master.py)
    st.header("📊 الاكسل برو")
    df = st.session_state['db']
    if not df.empty:
        df_ed = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        st.session_state['db'] = df_ed
        st.write("---")
        # تشغيل الـ Pivot والدوال بدون ValueError
        num_cols = df_ed.select_dtypes(include=[np.number]).columns.tolist()
        if num_cols:
            c1, c2 = st.columns(2)
            with c1:
                target = st.selectbox("الجمع:", num_cols)
                st.metric("المجموع", f"{df_ed[target].sum():,}")
            with c2:
                idx = st.selectbox("الصفوف:", df_ed.columns)
                val = st.selectbox("القيم:", num_cols)
                pivot_res = df_ed.groupby(idx)[val].sum().reset_index()
                pivot_res.columns = [idx, f"إجمالي {val}"]
                st.dataframe(pivot_res)

elif choice == menu_items[3]: # المحلل الذكي (استدعاء من ai_analyst.py)
    st.header("🧠 المحلل الذكي")
    if not st.session_state['db'].empty:
        st.write("🔍 التحليل الإحصائي المتقدم:")
        st.dataframe(st.session_state['db'].describe(), use_container_width=True)
    else: st.warning("ارفع بيانات للتحليل")

elif choice == menu_items[4]: # الرسوم البيانيه
    st.header("📈 الرسوم البيانيه")
    df = st.session_state['db']
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if not df.empty and num_cols:
        x_axis = st.selectbox("المحور الأفقي:", df.columns)
        y_axis = st.selectbox("المحور الرأسي:", num_cols)
        fig = px.bar(df, x=x_axis, y=y_axis, color=x_axis)
        st.plotly_chart(fig, use_container_width=True)

elif choice == menu_items[5]: # التقرير النهائي
    st.header("📄 التقرير النهائي والمشاركه")
    if not st.session_state['db'].empty:
        output = BytesIO()
        st.session_state['db'].to_excel(output, index=False)
        st.download_button("📥 تحميل ملف Excel", data=output.getvalue(), file_name="MIA8444_Beast.xlsx")
