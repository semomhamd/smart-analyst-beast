import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO
import urllib.parse

# --- 1. الإعدادات والهوية MIA8444 ---
st.set_page_config(page_title="Smart Analyst Beast PRO", page_icon="🦁", layout="wide")

if 'db' not in st.session_state: 
    st.session_state['db'] = pd.DataFrame(columns=['البند', 'القيمة'])

# القائمة المنظمة كما طلبت (بدون Pivot مستقل)
menu_items = [
    "الرئيسية", 
    "اكسل برو (المحرر والدوال والـ Pivot)", 
    "منظف البيانات (Cleaner)", 
    "المحلل الذكي (AI Analyst)", 
    "الرسوم البيانية", 
    "التقارير والمشاركة واتساب"
]

# --- 2. السايد بار ---
with st.sidebar:
    st.title("🦁 MIA8444 Beast")
    st.write("---")
    choice = st.radio("قائمة التحكم:", menu_items)
    st.write("---")
    st.caption("Developed by MIA8444")

# --- 3. تشغيل الصفحات ---

if choice == menu_items[0]: # الرئيسية
    st.header("Smart Analyst Beast")
    st.subheader("You don't have to be a data analyst.. Smart Analyst thinks for you") [cite: 2026-01-24]
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        if st.button("🚀 توليد بيانات اختبار فورية"):
            st.session_state['db'] = pd.DataFrame({
                'المنتج': ['موبايل', 'لاب توب', 'ساعة'] * 10,
                'المبيعات': np.random.randint(100, 5000, 30),
                'الكمية': np.random.randint(1, 20, 30)
            })
            st.success("تم شحن البيانات! اذهب للإكسيل برو.")
    
    up = st.file_uploader("أو ارفع ملفك الخاص", type=["csv", "xlsx"])
    if up: 
        st.session_state['db'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
        st.success("تم الرفع بنجاح!")

elif choice == menu_items[1]: # 📊 اكسل برو (الكل في واحد)
    st.header("📊 Excel Pro Workspace") [cite: 2026-01-15]
    df = st.session_state['db']
    
    if not df.empty:
        # 1. المحرر الاحترافي (إضافة/حذف/تعديل)
        st.subheader("📝 محرر البيانات الذكي:")
        df_ed = st.data_editor(df, num_rows="dynamic", use_container_width=True, key="main_editor")
        st.session_state['db'] = df_ed
        
        st.write("---")
        
        # 2. قسم الدوال والتحليل (Pivot & Functions)
        col_f1, col_f2 = st.columns([1, 2])
        
        with col_f1:
            st.subheader("🧮 دوال الإكسيل (Quick Calc):") [cite: 2025-11-13]
            num_cols = df_ed.select_dtypes(include=[np.number]).columns.tolist()
            if num_cols:
                target_col = st.selectbox("اختر العمود:", num_cols)
                st.metric("المجموع (SUM)", f"{df_ed[target_col].sum():,}")
                st.metric("المتوسط (AVERAGE)", f"{df_ed[target_col].mean():.2f}") [cite: 2025-11-13, 2026-01-20]
                st.metric("أعلى قيمة (MAX)", f"{df_ed[target_col].max():,}")
            else:
                st.info("أدخل أرقاماً لتفعيل الدوال.")

        with col_f2:
            st.subheader("📉 الـ Pivot Table المدمج:")
            if num_cols:
                p_c1, p_c2 = st.columns(2)
                with p_c1: p_idx = st.selectbox("الصفوف:", df_ed.columns, key="p_idx")
                with p_c2: p_val = st.selectbox("القيم:", num_cols, key="p_val")
                
                pivot_data = df_ed.groupby(p_idx)[p_val].sum().reset_index()
                pivot_data.columns = [p_idx, f"إجمالي {p_val}"]
                st.dataframe(pivot_data, use_container_width=True)
            else:
                st.warning("لا توجد بيانات رقمية للتحليل المحوري.")
    else:
        st.warning("يرجى رفع بيانات أو توليد ملف اختبار أولاً.")

elif choice == menu_items[2]: # Cleaner
    st.header("✨ Smart Data Cleaner") [cite: 2026-01-17]
    df = st.session_state['db']
    if not df.empty:
        if st.button("🚀 تنظيف البيانات MIA8444"):
            st.session_state['db'] = df.dropna(how='all').drop_duplicates().fillna(0)
            st.success("تم التنظيف وتصفير الفراغات!")
            st.rerun()

elif choice == menu_items[5]: # التقارير وواتساب
    st.header("📄 مركز التقارير")
    if not st.session_state['db'].empty:
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            st.session_state['db'].to_excel(writer, index=False)
        st.download_button("📥 تحميل التقرير (Excel)", data=output.getvalue(), file_name="MIA8444_Beast.xlsx")
        
        st.write("---")
        phone = st.text_input("رقم واتساب المدير:")
        if st.button("📲 إرسال إشعار"):
            msg = "التقرير جاهز يا فندم. التوقيع: MIA8444"
            url = f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"
            st.markdown(f'<a href="{url}" target="_blank">فتح واتساب</a>', unsafe_allow_html=True)
