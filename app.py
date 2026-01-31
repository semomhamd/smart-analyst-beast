import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO
import urllib.parse

# --- 1. الهوية MIA8444 والذاكرة ---
st.set_page_config(page_title="Smart Analyst Beast PRO", page_icon="🦁", layout="wide")

if 'db' not in st.session_state: 
    st.session_state['db'] = pd.DataFrame(columns=['البند', 'القيمة'])

# القائمة والترتيب اللي اتفقنا عليه
menu_items = [
    "🏠 الرئيسية", 
    "📊 الاكسل برو والpivot table", 
    "✨ cleaner", 
    "🧠 Ai analyst", 
    "📈 الرسوم البيانيه", 
    "📄 pdf والمشاركه علي الواتس"
]

# --- 2. السايد بار واللوجو MIA8444 ---
with st.sidebar:
    try:
        st.image("8888.jpg", use_column_width=True) 
    except:
        st.title("🦁 MIA8444 Beast")
    st.write("---")
    choice = st.radio("القائمة:", menu_items)
    st.write("---")
    st.caption("Signature: MIA8444")

# --- 3. تشغيل الصفحات الذكية ---

if choice == menu_items[0]: # الرئيسية
    st.header("Smart Analyst Beast")
    # الجملة اللي اتفقنا عليها بدون أي أخطاء برمجة
    st.subheader("You don't have to be a data analyst.. Smart Analyst thinks for you")
    up = st.file_uploader("ارفع ملفك الخاص", type=["csv", "xlsx"])
    if up: 
        st.session_state['db'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
        st.success("تم رفع البيانات بنجاح!")

elif choice == menu_items[1]: # الاكسل برو والpivot table
    st.header("📊 Excel Pro & Pivot Table")
    df = st.session_state['db']
    if not df.empty:
        st.write("📝 المحرر الذكي:")
        df_ed = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        st.session_state['db'] = df_ed
        st.write("---")
        st.subheader("📉 الجدول المحوري (Pivot Table):")
        num_cols = df_ed.select_dtypes(include=[np.number]).columns.tolist()
        if num_cols:
            c1, c2 = st.columns(2)
            with c1: idx = st.selectbox("Rows:", df_ed.columns)
            with c2: val = st.selectbox("Values (Numbers Only):", num_cols)
            # حل الـ ValueError بفصل الأرقام عن النصوص
            st.dataframe(df_ed.groupby(idx)[val].sum().reset_index(), use_container_width=True)
    else: st.warning("ارفع ملفاً أولاً")

elif choice == menu_items[2]: # cleaner
    st.header("✨ Smart Data Cleaner")
    df = st.session_state['db']
    if not df.empty:
        if st.button("🚀 ابدأ التنظيف فوراً"):
            # حذف الفراغات والتكرارات وتصفير الـ NaN
            st.session_state['db'] = df.dropna(how='all').drop_duplicates().fillna(0)
            st.success("تم تنظيف البيانات وحذف القيم الفارغة بنجاح!")
            st.rerun()
    else: st.warning("لا توجد بيانات لتنظيفها")

elif choice == menu_items[3]: # Ai analyst
    st.header("🧠 AI Analyst Intelligence")
    df = st.session_state['db']
    if not df.empty:
        st.write("💡 تحليل الذكاء الاصطناعي التلقائي:")
        st.dataframe(df.describe())
    else: st.warning("ارفع بيانات للتحليل")

elif choice == menu_items[4]: # الرسوم البيانيه
    st.header("📈 الرسوم البيانيه")
    df = st.session_state['db']
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if not df.empty and num_cols:
        x = st.selectbox("المحور الأفقي:", df.columns)
        y = st.selectbox("المحور الرأسي:", num_cols)
        st.plotly_chart(px.bar(df.head(50), x=x, y=y, color=y), use_container_width=True)

elif choice == menu_items[5]: # pdf والمشاركه علي الواتس
    st.header("📄 مركز التقارير والمشاركة")
    if not st.session_state['db'].empty:
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            st.session_state['db'].to_excel(writer, index=False)
        st.download_button("📥 تحميل التقرير (Excel)", data=output.getvalue(), file_name="MIA8444_Report.xlsx")
        
        st.write("---")
        phone = st.text_input("رقم واتساب المدير (بالكود الدولي):")
        if st.button("📲 إرسال إشعار للمدير"):
            msg = "التقرير جاهز يا فندم. التوقيع: MIA8444"
            url = f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"
            st.markdown(f'<a href="{url}" target="_blank">اضغط لفتح واتساب</a>', unsafe_allow_html=True)
