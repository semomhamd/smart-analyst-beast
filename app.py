import streamlit as st
import pandas as pd
import numpy as np

# محاولة تشغيل المكتبات بأمان عشان الزهق يخلص
try:
    import plotly.express as px
    CHART_READY = True
except:
    CHART_READY = False

# --- إعدادات الهوية MIA8444 --- [cite: 2026-01-26]
st.set_page_config(page_title="Smart Analyst Beast", layout="wide")

# محرك الذاكرة عشان البيانات ما تضيعش وأنت بتنقل بين الأدوات [cite: 2026-01-16]
if 'main_data' not in st.session_state:
    st.session_state['main_data'] = None

# --- السايد بار (ترسانة الأدوات الـ 8) ---
with st.sidebar:
    st.title("🦁 Smart Analyst")
    tool = st.radio("اختر سلاحك:", [
        "🏠 الرئيسية", "📄 الشيت الذكي", "🧹 المنظف", 
        "🧠 الذكاء الاصطناعي", "📊 الرسوم البيانية", "⚙️ الإعدادات"
    ])
    st.write("---")
    # تصليح كود الواتساب اللي كان عامل مشكلة في الصورة (55f98c54)
    st.markdown(f'<a href="https://wa.me/" target="_blank"><button style="width:100%; border-radius:10px; background-color:#25D366; color:white;">SHARE WHATSAPP</button></a>', unsafe_allow_html=True)
    st.caption("Signature: MIA8444")

# --- تشغيل الأدوات ---

if tool == "🏠 الرئيسية":
    st.header("Smart Analyst Beast")
    st.subheader("مرحباً بك يا حبيب قلبي") # [cite: 2026-01-27]
    file = st.file_uploader("ارفع ملف البيانات (Excel/CSV)", type=['xlsx', 'csv'])
    if file:
        df = pd.read_excel(file) if file.name.endswith('xlsx') else pd.read_csv(file)
        st.session_state['main_data'] = df
        st.success("البيانات دخلت عرين الأسد! ✅")

elif tool == "📄 الشيت الذكي":
    st.header("📝 محرك المعادلات (Duo)")
    if st.session_state['main_data'] is not None:
        # الربط: أي تعديل هنا بيسمع في الرسوم والـ AI [cite: 2026-01-25]
        updated_df = st.data_editor(st.session_state['main_data'], num_rows="dynamic", use_container_width=True)
        if st.button("⚡ حفظ التعديلات"):
            st.session_state['main_data'] = updated_df
            st.balloons()
    else: st.info("ارفع ملف من صفحة الرئيسية أولاً.")

elif tool == "🧠 الذكاء الاصطناعي":
    st.header("🧠 مخ الذكاء الاصطناعي (AI Analysis)")
    if st.session_state['main_data'] is not None:
        df = st.session_state['main_data']
        # حل مشكلة الـ UFunc في الصورة (fada2d) بتصفية الأرقام فقط
        numeric_df = df.select_dtypes(include=[np.number])
        col1, col2 = st.columns(2)
        col1.metric("عدد السجلات", len(df))
        if not numeric_df.empty:
            col2.metric("أعلى قيمة مالية", f"{numeric_df.max().max():,.2f}")
        st.write("تم تحليل البيانات المحدثة بتوقيع MIA8444.")
    else: st.warning("لا توجد بيانات للتحليل.")

elif tool == "📊 الرسوم البيانية":
    st.header("📊 مركز التحليل البصري")
    if not CHART_READY:
        st.error("مكتبة الرسوم ناقصة! تأكد من وجود plotly في ملف requirements.txt")
    elif st.session_state['main_data'] is not None:
        df = st.session_state['main_data']
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if numeric_cols:
            x_ax = st.selectbox("اختر المحور الأفقي:", df.columns)
            y_ax = st.selectbox("اختر محور الأرقام:", numeric_cols)
            fig = px.bar(df, x=x_ax, y=y_ax, title="تحليل الوحش الذكي")
            st.plotly_chart(fig, use_container_width=True)
        else: st.warning("الملف لا يحتوي على أرقام لرسمها!")
    else: st.error("البيانات غير موجودة.")

elif tool == "⚙️ الإعدادات":
    st.header("⚙️ إعدادات الوحش")
    st.selectbox("لغة التطبيق:", ["العربية", "English"])
    st.toggle("الوضع الليلي (MIA8444)")
    st.success("الإعدادات محفوظة.")
