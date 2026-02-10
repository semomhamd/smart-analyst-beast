import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression
import os

# ======== 1. الذاكرة المركزية (The Unified Brain) ========
if 'active_df' not in st.session_state:
    st.session_state.active_df = None # الذاكرة اللي شايلة البيانات اللي شغالين عليها حالياً

# ======== 2. الهوية والإعدادات (UI/UX) ========
APP_NAME = "Smart Analyst"
AUTHOR_SIGNATURE = "MIA8444"
LOGO_FILE = "8888.jpg"

st.set_page_config(page_title=f"{AUTHOR_SIGNATURE} | {APP_NAME}", layout="wide")

# ستايل "التكنولوجيا المظلمة"
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0d1117; color: white; }}
    .footer {{ position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; padding: 10px; background: #161b22; color: #8b949e; border-top: 1px solid #58a6ff; font-size: 12px; z-index: 100; }}
    </style>
    """, unsafe_allow_html=True)

# ======== 3. القائمة الجانبية (Command Center) ========
with st.sidebar:
    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, use_container_width=True)
    st.markdown(f"<h2 style='text-align:center;'>{APP_NAME}</h2>", unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("القائمة الرئيسية:", [
        "🏠 مركز التحكم والبوابة",
        "📂 ورشة البيانات (رفع وتوليد)",
        "✨ منظف البيانات العالمي",
        "🔮 محرك التنبؤ AI",
        "⚙️ الإعدادات (الترس)"
    ])
    st.markdown("---")
    st.info(f"المستخدم: {AUTHOR_SIGNATURE}")

# ======== 4. تنفيذ الأدوات المربوطة ========

# --- قسم ورشة البيانات (الرفع والتوليد) ---
if menu == "📂 ورشة البيانات (رفع وتوليد)":
    st.header("📂 ورشة عمل البيانات")
    
    tab1, tab2, tab3 = st.tabs(["📤 رفع ملفات", "🧪 توليد بيانات اختبار", "✍️ إدخال يدوي (Excel Pro)"])
    
    with tab1:
        st.subheader("تحميل ملفاتك الخاصة")
        uploaded_file = st.file_uploader("اختر ملف (Excel/CSV) لربطه بالمنصة", type=['csv', 'xlsx'])
        if uploaded_file:
            df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file)
            st.session_state.active_df = df
            st.success("✅ تم تحميل الملف وربطه بالذاكرة المركزية!")

    with tab2:
        st.subheader("مولد بيانات الاختبار (Test Data Generator)")
        rows = st.number_input("عدد الصفوف المراد توليدها:", min_value=10, max_value=1000, value=100)
        if st.button("🚀 توليد بيانات اختبار عالمية"):
            # توليد بيانات عشوائية احترافية للاختبار
            test_data = pd.DataFrame({
                'التاريخ': pd.date_range(start='2025-01-01', periods=rows),
                'المبيعات': np.random.randint(1000, 5000, size=rows),
                'التكاليف': np.random.randint(500, 3000, size=rows),
                'المنطقة': np.random.choice(['القاهرة', 'الأسكندرية', 'دبي', 'الرياض'], size=rows)
            })
            st.session_state.active_df = test_data
            st.success(f"✅ تم توليد {rows} سجل للاختبار وربطهم بالنظام!")

    with tab3:
        st.subheader("Excel Pro: إدخال يدوي")
        if st.session_state.active_df is not None:
            edited_df = st.data_editor(st.session_state.active_df, num_rows="dynamic", use_container_width=True)
            if st.button("💾 حفظ التعديلات اليدوية"):
                st.session_state.active_df = edited_df
                st.success("تم الحفظ!")

# --- قسم المنظف (بيشتغل على الـ active_df أوتوماتيك) ---
elif menu == "✨ منظف البيانات العالمي":
    st.header("✨ محرك التنظيف (Auto-Fix)")
    if st.session_state.active_df is not None:
        df = st.session_state.active_df
        st.write("البيانات الحالية المربوطة:")
        st.dataframe(df.head())
        
        if st.button("🚀 بدء الفحص والتنظيف الشامل"):
            # تنظيف ذكي
            df_clean = df.drop_duplicates().apply(lambda x: x.str.strip() if x.dtype == "object" else x)
            st.session_state.active_df = df_clean
            st.success("✅ تم التنظيف وتحديث "الذاكرة" بنجاح!")
    else:
        st.warning("⚠️ لا توجد بيانات. ارفع ملف أو ولد بيانات من 'ورشة البيانات' أولاً.")

# --- قسم التنبؤ (بيقرأ من الذاكرة) ---
elif menu == "🔮 محرك التنبؤ AI":
    st.header("🔮 AI Prediction Engine")
    if st.session_state.active_df is not None:
        df = st.session_state.active_df
        # كود التنبؤ الذكي هنا...
        st.plotly_chart(px.line(df, title="تحليل الاتجاه العام للبيانات المربوطة"))
    else:
        st.error("⚠️ النظام يحتاج لبيانات للتحليل. اذهب لورشة البيانات أولاً.")

# ======== 5. التوقيع (Footer) ========
st.markdown(f"<div class="footer">Property of {AUTHOR_SIGNATURE} | MIA8444 © 2026</div>", unsafe_allow_html=True)
