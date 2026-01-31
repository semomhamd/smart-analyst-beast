import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO

# --- 1. الهوية MIA8444 والإعدادات [cite: 2026-01-26] ---
st.set_page_config(page_title="Smart Analyst Beast PRO", page_icon="🦁", layout="wide")

if 'db' not in st.session_state: 
    # تهيئة بجدول إكسيل احترافي فاضي لإدخال بيانات حقيقية [cite: 2026-01-15]
    st.session_state['db'] = pd.DataFrame(columns=['البند', 'القيمة', 'التصنيف'])
if 'lang' not in st.session_state: st.session_state['lang'] = "العربية"
if 'theme' not in st.session_state: st.session_state['theme'] = "Dark"

# --- 2. محرك الثيم (أبيض وأسود) [cite: 2026-01-24] ---
if st.session_state['theme'] == "White & Black":
    st.markdown("""<style>
        .stApp { background-color: white !important; color: black !important; }
        h1, h2, h3, p, label, span { color: black !important; }
        .stButton>button { background-color: black !important; color: white !important; }
    </style>""", unsafe_allow_html=True)

# --- 3. السايد بار الكامل بتوقيعك MIA8444 [cite: 2026-01-26, 2026-01-28] ---
with st.sidebar:
    try:
        st.image("8888.jpg", use_column_width=True) # اللوجو المعتمد [cite: 2026-01-28]
    except:
        st.title("🦁 MIA8444 Beast")
    
    st.write("---")
    # القائمة الاحترافية اللي بتخدم شغلك [cite: 2026-01-15, 2026-01-17]
    choice = st.radio("القائمة الاحترافية:", 
                      ["🏠 الرئيسية", "📊 Excel Pro (إدخال بيانات)", "📉 Pivot & Analytics", "🧠 AI Analyst", "📊 الرسوم البيانية", "📄 PDF Report Center", "⚙️ الإعدادات"])
    st.write("---")
    st.caption("Signature: MIA8444")

# --- 4. منطق الصفحات (تشغيل الوحش بجد) ---

if choice == "🏠 الرئيسية":
    st.header("Smart Analyst Beast")
    st.subheader("You don't have to be a data analyst.. Smart Analyst thinks for you") # [cite: 2026-01-24]
    
    if st.button("🚀 توليد ملف اختبار (20,000 صف)"):
        with st.spinner('جاري التحميل...'):
            df = pd.DataFrame(np.random.randint(0, 1000, size=(20000, 10)), 
                              columns=[f'Data_{i}' for i in range(10)])
            st.session_state['db'] = df
            st.success("تم توليد 20,000 صف!")
            st.balloons()

    up = st.file_uploader("ارفع ملفك الحقيقي (Excel/CSV)", type=["csv", "xlsx"])
    if up: 
        st.session_state['db'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)

elif choice == "📊 Excel Pro (إدخال بيانات)":
    st.header("📊 Excel Pro Workspace") # [cite: 2026-01-15]
    st.write("استخدمه كإكسيل أصلي لإدخال بياناتك الحقيقية:")
    # إدخال وتعديل البيانات بيدك [cite: 2026-01-15]
    df_edited = st.data_editor(st.session_state['db'], num_rows="dynamic", use_container_width=True)
    st.session_state['db'] = df_edited
    
    # ميزة جمع الأعمدة (SUM) المتقدمة [cite: 2025-11-13]
    num_cols = df_edited.select_dtypes(include=[np.number]).columns.tolist()
    if num_cols:
        target = st.selectbox("اختر العمود لجمعه:", num_cols)
        if st.button("➕ احسب المجموع"):
            st.metric(f"إجمالي {target}", f"{df_edited[target].sum():,}")

elif choice == "📉 Pivot & Analytics":
    st.header("📉 Pivot Table & Summaries") # [cite: 2025-11-13, 2026-01-15]
    df = st.session_state['db']
    if not df.empty:
        idx = st.selectbox("التصنيف (Rows):", df.columns)
        val = st.selectbox("القيمة (Values):", df.select_dtypes(include=[np.number]).columns)
        pivot = df.groupby(idx)[val].sum().reset_index()
        st.write("ملخص الجدول المحوري:")
        st.dataframe(pivot, use_container_width=True)
    else: st.warning("دخل بيانات أولاً.")

elif choice == "🧠 AI Analyst":
    st.header("🧠 AI Analyst Core") # [cite: 2026-01-15]
    if st.session_state['db'] is not None:
        st.write("💡 ملخص إحصائي ذكي (Describe & Average):") # [cite: 2025-11-13, 2026-01-20]
        st.dataframe(st.session_state['db'].describe())
    else: st.warning("لا توجد بيانات للتحليل.")

elif choice == "📄 PDF Report Center":
    st.header("📄 تصدير التقارير لمديرك") # [cite: 2026-01-15]
    if not st.session_state['db'].empty:
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            st.session_state['db'].to_excel(writer, index=False)
        st.download_button("📥 تحميل ملف الإكسيل النهائي (جاهز للتحويل لـ PDF)", 
                           data=output.getvalue(), 
                           file_name="MIA8444_Report.xlsx")
    else: st.error("لا توجد بيانات لعمل تقرير.")

elif choice == "⚙️ الإعدادات":
    st.header("⚙️ الإعدادات")
    theme_on = st.toggle("تفعيل وضع الأبيض والأسود", value=(st.session_state['theme'] == "White & Black"))
    st.session_state['theme'] = "White & Black" if theme_on else "Dark"
    if st.button("حفظ الثيم"): st.rerun()
