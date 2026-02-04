import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from st_aggrid import AgGrid, GridOptionsBuilder

# 1. الخزنة الحديدية (Session State) لتثبيت البيانات MIA8444
if 'data_vault' not in st.session_state:
    st.session_state['data_vault'] = None

st.set_page_config(page_title="Smart Analyst Beast - Stress Test", layout="wide")

# 2. مولد البيانات العملاق (10,000 صف و 15 عمود)
def generate_giant_data(rows=10000):
    st.info(f"جاري توليد {rows} صف... استعد لقوة الوحش!")
    dates = [datetime(2020, 1, 1) + timedelta(days=np.random.randint(0, 2000)) for _ in range(rows)]
    
    data = {
        'ID_المعاملة': range(1, rows + 1),
        'التاريخ': dates,
        'المنتج': [f"منتج_{np.random.randint(1, 100)}" for _ in range(rows)],
        'المبيعات': np.random.uniform(100, 50000, size=rows),
        'الكمية': np.random.randint(1, 100, size=rows),
        'الفرع': [np.random.choice(['القاهرة', 'دبي', 'الرياض', 'لندن']) for _ in range(rows)],
        'العميل': [f"عميل_{np.random.randint(1, 500)}" for _ in range(rows)],
        'الخصم': np.random.uniform(0, 0.3, size=rows),
        'الضريبة': np.random.uniform(0.05, 0.15, size=rows),
        'تكلفة_الشحن': np.random.uniform(10, 500, size=rows),
        'طريقة_الدفع': [np.random.choice(['كاش', 'فيزا', 'تحويل']) for _ in range(rows)],
        'حالة_الطلب': [np.random.choice(['تم', 'جاري', 'ملغي']) for _ in range(rows)],
        'التقييم': np.random.randint(1, 6, size=rows),
        'وزن_الشحنة': np.random.uniform(0.5, 50, size=rows),
        'الموظف_المسؤول': [f"موظف_{np.random.randint(1, 50)}" for _ in range(rows)]
    }
    return pd.DataFrame(data)

# 3. القائمة الجانبية
with st.sidebar:
    st.header("MIA8444 Control Panel")
    menu = st.radio("القائمة:", ["🏠 بوابة التحميل", "📊 Excel Pro (اختبار الضغط)", "📈 تحليل البيانات الضخمة"])
    if st.button("🚀 توليد 10,000 صف (اختبار التحمل)"):
        st.session_state['data_vault'] = generate_giant_data(10000)
        st.success("✅ الوحش ولد 10,000 صف بنجاح!")
        st.rerun()

df = st.session_state['data_vault']

# 4. الصفحات
if menu == "🏠 بوابة التحميل":
    st.title("🦁 بوابة التحكم MIA8444")
    if df is not None:
        st.write(f"البيانات الحالية: *{len(df)} صف* و *{len(df.columns)} عمود*.")
        st.dataframe(df.head(100)) # عرض أول 100 بس عشان المتصفح ميهنجش
    else:
        st.warning("الخزنة فاضية.. اضغط على زر التوليد في الجنب!")

elif menu == "📊 Excel Pro (اختبار الضغط)":
    st.header("📊 اختبار سرعة الاستجابة لـ AgGrid")
    if df is not None:
        # تحسين للأداء مع البيانات الكبيرة
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=20) # تقسيم الصفحات مهم جداً هنا
        gb.configure_side_bar()
        gb.configure_default_column(editable=True, filterable=True)
        
        st.write("إرشادات: جرب تعمل Filter أو Sort وشوف السرعة.")
        grid_res = AgGrid(df, gridOptions=gb.build(), theme='balham', height=500, update_mode='VALUE_CHANGED')
    else:
        st.error("ارفع أو ولد بيانات أولاً.")

elif menu == "📈 تحليل البيانات الضخمة":
    st.header("📈 معالجة إحصائية فورية")
    if df is not None:
        c1, c2 = st.columns(2)
        with c1:
            st.metric("إجمالي المبيعات المليونية", f"{df['المبيعات'].sum():,.2f}")
        with c2:
            st.metric("متوسط التقييم", f"{df['التقييم'].mean():.2f}")
        
        st.subheader("توزيع المبيعات حسب الفرع")
        import plotly.express as px
        fig = px.box(df, x='الفرع', y='المبيعات', color='حالة_الطلب', title="تحليل ضخم للمبيعات")
        st.plotly_chart(fig, use_container_width=True)
