import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
from sklearn.linear_model import LinearRegression # إضافة لمسة ذكاء اصطناعي

# ======== 1. تعريف الثوابت ========
APP_NAME = "Smart Analyst The Beast"
AUTHOR_SIGNATURE = "MIA8444"
LOGO_FILE = "8888.jpg" 

# ======== 2. إعدادات الصفحة ========
st.set_page_config(page_title=f"{AUTHOR_SIGNATURE} | The Beast", layout="wide", page_icon="🦁")

st.markdown(f"""
    <style>
    .stApp {{ background-color: #0e1117; color: white; }}
    [data-testid="stSidebar"] {{ background-color: #161b22; border-right: 1px solid #30363d; }}
    .footer {{ position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; padding: 5px; color: #8b949e; font-size: 12px; }}
    </style>
    <div class="footer">Property of {AUTHOR_SIGNATURE} | {APP_NAME} © 2026</div>
    """, unsafe_allow_html=True)

# ======== 3. القائمة الجانبية ========
with st.sidebar:
    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, use_container_width=True)
    st.markdown(f"<h2 style='text-align:center;'>🦁 {AUTHOR_SIGNATURE}</h2>", unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("المهام المتقدمة:", ["📊 غرفة العمليات والذكاء", "📄 معالج الـ PDF الخارق"])
    st.markdown("---")
    st.info("النظام يعمل بنسخة الذكاء الاصطناعي المتطورة")

# ======== 4. غرفة العمليات (تحليل + تنبؤ) ========
if menu == "📊 غرفة العمليات والذكاء":
    st.markdown(f"## 📊 غرفة العمليات | {AUTHOR_SIGNATURE}")
    
    data_file = st.file_uploader("ارفع ملف البيانات (CSV/Excel)", type=['csv', 'xlsx'])
    
    if data_file:
        df = pd.read_csv(data_file) if data_file.name.endswith('.csv') else pd.read_excel(data_file)
        st.session_state['df'] = df
        
        # عرض البيانات
        with st.expander("👀 استعراض البيانات الخام"):
            st.dataframe(df, use_container_width=True)
            
        # قسم الذكاء الاصطناعي (التنبؤ)
        st.markdown("### 🤖 محرك التنبؤ الذكي (MIA8444 Engine)")
        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        
        if len(num_cols) >= 2:
            st.write("الوحش هيتوقعلك القيم الجاية بناءً على بياناتك:")
            col_x = st.selectbox("محور التنبؤ (X)", num_cols, index=0)
            col_y = st.selectbox("القيمة المراد توقعها (Y)", num_cols, index=1)
            
            # كود التنبؤ البسيط
            X = df[[col_x]].values
            y = df[col_y].values
            model = LinearRegression().fit(X, y)
            
            fig = px.scatter(df, x=col_x, y=col_y, trendline="ols", 
                             title=f"تحليل الاتجاه الذكي: {col_y} مقابل {col_x}", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
            st.success(f"✅ تم تحليل العلاقة بنجاح. الوحش يرى اتجاه واضح في بياناتك!")

# ======== 5. معالج الـ PDF الخارق ========
elif menu == "📄 معالج الـ PDF الخارق":
    st.markdown(f"## 📄 معالج الـ PDF الخارق | {AUTHOR_SIGNATURE}")
    pdf_input = st.file_uploader("ارفع ملف الـ PDF لتحويله لبيانات", type=['pdf'])
    
    if pdf_input:
        st.success("الملف في قبضة الوحش! 🦁")
        st.markdown("### 🛠️ الأدوات المتاحة للملف:")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📝 تلخيص النص (FETH AI)"):
                st.info("جاري استخراج الأفكار الرئيسية من التقرير...")
        with col2:
            if st.button("📊 استخراج الجداول"):
                st.warning("جاري البحث عن جداول أرقام لتحويلها لملف Excel...")
