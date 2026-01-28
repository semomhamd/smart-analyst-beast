import streamlit as st
import pandas as pd
import numpy as np
import duckdb

# ------------------ Page Config ------------------
st.set_page_config(
    page_title="Smart Analyst Beast",
    page_icon="📊",
    layout="wide"
)

# ------------------ Session State ------------------
if "dataset" not in st.session_state:
    st.session_state.dataset = pd.DataFrame()

# ------------------ Helper AI Stub ------------------
def ai_core(mode="summary"):
    if st.session_state.dataset.empty:
        return "No data available yet."

    df = st.session_state.dataset

    if mode == "summary":
        return f"""
        📌 Rows: {df.shape[0]}
        📌 Columns: {df.shape[1]}
        📌 Numeric Columns: {len(df.select_dtypes(include=np.number).columns)}
        """

# ------------------ Sidebar ------------------
st.sidebar.title("🧠 Smart Analyst Beast")

tool = st.sidebar.radio(
    "Tools",
    [
        "Excel Grid",
        "Power BI View",
        "SQL Lab",
        "Report Engine"
    ]
)

# ------------------ Excel Grid ------------------
if tool == "Excel Grid":
    st.header("📋 Excel-Like Data Grid")

    uploaded = st.file_uploader(
        "Upload CSV",
        type=["csv"]
    )

    if uploaded:
        df = pd.read_csv(uploaded)
        st.session_state.dataset = df
        st.success("Dataset loaded successfully ✅")

    if not st.session_state.dataset.empty:
        st.dataframe(
            st.session_state.dataset,
            use_container_width=True
        )

        st.markdown("### 🧠 AI Insight")
        st.write(ai_core("summary"))

# ------------------ Power BI View ------------------
elif tool == "Power BI View":
    st.header("📈 Power BI-Like Dashboard")

    if st.session_state.dataset.empty:
        st.warning("Upload data first from Excel Grid")
    else:
        df = st.session_state.dataset.copy()

        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

        if not numeric_cols:
            st.error("No numeric columns found")
        else:
            col_x = st.selectbox("X Axis", df.columns)
            col_y = st.selectbox("Y Axis", numeric_cols)

            chart_df = df[[col_x, col_y]].dropna()
            chart_df[col_x] = chart_df[col_x].astype(str)

            st.bar_chart(
                data=chart_df,
                x=col_x,
                y=col_y
            )

            st.markdown("### 🧠 AI Insight")
            st.write(ai_core("summary"))

# ------------------ SQL Lab ------------------
elif tool == "SQL Lab":
    st.header("🧪 SQL Lab")

    if st.session_state.dataset.empty:
        st.warning("Upload data first from Excel Grid")
    else:
        df = st.session_state.dataset

        query = st.text_area(
            "Write SQL Query",
            "SELECT * FROM df LIMIT 10"
        )

        if st.button("Run Query"):
            try:
                result = duckdb.query(query).df()
                st.dataframe(result, use_container_width=True)
            except Exception as e:
                st.error(str(e))

# ------------------ Report Engine ------------------
elif tool == "Report Engine":
    st.header("📄 Report Engine")

    if st.session_state.dataset.empty:
        st.warning("Upload data first")
    else:
        st.markdown("### Dataset Overview")
        st.write(ai_core("summary"))

        st.markdown("### Preview")
        st.dataframe(
            st.session_state.dataset.head(20),
            use_container_width=True
        )

        st.success("Report generated successfully 🚀")
