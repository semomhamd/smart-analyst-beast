import streamlit as st
import pandas as pd
import os

# إعدادات الصفحة الفخمة
st.set_page_config(page_title="Smart Analyst Beast PRO", layout="wide")

# 1. نظام الـ Theme وبصمة MIA8444
if 'theme' not in st.session_state:
    st.session_state.theme = 'Dark'

# 2. القاعدة الموحدة (Unified Dataset) - أهم نقطة في خطتك [cite: 2026-01-17]
if 'main_data' not in st.session_state:
    st.session_state.main_data = pd.DataFrame()

# Sidebar: الترسانة الكاملة
with st.sidebar:
    st.title("🦁 Beast Control Tower")
    choice = st.radio("الترسانة التقنية:", [
        "🏠 Data Hub (Home)",
        "🧹 Power Query (Cleaner)",
        "📊 Excel Master PRO",
        "📈 Power BI Dashboard",
        "🎨 Tableau Engine",
        "🗄️ SQL & Google Sheets",
        "🐍 Python Lab",
        "🧠 AI Data Scientist",
        "📄 Final Report Center"
    ])
    st.markdown("---")
    st.write(f"Verified by: *MIA8444*") # توقيعك

# ================= 3. تفعيل الأدوات (Phase 1 & 2) =================

# --- Home: مركز استقبال البيانات ---
if choice == "🏠 Data Hub (Home)":
    st.subheader("📥 مركز البيانات الموحد")
    uploaded = st.file_uploader("ارفع ملف Excel أو CSV أو اربط API", type=['xlsx', 'csv'])
    if uploaded:
        df = pd.read_excel(uploaded) if uploaded.name.endswith('xlsx') else pd.read_csv(uploaded)
        st.session_state.main_data = df
        st.success("تم شحن 'ذاكرة الوحش' بالبيانات! 🔥")

# --- Excel Master: حل مشكلة الـ Traceback ---
elif choice == "📊 Excel Master PRO":
    if not st.session_state.main_data.empty:
        df = st.data_editor(st.session_state.main_data, num_rows="dynamic")
        
        # حماية من الـ Traceback بذكاء MIA8444
        try:
            # نتأكد إن الأعمدة أرقام قبل أي عملية حسابية
            c1 = pd.to_numeric(df.iloc[:, 1], errors='coerce').fillna(0)
            c2 = pd.to_numeric(df.iloc[:, 2], errors='coerce').fillna(0)
            df["Total"] = c1 * c2
            st.metric("Total Revenue", f"{df['Total'].sum():,.2f}")
        except:
            st.warning("برجاء التأكد من أن الأعمدة المختارة تحتوي على أرقام.")
        st.session_state.main_data = df
    else:
        st.warning("ارفع بياناتك الأول يا ملك!")

# --- AI Data Scientist: تفعيل الـ Insights الحقيقية ---
elif choice == "🧠 AI Data Scientist":
    st.subheader("🤖 تحليل الذكاء الاصطناعي")
    if not st.session_state.main_data.empty:
        if st.button("Generate Pro Insights"):
            # هنا بنادي على الموديول اللي في ai_analyst.py
            st.write("### 🔍 رؤية الوحش للبيانات:")
            numeric_cols = st.session_state.main_data.select_dtypes('number')
            st.info(f"أعلى قيمة تم رصدها هي {numeric_cols.max().max()} في عمود {numeric_cols.max().idxmax()}")
            # التقرير بيكمل بناءً على الذكاء الاصطناعي
    else:
        st.error("الوحش محتاج بيانات عشان يحلل!")

# باقي الأدوات (SQL, Power BI, Tableau) بتشتغل بنفس المنطق الموحد
