import streamlit as st

def run_module():
    st.markdown("### 📈 Tableau Live Intelligence")
    # رابط تجريبي لداشبورد احترافي
    tableau_url = "https://public.tableau.com/views/Superstore_24/Overview"
    st.components.v1.iframe(tableau_url, height=800, scrolling=True)
