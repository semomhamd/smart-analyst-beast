import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Smart Analyst Beast",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Smart Analyst Beast")
st.subheader("المنظومة الذكية للمحاسبة وتحليل البيانات")
st.divider()

st.sidebar.header("⚙️ لوحة التحكم")
choice = st.sidebar.radio(
    "اختر القسم:",
    ["Dashboard", "Data Analysis"]
)

if choice == "Dashboard":
    st.success("☀️ صباح الفل يا مدير")

    col1, col2, col3 = st.columns(3)
    col1.metric("إيرادات", "—")
    col2.metric("مصروفات", "—")
    col3.metric("صافي الربح", "—")

elif choice == "Data Analysis":
    st.subheader("📂 تحليل الملفات")

    file = st.file_uploader(
        "ارفع ملف CSV أو Excel",
        type=["csv", "xlsx"]
    )

    if file is not None:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        st.dataframe(df.head())
