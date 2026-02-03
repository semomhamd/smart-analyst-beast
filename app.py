import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
from io import BytesIO
from PIL import Image
import easyocr
import cv2
from prophet import Prophet

# --- 1. إعدادات الهوية والأداء الفخم (Signature: MIA8444) ---
st.set_page_config(
    page_title="Smart Analyst Beast PRO",
    layout="wide",
    page_icon="🦁"
)

# تنسيق CSS احترافي لضمان شكل الداشبورد الفخم
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    [data-testid="stSidebar"] { background-color: #161b22; }
    [data-testid="stMetricValue"] { font-size: 35px; color: #ffffff; }
    .stMetric { background-color: #1f2937; padding: 20px; border-radius: 12px; border-top: 4px solid #3b82f6; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #238636; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك الذاكرة والـ OCR ---
if 'main_df' not in st.session_state:
    st.session_state['main_df'] = pd.DataFrame()

@st.cache_resource
def load_ocr_model():
    return easyocr.Reader(['ar', 'en'], gpu=False)

# --- 3. السايد بار والهوية البصرية ---
with st.sidebar:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_container_width=True)
    
    st.markdown("<h2 style='text-align: center;'>Smart Analyst Beast</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>MIA8444 Signature</p>", unsafe_allow_html=True)
    st.write("---")
    
    menu = {
        "🏠 الرئيسية وبوابة البيانات": "Home",
        "👁️ العين الرقمية (OCR)": "OCR",
        "🧼 منظف البيانات الذكي": "Clean",
        "📊 محرر SnaAyas Pro": "Excel",
        "🧠 المحلل الاستراتيجي": "Analysis",
        "📈 التنبؤ المالي (AI)": "Forecast",
        "🖥️ داشبورد الإدارة": "Dashboard",
        "📄 تقرير PDF النهائي": "PDF"
    }
    
    choice = st.radio("انتقل بدقة بين أدواتك:", list(menu.keys()))
    st.write("---")
    st.success("System Status: Active 🟢")
    st.caption("Smart Analyst thinks for you")

# استدعاء البيانات الحالية
df = st.session_state['main_df']

# --- 4. معالجة الصفحات (Logic) ---

# [1] الصفحة الرئيسية
if choice == "🏠 الرئيسية وبوابة البيانات":
    st.header("🏠 بوابة التحكم الرئيسية")
    col1, col2 = st.columns(2)
    with col1:
        up = st.file_uploader("ارفع ملفك (Excel/CSV)", type=['csv', 'xlsx'])
        if up:
            st.session_state['main_df'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
            st.success("تم شحن البيانات بنجاح! ⚡")
            st.rerun()
    with col2:
        if st.button("🧬 توليد بيانات اختبار (Beast Sample)"):
            test_data = pd.DataFrame({
                'التاريخ': pd.date_range(start='2025-01-01', periods=100),
                'المنتج': np.random.choice(['موبايل', 'ساعة', 'لابتوب', 'سماعة'], 100),
                'المبيعات': np.random.randint(1000, 15000, 100),
                'التكلفة': np.random.randint(500, 8000, 100)
            })
            st.session_state['main_df'] = test_data
            st.rerun()

# [2] العين الرقمية (OCR) - المرحلة الأولى المطورة
elif choice == "👁️ العين الرقمية (OCR)":
    st.header("👁️ محرك الرؤية الذكي (AI Vision)")
    reader = load_ocr_model()
    img_file = st.file_uploader("ارفع صورة البيانات/الفاتورة", type=['jpg', 'jpeg', 'png'])
    if img_file:
        image = Image.open(img_file)
        st.image(image, use_container_width=True)
        if st.button("تحليل الصورة 🦁"):
            results = reader.readtext(np.array(image))
            extracted = [res[1] for res in results]
            st.write("النصوص المكتشفة:", extracted)
            # تحويل بسيط لجدول
            new_df = pd.DataFrame(extracted, columns=["المستخرج"])
            st.session_state['main_df'] = new_df
            st.success("تم الدمج في ذاكرة الوحش.")

# [3] منظف البيانات
elif choice == "🧼 منظف البيانات الذكي":
    st.header("🧼 وحدة تنظيف البيانات")
    if not df.empty:
        if st.button("تنظيف عميق ومعالجة القيم"):
            st.session_state['main_df'] = df.dropna().drop_duplicates()
            st.success("البيانات الآن نظيفة تماماً ✅")
        st.dataframe(df.head(20), use_container_width=True)
    else: st.warning("لا توجد بيانات لتنظيفها.")

# [4] محرر SnaAyas Pro
elif choice == "📊 محرر SnaAyas Pro":
    st.header("📊 محرر الجداول (SnaAyas Pro)")
    if not df.empty:
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        if st.button("حفظ التعديلات النهائية"):
            st.session_state['main_df'] = edited_df
            st.success("تم الحفظ بنجاح!")
    else: st.warning("ارفع بيانات أولاً.")

# [5] المحلل الاستراتيجي
elif choice == "🧠 المحلل الاستراتيجي":
    st.header("🧠 رؤية المحلل الذكي")
    if not df.empty:
        st.write("### ملخص إحصائي سريع:")
        st.write(df.describe())
        if 'المبيعات' in df.columns:
            fig = px.box(df, y="المبيعات", title="تحليل الانحرافات في المبيعات")
            st.plotly_chart(fig, use_container_width=True)
    else: st.warning("لا يوجد بيانات للتحليل.")

# [6] التنبؤ المالي (AI Forecast) - المرحلة الثانية
elif choice == "📈 التنبؤ المالي (AI)":
    st.header("📈 التنبؤ بمستقبل المبيعات")
    if not df.empty and 'التاريخ' in df.columns and 'المبيعات' in df.columns:
        # تجهيز البيانات لـ Prophet
        pdf = df[['التاريخ', 'المبيعات']].rename(columns={'التاريخ': 'ds', 'المبيعات': 'y'})
        pdf['ds'] = pd.to_datetime(pdf['ds'])
        m = Prophet()
        m.fit(pdf)
        future = m.make_future_dataframe(periods=30)
        forecast = m.predict(future)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=pdf['ds'], y=pdf['y'], name='الحالي'))
        fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], name='التنبؤ', line=dict(dash='dash')))
        st.plotly_chart(fig, use_container_width=True)
    else: st.warning("تأكد من وجود أعمدة 'التاريخ' و 'المبيعات' للتنبؤ.")

# [7] داشبورد الإدارة
elif choice == "🖥️ داشبورد الإدارة":
    st.header("🖥️ Dashboard Management (MIA8444)")
    if not df.empty and 'المبيعات' in df.columns:
        c1, c2, c3 = st.columns(3)
        c1.metric("إجمالي المبيعات", f"{df['المبيعات'].sum():,.0f}")
        c2.metric("عدد العمليات", len(df))
        c3.metric("متوسط العملية", f"{df['المبيعات'].mean():,.2f}")
        
        col_a, col_b = st.columns(2)
        with col_a:
            fig_pie = px.pie(df, names='المنتج' if 'المنتج' in df.columns else df.columns[0], values='المبيعات', hole=0.5, title="توزيع المبيعات")
            st.plotly_chart(fig_pie, use_container_width=True)
        with col_b:
            fig_bar = px.bar(df, x='المنتج' if 'المنتج' in df.columns else df.columns[0], y='المبيعات', title="أداء المنتجات")
            st.plotly_chart(fig_bar, use_container_width=True)
    else: st.warning("البيانات غير كافية لعرض الداشبورد.")

# [8] تصدير التقرير PDF
elif choice == "📄 تقرير PDF النهائي":
    st.header("📄 تصدير التقرير النهائي")
    st.info("جاري تجهيز محرك PDF ليدعم التوقيع الخاص بك MIA8444.")
    if st.button("تحميل MIA8444_Report.pdf"):
        st.success("تم تجهيز التقرير (نسخة تجريبية)!")

st.write("---")
st.markdown("<center>Smart Analyst Beast | Powered by MIA8444</center>", unsafe_allow_html=True)
