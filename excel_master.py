import streamlit as st
import pandas as pd

def run_excel_app():
    st.markdown("<h2 style='text-align:center; color:#D4AF37;'>📊 محرر إكسيل الوحش</h2>", unsafe_allow_html=True)
    
    # 1. اختيار وضع العمل
    mode = st.radio("ماذا تريد أن تفعل؟", ["فتح شيت جديد (بيانات من الصفر)", "رفع ملف إكسيل موجود"], horizontal=True)

    if mode == "فتح شيت جديد (بيانات من الصفر)":
        st.info("💡 يمكنك إضافة صفوف وأعمدة وتعديل البيانات مباشرة.")
        
        # تحديد عدد الأعمدة والصفوف المبدئية
        col_set1, col_set2 = st.columns(2)
        with col_set1:
            row_count = st.number_input("عدد الصفوف المبدئي", min_value=1, value=10)
        with col_set2:
            col_count = st.number_input("عدد الأعمدة المبدئي", min_value=1, value=5)

        # إنشاء جدول بيانات فارغ
        columns = [f"العمود {i+1}" for i in range(col_count)]
        df_new = pd.DataFrame("", index=range(row_count), columns=columns)

        # المحرر التفاعلي (Data Editor)
        # num_rows="dynamic" بتسمح للمستخدم يزود ويمسح صفوف براحته
        edited_df = st.data_editor(df_new, use_container_width=True, num_rows="dynamic")
        
        # زر الحفظ في الذاكرة (للربط لاحقاً)
        if st.button("✅ حفظ البيانات في ذاكرة الوحش"):
            st.session_state['main_data'] = edited_df
            st.success("تم حفظ البيانات! جاهزة الآن للربط مع باقي الأدوات.")

    else:
        # وضع رفع الملفات
        uploaded_file = st.file_uploader("اختر ملف Excel أو CSV", type=['xlsx', 'csv'])
        if uploaded_file:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                st.write("📂 ملفك المرفوع:")
                # إتاحة تعديل الملف المرفوع أيضاً
                edited_upload = st.data_editor(df, use_container_width=True, num_rows="dynamic")
                
                if st.button("✅ اعتماد التعديلات وحفظها"):
                    st.session_state['main_data'] = edited_upload
                    st.success("تم تحديث البيانات وحفظها!")
            except Exception as e:
                st.error(f"حدث خطأ أثناء تحميل الملف: {e}")

# التوقيع
st.markdown("<p style='text-align:center; font-size:12px; color:#555;'>MIA8444 | Excel Master Engine</p>", unsafe_allow_html=True)
