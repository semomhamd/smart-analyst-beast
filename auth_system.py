import streamlit as st

def login_page():
    # تصميم واجهة MIA8444 الاحترافية
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
    """, unsafe_content_safe=True)

    st.title("🏆 MIA8444 | THE BEAST")
    st.subheader("نظام التحليل الذكي - الذاكرة السحابية")

    user_input = st.text_input("الإيميل أو رقم الهاتف")
    password = st.text_input("كلمة السر", type="password")

    if st.button("تسجيل الدخول"):
        if user_input and password:
            st.success(f"أهلاً بك يا وحش {user_input}")
        else:
            st.error("من فضلك أدخل البيانات")

    st.markdown("<br><br><p style='font-size: 12px;'>© 2026 MIA8444 | Beast v3.0</p>", unsafe_content_safe=True)

# هنا كان الخطأ.. لازم شرطتين تحت بعض كدة:
if _name_ == "_main_":
    login_page()
