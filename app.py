import streamlit as st
import pandas as pd
import os

# --- إعدادات MIA8444 ---
st.set_page_config(page_title="Smart Analyst Beast PRO", layout="wide")

if 'main_data' not in st.session_state:
    st.session_state['main_data'] = None

# --- السايد بار (Control Tower) ---
with st.sidebar:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_container_width=True)
    st.markdown("---")
    choice = st.radio("ترسانة الأدوات:", [
        "🏠 Smart Analyst (Home)",
        "📄 إنشاء شيت يدوي (Manual Sheet)",
        "📊 Excel Master",
        "🧠 AI Brain"
    ])
    st.write(f"Verified by: *MIA8444*")

# --- 🏠 الصفحة الرئيسية ---
if choice == "🏠 Smart Analyst (Home)":
    st.markdown("<h1 style='text-align: center;'>Smart Analyst</h1>", unsafe_allow_html=True)
    uploaded = st.file_uploader("ارفع ملفك أو روح افتح شيت فاضي", type=['xlsx', 'csv'])
    if uploaded:
        df = pd.read_excel(uploaded) if uploaded.name.endswith('xlsx') else pd.read_csv(uploaded)
        st.session_state['main_data'] = df
        st.success("البيانات جاهزة! 🔥")

# --- 📄 خاصية الشيت اليدوي (زي الإكسيل بالظبط) ---
elif choice == "📄 إنشاء شيت يدوي (Manual Sheet)":
    st.title("📄 محرك الشيتات اليدوية (Manual Editor)")
    st.info("هنا تقدر تفتح شيت فاضي وتكتب فيه كل حاجة بإيدك يا وحش.")

    # إنشاء شيت فاضي كبداية لو مفيش بيانات
    if st.session_state['main_data'] is None:
        initial_df = pd.DataFrame(
            [['', '', '']], 
            columns=['Column 1', 'Column 2', 'Column 3']
        )
    else:
        initial_df = st.session_state['main_data']

    # أداة التعديل اليدوي (Data Editor)
    st.subheader("📝 ابدأ الكتابة والتعديل:")
    edited_df = st.data_editor(
        initial_df, 
        num_rows="dynamic", # يخليك تضيف صفوف براحتك
        use_container_width=True,
        key="data_editor_beast"
    )

    if st.button("💾 حفظ الشيت في ذاكرة الوحش"):
        st.session_state['main_data'] = edited_df
        st.balloons()
        st.success("تم حفظ شغلك اليدوي بنجاح! MIA8444")

# --- الأدوات التانية (Excel & AI) ---
elif choice == "📊 Excel Master":
    st.title("📊 محرك الحسابات")
    if st.session_state['main_data'] is not None:
        st.dataframe(st.session_state['main_data'])
        # هنا بنحط الدوال اللي اتعلمناها (SUM/AVG) [cite: 2025-11-13]
    else:
        st.warning("افتح شيت يدوي أو ارفع ملف الأول.")
