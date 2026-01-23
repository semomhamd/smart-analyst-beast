import streamlit as st
import pandas as pd
import numpy as np
import easyocr
from PIL import Image
import base64

# 1. إعدادات الهوية البصرية (Smart Analyst)
st.set_page_config(page_title="Smart Analyst", layout="wide", page_icon="📊")

# ميزة تبديل اللغة
if 'lang' not in st.session_state:
    st.session_state.lang = 'العربية'

def switch_lang():
    st.session_state.lang = 'English' if st.session_state.lang == 'العربية' else 'العربية'

# قاموس المصطلحات الاحترافي
texts = {
    'العربية': {
        'title': "Smart Analyst",
        'tabs': ["لوحة القيادة", "المختبر المالي الاحترافي", "الذكاء البصري (OCR)"],
        'total': "إجمالي القيمة المضافة",
        'risk': "مؤشر التقلب (مستوى المخاطر)",
        'growth': "معدل النمو المحقق",
        'efficiency': "معامل كفاءة البيانات",
        'ocr_info': "قم برفع صورة المستند (خط يد أو فاتورة) لتحويلها إلى بيانات رقمية فوراً.",
        'sig': "توقيع الخبير المعتمد: MIA8444"
    },
    'English': {
        'title': "Smart Analyst",
        'tabs': ["Dashboard", "Pro Financial Lab", "Visual Intelligence (OCR)"],
        'total': "Total Added Value",
        'risk': "Volatility Index (Risk Level)",
        'growth': "Achieved Growth Rate",
        'efficiency': "Data Efficiency Factor",
        'ocr_info': "Upload a document image (Handwriting or Invoice) to convert it into digital data.",
        'sig': "Certified Expert Signature: MIA8444"
    }
}
L = texts[st.session_state.lang]

# 2. تصميم الواجهة العالمية (CSS)
st.markdown(f"""
    <style>
    .stApp {{ background-color: #f8f9fa; }}
    [data-testid="stHeader"] {{ background: rgba(0,0,0,0); }}
    .reportview-container .main .block-container {{ padding-top: 2rem; }}
    .footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: #1E3A8A;
        text-align: center;
        padding: 15px;
        font-weight: bold;
        border-top: 2px solid #1E3A8A;
        z-index: 100;
    }}
    .stMetric {{
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }}
    </style>
    """, unsafe_allow_html=True)

# الهيدر الاحترافي
c1, c2 = st.columns([5, 1])
with c1:
    st.title(f"🚀 {L['title']}")
with c2:
    st.button("🌐 Switch Language", on_click=switch_lang)

st.divider()

# 3. محرك التبويبات الذكي
t1, t2, t3 = st.tabs(L['tabs'])

with t1:
    st.info("مرحباً بك في منصة Smart Analyst. المحرك يعمل الآن بأقصى طاقة تحليلية.")
    # عرض اللوجو هنا في الداشبورد
    st.image("40833.jpg", width=150) # تأكد من رفع ملف اللوجو بنفس الاسم على GitHub

with t2:
    st.header(L['tabs'][1])
    file = st.file_uploader("ارفع ملف البيانات المالي:", type=['xlsx', 'csv'])
    if file:
        df = pd.read_excel(file) if file.name.endswith('xlsx') else pd.read_csv(file)
        st.dataframe(df.head(10), use_container_width=True)
        
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if num_cols:
            target = st.selectbox("اختر العمود للتحليل العميق:", num_cols)
            
            # معادلات محاسبية عليا (مخفية)
            total = df[target].sum()
            risk = df[target].std() # الانحراف المعياري
            growth = ((df[target].iloc[-1] - df[target].iloc[0]) / df[target].iloc[0] * 100) if df[target].iloc[0] != 0 else 0
            efficiency = (df[target].mean() / df[target].max()) if df[target].max() != 0 else 0
            
            # عرض النتائج كأنها تقرير خارج من تحت يد أذكى محاسب
            m1, m2, m3, m4 = st.columns(4)
            m1.metric(L['total'], f"{total:,.2f}")
            m2.metric(L['risk'], f"{risk:,.2f}")
            m3.metric(L['growth'], f"{growth:.2f}%")
            m4.metric(L['efficiency'], f"{efficiency:.2%}")

with t3:
    st.header(L['tabs'][2])
    st.markdown(f"*{L['ocr_info']}*")
    img_file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])
    if img_file:
        img = Image.open(img_file)
        st.image(img, width=400)
        if st.button("تحليل المستند"):
            with st.spinner("الوحش يقرأ البيانات الآن..."):
                reader = easyocr.Reader(['ar', 'en'])
                result = reader.readtext(np.array(img))
                final_text = " ".join([res[1] for res in result])
                st.subheader("📝 النص المستخرج بدقة:")
                st.text_area("", final_text, height=200)

# 4. التوقيع العالمي الثابت في الأسفل
st.markdown(f"""
    <div class="footer">
        Smart Analyst &nbsp; | &nbsp; {L['sig']}
    </div>
    """, unsafe_allow_html=True)
