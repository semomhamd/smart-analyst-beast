import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="MIA8444 THE BEAST", layout="wide")

# 2. تصميم الواجهة السوداء والذهبية مباشرة
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
    }
    </style>
""", unsafe_allow_html=True)

# 3. محتوى الصفحة
st.title("🏆 MIA8444 | THE BEAST")
st.subheader("نظام التحليل الذكي - v3.0")

user_input = st.text_input("الإيميل أو رقم الهاتف")
password = st.text_input("كلمة السر", type="password")

if st.button("تسجيل الدخول"):
    if user_input and password:
        st.success(f"أهلاً بك يا وحش {user_input}")
    else:
        st.error("من فضلك أدخل البيانات")

st.markdown("<br><br><p style='font-size: 12px;'>© 2026 MIA8444 | All Rights Reserved</p>", unsafe_allow_html=True)
