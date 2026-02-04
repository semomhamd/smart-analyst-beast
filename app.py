import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
from datetime import datetime, timedelta
from st_aggrid import AgGrid, GridOptionsBuilder

# --- 1. ذاكرة التطبيق (لحفظ بيانات المستخدمين أثناء الجلسة) ---
if 'main_data' not in st.session_state:
    st.session_state['main_data'] = None

st.set_page_config(page_title="Smart Analyst Beast", layout="wide", page_icon="🦁")

# --- 2. الواجهة الجانبية العامة ---
with st.sidebar:
    # عرض شعار التطبيق العام
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_container_width=True)
    
    st.markdown("<h2 style='text-align: center;'>Smart Analyst Beast</h2>", unsafe_allow_html=True)
    st.write("---")
    
    menu = {
        "🏠 الرئيسية (رفع البيانات)": "Home",
        "📊 محرر الجداول (Excel Pro)": "Excel",
        "📈 لوحة البيانات (Dashboard)": "Dash",
        "🧊 التحليل ثلاثي الأبعاد": "3D",
        "🧼 أدوات التنظيف الذكي": "Clean",
        "👁️ قارئ الصور (OCR)": "OCR"
    }
    choice = st.radio("اختر الأداة المطلوبة:", list(menu.keys()))
    
    st.write("---")
    # ميزة تجريبية للجمهور لاختبار التطبيق ببيانات ضخمة
    if st.button("🚀 توليد بيانات اختبار (10,000 صف)"):
        rows = 10000
        dates = [datetime(2023, 1, 1) + timedelta(days=np.random.randint(0, 1000)) for _ in range(rows)]
        data = {
            'ID': range(1, rows + 1),
            'التاريخ': dates,
            'المنتج': [f"منتج_{np.random.randint(1, 50)}" for _ in range(rows)],
            'المبيعات': np.random.uniform(500, 100000, size=rows),
            'الكمية': np.random.randint(1, 20, size=rows),
            'الفرع': [np.random.choice(['القاهرة', 'دبي', 'الرياض', 'لندن']) for _ in range(rows)],
            'التقييم': np.random.randint(1, 6, size=rows)
        }
        st.session_state['main_data'] = pd.DataFrame(data)
        st.success("تم إنشاء بيانات افتراضية للاختبار!")
        st.rerun()

    st.caption("Powered by Smart Analyst Beast • MIA8444")

# سحب البيانات الحالية من الجلسة
df = st.session_state['main_data']

# --- 3. محرك الأدوات ---

if menu[choice] == "Home":
    st.title("🦁 مرحباً بك في Smart Analyst Beast")
    st.markdown("قم برفع ملفاتك (Excel أو CSV) لتبدأ التحليل الذكي.")
    
    uploaded_file = st.file_uploader("اختر ملف البيانات", type=['xlsx', 'csv', 'xls'])
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('csv'):
                st.session_state['main_data'] = pd.read_csv(uploaded_file)
            else:
                st.session_state['main_data'] = pd.read_excel(uploaded_file)
            st.success("تم رفع البيانات ومعالجتها بنجاح!")
        except Exception as e:
            st.error(f"عذراً، حدث خطأ أثناء الرفع: {e}")

elif menu[choice] == "Excel":
    st.header("📊 المحرر الاحترافي (Excel Pro)")
    if df is not None:
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=15)
        gb.configure_default_column(editable=True, filterable=True, sortable=True)
        grid_res = AgGrid(df, gridOptions=gb.build(), theme='balham', height=500)
        
        if st.button("💾 حفظ التعديلات"):
            st.session_state['main_data'] = pd.DataFrame(grid_res['data'])
            st.success("تم حفظ التعديلات في جلسة العمل الحالية.")
    else:
        st.info("الرجاء رفع ملف بيانات أو استخدام 'بيانات الاختبار' من القائمة الجانبية.")

elif menu[choice] == "3D":
    st.header("🧊 التحليل المتطور ثلاثي الأبعاد")
    if df is not None:
        st.write("رسم بياني تفاعلي يحلل العلاقة بين المبيعات، الكمية، والتقييم.")
        fig = px.scatter_3d(df, x='الكمية', y='المبيعات', z='التقييم',
                            color='الفرع', opacity=0.7, height=700,
                            title="تحليل شامل للأداء")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("لا توجد بيانات متاحة للرسم البياني.")

elif menu[choice] == "Dash":
    st.header("📈 لوحة مراقبة الأداء")
    if df is not None:
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("إجمالي المبيعات", f"{df['المبيعات'].sum():,.0f}")
        with c2: st.metric("عدد العمليات", len(df))
        with c3: st.metric("متوسط التقييم", f"{df['التقييم'].mean():.2f}")
        
        st.write("---")
        st.subheader("تحليل المبيعات حسب المنطقة")
        st.bar_chart(df['الفرع'].value_counts())
    else:
        st.info("بانتظار رفع البيانات...")

# ضمان تشغيل التطبيق بشكل سليم
if __name__ == "__main__":
    pass
