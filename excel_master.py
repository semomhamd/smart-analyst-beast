import streamlit as st
import pandas as pd

def run_excel_app():
    st.markdown("<h2 style='text-align:center; color:#D4AF37;'>📟 محطة إكسيل الوحش (MIA8444)</h2>", unsafe_allow_html=True)

    # مخزن البيانات (لو مش موجود بنعمل واحد افتراضي)
    if 'main_data' not in st.session_state or st.session_state['main_data'] is None:
        st.session_state['main_data'] = pd.DataFrame([[0]*5 for _ in range(10)], columns=[f"Column {i+1}" for i in range(5)])

    # شريط أدوات سريع
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("➕ صف جديد"):
            new_row = pd.DataFrame([[0]*len(st.session_state['main_data'].columns)], columns=st.session_state['main_data'].columns)
            st.session_state['main_data'] = pd.concat([st.session_state['main_data'], new_row], ignore_index=True)
            st.rerun()
    with c2:
        if st.button("🗑️ مسح الشيت"):
            st.session_state['main_data'] = pd.DataFrame([[0]*5 for _ in range(10)], columns=[f"Column {i+1}" for i in range(5)])
            st.rerun()
    with c3:
        up = st.file_uploader("دمج ملف", type=['xlsx', 'csv'], label_visibility="collapsed")
        if up:
            st.session_state['main_data'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
            st.rerun()

    # المحرر الرئيسي - لا يسقط أبداً لأنه مرتبط بالـ session_state مباشرة
    st.write("📝 *محرر البيانات التفاعلي:*")
    edited_df = st.data_editor(
        st.session_state['main_data'],
        use_container_width=True,
        num_rows="dynamic",
        key="master_editor_key"
    )
    st.session_state['main_data'] = edited_df

    # العمليات الحسابية والرسوم
    st.markdown("---")
    numeric_df = edited_df.apply(pd.to_numeric, errors='coerce').fillna(0)
    
    tab1, tab2, tab3 = st.tabs(["🧮 الحسابات", "📈 الرسم البياني", "📱 واتساب"])
    
    with tab1:
        if not numeric_df.empty:
            for col in numeric_df.columns:
                col_sum = numeric_df[col].sum()
                if col_sum != 0:
                    st.metric(f"إجمالي {col}", f"{col_sum:,.2f}", f"Avg: {numeric_df[col].mean():,.2f}")
    
    with tab2:
        if not numeric_df.empty:
            sel = st.selectbox("اختر العمود:", numeric_df.columns)
            st.bar_chart(numeric_df[sel])
            
    with tab3:
        phone = st.text_input("رقم الواتساب (بالكود الدولي)")
        if st.button("إرسال التقرير"):
            import urllib.parse
            msg = f"تقرير الوحش MIA8444\nمجموع البيانات: {numeric_df.sum().sum()}"
            st.markdown(f"[فتح واتساب لإرسال البيانات](https://wa.me/{phone}?text={urllib.parse.quote(msg)})")

st.markdown("<p style='text-align:center; color:#555;'>MIA8444 | Pro Workspace</p>", unsafe_allow_html=True)
