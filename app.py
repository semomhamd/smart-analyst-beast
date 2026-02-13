import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')

# ======= الإعدادات =======
AUTHOR_SIGNATURE = "MIA8444"
APP_NAME = "The Beast Pro"
APP_VERSION = "4.0.0"

st.set_page_config(page_title=f"{AUTHOR_SIGNATURE} | {APP_NAME}", page_icon="🦁", layout="wide")

# ======= Session State =======
if 'beast_df' not in st.session_state:
    st.session_state.beast_df = None
if 'cleaning_log' not in st.session_state:
    st.session_state.cleaning_log = []
if 'ml_predictions' not in st.session_state:
    st.session_state.ml_predictions = None
if 'report_language' not in st.session_state:
    st.session_state.report_language = "ar"

# ======= CSS =======
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');
    * { font-family: 'Tajawal', sans-serif; direction: rtl; }
    .stApp { background: #0a0e17; color: #f3f4f6; }
    .glass-card {
        background: rgba(17, 24, 39, 0.7);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 24px;
        padding: 30px;
        margin: 20px 0;
    }
    .gradient-text {
        background: linear-gradient(135deg, #3b82f6 0%, #10b981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 2.5rem;
    }
    .metric-container {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        color: white;
    }
    .metric-value { font-size: 2.5rem; font-weight: 900; }
</style>
""", unsafe_allow_html=True)

# ======= Sidebar =======
with st.sidebar:
    st.markdown(f"<h1 class='gradient-text'>{APP_NAME}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:#6b7280;'>v{APP_VERSION} | {AUTHOR_SIGNATURE}</p>")
    st.markdown("---")
    
    menu = st.radio("القائمة:", [
        "🏠 الرئيسية",
        "📤 رفع البيانات", 
        "🧹 تنظيف ذكي",
        "📊 داشبورد Pro",
        "🧠 تنبؤ AI",
        "📄 تقرير PDF"
    ])

# ======= الصفحات =======

if menu == "🏠 الرئيسية":
    st.markdown("<h1 class='gradient-text'>The Beast Pro</h1>", unsafe_allow_html=True)
    st.write("مرحباً بك في نظام التحليل الذكي")
    
    if st.button("🚀 توليد بيانات تجريبية"):
        df = pd.DataFrame({
            'التاريخ': pd.date_range('2026-01-01', periods=100),
            'المبيعات': np.random.randint(10000, 50000, 100),
            'المصاريف': np.random.randint(5000, 20000, 100)
        })
        df['الربح'] = df['المبيعات'] - df['المصاريف']
        st.session_state.beast_df = df
        st.success(f"تم إنشاء {len(df)} سجل!")

elif menu == "📤 رفع البيانات":
    st.markdown("<h1 class='gradient-text'>رفع البيانات</h1>", unsafe_allow_html=True)
    
    file = st.file_uploader("اختر ملف", type=['csv', 'xlsx'])
    if file:
        try:
            if file.name.endswith('xlsx'):
                df = pd.read_excel(file, engine='openpyxl')
            else:
                df = pd.read_csv(file)
            st.session_state.beast_df = df
            st.success(f"تم التحميل: {len(df)} سجل")
            st.dataframe(df.head())
        except Exception as e:
            st.error(f"خطأ: {e}")

elif menu == "🧹 تنظيف ذكي":
    st.markdown("<h1 class='gradient-text'>تنظيف ذكي</h1>", unsafe_allow_html=True)
    
    if st.session_state.beast_df is None:
        st.warning("ارفع البيانات أولاً")
    else:
        df = st.session_state.beast_df
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("السجلات", len(df))
        with col2:
            st.metric("مكرر", df.duplicated().sum())
        with col3:
            st.metric("فارغ", df.isnull().sum().sum())
        with col4:
            quality = max(0, 100 - (df.isnull().sum().sum() + df.duplicated().sum()) / len(df) * 100)
            st.metric("الجودة", f"{quality:.0f}%")
        
        if st.button("🚀 تنظيف"):
            df = df.drop_duplicates()
            st.session_state.beast_df = df
            st.session_state.cleaning_log.append("حذف التكرار")
            st.success("تم التنظيف!")

elif menu == "📊 داشبورد Pro":
    st.markdown("<h1 class='gradient-text'>الداشبورد</h1>", unsafe_allow_html=True)
    
    if st.session_state.beast_df is None:
        st.warning("ارفع البيانات أولاً")
    else:
        df = st.session_state.beast_df
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if numeric_cols:
            fig = px.line(df, y=numeric_cols[0], template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

elif menu == "🧠 تنبؤ AI":
    st.markdown("<h1 class='gradient-text'>تنبؤ AI</h1>", unsafe_allow_html=True)
    
    if st.session_state.beast_df is None:
        st.warning("ارفع البيانات أولاً")
    else:
        df = st.session_state.beast_df
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if numeric_cols and st.button("🔮 تنبؤ"):
            try:
                from sklearn.linear_model import LinearRegression
                X = np.arange(len(df)).reshape(-1, 1)
                y = df[numeric_cols[0]].values
                model = LinearRegression()
                model.fit(X, y)
                future = model.predict(np.array([[len(df) + i] for i in range(30)]))
                st.line_chart(list(y) + list(future))
                st.success("تم التنبؤ!")
            except Exception as e:
                st.error(f"خطأ: {e}")

elif menu == "📄 تقرير PDF":
    st.markdown("<h1 class='gradient-text'>تقرير PDF</h1>", unsafe_allow_html=True)
    
    if st.session_state.beast_df is None:
        st.warning("ارفع البيانات أولاً")
    else:
        if st.button("📄 إنشاء PDF"):
            try:
                from reportlab.lib.pagesizes import A4
                from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
                from reportlab.lib.styles import getSampleStyleSheet
                from io import BytesIO
                
                buffer = BytesIO()
                doc = SimpleDocTemplate(buffer, pagesize=A4)
                styles = getSampleStyleSheet()
                elements = []
                
                elements.append(Paragraph("The Beast Pro Report", styles['Title']))
                elements.append(Spacer(1, 12))
                elements.append(Paragraph(f"Records: {len(st.session_state.beast_df)}", styles['Normal']))
                
                doc.build(elements)
                buffer.seek(0)
                
                st.download_button("تحميل PDF", buffer.getvalue(), "report.pdf", "application/pdf")
            except Exception as e:
                st.error(f"خطأ: {e}")

st.markdown("---")
st.caption(f"{APP_NAME} | {AUTHOR_SIGNATURE} © 2026")
