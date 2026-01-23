import streamlit as st
import pandas as pd
import numpy as np
import os

# 1. إعدادات الهوية والاحترافية
st.set_page_config(page_title="Smart Analyst PRO", layout="wide", page_icon="📊")

# 2. لغة الديزاين (CSS) لتحويل الشكل للنمط الفاخر (Dark & Gold)
st.markdown("""
    <style>
    /* الخلفية الداكنة العميقة */
    .stApp { background-color: #0d1117; color: #e6edf3; }
    
    /* تصميم البطاقات الاحترافي (Cards) */
    .metric-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 25px;
        text-align: center;
        transition: 0.3s;
    }
    .metric-card:hover { border-color: #d4af37; transform: translateY(-5px); }
    
    /* النصوص الذهبية */
    .gold-header { color: #d4af37; font-family: 'Arial'; font-weight: bold; }
    
    /* أزرار التصدير الذهبية المتدرجة */
    .export-btn {
        background: linear-gradient(135deg, #d4af37 0%, #f1d37e 100%);
        color: #000 !important;
        padding: 12px 25px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
        display: block;
        text-align: center;
        margin-top: 10px;
    }
    
    /* الشريط السفلي (MIA8444) */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #161b22;
        color: #d4af37;
        text-align: center;
        padding: 10px;
        border-top: 1px solid #30363d;
        font-size: 14px;
        z-index: 999;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. الهيدر (اللوجو والعنوان)
c1, c2 = st.columns([1, 5])
with c1:
    if os.path.exists("40833.jpg"):
        st.image("40833.jpg", width=90)
with c2:
    st.markdown("<h1 class='gold-header'>Smart Analyst <span style='color:white;'>PRO</span></h1>", unsafe_allow_html=True)
    st.caption("The Ultimate Financial Brand - Powered by MIA8444")

st.markdown("---")

# 4. توزيع العناصر (الـ Dashboard) كما في الصورة
col_side, col_main = st.columns([1, 3])

with col_side:
    st.markdown("<h3 class='gold-header'>Review & Edit</h3>", unsafe_allow_html=True)
    doc_type = st.selectbox("Select Document Type", ["Expenses", "Revenue", "Journals"])
    month = st.selectbox("Select Month", ["January", "February", "December"])
    
    st.markdown("---")
    file = st.file_uploader("Upload Documents", type=['xlsx', 'csv'])

with col_main:
    if file:
        df = pd.read_excel(file) if file.name.endswith('xlsx') else pd.read_csv(file)
        st.markdown("<p style='color: #8b949e;'>Data Preview & Analysis</p>", unsafe_allow_html=True)
        st.dataframe(df.head(10), use_container_width=True)
        
        # العمليات الحسابية (المحرك الخفي)
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if num_cols:
            target = st.selectbox("Choose Column for Insight:", num_cols)
            total = df[target].sum()
            avg = df[target].mean()
            
            # عرض البطاقات (Cards)
            m1, m2 = st.columns(2)
            with m1:
                st.markdown(f"<div class='metric-card'><p>Total Summation</p><h2 class='gold-header'>{total:,.2f}</h2></div>", unsafe_allow_html=True)
            with m2:
                st.markdown(f"<div class='metric-card'><p>Average Rating</p><h2 class='gold-header'>{avg:,.2f}</h2></div>", unsafe_allow_html=True)

    else:
        st.info("قم برفع ملف البيانات لبدء التحليل في لوحة القيادة.")

# 5. منطقة التصدير (Export & Share)
st.markdown("---")
st.markdown("<h3 class='gold-header'>Export & Share</h3>", unsafe_allow_html=True)
ce1, ce2 = st.columns(2)
with ce1:
    st.markdown('<a href="#" class="export-btn">📄 Export Excel</a>', unsafe_allow_html=True)
with ce2:
    st.markdown('<a href="#" class="export-btn">📑 Export PDF</a>', unsafe_allow_html=True)

# 6. التوقيع العالمي الثابت
st.markdown("<div class='footer'>Smart Analyst PRO | توقيع الخبير المعتمد: MIA8444</div>", unsafe_allow_html=True)
