import streamlit as st
import pandas as pd
import numpy as np
import os

# --- 1. إعدادات الهوية والسمة MIA8444 --- [cite: 2026-01-26]
st.set_page_config(page_title="Smart Analyst Beast PRO", layout="wide", initial_sidebar_state="expanded")

# محرك الذاكرة الموحد [cite: 2026-01-16]
if 'data' not in st.session_state: st.session_state['data'] = None
if 'theme' not in st.session_state: st.session_state['theme'] = 'Dark'

# --- 2. السايد بار (لوحة التحكم الاحترافية) ---
with st.sidebar:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_container_width=True) # اللوجو الخاص بك [cite: 2026-01-28]
    
    st.markdown("### 🛠️ ترسانة الأدوات")
    menu = st.radio("اختر سلاحك:", [
        "🏠 الرئيسية (Home)", 
        "📄 شيت المعادلات (Manual)", 
        "🧹 منظف البيانات (Cleaner)", 
        "🧠 المحلل الذكي (AI)", 
        "📊 الرسوم البيانية (Charts)",
        "☁️ جوجل شيتس (Cloud)",
        "📑 تصدير التقارير (Export)",
        "⚙️ الإعدادات (Settings)"
    ])
    
    st.write("---")
    # تبديل اللغة والثيم
    col_l, col_t = st.columns(2)
    with col_l: st.button("🌐 EN/AR")
    with col_t: 
        if st.button("🌙/☀️"): 
            st.session_state['theme'] = 'Light' if st.session_state['theme'] == 'Dark' else 'Dark'
    
    st.caption(f"Verified by: *MIA8444*")

# --- 3. تشغيل الـ 8 أدوات (واحدة واحدة وبذكاء) ---

if menu == "🏠 الرئيسية (Home)":
    st.markdown("<h1 style='text-align: center;'>Smart Analyst</h1>", unsafe_allow_html=True)
    st.write("### 'لا داعي لأن تكون محلل بيانات.. المحلل الذكي يفكر بدلاً منك' [cite: 2026-01-24]")
    uploaded = st.file_uploader("ارفع ملفك (Excel/CSV)", type=['xlsx', 'csv'])
    if uploaded:
        st.session_state['data'] = pd.read_excel(uploaded) if uploaded.name.endswith('xlsx') else pd.read_csv(uploaded)
        st.success("تم ترويض البيانات بنجاح! 🔥")

elif menu == "📄 شيت المعادلات (Manual)":
    st.title("📝 محرك المعادلات اليدوي (Duo Engine)")
    st.info("اكتب معادلاتك يدوي أو عدل البيانات المرفوعة.")
    df_to_use = st.session_state['data'] if st.session_state['data'] is not None else pd.DataFrame([['',0,0]], columns=['البيان','الكمية','السعر'])
    
    edited = st.data_editor(df_to_use, num_rows="dynamic", use_container_width=True)
    
    if st.button("⚡ تطبيق معادلات الإكسيل"):
        # محرك حساب تلقائي (الكمية * السعر) [cite: 2025-11-13]
        if 'الكمية' in edited.columns and 'السعر' in edited.columns:
            edited['الإجمالي'] = pd.to_numeric(edited['الكمية'], errors='coerce') * pd.to_numeric(edited['السعر'], errors='coerce')
        st.session_state['data'] = edited
        st.success("تم تحديث الحسابات بتوقيع MIA8444!")

elif menu == "🧠 المحلل الذكي (AI)":
    st.title("🧠 مخ الذكاء الاصطناعي (AI Brain)")
    if st.session_state['data'] is not None:
        df = st.session_state['data']
        if st.button("بدأ التحليل العميق"):
            # حماية من خطأ UFuncNoLoopError
            num_df = df.select_dtypes(include=[np.number])
            st.write(f"📊 عدد السجلات: {len(df)}")
            if not num_df.empty:
                st.metric("أعلى قيمة مكتشفة", f"{num_df.max().max():,.2f}")
                st.balloons()
    else: st.warning("ارفع ملف الأول يا وحش!")

elif menu == "🧹 منظف البيانات (Cleaner)":
    st.title("🧹 المنظف الاحترافي")
    if st.session_state['data'] is not None:
        if st.button("حذف الصفوف الفارغة"):
            st.session_state['data'] = st.session_state['data'].dropna(how='all')
            st.success("تم تنظيف البيانات! MIA8444")
    else: st.warning("لا توجد بيانات لتنظيفها.")

# باقي الأدوات (Charts, Cloud, Export, Settings) يتم تفعيلها بنفس الطريقة..
else:
    st.title(f"🛠️ {menu}")
    st.info("هذه الأداة قيد التفعيل النهائي لضمان أعلى أداء.")
