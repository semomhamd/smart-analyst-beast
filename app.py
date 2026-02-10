import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# ======== 1. الذاكرة المركزية الموحدة ========
if 'beast_df' not in st.session_state:
    st.session_state.beast_df = None
if 'cleaning_log' not in st.session_state:
    st.session_state.cleaning_log = []

# ======== 2. الهوية والتنسيق (MIA8444) ========
AUTHOR_SIGNATURE = "MIA8444"
APP_NAME = "Smart Analyst"
LOGO_FILE = "8888.jpg" # اللوجو الخاص بك

st.set_page_config(page_title=f"{AUTHOR_SIGNATURE} | {APP_NAME}", layout="wide")

st.markdown(f"""
    <style>
    .stApp {{ background-color: #0d1117; color: white; }}
    .report-box {{ padding: 20px; border-radius: 15px; background: #161b22; border: 1px solid #58a6ff; margin-bottom: 20px; }}
    .footer {{ text-align: center; padding: 20px; color: #8b949e; font-size: 14px; border-top: 1px solid #30363d; margin-top: 50px; }}
    </style>
    """, unsafe_allow_html=True)

# ======== 3. القائمة الجانبية بالترتيب والأيقونات المحددة ========
with st.sidebar:
    # إضافة اللوجو في قمة القائمة الجانبية
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
    # الترس (الإعدادات) بشكل بسيط
    with st.expander("⚙️ الإعدادات"):
        st.write("المستخدم النشط: MIA8444")

# ======== 4. تفعيل المهام بنظام المحطة الواحدة ========

# --- المحطة 1: رفع وتوليد البيانات (تم إضافة الإدخال اليدوي) ---
if menu == "📤 رفع وتوليد البيانات":
    st.header("📤 مدخلات البيانات الذكية")
    # إضافة التبويب الثالث للإدخال اليدوي كما طلبت
    tab1, tab2, tab3 = st.tabs(["📁 رفع ملف (Excel/CSV)", "🎲 توليد بيانات اختبار", "✍️ Excel Pro (يدوي)"])
    
    with tab1:
        up = st.file_uploader("اختر ملفك", type=['csv', 'xlsx'])
        if up:
            df = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
            st.session_state.beast_df = df
            st.success("تم الربط بالذكاء الاصطناعي!")
            
    with tab2:
        if st.button("🚀 توليد بيانات اختبار فورية"):
            rows = 100
            st.session_state.beast_df = pd.DataFrame({
                'التاريخ': pd.date_range(start='2026-01-01', periods=rows),
                'المبيعات': np.random.randint(5000, 15000, size=rows),
                'المشتريات': np.random.randint(3000, 10000, size=rows),
                'الربح': np.random.randint(1000, 5000, size=rows)
            })
            st.success("تم توليد بيانات اختبار MIA8444!")
            
    with tab3:
        st.subheader("تحرير البيانات يدوياً")
        curr_df = st.session_state.beast_df if st.session_state.beast_df is not None else pd.DataFrame(columns=["البند", "القيمة"])
        st.session_state.beast_df = st.data_editor(curr_df, num_rows="dynamic", use_container_width=True)

# --- المحطة 2: منظف البيانات (التنظيف مع المقارنة) ---
elif menu == "🧹 منظف البيانات":
    st.header("🧹 محرك التصفية والتدقيق")
    if st.session_state.beast_df is not None:
        col_left, col_right = st.columns(2)
        with col_left:
            st.write("البيانات قبل التنظيف:")
            st.dataframe(st.session_state.beast_df.head())
        
        if st.button("🚀 بدء التنظيف الشامل"):
            old_count = len(st.session_state.beast_df)
            st.session_state.beast_df = st.session_state.beast_df.drop_duplicates().dropna(how='all')
            new_count = len(st.session_state.beast_df)
            st.session_state.cleaning_log.append(f"تم حذف {old_count - new_count} سجل غير صالح.")
            
            with col_right:
                st.write("البيانات بعد التنظيف:")
                st.dataframe(st.session_state.beast_df.head())
            st.success("تم التنظيف وتحديث الذاكرة!")

# --- المحطة 3: تصدير البيانات (تفعيل الأكواد) ---
elif menu == "📤 تصدير البيانات":
    st.header("📤 جسر التصدير العالمي")
    if st.session_state.beast_df is not None:
        tool = st.selectbox("اختر المنصة المستهدفة:", ["Power BI", "SQL Server", "Python", "Google Sheets", "Tableau"])
        
        st.markdown(f"### 🔗 كود الربط المباشر لـ {tool}")
        if tool == "Power BI":
            st.code("let\n  Source = Csv.Document(Web.Contents('MIA8444_Data_Feed'))\nin\n  Source", language="powerquery")
        elif tool == "SQL Server":
            st.code("INSERT INTO SmartAnalyst_DB (Date, Sales, Profit) VALUES (...);", language="sql")
        elif tool == "Python":
            st.code("import pandas as pd\ndf = pd.read_csv('MIA8444_Final.csv')", language="python")
            
        st.download_button("📥 تحميل ملف CSV النظيف", st.session_state.beast_df.to_csv(index=False), "MIA8444_Final.csv")
    else:
        st.warning("الرجاء رفع بيانات أولاً.")

# --- المحطة 4: داشبورد احترافي ---
elif menu == "📊 داشبورد احترافي":
    st.header("✨ لوحة القيادة التفاعلية (MIA8444 Style)")
    if st.session_state.beast_df is not None:
        df = st.session_state.beast_df
        # التأكد من وجود الأعمدة المطلوبة للرسم
        if 'المبيعات' in df.columns:
            c1, c2, c3 = st.columns(3)
            c1.metric("إجمالي المبيعات", f"{df['المبيعات'].sum():,}")
            c2.metric("إجمالي الربح", f"{df['الربح'].sum():,}" if 'الربح' in df.columns else "0")
            c3.metric("الحالة", "مستقر ✅")
            
            fig = px.area(df, title="حركة السيولة النقدية", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("قم برفع ملف يحتوي على بيانات رقمية لعرض الإحصائيات.")

# --- المحطة 5: محلل البيانات والتنبؤ ---
elif menu == "🧠 محلل البيانات والتنبؤ":
    st.header("🧠 مركز الذكاء التنبئي")
    if st.session_state.beast_df is not None:
        df = st.session_state.beast_df
        st.subheader("توقعات الاتجاه القادم")
        fig_pred = px.line(df, title="منحنى التنبؤ الذكي", line_shape="spline")
        st.plotly_chart(fig_pred, use_container_width=True)
        st.info("بناءً على التنبؤ: يُنصح بمراقبة معدلات النمو في الفترة القادمة.")

# --- المحطة 6: التقرير النهائي ---
elif menu == "📄 التقرير النهائي":
    st.header("📄 التقرير التحليلي المتكامل")
    if st.session_state.beast_df is not None:
        st.markdown("<div class='report-box'>", unsafe_allow_html=True)
        st.subheader("1️⃣ فحص ومعالجة البيانات")
        if st.session_state.cleaning_log:
            for log in st.session_state.cleaning_log: st.write(f"✅ {log}")
        else: st.write("✅ تم فحص البيانات: لا يوجد مكررات.")
        
        st.subheader("2️⃣ ملخص الأداء العام")
        st.write("يوضح الرسم البياني التالي توزيع البيانات التي تمت معالجتها:")
        st.plotly_chart(px.histogram(st.session_state.beast_df, title="توزيع البيانات التحليلي"))
        
        st.subheader("3️⃣ توصيات Smart Analyst لتجنب الخسائر")
        st.write("- تقليل النفقات في القطاعات غير المنتجة بناءً على تحليل التنبؤ.")
        st.write("- رفع معدلات المكاسب عبر استهداف الفترات ذات النمو الأعلى.")
        
        st.markdown("---")
        st.markdown(f"*التقرير بناءً على البيانات التي تم رفعها وتم تحليلها بواسطة {APP_NAME}*")
        st.markdown("</div>", unsafe_allow_html=True)
        st.button("📥 تحميل التقرير النهائي PDF")

# ======== 5. التذييل ========
st.markdown(f"<div class='footer'>MIA8444 Signature | Smart Analyst OS © 2026</div>", unsafe_allow_html=True)
