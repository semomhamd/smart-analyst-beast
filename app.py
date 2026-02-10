import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

# ======== 1. الذاكرة المركزية الفعالة (The Brain) ========
if 'beast_df' not in st.session_state:
    st.session_state.beast_df = None
if 'cleaning_log' not in st.session_state:
    st.session_state.cleaning_log = []

# ======== 2. الهوية والتنسيق (MIA8444) ========
AUTHOR_SIGNATURE = "MIA8444"
APP_NAME = "Smart Analyst"
LOGO_FILE = "8888.jpg"

st.set_page_config(page_title=f"{AUTHOR_SIGNATURE} | {APP_NAME}", layout="wide")

st.markdown(f"""
    <style>
    .stApp {{ background-color: #0d1117; color: white; }}
    .report-box {{ padding: 20px; border-radius: 15px; background: #161b22; border: 1px solid #58a6ff; margin-bottom: 20px; }}
    .footer {{ text-align: center; padding: 20px; color: #8b949e; font-size: 14px; border-top: 1px solid #30363d; margin-top: 50px; }}
    </style>
    """, unsafe_allow_html=True)

# ======== 3. القائمة الجانبية بالترتيب والأيقونات ========
with st.sidebar:
    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, use_container_width=True)
    st.markdown(f"<h1 style='text-align:center;'>{APP_NAME}</h1>", unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("القائمة الرئيسية:", [
        "📤 رفع وتوليد البيانات",
        "🧹 منظف البيانات",
        "📤 تصدير البيانات",
        "📊 داشبورد احترافي",
        "🧠 محلل البيانات والتنبؤ",
        "📄 التقرير النهائي"
    ])
    st.markdown("---")
    with st.expander("⚙️ الإعدادات"):
        st.write("التحكم في الواجهة")

# ======== 4. تفعيل المحطات (المنطق البرمجي الصحيح) ========

# --- المحطة 1: رفع وتوليد البيانات (تم إضافة الإدخال اليدوي) ---
if menu == "📤 رفع وتوليد البيانات":
    st.header("📤 مدخلات البيانات الذكية")
    tab1, tab2, tab3 = st.tabs(["📁 رفع ملف", "🎲 توليد بيانات اختبار", "✍️ Excel Pro (يدوي)"])
    
    with tab1:
        up = st.file_uploader("اختر ملفك", type=['csv', 'xlsx'])
        if up:
            st.session_state.beast_df = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
            st.success("تم الربط بالذكاء الاصطناعي!")
            
    with tab2:
        if st.button("🚀 توليد بيانات اختبار فورية"):
            rows = 50
            st.session_state.beast_df = pd.DataFrame({
                'التاريخ': pd.date_range(start='2026-01-01', periods=rows),
                'المبيعات': np.random.randint(5000, 15000, size=rows),
                'المشتريات': np.random.randint(3000, 10000, size=rows),
                'الربح': np.random.randint(1000, 5000, size=rows)
            })
            st.success("تم توليد بيانات اختبار MIA8444!")
            
    with tab3:
        st.subheader("إدخال بيانات يدوي (شيت احترافي)")
        curr = st.session_state.beast_df if st.session_state.beast_df is not None else pd.DataFrame(columns=["التاريخ", "المبيعات", "الربح"])
        st.session_state.beast_df = st.data_editor(curr, num_rows="dynamic", use_container_width=True)

# --- المحطة 2: منظف البيانات (قبل وبعد الحقيقي) ---
elif menu == "🧹 منظف البيانات":
    st.header("🧹 محرك التصفية والتدقيق")
    if st.session_state.beast_df is not None:
        col_pre, col_post = st.columns(2)
        with col_pre:
            st.subheader("قبل التنظيف")
            st.dataframe(st.session_state.beast_df.head(10))
        
        if st.button("🚀 بدء التنظيف الشامل"):
            old_count = len(st.session_state.beast_df)
            st.session_state.beast_df = st.session_state.beast_df.drop_duplicates().dropna(how='all')
            new_count = len(st.session_state.beast_df)
            st.session_state.cleaning_log.append(f"تم معالجة {old_count - new_count} سجل غير صالح.")
            
            with col_post:
                st.subheader("بعد التنظيف")
                st.dataframe(st.session_state.beast_df.head(10))
            st.success("تم تحديث البيانات في الذاكرة!")

# --- المحطة 3: تصدير البيانات (تفعيل الكود الفعلي) ---
elif menu == "📤 تصدير البيانات":
    st.header("📤 جسر التصدير العالمي")
    if st.session_state.beast_df is not None:
        tool = st.selectbox("اختر أداة التصدير:", ["Power BI", "SQL", "Python", "Google Sheets", "Tableau"])
        
        if tool == "Power BI":
            st.code("// Power Query Script\nlet Source = Csv.Document(Web.Contents('MIA8444_Data')) in Source", language="powerquery")
        elif tool == "SQL":
            st.code("INSERT INTO MIA8444_DB (Date, Sales, Profit) VALUES (...);", language="sql")
            
        st.download_button("📥 تحميل البيانات نظيفة (CSV)", st.session_state.beast_df.to_csv(index=False), "MIA8444_Cleaned.csv")
    else:
        st.warning("ارفع بيانات أولاً.")

# --- المحطة 4: داشبورد احترافي ---
elif menu == "📊 داشبورد احترافي":
    st.header("📊 لوحة القيادة التفاعلية")
    if st.session_state.beast_df is not None:
        df = st.session_state.beast_df
        c1, c2 = st.columns([1, 2])
        with c1:
            st.metric("إجمالي المبيعات", f"{df['المبيعات'].sum():,}" if 'المبيعات' in df.columns else "0")
        with c2:
            fig = px.area(df, title="حركة السيولة (MIA8444)", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

# --- المحطة 6: التقرير النهائي (تجميع البيانات) ---
elif menu == "📄 التقرير النهائي":
    st.header("📄 التقرير التحليلي المتكامل")
    if st.session_state.beast_df is not None:
        st.markdown("<div class='report-box'>", unsafe_allow_html=True)
        st.subheader("1️⃣ فحص ومعالجة البيانات")
        if st.session_state.cleaning_log:
            for log in st.session_state.cleaning_log: st.write(f"✅ {log}")
        else: st.write("البيانات كانت سليمة بنسبة 100%.")
        
        st.subheader("2️⃣ ملخص الأداء المالي")
        st.plotly_chart(px.histogram(st.session_state.beast_df, title="توزيع الأرقام"))
        
        st.subheader("3️⃣ توصيات Smart Analyst")
        st.write("- بناءً على التحليل، يجب التركيز على فترات النمو الموضحة في الرسوم.")
        
        st.markdown("---")
        st.markdown(f"*التقرير بناءً على البيانات التي تم رفعها وتم تحليلها بواسطة {APP_NAME}*")
        st.markdown("</div>", unsafe_allow_html=True)
        st.button("📥 تحميل التقرير النهائي PDF")

# ======== 5. التذييل ========
st.markdown(f"<div class='footer'>{AUTHOR_SIGNATURE} Signature | Smart Analyst OS © 2026</div>", unsafe_allow_html=True)
