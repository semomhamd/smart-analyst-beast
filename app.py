import streamlit as st
import pandas as pd
import numpy as np
import os
from io import BytesIO

# 1. إعدادات الهوية والدارك مود
st.set_page_config(page_title="Smart Analyst Beast PRO", page_icon="🦁", layout="wide")

# الجملة اللي بتميزنا
slogan = "You don't have to be a data analyst.. Smart Analyst thinks for you"

# 2. نظام الإعدادات واللغة والدارك مود
if 'language' not in st.session_state: st.session_state.language = 'العربية'
if 'theme' not in st.session_state: st.session_state.theme = 'Dark'

with st.sidebar:
    # إظهار اللوجو 8888.jpg (تأكد من وجود الملف في الـ GitHub)
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_column_width=True)
    else:
        st.title("🦁 MIA8444")
    
    st.write(f"*{slogan}*")
    st.write("---")
    
    # قسم الإعدادات
    with st.expander("⚙️ الإعدادات (Settings)"):
        st.session_state.language = st.selectbox("اللغة", ["العربية", "English"])
        st.session_state.theme = st.selectbox("المظهر", ["Dark", "Light"])
    
    st.write("---")
    menu = ["الرئيسية", "منظف البيانات", "الاكسل برو", "المحلل الذكي", "الرسوم البيانيه", "التقرير النهائي"]
    choice = st.radio("القائمة:", menu)
    st.write("---")
    st.caption("Signature: MIA8444")

# 3. تشغيل المحرك
df = st.session_state.get('db', pd.DataFrame())

if choice == "الرئيسية":
    st.header("🏠 Smart Analyst Beast")
    st.subheader(slogan) # الجملة اللي طلبتها
    up = st.file_uploader("ارفع ملفك (Excel/CSV)", type=["csv", "xlsx"])
    if up:
        st.session_state['db'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
        st.success("تم الرفع بنجاح!")

elif choice == "منظف البيانات":
    st.header("✨ منظف البيانات")
    if not df.empty:
        if st.button("🚀 تنظيف احترافي"):
            st.session_state['db'] = df.dropna(how='all').drop_duplicates().fillna(0)
            st.success("البيانات أصبحت جاهزة ونظيفة!")
    else: st.warning("ارفع ملف أولاً")

elif choice == "الاكسل برو":
    st.header("📊 الاكسل برو")
    if not df.empty:
        df_ed = st.data_editor(df, use_container_width=True)
        st.session_state['db'] = df_ed
        # دوال متقدمة
        num_cols = df_ed.select_dtypes(include=[np.number]).columns.tolist()
        if num_cols:
            col1, col2 = st.columns(2)
            with col1:
                target = st.selectbox("العمود الحسابي:", num_cols)
                st.metric("المجموع", f"{df_ed[target].sum():,}")
            with col2:
                # حل مشكلة الـ Pivot والـ ValueError
                idx = st.selectbox("تصنيف حسب:", [c for c in df_ed.columns if c != target])
                res = df_ed.groupby(idx)[target].sum().reset_index()
                res.columns = [idx, f"إجمالي {target}"]
                st.dataframe(res)

elif choice == "المحلل الذكي":
    st.header("🧠 المحلل الذكي (AI Analysis)")
    if not df.empty:
        st.write("### 💡 استنتاجات البيانات:")
        col1, col2 = st.columns(2)
        with col1:
            st.write("*ملخص الأرقام:*")
            st.write(df.describe())
        with col2:
            st.write("*تحليل الجودة:*")
            st.write(f"- عدد الأعمدة: {len(df.columns)}")
            st.write(f"- عدد السجلات: {len(df)}")
            st.write(f"- القيم المفقودة: {df.isnull().sum().sum()}")
    else: st.warning("لا توجد بيانات للتحليل")
