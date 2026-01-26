import streamlit as st

def login_page():
    # تصميم واجهة MIA8444 الاحترافية باللون الأسود والذهبي
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

    st.title("🏆 MIA8444 | THE BEAST")
    st.subheader("نظام التحليل الذكي - الذاكرة السحابية")

    user_input = st.text_input("الإيميل أو رقم الهاتف")
    password = st.text_input("كلمة السر", type="password")

    if st.button("تسجيل الدخول"):
        if user_input and password:
            st.success(f"أهلاً بك يا وحش {user_input}")
            st.session_state['logged_in'] = True
        else:
            st.error("من فضلك أدخل البيانات")

    st.markdown("<br><br><p style='font-size: 12px;'>© 2026 MIA8444 | Beast v3.0</p>", unsafe_allow_html=True)

# التصحيح اللي كان عامل المشكلة (شرطتين تحت بعض)
if _name_ == "_main_":
    login_page()
