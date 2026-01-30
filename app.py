import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px  # مكتبة الرسوم البيانية الاحترافية
import urllib.parse

# --- 1. إعدادات التطبيق الأساسية MIA8444 --- [cite: 2026-01-26]
st.set_page_config(page_title="Smart Analyst Beast", layout="wide")

# محرك الذاكرة الموحد (Session State) لربط كل الأدوات [cite: 2026-01-16]
if 'db' not in st.session_state: st.session_state['db'] = None
if 'language' not in st.session_state: st.session_state['language'] = 'Arabic'
if 'theme' not in st.session_state: st.session_state['theme'] = 'Dark'

# --- 2. السايد بار (ترسانة الأدوات المترابطة) ---
with st.sidebar:
    st.title("🦁 Smart Analyst") # تم تغيير الاسم حسب طلبك
    tool = st.radio("الترسانة الموحدة:", [
        "🏠 الرئيسية", "📄 الشيت الذكي", "🧹 المنظف", 
        "🧠 الذكاء الاصطناعي", "📊 الرسوم البيانية", "⚙️ الإعدادات"
    ])
    
    st.write("---")
    # زر مشاركة واتساب [جديد]
    share_msg = urllib.parse.quote(f"بص على تطبيق Smart Analyst Beast بتوقيع MIA8444! عبقرية في تحليل البيانات.")
    st.markdown(f'[![Share on WhatsApp](https://img.shields.io/badge/Share-WhatsApp-25D366?style=for-the-badge&logo=whatsapp)](https://wa.me/?text={share_msg})')
    
    st.caption("MIA8444 - النسخة الفخمة 2026")

# --- 3. تشغيل المحركات المترابطة ---

# أ. الصفحة الرئيسية (مدخل البيانات)
if tool == "🏠 الرئيسية":
    st.header("Smart Analyst Beast")
    st.subheader("مرحباً بك يا حبيب قلبي [cite: 2026-01-27]")
    up = st.file_uploader("ارفع ملفك لتبدأ الترويض", type=["csv", "xlsx"])
    if up:
        st.session_state['db'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
        st.success("البيانات جاهزة في كل الأدوات! ✅")
        st.dataframe(st.session_state['db'].head(10))

# ب. الشيت الذكي (التعديل الذي يسمع في كل مكان)
elif tool == "📄 الشيت الذكي":
    st.header("📝 محرك المعادلات (Duo)")
    data = st.session_state['db'] if st.session_state['db'] is not None else pd.DataFrame([['', 0, 0]], columns=['الصنف', 'الكمية', 'السعر'])
    
    # أي تعديل هنا بيتحفظ في الذاكرة الموحدة [cite: 2026-01-25]
    edited_df = st.data_editor(data, num_rows="dynamic", use_container_width=True)
    
    if st.button("⚡ حفظ وتحديث المحرك"):
        # حساب تلقائي ذكي [cite: 2025-11-13]
        if 'الكمية' in edited_df.columns and 'السعر' in edited_df.columns:
            edited_df['الإجمالي'] = pd.to_numeric(edited_df['الكمية'], errors='coerce') * pd.to_numeric(edited_df['السعر'], errors='coerce')
        st.session_state['db'] = edited_df
        st.success("تم التحديث! روح للرسوم البيانية هتلاقيها اتغيرت لوحدها. 🔥")

# ج. الذكاء الاصطناعي (تحليل البيانات المحدثة)
elif tool == "🧠 الذكاء الاصطناعي":
    st.header("🧠 مخ الذكاء الاصطناعي (AI Analysis)")
    if st.session_state['db'] is not None:
        df = st.session_state['db']
        numeric_df = df.select_dtypes(include=[np.number])
        
        st.write(f"### تحليل MIA8444 الذكي:")
        c1, c2 = st.columns(2)
        with c1: st.metric("إجمالي السجلات", len(df))
        with c2: 
            if not numeric_df.empty: st.metric("أعلى قيمة مسجلة", f"{numeric_df.max().max():,.2f}")
        
        st.write("---")
        st.info("الذكاء الاصطناعي يحلل البيانات المحدثة من 'الشيت الذكي' حالياً.")
    else: st.warning("ارفع ملف أولاً.")

# د. الرسوم البيانية (تفاعل فوري)
elif tool == "📊 الرسوم البيانية":
    st.header("📊 مركز التحليل البصري")
    if st.session_state['db'] is not None:
        df = st.session_state['db']
        cols = df.columns.tolist()
        
        col_x = st.selectbox("اختر العمود الأفقي (X):", cols)
        col_y = st.selectbox("اختر عمود البيانات (Y):", [c for c in cols if df[c].dtype != 'object'])
        
        chart_type = st.radio("نوع الرسم:", ["Bar Chart", "Line Chart", "Pie Chart"])
        
        if chart_type == "Bar Chart": fig = px.bar(df, x=col_x, y=col_y, color=col_x, title="MIA8444 Analytics")
        elif chart_type == "Line Chart": fig = px.line(df, x=col_x, y=col_y, title="MIA8444 Trends")
        else: fig = px.pie(df, names=col_x, values=col_y, title="MIA8444 Distribution")
        
        st.plotly_chart(fig, use_container_width=True)
    else: st.error("لا توجد بيانات لرسمها.")

# هـ. الإعدادات واللغة
elif tool == "⚙️ الإعدادات":
    st.header("⚙️ إعدادات الوحش")
    st.session_state['language'] = st.selectbox("لغة التطبيق:", ["Arabic", "English"], index=0 if st.session_state['language']=='Arabic' else 1)
    st.session_state['theme'] = st.radio("سمة التطبيق:", ["Dark", "Light"])
    st.success(f"تم ضبط الإعدادات على {st.session_state['language']} - {st.session_state['theme']}")

# Footer الموحد [cite: 2026-01-26]
st.markdown("---")
st.caption(f"Signature: MIA8444 | Smart Analyst Beast v2.0")
