import streamlit as st
import pandas as pd
# استيراد الأدوات المتقدمة من الملفات اللي جهزناها
from cleaner_pro import run_cleaner
from ai_analyst import run_analysis
from sql_beast import connect_sql # لربط الـ SQL

# 1. إعداد قاعدة البيانات الموحدة (Unified Dataset)
if 'main_data' not in st.session_state:
    st.session_state['main_data'] = pd.DataFrame()

# 2. تصميم Sidebar الاحترافي
with st.sidebar:
    st.title("🦁 Smart Analyst Beast")
    st.info("You don't have to be a data analyst.. Smart Analyst thinks for you") # شعارنا [cite: 2026-01-24]
    
    choice = st.selectbox("اختر أداة التحليل:", [
        "🏠 Home (Data Hub)",
        "🧹 Power Query (Cleaner)",
        "📊 Excel Master",
        "📈 Power BI Dashboard",
        "🎨 Tableau Connect",
        "🔗 Google Sheets & SQL",
        "🐍 Python Lab",
        "🧠 AI Brain Insights",
        "📄 Final Report Center"
    ])
    st.markdown(f"<h6 style='text-align: center;'>Sign: MIA8444</h6>", unsafe_allow_html=True) # بصمتك [cite: 2026-01-26]

# ================= 3. تنفيذ الوحدات (Phase 1 & 2) =================

if "Home" in choice:
    st.subheader("📥 مركز استقبال البيانات (Data Lake)")
    uploaded = st.file_uploader("ارفع ملفك (Excel/CSV)", type=['xlsx', 'csv'])
    if uploaded:
        st.session_state['main_data'] = pd.read_excel(uploaded) if uploaded.name.endswith('xlsx') else pd.read_csv(uploaded)
        st.success("البيانات دخلت المعمل بنجاح! 🔥")

elif "Power Query" in choice:
    # نداء لملف الـ Cleaner المطور اللي صلحناه سوا
    run_cleaner()

elif "Power BI" in choice or "Tableau" in choice:
    st.subheader(f"📊 واجهة {choice}")
    if not st.session_state['main_data'].empty:
        df = st.session_state['main_data']
        # هنا بنعرض الـ Charts التفاعلية بـ Plotly أو Streamlit Charts
        st.bar_chart(df.select_dtypes(include='number'))
    else:
        st.warning("فين البيانات يا وحش؟ ارفعها من الـ Home الأول.")

elif "AI Brain" in choice:
    # نداء لمخ الذكاء الاصطناعي
    run_analysis(st.session_state['main_data'])

elif "Google Sheets & SQL" in choice:
    st.subheader("🔗 ربط المصادر الخارجية")
    db_url = st.text_input("ادخل رابط SQL أو Google Sheet")
    if st.button("Connect"):
        st.info("جاري الربط مع 'The Beast's Memory'...") # فلسفة الذاكرة [cite: 2026-01-24]
