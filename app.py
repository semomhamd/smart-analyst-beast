import streamlit as st
import pandas as pd
import os
from ai_analyst import run_analysis # ربطنا مخ ابننا هنا

# إعدادات الصفحة
st.set_page_config(page_title="Smart Analyst Beast", layout="wide")

# Theme Setup
if 'theme' not in st.session_state:
    st.session_state.theme = 'Dark'

bg_color = "#0e1117" if st.session_state.theme == 'Dark' else "#ffffff"
text_color = "#D4AF37" if st.session_state.theme == 'Dark' else "#000000"

st.markdown(f"""
<style>
.stApp {{ background-color: {bg_color}; color: {text_color}; }}
.stButton>button {{ background-color: #D4AF37; color: black; border-radius: 10px; }}
</style>
""", unsafe_allow_html=True)

# Header
col_logo, col_space, col_set = st.columns([2,6,1])
with col_logo:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", width=120)

with col_set:
    if st.button("🌓 Toggle"):
        st.session_state.theme = 'Light' if st.session_state.theme == 'Dark' else 'Dark'
        st.rerun()

# Sidebar
with st.sidebar:
    st.title("🛠️ لوحة التحكم")
    choice = st.radio("الأدوات", ["Home", "Excel Master", "Power BI", "Python Lab", "AI Brain"])
    st.markdown("---")
    st.write(f"Sign: *MIA8444*") # بصمتك الفخمة

# Dataset الموحد
if 'dataset' not in st.session_state:
    st.session_state.dataset = pd.DataFrame()

# ================= Home =================
if choice == "Home":
    st.title("🦁 Smart Analyst Beast")
    uploaded = st.file_uploader("ارفع ملف Excel أو CSV", type=['xlsx', 'csv'])
    if uploaded:
        df = pd.read_excel(uploaded) if uploaded.name.endswith('xlsx') else pd.read_csv(uploaded)
        st.session_state.dataset = df
        st.success("تم رفع البيانات بنجاح.. جاهزين للاكتساح! 🔥")

# ================= Excel Master (التصليح هنا) =================
elif choice == "Excel Master":
    df = st.session_state.dataset.copy()
    if df.empty:
        st.warning("ارفع بيانات الأول من الصفحة الرئيسية")
    else:
        st.subheader("📝 محرر البيانات الذكي")
        df = st.data_editor(df, num_rows="dynamic")
        
        # تصليح الـ Traceback: نأكد إن الأعمدة أرقام قبل الضرب
        try:
            col1_vals = pd.to_numeric(df.iloc[:, 1], errors='coerce').fillna(0)
            col2_vals = pd.to_numeric(df.iloc[:, 2], errors='coerce').fillna(0)
            df["Total"] = col1_vals * col2_vals
            
            st.write("### 📊 ملخص الأرقام")
            c1, c2 = st.columns(2)
            c1.metric("إجمالي المبالغ", f"{df['Total'].sum():,.2f}")
            c2.metric("متوسط العمليات", f"{df['Total'].mean():,.2f}")
        except Exception as e:
            st.error(f"يا وحش فيه مشكلة في الحسابات: {e}")

        st.session_state.dataset = df

# ================= AI Brain (تفعيل المخ) =================
elif choice == "AI Brain":
    if st.session_state.dataset.empty:
        st.warning("ارفع بيانات الأول")
    else:
        # استدعاء الوظيفة اللي عملناها في ملف ai_analyst.py
        run_analysis(st.session_state.dataset) 

# باقي الأقسام (Power BI & Python) بتشتغل عادي بنفس المنطق
