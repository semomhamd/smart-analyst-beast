import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO
import urllib.parse

# 1. إعدادات الهوية (تم إخفاء التواريخ نهائياً)
st.set_page_config(page_title="Smart Analyst Beast PRO", page_icon="🦁", layout="wide")

if 'db' not in st.session_state: 
    st.session_state['db'] = pd.DataFrame(columns=['البند', 'القيمة'])

# القائمة المحدثة بناءً على طلبك الأخير
menu_items = [
    "الرئيسية", 
    "الاكسل برو", 
    "منظف البيانات", 
    "المحلل الذكي", 
    "الرسوم البيانيه", 
    "التقرير النهائي(pdf, المشاركه)"
]

# 2. السايد بار (MIA8444)
with st.sidebar:
    try:
        st.image("8888.jpg", use_column_width=True) 
    except:
        st.title("🦁 MIA8444 Beast")
    st.write("---")
    choice = st.radio("القائمة:", menu_items)
    st.write("---")
    st.caption("Signature: MIA8444")

# 3. تشغيل الصفحات

if choice == menu_items[0]: # الرئيسية
    st.header("Smart Analyst Beast")
    st.subheader("You don't have to be a data analyst.. Smart Analyst thinks for you")
    
    if st.button("🚀 توليد بيانات اختبار"):
        st.session_state['db'] = pd.DataFrame({
            'المنتج': ['موبايل', 'لاب توب', 'ساعة'] * 10,
            'المبيعات': np.random.randint(100, 5000, 30),
            'الكمية': np.random.randint(1, 20, 30)
        })
        st.success("تم شحن البيانات! اذهب للاكسل برو.")
    
    up = st.file_uploader("ارفع ملفك الخاص", type=["csv", "xlsx"])
    if up: 
        st.session_state['db'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
        st.success("تم الرفع بنجاح!")

elif choice == menu_items[1]: # الاكسل برو (المحرر والدوال والبيفوت مدمجين)
    st.header("📊 الاكسل برو")
    df = st.session_state['db']
    if not df.empty:
        st.subheader("📝 محرر البيانات (Excel Editor):")
        df_ed = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        st.session_state['db'] = df_ed
        
        st.write("---")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.subheader("🧮 الدوال:")
            num_cols = df_ed.select_dtypes(include=[np.number]).columns.tolist()
            if num_cols:
                target = st.selectbox("العمود:", num_cols)
                st.metric("المجموع", f"{df_ed[target].sum():,}")
                st.metric("المتوسط", f"{df_ed[target].mean():.2f}")
        with col2:
            st.subheader("📉 التحليل المحوري (Pivot):")
            if num_cols:
                idx = st.selectbox("الصفوف:", df_ed.columns)
                val = st.selectbox("القيم:", num_cols)
                pivot_res = df_ed.groupby(idx)[val].sum().reset_index()
                pivot_res.columns = [idx, f"إجمالي {val}"]
                st.dataframe(pivot_res, use_container_width=True)

elif choice == menu_items[2]: # منظف البيانات
    st.header("✨ منظف البيانات")
    df = st.session_state['db']
    if not df.empty and st.button("🚀 ابدأ التنظيف فوراً"):
        st.session_state['db'] = df.dropna(how='all').drop_duplicates().fillna(0)
        st.success("تم تنظيف البيانات بنجاح!")

elif choice == menu_items[3]: # المحلل الذكي
    st.header("🧠 المحلل الذكي")
    if not st.session_state['db'].empty:
        st.write("💡 ملخص إحصائي سريع:")
        st.dataframe(st.session_state['db'].describe())

elif choice == menu_items[4]: # الرسوم البيانيه
    st.header("📈 الرسوم البيانيه")
    df = st.session_state['db']
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if not df.empty and num_cols:
        x = st.selectbox("المحور الأفقي:", df.columns)
        y = st.selectbox("المحور الرأسي:", num_cols)
        st.plotly_chart(px.bar(df.head(50), x=x, y=y, color=y))

elif choice == menu_items[5]: # التقرير النهائي(pdf, المشاركه)
    st.header("📄 التقرير النهائي والمشاركه")
    if not st.session_state['db'].empty:
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            st.session_state['db'].to_excel(writer, index=False)
        st.download_button("📥 تحميل التقرير (Excel)", data=output.getvalue(), file_name="MIA8444_Report.xlsx")
        
        st.write("---")
        phone = st.text_input("رقم واتساب المدير:")
        if st.button("📲 مشاركة التقرير"):
            msg = "التقرير النهائي جاهز. التوقيع: MIA8444"
            url = f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"
            st.markdown(f'<a href="{url}" target="_blank">فتح واتساب للإرسال</a>', unsafe_allow_html=True)
