import streamlit as st
import pandas as pd
import io
import sys

def run_python_app():
    st.markdown("<h2 style='text-align:center; color:#D4AF37;'>🐍 محرك بايثون الذكي (Python Beast)</h2>", unsafe_allow_html=True)

    # 1. فحص البيانات المتوفرة في الذاكرة
    if 'main_data' in st.session_state and st.session_state['main_data'] is not None:
        df = st.session_state['main_data']
        st.success("✅ البيانات جاهزة للتحليل البرمجي (المتغير df جاهز للاستخدام)")
        
        with st.expander("👁️ عرض هيكل البيانات (Columns & Types)"):
            st.write(df.dtypes)
            st.dataframe(df.head(5))

        st.markdown("---")
        
        # 2. منطقة كتابة الكود
        st.write("💻 *اكتب كود بايثون لتحليل البيانات:*")
        default_code = """# مثال: رسم بياني بسيط أو حسابات
# df['النتيجة'] = df['المبلغ'] * 1.14
st.write("إحصائيات البيانات:")
st.write(df.describe())
"""
        code_input = st.text_area("Python Script Editor", value=default_code, height=200)

        # 3. زرار التشغيل والتنفيذ
        if st.button("🚀 تشغيل الكود (Run Script)"):
            try:
                # بيئة لتنفيذ الكود وعرض النتائج
                st.markdown("### 🖥️ مخرجات الكود:")
                # تنفيذ الكود مع تمرير الـ df له
                exec_scope = {'df': df, 'st': st, 'pd': pd}
                exec(code_input, exec_scope)
                st.balloons()
            except Exception as e:
                st.error(f"❌ حدث خطأ في الكود: {e}")

    else:
        st.warning("⚠️ الذاكرة فارغة. الوحش محتاج بيانات عشان يحللها، ارجع للأدوات اللي فاتت أولاً.")
        st.info("💡 يمكنك كتابة كود بايثون حر هنا حتى لو مفيش بيانات:")
        free_code = st.text_area("Free Coding Space", "print('Hello MIA8444')")
        if st.button("Execute"):
            st.code("Output: Hello MIA8444")

# التوقيع MIA8444
st.markdown("<p style='text-align:center; font-size:12px; color:#555;'>MIA8444 | Python Analysis Engine</p>", unsafe_allow_html=True)
