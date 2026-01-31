import streamlit as st
import pandas as pd
import numpy as np

# --- 1. إعدادات الصفحة والهوية MIA8444 [cite: 2026-01-26] ---
st.set_page_config(page_title="Smart Analyst Beast", page_icon="🦁", layout="wide")

# تهيئة مخزن البيانات واللغة [cite: 2026-01-16]
if 'db' not in st.session_state: st.session_state['db'] = None
if 'lang' not in st.session_state: st.session_state['lang'] = "العربية"
if 'theme' not in st.session_state: st.session_state['theme'] = "Dark"

# قاموس اللغات (نظام ترجمة حقيقي) [cite: 2026-01-09]
texts = {
    "العربية": {
        "slogan": "You don't have to be a data analyst.. Smart Analyst thinks for you",
        "menu": ["🏠 الرئيسية", "📄 الشيت الذكي", "📊 الرسوم البيانية", "⚙️ الإعدادات"],
        "gen_btn": "🚀 توليد ملف الوحش للاختبار (الآلاف من الصفوف)",
        "upload": "ارفع ملفك الآن لتبدأ الترويض",
        "success": "تم رفع البيانات بنجاح!"
    },
    "English": {
        "slogan": "You don't have to be a data analyst.. Smart Analyst thinks for you",
        "menu": ["🏠 Home", "📄 Smart Sheet", "📊 Charts", "⚙️ Settings"],
        "gen_btn": "🚀 Generate Beast File (Stress Test)",
        "upload": "Upload your file to start taming",
        "success": "Data uploaded successfully!"
    }
}

T = texts[st.session_state['lang']]

# تطبيق ثيم الأبيض والأسود [cite: 2026-01-24]
if st.session_state['theme'] == "White & Black":
    st.markdown("""<style>
        .stApp { background-color: white !important; color: black !important; }
        p, h1, h2, h3, label, span { color: black !important; }
        .stButton>button { background-color: black !important; color: white !important; }
    </style>""", unsafe_allow_html=True)

# --- 2. السايد بار بتوقيعك MIA8444 [cite: 2026-01-26] ---
with st.sidebar:
    # عرض اللوجو 8888.jpg [cite: 2026-01-28]
    try:
        st.image("8888.jpg", use_column_width=True)
    except:
        st.title("🦁 Smart Analyst")
    
    st.write("---")
    choice = st.radio("القائمة:", T["menu"])
    st.write("---")
    st.caption("Signature: MIA8444")

# --- 3. الصفحات وتطوير الميزات ---

if choice == T["menu"][0]: # الرئيسية
    st.header("Smart Analyst Beast")
    st.subheader(T["slogan"]) # الجملة الاحترافية [cite: 2026-01-24]
    st.write("---")
    
    # ميزة مولد الملفات للاختبار [اليوم الثاني في الخطة]
    st.markdown("### 🧪 معمل اختبار الوحش")
    if st.button(T["gen_btn"]):
        with st.spinner('جاري توليد آلاف الصفوف...'):
            # توليد 10,000 صف و 20 عمود لاختبار التحمل
            test_df = pd.DataFrame(np.random.randint(0, 1000, size=(10000, 20)),
                                  columns=[f'Metric_{i}' for i in range(20)])
            st.session_state['db'] = test_df
            st.balloons()
            st.success("تم شحن الوحش بـ 10,000 صف! اذهب للشيت الذكي الآن.")

    up = st.file_uploader(T["upload"], type=["csv", "xlsx"])
    if up:
        st.session_state['db'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
        st.success(T["success"])

elif choice == T["menu"][1]: # الشيت الذكي
    st.header(T["menu"][1])
    if st.session_state['db'] is not None:
        st.data_editor(st.session_state['db'], use_container_width=True)
    else:
        st.info("ارفع ملف أو ولد بيانات من الرئيسية.")

elif choice == T["menu"][3]: # الإعدادات
    st.header(T["menu"][3])
    
    # تغيير اللغة حقيقي [cite: 2026-01-09]
    lang = st.selectbox("اختر اللغة / Select Language", ["العربية", "English"], 
                        index=0 if st.session_state['lang'] == "العربية" else 1)
    if lang != st.session_state['lang']:
        st.session_state['lang'] = lang
        st.rerun()
    
    # تغيير الثيم حقيقي (أبيض وأسود)
    theme = st.toggle("تفعيل وضع الأبيض والأسود", value=(st.session_state['theme'] == "White & Black"))
    st.session_state['theme'] = "White & Black" if theme else "Dark"
    if st.button("حفظ الإعدادات"): st.rerun()
    
    st.write("---")
    st.subheader("👤 تسجيل الدخول (MIA8444 Safe)")
    st.text_input("البريد الإلكتروني أو الهاتف")
    st.text_input("كلمة المرور", type="password")
    if st.button("دخول"): st.success("مرحباً بك في نظام MIA8444")
