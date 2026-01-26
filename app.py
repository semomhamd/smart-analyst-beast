import streamlit as st

# 1. إعدادات الصفحة بالاسم الرسمي الجديد
st.set_page_config(page_title="Smart Analyst The Beast", layout="wide")

# 2. تصميم الواجهة السوداء والذهبية (MIA8444 Signature)
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    h1, h2, h3, p { color: #D4AF37 !important; text-align: center; }
    .stButton>button { 
        background-color: #D4AF37; 
        color: black; 
        border-radius: 20px;
        width: 100%;
        font-weight: bold;
        border: none;
    }
    .stTextInput>div>div>input {
        background-color: #1a1a1a;
        color: #D4AF37;
        border: 1px solid #D4AF37;
    }
    </style>
""", unsafe_allow_html=True)

# 3. محتوى واجهة الدخول
st.title("🏆 Smart Analyst The Beast")
st.subheader("نظام التحليل الذكي - النسخة الفخمة")

user_input = st.text_input("الإيميل أو رقم الهاتف")
password = st.text_input("كلمة السر", type="password")

if st.button("دخول الوحش"):
    if user_input and password:
        st.success(f"أهلاً بك يا وحش MIA8444 - تم تسجيل الدخول")
    else:
        st.error("من فضلك أدخل البيانات")

# 4. حقوق الملكية (Signature)
st.markdown("<br><br><p style='font-size: 12px;'>© 2026 Smart Analyst The Beast | MIA8444</p>", unsafe_allow_html=True)
