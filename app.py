import streamlit as st
import pandas as pd
import numpy as np
import google.generativeai as genai
import hashlib
import plotly.express as px
from io import BytesIO

# 1. إعدادات الصفحة الاحترافية
st.set_page_config(page_title="Smart Analyst Ultimate", layout="wide", initial_sidebar_state="expanded")

# 2. إعداد الذكاء الاصطناعي (Gemini)
genai.configure(api_key="AIzaSyBBiIEEGCzXpv80cwR9yzLXuQdj_J5n9tA")
model = genai.GenerativeModel('gemini-pro')

# --- وظائف الأمان والنظام ---
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text: return hashed_text
    return False

if 'user_db' not in st.session_state:
    st.session_state.user_db = {"admin": make_hashes("1234"), "semomohamed": make_hashes("123456")} 

if 'auth' not in st.session_state:
    st.session_state.auth = False

# 3. واجهة الدخول
if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center; color: #fbbf24;'>🔐 Smart Analyst Ultimate Login</h1>", unsafe_allow_html=True)
    t_login, t_signup = st.tabs(["دخول", "إنشاء حساب"])
    with t_login:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Login"):
            if u in st.session_state.user_db and check_hashes(p, st.session_state.user_db[u]):
                st.session_state.auth = True
                st.rerun()
            else: st.error("خطأ في البيانات")
    st.stop()

# 4. الستايل العالمي (ألوان مثالية)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; background-color: #0e1117; color: white; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { background-color: #161b22; border: 1px solid #fbbf24; border-radius: 10px; padding: 10px 20px; color: white; }
    .header-box { display: flex; align-items: center; justify-content: center; background: #161b22; padding: 20px; border-radius: 15px; border: 2px solid #fbbf24; margin-bottom: 25px; }
</style>
""", unsafe_allow_html=True)

# 5. الهيدر (اللغة والإعدادات)
col_l, col_m, col_r = st.columns([1, 3, 1])
with col_l:
    if st.button("🌐 English/عربي"): st.toast("جاري التبديل...")
with col_r:
    if st.button("⚙️ Settings"): st.toast("فتح الإعدادات...")

st.markdown(f"""
<div class='header-box'>
    <img src="https://raw.githubusercontent.com/semomhamd/smart-analyst-beast/main/99afc3d2-b6ef-4eda-977f-2fdc4b6621dd.jpg" style="width:70px; border-radius:15px; margin-left:20px;">
    <h1 style='color: #fbbf24; margin: 0;'>Smart Analyst Ultimate Pro</h1>
</div>
""", unsafe_allow_html=True)

# 6. المساعد الذكي (AI in Data)
with st.sidebar:
    st.header("🤖 AI Analysis Center")
    chat = st.text_input("اسأل المساعد عن بياناتك...")
    if chat:
        try:
            res = model.generate_content(chat)
            st.info(res.text)
        except Exception as e: st.error(f"Error: {e}")
    st.divider()
    st.markdown("### 📊 أدوات الربط")
    st.button("🔗 Google Sheets Connect")
    st.button("🔗 Power Query Engine")

# 7. التبويبات الرئيسية (الأدوات)
tab1, tab2, tab3, tab4 = st.tabs(["📑 Excel Pro", "📊 Power BI Dash", "🐍 Python Lab", "📄 Report PDF"])

with tab1:
    st.subheader("📝 Advanced Excel Sheet")
    uploaded_file = st.file_uploader("ارفع ملف Excel أو CSV", type=['xlsx', 'csv'])
    if uploaded_file:
        df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file)
        # عرض الإكسيل بشكل احترافي يشبه مايكروسوفت
        st.dataframe(df, use_container_width=True, height=400)
        st.success("الملف جاهز للتحليل")
        
with tab2:
    st.subheader("📈 Professional Dashboard")
    if uploaded_file:
        num_cols = df.select_dtypes(include=[np.number]).columns
        if len(num_cols) >= 2:
            fig = px.bar(df, x=df.columns[0], y=num_cols[0], color=num_cols[0], template="plotly_dark", color_continuous_scale="Viridis")
            st.plotly_chart(fig, use_container_width=True)
    else: st.warning("ارفع ملفاً أولاً لتوليد الداشبورد")

with tab3:
    st.subheader("🐍 Python Analysis Engine")
    code = st.text_area("اكتب كود البايثون هنا للتحليل المتقدم", "df.describe()")
    if st.button("Run Python"):
        st.code("Processing data with Python Engine...")

with tab4:
    st.subheader("🖨️ Final Report Center")
    if st.button("Download as PDF"):
        st.download_button("تحميل التقرير النهائي (PDF)", data=b"Report Content", file_name="Smart_Analyst_Report.pdf")

# 8. الفوتر
st.markdown("<div style='text-align: center; color: #fbbf24; padding: 20px;'>© 2026 Smart Analyst Ultimate | Powered by Gemini & Python</div>", unsafe_allow_html=True)
