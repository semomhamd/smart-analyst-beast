import streamlit as st
import pandas as pd
import numpy as np
import google.generativeai as genai
import hashlib
import plotly.express as px
from io import BytesIO
from fpdf import FPDF
from PIL import Image

# 1. إعدادات الواجهة الملكية والأيقونات
st.set_page_config(page_title="Smart Analyst Ultimate Pro", page_icon="👑", layout="wide")

# روابط الأيقونات واللوجو (روابط دائمة)
LOGO_URL = "https://raw.githubusercontent.com/semomhamd/smart-analyst-beast/main/99afc3d2-b6ef-4eda-977f-2fdc4b6621dd.jpg"
EXCEL_ICON = "https://cdn-icons-png.flaticon.com/512/732/732220.png"
CHART_ICON = "https://cdn-icons-png.flaticon.com/512/1162/1162456.png"
OCR_ICON = "https://cdn-icons-png.flaticon.com/512/1055/1055644.png"
PDF_ICON = "https://cdn-icons-png.flaticon.com/512/337/337946.png"

# 2. تفعيل الذكاء الاصطناعي (Gemini) - لمعالجة الصور والبيانات
genai.configure(api_key="AIzaSyBBiIEEGCzXpv80cwR9yzLXuQdj_J5n9tA")
model = genai.GenerativeModel('gemini-1.5-flash') # نسخة تدعم الصور

# 3. نظام الأمان والدخول
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image(LOGO_URL, width=150)
        st.markdown("<h2 style='text-align: center;'>🔐 نظام التحليل المشفر</h2>", unsafe_allow_html=True)
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("دخول آمن", use_container_width=True):
            if u == "semomohamed" and p == "123456":
                st.session_state.auth = True
                st.rerun()
            else: st.error("⚠️ بيانات الدخول غير صحيحة")
    st.stop()

# 4. التصميم الاحترافي (CSS)
st.markdown(f"""
    <style>
    .main-card {{ background-color: #1e1e1e; border-radius: 15px; padding: 20px; border: 1px solid #fbbf24; }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 10px; }}
    .stTabs [data-baseweb="tab"] {{
        background-color: #262626; border-radius: 10px; color: white; padding: 10px 20px; border: 1px solid #333;
    }}
    .stTabs [aria-selected="true"] {{ background-color: #fbbf24 !important; color: black !important; }}
    </style>
    """, unsafe_allow_html=True)

# 5. القائمة الجانبية (الأدوات الذكية)
st.sidebar.image(LOGO_URL, use_container_width=True)
with st.sidebar:
    st.markdown("### 🤖 مساعدك الشخصي")
    user_query = st.text_area("اسأل عن أي شيء في بياناتك أو صورك...")
    if st.button("إرسال استفسار"):
        if user_query:
            try:
                response = model.generate_content(user_query)
                st.info(response.text)
            except: st.error("يرجى التأكد من الـ API Key")

# 6. التبويبات الرئيسية (أيقونات لكل أداة)
t1, t2, t3, t4 = st.tabs([
    "📑 رفع الملفات", 
    "📊 لوحة البيانات", 
    "📷 فحص الفواتير", 
    "📥 تقارير PDF"
])

# --- التبويب الأول: رفع ملفات متعددة ---
with t1:
    st.image(EXCEL_ICON, width=50)
    st.subheader("إدارة الملفات المتعددة")
    uploaded_files = st.file_uploader("ارفع ملفات Excel أو CSV (يمكنك اختيار أكثر من ملف)", type=['xlsx', 'csv'], accept_multiple_files=True)
    
    if uploaded_files:
all_dfs = []
        for file in uploaded_files:
            # قراءة الملف
            df = pd.read_excel(file) if file.name.endswith('xlsx') else pd.read_csv(file)
            
            # تفعيل المحرك الاحترافي (Sprint 1)
            df, logs = smart_analyst_core(df)
            
            # عرض سجل العمليات لكل ملف
            st.success(f"🔍 تم فحص وتنظيف: {file.name}")
            for log in logs:
                st.info(log)
            
            all_dfs.append(df)

        # دمج البيانات في ذاكرة الوحش (Master Data)
        if all_dfs:
            st.session_state.master_df = pd.concat(all_dfs, ignore_index=True)
            st.success(f"✅ تم دمج {len(uploaded_files)} ملفات بنجاح!")
            st.data_editor(st.session_state.master_df, use_container_width=True)
        st.data_editor(st.session_state.master_df, use_container_width=True)

# --- التبويب الثاني: الرسم البياني الذكي ---
with t2:
    st.image(CHART_ICON, width=50)
    st.subheader("التحليل البصري المتقدم")
    if 'master_df' in st.session_state:
        df = st.session_state.master_df
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if num_cols:
            col_to_plot = st.selectbox("اختر العمود للتحليل:", num_cols)
            fig = px.area(df, y=col_to_plot, template="plotly_dark", color_discrete_sequence=['#fbbf24'])
            st.plotly_chart(fig, use_container_width=True)
        else: st.error("لا توجد أرقام للرسم البياني")
    else: st.warning("ارفع الملفات أولاً")

# --- التبويب الثالث: رفع الصور والفواتير (OCR) ---
with t3:
    st.image(OCR_ICON, width=50)
    st.subheader("فحص الفواتير المكتوبة بخط اليد")
    invoice_img = st.file_uploader("ارفع صورة الفاتورة أو المستند", type=['jpg', 'jpeg', 'png'])
    
    if invoice_img:
        img = Image.open(invoice_img)
        st.image(img, caption="الفاتورة المرفوعة", width=400)
        if st.button("تحليل الفاتورة بالذكاء الاصطناعي"):
            with st.spinner("جاري استخراج البيانات..."):
                try:
                    res = model.generate_content(["قم باستخراج البيانات المالية من هذه الصورة بالتفصيل وتحويلها لجدول", img])
                    st.success("تم الاستخراج!")
                    st.markdown(res.text)
                except Exception as e: st.error(f"خطأ في التحليل: {e}")

# --- التبويب الرابع: استخراج التقرير النهائي ---
with t4:
    st.image(PDF_ICON, width=50)
    st.subheader("توليد التقارير الرسمية")
    if st.button("إنشاء ملف PDF للطباعة"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="Smart Analyst Ultimate Report", ln=1, align='C')
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        st.download_button("تحميل التقرير النهائي", data=pdf_bytes, file_name="Smart_Report.pdf", mime="application/pdf")

st.markdown("<hr><center>Certified System | Powered by Gemini 1.5 | 2026</center>", unsafe_allow_html=True)
def smart_analyst_core(df):
    cleaning_logs = []
    # 1. حذف الأعمدة شبه الفارغة
    df = df.dropna(how='all', axis=1) 
    cols_to_drop = [col for col in df.columns if df[col].isnull().mean() > 0.95]
    if cols_to_drop:
        df = df.drop(columns=cols_to_drop)
        cleaning_logs.append(f"🗑️ حذفنا أعمدة فاضية خالص: {', '.join(cols_to_drop)}")
    
    # 2. كاشف التواريخ (الـ 70% اللي اتفقنا عليها)
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                converted = pd.to_datetime(df[col], errors='coerce')
                if converted.notna().mean() > 0.7:
                    df[col] = converted
                    cleaning_logs.append(f"📅 العمود '{col}' اتحول لتاريخ تلقائي.")
            except: continue
            
    return df, cleaning_logs
