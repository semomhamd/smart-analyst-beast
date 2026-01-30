import streamlit as st
import pandas as pd
import os

# إعدادات MIA8444
st.set_page_config(page_title="Smart Analyst Beast PRO", layout="wide")

if 'manual_df' not in st.session_state:
    # جدول مبدئي فيه أعمدة للحسابات
    st.session_state['manual_df'] = pd.DataFrame(
        [['منتج 1', 10, 5, 0], ['منتج 2', 20, 3, 0]], 
        columns=['البيان', 'الكمية', 'السعر', 'الإجمالي']
    )

with st.sidebar:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_container_width=True)
    st.write("---")
    st.success("✅ المرحلة 1: الشيت اليدوي")
    st.success("🚀 المرحلة 2: محرك الدوال (Active)")
    st.caption("Signature: MIA8444")

st.markdown("<h1 style='text-align: center;'>Smart Analyst</h1>", unsafe_allow_html=True)

# عرض الجدول للتعديل
st.subheader("📝 جدول البيانات والمعادلات")
edited_df = st.data_editor(
    st.session_state['manual_df'], 
    num_rows="dynamic", 
    use_container_width=True,
    key="formula_editor"
)

if st.button("⚡ تنفيذ الدوال وحفظ البيانات"):
    try:
        # تحويل الأعمدة لأرقام عشان الحسابات ما تضربش
        edited_df['الكمية'] = pd.to_numeric(edited_df['الكمية'], errors='coerce').fillna(0)
        edited_df['السعر'] = pd.to_numeric(edited_df['السعر'], errors='coerce').fillna(0)
        
        # 1. دالة الضرب التلقائي (الكمية × السعر)
        edited_df['الإجمالي'] = edited_df['الكمية'] * edited_df['السعر']
        
        st.session_state['manual_df'] = edited_df
        st.success("تم تنفيذ العمليات الحسابية بنجاح! MIA8444")
        
        # 2. ملخص الدوال الأساسية (SUM / AVG / COUNT) [cite: 2025-11-13]
        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("إجمالي المبالغ (SUM)", f"{edited_df['الإجمالي'].sum():,.2f}")
        with c2: st.metric("متوسط الأسعار (AVG)", f"{edited_df['السعر'].mean():,.2f}")
        with c3: st.metric("عدد البنود (COUNT)", f"{len(edited_df)}")
        
    except Exception as e:
        st.error(f"حصلت مشكلة في الحساب: {e}")
