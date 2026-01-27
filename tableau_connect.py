import streamlit as st
import pandas as pd

def run_tableau():
    st.markdown("<h2 style='text-align:center; color:#E97627;'>🖼️ محرك Tableau (Expert Mode)</h2>", unsafe_allow_html=True)

    if 'main_data' in st.session_state and st.session_state['main_data'] is not None:
        df = st.session_state['main_data']
        st.success("✅ البيانات جاهزة للتصدير لـ Tableau.")

        st.info("💡 نصيحة: Tableau بيحب ملفات الـ CSV عشان السرعة في الـ Large Data.")

        c1, c2 = st.columns([2, 1])
        with c1:
            csv = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 تصدير ملف .CSV لـ Tableau",
                data=csv,
                file_name="MIA8444_Tableau_Ready.csv",
                mime='text/csv'
            )
        
        with c2:
            st.write("🛠️ *الإعدادات:*")
            st.checkbox("تفعيل UTF-8 (للعربي)", value=True)

        st.markdown("---")
        st.write("📊 *توزيع البيانات المكتشفة:*")
        st.bar_chart(df.count()) # رسم بياني يوضح اكتمال البيانات في كل عمود
    else:
        st.warning("⚠️ مفيش بيانات يا صديقي. ارفع ملفك الأول عشان 'تابلوه' ينور.")

st.markdown("<p style='text-align:center; font-size:12px; color:#555;'>MIA8444 | Tableau Visualization Bridge</p>", unsafe_allow_html=True)
