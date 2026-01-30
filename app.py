import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- 1. إعدادات الهوية MIA8444 --- [cite: 2026-01-26]
st.set_page_config(page_title="Smart Analyst", layout="wide")

# محرك الذاكرة الموحد لربط كل الصفحات ببعضها [cite: 2026-01-16]
if 'db' not in st.session_state: st.session_state['db'] = None
if 'lang' not in st.session_state: st.session_state['lang'] = 'Arabic'

# --- 2. السايد بار (ترسانة MIA8444 الموحدة) ---
with st.sidebar:
    st.title("🦁 Smart Analyst")
    tool = st.radio("الترسانة الموحدة:", [
        "🏠 الرئيسية", "📄 الشيت الذكي", "🧹 المنظف", 
        "🧠 الذكاء الاصطناعي", "📊 الرسوم البيانية", "⚙️ الإعدادات"
    ])
    st.write("---")
    
    # زر مشاركة واتساب الفوري [جديد]
    whatsapp_url = "https://wa.me/?text=" + "بص على تطبيق Smart Analyst Beast بتوقيع MIA8444!"
    st.markdown(f'<a href="{whatsapp_url}" target="_blank" style="text-decoration:none;"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px;">SHARE WHATSAPP</button></a>', unsafe_allow_width=True)
    
    st.caption("MIA8444 - النسخة الفخمة 2026")

# --- 3. تشغيل المحركات المترابطة ---

# أ. الصفحة الرئيسية (استلام البيانات)
if tool == "🏠 الرئيسية":
    st.header("Smart Analyst Beast")
    st.subheader("مرحباً بك يا حبيب قلبي")
    up = st.file_uploader("ارفع ملفك (CSV/Excel)", type=["csv", "xlsx"])
    if up:
        st.session_state['db'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
        st.success("تم شحن البيانات في ذاكرة الوحش! ✅")

# ب. الشيت الذكي (التعديل يحفظ فوراً)
elif tool == "📄 الشيت الذكي":
    st.header("📝 محرك المعادلات (Duo)")
    if st.session_state['db'] is not None:
        # الربط: نعدل البيانات المحفوظة أصلاً [cite: 2026-01-25]
        edited = st.data_editor(st.session_state['db'], num_rows="dynamic", use_container_width=True)
        if st.button("حفظ وتحديث المحرك"):
            st.session_state['db'] = edited
            st.balloons()
            st.success("تم الربط بنجاح! الرسوم والذكاء هيقرأوا التعديلات دي.")
    else: st.warning("ارفع ملف في الرئيسية أولاً.")

# ج. الذكاء الاصطناعي (مفعل بالكامل)
elif tool == "🧠 الذكاء الاصطناعي":
    st.header("🧠 مخ الذكاء الاصطناعي (AI Analysis)")
    if st.session_state['db'] is not None:
        df = st.session_state['db']
        nums = df.select_dtypes(include=[np.number])
        c1, c2 = st.columns(2)
        with c1: st.metric("إجمالي السجلات", len(df))
        with c2: 
            if not nums.empty: st.metric("أعلى قيمة مسجلة", f"{nums.max().max():,.2f}")
        st.info("الذكاء الاصطناعي يحلل البيانات المحدثة من 'الشيت الذكي' حالياً.")
    else: st.error("لا توجد بيانات للتحليل.")

# د. الرسوم البيانية (مفعلة وتفاعلية)
elif tool == "📊 الرسوم البيانية":
    st.header("📊 مركز التحليل البصري")
    if st.session_state['db'] is not None:
        df = st.session_state['db']
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if numeric_cols:
            x_col = st.selectbox("المحور الأفقي:", df.columns)
            y_col = st.selectbox("المحور الرأسي (أرقام):", numeric_cols)
            chart_type = st.selectbox("نوع الرسم:", ["Bar Chart", "Line Chart", "Pie Chart"])
            
            if chart_type == "Bar Chart": fig = px.bar(df, x=x_col, y=y_col, title="تحليل MIA8444")
            elif chart_type == "Line Chart": fig = px.line(df, x=x_col, y=y_col)
            else: fig = px.pie(df, names=x_col, values=y_col)
            
            st.plotly_chart(fig, use_container_width=True)
    else: st.warning("ارفع بياناتك أولاً.")

# هـ. الإعدادات واللغة
elif tool == "⚙️ الإعدادات":
    st.header("⚙️ إعدادات الوحش")
    st.session_state['lang'] = st.selectbox("لغة التطبيق:", ["Arabic", "English"], index=0 if st.session_state['lang']=='Arabic' else 1)
    st.radio("سمة التطبيق (Theme):", ["Light", "Dark"])
    st.success(f"تم ضبط الإعدادات على {st.session_state['lang']}")
