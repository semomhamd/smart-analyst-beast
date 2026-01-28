import streamlit as st
import pandas as pd
import numpy as np
import duckdb
from datetime import datetime

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Smart Analyst Beast",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# SESSION STATE INIT
# =========================
if "dataset" not in st.session_state:
    st.session_state.dataset = pd.DataFrame()

if "dataset_version" not in st.session_state:
    st.session_state.dataset_version = 0

if "events" not in st.session_state:
    st.session_state.events = []

# =========================
# STYLES
# =========================
st.markdown("""
<style>
.stApp { background-color:#0e1117; color:#d4af37; }
.tool-indicator { font-size:14px; margin-bottom:6px; }
.footer {
    position:fixed;
    bottom:0;
    width:100%;
    text-align:center;
    font-size:12px;
    color:#777;
}
</style>
""", unsafe_allow_html=True)

# =========================
# AI CORE (Mock – Ready for GPT)
# =========================
def ai_core(task, context=None):
    if task == "formula":
        return "=(Current - Previous) / Previous"
    if task == "summary":
        return "📌 ملخص تنفيذي: البيانات تشير إلى تحسن في الأداء مع وجود تراجع في بعض البنود التشغيلية."
    if task == "sql":
        return "SELECT * FROM data LIMIT 10;"
    return "AI response"

# =========================
# DATA BUS
# =========================
def publish_dataset():
    st.session_state.dataset_version += 1
    event = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "version": st.session_state.dataset_version,
        "rows": len(st.session_state.dataset),
        "cols": len(st.session_state.dataset.columns)
    }
    st.session_state.events.append(event)
    st.success(f"Dataset Published | Version v{event['version']}")

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.image("8888.jpg", use_column_width=True)
    st.markdown("### Tools Status")

    def indicator(name, ready):
        color = "🟢" if ready else "🟡"
        st.markdown(f"{color} {name}", unsafe_allow_html=True)

    indicator("Excel Grid", not st.session_state.dataset.empty)
    indicator("Power BI View", not st.session_state.dataset.empty)
    indicator("SQL Lab", not st.session_state.dataset.empty)
    indicator("Report Engine", not st.session_state.dataset.empty)

    tool = st.radio("Tools", [
        "Excel Grid",
        "Power BI View",
        "SQL Lab",
        "Report & PDF"
    ])

# =========================
# EXCEL-LIKE GRID
# =========================
if tool == "Excel Grid":
    st.header("📊 Excel-like Data Grid")

    uploaded = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded:
        st.session_state.dataset = pd.read_csv(uploaded)

    if st.session_state.dataset.empty:
        st.info("No data loaded")
    else:
        edited_df = st.data_editor(
            st.session_state.dataset,
            num_rows="dynamic",
            use_container_width=True
        )
        st.session_state.dataset = edited_df

        col1, col2 = st.columns(2)

        with col1:
            st.text_input(
                "AI Formula Suggest",
                value=ai_core("formula"),
                disabled=True
            )

        with col2:
            if st.button("🚀 Publish Dataset"):
                publish_dataset()

# =========================
# POWER BI LIKE VIEW
# =========================
elif tool == "Power BI View":
    st.header("📈 Power BI-like Dashboard")

    if st.session_state.dataset.empty:
        st.warning("Publish data first")
    else:
        df = st.session_state.dataset

        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        col_x = st.selectbox("X Axis", df.columns)
        col_y = st.selectbox("Y Axis", numeric_cols)

        st.bar_chart(df[[col_x, col_y]].set_index(col_x))

        st.info("Insight")
        st.write(ai_core("summary"))

# =========================
# SQL LAB
# =========================
elif tool == "SQL Lab":
    st.header("🗄️ SQL Lab")

    if st.session_state.dataset.empty:
        st.warning("No data available")
    else:
        con = duckdb.connect()
        con.register("data", st.session_state.dataset)

        query = st.text_area("SQL Query", ai_core("sql"))
        if st.button("Run Query"):
            result = con.execute(query).df()
            st.dataframe(result)

# =========================
# REPORT & PDF
# =========================
elif tool == "Report & PDF":
    st.header("📄 Report Engine")

    if st.session_state.dataset.empty:
        st.warning("No data to report")
    else:
        st.subheader("Executive Summary")
        st.write(ai_core("summary"))

        st.subheader("Preview Data")
        st.dataframe(st.session_state.dataset.head())

        if st.button("📤 Export PDF (WhatsApp Ready)"):
            st.success("PDF Generated ✔ (integration hook ready)")

# =========================
# FOOTER
# =========================
st.markdown("""
<div class="footer">
Smart Analyst Beast | Signature MIA8444
</div>
""", unsafe_allow_html=True)
