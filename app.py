import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
from io import BytesIO
import streamlit.components.v1 as components
from PIL import Image
import pytesseract

# 1. إعدادات الهوية الفخمة (MIA8444)
st.set_page_config(page_title="Smart Analyst Beast PRO", page_icon="🦁", layout="wide")
slogan = "You don't have to be a data analyst.. Smart Analyst thinks for you"

if 'db' not in st.session_state:
    st.session_state['db'] = pd.DataFrame()

# --- مركز التحكم الصوتي (Voice Control Active) ---
def beast_voice_active():
    st.write("---")
    voice_js = """
    <script>
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'ar-SA';
    function startDictation() {
        const btn = document.getElementById("beast-mic");
        btn.innerHTML = "🌀 جاري الاستماع للوحش...";
        btn.style.backgroundColor = "#2ecc71";
        recognition.start();
        recognition.onresult = (event) => {
            const text = event.results[0][0].transcript;
            window.parent.postMessage({type: 'voice_text', data: text}, '*');
            btn.innerHTML = "🎤 ابدأ التحدث (Voice)";
            btn.style.backgroundColor = "#FF4B4B";
            alert("MIA8444 سمعك بتقول: " + text);
        };
    };
    </script>
    <button id="beast-mic" onclick="startDictation()" style="width:100%; padding:12px; border-radius:15px; background-color:#FF4B4B; color:white; border:none; cursor:pointer; font-weight:bold;">
        🎤 ابدأ التحدث (Voice)
    </button>
    """
    components.html(voice_js, height=70)

# 2. السايد بار (ثابت مع اللوجو والشات والمايك)
with st.sidebar:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_column_width=True) # اللوجو ثابت
    
    st.markdown(f"<center><b>{slogan}</b></center>", unsafe_allow_html=True)
    
    beast_voice_active() # المايك تحت اللوجو مباشرة
    
    chat_input = st.text_input("💬 شات MIA8444 الثابت:", placeholder="اسأل الوحش أي حاجة...") # خانة شات ثابتة [cite: 2026-01-07]
    if chat_input:
        st.info(f"🦁 جاري تحليل طلبك: {chat_input}")
    
    st.write("---")
    menu = ["الرئيسية", "منظف البيانات", "الاكسل برو", "المحلل الذكي", "الرؤية الذكية (OCR)", "المستشار المالي (AI)", "الرسوم البيانيه", "التقرير النهائي"]
    choice = st.radio("القائمة الرئيسية:", menu)
    st.write("---")
    st.info("App: Smart Analyst Beast\nSignature: MIA8444")

df = st.session_state['db']

# 3. تشغيل الرؤية الذكية (OCR Engine) - ميزة محمد المفضلة
if choice == "الرؤية الذكية (OCR)":
    st.header("👁️ رؤية الوحش الذكية (Active OCR)")
    st.write("حول صور التقارير الورقية إلى بيانات رقمية في ثانية.")
    
    col1, col2 = st.columns(2)
    with col1:
        img = st.file_uploader("ارفع صورة التقرير", type=['png', 'jpg', 'jpeg'])
    with col2:
        cam = st.camera_input("أو صور التقرير بالماكينة")
    
    active_img = img if img else cam
    if active_img:
        image = Image.open(active_img)
        st.image(image, caption="الصورة الحالية", width=400)
        if st.button("🔍 ابدأ المسح الضوئي (Start OCR)"):
            with st.spinner("MIA8444 يقرأ البيانات دلوقت..."):
                try:
                    text = pytesseract.image_to_string(image, lang='ara+eng')
                    st.success("تمت القراءة!")
                    st.text_area("النص المستخرج:", text, height=150)
                    # تحويل النص لجدول بيانات بسيط
                    lines = [l.split() for l in text.split('\n') if l.strip()]
                    if lines:
                        st.session_state['db'] = pd.DataFrame(lines)
                        st.write("✅ تم تحديث قاعدة بيانات الوحش بنجاح.")
                except Exception as e:
                    st.error(f"تأكد من تنصيب tesseract على النظام: {e}")

# --- باقي الصفحات (نفس القوة والاستقرار) ---
elif choice == "الرئيسية":
    st.header("🏠 بوابة البيانات")
    up = st.file_uploader("ارفع ملف Excel/CSV", type=["csv", "xlsx"])
    if up:
        st.session_state['db'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
        st.success("تم شحن الوحش بالبيانات!")

elif choice == "المستشار المالي (AI)":
    st.header("📉 مستشار التوقعات الذكي")
    if not df.empty:
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if num_cols:
            target = st.selectbox("اختر العمود للتنبؤ بمستقبله:", num_cols)
            y = df[target].values
            prediction = np.poly1d(np.polyfit(np.arange(len(y)), y, 1))(np.arange(len(y), len(y) + 5))
            st.write("🔮 التوقعات للفترات الـ 5 القادمة:")
            st.table(pd.DataFrame({'الفترة': [f"T+{i+1}" for i in range(5)], 'التوقع': prediction}))
            st.line_chart(np.append(y, prediction)) #

elif choice == "التقرير النهائي":
    st.header("📄 تصدير التقرير النهائي")
    if not df.empty:
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        st.download_button("📥 تحميل التقرير (Excel)", output.getvalue(), "MIA8444_Beast_Report.xlsx") #
