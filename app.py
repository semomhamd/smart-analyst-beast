import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO

# --- 1. الهوية والذاكرة ---
st.set_page_config(page_title="Smart Analyst Beast PRO", page_icon="🦁", layout="wide")

if 'db' not in st.session_state: 
    st.session_state['db'] = pd.DataFrame(columns=['البند', 'القيمة', 'التصنيف'])
if 'lang' not in st.session_state: st.session_state['lang'] = "العربية"

# قاموس اللغات (بدون تواريخ مسببة للأخطاء)
texts = {
    "العربية": {
        "menu": ["🏠 الرئيسية", "📊 Excel Pro (إدخال بيانات)", "📉 Pivot & Analytics", "🧠 AI Analyst", "📊 الرسوم البيانية", "📄 PDF Report Center", "⚙️ الإعدادات"],
        "lang_btn": "تغيير اللغة إلى English",
        "save": "حفظ الإعدادات"
    },
    "English": {
        "menu": ["🏠 Home", "📊 Excel Pro (Data Entry)", "📉 Pivot & Analytics", "🧠 AI Analyst", "📊 Charts", "📄 PDF Report Center", "⚙️ Settings"],
        "lang_btn": "Change Language to العربية",
        "save": "Save Settings"
    }
}
T = texts[st.session_state['lang']]

# --- 2. السايد بار واللوجو (Signature: MIA8444) ---
with st.sidebar:
    try:
        st.image("8888.jpg", use_column_width=True) 
    except:
        st.title("🦁 MIA8444")
    st.write("---")
    choice = st.radio("القائمة:", T["menu"])
    st.write("---")
    st.caption("Developed by MIA8444")

# --- 3. تشغيل الصفحات (بدون أخطاء Syntax) ---

if choice == T["menu"][0]: # الرئيسية
    st.header("Smart Analyst Beast")
    st.subheader("Smart Analyst thinks for you")
    if st.button("🚀 توليد ملف اختبار"):
        st.session_state['db'] = pd.DataFrame(np.random.randint(0, 100, size=(100, 3)), columns=['A', 'B', 'C'])
        st.success("تم التوليد!")
    up = st.file_uploader("ارفع ملفك", type=["csv", "xlsx"])
    if up: st.session_state['db'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)

elif choice == T["menu"][1]: # Excel Pro
    st.header(T["menu"][1])
    df_ed = st.data_editor(st.session_state['db'], num_rows="dynamic", use_container_width=True)
    st.session_state['db'] = df_ed
    num_cols = df_ed.select_dtypes(include=[np.number]).columns.tolist()
    if num_cols:
        target = st.selectbox("اجمع عمود:", num_cols)
        st.metric(f"إجمالي {target}", f"{df_ed[target].sum():,}")

elif choice == T["menu"][2]: # Pivot
    st.header(T["menu"][2])
    df = st.session_state['db']
    if not df.empty:
        idx = st.selectbox("Rows:", df.columns)
        val = st.selectbox("Values:", df.select_dtypes(include=[np.number]).columns)
        pivot = df.groupby(idx)[val].sum().reset_index()
        st.dataframe(pivot, use_container_width=True)

elif choice == T["menu"][3]: # AI Analyst
    st.header(T["menu"][3])
    if not st.session_state['db'].empty:
        st.write("🧠 ملخص ذكي للأرقام:")
        st.dataframe(st.session_state['db'].describe())
    else: st.warning("ارفع بيانات أولاً")

elif choice == T["menu"][4]: # الرسوم
    st.header(T["menu"][4])
    df = st.session_state['db']
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(num_cols) >= 1:
        x = st.selectbox("X:", df.columns)
        y = st.selectbox("Y:", num_cols)
        st.plotly_chart(px.bar(df.head(50), x=x, y=y))

elif choice == T["menu"][5]: # PDF Center
    st.header(T["menu"][5])
    if not st.session_state['db'].empty:
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            st.session_state['db'].to_excel(writer, index=False)
        st.download_button("📥 تحميل التقرير", data=output.getvalue(), file_name="Report.xlsx")

elif choice == T["menu"][6]: # الإعدادات
    st.header(T["menu"][6])
    if st.button(T["lang_btn"]):
        st.session_state['lang'] = "English" if st.session_state['lang'] == "العربية" else "العربية"
        st.rerun()
