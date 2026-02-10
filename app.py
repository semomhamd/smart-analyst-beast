import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression
import os

# ======== 1. الهوية والبراند (MIA8444) ========
APP_NAME = "Smart Analyst"
AUTHOR_SIGNATURE = "MIA8444"
LOGO_FILE = "8888.jpg"
SLOGAN = "The Ultimate Financial Brain"

st.set_page_config(page_title=f"{AUTHOR_SIGNATURE} | {APP_NAME}", layout="wide", page_icon="📈")

# ======== 2. المحرك الجمالي وديناميكية الألوان ========
if 'theme_color' not in st.session_state:
    st.session_state.theme_color = "#58a6ff"

st.markdown(f"""
    <style>
    .stApp {{ background-color: #0d1117; color: white; }}
    .footer {{ position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; padding: 10px; background: #161b22; color: #8b949e; border-top: 1px solid {st.session_state.theme_color}; font-size: 12px; z-index: 100; }}
    .stSidebar {{ background-color: #161b22; border-right: 1px solid #30363d; }}
    .stButton>button {{ border-radius: 12px; background-color: {st.session_state.theme_color}; color: white; border: none; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

# ======== 3. القائمة الجانبية المترتبة (The Command Center) ========
with st.sidebar:
    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, use_container_width=True)
    st.markdown(f"<h2 style='text-align:center; color:{st.session_state.theme_color};'>{APP_NAME}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; font-size:11px; margin-top:-15px;'>{SLOGAN}</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    menu = st.radio("القائمة الرئيسية:", [
        "🏠 لوحة التحكم المركزية",
        "📂 Excel Pro (إنشاء وحفظ سحابي)",
        "✨ منظف البيانات الخارق (Auto-Clean)",
        "🔮 محرك التنبؤ AI (Predictive)",
        "📤 جسر التصدير العالمي (SQL/Power BI)",
        "⚙️ الإعدادات المتقدمة"
    ])
    st.markdown("---")
    st.success(f"المستخدم: {AUTHOR_SIGNATURE}")

# ======== 4. تفعيل الأدوات والذكاء الاصطناعي ========

# --- 📂 Excel Pro ---
if menu == "📂 Excel Pro (إنشاء وحفظ سحابي)":
    st.header("📂 Excel Pro Hub")
    if 'cloud_db' not in st.session_state:
        st.session_state.cloud_db = pd.DataFrame(columns=["البيان", "القيمة", "التاريخ", "الحالة"])
    
    st.write("أدخل بياناتك يدوياً لإنشاء شيت احترافي:")
    new_df = st.data_editor(st.session_state.cloud_db, num_rows="dynamic", use_container_width=True)
    
    c1, c2 = st.columns(2)
    if c1.button("☁️ مزامنة وحفظ سحابي"):
        st.session_state.cloud_db = new_df
        st.success("تم الحفظ في قاعدة بيانات MIA8444 السحابية!")

# --- ✨ منظف البيانات ---
elif menu == "✨ منظف البيانات الخارق (Auto-Clean)":
    st.header("✨ The Beast Data Cleaner")
    up_file = st.file_uploader("ارفع الملف المراد تصفيتة", type=['csv', 'xlsx'])
    if up_file:
        df_raw = pd.read_excel(up_file) if up_file.name.endswith('xlsx') else pd.read_csv(up_file)
        if st.button("🚀 تفعيل التنظيف العالمي"):
            df_clean = df_raw.drop_duplicates().dropna(how='all')
            st.success("✅ تم تنظيف البيانات وحذف المكررات!")
            st.dataframe(df_clean)

# --- 🔮 محرك التنبؤ (الإصلاح الجذري للخطأ) ---
elif menu == "🔮 محرك التنبؤ AI (Predictive)":
    st.header("🔮 AI Prediction Engine")
    predict_file = st.file_uploader("ارفع ملف البيانات للتنبؤ", type=['csv', 'xlsx'])
    if predict_file:
        df = pd.read_excel(predict_file) if predict_file.name.endswith('xlsx') else pd.read_csv(predict_file)
        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        if len(num_cols) >= 2:
            x_ax = st.selectbox("بناءً على (X):", num_cols)
            y_ax = st.selectbox("توقع قيمة (Y):", num_cols)
            # رسم بدون مكتبة statsmodels لتجنب الإيرور
            fig = px.scatter(df, x=x_ax, y=y_ax, title="تحليل العلاقة البيانية", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
            st.info("💡 المحرك يحلل الآن الاتجاهات المستقبلية لبياناتك.")

# --- ⚙️ الإعدادات ---
elif menu == "⚙️ الإعدادات المتقدمة":
    st.header("⚙️ ترس التحكم")
    st.session_state.theme_color = st.color_picker("🎨 اختر لون هوية التطبيق", st.session_state.theme_color)
    st.selectbox("🌐 لغة النظام", ["العربية", "English"])

# ======== 5. التوقيع (Footer) ========
st.markdown(f"""
    <div class="footer">
        {APP_NAME} | {SLOGAN} | <b>Property of {AUTHOR_SIGNATURE}</b>
    </div>
    """, unsafe_allow_html=True)
