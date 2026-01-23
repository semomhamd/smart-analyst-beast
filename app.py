import streamlit as st
import pandas as pd
import numpy as np
import google.generativeai as genai
import time

# 1. إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="Smart Analyst Ultimate",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. إعداد الذكاء الاصطناعي (Gemini)
# استبدل XXXXX بالكود اللي آخره n9tA اللي صورتهولي
genai.configure(api_key="XXXXX") 
model = genai.GenerativeModel('gemini-pro')

# 3. نظام تسجيل الدخول (لحماية تطبيقك كـ APK)
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center; color: #fbbf24;'>🔐 Smart Analyst Ultimate</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("برجاء تسجيل الدخول للوصول إلى الأدوات التحليلية")
        user = st.text_input("اسم المستخدم")
        password = st.text_input("كلمة المرور", type="password")
        if st.button("دخول للنظام 🚀"):
            if user == "admin" and password == "1234": # تقدر تغيرهم لأي اسم وباسورد تحبهم
                st.session_state.auth = True
                st.success("تم تسجيل الدخول بنجاح!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("بيانات الدخول غير صحيحة يا صديقي")
    st.stop()

# 4. الستايل المطور (CSS) لتحسين مظهر التطبيق عالمياً
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .stApp { background-color: #0d1117; color: #fbbf24; }
    
    .header-container { 
        display: flex; 
        align-items: center; 
        justify-content: space-between; 
        padding: 15px; 
        background: #161b22; 
        border-radius: 15px; 
        border: 2px solid #fbbf24;
        margin-bottom: 25px;
    }
    .app-title { font-size: 28px; font-weight: bold; color: #fbbf24; margin-right: 20px; }
    .footer-bar { 
        position: fixed; 
        bottom: 0; 
        left: 0;
        width: 100%; 
        background: #161b22; 
        color: #fbbf24; 
        text-align: center; 
        padding: 10px; 
        font-size: 14px;
        border-top: 1px solid #fbbf24;
    }
</style>
""", unsafe_allow_html=True)

# 5. الهيدر (اللوجو الجديد + العنوان)
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown(f"""
    <div class='header-container'>
        <div style='display: flex; align-items: center;'>
            <img src="https://raw.githubusercontent.com/semomhamd/smart-analyst-beast/main/99afc3d2-b6ef-4eda-977f-2fdc4b6621dd.jpg" style="width:70px; border-radius:10px; border: 1px solid #fbbf24;">
            <div class='app-title'>Smart Analyst Ultimate</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_h2:
    lang = st.selectbox("🌐 اللغة", ["العربية", "English"], label_visibility="collapsed")
    profile = st.selectbox("👤 الحساب", ["الملف الشخصي", "الإعدادات", "خروج"], label_visibility="collapsed")

# 6. المساعد الذكي (Gemini AI) في الـ Sidebar
with st.sidebar:
    st.markdown("### 🤖 مساعدك المالي الذكي")
    st.write("أنا مدعوم بذكاء Gemini لتحليل بياناتك.")
    chat_input = st.text_input("اسألني عن أي معادلة أو تحليل...")
    
    if chat_input:
        with st.spinner("جاري التفكير..."):
            try:
                response = model.generate_content(chat_input)
                st.markdown(f"*💡 رد المساعد:*\n\n{response.text}")
            except Exception as e:
                st.error("حدث خطأ في الاتصال بالذكاء الاصطناعي.")

# 7. منطقة العمل الرئيسية (Tabs) لتقسيم الأدوات
t1, t2, t3 = st.tabs(["📊 مركز إدخال البيانات", "🛠️ منصة الأدوات", "📈 النتائج والداشبورد"])

with t1:
    st.markdown("### 📂 رفع ملفات البيانات")
    uploaded_files = st.file_uploader("اختر ملفات Excel أو CSV", accept_multiple_files=True)
    if uploaded_files:
        st.success(f"✅ تم استلام {len(uploaded_files)} ملفات بنجاح.")

with t2:
    st.markdown("### ⚙️ تخصيص المعالجة")
    col_tools1, col_tools2 = st.columns(2)
    with col_tools1:
        st.checkbox("تفعيل Excel Pro Engine", value=True)
        st.checkbox("استخدام AI OCR (قراءة الصور)", value=False)
    with col_tools2:
        st.checkbox("تحليل Python Analytics", value=True)
        st.checkbox("ربط Power BI Dashboard", value=False)

with t3:
    if uploaded_files:
        st.markdown("### 📈 التحليل البياني المبدئي")
        # بيانات تجريبية للرسم
        chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['نمو', 'مصاريف', 'أرباح'])
        st.line_chart(chart_data)
        st.button("تحديث وتحميل التقرير النهائي 📥")
    else:
        st.warning("الرجاء رفع ملفات البيانات في التبويب الأول لتظهر النتائج هنا.")

# 8. الفوتر الثابت (يظهر في أسفل الشاشة دائماً)
st.markdown("<div class='footer-bar'>Smart Analyst Ultimate | Certified System by MIA8444 | 2026</div>", unsafe_allow_html=True)
