import streamlit as st
import pandas as pd
import numpy as np
import google.generativeai as genai
import hashlib
import plotly.express as px
from io import BytesIO
from fpdf import FPDF
# 1. الإعدادات الملكية للواجهة
st.set_page_config(page_title="Smart Analyst Ultimate Pro", layout="wide")

# 2. تفعيل ذكاء Gemini (باستخدام كودك الخاص)
genai.configure(api_key="AIzaSyBBiIEEGCzXpv80cwR9yzLXuQdj_J5n9tA")
model = genai.GenerativeModel('gemini-pro')

# وظائف الأمان
def make_hashes(password): return hashlib.sha256(str.encode(password)).hexdigest()
def check_hashes(password, hashed_text): return make_hashes(password) == hashed_text

if 'user_db' not in st.session_state:
    st.session_state.user_db = {"admin": make_hashes("1234"), "semomohamed": make_hashes("123456")} 
if 'auth' not in st.session_state: st.session_state.auth = False

# واجهة الدخول
if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center; color: #fbbf24;'>👑 Smart Analyst Pro Login</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("دخول للنظام"):
            if u in st.session_state.user_db and check_hashes(p, st.session_state.user_db[u]):
                st.session_state.auth = True
                st.rerun()
            else: st.error("بيانات الدخول غير صحيحة")
    st.stop()

# 3. ستايل الألوان المثالية (Power BI Style)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .header-box { background: linear-gradient(90deg, #161b22, #fbbf24); padding: 15px; border-radius: 15px; text-align: center; color: white; border: 2px solid #fbbf24; }
    .stDataEditor { border: 1.5px solid #fbbf24 !important; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# أزرار التحكم العلوية
c1, c2, c3 = st.columns([1, 4, 1])
with c1: st.button("🌐 لغة النظام")
with c3: st.button("⚙️ الإعدادات")
with c2: st.markdown("<div class='header-box'><h1>Smart Analyst Ultimate Pro Edition</h1></div>", unsafe_allow_html=True)

# 4. المساعد الذكي (AI in Data)
with st.sidebar:
    st.image("https://raw.githubusercontent.com/semomhamd/smart-analyst-beast/main/99afc3d2-b6ef-4eda-977f-2fdc4b6621dd.jpg")
    st.header("🤖 مساعدك الذكي Gemini")
    chat = st.text_input("اسأل المساعد عن أي شيء في بياناتك...")
    if chat:
        try:
            res = model.generate_content(chat)
            st.info(res.text)
        except Exception as e: st.error(f"خطأ في الاتصال: {e}")
    st.divider()
    st.markdown("### 🔗 أدوات الربط والتحليل")
    st.button("🔗 Power BI Connector")
    st.button("🔗 Google Sheets Sync")

# 5. الأدوات الاحترافية المطلوبة (Tabs)
t_ex, t_bi, t_py, t_pdf = st.tabs(["📑 Excel Professional", "📊 Dashboards", "🐍 Python Lab", "📥 PDF Export"])

with t_ex:
    st.subheader("📝 Microsoft Excel Workstation")
    up = st.file_uploader("ارفع ملف Excel أو CSV", type=['xlsx', 'csv'])
    if up:
        df = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
        # عرض إكسيل ميكروسوفت التفاعلي بدقة عالية
        st.data_editor(df, use_container_width=True, num_rows="dynamic", height=500)
        st.success("البيانات جاهزة للتحليل")

with t_bi:
    st.subheader("📈 Professional Analytics (High Quality)")
    if up:
        c1, c2 = st.columns(2)
        with c1: x_axis = st.selectbox("المحور الأفقي", df.columns)
        with c2: y_axis = st.selectbox("المحور الرأسي", df.select_dtypes(include=np.number).columns)
        
        fig = px.area(df, x=x_axis, y=y_axis, template="plotly_dark", color_discrete_sequence=['#fbbf24'])
        st.plotly_chart(fig, use_container_width=True)
    else: st.warning("الرجاء رفع الملف أولاً")

with t_py:
    st.subheader("🐍 Advanced Python Engine")
    st.code("import pandas as pd\n# محرك تحليل البيانات المتقدم\nresult = df.describe()\nprint(result)", language='python')
    st.button("Run Python Code")

with t_pdf:
    st.subheader("📥 تقارير PDF عالية الدقة")
    st.write("جاهز للإرسال والطباعة")
    # حل مشكلة الصورة 24 (توليد ملف حقيقي بسيط)
    pdf_buffer = BytesIO()
    pdf_buffer.write(b"Smart Analyst Report Content")
    st.download_button("تحميل التقرير النهائي (PDF)", data=pdf_buffer.getvalue(), file_name="Smart_Analyst_Report.pdf", mime="application/pdf")

st.markdown("<p style='text-align: center; color: #fbbf24; margin-top: 50px;'>Certified System | Designed for semomohamed | 2026</p>", unsafe_allow_html=True)
# ابحث عن التبويب الخاص بالتقارير (غالباً t4 أو tab4) وحط الكود ده جواه:
with t3:
    st.subheader("📥 مركز استخراج التقارير النهائية")
    st.write("اضغط لتوليد ملف PDF احترافي قابل للإرسال")
    
    if st.button("تجهيز التقرير للتحميل"):
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt="Smart Analyst Ultimate Pro", ln=1, align='C')
            pdf.ln(10)
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Certified Data Analysis Report - 2026", ln=2, align='C')
            
            # تصدير الملف بصيغة بايتات متوافقة مع المتصفحات
            pdf_output = pdf.output(dest='S').encode('latin-1')
            
            st.download_button(
                label="تحميل التقرير الآن (PDF)",
                data=pdf_output,
                file_name="Smart_Analyst_Report.pdf",
                mime="application/pdf"
            )
            st.success("✅ الملف جاهز! اضغط على زر التحميل أعلاه")
        except Exception as e:
            st.error(f"خطأ تقني: {e}")
