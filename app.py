import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
from datetime import datetime, timedelta
from st_aggrid import AgGrid, GridOptionsBuilder

# --- 1. ذاكرة التطبيق (حفظ البيانات للجمهور) ---
if 'public_vault' not in st.session_state:
    st.session_state['public_vault'] = None

st.set_page_config(page_title="Smart Analyst Beast PRO", layout="wide", page_icon="🦁")

# --- 2. القائمة الجانبية واللوجو ---
with st.sidebar:
    # إظهار اللوجو 8888.jpg (تأكد من وجود الملف في GitHub)
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_container_width=True)
    
    st.markdown("<h3 style='text-align: center;'>Smart Analyst Beast</h3>", unsafe_allow_html=True)
    st.write("---")
    
    menu = {
        "🏠 مركز التحكم (رفع الملفات)": "Home",
        "📊 محرر الجداول (Excel Pro)": "Excel",
        "🧊 التحليل الثلاثي (3D)": "3D",
        "📈 لوحة البيانات (Dash)": "Dash"
    }
    choice = st.radio("القائمة العامة:", list(menu.keys()))
    
    st.write("---")
    if st.button("🚀 توليد 10,000 صف (اختبار تحمل)"):
        rows = 10000
        data = {
            'ID': range(1, rows + 1),
            'التاريخ': [datetime(2024, 1, 1) + timedelta(days=np.random.randint(0, 365)) for _ in range(rows)],
            'المنتج': [f"منتج_{np.random.randint(1, 100)}" for _ in range(rows)],
            'المبيعات': np.random.uniform(500, 50000, size=rows),
            'الكمية': np.random.randint(1, 50, size=rows),
            'الفرع': [np.random.choice(['القاهرة', 'دبي', 'الرياض', 'لندن']) for _ in range(rows)],
            'التقييم': np.random.randint(1, 6, size=rows)
        }
        st.session_state['public_vault'] = pd.DataFrame(data)
        st.success("تم شحن 10,000 صف!")
        st.rerun()

    st.caption("Developed by MIA8444")

# سحب البيانات الحالية
df = st.session_state['public_vault']

# --- 3. تشغيل الأدوات ---

if menu[choice] == "Home":
    st.title("🦁 بوابة التحكم - Smart Analyst Beast")
    st.write("مرحباً بك! ارفع ملف Excel أو CSV لبدء التحليل.")
    up = st.file_uploader("اختر ملفك", type=['xlsx', 'csv'])
    if up:
        st.session_state['public_vault'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
        st.success("تم تثبيت البيانات!")

elif menu[choice] == "Excel":
    st.header("📊 Excel Pro (المحرر الأبيض)")
    if df is not None:
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=15)
        gb.configure_default_column(editable=True, filterable=True)
        grid_res = AgGrid(df, gridOptions=gb.build(), theme='balham', height=500)
        if st.button("💾 حفظ التعديلات"):
            st.session_state['public_vault'] = pd.DataFrame(grid_res['data'])
            st.success("تم الحفظ!")
    else: st.warning("الخزنة فارغة.")

elif menu[choice] == "3D":
    st.header("🧊 تحليل البيانات ثلاثي الأبعاد")
    if df is not None:
        fig = px.scatter_3d(df, x='الكمية', y='المبيعات', z='التقييم', color='الفرع', 
                            title="تحليل شامل للعلاقات")
        st.plotly_chart(fig, use_container_width=True)
    else: st.error("ارفع بيانات أولاً.")

# --- التصحيح النهائي للـ NameError (الشرطتين __) ---
if __name__ == "__main__":
    pass
