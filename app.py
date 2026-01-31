import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO
import urllib.parse

# 1. إعدادات الهوية والواجهة
st.set_page_config(page_title="Smart Analyst Beast PRO", page_icon="🦁", layout="wide")

if 'db' not in st.session_state: 
    st.session_state['db'] = pd.DataFrame(columns=['البند', 'القيمة'])

# القائمة الموحدة والمنظمة (منظف البيانات بعد الرئيسية)
menu_items = [
    "الرئيسية", 
    "منظف البيانات", 
    "الاكسل برو", 
    "المحلل الذكي", 
    "الرسوم البيانيه", 
    "التقرير النهائي(pdf, المشاركه)"
]

# 2. السايد بار (MIA8444)
with st.sidebar:
    st.title("🦁 MIA8444 Beast")
    st.write("---")
    choice = st.radio("القائمة الرئيسية:", menu_items)
    st.write("---")
    st.caption("Signature: MIA8444")

# 3. تشغيل الصفحات

if choice == menu_items[0]: # الرئيسية
    st.header("Smart Analyst Beast")
    st.subheader("You don't have to be a data analyst.. Smart Analyst thinks for you")
    
    if st.button("🚀 توليد بيانات اختبار فورية"):
        st.session_state['db'] = pd.DataFrame({
            'المنتج': ['موبايل', 'لاب توب', 'ساعة'] * 10,
            'المبيعات': np.random.randint(100, 5000, 30),
            'الكمية': np.random.randint(1, 20, 30)
        })
        st.success("تم شحن البيانات! اذهب لمنظف البيانات أو الاكسل برو.")
    
    up = st.file_uploader("ارفع ملفك الخاص", type=["csv", "xlsx"])
    if up: 
        st.session_state['db'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
        st.success("تم الرفع بنجاح!")

elif choice == menu_items[1]: # منظف البيانات (مفعل الآن!)
    st.header("✨ منظف البيانات الذكي")
    df = st.session_state['db']
    if not df.empty:
        st.write("بياناتك الحالية تحتوي على:", df.shape[0], "صف.")
        if st.button("🚀 ابدأ التنظيف (حذف الفراغات والتكرارات)"):
            # تصفير الفراغات وحذف المكرر
            cleaned_df = df.dropna(how='all').drop_duplicates().fillna(0)
            st.session_state['db'] = cleaned_df
            st.success("تم تنظيف البيانات بنجاح! جاهزة للاستخدام في الاكسل برو.")
            st.dataframe(cleaned_df.head())
    else:
        st.warning("يرجى رفع ملف من الرئيسية أولاً.")

elif choice == menu_items[2]: # الاكسل برو
    st.header("📊 الاكسل برو")
    df = st.session_state['db']
    if not df.empty:
        st.subheader("📝 محرر البيانات (Excel Editor):")
        df_ed = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        st.session_state['db'] = df_ed
        
        st.write("---")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.subheader("🧮 الدوال:")
            num_cols = df_ed.select_dtypes(include=[np.number]).columns.tolist()
            if num_cols:
                target = st.selectbox("العمود:", num_cols)
                st.metric("المجموع", f"{df_ed[target].sum():,}")
        with col2:
            st.subheader("📉 التحليل المحوري (Pivot):")
            if num_cols:
                idx = st.selectbox("الصفوف:", df_ed.columns)
                val = st.selectbox("القيم:", num_cols)
                # حل مشكلة الـ ValueError بمنع تكرار الأسماء
                pivot_res = df_ed.groupby(idx)[val].sum().reset_index()
                pivot_res.columns = [idx, f"إجمالي {val}"]
                st.dataframe(pivot_res, use_container_width=True)

elif choice == menu_items[5]: # التقرير النهائي(pdf, المشاركه)
    st.header("📄 التقرير النهائي والمشاركه")
    if not st.session_state['db'].empty:
        output = BytesIO()
        # استخدام المحرك الافتراضي لتجنب أخطاء المكتبات المفقودة
        st.session_state['db'].to_excel(output, index=False)
        st.download_button("📥 تحميل التقرير (Excel)", data=output.getvalue(), file_name="MIA8444_Report.xlsx")
        
        st.write("---")
        phone = st.text_input("رقم واتساب المدير:")
        if st.button("📲 مشاركة"):
            msg = "التقرير النهائي جاهز. التوقيع: MIA8444"
            url = f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"
            st.markdown(f'<a href="{url}" target="_blank">فتح واتساب للإرسال</a>', unsafe_allow_html=True)
