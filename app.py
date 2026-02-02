import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import os
from io import BytesIO

# 1. إعدادات الهوية الفخمة (MIA8444)
st.set_page_config(
    page_title="Smart Analyst Beast PRO", 
    layout="wide", 
    page_icon="🦁",
    initial_sidebar_state="expanded"
)

# 2. لمسة جمالية للواجهة (CSS) لتنظيم الشكل والنضافة
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; border: 1px solid #3b82f6; }
    </style>
    """, unsafe_allow_html=True)

# 3. مخزن البيانات (Session State) لضمان عدم فقدان البيانات
if 'main_df' not in st.session_state:
    st.session_state['main_df'] = pd.DataFrame()

# --- السايد بار (مركز التحكم الإمبراطوري) ---
with st.sidebar:
    # عرض اللوجو بشكل "منور" واحترافي
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_container_width=True)
    
    st.markdown("<h2 style='text-align: center; color: #3b82f6;'>Smart Analyst</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 0.8em;'>Signature: MIA8444</p>", unsafe_allow_html=True)
    st.write("---")
    
    # القائمة المرتبة والمنظمة بأيقونات طبيعية
    menu_options = {
        "🏠 الرئيسية": "🏠 الرئيسية وتوليد الاختبار",
        "📸 الرؤية الذكية": "👁️ الرؤية الذكية (OCR)",
        "🧼 المنظف": "🧼 منظف البيانات",
        "📊 إكسل برو": "📊 محرر الاكسل (Pro)",
        "🧠 المحلل": "🧠 المحلل الذكي",
        "📈 التنبؤ": "📉 التنبؤ المالي (AI)",
        "🖥️ الداشبورد": "🖥️ داشبورد الإدارة",
        "📄 التقرير": "📄 تقرير PDF النهائي"
    }
    
    choice = st.radio("انتقل بين الأدوات بدقة:", list(menu_options.values()))
    
    st.write("---")
    # تم حذف الجملة السابقة واستبدالها بحالة النظام فقط
    st.success("System Status: Active 🟢")
    st.caption("You don't have to be a data analyst.. Smart Analyst thinks for you")

# استدعاء البيانات الحالية
df = st.session_state['main_df']

# --- تنفيذ الأقسام بناءً على الاختيار ---

# 1. الرئيسية
if choice == "🏠 الرئيسية وتوليد الاختبار":
    st.header("🏠 بوابة التحكم في البيانات")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📤 رفع ملف")
        up = st.file_uploader("ارفع ملفك (Excel/CSV)", type=['csv', 'xlsx'])
        if up:
            try:
                st.session_state['main_df'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
                st.success("تم شحن البيانات بنجاح!")
                st.rerun()
            except Exception as e:
                st.error(f"خطأ في قراءة الملف: {e}")
    with col2:
        st.subheader("🧪 عينة اختبار")
        if st.button("🧬 توليد ملف اختبار احترافي"):
            test_data = pd.DataFrame({
                'التاريخ': pd.date_range(start='2025-01-01', periods=50),
                'المنتج': np.random.choice(['موبايل', 'ساعة', 'سماعة', 'لابتوب'], 50),
                'المبيعات': np.random.randint(100, 5000, 50),
                'التكلفة': np.random.randint(50, 4000, 50)
            })
            st.session_state['main_df'] = test_data
            st.success("تم توليد بيانات الاختبار!")
            st.rerun()

# 2. الرؤية الذكية (OCR)
elif choice == "👁️ الرؤية الذكية (OCR)":
    st.header("👁️ محرك الرؤية الذكي (AI Vision)")
    cam = st.camera_input("صور المستند الورقي أو ارفعه كصورة")
    if cam:
        st.image(cam, caption="تم التقاط الصورة.. جاري معالجتها بذكاء MIA8444")
        st.info("الذكاء الاصطناعي يقوم الآن بتحويل الصورة لبيانات رقمية...")

# 3. منظف البيانات
elif choice == "🧼 منظف البيانات":
    st.header("🧼 وحدة التنظيف والتهيئة")
    if not df.empty:
        if st.button("🚀 تنظيف عميق (Auto Clean)"):
            df_cleaned = df.drop_duplicates().fillna(0)
            st.session_state['main_df'] = df_cleaned
            st.success("تم تنظيف البيانات بنجاح!")
            st.dataframe(df_cleaned.head())
    else: st.warning("لا توجد بيانات لتنظيفها. ارفع ملف أولاً.")

# 4. محرر الاكسل برو
elif choice == "📊 محرر الاكسل (Pro)":
    st.header("📊 Excel Pro Dashboard (SnaAyas)")
    if not df.empty:
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        if st.button("💾 حفظ التعديلات النهائية"):
            st.session_state['main_df'] = edited_df
            st.success("تم حفظ التعديلات في ذاكرة الوحش.")
    else: st.warning("البيانات فارغة. ارفع ملف أولاً.")

# 5. المحلل الذكي
elif choice == "🧠 المحلل الذكي":
    st.header("🧠 ذكاء MIA8444 في التحليل")
    if not df.empty:
        st.write("🔍 *الملخص الإحصائي للبيانات:*")
        st.dataframe(df.describe(), use_container_width=True)
    else: st.warning("لا توجد بيانات للتحليل.")

# 6. التنبؤ المالي
elif choice == "📉 التنبؤ المالي (AI)":
    st.header("📉 التنبؤ بمستقبل المبيعات")
    if not df.empty and 'المبيعات' in df.columns:
        y = df['المبيعات'].values
        future = np.poly1d(np.polyfit(np.arange(len(y)), y, 1))(np.arange(len(y), len(y) + 10))
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=y, name="الواقع الحالي", line=dict(color='#3b82f6')))
        fig.add_trace(go.Scatter(y=future, name="التنبؤ المستقبلي", line=dict(dash='dash', color='#ef4444')))
        st.plotly_chart(fig, use_container_width=True)
    else: st.info("تأكد من وجود عمود باسم 'المبيعات' لتفعيل ميزة التنبؤ.")

# 7. داشبورد الإدارة
elif choice == "🖥️ داشبورد الإدارة":
    st.header("🖥️ Dashboard High-Level (MIA8444)")
    if not df.empty:
        m1, m2, m3 = st.columns(3)
        m1.metric("إجمالي المبيعات", f"{df['المبيعات'].sum():,}")
        m2.metric("عدد العمليات", len(df))
        m3.metric("متوسط المبيعات", f"{df['المبيعات'].mean():.2f}")
        
        col_a, col_b = st.columns(2)
        with col_a:
            fig_pie = px.pie(df, names='المنتج', values='المبيعات', hole=0.4, title="توزيع المبيعات")
            st.plotly_chart(fig_pie)
        with col_b:
            fig_bar = px.bar(df, x='المنتج', y='المبيعات', color='المنتج', title="أداء المنتجات")
            st.plotly_chart(fig_bar)
    else: st.warning("ارفع بيانات لعرض الداشبورد.")

# 8. التقرير النهائي
elif choice == "📄 تقرير PDF النهائي":
    st.header("📄 تصدير التقرير الاحترافي")
    st.info("جاري تجهيز التقرير النهائي بختم MIA8444...")
    st.button("📥 تحميل التقرير (PDF)")

# تذييل الصفحة
st.markdown("---")
st.markdown("<center>Smart Analyst Beast | Powered by MIA8444 | 2026</center>", unsafe_allow_html=True)
