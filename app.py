import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
from datetime import datetime, timedelta
# استيراد آمن للمكتبات الخارجية
try:
    from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode
except:
    st.error("⚠️ مكتبة st_aggrid ناقصة، تأكد من وجود streamlit-aggrid في ملف requirements.txt")

# --- 1. ذاكرة التطبيق الدائمة MIA8444 ---
if 'beast_vault' not in st.session_state:
    st.session_state['beast_vault'] = None

# إعداد الصفحة (يجب أن يكون أول أمر في Streamlit)
st.set_page_config(page_title="Smart Analyst Beast PRO", layout="wide", page_icon="🦁")

# --- 2. القائمة الرئيسية واللوجو (sidebar) ---
with st.sidebar:
    # محاولة عرض اللوجو
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_container_width=True)
    else:
        st.info("🦁 شعار Smart Analyst Beast")

    st.markdown("<h2 style='text-align: center;'>Smart Analyst Beast</h2>", unsafe_allow_html=True)
    st.write("---")
    
    # القائمة الكاملة والنهائية للجمهور
    menu_map = {
        "🏠 الرئيسية (بوابة الهوم)": "Home",
        "📥 استدعاء وتوليد البيانات": "Data",
        "📊 Excel Pro (المحاكي الأصلي)": "Excel",
        "🧠 المحلل الذكي (Smart Analyst)": "Analyst",
        "🔮 التنبؤ المالي (AI Forecast)": "Forecast",
        "🎯 التحليل الإستراتيجي": "Strategic",
        "🖥️ الداشبورد الأحدث (Beast Dash)": "Dash"
    }
    choice = st.radio("القائمة الإدارية:", list(menu_map.keys()))
    
    st.write("---")
    # زر توليد الـ 10,000 صف للاختبار
    if st.button("🚀 توليد 10,000 صف (اختبار تحمل)"):
        rows = 10000
        data = {
            'ID': range(1, rows + 1),
            'التاريخ': [datetime(2024, 1, 1) + timedelta(days=np.random.randint(0, 365)) for _ in range(rows)],
            'المنتج': [f"منتج_{np.random.randint(1, 100)}" for _ in range(rows)],
            'المبيعات': np.random.uniform(1000, 100000, size=rows),
            'الكمية': np.random.randint(1, 50, size=rows),
            'الفرع': [np.random.choice(['القاهرة', 'دبي', 'الرياض', 'لندن']) for _ in range(rows)],
            'التقييم': np.random.randint(1, 6, size=rows)
        }
        st.session_state['beast_vault'] = pd.DataFrame(data)
        st.success("✅ تم شحن الذاكرة بـ 10,000 صف!")
        st.rerun()

    st.caption("Owner Signature: MIA8444")

# سحب البيانات الحالية
df = st.session_state['beast_vault']

# --- 3. محرك الصفحات ---

if menu_map[choice] == "Home":
    st.title("🦁 بوابة الهوم - Smart Analyst Beast")
    st.markdown("""
    ### أهلاً بك في النسخة الاحترافية العامة.
    استخدم القائمة الجانبية للوصول لجميع الأدوات:
    - *Excel Pro*: لتعديل البيانات وإضافة المعادلات.
    - *Smart Analyst*: للتحليل الإحصائي الذكي.
    - *Data Center*: لرفع ملفاتك الخاصة.
    """)
    if df is not None:
        st.success(f"الوحش يعمل حالياً على تحليل {len(df)} صف.")

elif menu_map[choice] == "Data":
    st.header("📥 مركز إدارة واستدعاء البيانات")
    up = st.file_uploader("ارفع ملفك (Excel/CSV)", type=['xlsx', 'csv'])
    if up:
        st.session_state['beast_vault'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
        st.success("✅ تم استيراد البيانات بنجاح!")

elif menu_map[choice] == "Excel":
    st.header("📊 Excel Pro - محاكي الإكسل الأصلي")
    if df is not None:
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=20)
        gb.configure_default_column(editable=True, filterable=True, sortable=True)
        # تشغيل الجدول الاحترافي
        grid_res = AgGrid(df, gridOptions=gb.build(), theme='alpine', height=500)
        if st.button("💾 حفظ التعديلات والمعادلات"):
            st.session_state['beast_vault'] = pd.DataFrame(grid_res['data'])
            st.success("تم الحفظ!")
    else: st.warning("الرجاء استدعاء بيانات أولاً.")

elif menu_map[choice] == "Analyst":
    st.header("🧠 المحلل الذكي (Smart Analyst)")
    if df is not None:
        st.write("إحصائيات البيانات الكبرى:")
        st.dataframe(df.describe())
        fig = px.histogram(df, x="المبيعات", color="الفرع", title="توزيع المبيعات حسب الفروع")
        st.plotly_chart(fig, use_container_width=True)
    else: st.error("لا توجد بيانات للتحليل.")

elif menu_map[choice] == "Dash":
    st.header("🖥️ Beast Dash - لوحة القيادة")
    if df is not None:
        c1, c2 = st.columns(2)
        c1.metric("إجمالي المبيعات", f"{df['المبيعات'].sum():,.2f}")
        c2.metric("عدد العمليات", len(df))
        st.bar_chart(df['الفرع'].value_counts())

# --- التصحيح النهائي (شرطتين تحت بعض __) ---
if _name_ == "_main_":
    pass
