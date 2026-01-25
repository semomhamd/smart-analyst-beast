import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# ================== 1. إعدادات الهوية والصفحة ==================
st.set_page_config(page_title="Smart Analyst Beast", page_icon="🐉", layout="wide")

# تهيئة حالة الجلسة
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'theme' not in st.session_state: st.session_state.theme = "Dark"

# ================== 2. محرك الأسلوب (إصلاح شامل للأخطاء) ==================
# هنا فصلت الألوان عشان ميبقاش فيه أي تعارض في النصوص
bg_color = "#0E1117" if st.session_state.theme == "Dark" else "#F0F2F6"
text_color = "white" if st.session_state.theme == "Dark" else "black"

# الطريقة الآمنة لكتابة CSS في Streamlit لتجنب أخطاء الصور
st.markdown(f"""
<style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    .app-title {{
        font-size: 45px;
        font-weight: 800;
        color: #00C853;
        text-align: center;
        margin-bottom: 0px;
    }}
    .app-signature {{
        font-size: 14px;
        font-family: 'Courier New';
        color: {text_color};
        opacity: 0.7;
        text-align: center;
        margin-top: -10px;
        letter-spacing: 2px;
    }}
    .welcome-msg {{
        color: #00C853;
        font-size: 18px;
        font-weight: bold;
        text-align: center;
        margin-top: 20px;
        border: 1px dashed #00C853;
        padding: 15px;
        border-radius: 12px;
    }}
    [data-testid="stSidebar"] {{
        border-right: 2px solid #00C853;
    }}
    .stButton>button {{
        background-color: #00C853;
        color: white;
        border-radius: 12px;
        font-weight: bold;
    }}
</style>
""", unsafe_allow_html=True)

# ================== 3. نظام الدخول الآمن ==================
if not st.session_state.logged_in:
    st.markdown("<div class='app-title'>SMART ANALYST BEAST</div>", unsafe_allow_html=True)
    st.markdown("<div class='app-signature'>by MIA8444</div>", unsafe_allow_html=True)
    
    with st.form("LoginGate"):
        st.subheader("🔑 Secure Access")
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.form_submit_button("Wake the Beast"):
            if u == "semomohamed" and p == "123456":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Access Denied")
    st.stop()

# ================== 4. الواجهة الرئيسية بعد الدخول ==================
st.markdown("<div class='app-title'>SMART ANALYST BEAST</div>", unsafe_allow_html=True)
st.markdown("<div class='app-signature'>Designed & Engineered by MIA8444</div>", unsafe_allow_html=True)

st.markdown("<div class='welcome-msg'>\"You don't have to be a data analyst.. Smart Analyst thinks for you\"</div>", unsafe_allow_html=True)

# القائمة الجانبية
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    theme = st.radio("🌗 Mode", ["Dark", "Light"], index=0 if st.session_state.theme == "Dark" else 1)
    if theme != st.session_state.theme:
        st.session_state.theme = theme
        st.rerun()
    
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()

# التبويبات (Tabs)
t1, t2, t3, t4, t5 = st.tabs(["📂 Intake", "🧹 Cleaning", "📊 Analysis", "⭐ Dashboard", "📤 Export"])

with t1:
    st.info("ارفع ملفاتك هنا يا محمد")
    st.file_uploader("Upload Data", accept_multiple_files=True)

with t4:
    # رسم بياني ملون تلقائياً كنموذج للداشبورد
    st.subheader("Smart Visuals")
    sample_data = pd.DataFrame({"Month": ["Jan", "Feb", "Mar"], "Power": [50, 80, 65]})
    fig, ax = plt.subplots()
    sns.barplot(data=sample_data, x="Month", y="Power", palette="viridis", ax=ax)
    st.pyplot(fig)
