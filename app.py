import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- 1. الهوية والإعدادات MIA8444 [cite: 2026-01-26] ---
st.set_page_config(page_title="Smart Analyst Beast", page_icon="🦁", layout="wide")

if 'db' not in st.session_state: st.session_state['db'] = None
if 'lang' not in st.session_state: st.session_state['lang'] = "العربية"

# --- 2. السايد بار [cite: 2026-01-26] ---
with st.sidebar:
    try: st.image("8888.jpg", use_column_width=True) # اللوجو [cite: 2026-01-28]
    except: st.title("🦁 Smart Analyst")
    st.write("---")
    choice = st.radio("القائمة:", ["🏠 الرئيسية", "📄 الشيت والكلينر", "🧠 AI Analyst", "📊 الرسوم البيانية", "⚙️ الإعدادات"])
    st.caption("Signature: MIA8444")

# --- 3. الصفحات وتفعيل الأدوات ---

if choice == "🏠 الرئيسية":
    st.header("Smart Analyst Beast")
    st.subheader("You don't have to be a data analyst.. Smart Analyst thinks for you") # [cite: 2026-01-24]
    
    if st.button("🚀 توليد ملف اختبار ضخم (10,000 صف)"):
        st.session_state['db'] = pd.DataFrame(np.random.randint(0, 500, size=(10000, 5)), columns=['A', 'B', 'C', 'D', 'E'])
        st.success("تم شحن الوحش!")

    up = st.file_uploader("ارفع ملفك", type=["csv", "xlsx"])
    if up: 
        st.session_state['db'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)

elif choice == "📄 الشيت والكلينر":
    st.header("📄 محرك المعادلات والكلينر")
    if st.session_state['db'] is not None:
        df = st.session_state['db']
        
        # ميزة الكلينر (Cleaner): حذف القيم الفارغة [cite: 2026-01-18]
        if st.button("🧹 تنظيف البيانات (حذف الفارغ)"):
            st.session_state['db'] = df.dropna()
            st.success("تم التنظيف!")
            st.rerun()

        # ميزة تجميع الأعمدة (Sum Column) [cite: 2025-11-13]
        cols = df.select_dtypes(include=[np.number]).columns.tolist()
        target_col = st.selectbox("اختر العمود لجمعه:", cols)
        if st.button(f"➕ احسب مجموع {target_col}"):
            total = df[target_col].sum()
            st.metric(label=f"إجمالي {target_col}", value=f"{total:,}")

        st.data_editor(st.session_state['db'], use_container_width=True)
    else: st.info("ارفع بيانات أولاً.")

elif choice == "🧠 AI Analyst":
    st.header("🧠 AI Smart Analyst") # [cite: 2026-01-30]
    if st.session_state['db'] is not None:
        df = st.session_state['db']
        st.write("💡 *رؤية الذكاء الاصطناعي:*")
        st.write(f"ملفك يحتوي على {len(df)} سجلات. إليك ملخص ذكي:")
        st.dataframe(df.describe()) # التحليل الإحصائي التلقائي [cite: 2025-11-13]
        
        # حساب المتوسط (AVERAGE) [cite: 2025-11-13, 2026-01-20]
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if num_cols:
            avg_val = df[num_cols[0]].mean()
            st.write(f"متوسط أول عمود رقمي ({num_cols[0]}) هو: *{avg_val:.2f}*")
    else: st.warning("لا توجد بيانات للتحليل.")

elif choice == "📊 الرسوم البيانية":
    st.header("📊 مركز التحليل البصري")
    if st.session_state['db'] is not None:
        df = st.session_state['db']
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if len(num_cols) >= 2:
            x_ax = st.selectbox("المحور الأفقي X:", df.columns)
            y_ax = st.selectbox("المحور الرأسي Y:", num_cols)
            fig = px.bar(df.head(100), x=x_ax, y=y_ax, title="تحليل مرئي (أول 100 صف)") # [cite: 2026-01-18]
            st.plotly_chart(fig, use_container_width=True)
        else: st.error("البيانات لا تحتوي على أعمدة أرقام كافية للرسم.")
    else: st.info("ارفع بيانات أولاً.")
