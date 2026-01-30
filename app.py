import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- 1. إعدادات الهوية واللوجو MIA8444 --- [cite: 2026-01-26]
st.set_page_config(page_title="Smart Analyst Beast", page_icon="🦁", layout="wide")

# عرض اللوجو 8888.jpg في أعلى التطبيق [cite: 2026-01-28]
try:
    st.image("8888.jpg", width=120)
except:
    st.title("🦁 Smart Analyst Beast")

# محرك الذاكرة لربط الأدوات ببعضها [cite: 2026-01-16]
if 'main_df' not in st.session_state:
    st.session_state['main_df'] = None

# --- 2. السايد بار (ترسانة الأدوات الـ 8) ---
with st.sidebar:
    st.header("Smart Analyst")
    tool = st.radio("اختر سلاحك:", [
        "🏠 الرئيسية", "📄 الشيت الذكي", "🧠 الذكاء الاصطناعي", "📊 الرسوم البيانية"
    ])
    st.write("---")
    # توقيع MIA8444 ثابت في كل الصفحات [cite: 2026-01-26]
    st.caption("Signature: MIA8444")

# --- 3. تشغيل المحركات والربط ---

if tool == "🏠 الرئيسية":
    st.header("Smart Analyst Beast")
    # الجملة الافتتاحية الاحترافية التي اتفقنا عليها [cite: 2026-01-24]
    st.subheader("You don't have to be a data analyst.. Smart Analyst thinks for you")
    
    st.write("---")
    file = st.file_uploader("ارفع ملف البيانات (Excel/CSV)", type=['xlsx', 'csv'])
    if file:
        df = pd.read_excel(file) if file.name.endswith('xlsx') else pd.read_csv(file)
        st.session_state['main_df'] = df
        st.success("تم شحن البيانات في قلب الوحش! ✅")

elif tool == "📄 الشيت الذكي":
    st.header("📝 محرك المعادلات (Smart Sheet)")
    if st.session_state['main_df'] is not None:
        # الربط: التعديل هنا يغير النتائج في الرسوم والذكاء الاصطناعي [cite: 2026-01-25]
        updated_df = st.data_editor(st.session_state['main_df'], num_rows="dynamic", use_container_width=True)
        if st.button("⚡ حفظ وتحديث النظام"):
            st.session_state['main_df'] = updated_df
            st.balloons()
    else: st.info("برجاء رفع ملف من الصفحة الرئيسية أولاً.")

elif tool == "🧠 الذكاء الاصطناعي":
    st.header("🧠 مخ الذكاء الاصطناعي (AI Analysis)")
    if st.session_state['main_df'] is not None:
        df = st.session_state['main_df']
        numeric_df = df.select_dtypes(include=[np.number])
        col1, col2 = st.columns(2)
        col1.metric("إجمالي السجلات", len(df))
        if not numeric_df.empty:
            col2.metric("أعلى قيمة مالية", f"{numeric_df.max().max():,.2f}")
        st.info("الذكاء الاصطناعي يحلل البيانات المحدثة بتوقيع MIA8444.")
    else: st.warning("لا توجد بيانات للتحليل.")

elif tool == "📊 الرسوم البيانية":
    st.header("📊 مركز التحليل البصري")
    if st.session_state['main_df'] is not None:
        df = st.session_state['main_df']
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if num_cols:
            x_ax = st.selectbox("المحور الأفقي:", df.columns)
            y_ax = st.selectbox("المحور الرأسي (أرقام):", num_cols)
            fig = px.bar(df, x=x_ax, y=y_ax, title="تحليل الوحش الذكي", color=x_ax)
            st.plotly_chart(fig, use_container_width=True)
    else: st.error("ارفع بياناتك أولاً ليرسمها الوحش.")
