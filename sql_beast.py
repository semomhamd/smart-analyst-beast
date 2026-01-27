import streamlit as st
import pandas as pd

def run_sql_app():
    st.markdown("<h2 style='text-align:center; color:#D4AF37;'>🗄️ محرك قواعد البيانات (SQL Beast)</h2>", unsafe_allow_html=True)

    # 1. التحقق من وجود بيانات جاهزة
    if 'main_data' in st.session_state and st.session_state['main_data'] is not None:
        df = st.session_state['main_data']
        st.success("✅ تم استلام البيانات المنظفة وجاهزة للتحويل إلى SQL.")
        
        st.write("📊 معاينة سريعة للبيانات:")
        st.dataframe(df.head(5), use_container_width=True)

        st.markdown("---")
        
        # 2. إعدادات تحويل الجدول لـ SQL
        col1, col2 = st.columns(2)
        with col1:
            table_name = st.text_input("اسم الجدول في قاعدة البيانات", value="MIA8444_Table")
        with col2:
            db_type = st.selectbox("نوع قاعدة البيانات", ["MySQL", "PostgreSQL", "SQL Server", "SQLite"])

        if st.button("🚀 توليد كود الـ Create & Insert"):
            # توليد كود CREATE TABLE تلقائي
            cols_types = []
            for col in df.columns:
                cols_types.append(f"[{col}] NVARCHAR(MAX)") # تنسيق عام
            
            create_query = f"CREATE TABLE {table_name} (\n  " + ",\n  ".join(cols_types) + "\n);"
            
            # توليد كود INSERT
            st.markdown("### 📜 الكود الناتج:")
            st.code(create_query, language="sql")
            
            # عرض أول 5 صفوف كأوامر Insert كمثال
            insert_statements = []
            for _, row in df.head(5).iterrows():
                values = "','".join([str(v).replace("'", "''") for v in row.values])
                insert_statements.append(f"INSERT INTO {table_name} VALUES ('{values}');")
            
            st.code("\n".join(insert_statements), language="sql")
            st.info("💡 يمكنك نسخ هذا الكود وتشغيله مباشرة في مدير قاعدة البيانات الخاص بك.")

    else:
        st.warning("⚠️ الذاكرة فارغة. ارفع ملف أو استخدم الـ OCR أولاً.")
        st.info("يمكنك أيضاً كتابة استعلام SQL يدوي هنا:")
        manual_query = st.text_area("SQL Query Editor", placeholder="SELECT * FROM users WHERE id = MIA8444...")
        if st.button("Run Query (Simulated)"):
            st.error("يرجى ربط قاعدة البيانات أولاً من الإعدادات.")

# التوقيع MIA8444
st.markdown("<p style='text-align:center; font-size:12px; color:#555;'>MIA8444 | SQL Beast Engine</p>", unsafe_allow_html=True)
