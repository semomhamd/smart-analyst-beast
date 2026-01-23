import streamlit as st
import pandas as pd

# 1. إعدادات واجهة "الوحش التقني"
st.set_page_config(page_title="Smart Analyst Beast", layout="wide")

# 2. تصميم العنوان
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🤖 Smart Analyst Beast</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>المنظومة الذكية للمحاسبة وتحليل البيانات</h3>", unsafe_allow_html=True)
st.divider()

# 3. القائمة الجانبية
with st.sidebar:
    st.header("⚙️ لوحة التحكم")
    choice = st.radio("اختر القسم:", ["Dashboard", "Data Analysis"])

# 4. قسم الداشبورد (اللي ظهر في صورتك)
if choice == "Dashboard":
    st.success("صباح الفل يا مدير! ☀️")
    col1, col2, col3 = st.columns(3)
    col1.metric("الإيرادات", "0", "0%")
    col2.metric("المصروفات", "0", "0%")
    col3.metric("صافي الربح", "0", "0%")

# 5. قسم تحليل البيانات (ربط الإكسل)
if choice == "Data Analysis":
    st.header("📊 معالج البيانات الذكي")
    file = st.file_uploader("ارفع ملف الإكسل (xlsx أو csv):", type=['xlsx', 'csv'])
    
    if file:
        # قراءة الملف أوتوماتيكياً
        df = pd.read_excel(file) if file.name.endswith('xlsx') else pd.read_csv(file)
        st.write("✅ تم قراءة الملف! إليك أول 5 صفوف:")
        st.dataframe(df.head())
        
        # استخراج الأعمدة اللي فيها أرقام بس
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if numeric_cols:
            col_to_analyze = st.selectbox("اختار العمود عشان أحسبه:", numeric_cols)
            
            # حساب المعادلات المحاسبية
            total = df[col_to_analyze].sum()
            avg = df[col_to_analyze].mean()
            
            # عرض النتائج في مربعات شيك
            st.divider()
            c1, c2 = st.columns(2)
            c1.metric(f"إجمالي {col_to_analyze} (SUM)", f"{total:,.2f}")
            c2.metric(f"متوسط {col_to_analyze} (AVERAGE)", f"{avg:,.2f}")
        else:
            st.warning("الملف ده مفيش فيه أرقام عشان أحسبها يا مدير!")
