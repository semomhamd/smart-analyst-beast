import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

# ======== 1. الذاكرة والتعريفات ========
if 'beast_df' not in st.session_state:
    st.session_state.beast_df = None
if 'cleaning_log' not in st.session_state:
    st.session_state.cleaning_log = []

AUTHOR_SIGNATURE = "MIA8444"
LOGO_FILE = "8888.jpg"

st.set_page_config(page_title=f"{AUTHOR_SIGNATURE} | Smart Analyst", layout="wide")

# ======== 2. التنسيق البصري (MIA8444 Style) ========
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: white; }
    .report-card { padding: 20px; border-radius: 15px; background: #161b22; border: 1px solid #58a6ff; }
    .footer { text-align: center; color: #8b949e; margin-top: 50px; font-size: 13px; }
    </style>
    """, unsafe_allow_html=True)

# ======== 3. القائمة الجانبية ========
with st.sidebar:
    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, use_container_width=True)
    st.markdown("<h2 style='text-align:center;'>Smart Analyst</h2>", unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("القائمة الرئيسية:", [
        "📤 ورشة البيانات (رفع وتوليد)",
        "🧹 منظف البيانات العالمي",
        "📤 جسر التصدير العالمي",
        "📊 داشبورد احترافي",
        "🧠 AI محرك التنبؤ",
        "📄 التقرير النهائي"
    ])
    st.markdown("---")
    st.info(f"المستخدم: {AUTHOR_SIGNATURE}")

# ======== 4. المحطات التشغيلية ========

# المحطة 1: ورشة البيانات
if menu == "📤 ورشة البيانات (رفع وتوليد)":
    st.header("📤 (Data Hub) ورشة عمل البيانات")
    t1, t2, t3 = st.tabs(["📁 رفع ملفات", "🎲 توليد بيانات اختبار", "✍️ Excel Pro (إدخال يدوي)"])
    with t1:
        up = st.file_uploader("اربط ملفك (Excel/CSV)", type=['csv', 'xlsx'])
        if up:
            st.session_state.beast_df = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
            st.success("تم رفع البيانات بنجاح!")
    with t2:
        if st.button("🚀 توليد بيانات اختبار فورية"):
            st.session_state.beast_df = pd.DataFrame({
                'Date': pd.date_range(start='2025-01-01', periods=50),
                'Sales': np.random.randint(1000, 5000, 50),
                'Costs': np.random.randint(500, 3000, 50),
                'Region': np.random.choice(['Dubai', 'Riyadh', 'Cairo'], 50)
            })
            st.success("تم توليد بيانات MIA8444 الاختبارية!")
    with t3:
        curr = st.session_state.beast_df if st.session_state.beast_df is not None else pd.DataFrame(columns=["البند", "القيمة"])
        st.session_state.beast_df = st.data_editor(curr, num_rows="dynamic", use_container_width=True)

# المحطة 2: منظف البيانات (تم إصلاح SyntaxError)
elif menu == "🧹 منظف البيانات العالمي":
    st.header("🧹 (Beast Cleaner) محرك التنظيف")
    if st.session_state.beast_df is not None:
        st.subheader("البيانات الحالية:")
        st.dataframe(st.session_state.beast_df.head())
        if st.button("🚀 تشغيل التنظيف التلقائي"):
            old = len(st.session_state.beast_df)
            st.session_state.beast_df = st.session_state.beast_df.drop_duplicates()
            st.session_state.cleaning_log.append(f"تم حذف {old - len(st.session_state.beast_df)} سجل مكرر")
            st.success("تم التنظيف وتحديث الذاكرة بنجاح!") # تم إصلاح الخطأ هنا
    else:
        st.warning("ارفع ملف أولاً!")

# المحطة 3: جسر التصدير
elif menu == "📤 جسر التصدير العالمي":
    st.header("📤 جسر التصدير العالمي")
    if st.session_state.beast_df is not None:
        tool = st.selectbox("اختر أداة التصدير:", ["Power BI", "SQL", "Python", "Tableau"])
        if tool == "Power BI":
            st.code("let Source = Csv.Document(Web.Contents('MIA8444_Data')) in Source", language="powerquery")
        elif tool == "SQL":
            st.code("INSERT INTO MIA8444_DB (Date, Sales) VALUES (...);", language="sql")
        st.download_button("📥 (CSV) تحميل البيانات نظيفة", st.session_state.beast_df.to_csv(index=False), "MIA8444_Final.csv")
    else:
        st.error("لا توجد بيانات للتصدير.")

# المحطة 4: داشبورد احترافي (تم إصلاح ValueError الخاص بالأعمدة)
elif menu == "📊 داشبورد احترافي":
    st.header("📊 لوحة القيادة التفاعلية")
    if st.session_state.beast_df is not None:
        df = st.session_state.beast_df
        nums = df.select_dtypes(include=[np.number]).columns.tolist()
        if nums:
            st.metric("إجمالي القيم الرقمية", f"{df[nums[0]].sum():,}")
            # حماية الرسم البياني من الأعمدة غير الموجودة
            fig = px.line(df, title=f"تحليل الاتجاه لـ {nums[0]}", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("البيانات المرفوعة لا تحتوي على أعمدة رقمية للرسم!")
    else:
        st.warning("ارفع بياناتك أولاً يا بطل.")

# المحطة 6: التقرير النهائي (تم إصلاح ValueError للهيستوجرام)
elif menu == "📄 التقرير النهائي":
    st.header("📄 التقرير التحليلي المتكامل")
    if st.session_state.beast_df is not None:
        st.markdown("<div class='report-card'>", unsafe_allow_html=True)
        st.subheader("🛠️ سجل العمليات")
        for log in st.session_state.cleaning_log: st.write(f"✅ {log}")
        
        # التأكد من وجود بيانات للرسم
        nums = st.session_state.beast_df.select_dtypes(include=[np.number]).columns.tolist()
        if nums:
            fig = px.histogram(st.session_state.beast_df, x=nums[0], title="توزيع البيانات")
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.write(f"تم التحليل بواسطة Smart Analyst - توقيع: {AUTHOR_SIGNATURE}")
        st.markdown("</div>", unsafe_allow_html=True)
        st.button("📥 تحميل التقرير PDF")

# ======== تذييل ========
st.markdown(f"<div class='footer'>Property of {AUTHOR_SIGNATURE} | Smart Analyst OS © 2026</div>", unsafe_allow_html=True)
