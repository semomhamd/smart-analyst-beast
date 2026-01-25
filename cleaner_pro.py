import streamlit as st
def apply_clean(df):
    st.markdown("### 🧹 Power Query Cleaner")
    if df is not None:
        st.success("Ready to clean your data!")
