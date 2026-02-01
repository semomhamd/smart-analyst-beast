import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image
import os

# 1. إعدادات الهوية الفخمة (MIA8444)
st.set_page_config(page_title="Smart Analyst Beast PRO", page_icon="🦁", layout="wide")

# الجملة الرسمية اللي اتفقنا عليها
slogan = "You don't have to be a data analyst.. Smart Analyst thinks for you"

if 'db' not in st.session_state:
    st.session_state['db'] = pd.DataFrame()

# 2. السايد بار (الهوية الكاملة)
with st.sidebar:
    # إظهار اللوجو 8888.jpg
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_column_width=True)
    
    # الجملة تحت اللوجو مباشرة
    st.markdown(f"<center><b>{slogan}</b></center>", unsafe_allow_html=True)
    st.write("---")
    
    # قسم الإعدادات المتطور
    with st.expander("⚙️ الإعدادات (Settings)"):
        st.selectbox("اللغة", ["العربية", "English"])
        st.selectbox("المظهر", ["Dark Mode", "Light Mode"])
    
    st.write("---")
    menu = ["الرئيسية", "منظف البيانات", "الاكسل برو", "المحلل الذكي", "الرسوم البيانيه", "التقرير النهائي"]
    choice = st.radio("القائمة الرئيسية:", menu)
    st.write("---")
    st.info("Signature: MIA8444")

# 3. محرك العمليات (الربط مع مكتباتك)
df = st.session_state['db']

if choice == "الرئيسية":
    st.header("🏠 بوابة البيانات الذكية")
    col1, col2 = st.columns([3, 1])
    with col1:
        up = st.file_uploader("ارفع ملف Excel أو CSV", type=["csv", "xlsx"])
        if up:
            st.session_state['db'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
            st.success("تم شحن الوحش بالبيانات!")
    with col2:
        st.write("🔧 توليد سريع")
        if st.button("🚀 بيانات اختبار"):
            st.session_state['db'] = pd.DataFrame({
                'المنتج': ['موبايل', 'ساعة', 'سماعة'] * 10,
                'المبيعات': np.random.randint(100, 1000, 30),
                'الكمية': np.random.randint(1, 20, 30)
            })
            st.rerun()

elif choice == "منظف البيانات":
    st.header("✨ منظف البيانات الاحترافي")
    if not df.empty:
        if st.button("🚀 تنظيف عميق (Deep Clean)"):
            # تنظيف بدون الحاجة لملفات خارجية حالياً لتجنب أخطاء الربط
            st.session_state['db'] = df.dropna(how='all').drop_duplicates().fillna(0)
            st.success("تم غسيل البيانات بنجاح!")
            st.dataframe(st.session_state['db'].head())
    else:
        st.warning("ارفع بياناتك الأول يا بطل")

elif choice == "الاكسل برو":
    st.header("📊 محرر الاكسل الذكي")
    if not df.empty:
        # حل مشكلة الـ ValueError نهائياً (الصورة 954afff6)
        df_ed = st.data_editor(df, use_container_width=True, key="beast_editor")
        st.session_state['db'] = df_ed
        
        num_cols = df_ed.select_dtypes(include=[np.number]).columns.tolist()
        if num_cols:
            st.write("---")
            target = st.selectbox("عمود الحساب الرقمي:", num_cols)
            other_cols = [c for c in df_ed.columns if c != target]
            idx = st.selectbox("تصنيف حسب (عمود نصي):", other_cols if other_cols else df_ed.columns)
            
            res = df_ed.groupby(idx)[target].sum().reset_index()
            res.columns = [idx, f"إجمالي {target}"]
            st.dataframe(res, use_container_width=True)

elif choice == "الرسوم البيانيه":
    st.header("📈 الرسوم البيانيه (Plotly)")
    if not df.empty:
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if num_cols:
            x_ax = st.selectbox("المحور الأفقي:", df.columns)
            y_ax = st.selectbox("المحور الرأسي:", num_cols)
            fig = px.bar(df, x=x_ax, y=y_ax, color=x_ax, template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("لا توجد أعمدة رقمية للرسم!")
    else:
        st.warning("ارفع بيانات أولاً")

elif choice == "المحلل الذكي":
    st.header("🧠 المحلل الذكي")
    if not df.empty:
        st.write("💡 الملخص الإحصائي:")
        st.dataframe(df.describe())
