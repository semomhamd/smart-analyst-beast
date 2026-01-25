import streamlit as st

def apply_power_query(df):
    st.markdown("### 🧹 Power Query Cleaner")
    if df is not None:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔥 Auto-Clean (Fix Headers & Nulls)"):
                df.columns = [c.strip().upper().replace(" ", "_") for c in df.columns]
                df.dropna(how='all', inplace=True)
                st.success("Data is now Crystal Clear!")
        with col2:
            if st.button("🚫 Remove Duplicates"):
                df.drop_duplicates(inplace=True)
                st.success("Duplicates Purged!")
        st.dataframe(df)
        return df
    else:
        st.warning("Please upload data first in the Intake tab.")
    return df
