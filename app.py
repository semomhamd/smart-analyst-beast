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

# 4. قسم الداشبورد (اللي ظهر معاك في الصورة)
if choice == "Dashboard":
    st.success("صباح الفل يا مدير! ☀️")
    col1, col2, col3 = st.columns(3)
    col1.metric("الإيرادات", "0", "0%")
    col2.metric("المصروفات", "0", "0%")
    col3.metric("صافي الربح", "0", "0%")

# 5. قسم تحليل البيانات (الوحش الحقيقي)
if choice == "Data Analysis":
    st.header("📊 معالج البيانات الذكي")
    uploaded_file = st.file_uploader("ارفع ملف الإكسل هنا عشان أحسبلك الـ SUM والـ AVERAGE", type=['xlsx', 'csv'])
    
    if uploaded_file:
        # قراءة الملف
        df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file)
        st.write("✅ تم قراءة الملف بنجاح! إليك أول 5 صفوف:")
        st.dataframe(df.head())
        
        # اختيار العمود اللي فيه الأرقام
        column = st.selectbox("اختار العمود اللي عايز تحسبه:", df.columns)
        
        if column:
            total_sum = df[column].sum()
            average_val = df[column].mean()
            
            # عرض النتائج بشكل شيك
            c1, c2 = st.columns(2)
            c1.metric(f"إجمالي {column} (SUM)", f"{total_sum:,.2f}")
            c2.metric(f"متوسط {column} (AVERAGE)", f"{average_val:,.2f}")
