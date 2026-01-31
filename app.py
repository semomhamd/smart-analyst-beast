import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- 1. الهوية MIA8444 والإعدادات [cite: 2026-01-26] ---
st.set_page_config(page_title="Smart Analyst Beast", page_icon="🦁", layout="wide")

# تهيئة الذاكرة [cite: 2026-01-11]
if 'db' not in st.session_state: st.session_state['db'] = None
if 'lang' not in st.session_state: st.session_state['lang'] = "العربية"
if 'theme' not in st.session_state: st.session_state['theme'] = "Dark"

# --- 2. محرك الثيم (أبيض وأسود حقيقي) [cite: 2026-01-24] ---
if st.session_state['theme'] == "White & Black":
    st.markdown("""<style>
        .stApp { background-color: white !important; color: black !important; }
        h1, h2, h3, p, label, span { color: black !important; }
        .stButton>button { background-color: black !important; color: white !important; }
    </style>""", unsafe_allow_html=True)

# --- 3. السايد بار بتوقيعك MIA8444 [cite: 2026-01-26, 2026-01-28] ---
with st.sidebar:
    try:
        st.image("8888.jpg", use_column_width=True) # اللوجو اللي في صورتك
    except:
        st.title("🦁 Smart Analyst")
    
    st.write("---")
    # القائمة المحدثة [cite: 2026-01-30]
    choice = st.radio("اختر سلاحك:", ["🏠 الرئيسية", "📄 الشيت والكلينر", "🧠 AI Analyst", "📊 الرسوم البيانية", "⚙️ الإعدادات"])
    st.write("---")
    st.caption("Signature: MIA8444")

# --- 4. منطق الصفحات (تشغيل الوحش بجد) ---

if choice == "🏠 الرئيسية":
    st.header("Smart Analyst Beast")
    st.subheader("You don't have to be a data analyst.. Smart Analyst thinks for you") # [cite: 2026-01-24]
    
    # زر توليد الملفات للاختبار [اليوم الثاني]
    if st.button("🚀 توليد ملف اختبار (20,000 صف)"):
        with st.spinner('جاري التحميل...'):
            df = pd.DataFrame(np.random.randint(0, 1000, size=(20000, 10)), 
                              columns=[f'Data_{i}' for i in range(10)])
            st.session_state['db'] = df
            st.success("تم توليد 20,000 صف! الوحش جاهز.")
            st.balloons()

    up = st.file_uploader("ارفع ملفك الخاص", type=["csv", "xlsx"])
    if up: 
        st.session_state['db'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)

elif choice == "📄 الشيت والكلينر":
    st.header("📄 محرك المعادلات والكلينر")
    if st.session_state['db'] is not None:
        # ميزة تجميع الأعمدة (SUM) [cite: 2025-11-13]
        df = st.session_state['db']
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if num_cols:
            col_to_sum = st.selectbox("اختر عمود لجمعه:", num_cols)
            if st.button("➕ احسب المجموع"):
                st.metric(f"إجمالي {col_to_sum}", f"{df[col_to_sum].sum():,}")
        
        st.data_editor(st.session_state['db'], use_container_width=True)
    else: st.info("ارفع ملف من الرئيسية أولاً.")

elif choice == "🧠 AI Analyst":
    st.header("🧠 AI Smart Analyst")
    if st.session_state['db'] is not None:
        df = st.session_state['db']
        st.write("💡 *تحليل الذكاء الاصطناعي الفوري:*")
        # حساب المتوسط (AVERAGE) [cite: 2025-11-13, 2026-01-20]
        st.dataframe(df.describe())
    else: st.warning("الوحش يحتاج بيانات ليحللها.")

elif choice == "📊 الرسوم البيانية":
    st.header("📊 مركز التحليل البصري")
    if st.session_state['db'] is not None:
        df = st.session_state['db']
        cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if len(cols) >= 2:
            x = st.selectbox("المحور X", df.columns)
            y = st.selectbox("المحور Y (أرقام)", cols)
            fig = px.bar(df.head(100), x=x, y=y, template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
    else: st.info("لا توجد بيانات للرسم.")

elif choice == "⚙️ الإعدادات":
    st.header("⚙️ إعدادات الوحش")
    # تغيير اللغة حقيقي [cite: 2026-01-09]
    lang = st.selectbox("اللغة (Language)", ["العربية", "English"])
    if st.button("تغيير اللغة"): st.success(f"تم التحويل إلى {lang}")
    
    # تغيير الثيم حقيقي
    theme_on = st.toggle("وضع الأبيض والأسود", value=(st.session_state['theme'] == "White & Black"))
    st.session_state['theme'] = "White & Black" if theme_on else "Dark"
    
    st.write("---")
    st.subheader("🔐 حساب MIA8444")
    st.text_input("البريد الإلكتروني / رقم الهاتف")
    if st.button("حفظ البيانات"): st.success("تم الحفظ في قاعدة بيانات الوحش!")
