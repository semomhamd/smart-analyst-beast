import streamlit as st
import pandas as pd
import numpy as np
import os
from PIL import Image

# 1. استيراد الوظائف من ملفاتك (تأكد من عدم وجود مسافات قبل السطور دي)
try:
    from cleaner_pro import clean_data
    from excel_master import process_excel
    from ai_analyst import run_analysis
    from power_bi_hub import show_charts
    from ai_vision import run_ocr
except Exception as e:
    st.error(f"🦁 الوحش بيقولك فيه ملف ناقص أو اسم وظيفة غلط: {e}")

# 2. إعداد الهوية (MIA8444)
st.set_page_config(page_title="Smart Analyst Beast PRO", layout="wide")

# 3. السايد بار (اللوجو + الشات + القائمة)
with st.sidebar:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg") # اللوجو الفخم
    st.markdown("<center><b>Smart Analyst thinks for you</b></center>", unsafe_allow_html=True)
    st.write("---")
    
    # خانة الشات الثابتة
    user_msg = st.text_input("💬 اسأل MIA8444 (شات ثابت):")
    if user_msg:
        st.info(f"🦁 جارِ التفكير في: {user_msg}")
    
    st.write("---")
    menu = ["الرئيسية", "منظف البيانات", "الاكسل برو", "المحلل الذكي", "الرؤية الذكية (OCR)", "الرسوم البيانيه", "المستشار المالي"]
    choice = st.radio("القائمة الرئيسية:", menu)
    st.write("---")
    st.caption("Signature: MIA8444")

# 4. إدارة البيانات (Session State)
if 'db' not in st.session_state:
    st.session_state['db'] = pd.DataFrame()

df = st.session_state['db']

# 5. منطق الصفحات (تشغيل الأدوات)
if choice == "الرئيسية":
    st.header("🏠 بوابة البيانات الذكية")
    up = st.file_uploader("ارفع ملف Excel أو CSV", type=['csv', 'xlsx'])
    if up:
        st.session_state['db'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
        st.success("تم رفع البيانات بنجاح يا بطل!")
    if st.button("🚀 تجربة بيانات اختبار"):
        st.session_state['db'] = pd.DataFrame({'المنتج': ['موبايل', 'ساعة', 'سماعة']*10, 'المبيعات': np.random.randint(100, 1000, 30)})
        st.rerun()

elif choice == "منظف البيانات":
    st.header("🧼 منظف البيانات الاحترافي")
    if not df.empty:
        # استدعاء الوظيفة من ملف cleaner_pro.py
        if st.button("بدء التنظيف العميق ✨"):
            st.session_state['db'] = clean_data(df)
            st.success("البيانات بقت زي الفل!")
            st.dataframe(st.session_state['db'].head())
    else: st.warning("لازم ترفع ملف الأول")

elif choice == "الاكسل برو":
    st.header("📊 محرر الاكسل الذكي")
    if not df.empty:
        process_excel(df) # من ملف excel_master.py
    else: st.warning("الوحش مستني ترفع الملف")

elif choice == "المحلل الذكي":
    st.header("🧠 المحلل الذكي (AI Analysis)")
    if not df.empty:
        run_analysis(df) # من ملف ai_analyst.py

elif choice == "الرؤية الذكية (OCR)":
    st.header("👁️ رؤية الوحش (OCR Vision)")
    run_ocr() # من ملف ai_vision.py

elif choice == "الرسوم البيانيه":
    st.header("📈 الرسوم البيانيه")
    if not df.empty:
        show_charts(df) # من ملف power_bi_hub.py

elif choice == "المستشار المالي":
    st.header("📉 مستشار التوقعات الذكي")
    if not df.empty:
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if num_cols:
            target = st.selectbox("توقع مستقبل عمود:", num_cols)
            y = df[target].values
            pred = np.poly1d(np.polyfit(np.arange(len(y)), y, 1))(np.arange(len(y), len(y) + 5))
            st.write("🔮 توقعات MIA8444 القادمة:")
            st.line_chart(np.append(y, pred)) #
