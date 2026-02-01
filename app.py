import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

# 1. إعدادات الواجهة (MIA8444)
st.set_page_config(page_title="Smart Analyst Beast", page_icon="🦁", layout="centered")

if 'db' not in st.session_state: 
    st.session_state['db'] = pd.DataFrame(columns=['البند', 'القيمة'])

# القائمة المنظمة (اليوم الثالث)
menu = ["الرئيسية", "منظف البيانات", "الاكسل برو", "المحلل الذكي", "الرسوم البيانيه", "التقرير النهائي"]

with st.sidebar:
    st.title("🦁 Beast MIA8444")
    choice = st.radio("القائمة:", menu)
    st.write("---")
    st.caption("Focus: Day 3 MVP")

# 2. تنفيذ الصفحات
if choice == menu[0]: # الرئيسية
    st.header("🏠 ارفع ملفك")
    up = st.file_uploader("ارفع Excel/CSV", type=["csv", "xlsx"])
    if up:
        try:
            st.session_state['db'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
            st.success("تم الرفع! اجهز يا محمد.")
        except Exception as e: st.error(f"خطأ: {e}")
    
    if st.button("🚀 تجربة ببيانات سريعة"):
        st.session_state['db'] = pd.DataFrame({'المنتج': ['أ', 'ب', 'ج']*5, 'المبيعات': np.random.randint(100,500,15)})

elif choice == menu[1]: # منظف البيانات
    st.header("✨ منظف البيانات")
    df = st.session_state['db']
    if not df.empty:
        if st.button("🚀 غسيل البيانات (حذف التكرار)"):
            st.session_state['db'] = df.dropna(how='all').drop_duplicates().fillna(0)
            st.success("البيانات بقت فلة!")

elif choice == menu[2]: # الاكسل برو (حل مشكلة الصورة 954afff6)
    st.header("📊 الاكسل برو")
    df = st.session_state['db']
    if not df.empty:
        df_ed = st.data_editor(df, use_container_width=True)
        st.session_state['db'] = df_ed
        
        num_cols = df_ed.select_dtypes(include=[np.number]).columns.tolist()
        if num_cols:
            st.write("---")
            target = st.selectbox("عمود الحساب (المبيعات):", num_cols)
            st.metric("المجموع", f"{df_ed[target].sum():,}")
            
            st.subheader("📉 ملخص Pivot ذكي")
            # الحل هنا: بنخلي العمود المختار للحساب ميبقاش موجود في خيارات التصنيف
            other_cols = [c for c in df_ed.columns if c != target]
            idx = st.selectbox("تصنيف حسب (اختر عمود مختلف):", other_cols if other_cols else df_ed.columns)
            
            # منع الـ ValueError عن طريق إعادة تسمية الأعمدة فوراً
            res = df_ed.groupby(idx)[target].sum().reset_index()
            res.columns = [idx, f"إجمالي {target}"] 
            st.dataframe(res, use_container_width=True)

elif choice == menu[5]: # التقرير النهائي
    st.header("📄 تصدير البيانات")
    if not st.session_state['db'].empty:
        buf = BytesIO()
        st.session_state['db'].to_excel(buf, index=False)
        st.download_button("📥 تحميل ملفك المعدل", buf.getvalue(), "MIA8444_Beast.xlsx")
