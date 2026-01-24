import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime

# =====================================================
# 1. إعدادات الصفحة
# =====================================================
st.set_page_config(
    page_title="Smart Analyst Beast",
    page_icon="🐉",
    layout="wide"
)

EXCEL_ICON = "https://cdn-icons-png.flaticon.com/512/732/732220.png"
CHART_ICON = "https://cdn-icons-png.flaticon.com/512/1611/1611177.png"

# =====================================================
# 2. Smart Data Cleaner (Production MVP)
# =====================================================
def smart_analyst_core(df: pd.DataFrame):
    cleaning_logs = []
    threshold = 0.95

    # --- حذف الأعمدة شبه الفارغة ---
    null_ratio = df.isnull().mean()
    cols_to_drop = null_ratio[null_ratio > threshold].index.tolist()

    if cols_to_drop:
        df = df.drop(columns=cols_to_drop)
        cleaning_logs.append(
            f"🗑️ تم حذف أعمدة شبه فارغة (>95%): {', '.join(cols_to_drop)}"
        )

    # --- اكتشاف وتوحيد التواريخ ---
    for col in df.columns:
        if df[col].dtype == "object":
            try:
                converted = pd.to_datetime(df[col], errors="coerce")
                success_ratio = converted.notna().mean()

                if success_ratio > 0.7:
                    sample_before = str(df[col].dropna().iloc[0]) if not df[col].dropna().empty else "—"
                    df[col] = converted
                    cleaning_logs.append(
                        f"📅 تم توحيد العمود '{col}' كتاريخ (مثال: {sample_before} → ISO)"
                    )
            except Exception:
                continue

    # --- اكتشاف القيم الشاذة (IQR) ---
    num_cols = df.select_dtypes(include=[np.number]).columns

    for col in num_cols:
        if df[col].nunique() < 5:
            continue

        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        if IQR == 0:
            continue

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        outliers_count = ((df[col] < lower) | (df[col] > upper)).sum()

        if outliers_count > 0:
            cleaning_logs.append(
                f"⚠️ تم رصد {outliers_count} قيم غير طبيعية في '{col}' (لم يتم حذفها)"
            )

    return df, cleaning_logs

# =====================================================
# 3. نظام الدخول الآمن
# =====================================================
ADMIN_USER = os.getenv("SA_USER")
ADMIN_PASS = os.getenv("SA_PASS")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🐉 Smart Analyst")
    st.subheader("نظام التحليل الذكي – دخول آمن")

    with st.form("login_form"):
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        submit = st.form_submit_button("دخول")

        if submit:
            if user == ADMIN_USER and pw == ADMIN_PASS:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("بيانات الدخول غير صحيحة")

    st.stop()

# =====================================================
# 4. الواجهة الرئيسية
# =====================================================
st.title("🚀 Smart Analyst Beast")
st.caption(f"مرحباً محمد | {datetime.now().strftime('%Y-%m-%d')}")

t1, t2 = st.tabs(["📂 إدارة البيانات", "🧠 تحليل الذكاء الاصطناعي"])

# =====================================================
# 5. تبويب رفع وإدارة البيانات
# =====================================================
with t1:
    st.image(EXCEL_ICON, width=50)
    st.subheader("رفع ودمج الملفات")

    uploaded_files = st.file_uploader(
        "ارفع ملفات Excel أو CSV",
        accept_multiple_files=True,
        type=["csv", "xlsx", "xls"]
    )

    if uploaded_files:
        all_dfs = []
        all_logs = []

        for file in uploaded_files:
            try:
                if file.name.endswith(("xlsx", "xls")):
                    df = pd.read_excel(file)
                else:
                    df = pd.read_csv(file)

                df, logs = smart_analyst_core(df)

                with st.expander(f"⚙️ معالجة الملف: {file.name}"):
                    for log in logs:
                        st.info(log)

                all_logs.extend(logs)
                all_dfs.append(df)

            except Exception as e:
                st.error(f"❌ خطأ في الملف {file.name}: {e}")

        if all_dfs:
            st.session_state.master_df = pd.concat(all_dfs, ignore_index=True)
            st.session_state.cleaning_logs = all_logs

            st.toast("🐉 تم دمج وتنظيف البيانات بنجاح", icon="🎉")
            st.markdown("---")
            st.subheader("📋 قاعدة بيانات الوحش الموحدة")

            st.data_editor(
                st.session_state.master_df,
                use_container_width=True,
                disabled=True
            )

# =====================================================
# 6. تبويب AI Explainer (جاهز للربط)
# =====================================================
with t2:
    st.image(CHART_ICON, width=50)
    st.subheader("عقل الوحش (AI Explainer)")

    if "master_df" in st.session_state:
        st.success("البيانات جاهزة للتحليل الذكي")

        if st.button("🧠 شغّل عقل الوحش"):
            st.info(
                "الخطوة التالية: إرسال البيانات + Logs + Summary إلى Gemini لشرح ذكي."
            )
    else:
        st.warning("من فضلك ارفع البيانات أولاً")

# =====================================================
# 7. الشريط الجانبي
# =====================================================
st.sidebar.markdown("---")
st.sidebar.write("🐉 Smart Analyst MVP")
st.sidebar.write("Powered by Gemini | 2026")
