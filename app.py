import streamlit as st
import pandas as pd
import os

# 1. إعدادات الصفحة الأساسية (أول سطر في البرمجة)
st.set_page_config(page_title="Smart Analyst Beast", layout="wide")

# 2. إدارة الثيم (أبيض/أسود) وحفظها في الذاكرة
if 'theme' not in st.session_state:
    st.session_state.theme = 'Dark'

# تطبيق الألوان بناءً على اختيارك من ترس الإعدادات
bg_color = "#0e1117" if st.session_state.theme == 'Dark' else "#ffffff"
text_color = "#D4AF37" if st.session_state.theme == 'Dark' else "#000000"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; color: {text_color}; }}
    .footer {{ position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; font-size: 12px; color: #888; padding: 5px; background: transparent; }}
    </style>
""", unsafe_allow_html=True)

# 3. الهيدر (اللغة والترس في أعلى اليمين)
col_space, col_lang, col_set = st.columns([10, 1.2, 0.8])
with col_lang:
    st.button("🌐 AR/EN")
with col_set:
    with st.popover("⚙️"): # ترس الإعدادات شغال بقائمة منسدلة
        st.markdown("### الإعدادات")
        st.text_input("التسجيل (Email / Phone)")
        if st.button("تبديل النمط (Light/Dark)"):
            st.session_state.theme = 'Light' if st.session_state.theme == 'Dark' else 'Dark'
            st.rerun()

# 4. القائمة الجانبية (الترسانة الكاملة بملفاتها)
with st.sidebar:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg")
    st.markdown("---")
    choice = st.radio("🛠️ الأدوات:", [
        "🏠 الرئيسية", "📊 Excel Master", "🧹 Power Query", "📈 Power BI", 
        "🐍 Python Lab", "👁️ OCR Engine", "☁️ Google Sheets", 
        "🖼️ Tableau", "🗄️ SQL Lab", "🤖 AI Brain (Core)"
    ])

# 5. منطقة العمل (Main Content)
if choice == "🏠 الرئيسية":
    st.title("The Ultimate Financial Brain")
    st.write("مرحباً بك في لوحة تحكم MIA8444")
    uploaded = st.file_uploader("ارفع ملف البيانات هنا", type=['xlsx', 'csv'])
    if uploaded:
        st.session_state['data'] = pd.read_excel(uploaded) if uploaded.name.endswith('xlsx') else pd.read_csv(uploaded)
        st.success("تم الربط بالترسانة!")

# سيتم استدعاء الملفات (import) داخل كل شرط بناءً على صورتك لملفات المشروع
elif choice == "🤖 AI Brain (Core)":
    st.header("🧠 الذكاء الاصطناعي المركزي")
    st.text_input("اسأل 'الوحش' عن بياناتك:", placeholder="اكتب سؤالك هنا...")
    # هنا يتم الربط مع Gemini/GPT لاحقاً
    st.button("تحليل وإرسال PDF واتساب")

# 6. التوقيع (MIA8444) بخط صغير تحت في النص
st.markdown(f"""
    <div class="footer">
        Property of Smart Analyst Beast | Signature MIA8444 | v1.0
    </div>
""", unsafe_allow_html=True)
