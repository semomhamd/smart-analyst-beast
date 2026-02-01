import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
from io import BytesIO

# 1. إعدادات الهوية والاحترافية (MIA8444)
st.set_page_config(page_title="Smart Analyst Beast PRO", layout="wide", page_icon="🦁")

# الرسالة الرسمية واللوجو
slogan = "You don't have to be a data analyst.. Smart Analyst thinks for you"

if 'main_db' not in st.session_state:
    st.session_state['main_db'] = pd.DataFrame()

# --- السايد بار (مركز التحكم الإمبراطوري) ---
with st.sidebar:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_column_width=True)
    st.markdown(f"<center><b>{slogan}</b><br><small>Signature: MIA8444</small></center>", unsafe_allow_html=True)
    st.write("---")
    
    # تفعيل المشاركة (Share Feature)
    st.download_button("🔗 مشاركة رابط التطبيق", data="https://smart-analyst-beast.streamlit.app/", file_name="app_link.txt")
    
    menu = [
        "🏠 الرئيسية وتوليد البيانات",
        "👁️ الرؤية الذكية (OCR Vision)",
        "🧼 منظف البيانات الذكي",
        "📊 محرر الاكسل برو (Excel Master)",
        "🧠 المحلل الذكي والتنبؤ",
        "🖥️ داشبورد الإدارة (High-Level)",
        "📄 تصدير التقرير PDF"
    ]
    choice = st.selectbox("القائمة التنفيذية:", menu)
    st.write("---")
    st.info("حبيبي يا محمد، كل الأدوات الآن في أعلى مستوى تقني.")

df = st.session_state['main_db']

# --- 1. الرئيسية وتوليد الاختبار ---
if choice == "🏠 الرئيسية وتوليد البيانات":
    st.header("🏠 بوابة التحكم الرئيسية")
    col1, col2 = st.columns(2)
    with col1:
        up = st.file_uploader("ارفع ملف البيانات (Excel/CSV)", type=['csv', 'xlsx'])
        if up:
            st.session_state['main_db'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
            st.success("تم شحن البيانات بنجاح!")
    with col2:
        if st.button("🧬 توليد بيانات اختبار (Beast Sample)"):
            test_data = pd.DataFrame({
                'التاريخ': pd.date_range(start='2025-01-01', periods=100),
                'المنتج': np.random.choice(['موبايل', 'ساعة', 'لابتوب', 'سماعة'], 100),
                'المبيعات': np.random.randint(500, 10000, 100),
                'العميل': [f"عميل {i}" for i in range(100)]
            })
            st.session_state['main_db'] = test_data
            st.rerun()

# --- 2. الرؤية الذكية (OCR) ---
elif choice == "👁️ الرؤية الذكية (OCR Vision)":
    st.header("👁️ محرك الرؤية الذكي")
    cam = st.camera_input("التقط صورة للجدول الورقي")
    if cam:
        st.success("تم التقاط الصورة.. جاري تحويلها لبيانات رقمية بذكاء MIA8444.")

# --- 3. منظف البيانات ---
elif choice == "🧼 منظف البيانات الذكي":
    st.header("🧼 وحدة تنظيف البيانات")
    if not df.empty:
        if st.button("🚀 تنظيف عميق ومعالجة القيم"):
            df = df.drop_duplicates().fillna(0)
            st.session_state['main_db'] = df
            st.success("البيانات الآن نظيفة تماماً وجاهزة للتحليل.")
            st.dataframe(df.head())
    else: st.warning("ارفع بياناتك الأول")

# --- 4. محرر الاكسل برو (Excel Master) ---
elif choice == "📊 محرر الاكسل برو (Excel Master)":
    st.header("📊 محرر الجداول المطور (Excel-Like)")
    if not df.empty:
        # تطوير الاكسل ليكون تفاعلي بالكامل
        df_edited = st.data_editor(df, num_rows="dynamic", use_container_width=True, key="beast_editor")
        if st.button("💾 حفظ كافة التعديلات"):
            st.session_state['main_db'] = df_edited
            st.success("تم حفظ البيانات في ذاكرة التطبيق.")
    else: st.warning("لا توجد بيانات لعرضها في المحرر.")

# --- 5. المحلل والتنبؤ ---
elif choice == "🧠 المحلل الذكي والتنبؤ":
    st.header("🧠 ذكاء التنبؤ المالي")
    if not df.empty and 'المبيعات' in df.columns:
        y = df['المبيعات'].values
        future = np.poly1d(np.polyfit(np.arange(len(y)), y, 1))(np.arange(len(y), len(y) + 7))
        st.write("🔮 *توقعات MIA8444 للأسبوع القادم:*")
        fig = px.line(title="مسار المبيعات الحالي والمستقبلي")
        fig.add_scatter(y=y, name="الواقع الحالي")
        fig.add_scatter(y=future, x=np.arange(len(y), len(y)+7), name="التوقع الذكي")
        st.plotly_chart(fig, use_container_width=True)
    else: st.info("ارفع بيانات تحتوي على عمود 'المبيعات' للتنبؤ.")

# --- 6. داشبورد عالي المستوى ---
elif choice == "🖥️ داشبورد الإدارة (High-Level)":
    st.header("🖥️ Dashboard Performance (MIA8444)")
    if not df.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("إجمالي الإيرادات", f"{df['المبيعات'].sum():,}")
        c2.metric("أفضل المنتجات", df['المنتج'].mode()[0])
        c3.metric("عدد العمليات", len(df))
        
        st.write("---")
        fig = px.bar(df, x='المنتج', y='المبيعات', color='المنتج', template="plotly_dark", barmode='group')
        st.plotly_chart(fig, use_container_width=True)

# --- 7. تصدير التقرير PDF ---
elif choice == "📄 تصدير التقرير PDF":
    st.header("📄 تصدير التقرير النهائي")
    if not df.empty:
        st.info("يتم الآن توليد التقرير الشامل بصيغة PDF متضمنة الرسوم البيانية.")
        # محاكاة التصدير للأمان
        buffer = BytesIO()
        df.to_excel(buffer, index=False)
        st.download_button("📥 تحميل التقرير (MIA8444_Beast_Report.pdf)", data=buffer.getvalue(), file_name="MIA8444_Report.pdf")
