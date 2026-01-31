import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO

# --- 1. إعدادات الهوية والذاكرة MIA8444 [cite: 2026-01-26] ---
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
        "lang_label": "اختر اللغة",
        "theme_label": "تفعيل وضع الأبيض والأسود",
        "save_btn": "حفظ الإعدادات"
    },
    "English": {
        "menu": ["🏠 Home", "📊 Excel Pro (Data Entry)", "📉 Pivot & Analytics", "🧠 AI Analyst", "📊 Charts", "📄 PDF Report Center", "⚙️ Settings"],
        "slogan": "You don't have to be a data analyst.. Smart Analyst thinks for you",
        "lang_label": "Select Language",
        "theme_label": "Enable Black & White Mode",
        "save_btn": "Save Settings"
    }
}

T = texts[st.session_state['lang']]

# --- 2. محرك الثيم (أبيض وأسود) [cite: 2026-01-24] ---
if st.session_state['theme'] == "White & Black":
    st.markdown("""<style>
        .stApp { background-color: white !important; color: black !important; }
        h1, h2, h3, p, label, span { color: black !important; }
        .stButton>button { background-color: black !important; color: white !important; }
    </style>""", unsafe_allow_html=True)

# --- 3. السايد بار واللوجو MIA8444 ---
with st.sidebar:
    try: st.image("8888.jpg", use_column_width=True) # اللوجو اللي في صورتك
    except: st.title("🦁 MIA8444 Beast")
    st.write("---")
    choice = st.radio("القائمة الاحترافية:", T["menu"])
    st.write("---")
    st.caption("Signature: MIA8444")

# --- 4. تشغيل الصفحات بجد ---

if choice == T["menu"][0]: # الرئيسية
    st.header("Smart Analyst Beast")
    st.subheader(T["slogan"]) #
    if st.button("🚀 توليد ملف اختبار (20,000 صف)"):
        st.session_state['db'] = pd.DataFrame(np.random.randint(0, 1000, size=(20000, 5)), columns=['A', 'B', 'C', 'D', 'E'])
        st.success("تم شحن الوحش!")
        st.balloons()
    up = st.file_uploader("ارفع ملفك الخاص", type=["csv", "xlsx"])
    if up: st.session_state['db'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)

elif choice == T["menu"][1]: # Excel Pro
    st.header(T["menu"][1])
    df_edited = st.data_editor(st.session_state['db'], num_rows="dynamic", use_container_width=True)
    st.session_state['db'] = df_edited
    num_cols = df_edited.select_dtypes(include=[np.number]).columns.tolist()
    if num_cols:
        target = st.selectbox("اختر العمود لجمعه:", num_cols)
        if st.button("➕ احسب المجموع"):
            st.metric(f"إجمالي {target}", f"{df_edited[target].sum():,}")

elif choice == T["menu"][6]: # الإعدادات (هنا زر اللغة)
    st.header(T["menu"][6])
    
    # ميزة اختيار اللغة
    new_lang = st.selectbox(T["lang_label"], ["العربية", "English"], 
                            index=0 if st.session_state['lang'] == "العربية" else 1)
    
    # ميزة الثيم
    theme_on = st.toggle(T["theme_label"], value=(st.session_state['theme'] == "White & Black"))
    
    if st.button(T["save_btn"]):
        st.session_state['lang'] = new_lang
        st.session_state['theme'] = "White & Black" if theme_on else "Dark"
        st.rerun()

elif choice == T["menu"][5]: # PDF Report Center
    st.header(T["menu"][5])
    if not st.session_state['db'].empty:
        output = BytesIO()
        # استخدام openpyxl لحل الخطأ الأحمر
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            st.session_state['db'].to_excel(writer, index=False)
        st.download_button("📥 تحميل التقرير (Excel/PDF)", data=output.getvalue(), file_name="MIA8444_Report.xlsx")
    else: st.error("لا توجد بيانات!")
