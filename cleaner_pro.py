import streamlit as st
import pandas as pd

def run_cleaner():
    st.markdown("<h2 style='text-align:center; color:#D4AF37;'>🧹 منظف البيانات الاحترافي (Cleaner Pro)</h2>", unsafe_allow_html=True)

    # التحقق من وجود بيانات في الذاكرة المركزية
    if 'main_data' in st.session_state and st.session_state['main_data'] is not None:
        df = st.session_state['main_data']
        st.info("✅ البيانات محملة وجاهزة للتنظيف.")
        
        st.write("📊 معاينة البيانات:")
        st.dataframe(df.head(10), use_container_width=True)

        st.markdown("---")
        st.write("🛠️ *أدوات التنظيف السريع:*")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("🗑️ مسح الصفوف الفارغة"):
                st.session_state['main_data'] = df.dropna(how='all')
                st.success("تم مسح الفراغات!")
                st.rerun()

        with c2:
            if st.button("✨ إزالة التكرارات"):
                st.session_state['main_data'] = df.drop_duplicates()
                st.success("تم إزالة المتكرر!")
                st.rerun()

        with c3:
            if st.button("🔢 إصلاح الأرقام"):
                numeric_df = df.apply(pd.to_numeric, errors='coerce').fillna(0)
                st.session_state['main_data'] = numeric_df
                st.success("تم توحيد الأرقام!")
                st.rerun()

        st.markdown("---")
        if st.button("💾 اعتماد وحفظ البيانات"):
            st.balloons()
            st.success("تم حفظ النسخة المنظفة بنجاح في ذاكرة الوحش!")
    else:
        st.warning("⚠️ الذاكرة فارغة. ارفع ملف في 'إكسيل' أولاً.")

st.markdown("<p style='text-align:center; font-size:12px; color:#555;'>MIA8444 | Data Cleaning Engine</p>", unsafe_allow_html=True)
