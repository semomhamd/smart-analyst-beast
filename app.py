import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- 1. نظام الترجمة (الحقيقي) ---
texts = {
    "العربية": {
        "title": "Smart Analyst Beast",
        "slogan": "You don't have to be a data analyst.. Smart Analyst thinks for you",
        "menu": ["🏠 الرئيسية", "📄 الشيت الذكي", "🧠 الذكاء الاصطناعي", "📊 الرسوم البيانية", "⚙️ الإعدادات"],
        "gen_btn": "🚀 توليد ملف الوحش (20,000 صف)",
        "save_btn": "💾 حفظ البيانات",
        "login": "تسجيل الدخول",
        "theme_label": "وضع الأبيض والأسود",
        "lang_label": "اختر اللغة"
    },
    "English": {
        "title": "Smart Analyst Beast",
        "slogan": "You don't have to be a data analyst.. Smart Analyst thinks for you",
        "menu": ["🏠 Home", "📄 Smart Sheet", "🧠 AI Analyst", "📊 Charts", "⚙️ Settings"],
        "gen_btn": "🚀 Generate Beast File (20,000 Rows)",
        "save_btn": "💾 Save Data",
        "login": "Login",
        "theme_label": "B&W Mode",
        "lang_label": "Select Language"
    }
}

# --- 2. الإعدادات والذاكرة ---
st.set_page_config(page_title="Smart Analyst Beast", page_icon="🦁", layout="wide")

if 'lang' not in st.session_state: st.session_state['lang'] = "العربية"
if 'db' not in st.session_state: st.session_state['db'] = None
if 'theme' not in st.session_state: st.session_state['theme'] = "Dark"

T = texts[st.session_state['lang']] # القاموس النشط

# --- 3. محرك الثيم (حقيقي) ---
if st.session_state['theme'] == "White & Black":
    st.markdown("""<style>
        .stApp { background-color: white !important; color: black !important; }
        p, h1, h2, h3, span, label { color: black !important; }
        .stButton>button { background-color: black !important; color: white !important; border-radius: 10px; }
    </style>""", unsafe_allow_html=True)

# --- 4. السايد بار ---
with st.sidebar:
    st.title("🦁 MIA8444")
    st.write("---")
    choice = st.radio("Menu:", T["menu"])
    st.write("---")
    st.caption("Developed by MIA8444")

# --- 5. الصفحات ---

if choice in [T["menu"][0]]: # الرئيسية
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.markdown(f"<h1 style='text-align: center;'>{T['title']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-size: 20px;'>{T['slogan']}</p>", unsafe_allow_html=True)
        st.write("---")
        
        if st.button(T["gen_btn"]):
            with st.spinner('Beast is Loading...'):
                df = pd.DataFrame(np.random.randn(20000, 10), columns=[f'Data_{i}' for i in range(10)])
                st.session_state['db'] = df
                st.balloons()
                st.success("20,000 Rows Generated!")

        file = st.file_uploader("Upload CSV/Excel", type=['xlsx', 'csv'])
        if file:
            st.session_state['db'] = pd.read_excel(file) if file.name.endswith('xlsx') else pd.read_csv(file)

elif choice in [T["menu"][1]]: # الشيت الذكي
    st.header(T["menu"][1])
    if st.session_state['db'] is not None:
        if st.button(T["save_btn"]):
            st.toast("Data Saved Locally ✅")
        st.data_editor(st.session_state['db'], use_container_width=True)
    else: st.info("No data found.")

elif choice in [T["menu"][4]]: # الإعدادات
    st.header(T["menu"][4])
    
    # تغيير اللغة حقيقي
    new_lang = st.selectbox(T["lang_label"], ["العربية", "English"], 
                            index=0 if st.session_state['lang'] == "العربية" else 1)
    if new_lang != st.session_state['lang']:
        st.session_state['lang'] = new_lang
        st.rerun()

    # تغيير الثيم حقيقي
    theme_on = st.toggle(T["theme_label"], value=(st.session_state['theme'] == "White & Black"))
    st.session_state['theme'] = "White & Black" if theme_on else "Dark"
    if st.button("Apply Theme"): st.rerun()

    st.write("---")
    st.subheader(T["login"])
    contact = st.text_input("Email / Phone")
    if st.button(T["login"]): st.success(f"Welcome {contact}!")
