import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from fpdf import FPDF
import os
import google.generativeai as genai

# ================== CONFIG ==================
st.set_page_config(
    page_title="Smart Analyst Beast",
    page_icon="🐉",
    layout="wide"
)

# ================== LOGIN ==================
ADMIN_USER = "semomohamed"
ADMIN_PASS = "123456"

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🐉 Smart Analyst Beast")
    st.subheader("نظام التحليل المشفر – Production MVP")
    with st.form("login_form"):
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        submit = st.form_submit_button("دخول آمن")
        if submit:
            if user == ADMIN_USER and pw == ADMIN_PASS:
                st.session_state.logged_in = True
                st.success("تم تسجيل الدخول! 🚀")
                st.experimental_rerun()
            else:
                st.error("بيانات الدخول غير صحيحة")
    st.stop()

# ================== LOGO ==================
# رابط Raw صحيح من GitHub أو أي رابط مباشر للصورة
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
    "📂 رفع ودمج البيانات",
    "🧠 عقل الوحش (AI Explainer)",
    "📄 تصدير PDF"
])

# ---------- TAB 1 ----------
with tab1:
    st.subheader("رفع CSV / Excel")
    uploaded_files = st.file_uploader(
        "ارفع ملفات Excel أو CSV", type=["csv", "xlsx"], accept_multiple_files=True
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
                with st.expander(f"⚙️ معالجة: {file.name}"):
                    for l in logs:
                        st.info(l)
                all_dfs.append(df)
            except Exception as e:
                st.error(f"خطأ في {file.name}: {e}")

        if all_dfs:
            st.session_state.master_df = pd.concat(all_dfs, ignore_index=True)
            st.success("🔥 البيانات اتجهزت")
            st.dataframe(st.session_state.master_df, use_container_width=True)

# ---------- TAB 2 ----------
with tab2:
    if "master_df" not in st.session_state:
        st.warning("ارفع بيانات أولاً")
    elif not model:
        st.error("⚠️ Gemini API Key مش متظبط")
    else:
        if st.button("🧠 شغل عقل الوحش"):
            with st.spinner("الوحش بيفكر…"):
                df_head = st.session_state.master_df.head(50).to_string()
                prompt = f"""
                تحليل البيانات دي واديني:
                - ملخص
                - أهم الملاحظات
                - تحذيرات
                - اقتراحات
                البيانات:
                {df_head}
                """
                response = model.generate_content(prompt)
                st.session_state.ai_result = response.text
                st.success("✅ التحليل جاهز")

        if "ai_result" in st.session_state:
            st.markdown(st.session_state.ai_result)

# ---------- TAB 3 ----------
with tab3:
    if "ai_result" in st.session_state:
        if st.button("📄 تصدير PDF"):
            path = export_pdf(st.session_state.ai_result)
            with open(path, "rb") as f:
                st.download_button(
                    "⬇️ تحميل التقرير",
                    f,
                    file_name=path
                )
    else:
        st.info("اعمل تحليل AI الأول")

# ================== SIDEBAR ==================
st.sidebar.markdown("---")
st.sidebar.write("🐉 Smart Analyst Beast | MVP")
st.sidebar.caption("Developed with ❤️ by Smart Analyst")
