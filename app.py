import streamlit as st
import pandas as pd
import numpy as np
import easyocr
from PIL import Image
import os

# 1. إعدادات الهوية (Smart Analyst)
st.set_page_config(page_title="Smart Analyst", layout="wide", page_icon="📊")

if 'lang' not in st.session_state:
    st.session_state.lang = 'العربية'

def switch_lang():
    st.session_state.lang = 'English' if st.session_state.lang == 'العربية' else 'العربية'

texts = {
    'العربية': {
        'title': "Smart Analyst",
        'tabs': ["لوحة القيادة", "المختبر المالي الاحترافي", "الذكاء البصري (OCR)"],
        'total': "إجمالي القيمة المضافة",
        'risk': "مؤشر التقلب (المخاطر)",
        'growth': "معدل النمو",
        'sig': "توقيع الخبير المعتمد: MIA8444"
    },
    'English': {
        'title': "Smart Analyst",
        'tabs': ["Dashboard", "Pro Financial Lab", "Visual Intelligence (OCR)"],
        'total': "Total Added Value",
        'risk': "Volatility Index",
        'growth': "Growth Rate",
        'sig': "Certified Expert Signature: MIA8444"
    }
}
L = texts[st.session_state.lang]

# 2. تصميم الواجهة (CSS) لتثبيت التوقيع تحت
st.markdown(f"""
    <style>
    .stApp {{ background-color: #f8f9fa; }}
    .footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: #1E3A8A;
        text-align: center;
        padding: 10px;
        font-weight: bold;
        border-top: 2px solid #1E3A8A;
        z-index: 999;
    }}
    .stMetric {{ background: white; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border: 1px solid #eee; }}
    </style>
    """, unsafe_allow_html=True)

# الهيدر
c1, c2 = st.columns([5, 1])
with c1:
    st.title(L['title'])
with c2:
    st.button("🌐 Switch Language", on_click=switch_lang)

st.divider()

# 3. التبويبات
t1, t2, t3 = st.tabs(L['tabs'])

with t1:
    st.info("المحرك يعمل الآن بأقصى طاقة تحليلية.")
    # التأكد من وجود اللوجو قبل عرضه لتجنب الخطأ
    if os.path.exists("40833.jpg"):
        st.image("40833.jpg", width=180)
    else:
        st.warning("الرجاء رفع ملف 40833.jpg على GitHub ليظهر اللوجو هنا.")

with t2:
    st.header(L['tabs'][1])
    file = st.file_uploader("Upload Financial Data:", type=['xlsx', 'csv'])
    if file:
        df = pd.read_excel(file) if file.name.endswith('xlsx') else pd.read_csv(file)
        st.dataframe(df.head(10), use_container_width=True)
        
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if num_cols:
            target = st.selectbox("Select Column for Deep Analysis:", num_cols)
            
            # معادلات محاسبية عليا (محرك الوحش الخفي)
            total = df[target].sum()
            risk = df[target].std() # الانحراف المعياري للمخاطر
            growth = ((df[target].iloc[-1] - df[target].iloc[0]) / df[target].iloc[0] * 100) if df[target].iloc[0] != 0 else 0
            
            m1, m2, m3 = st.columns(3)
            m1.metric(L['total'], f"{total:,.2f}")
            m2.metric(L['risk'], f"{risk:,.2f}")
            m3.metric(L['growth'], f"{growth:.2f}%")

with t3:
    st.header(L['tabs'][2])
    img_file = st.file_uploader("Upload Document Image:", type=['jpg', 'png', 'jpeg'])
    if img_file:
        img = Image.open(img_file)
        st.image(img, width=400)
        if st.button("تحليل النص المستند"):
            with st.spinner("جاري التحليل..."):
                reader = easyocr.Reader(['ar', 'en'])
                result = reader.readtext(np.array(img))
                st.subheader("البيانات المستخرجة:")
                st.text_area("", " ".join([res[1] for res in result]), height=200)

# 4. التوقيع الثابت (العالمي)
st.markdown(f'<div class="footer">Smart Analyst &nbsp; | &nbsp; {L["sig"]}</div>', unsafe_allow_html=True)
