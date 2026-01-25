import streamlit as st

def run_module():
    st.markdown("### 📊 Power BI Dashboard Hub")
    st.write("Engineered by MIA8444 for Executive Insights.")
    
    # مكان لوضع رابط التقرير (Embed Link)
    bi_url = st.text_input("Paste your Power BI Embed URL here:", placeholder="https://app.powerbi.com/reportEmbed?...")
    
    if bi_url:
        st.info("🔄 Beast is establishing a secure tunnel to Power BI Servers...")
        st.components.v1.iframe(bi_url, height=600, scrolling=True)
    else:
        st.warning("Please provide a Power BI link to activate the Live View.")
