import streamlit as st

def run_auth():
    # التصميم والواجهة (نفس ذوقك الفخم اللي في الصورة)
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

    st.title("🛡️ MIA8444 | THE BEAST")
    st.subheader("(نظام التحليل الذكي - الذاكرة السحابية)")

    # مدخلات البيانات
    user_input = st.text_input("الإيميل أو رقم الهاتف")
    password = st.text_input("كلمة السر", type="password")

    if st.button("تسجيل الدخول"):
        if user_input and password:
            # هنا بنفعل "جلسة الدخول" عشان التطبيق يفتح
            st.session_state['logged_in'] = True
            st.session_state['user_name'] = user_input
            st.success(f"أهلاً بك يا وحش {user_input}")
            st.rerun() # لإعادة التشغيل وفتح التطبيق الرئيسي
        else:
            st.error("من فضلك أدخل البيانات")

# التوقيع MIA8444
st.markdown("<p style='text-align:center; font-size:12px; color:#555;'>MIA8444 | Secured Access</p>", unsafe_allow_html=True)
