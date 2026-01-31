import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO

# --- 1. الهوية MIA8444 والإعدادات [cite: 2026-01-26] ---
st.set_page_config(page_title="Smart Analyst Beast PRO", page_icon="🦁", layout="wide")

if 'db' not in st.session_state: 
    st.session_state['db'] = pd.DataFrame(columns=['البند', 'القيمة', 'التصنيف'])
if 'lang' not in st.session_state: st.session_state['lang'] = "العربية"
if 'theme' not in st.session_state: st.session_state['theme'] = "Dark"

# قاموس اللغات الاحترافي [cite: 2026-01-09]
texts = {
    "العربية": {
        "menu": ["🏠 الرئيسية", "📊 Excel Pro (إدخال بيانات)", "📉 Pivot & Analytics", "🧠 AI Analyst", "📊 الرسوم البيانية", "📄 PDF Report Center", "⚙️ الإعدادات"],
        "slogan": "You don't have to be a data analyst.. Smart Analyst thinks for you"
    },
    "English": {
        "menu": ["🏠 Home", "📊 Excel Pro (Data Entry)", "📉 Pivot & Analytics", "🧠 AI Analyst", "📊 Charts", "📄 PDF Report Center", "⚙️ Settings"],
        "slogan": "You don't have to be a data analyst.. Smart Analyst thinks for you"
    }
}
T = texts[st.session_state['lang']]

# --- 2. السايد بار واللوجو MIA8444 ---
with st.sidebar:
    try: st.image("8888.jpg", use_column_width=True)
    except: st.title("🦁 MIA8444 Beast")
    st.write("---")
    choice = st.radio("القائمة الاحترافية:", T["menu"])
    st.write("---")
    st.caption("Signature: MIA8444")

# --- 3. تشغيل الوظائف (AI, Pivot, Graphs) ---

if choice == T["menu"][0]: # الرئيسية
    st.header("Smart Analyst Beast")
    st.subheader(T["slogan"]) [cite: 2026-01-24]
    if st.button("🚀 توليد ملف اختبار (20,000 صف)"):
        st.session_state['db'] = pd.DataFrame(np.random.randint(0, 1000, size=(20000, 5)), columns=['المبيعات', 'المخزون', 'التكلفة', 'الربح', 'العملاء'])
        st.success("تم شحن الوحش!")
    up = st.file_uploader("ارفع ملفك الخاص", type=["csv", "xlsx"])
    if up: st.session_state['db'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)

elif choice == T["menu"][1]: # Excel Pro
    st.header(T["menu"][1])
    # ميزة إدخال بيانات حقيقية [cite: 2026-01-15]
    df_edited = st.data_editor(st.session_state['db'], num_rows="dynamic", use_container_width=True)
    st.session_state['db'] = df_edited

elif choice == T["menu"][2]: # 📉 Pivot & Analytics (شغال الآن!)
    st.header(T["menu"][2])
    df = st.session_state['db']
    if not df.empty:
        col1, col2 = st.columns(2)
        with col1:
            idx = st.selectbox("تصنيف حسب (الصفوف):", df.columns)
        with col2:
            num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            val = st.selectbox("القيم لجمعها (المجموع):", num_cols)
        
        if val:
            pivot = df.groupby(idx)[val].sum().reset_index()
            st.write("📊 الجدول المحوري (Pivot Table):")
            st.dataframe(pivot, use_container_width=True)
    else: st.warning("لا توجد بيانات للتحليل!")

elif choice == T["menu"][3]: # 🧠 AI Analyst (شغال الآن!)
    st.header(T["menu"][3])
    df = st.session_state['db']
    if not df.empty:
        st.write("💡 *رؤية الذكاء الاصطناعي (تحليل تلقائي):*") [cite: 2026-01-30]
        # حساب المتوسط والتحليل الإحصائي (AVERAGE & Describe) [cite: 2025-11-13, 2026-01-20]
        st.dataframe(df.describe())
        st.success("الذكاء الاصطناعي قام بتحليل كافة الأعمدة الرقمية.")
    else: st.warning("ارفع بيانات أولاً!")

elif choice == T["menu"][4]: # 📊 الرسوم البيانية (شغال الآن!)
    st.header(T["menu"][4])
    df = st.session_state['db']
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(num_cols) >= 1:
        x_axis = st.selectbox("المحور الأفقي (X):", df.columns)
        y_axis = st.selectbox("المحور الرأسي (Y):", num_cols)
        # رسم بياني احترافي [cite: 2026-01-18]
        fig = px.bar(df.head(100), x=x_axis, y=y_axis, color=y_axis, title="تحليل مرئي احترافي")
        st.plotly_chart(fig, use_container_width=True)
    else: st.info("الرسوم البيانية تحتاج أعمدة بها أرقام.")

elif choice == T["menu"][5]: # PDF Report Center
    st.header(T["menu"][5])
    if not st.session_state['db'].empty:
        output = BytesIO()
        # استخدام openpyxl لحل الخطأ الأحمر في صورتك
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            st.session_state['db'].to_excel(writer, index=False)
        st.download_button("📥 تحميل التقرير النهائي لمديرك", data=output.getvalue(), file_name="MIA8444_Report.xlsx")
