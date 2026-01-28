import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import duckdb
from io import BytesIO
from datetime import datetime

# ------------------ Page & Theme ------------------
st.set_page_config(page_title="Smart Analyst Beast", layout="wide")
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

bg_color = "#0e1117" if st.session_state.theme == "Dark" else "#ffffff"
text_color = "#D4AF37" if st.session_state.theme == "Dark" else "#000000"

st.markdown(f"""
<style>
.stApp {{ background-color: {bg_color}; color: {text_color}; }}
.header {{ display: flex; justify-content: space-between; align-items: center; }}
.footer {{ text-align: center; font-size: 12px; color: #888; padding: 5px; }}
</style>
""", unsafe_allow_html=True)

# ------------------ Header ------------------
cols = st.columns([3, 1, 1])
with cols[0]:
    st.image("8888.jpg", width=120)
with cols[1]:
    if st.button("🌐 AR/EN"):
        st.session_state.lang = "EN" if st.session_state.get("lang","AR")=="AR" else "AR"
with cols[2]:
    with st.expander("⚙️ Settings"):
        if st.button("Toggle Theme"):
            st.session_state.theme = "Light" if st.session_state.theme=="Dark" else "Dark"
            st.experimental_rerun()

# ------------------ Sidebar ------------------
tool = st.sidebar.radio(
    "Tools",
    ["Excel Grid", "Power BI View", "SQL Lab", "Report Engine"]
)

# ------------------ AI Core ------------------
def ai_core(mode="summary"):
    if "dataset" not in st.session_state or st.session_state.dataset.empty:
        return "No data available."
    df = st.session_state.dataset
    if mode=="summary":
        return f"Rows: {df.shape[0]}, Columns: {df.shape[1]}, Numeric Columns: {len(df.select_dtypes(include=np.number).columns)}"
    elif mode=="columns":
        return df.columns.tolist()

# ------------------ Excel Grid ------------------
if tool=="Excel Grid":
    st.header("📋 Excel-Like Grid with Manual Input")
    
    uploaded = st.file_uploader("Upload CSV/XLSX", type=["csv","xlsx"])
    
    if uploaded:
        try:
            if uploaded.name.endswith(".csv"):
                df = pd.read_csv(uploaded, dtype=object)
            else:
                df = pd.read_excel(uploaded, dtype=object)
            
            # تحويل الأعمدة التي يمكن تحويلها لتواريخ
            for col in df.columns:
                try:
                    df[col] = pd.to_datetime(df[col])
                except:
                    pass
            
            st.session_state.dataset = df
            st.success("Dataset Loaded ✅")
        except Exception as e:
            st.error(f"Error loading file: {e}")
    
    # إدخال بيانات يدوي
    if not st.session_state.dataset.empty:
        st.markdown("### Manual Data Input")
        edited_df = st.experimental_data_editor(st.session_state.dataset, num_rows="dynamic")
        st.session_state.dataset = edited_df
        st.markdown("### 🧠 AI Insight")
        st.write(ai_core("summary"))

# ------------------ Power BI View ------------------
elif tool=="Power BI View":
    st.header("📈 Power BI-Like Dashboard")
    if "dataset" not in st.session_state or st.session_state.dataset.empty:
        st.warning("Upload data first")
    else:
        df = st.session_state.dataset.copy()
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        if numeric_cols:
            col_x = st.selectbox("X Axis", df.columns)
            col_y = st.selectbox("Y Axis", numeric_cols)
            
            chart_df = df[[col_x, col_y]].dropna()
            chart_df[col_x] = chart_df[col_x].astype(str)
            
            chart = alt.Chart(chart_df).mark_bar(color="#D4AF37").encode(
                x=alt.X(col_x, sort=None),
                y=col_y
            ).properties(width=700, height=400)
            
            st.altair_chart(chart, use_container_width=True)
            st.markdown("### 🧠 AI Insight")
            st.write(ai_core("summary"))

# ------------------ SQL Lab ------------------
elif tool=="SQL Lab":
    st.header("🧪 SQL Lab")
    if "dataset" not in st.session_state or st.session_state.dataset.empty:
        st.warning("Upload data first")
    else:
        df = st.session_state.dataset
        query = st.text_area("Write SQL Query", "SELECT * FROM df LIMIT 10")
        if st.button("Run Query"):
            try:
                result = duckdb.query(query).df()
                st.dataframe(result)
            except Exception as e:
                st.error(str(e))

# ------------------ Report Engine ------------------
elif tool=="Report Engine":
    st.header("📄 Report Engine")
    if "dataset" not in st.session_state or st.session_state.dataset.empty:
        st.warning("Upload data first")
    else:
        st.markdown("### Dataset Overview")
        st.write(ai_core("summary"))
        st.dataframe(st.session_state.dataset.head(20))

        # PDF & WhatsApp Placeholder
        st.markdown("### 📤 Export / WhatsApp")
        st.button("Export as PDF with Logo & Signature MIA8444")
        st.button("Share on WhatsApp")
        
# ------------------ Footer ------------------
st.markdown(f"""
<div class="footer">
Property of Smart Analyst Beast | Signature MIA8444 | v1.0
</div>
""", unsafe_allow_html=True)
