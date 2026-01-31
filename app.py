import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO
import urllib.parse

# --- 1. الإعدادات والذاكرة ---
st.set_page_config(page_title="Smart Analyst Beast PRO", page_icon="🦁", layout="wide")

if 'db' not in st.session_state: 
    st.session_state['db'] = pd.DataFrame(columns=['البند', 'القيمة'])

# القائمة الموحدة باللغة العربية (بدون عشوائية)
menu_items = [
    "الرئيسية", 
    "اكسل برو و Pivot Table", 
    "منظف البيانات (Cleaner)", 
    "المحلل الذكي (AI Analyst)", 
    "الرسوم البيانية", 
    "التقارير والمشاركة واتساب"
]

# --- 2. السايد بار واللوجو MIA8444 ---
with st.sidebar:
    try:
        st.image("8888.jpg", use_column_width=True) 
    except:
        st.title("🦁 MIA8444")
    st.write("---")
    choice = st.radio("قائمة التحكم:", menu_items)
    st.write("---")
    st.caption("Signature: MIA8444")

# --- 3. تشغيل الصفحات ---

if choice == menu_items[0]: # الرئيسية
    st.header("Smart Analyst Beast")
    st.subheader("You don't have to be a data analyst.. Smart Analyst thinks for you")
    up = st.file_uploader("ارفع ملف البيانات الخاص بك", type=["csv", "xlsx"])
    if up: 
        st.session_state['db'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
        st.success("تم رفع البيانات بنجاح!")

elif choice == menu_items[1]: # اكسل برو و Pivot Table
    st.header("📊 Excel Pro & Pivot Table")
    df = st.session_state['db']
    if not df.empty:
        st.subheader("📝 محرر البيانات (Excel Editor):")
        df_ed = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        st.session_state['db'] = df_ed
        
        st.write("---")
        st.subheader("📉 أدوات الـ Pivot Table:")
        num_cols = df_ed.select_dtypes(include=[np.number]).columns.tolist()
        if num_cols:
            c1, c2 = st.columns(2)
            with c1: idx = st.selectbox("تصنيف الصفوف (Rows):", df_ed.columns)
            with c2: val = st.selectbox("القيم المراد جمعها (Values):", num_cols)
            # حل مشكلة الـ ValueError في الصور
            pivot_res = df_ed.groupby(idx)[val].sum().reset_index()
            st.dataframe(pivot_res, use_container_width=True)
        else:
            st.warning("يرجى التأكد من وجود أعمدة تحتوي على أرقام لاستخدام الـ Pivot.")
    else: st.warning("ارفع ملفاً من الرئيسية أولاً")

elif choice == menu_items[2]: # منظف البيانات (Cleaner)
    st.header("✨ Smart Data Cleaner")
    df = st.session_state['db']
    if not df.empty:
        if st.button("🚀 ابدأ التنظيف (حذف الفراغات والتكرارات)"):
            st.session_state['db'] = df.dropna(how='all').drop_duplicates().fillna(0)
            st.success("تم تنظيف البيانات بنجاح!")
            st.rerun()
    else: st.warning("لا توجد بيانات لتنظيفها")

elif choice == menu_items[3]: # المحلل الذكي (AI Analyst)
    st.header("🧠 AI Analyst")
    df = st.session_state['db']
    if not df.empty:
        st.write("💡 الملخص الإحصائي التلقائي:")
        st.dataframe(df.describe())
    else: st.warning("ارفع بيانات للتحليل")

elif choice == menu_items[4]: # الرسوم البيانية
    st.header("📈 الرسوم البيانية")
    df = st.session_state['db']
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if not df.empty and num_cols:
        x = st.selectbox("المحور الأفقي:", df.columns)
        y = st.selectbox("المحور الرأسي:", num_cols)
        st.plotly_chart(px.bar(df.head(50), x=x, y=y, color=y), use_container_width=True)

elif choice == menu_items[5]: # التقارير والمشاركة واتساب
    st.header("📄 مركز التقارير")
    if not st.session_state['db'].empty:
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            st.session_state['db'].to_excel(writer, index=False)
        st.download_button("📥 تحميل التقرير النهائي (Excel)", data=output.getvalue(), file_name="MIA8444_Report.xlsx")
        
        st.write("---")
        phone = st.text_input("رقم واتساب المدير (بالكود الدولي مثل 201xxxx):")
        if st.button("📲 إرسال إشعار للمدير"):
            msg = "التقرير جاهز يا فندم. التوقيع: MIA8444"
            url = f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"
            st.markdown(f'<a href="{url}" target="_blank">اضغط هنا لفتح واتساب</a>', unsafe_allow_html=True)
