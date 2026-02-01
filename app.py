import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
from io import BytesIO
import streamlit.components.v1 as components

# 1. إعدادات الهوية الفخمة (MIA8444)
st.set_page_config(page_title="Smart Analyst Beast PRO", page_icon="🦁", layout="wide")

slogan = "You don't have to be a data analyst.. Smart Analyst thinks for you"

if 'db' not in st.session_state:
    st.session_state['db'] = pd.DataFrame()

# --- محرك المساعد الصوتي والشات الثابت ---
def beast_ai_console():
    st.write("---")
    # ميزة المايك (Voice Control)
    voice_js = """
    <script>
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'ar-SA';
    function startDictation() {
        recognition.start();
        recognition.onresult = (event) => {
            const text = event.results[0][0].transcript;
            window.parent.postMessage({type: 'voice_text', data: text}, '*');
            alert("الوحش سمعك وببيقولك: " + text);
        };
    };
    </script>
    <div style="text-align: center;">
        <button onclick="startDictation()" style="width:100%; padding:10px; border-radius:15px; background-color:#FF4B4B; color:white; border:none; cursor:pointer; font-weight:bold;">
            🎤 تحدث مع الوحش (Voice)
        </button>
    </div>
    """
    components.html(voice_js, height=60)
    
    # خانة الشات الثابتة (Chat Console)
    user_query = st.text_input("💬 اسأل الوحش (Chat with MIA8444):", placeholder="اكتب سؤالك هنا...")
    if user_query:
        st.write(f"🦁: جارِ تحليل '{user_query}'...")
    st.write("---")

# 2. السايد بار (مركز التحكم الشامل)
with st.sidebar:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_column_width=True) # اللوجو الثابت [cite: 2026-01-28]
    
    st.markdown(f"<center><b>{slogan}</b></center>", unsafe_allow_html=True)
    
    # استدعاء المايك والشات الثابت تحت اللوجو مباشرة
    beast_ai_console()
    
    menu = ["الرئيسية", "منظف البيانات", "الاكسل برو", "المحلل الذكي", "الرؤية الذكية (OCR)", "المستشار المالي (AI)", "الرسوم البيانيه", "التقرير النهائي"]
    choice = st.radio("انتقل إلى:", menu)
    
    st.info(f"App: Smart Analyst Beast\nSignature: MIA8444")

# محرك العمليات الرئيسي
df = st.session_state['db']

# --- صفحة التنبؤ المالي المدمجة ---
def run_forecasting(data):
    st.subheader("📉 مستشار التوقعات الذكي")
    num_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    if num_cols:
        target = st.selectbox("عمود التنبؤ:", num_cols)
        y = data[target].values
        x = np.arange(len(y))
        prediction = np.poly1d(np.polyfit(x, y, 1))(np.arange(len(y), len(y) + 5))
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("🔮 *توقعات MIA8444 القادمة:*")
            st.table(pd.DataFrame({'الفترة': [f"T+{i+1}" for i in range(5)], 'التوقع': prediction}))
        with col2:
            fig = px.line(title="مسار النمو المتوقع")
            fig.add_scatter(y=y, name="البيانات")
            fig.add_scatter(y=prediction, x=np.arange(len(y), len(y) + 5), name="التوقع")
            st.plotly_chart(fig, use_container_width=True)

# 3. منطق الصفحات
if choice == "الرئيسية":
    st.header("🏠 بوابة البيانات الذكية")
    up = st.file_uploader("ارفع ملفك (Excel/CSV)", type=["csv", "xlsx"])
    if up:
        st.session_state['db'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
        st.success("تم شحن الوحش!")
    if st.button("🚀 توليد بيانات اختبار"):
        st.session_state['db'] = pd.DataFrame({'المنتج': ['موبايل', 'ساعة', 'سماعة']*10, 'المبيعات': np.random.randint(100, 1000, 30)})
        st.rerun()

elif choice == "منظف البيانات":
    st.header("✨ منظف البيانات الاحترافي")
    if not df.empty:
        if st.button("🚀 تنظيف عميق (Deep Clean)"):
            st.session_state['db'] = df.drop_duplicates().fillna(0)
            st.success("تم غسيل البيانات بنجاح!")
            st.dataframe(st.session_state['db'].head())
    else: st.warning("ارفع بياناتك الأول يا بطل")

elif choice == "الاكسل برو":
    st.header("📊 محرر الاكسل الذكي")
    if not df.empty:
        df_ed = st.data_editor(df, use_container_width=True)
        st.session_state['db'] = df_ed
        num_cols = df_ed.select_dtypes(include=[np.number]).columns.tolist()
        if num_cols:
            idx = st.selectbox("تصنيف حسب:", [c for c in df_ed.columns if c != num_cols[0]])
            st.dataframe(df_ed.groupby(idx)[num_cols[0]].sum().reset_index())

elif choice == "المحلل الذكي":
    st.header("🧠 المحلل الذكي (AI Analysis)")
    if not df.empty:
        st.write("📊 *الملخص الإحصائي الشامل:*")
        st.dataframe(df.describe())
    else: st.warning("لا توجد بيانات للتحليل")

elif choice == "المستشار المالي (AI)":
    if not df.empty: run_forecasting(df)
    else: st.warning("ارفع بيانات رقمية للتنبؤ")

elif choice == "الرسوم البيانيه":
    st.header("📈 الرسوم البيانيه")
    if not df.empty:
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if num_cols:
            fig = px.bar(df, x=df.columns[0], y=num_cols[0], template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

elif choice == "التقرير النهائي":
    st.header("📄 تصدير التقرير النهائي")
    if not df.empty:
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        st.download_button("📥 تحميل التقرير (Excel)", data=output.getvalue(), file_name="MIA8444_Report.xlsx")
