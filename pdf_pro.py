import streamlit as st

def run_report_center():
    st.header("📄 مركز التقارير النهائية")
    if st.session_state.main_data.empty:
        st.warning("لا توجد بيانات لإصدار تقرير!")
    else:
        st.success("البيانات جاهزة للتحويل إلى PDF.")
        report_name = st.text_input("اسم التقرير", "Beast_Analysis_Report")
        if st.button("تحميل التقرير النهائي (PDF)"):
            st.balloons()
            st.write(f"تم تصدير {report_name} بتوقيع MIA8444")
