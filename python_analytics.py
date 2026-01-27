import streamlit as st
import pandas as pd

def run_python_app():
    st.markdown("<h2 style='text-align:center; color:#D4AF37;'>🐍 محرك بايثون للتحليل (Python Beast)</h2>", unsafe_allow_html=True)

    if 'main_data' in st.session_state and st.session_state['main_data'] is not None:
        df = st.session_state['main_data']
        st.success("✅ البيانات جاهزة للتحليل البرمجي.")
        
        st.write("💻 *منطقة كتابة الأكواد:*")
        code = st.text_area("Python Script:", value="st.write(df.describe())\nst.line_chart(df)")
        
        if st.button("🚀 تشغيل الكود"):
            try:
                exec(code)
                st.balloons()
            except Exception as e:
                st.error(f"خطأ في الكود: {e}")
    else:
        st.warning("⚠️ ارجع للأداة الأولى وارفع بيانات الأول يا وحش.")

st.markdown("<p style='text-align:center; font-size:12px; color:#555;'>MIA8444 | Python Engine</p>", unsafe_allow_html=True)
