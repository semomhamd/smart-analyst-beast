import streamlit as st
import pandas as pd
import numpy as np
import time
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 تسجيل الدخول")
    user = st.text_input("اسم المستخدم")
    password = st.text_input("كلمة المرور", type="password")
    if st.button("دخول"):
        if user == "admin" and password == "1234": # غيرهم براحتك
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("البيانات غلط")
    st.stop()
# 1. إعدادات الصفحة لدعم الموبايل والكمبيوتر
st.set_page_config(
    page_title="Smart Analyst Ultimate",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. الستايل المطور (أيقونات + تنسيق اللوجو + الألوان)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .stApp { background-color: #0d1117; color: #fbbf24; }
    
    /* اللوجو والاسم المتناسق */
    .header-container { display: flex; align-items: center; justify-content: space-between; padding: 10px; background: #161b22; border-radius: 15px; margin-bottom: 25px; border: 1px solid #fbbf24; }
    .logo-box { background: #fbbf24; color: #0d1117; padding: 10px 20px; border-radius: 10px; font-weight: bold; font-size: 24px; box-shadow: 0 4px 15px rgba(251, 191, 36, 0.3); }
    .app-title { font-size: clamp(18px, 4vw, 30px); font-weight: bold; color: #fbbf24; margin-right: 15px; }
    
    /* أيقونات الأقسام */
    .section-icon { font-size: 24px; margin-left: 10px; vertical-align: middle; }
    
    /* الفوتر */
    .footer-bar { position: fixed; left: 0; bottom: 0; width: 100%; background: #161b22; color: #fbbf24; text-align: center; padding: 8px; border-top: 1px solid #fbbf24; font-size: 12px; z-index: 1000; }
    </style>
    """, unsafe_allow_html=True)

import google.generativeai as genai

# إعداد الذكاء الاصطناعي
# ملاحظة: يفضل مستقبلاً استخدام st.secrets لحماية الكود
genai.configure(api_key="حط_الكود_بتاعك_هنا") 
model = genai.GenerativeModel('gemini-pro')

with st.sidebar:
    st.markdown("### 🤖 مساعدك الذكي")
    st.info("أنا هنا لمساعدتك في تحليل البيانات واقتراح الحلول.")
    chat_input = st.text_input("...اسألني أي شيء عن بياناتك")
    
    if chat_input:
        with st.spinner("جاري التفكير في حل ذكي..."):
            # هنا بنخلي Gemini يرد بجد بناءً على سؤالك
            try:
                response = model.generate_content(chat_input)
                st.write(f"💡 المساعد: {response.text}")
            except Exception as e:
                st.error("حصلت مشكلة بسيطة في الاتصال، جرب تاني.")قتراح: بناءً على سؤالك حول '{chat_input}'، أنصحك بفحص تكرار البيانات في شيت الإكسل المرفوع.")
    st.divider()
    st.markdown("#### 📱 وضع الموبايل: نشط")

# 4. الهيدر (اللوجو والأزرار التفاعلية)
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown(f"""
        <div class='header-container'>
            <div style='display: flex; align-items: center;'>
                <img src="https://raw.githubusercontent.com/semomhamd/smart-analyst-beast/main/99afc3d2-b6ef-4eda-977f-2fdc4b6621dd.jpg" style="width:80px; margin-right:15px;">
                <div class='app-title'>Smart Analyst Ultimate</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col_h2:
    lang = st.selectbox("🌐 اللغة", ["العربية", "English"], label_visibility="collapsed")
    profile = st.selectbox("⚙️ الحساب", ["الملف الشخصي", "الإعدادات", "خروج"], label_visibility="collapsed")

# 5. منطقة العمل الرئيسية (الأقسام الملونة بأيقونات واضحة)
t1, t2, t3 = st.tabs(["📥 مركز الإدخال", "🛠️ منصة الأدوات", "📊 النتائج والداشبورد"])

with t1:
    st.markdown("### <span class='section-icon'>📂</span> مركز إدخال البيانات الذكي", unsafe_allow_html=True)
    uploaded_files = st.file_uploader("ارفع الصور (خط يد)، ملفات PDF، أو إكسل", accept_multiple_files=True)
    if uploaded_files:
        st.success(f"تم استلام {len(uploaded_files)} ملفات بنجاح.")

with t2:
    st.markdown("### <span class='section-icon'>🛠️</span> التحكم في الأدوات", unsafe_allow_html=True)
    auto_mode = st.toggle("تفعيل المعالجة التلقائية الكاملة", value=True)
    
    col_tools = st.columns(2)
    with col_tools[0]:
        st.checkbox("📈 Excel Pro Engine", value=auto_mode)
        st.checkbox("✍️ AI OCR (خط اليد)", value=auto_mode)
    with col_tools[1]:
        st.checkbox("🐍 Python Analytics", value=auto_mode)
        st.checkbox("📊 Power BI Dashboard", value=auto_mode)

with t3:
    st.markdown("### <span class='section-icon'>📉</span> التقارير والداشبورد", unsafe_allow_html=True)
    if uploaded_files:
        st.button("🚀 تحديث النتائج فوراً")
        # مثال لداشبورد زاهي
        chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['أرباح', 'مصاريف', 'نمو'])
        st.line_chart(chart_data)
        st.download_button("📩 تحميل التقرير للمدير (Excel)", "data", file_name="Report.xlsx")
    else:
        st.warning("يرجى رفع ملفات في القسم الأول ليتمكن النظام من عرض النتائج هنا.")

# 6. الفوتر الثابت
st.markdown("<div class='footer-bar'>Smart Analyst Ultimate | Certified System by MIA8444 | 2026</div>", unsafe_allow_html=True)
