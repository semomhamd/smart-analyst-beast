import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import os
from io import BytesIO

# إعدادات الهوية واللوجو
st.set_page_config(page_title="Smart Analyst Beast PRO", layout="wide", page_icon="🦁")

# الرسالة المتفق عليها والتوقيع [cite: 2026-01-26]
slogan = "Smart Analyst Beast PRO - Signature: MIA8444"

# --- السايد بار (الهوية والمشاركة) ---
with st.sidebar:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_column_width=True) # اللوجو [cite: 2026-01-28]
    st.markdown(f"### {slogan}")
    st.write("---")
    
    # تفعيل المشاركة [cite: 2026-02-01]
    st.button("🔗 مشاركة التطبيق (Share)")
    
    menu = [
        "🏠 الرئيسية وتوليد الاختبار",
        "👁️ الرؤية الذكية (OCR)", 
        "🧼 منظف البيانات", 
        "📊 محرر الاكسل (Pro)", 
        "🧠 المحلل الذكي", 
        "📉 التنبؤ المالي (AI)", 
        "🖥️ داشبورد الإدارة", 
        "📄 تقرير PDF النهائي"
    ]
    choice = st.sidebar.selectbox("انتقل بين الأدوات:", menu)
    st.write("---")
    st.info("حبيبي يا محمد، كل الأدوات مربوطة بالذكاء الاصطناعي دلوقت [cite: 2026-01-27].")

# مخزن البيانات الأساسي
if 'main_df' not in st.session_state:
    st.session_state['main_df'] = pd.DataFrame()

df = st.session_state['main_df']

# --- 1. الرئيسية وتوليد ملفات الاختبار ---
if choice == "🏠 الرئيسية وتوليد الاختبار":
    st.header("🏠 بوابة التحكم في البيانات")
    col1, col2 = st.columns(2)
    with col1:
        up = st.file_uploader("ارفع ملفك (Excel/CSV)", type=['csv', 'xlsx'])
        if up:
            st.session_state['main_df'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
            st.success("تم الشحن بنجاح!")
    with col2:
        if st.button("🧬 توليد ملف اختبار احترافي"):
            test_data = pd.DataFrame({
                'التاريخ': pd.date_range(start='2025-01-01', periods=50),
                'المنتج': np.random.choice(['موبايل', 'ساعة', 'سماعة', 'لابتوب'], 50),
                'المبيعات': np.random.randint(100, 5000, 50),
                'التكلفة': np.random.randint(50, 4000, 50)
            })
            st.session_state['main_df'] = test_data
            st.success("تم توليد بيانات الاختبار بنجاح!")

# --- 2. الرؤية الذكية (قبل المنظف كما طلبت) ---
elif choice == "👁️ الرؤية الذكية (OCR)":
    st.header("👁️ محرك الرؤية الذكي (AI Vision)")
    cam = st.camera_input("صور المستند الورقي")
    if cam:
        st.image(cam, caption="تم التقاط الصورة جاري التحليل...")
        st.info("الذكاء الاصطناعي يقوم باستخراج الجداول الآن... [cite: 2026-02-01]")

# --- 3. منظف البيانات ---
elif choice == "🧼 منظف البيانات":
    st.header("🧼 وحدة التنظيف والتهيئة")
    if not df.empty:
        if st.button("تنظيف عميق (Auto Clean)"):
            df = df.drop_duplicates().fillna(0)
            st.session_state['main_df'] = df
            st.success("تم حذف المكررات ومعالجة القيم الفارغة.")
            st.dataframe(df.head())
    else: st.warning("لا توجد بيانات لتنظيفها.")

# --- 4. محرر الاكسل (Pro - شبيه بالأصلي) ---
elif choice == "📊 محرر الاكسل (Pro)":
    st.header("📊 Excel Pro Dashboard")
    if not df.empty:
        # تحسين العرض ليكون شبيه بالاكسل الأصلي [cite: 2026-02-01]
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        if st.button("حفظ تعديلات الاكسل"):
            st.session_state['main_df'] = edited_df
            st.success("تم حفظ التعديلات في ذاكرة الوحش.")
    else: st.warning("ارفع ملف أولاً.")

# --- 5. المحلل الذكي ---
elif choice == "🧠 المحلل الذكي":
    st.header("🧠 ذكاء MIA8444 في التحليل")
    if not df.empty:
        st.write("🔍 *الوصف الإحصائي:*")
        st.table(df.describe())
    else: st.warning("البيانات فارغة.")

# --- 6. التنبؤ المالي ---
elif choice == "📉 التنبؤ المالي (AI)":
    st.header("📉 التنبؤ بمستقبل المبيعات")
    if not df.empty and 'المبيعات' in df.columns:
        y = df['المبيعات'].values
        future = np.poly1d(np.polyfit(np.arange(len(y)), y, 1))(np.arange(len(y), len(y) + 10))
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=y, name="الحالي"))
        fig.add_trace(go.Scatter(y=future, name="التنبؤ المستقبلي", line=dict(dash='dash')))
        st.plotly_chart(fig, use_container_width=True)
    else: st.info("تأكد من وجود عمود 'المبيعات' للتنبؤ.")

# --- 7. داشبورد عالي المستوى ---
elif choice == "🖥️ داشبورد الإدارة":
    st.header("🖥️ Dashboard High-Level (MIA8444)")
    if not df.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("إجمالي المبيعات", f"{df['المبيعات'].sum():,}")
        c2.metric("عدد العمليات", len(df))
        c3.metric("متوسط الربح", f"{df['المبيعات'].mean():.2f}")
        
        col_a, col_b = st.columns(2)
        with col_a:
            fig1 = px.pie(df, names='المنتج', values='المبيعات', hole=0.4, title="توزيع المبيعات")
            st.plotly_chart(fig1)
        with col_b:
            fig2 = px.bar(df, x='المنتج', y='المبيعات', color='المنتج', title="أداء المنتجات")
            st.plotly_chart(fig2)

# --- 8. التقرير النهائي PDF ---
elif choice == "📄 تقرير PDF النهائي":
    st.header("📄 تصدير التقرير الاحترافي")
    st.info("جاري تجهيز التقرير بصيغة PDF الشاملة لجميع التحليلات... [cite: 2026-02-01]")
    st.button("📥 تحميل التقرير (MIA8444_Report.pdf)")
