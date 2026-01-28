import streamlit as st
import pandas as pd
import os
from core_engine import load_file, clean_df
from PIL import Image
import base64

# =================== إعداد الصفحة ===================
st.set_page_config(page_title="Smart Analyst Beast", layout="wide")

# =================== الثيم ===================
if 'theme' not in st.session_state:
    st.session_state.theme = 'Dark'

bg_color = "#0e1117" if st.session_state.theme == 'Dark' else "#ffffff"
text_color = "#D4AF37" if st.session_state.theme == 'Dark' else "#000000"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; color: {text_color}; }}
    .footer {{ position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; font-size: 12px; color: #888; padding: 5px; background: transparent; }}
    </style>
""", unsafe_allow_html=True)

# =================== الهيدر ===================
col_space, col_lang, col_set = st.columns([10, 1.2, 0.8])
with col_lang:
    st.button("🌐 AR/EN")
with col_set:
    with st.expander("⚙️ الإعدادات"):
        st.text_input("التسجيل (Email / Phone)")
        if st.button("تبديل النمط (Light/Dark)"):
            st.session_state.theme = 'Light' if st.session_state.theme == 'Dark' else 'Dark'
            st.experimental_rerun()

# =================== اللوجو ===================
logo_path = "المخ/8888.jpg"
if os.path.exists(logo_path):
    st.image(logo_path, width=120)
else:
    st.warning("اللوجو مش موجود! تأكد من المسار.")

# =================== القائمة الجانبية ===================
with st.sidebar:
    st.markdown("---")
    choice = st.radio("🛠️ الأدوات:", [
        "🏠 الرئيسية", "📊 Excel Master", "🧹 Power Query", "📈 Power BI", 
        "🐍 Python Lab", "👁️ OCR Engine", "☁️ Google Sheets", 
        "🖼️ Tableau", "🗄️ SQL Lab", "🤖 AI Brain (Core)"
    ])

# =================== منطقة العمل ===================
if 'dataset' not in st.session_state:
    st.session_state.dataset = pd.DataFrame()

# --- الرئيسية ---
if choice == "🏠 الرئيسية":
    st.title("The Ultimate Financial Brain")
    uploaded = st.file_uploader("ارفع أي ملف بيانات (Excel/CSV/ODS) هنا", type=['xlsx','csv','ods'])
    if uploaded:
        try:
            st.session_state.dataset = load_file(uploaded)
            st.success("تم رفع الملف وربطه بالترسانة!")
        except Exception as e:
            st.error(f"في مشكلة في رفع الملف: {e}")

# --- Excel Master ---
elif choice == "📊 Excel Master":
    st.header("📊 Excel Master")
    df = st.session_state.dataset.copy()
    if not df.empty:
        edited_df = st.data_editor(df, num_rows="dynamic")  # إدخال يدوي مباشر
        st.session_state.dataset = edited_df
        st.success("تم تحديث البيانات بنجاح!")
        # زر Export Excel
        st.download_button(
            "⬇️ تحميل Shit Excel",
            data=edited_df.to_excel(index=False),
            file_name="Edited_Data.xlsx"
        )
    else:
        st.info("ارفع ملف أولًا من الرئيسية")

# --- Power BI ---
elif choice == "📈 Power BI":
    st.header("📈 Power BI Simulator")
    if st.session_state.dataset.empty:
        st.info("ارفع بيانات أولًا في Excel Master")
    else:
        st.bar_chart(st.session_state.dataset.select_dtypes(include='number'))

# --- Python Lab ---
elif choice == "🐍 Python Lab":
    st.header("🐍 Python Analytics")
    if st.session_state.dataset.empty:
        st.info("ارفع بيانات أولًا")
    else:
        st.write(st.session_state.dataset.describe())

# --- AI Brain ---
elif choice == "🤖 AI Brain (Core)":
    st.header("🧠 الذكاء الاصطناعي المركزي")
    question = st.text_input("اسأل الوحش عن بياناتك:", placeholder="اكتب سؤالك هنا...")
    if st.button("تحليل وإرسال PDF واتساب"):
        if question.strip():
            st.success(f"الذكاء الاصطناعي بيحلل: {question}")
        else:
            st.warning("اكتب سؤالك الأول!")

# =================== التوقيع ===================
st.markdown(f"""
    <div class="footer">
        Property of Smart Analyst Beast | Signature MIA8444 | v1.0
    </div>
""", unsafe_allow_html=True)
