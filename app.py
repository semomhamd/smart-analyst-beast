import streamlit as st
import pandas as pd
import easyocr
import numpy as np
from PIL import Image
from datetime import datetime

# 1. نظام اللغات والتوقيع MIA8444
if 'lang' not in st.session_state:
    st.session_state.lang = 'العربية'

def switch_lang():
    st.session_state.lang = 'English' if st.session_state.lang == 'العربية' else 'العربية'

# نصوص الواجهة الاحترافية
translations = {
    'العربية': {
        'title': "THE BEAST | المنظومة الذكية",
        'dev': "المصمم المعتمد: MIA8444",
        'tabs': ["لوحة التحكم", "المختبر المحاسبي", "قارئ خط اليد"],
        'ocr_btn': "ابدأ قراءة الخط الآن",
        'sig': "توقيع مصمم التطبيق المعتمد: MIA8444"
    },
    'English': {
        'title': "THE BEAST | Smart System",
        'dev': "Certified Designer: MIA8444",
        'tabs': ["Dashboard", "Accounting Lab", "Handwriting Reader"],
        'ocr_btn': "Start Reading Now",
        'sig': "Authorized Designer Signature: MIA8444"
    }
}
L = translations[st.session_state.lang]

# 2. التنسيق الجمالي (CSS)
st.set_page_config(page_title=f"The Beast - {st.session_state.lang}", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    .footer-sig { text-align: center; border-top: 2px solid #1E3A8A; padding: 20px; margin-top: 50px; color: #1E3A8A; font-weight: bold; }
    .stMetric { background: white; border: 1px solid #ddd; border-radius: 10px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

# الهيدر وزر اللغة
c1, c2 = st.columns([5, 1])
with c1:
    st.title(L['title'])
    st.write(f"🚀 *{L['dev']}*")
with c2:
    st.button("🌐 Switch Language", on_click=switch_lang)

st.divider()

# 3. التبويبات (Tabs)
t1, t2, t3 = st.tabs(L['tabs'])

with t1:
    st.success("المنظومة تعمل بكامل طاقتها تحت إشراف MIA8444")
    col_a, col_b = st.columns(2)
    col_a.metric("حالة المحرك", "Active / نشط")
    col_b.metric("إصدار النظام", "V2.5 Pro")

with t2:
    st.header(L['tabs'][1])
    file = st.file_uploader("ارفع ملف البيانات (Excel/CSV):", type=['xlsx', 'csv'])
    if file:
        df = pd.read_excel(file) if file.name.endswith('xlsx') else pd.read_csv(file)
        st.dataframe(df.head(10))
        # تحليل حسابي سريع
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if num_cols:
            target = st.selectbox("اختر العمود المالي:", num_cols)
            m1, m2 = st.columns(2)
            m1.metric("الإجمالي (SUM)", f"{df[target].sum():,.2f}")
            m2.metric("المتوسط (AVG)", f"{df[target].mean():,.2f}")

with t3:
    st.header(L['tabs'][2])
    st.info("ارفع صورة لنص مكتوب بخط اليد (فاتورة أو ملاحظات) لتحويلها إلى نص رقمي.")
    img_file = st.file_uploader("ارفع الصورة هنا:", type=['jpg', 'png', 'jpeg'])
    if img_file:
        img = Image.open(img_file)
        st.image(img, width=400, caption="المستند المرفوع")
        if st.button(L['ocr_btn']):
            with st.spinner("الوحش يحلل الخط... برجاء الانتظار قليلاً"):
                # استدعاء محرك الذكاء الاصطناعي
                reader = easyocr.Reader(['ar', 'en'])
                result = reader.readtext(np.array(img))
                final_text = " ".join([res[1] for res in result])
                st.subheader("📝 النص المستخرج:")
                st.text_area("", final_text, height=200)

# 4. التوقيع النهائي
st.markdown(f'<div class="footer-sig">{L["sig"]}</div>', unsafe_allow_html=True)
