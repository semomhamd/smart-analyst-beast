import streamlit as st
import pandas as pd

def run_module():
    st.markdown("### 🐍 Python Analytics Engine")
    st.write("Advanced Statistical Modeling by MIA8444.")
    
    file = st.file_uploader("Upload Data for Python Analysis", type=['csv', 'xlsx'], key="py_beast")
    
    if file:
        df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
        st.write("📈 *Statistical Summary:*")
        st.write(df.describe())
        
        if st.checkbox("Show Correlation Matrix"):
            st.write(df.corr(numeric_only=True))
            st.success("Analysis Engine: Patterns identified!")
