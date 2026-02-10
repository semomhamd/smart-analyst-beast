import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

# ======== 1. الذاكرة المركزية (Session State) ========
# دي اللي هتربط كل الأدوات ببعض وتمنع اللخبطة
if 'main_data' not in st.session_state:
    st.session_state.main_data = None  # هنا البيانات بتتحفظ طول ما إنت فاتح

# ======== 2. الهوية والإعدادات ========
APP_NAME = "Smart Analyst"
AUTHOR_SIGNATURE = "MIA8444"
LOGO_FILE = "8888.jpg"

st.set_page_config(page_title=f"{AUTHOR_SIGNATURE} | {APP_NAME}", layout="wide")

# ======== 3. القائمة الجانبية المترتبة ========
with st.sidebar:
    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, use_container_width=True)
    st.markdown(f"<h2 style='text-align:center;'>{APP_NAME}</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    menu = st.radio("القائمة الرئيسية:", [
        "🏠 مركز التحكم",
        "📂 Excel Pro (إدخال يدوي)",
        "✨ منظف البيانات الخارق",
        "🔮 محرك التنبؤ والذكاء",
        "📤 جسر التصدير العالمي"
    ])
    
    st.markdown("---")
    with st.expander("⚙️ الإعدادات (الترس)"):
        st.selectbox("🌐 اللغة", ["العربية", "English"])
        st.color_picker("🎨 لون الهوية", "#58a6ff")

# ======== 4. تفعيل الأدوات المربوطة ببعضها ========

# --- قسم Excel Pro (هنا تقدر تدخل بيانات يدوي) ---
if menu == "📂 Excel Pro (إدخال يدوي)":
    st.header("📂 Excel Pro Hub")
    st.write("أدخل بياناتك هنا وسيقوم النظام بحفظها لكل الأدوات:")
    
    # جدول تفاعلي للإدخال اليدوي
    if 'manual_df' not in st.session_state:
        st.session_state.manual_df = pd.DataFrame(columns=["البند", "القيمة", "التاريخ"])
    
    input_df = st.data_editor(st.session_state.manual_df, num_rows="dynamic", use_container_width=True)
    
    if st.button("✅ اعتماد البيانات وربطها بالأدوات"):
        st.session_state.main_data = input_df
        st.session_state.manual_df = input_df
        st.success("تم الربط! البيانات الآن متاحة في المنظف والمحرك التنبئي.")

# --- قسم منظف البيانات (بيسحب من اللي دخلته فوق) ---
elif menu == "✨ منظف البيانات الخارق":
    st.header("✨ منظف البيانات")
    
    # اختيار: ترفع ملف جديد ولا تستخدم اللي دخلته يدوي؟
    source = st.radio("مصدر البيانات:", ["البيانات الحالية في الذاكرة", "رفع ملف جديد"])
    
    if source == "البيانات الحالية في الذاكرة" and st.session_state.main_data is not None:
        df = st.session_state.main_data
        st.write("البيانات اللي دخلتها يدوياً جاهزة للتنظيف:")
        st.dataframe(df)
        
        if st.button("🚀 بدء التنظيف الذكي"):
            df_clean = df.drop_duplicates().dropna(how='all')
            st.session_state.main_data = df_clean # تحديث الذاكرة بالبيانات النضيفة
            st.success("تم التنظيف وتحديث الذاكرة المركزية!")
    else:
        uploaded_file = st.file_uploader("ارفع ملف جديد لربطه بالنظام", type=['csv', 'xlsx'])
        if uploaded_file:
            df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file)
            st.session_state.main_data = df
            st.success("تم الرفع والربط بنجاح!")

# --- قسم التنبؤ (بيحلل البيانات اللي متنظفة في الذاكرة) ---
elif menu == "🔮 محرك التنبؤ والذكاء":
    st.header("🔮 محرك التنبؤ")
    if st.session_state.main_data is not None:
        df = st.session_state.main_data
        st.write("البيانات المربوطة جاهزة للتحليل:")
        st.dataframe(df.head())
        # هنا تحط كود التنبؤ اللي بيسحب من df
    else:
        st.warning("⚠️ لا توجد بيانات في الذاكرة. من فضلك ادخل بيانات في Excel Pro أولاً.")

# ======== 5. التوقيع النهائي ========
st.markdown(f"<div style='text-align:center; padding:20px; color:#8b949e;'>Property of {AUTHOR_SIGNATURE} | MIA8444 © 2026</div>", unsafe_allow_html=True)
