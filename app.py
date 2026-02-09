import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

# ======== 1. تعريف الهوية (عشان الـ NameError يختفي) ========
APP_NAME = "Smart Analyst The Beast"
AUTHOR_SIGNATURE = "MIA8444"
LOGO_FILE = "8888.jpg" # اتأكد إن الملف ده مرفوع في نفس فولدر الكود على GitHub

# ======== 2. إعدادات الصفحة ========
st.set_page_config(page_title=f"{AUTHOR_SIGNATURE} | The Beast", layout="wide", page_icon="🦁")

# ستايل "الساعة" - بسيط، فخم، ومنظم
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0e1117; color: white; }}
    [data-testid="stSidebar"] {{ background-color: #161b22; border-right: 1px solid #30363d; }}
    .footer {{ position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; padding: 5px; color: #8b949e; font-size: 12px; }}
    </style>
    <div class="footer">Developed by {AUTHOR_SIGNATURE} | {APP_NAME} © 2026</div>
    """, unsafe_allow_html=True)

# ======== 3. الـ Sidebar (إظهار اللوجو والتحكم) ========
with st.sidebar:
    # محاولة إظهار اللوجو
    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, use_container_width=True)
    else:
        st.markdown(f"<h1 style='text-align:center; color:#58a6ff;'>🦁 {AUTHOR_SIGNATURE}</h1>", unsafe_allow_html=True)
    
    st.markdown("---")
    menu = st.radio("المهام المتاحة:", ["📊 غرفة العمليات التحليلية", "📄 وحدة معالجة الـ PDF"])
    st.markdown("---")
    st.info(f"نظام {AUTHOR_SIGNATURE} جاهز للعمل")

# ======== 4. تطوير الأدوات (غرفة العمليات التحليلية) ========
if menu == "📊 غرفة العمليات التحليلية":
    st.markdown(f"## 🛠️ مركز تحليل البيانات | {AUTHOR_SIGNATURE}")
    
    file = st.file_uploader("ارفع ملف البيانات (Excel/CSV):", type=['csv', 'xlsx'])
    
    if file:
        df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
        st.session_state.df = df
        
        col1, col2, col3 = st.columns(3)
        col1.metric("إجمالي السجلات", len(df))
        col2.metric("عدد الأعمدة", len(df.columns))
        col3.metric("توقيع المحلل", AUTHOR_SIGNATURE)
        
        st.markdown("### 📈 التحليل البصري التفاعلي")
        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        
        if num_cols:
            c1, c2 = st.columns(2)
            with c1: x_axis = st.selectbox("المحور الأفقي", df.columns)
            with c2: y_axis = st.selectbox("المحور الرأسي", num_cols)
            
            fig = px.bar(df, x=x_axis, y=y_axis, template="plotly_dark", color_discrete_sequence=['#58a6ff'])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("الملف لا يحتوي على بيانات رقمية للرسم.")

# ======== 5. تطوير وحدة الـ PDF ========
elif menu == "📄 وحدة معالجة الـ PDF":
    st.markdown(f"## 📄 معالج التقارير الذكي | {AUTHOR_SIGNATURE}")
    pdf_file = st.file_uploader("ارفع ملف PDF للتحليل:", type=['pdf'])
    
    if pdf_file:
        st.success("تم استلام الملف بنجاح.")
        st.info("💡 جاري ربط محرك التلخيص الذكي (FETH AI)...")
        # هنا الخطوة الجاية هنضيف كود التلخيص الفعلي
        st.write("ملخص أولي: الملف جاهز للاستخراج.")
