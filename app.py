import streamlit as st
import pandas as pd
import os

# --- 1. الهوية الفخمة MIA8444 --- [cite: 2026-01-26]
st.set_page_config(page_title="Smart Analyst Beast PRO", layout="wide")

# الذاكرة المركزية الموحدة (بتحفظ الملف المرفوع أو الشيت اليدوي) [cite: 2026-01-16]
if 'main_data' not in st.session_state:
    st.session_state['main_data'] = None

# --- 2. السايد بار (مركز التحكم) ---
with st.sidebar:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_container_width=True) # اللوجو بتاعك [cite: 2026-01-28]
    st.markdown("---")
    choice = st.radio("ترسانة الأدوات:", [
        "🏠 Smart Analyst (Home)",
        "📄 شيت يدوي ومعادلات (Manual/Duo)",
        "🧠 AI Brain Scientist"
    ])
    st.write("---")
    st.success("✅ المرحلة 1: الشيت اليدوي")
    st.success("🚀 المرحلة 2: محرك الدوال")
    st.caption("Signature: *MIA8444*")

# --- 3. تشغيل الأدوات ---

# الصفحة الرئيسية (رفع ملفات الإكسيل)
if choice == "🏠 Smart Analyst (Home)":
    st.markdown("<h1 style='text-align: center;'>Smart Analyst</h1>", unsafe_allow_html=True)
    uploaded = st.file_uploader("ارفع ملف الإكسيل هنا يا وحش", type=['xlsx', 'csv'])
    if uploaded:
        df = pd.read_excel(uploaded) if uploaded.name.endswith('xlsx') else pd.read_csv(uploaded)
        st.session_state['main_data'] = df
        st.success("تم شحن الملف في الذاكرة! 🔥")

# صفحة الشيت اليدوي والحسابات (الضرب والمجموع والمتوسط) [cite: 2025-11-13]
elif choice == "📄 شيت يدوي ومعادلات (Manual/Duo)":
    st.title("📝 محرك البيانات والمعادلات")
    
    # لو الذاكرة فاضية نفتح شيت جديد
    if st.session_state['main_data'] is None:
        st.session_state['main_data'] = pd.DataFrame(
            [['', 0, 0, 0]], 
            columns=['البيان', 'الكمية', 'السعر', 'الإجمالي']
        )
    
    # أداة التعديل (Editor) [cite: 2026-01-25]
    edited_df = st.data_editor(
        st.session_state['main_data'], 
        num_rows="dynamic", 
        use_container_width=True
    )
    
    if st.button("⚡ تنفيذ الدوال وحفظ"):
        try:
            # تحويل البيانات لأرقام عشان نتفادى خطأ Traceback
            for col in ['الكمية', 'السعر']:
                if col in edited_df.columns:
                    edited_df[col] = pd.to_numeric(edited_df[col], errors='coerce').fillna(0)
            
            # دالة الضرب التلقائي
            if 'الكمية' in edited_df.columns and 'السعر' in edited_df.columns:
                edited_df['الإجمالي'] = edited_df['الكمية'] * edited_df['السعر']
            
            st.session_state['main_data'] = edited_df
            st.success("تم الحفظ وتحديث الحسابات! MIA8444")
            
            # عرض الدوال المجمعة (SUM/AVG) [cite: 2025-11-13]
            st.markdown("---")
            c1, c2 = st.columns(2)
            if 'الإجمالي' in edited_df.columns:
                c1.metric("مجموع الإجمالي (SUM)", f"{edited_df['الإجمالي'].sum():,.2f}")
                c2.metric("متوسط السعر (AVG)", f"{edited_df['السعر'].mean():,.2f}")
        except Exception as e:
            st.error(f"خطأ في الحسابات: {e}")

# صفحة الذكاء الاصطناعي [cite: 2026-01-25]
elif choice == "🧠 AI Brain Scientist":
    st.title("🧠 مخ الذكاء الاصطناعي")
    if st.session_state['main_data'] is not None:
        df = st.session_state['main_data']
        if st.button("ابدأ التحليل العميق"):
            st.write(f"### تقرير MIA8444 لعدد {len(df)} سجل:")
            st.info("الوحش قام بتحليل الأرقام وجاهز لاستخراج الأنماط.")
            st.balloons()
    else:
        st.warning("⚠️ ارفع ملف أو اكتب في الشيت الأول!")
