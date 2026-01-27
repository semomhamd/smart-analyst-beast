import streamlit as st
import pandas as pd

def run_cleaner():
    st.markdown("<h2 style='text-align:center; color:#D4AF37;'>🧹 منظف البيانات (Cleaner Pro)</h2>", unsafe_allow_html=True)

    # التحقق من وجود بيانات في "ذاكرة الوحش"
    if 'main_data' in st.session_state and st.session_state['main_data'] is not None:
        df = st.session_state['main_data']
        st.success("✅ تم العثور على بيانات في الذاكرة جاهزة للتنظيف.")
        
        st.write("📊 معاينة البيانات الحالية:")
        st.dataframe(df.head(10), use_container_width=True)

        st.markdown("---")
        st.write("🛠️ *أدوات التنظيف السريع:*")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🗑️ مسح الصفوف الفارغة"):
                df = df.dropna(how='all')
                st.session_state['main_data'] = df
                st.rerun()

        with col2:
            if st.button("✨ مسح التكرارات"):
                df = df.drop_duplicates()
                st.session_state['main_data'] = df
                st.rerun()

        with col3:
            if st.button("📅 توحيد تنسيق التاريخ"):
                # محاولة تحويل أي عمود فيه كلمة تاريخ لنسخة موحدة
                for col in df.columns:
                    if 'تاريخ' in col or 'date' in col.lower():
                        df[col] = pd.to_datetime(df[col], errors='coerce')
                st.session_state['main_data'] = df
                st.rerun()

        st.markdown("---")
        # خيارات متقدمة
        new_col_name = st.text_input("إعادة تسمية الأعمدة (اختياري)", placeholder="الاسم القديم: الاسم الجديد")
        
        if st.button("💾 حفظ البيانات المنظفة وإرسالها للأدوات"):
            st.session_state['main_data'] = df
            st.balloons()
            st.success("تم تنظيف البيانات بنجاح! جاهزة الآن للتصدير.")

    else:
        st.warning("⚠️ لا توجد بيانات في الذاكرة حالياً. ارفع ملف في 'إكسيل' أو استخدم الـ 'OCR' أولاً.")
        
        # خيار رفع ملف مباشرة في المنظف لو حابب
        uploaded_file = st.file_uploader("أو ارفع ملف جديد للتنظيف مباشرة هنا", type=['csv', 'xlsx'])
        if uploaded_file:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            st.session_state['main_data'] = df
            st.rerun()

# التوقيع MIA8444
st.markdown("<p style='text-align:center; font-size:12px; color:#555;'>MIA8444 | Data Cleaning Engine</p>", unsafe_allow_html=True)
