import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
from io import BytesIO

# 1. إعدادات الهوية الفخمة (MIA8444)
st.set_page_config(page_title="Smart Analyst Beast PRO", layout="wide", page_icon="🦁")

# لمسة CSS احترافية لتنسيق الألوان وتوسيط اللوجو
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    [data-testid="stSidebar"] { background-color: #161b22; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; border-left: 5px solid #3b82f6; }
    div.stButton > button:first-child { background-color: #3b82f6; color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. مخزن البيانات الأساسي
if 'main_df' not in st.session_state:
    st.session_state['main_df'] = pd.DataFrame()

df = st.session_state['main_df']

# --- السايد بار (مركز التحكم الإمبراطوري) ---
with st.sidebar:
    # اللوجو منور الدنيا فوق خالص
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_container_width=True)
    
    st.markdown("<h2 style='text-align: center; color: white;'>Smart Analyst Beast</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>Signature: MIA8444</p>", unsafe_allow_html=True)
    st.write("---")
    
    # القائمة المرتبة بأيقونات طبيعية ومنظمة
    st.markdown("### 🛠️ القائمة التنفيذية")
    menu = {
        "🏠 الرئيسية وتوليد الاختبار": "الرئيسية",
        "📸 الرؤية الذكية (OCR)": "OCR",
        "🧼 منظف البيانات الذكي": "Clean",
        "📊 محرر الاكسل (Pro)": "Excel",
        "🧠 المحلل الذكي": "Analysis",
        "📈 التنبؤ المالي (AI)": "Forecast",
        "🖥️ داشبورد الإدارة": "Dashboard",
        "📄 تقرير PDF النهائي": "PDF"
    }
    
    # استخدام Radio button بشكل شيك كأنه Menu
    choice = st.radio("انتقل بين الأدوات بدقة:", list(menu.keys()))
    
    st.write("---")
    # حالة النظام (Active) بدون أي جمل إضافية
    st.success("System Status: Active 🟢")
    st.caption("Smart Analyst thinks for you")

# --- محتوى الأدوات المربوطة ---

# 1. الرئيسية
if choice == "🏠 الرئيسية وتوليد الاختبار":
    st.header("🏠 بوابة التحكم الرئيسية")
    col1, col2 = st.columns(2)
    with col1:
        up = st.file_uploader("ارفع ملف البيانات (Excel/CSV)", type=['csv', 'xlsx'])
        if up:
            st.session_state['main_df'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
            st.success("تم الشحن بنجاح!")
    with col2:
        if st.button("🧬 توليد بيانات اختبار (Beast Sample)"):
            test_data = pd.DataFrame({
                'التاريخ': pd.date_range(start='2025-01-01', periods=100),
                'المنتج': np.random.choice(['موبايل', 'ساعة', 'لابتوب', 'سماعة'], 100),
                'المبيعات': np.random.randint(500, 10000, 100),
                'التكلفة': np.random.randint(300, 8000, 100)
            })
            st.session_state['main_df'] = test_data
            st.rerun()

# 2. الرؤية الذكية
elif choice == "📸 الرؤية الذكية (OCR)":
    st.header("📸 محرك الرؤية الذكي (AI Vision)")
    cam = st.camera_input("التقط صورة للجدول")
    if cam: st.info("جاري استخراج البيانات بذكاء MIA8444...")

# 3. المنظف
elif choice == "🧼 منظف البيانات الذكي":
    st.header("🧼 وحدة تنظيف البيانات")
    if not df.empty:
        if st.button("🚀 تنظيف عميق ومعالجة القيم"):
            st.session_state['main_df'] = df.drop_duplicates().fillna(0)
            st.success("البيانات الآن نظيفة تماماً!")
    else: st.warning("ارفع بياناتك أولاً.")

# 4. محرر الإكسل (SnaAyas)
elif choice == "📊 محرر الاكسل (Pro)":
    st.header("📊 محرر الجداول المطور (SnaAyas)")
    if not df.empty:
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        if st.button("💾 حفظ التعديلات"):
            st.session_state['main_df'] = edited_df
            st.success("تم الحفظ في ذاكرة الوحش.")
    else: st.warning("لا توجد بيانات للعرض.")

# 5. المحلل
elif choice == "🧠 المحلل الذكي":
    st.header("🧠 ذكاء MIA8444 في التحليل")
    if not df.empty:
        st.write("🔍 *الوصف الإحصائي:*")
        st.table(df.describe())

# 6. التنبؤ
elif choice == "📈 التنبؤ المالي (AI)":
    st.header("📈 التنبؤ بمستقبل المبيعات")
    if not df.empty and 'المبيعات' in df.columns:
        y = df['المبيعات'].values
        future = np.poly1d(np.polyfit(np.arange(len(y)), y, 1))(np.arange(len(y), len(y) + 10))
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=y, name="الحالي", line=dict(color='#3b82f6')))
        fig.add_trace(go.Scatter(y=future, name="التنبؤ", line=dict(dash='dash', color='red')))
        st.plotly_chart(fig, use_container_width=True)

# 7. الداشبورد (High-Level)
elif choice == "🖥️ داشبورد الإدارة":
    st.header("🖥️ Dashboard Performance (MIA8444)")
    if not df.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("إجمالي المبيعات", f"{df['المبيعات'].sum():,}")
        c2.metric("عدد العمليات", len(df))
        c3.metric("المتوسط", f"{df['المبيعات'].mean():.2f}")
        
        ca, cb = st.columns(2)
        with ca:
            st.plotly_chart(px.pie(df, names='المنتج', values='المبيعات', hole=0.4, title="توزيع المبيعات"), use_container_width=True)
        with cb:
            st.plotly_chart(px.bar(df, x='المنتج', y='المبيعات', color='المنتج', title="أداء المنتجات"), use_container_width=True)

# 8. PDF
elif choice == "📄 تقرير PDF النهائي":
    st.header("📄 تصدير التقرير النهائي")
    st.button("📥 تحميل التقرير (MIA8444_Report.pdf)")

st.write("---")
st.markdown("<center>Smart Analyst Beast | Powered by MIA8444</center>", unsafe_allow_html=True)
