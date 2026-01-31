import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO

# --- 1. الهوية MIA8444 والذاكرة [cite: 2026-01-26] ---
st.set_page_config(page_title="Smart Analyst Beast PRO", page_icon="🦁", layout="wide")

if 'db' not in st.session_state: 
    st.session_state['db'] = pd.DataFrame(columns=['البند', 'القيمة', 'التصنيف'])
if 'lang' not in st.session_state: st.session_state['lang'] = "العربية"
if 'theme' not in st.session_state: st.session_state['theme'] = "Dark"

# قاموس اللغات الاحترافي [cite: 2026-01-09]
texts = {
    "العربية": {
        "menu": ["🏠 الرئيسية", "📊 Excel Pro (إدخال بيانات)", "📉 Pivot & Analytics", "🧠 AI Analyst", "📊 الرسوم البيانية", "📄 PDF Report Center", "⚙️ الإعدادات"],
        "slogan": "You don't have to be a data analyst.. Smart Analyst thinks for you",
        "lang_btn": "تغيير اللغة إلى English",
        "save": "حفظ الإعدادات"
    },
    "English": {
        "menu": ["🏠 Home", "📊 Excel Pro (Data Entry)", "📉 Pivot & Analytics", "🧠 AI Analyst", "📊 Charts", "📄 PDF Report Center", "⚙️ Settings"],
        "slogan": "You don't have to be a data analyst.. Smart Analyst thinks for you",
        "lang_btn": "Change Language to العربية",
        "save": "Save Settings"
    }
}
T = texts[st.session_state['lang']]

# --- 2. السايد بار واللوجو MIA8444 ---
with st.sidebar:
    try:
        st.image("8888.jpg", use_column_width=True) 
    except:
        st.title("🦁 MIA8444 Beast")
    st.write("---")
    choice = st.radio("القائمة:", T["menu"])
    st.write("---")
    st.caption("Signature: MIA8444")

# --- 3. تشغيل الصفحات (حل مشكلة السواد والتعليق) ---

if choice == T["menu"][0]: # الرئيسية
    st.header("Smart Analyst Beast")
    st.subheader(T["slogan"]) # تم تصليح السطر ده من الصورة
    if st.button("🚀 توليد ملف اختبار (20,000 صف)"):
        st.session_state['db'] = pd.DataFrame(np.random.randint(0, 1000, size=(20000, 5)), 
                                              columns=['المبيعات', 'المخزون', 'التكلفة', 'الربح', 'العملاء'])
        st.success("تم شحن الوحش!")
    up = st.file_uploader("ارفع ملفك الخاص", type=["csv", "xlsx"])
    if up: st.session_state['db'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)

elif choice == T["menu"][1]: # Excel Pro
    st.header(T["menu"][1])
    # جدول تفاعلي لإدخال البيانات يدوياً [cite: 2026-01-15]
    df_edited = st.data_editor(st.session_state['db'], num_rows="dynamic", use_container_width=True)
    st.session_state['db'] = df_edited
    # ميزة الجمع الذكي لكل عمود [cite: 2025-11-13]
    num_cols = df_edited.select_dtypes(include=[np.number]).columns.tolist()
    if num_cols:
        target = st.selectbox("جمع عمود:", num_cols)
        st.metric(f"إجمالي {target}", f"{df_edited[target].sum():,}")

elif choice == T["menu"][2]: # Pivot & Analytics
    st.header(T["menu"][2])
    df = st.session_state['db']
    if not df.empty:
        idx = st.selectbox("Rows:", df.columns)
        val = st.selectbox("Values:", df.select_dtypes(include=[np.number]).columns)
        pivot = df.groupby(idx)[val].sum().reset_index()
        st.write("📊 ملخص الجدول المحوري:")
        st.dataframe(pivot, use_container_width=True)
    else: st.info("ارفع بيانات أولاً!")

elif choice == T["menu"][3]: # AI Analyst
    st.header(T["menu"][3])
    if not st.session_state['db'].empty:
        st.write("🧠 *تحليل الذكاء الاصطناعي التلقائي:*") [cite: 2026-01-30]
        st.dataframe(st.session_state['db'].describe())
    else: st.warning("الوحش يحتاج بيانات ليحللها.")

elif choice == T["menu"][4]: # الرسوم البيانية
    st.header(T["menu"][4])
    df = st.session_state['db']
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(num_cols) >= 1:
        x = st.selectbox("X Axis:", df.columns)
        y = st.selectbox("Y Axis:", num_cols)
        fig = px.bar(df.head(100), x=x, y=y, color=y, title="Professional Chart")
        st.plotly_chart(fig, use_container_width=True)

elif choice == T["menu"][6]: # الإعدادات (زر اللغة واللون)
    st.header(T["menu"][6])
    if st.button(T["lang_btn"]):
        st.session_state['lang'] = "English" if st.session_state['lang'] == "العربية" else "العربية"
        st.rerun()
    theme_on = st.toggle("Black & White Mode", value=(st.session_state['theme'] == "White & Black"))
    if st.button(T["save"]):
        st.session_state['theme'] = "White & Black" if theme_on else "Dark"
        st.rerun()

elif choice == T["menu"][5]: # PDF Center
    st.header(T["menu"][5])
    if not st.session_state['db'].empty:
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer: # حل الخطأ الأحمر
            st.session_state['db'].to_excel(writer, index=False)
        st.download_button("📥 تحميل التقرير لمديرك", data=output.getvalue(), file_name="MIA8444_Report.xlsx")
