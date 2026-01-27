import streamlit as st
import pandas as pd

def run_sql_app():
    st.markdown("<h2 style='text-align:center; color:#D4AF37;'>🗄️ محرك قواعد البيانات (SQL Beast)</h2>", unsafe_allow_html=True)

    if 'main_data' in st.session_state and st.session_state['main_data'] is not None:
        df = st.session_state['main_data']
        st.success("✅ البيانات جاهزة للتحويل لـ SQL.")
        
        table_name = st.text_input("اسم الجدول المقترح:", value="MIA8444_Table")
        
        if st.button("🚀 توليد كود SQL الآن"):
            # إنشاء كود CREATE TABLE
            cols = ", ".join([f"[{c}] NVARCHAR(MAX)" for c in df.columns])
            create_sql = f"CREATE TABLE {table_name} ({cols});"
            
            st.markdown("### 📜 كود إنشاء الجدول:")
            st.code(create_sql, language="sql")
            
            # إنشاء كود INSERT لأول 10 صفوف
            st.markdown("### 📝 أوامر إدخال البيانات:")
            insert_statements = []
            for _, row in df.head(10).iterrows():
                vals = "', '".join([str(v).replace("'", "''") for v in row.values])
                insert_statements.append(f"INSERT INTO {table_name} VALUES ('{vals}');")
            
            st.code("\n".join(insert_statements), language="sql")
            st.info("💡 انسخ الكود واستخدمه في SQL Server أو MySQL.")
    else:
        st.warning("⚠️ لا توجد بيانات. ابدأ من أداة الإكسيل أو الـ OCR أولاً.")

st.markdown("<p style='text-align:center; font-size:12px; color:#555;'>MIA8444 | SQL Database Engine</p>", unsafe_allow_html=True)
