import streamlit as st
import pandas as pd
import duckdb
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# ===============================
# Core Config
# ===============================
st.set_page_config(
    page_title="Smart Analyst Beast",
    page_icon="🧠",
    layout="wide"
)

# ===============================
# Session State
# ===============================
if "dataset" not in st.session_state:
    st.session_state.dataset = pd.DataFrame()

if "events" not in st.session_state:
    st.session_state.events = []

# ===============================
# AI CORE (Mock)
# ===============================
def ai_core(task):
    if task == "summary":
        return "Executive Summary: The data shows clear performance trends."
    if task == "formula":
        return "=SUM(A1:A10)"
    if task == "sql":
        return "SELECT * FROM data LIMIT 10;"
    return "AI Response"

# ===============================
# Data Bus
# ===============================
def publish_dataset(target):
    st.session_state.events.append({
        "time": str(datetime.now()),
        "target": target,
        "rows": len(st.session_state.dataset)
    })

# ===============================
# Sidebar
# ===============================
st.sidebar.title("Smart Analyst Beast")
tool = st.sidebar.radio(
    "Tools",
    ["Excel Grid", "Power BI View", "SQL Lab", "Report Engine"]
)

# ===============================
# Excel-like Grid
# ===============================
if tool == "Excel Grid":
    st.header("Excel-like Data Grid")

    uploaded = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded:
        st.session_state.dataset = pd.read_csv(uploaded)

    st.session_state.dataset = st.data_editor(
        st.session_state.dataset,
        num_rows="dynamic",
        use_container_width=True
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("AI Formula Suggest"):
            st.code(ai_core("formula"))

    with col2:
        if st.button("Publish Dataset"):
            publish_dataset("ALL")
            st.success("Dataset Published")

# ===============================
# Power BI-like View
# ===============================
elif tool == "Power BI View":
    st.header("BI Dashboard")

    if st.session_state.dataset.empty:
        st.warning("No data loaded")
    else:
        st.bar_chart(st.session_state.dataset.select_dtypes("number"))
        if st.button("AI Insight"):
            st.info(ai_core("summary"))

# ===============================
# SQL Lab
# ===============================
elif tool == "SQL Lab":
    st.header("SQL Lab")

    if st.session_state.dataset.empty:
        st.warning("No data available")
    else:
        con = duckdb.connect()
        con.register("data", st.session_state.dataset)

        query = st.text_area("SQL Query", ai_core("sql"))
        if st.button("Run Query"):
            result = con.execute(query).df()
            st.dataframe(result)

# ===============================
# Report Engine
# ===============================
elif tool == "Report Engine":
    st.header("Report & PDF Engine")

    if st.button("Generate PDF"):
        pdf_path = "Smart_Report.pdf"
        doc = SimpleDocTemplate(pdf_path)
        styles = getSampleStyleSheet()

        content = [
            Paragraph("Smart Analyst Report", styles["Title"]),
            Paragraph(ai_core("summary"), styles["Normal"]),
            Paragraph("Generated: " + str(datetime.now()), styles["Normal"]),
            Paragraph("Signature: MIA8444", styles["Normal"])
        ]

        doc.build(content)
        st.success("PDF Generated")
        st.download_button(
            "Download PDF",
            open(pdf_path, "rb"),
            file_name="Smart_Report.pdf"
        )

# ===============================
# Footer
# ===============================
st.markdown("---")
st.markdown(
    "<div style='text-align:center; opacity:0.6;'>"
    "Smart Analyst Beast | Signature: <b>MIA8444</b>"
    "</div>",
    unsafe_allow_html=True
)
