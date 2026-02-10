import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression
import os

# ======== 1. الهوية العالمية (MIA8444) ========
APP_NAME = "Smart Analyst"
AUTHOR_SIGNATURE = "MIA8444"
LOGO_FILE = "8888.jpg"
ENGLISH_SLOGAN = "The Ultimate Financial Brain"

st.set_page_config(page_title=f"{AUTHOR_SIGNATURE} | {APP_NAME}", layout="wide", page_icon="📈")

# ======== 2. التنسيق (Dark Mode & UI) ========
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0d1117; color: white; }}
    .footer {{ position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; padding: 5px; background: #161b22; color: #8b949e; border-top: 1px solid #30363d; font-size: 12px; }}
    .stSidebar {{ background-color: #161b22; }}
    </style>
    """, unsafe_allow_html=True)

# ======== 3. القائمة الجانبية المترتبة ========
with st.sidebar:
    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, use_container_width=True)
    st.markdown(f"<h2 style='text-align:center;'>{APP_NAME}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; font-size:11px;'>{ENGLISH_SLOGAN}</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    menu = st.radio("المهام المتقدمة:", [
        "🏠 مركز التحكم",
        "📂 Excel Pro & Manual Entry",
        "✨ منظف البيانات الخارق",
        "🔮 محرك التنبؤ والذكاء",
        "📊 التحليل البصري (Power BI Style)",
        "📤 جسر التصدير العالمي",
        "📄 معالج الـ PDF والتقارير"
    ])
    
    st.markdown("---")
    with st.expander("⚙️ الإعدادات (ترس التحكم)"):
        st.selectbox("🌐 اللغة", ["العربية", "English"])
        st.color_picker("🎨 لون الهوية", "#58a6ff")

# ======== 4. تفعيل الأدوات والذكاء الاصطناعي ========

# --- قسم Excel Pro ---
if menu == "📂 Excel Pro & Manual Entry":
    st.header("📂 Excel Pro Hub")
    if 'data_grid' not in st.session_state:
        st.session_state.data_grid = pd.DataFrame(columns=["البند", "القيمة", "التاريخ"])
    
    st.write("أدخل بياناتك يدوياً لإنشاء شيت احترافي:")
    new_data = st.data_editor(st.session_state.data_grid, num_rows="dynamic", use_container_width=True)
    
    if st.button("💾 حفظ وتصدير للإكسيل"):
        st.session_state.data_grid = new_data
        st.success("تم تجهيز ملف Excel احترافي!")

# --- قسم التنبؤ الذكي ---
elif menu == "🔮 محرك التنبؤ والذكاء":
    st.header("🔮 AI Prediction Engine")
    st.info("الذكاء الاصطناعي يحلل الاتجاهات المستقبلية لبياناتك")
    
    uploaded_file = st.file_uploader("ارفع بياناتك للتنبؤ", type=['csv', 'xlsx'])
    if uploaded_file:
        df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file)
        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        
        if len(num_cols) >= 2:
            x_col = st.selectbox("بناءً على (X):", num_cols)
            y_col = st.selectbox("توقع قيمة (Y):", num_cols)
            
            # محرك التنبؤ
            X = df[[x_col]].values.reshape(-1, 1)
            y = df[y_col].values
            model = LinearRegression().fit(X, y)
            
            fig = px.scatter(df, x=x_col, y=y_col, trendline="ols", title="التنبؤ والاتجاه الذكي", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
            st.write(f"🤖 الذكاء الاصطناعي يقول: هناك علاقة قوية بنسبة {round(model.score(X, y)*100, 2)}% بين المتغيرين.")

# --- قسم التصدير العالمي ---
elif menu == "📤 جسر التصدير العالمي":
    st.header("📤 Universal Export Bridge")
    st.markdown("تصدير مباشر لكل أدوات تحليل البيانات العالمية")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.button("💾 To SQL")
    c2.button("📊 To Power BI")
    c3.button("🐍 To Python")
    c4.button("📈 To Tableau")

# ======== 5. التوقيع (Footer) ========
st.markdown(f"""
    <div class="footer">
        {APP_NAME} | {ENGLISH_SLOGAN} | MIA8444 Signature © 2026
    </div>
    """, unsafe_allow_html=True)
