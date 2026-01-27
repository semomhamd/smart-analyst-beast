import streamlit as st
import pandas as pd
from PIL import Image
# سنستخدم مكتبة Gemini للذكاء الاصطناعي لاحقاً للقراءة الاحترافية

def run_ocr_app():
    st.markdown("<h2 style='text-align:center; color:#D4AF37;'>👁️ محرك قراءة الصور (The Beast OCR)</h2>", unsafe_allow_html=True)
    
    # 1. منطقة رفع الصور
    uploaded_images = st.file_uploader("ارفع صور الفواتير أو الكشوفات (PNG, JPG)", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

    if uploaded_images:
        st.success(f"تم استلام {len(uploaded_images)} صورة. جاري التجهيز للمعالجة...")
        
        # عرض الصور المرفوعة بشكل شيك
        cols = st.columns(3)
        for idx, img_file in enumerate(uploaded_images):
            with cols[idx % 3]:
                img = Image.open(img_file)
                st.image(img, caption=f"صورة: {img_file.name}", use_container_width=True)

        st.markdown("---")
        
        # 2. زرار السحر (بدء القراءة والتحويل لبيانات)
        if st.button("🪄 استخراج البيانات وتحويلها لجدول"):
            with st.spinner("الوحش يقرأ التفاصيل الآن..."):
                # هنا بنجهز مكان لاستقبال البيانات المستخرجة
                # كمثال مبدئي: هنكريت جدول وهمي كأننا قرأنا البيانات
                extracted_data = {
                    "التاريخ": ["2026-01-27"],
                    "البيان": ["فاتورة مشتريات"],
                    "المبلغ": [1500]
                }
                df_extracted = pd.DataFrame(extracted_data)
                
                st.write("✅ تم استخراج البيانات المبدئية:")
                st.table(df_extracted)
                
                # 3. الربط المركزي (السر اللي اتفقنا عليه)
                if st.button("📤 إرسال البيانات لمحرر الإكسيل"):
                    st.session_state['main_data'] = df_extracted
                    st.success("تم إرسال البيانات! روح دلوقتي على أداة Excel هتلاقيها هناك.")

    else:
        st.info("قم برفع الصور التي تريد استخراج البيانات منها. يدعم خط اليد المكتوب بوضوح.")

# التوقيع MIA8444
st.markdown("<p style='text-align:center; font-size:12px; color:#555;'>MIA8444 | OCR & Vision Engine</p>", unsafe_allow_html=True)
