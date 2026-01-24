import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from fpdf import FPDF
import os
import google.generativeai as genai

# ================== CONFIG ==================
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if st.session_state.theme == 'dark':
    st.markdown(
        """<style>body{background-color:#111;color:white;}</style>""",
        unsafe_allow_html=True
    )

st.set_page_config(
    page_title="Smart Analyst Beast",
    page_icon="🐉",
    layout="wide"
)

# ================== Login ==================
ADMIN_USER = "semomohamed"
ADMIN_PASS = "123456"

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🐉 Smart Analyst Beast")
    st.subheader("نظام التحليل المشفر – Production MVP")
    
    # Language switcher
    if 'lang' not in st.session_state:
        st.session_state.lang = 'ar'
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("🇦🇪 عربي"):
            st.session_state.lang = 'ar'
            st.experimental_rerun()
    with col2:
        if st.button("🇺🇸 English"):
            st.session_state.lang = 'en'
            st.experimental_rerun()
    
    with st.form("login_form"):
        user = st.text_input("Username" if st.session_state.lang=='en' else "اسم المستخدم")
        pw = st.text_input("Password" if st.session_state.lang=='en' else "كلمة السر", type="password")
        submit = st.form_submit_button("Login" if st.session_state.lang=='en' else "دخول آمن")
        if submit:
            if user == ADMIN_USER and pw == ADMIN_PASS:
                st.session_state.logged_in = True
                st.success("✅ Login Success!" if st.session_state.lang=='en' else "تم تسجيل الدخول! 🚀")
                st.experimental_rerun()
            else:
                st.error("❌ Wrong credentials" if st.session_state.lang=='en' else "بيانات الدخول غير صحيحة")
    st.stop()

# ================== SIDEBAR ==================
st.sidebar.title("⚙️ Settings")
# Theme switcher
theme_choice = st.sidebar.radio("Theme / الوضع", ['Light','Dark'])
st.session_state.theme = 'dark' if theme_choice=='Dark' else 'light'

# ================== LOGO ==================
LOGO_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/99afc3d2-b6ef-4eda-977f-2fdc4b6621dd.jpg"
st.image(LOGO_URL, width=180, caption="Smart Analyst Beast 🐉")
st.title("🐉 Smart Analyst Beast – Production MVP")
st.caption("AI‑Powered Data Brain | Copy & Paste Ready")

# ================== GEMINI ==================
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-pro")
else:
    model = None

# ================== DATA CLEANER ==================
def smart_cleaner(df):
    logs = []
    before = df.shape[1]
    df = df.dropna(axis=1, how="all")
    if df.shape[1] != before:
        logs.append(f"🧹 حذف {before - df.shape[1]} عمود فاضي")
    for col in df.columns:
        if 'date' in col.lower() or 'تاريخ' in col:
            original_sample = str(df[col].iloc[0]) if not df[col].empty else ""
            df[col] = pd.to_datetime(df[col], errors='coerce')
            logs.append(f"📅 تحويل '{col}' لتاريخ (مثال: {original_sample} -> ISO)")
    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5*IQR
        upper = Q3 + 1.5*IQR
        outliers = ((df[col] < lower) | (df[col] > upper)).sum()
        if outliers > 0:
            logs.append(f"⚠️ اكتشاف {outliers} قيمة شاذة في '{col}'")
    return df, logs

# ================== PDF EXPORT ==================
def export_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        pdf.multi_cell(0, 8, line)
    path = f"Smart_Analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(path)
    return path

# ================== TABS ==================
tab1, tab2, tab3 = st.tabs([
    "📂 Upload & Merge / رفع البيانات",
    "🧠 AI Explainer / عقل الوحش",
    "📄 Export PDF / تصدير"
])

# ---------- TAB 1 ----------
with tab1:
    st.subheader("Upload CSV / Excel / رفع ملفات")
    uploaded_files = st.file_uploader(
        "Upload files or ارفع ملفات Excel/CSV", type=["csv", "xlsx"], accept_multiple_files=True
    )
    if uploaded_files:
        all_dfs = []
        for file in uploaded_files:
            try:
                if file.name.endswith(".csv"):
                    df = pd.read_csv(file)
                else:
                    df = pd.read_excel(file)
                df, logs = smart_cleaner(df)
                with st.expander(f"⚙️ Processed: {file.name}"):
                    for l in logs:
                        st.info(l)
                all_dfs.append(df)
            except Exception as e:
                st.error(f"Error in {file.name}: {e}")
        if all_dfs:
            st.session_state.master_df = pd.concat(all_dfs, ignore_index=True)
            st.success("🔥 Data Ready | البيانات جاهزة")
            st.dataframe(st.session_state.master_df, use_container_width=True)

# ---------- TAB 2 ----------
with tab2:
    if "master_df" not in st.session_state:
        st.warning("Upload data first / ارفع البيانات أولاً")
    elif not model:
        st.error("⚠️ Gemini API Key missing / مفتاح Gemini مش موجود")
    else:
        if st.button("🧠 Run AI / شغل العقل"):
            with st.spinner("Thinking… / الوحش بيفكر…"):
                df_head = st.session_state.master_df.head(50).to_string()
                prompt = f"""
                Analyze this data and give:
                - Summary
                - Insights
                - Warnings
                - Recommendations
                البيانات:
                {df_head}
                """
                response = model.generate_content(prompt)
                st.session_state.ai_result = response.text
                st.success("✅ Analysis Ready / التحليل جاهز")
        if "ai_result" in st.session_state:
            st.markdown(st.session_state.ai_result)

# ---------- TAB 3 ----------
with tab3:
    if "ai_result" in st.session_state:
        if st.button("📄 Export PDF / تصدير PDF"):
            path = export_pdf(st.session_state.ai_result)
            with open(path, "rb") as f:
                st.download_button(
                    "⬇️ Download / تحميل التقرير",
                    f,
                    file_name=path
                )
    else:
        st.info("Run AI first / شغل العقل الأول")

# ================== SIDEBAR ==================
st.sidebar.markdown("---")
st.sidebar.write("🐉 Smart Analyst Beast | MVP")
st.sidebar.caption("Developed with ❤️ by Smart Analyst")
