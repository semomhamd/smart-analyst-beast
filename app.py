import streamlit as st
import pandas as pd
import numpy as np

# =========================
# إعداد الصفحة
# =========================
st.set_page_config(
    page_title="Smart Analyst Beast",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# الحالة (Session State)
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = True

if "lang" not in st.session_state:
    st.session_state.lang = "ar"

# =========================
# اللغة
# =========================
LANG = {
    "ar": {
        "title": "📊 Smart Analyst Beast",
        "upload": "📤 رفع الملفات",
        "dashboard": "📈 لوحة التحكم",
        "tools": "🧰 أدوات التحليل",
        "logout": "تسجيل الخروج",
        "welcome": "صباح الفل يا مدير 😎",
        "file_hint": "ارفع ملف Excel / CSV / صورة فاتورة",
        "no_data": "مفيش بيانات لسه",
        "charts": "📊 الرسوم البيانية",
        "clean": "🧹 تنظيف البيانات (Power Query)",
    },
    "en": {
        "title": "📊 Smart Analyst Beast",
        "upload": "📤 Upload Files",
        "dashboard": "📈 Dashboard",
        "tools": "🧰 Analysis Tools",
        "logout": "Logout",
        "welcome": "Welcome Boss 😎",
        "file_hint": "Upload Excel / CSV / Invoice Image",
        "no_data": "No data yet",
        "charts": "📊 Charts",
        "clean": "🧹 Data Cleaning (Power Query)",
    }
}

L = LANG[st.session_state.lang]

# =========================
# الشريط الجانبي
# =========================
with st.sidebar:
    st.markdown(f"## {L['title']}")
    st.markdown("---")

    menu = st.radio(
        "القائمة",
        [L["upload"], L["dashboard"], L["tools"]],
        label_visibility="collapsed"
    )

    st.markdown("---")

    lang_choice = st.selectbox(
        "🌍 Language",
        ["ar", "en"],
        index=0 if st.session_state.lang == "ar" else 1
    )
    st.session_state.lang = lang_choice

    st.markdown("---")

    if st.button(f"🚪 {L['logout']}"):
        st.session_state.logged_in = False
        st.rerun()

# =========================
# العنوان
# =========================
st.markdown(f"# {L['welcome']}")

# =========================
# تخزين البيانات
# =========================
if "data" not in st.session_state:
    st.session_state.data = None

# =========================
# 📤 رفع الملفات
# =========================
if menu == L["upload"]:
    st.subheader(L["upload"])
    uploaded_file = st.file_uploader(
        L["file_hint"],
        type=["csv", "xlsx"]
    )

    if uploaded_file:
        if uploaded_file.name.endswith(".csv"):
            st.session_state.data = pd.read_csv(uploaded_file)
        else:
            st.session_state.data = pd.read_excel(uploaded_file)

        st.success("✅ تم تحميل الملف بنجاح")
        st.dataframe(st.session_state.data.head())

# =========================
# 📈 لوحة التحكم
# =========================
elif menu == L["dashboard"]:
    st.subheader(L["dashboard"])

    if st.session_state.data is None:
        st.warning(L["no_data"])
    else:
        df = st.session_state.data

        col1, col2, col3 = st.columns(3)
        col1.metric("عدد الصفوف", df.shape[0])
        col2.metric("عدد الأعمدة", df.shape[1])
        col3.metric("القيم الفارغة", df.isna().sum().sum())

        st.markdown("---")
        st.subheader(L["charts"])

        numeric_cols = df.select_dtypes(include=np.number).columns

        if len(numeric_cols) >= 1:
            st.line_chart(df[numeric_cols])
        else:
            st.info("لا توجد أعمدة رقمية للرسم")

# =========================
# 🧰 أدوات التحليل
# =========================
elif menu == L["tools"]:
    st.subheader(L["tools"])

    if st.session_state.data is None:
        st.warning(L["no_data"])
    else:
        df = st.session_state.data

        st.markdown(f"### {L['clean']}")
        if st.button("🧽 حذف الصفوف الفارغة"):
            df = df.dropna()
            st.session_state.data = df
            st.success("تم تنظيف البيانات")

        st.markdown("---")

        st.markdown("### 🔗 أدوات قادمة")
        st.write("""
        - 📊 Excel Analytics  
        - 🔥 Power BI Logic  
        - 🐍 Python Analysis  
        - 📉 Tableau Style Charts  
        - 📄 Google Sheets Sync  
        - 🤖 AI in Data Analysis  
        """)

# =========================
# الفوتر
# =========================
st.markdown("---")
st.caption("🚀 Built with love | Smart Analyst Beast")
