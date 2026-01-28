import streamlit as st
import pandas as pd
# استيراد الملفات اللي ظهرت في صورتك
import excel_master as excel
import cleaner_pro as cleaner
import ocr_engine as ocr
import python_analytics as py_analyst

# 1. إعدادات الهوية الملكية (MIA8444 Edition)
st.set_page_config(page_title="Smart Analyst Beast", layout="wide")

# 2. الثيم الأسود والذهبي
st.markdown("""
    <style>
    .main { background-color: #000000; color: #D4AF37; }
    .stSidebar { background-color: #111111; border-right: 1px solid #D4AF37; }
    div.stButton > button { background-color: #D4AF37; color: black; border-radius: 10px; width: 100%; }
    </style>
""", unsafe_allow_html=True)

# 3. الذاكرة الموحدة (Unified Data Hub) - Phase 1
if 'unified_data' not in st.session_state:
    st.session_state['unified_data'] = None

# 4. القائمة الجانبية (The Sidebar)
with st.sidebar:
    st.image("8888.jpg") # اللوجو المعتمد في الفولدر
    st.markdown("<h2 style='text-align:center;'>MIA8444</h2>", unsafe_allow_html=True)
    choice = st.radio("الترسانة:", ["🏠 الرئيسية", "📊 Excel Master", "🧹 Cleaner Pro", "👁️ OCR Engine", "🤖 AI Brain (Gemini/GPT)"])

# 5. منطق الربط بين الملفات (The Gateway)
if choice == "🏠 الرئيسية":
    st.title("Welcome to Smart Analyst Beast 🔥")
    up = st.file_uploader("ارفع ملفك هنا لتبدأ الترسانة بالعمل", type=['xlsx', 'csv'])
    if up:
        st.session_state['unified_data'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
        st.success("تم شحن 'الوحش' بالبيانات بنجاح!")

elif choice == "📊 Excel Master":
    excel.run_excel_logic() # استدعاء الملف المستقل

elif choice == "🧹 Cleaner Pro":
    cleaner.run_cleaner_logic() # استدعاء ملف التنظيف

elif choice == "🤖 AI Brain (Gemini/GPT)":
    st.subheader("🧠 الذكاء الاصطناعي المركزي")
    # هنا هنحط الكود اللي بيكلم Gemini أو GPT
    user_query = st.text_input("اسأل 'الوحش' عن بياناتك:")
    if user_query and st.session_state['unified_data'] is not None:
        st.info("جاري تحليل البيانات باستخدام AI Core...")
        # الربط الفعلي بيحتاج API Key (ممكن نبرمجه الخطوة الجاية)
        st.write("الرد الذكي سيظهر هنا بناءً على ملفاتك المرفوعة.")
