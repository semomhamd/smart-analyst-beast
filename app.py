import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO
import urllib.parse

# --- 1. هوية MIA8444 والذاكرة [cite: 2026-01-26] ---
st.set_page_config(page_title="Smart Analyst Beast PRO", page_icon="🦁", layout="wide")

if 'db' not in st.session_state: 
    st.session_state['db'] = pd.DataFrame(columns=['البند', 'القيمة'])

# القائمة المطلوبة بالترتيب الجديد [cite: 2026-01-31]
menu_items = [
    "🏠 الرئيسية", 
    "📊 الاكسل برو والpivot table", 
    "✨ Cleaner", 
    "🧠 Ai analyst", 
    "📈 الرسوم البيانيه", 
    "📄 pdf والمشاركه علي الواتس"
]

# --- 2. السايد بار بتوقيع MIA8444 ---
with st.sidebar:
    st.title("🦁 MIA8444 Beast")
    st.write("---")
    choice = st.radio("القائمة:", menu_items)
    st.write("---")
    st.caption("Developed by MIA8444")
    st.info("You don't have to be a data analyst.. Smart Analyst thinks for you")

# --- 3. محرك الصفحات ---

if choice == menu_items[0]: # الرئيسية
    st.header("Smart Analyst Beast")
    st.subheader("أهلاً بك يا صديقي في مركز إدارة البيانات") [cite: 2026-01-11]
    up = st.file_uploader("ارفع ملفك الخاص (Excel/CSV)", type=["csv", "xlsx"])
    if up: 
        st.session_state['db'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
        st.success("تم رفع البيانات بنجاح! جاهز للانطلاق.")

elif choice == menu_items[1]: # 📊 الاكسل برو والpivot table
    st.header("📊 Excel Pro & Pivot Table") [cite: 2026-01-15]
    df = st.session_state['db']
    if not df.empty:
        st.subheader("📝 المحرر الذكي (تعديل مباشر):")
        df_ed = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        st.session_state['db'] = df_ed
        
        st.write("---")
        st.subheader("📉 الجدول المحوري (Pivot):")
        num_cols = df_ed.select_dtypes(include=[np.number]).columns.tolist()
        if num_cols:
            c1, c2 = st.columns(2)
            with c1: idx = st.selectbox("تصنيف (Rows):", df_ed.columns)
            with c2: val = st.selectbox("قيم (Values):", num_cols)
            st.dataframe(df_ed.groupby(idx)[val].sum().reset_index(), use_container_width=True)
    else: st.warning("ارفع ملفاً من الرئيسية أولاً")

elif choice == menu_items[2]: # ✨ Cleaner (صفحة التنظيف المستقلة)
    st.header("✨ Smart Data Cleaner") [cite: 2026-01-17, 2026-01-24]
    df = st.session_state['db']
    if not df.empty:
        st.write("بياناتك قبل التنظيف:")
        st.dataframe(df.head(5))
        if st.button("🚀 ابدأ عملية التنظيف الذكي (MIA8444 Version)"):
            # خوارزمية التنظيف المعتمدة [cite: 2025-11-13]
            df_cleaned = df.dropna(how='all').drop_duplicates().fillna(0)
            st.session_state['db'] = df_cleaned
            st.success("تم حذف الفراغات، التكرارات، وتصفير القيم الناقصة بنجاح!")
            st.balloons()
            st.dataframe(df_cleaned.head(5))
    else: st.warning("لا توجد بيانات لتنظيفها")

elif choice == menu_items[3]: # 🧠 Ai analyst
    st.header("🧠 AI Analyst Intelligence")
    df = st.session_state['db']
    if not df.empty:
        st.subheader("💡 تحليل الأنماط والنتائج:")
        st.write("بناءً على بياناتك، إليك أهم المؤشرات:")
        st.dataframe(df.describe()) # متوسطات وقمم البيانات [cite: 2025-11-13]
        st.metric("إجمالي السجلات", len(df))
    else: st.warning("لا توجد بيانات للتحليل")

elif choice == menu_items[4]: # 📈 الرسوم البيانيه
    st.header("📈 الرسوم البيانيه")
    df = st.session_state['db']
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if not df.empty and num_cols:
        x_axis = st.selectbox("اختر العمود الأفقي:", df.columns)
        y_axis = st.selectbox("اختر العمود الرأسي:", num_cols)
        fig = px.bar(df, x=x_axis, y=y_axis, color=y_axis, title=f"تحليل {y_axis} بواسطة {x_axis}")
        st.plotly_chart(fig, use_container_width=True)

elif choice == menu_items[5]: # 📄 pdf والمشاركه علي الواتس
    st.header("📄 مركز التقارير والمشاركة") [cite: 2026-01-15]
    if not st.session_state['db'].empty:
        # تصدير الملف
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            st.session_state['db'].to_excel(writer, index=False)
        st.download_button("📥 تحميل ملف الإكسيل النظيف", data=output.getvalue(), file_name="MIA8444_Clean_Report.xlsx")
        
        # مشاركة واتساب [cite: 2026-01-31]
        st.write("---")
        phone = st.text_input("رقم واتساب المدير (مثال: 2010xxxxxxxx):")
        if st.button("📲 إرسال إشعار التقرير"):
            msg = f"تم الانتهاء من التقرير وتنظيف البيانات بنجاح. تحياتي: MIA8444"
            url = f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"
            st.markdown(f'<a href="{url}" target="_blank">اضغط هنا لفتح واتساب وإرسال الرسالة</a>', unsafe_allow_width=True)
