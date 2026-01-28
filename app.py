import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة (يجب أن تكون أول أمر)
st.set_page_config(page_title="Smart Analyst | MIA8444", layout="wide")

# 2. إدارة الثيم (Session State)
if 'theme' not in st.session_state:
    st.session_state.theme = 'Dark'

# 3. القائمة الجانبية (Sidebar)
with st.sidebar:
    st.markdown("<h2 style='text-align:right; color:#D4AF37;'>⚙️ الإعدادات</h2>", unsafe_allow_html=True)
    
    # اختيار اللغة
    st.selectbox("🌐 لغة التطبيق", ["العربية", "English"])
    
    # اختيار النمط (Dark/Light)
    theme_choice = st.radio("🌓 نمط العرض", ["Dark", "Light"], 
                            index=0 if st.session_state.theme == 'Dark' else 1)
    
    if theme_choice != st.session_state.theme:
        st.session_state.theme = theme_choice
        st.rerun()

    st.markdown("---")
    st.markdown("<h3 style='text-align:right;'>🛠️ الأدوات</h3>", unsafe_allow_html=True)
    
    # قائمة الأدوات المتاحة
    tool = st.radio("", [
        "📊 إكسيل الوحش", "🤖 AI Vision", "👁️ OCR", 
        "🧹 Cleaner", "🗄️ SQL", "📄 PDF Pro", 
        "☁️ Sheets", "🐍 Python", "📈 Power BI", "🖼️ Tableau"
    ])

# 4. واجهة اللوجو الفخم (Signature MIA8444)
st.markdown(f"""
    <div style="background-color: #000000; padding: 30px; border-radius: 15px; border: 3px solid #D4AF37; text-align: center; margin-bottom: 25px;">
        <h1 style="color: #D4AF37; font-size: 50px; margin: 0; font-family: 'Arial Black';">SMART ANALYST</h1>
        <p style="color: #ffffff; font-size: 15px; letter-spacing: 3px; margin: 5px 0;">THE BEAST EDITION - INTELLIGENT DATA ENGINE</p>
        <div style="text-align: right; color: #D4AF37; font-size: 12px; font-weight: bold; margin-top:10px;">MIA8444 Signature</div>
    </div>
""", unsafe_allow_html=True)

# 5. منطق تشغيل الأدوات
def start_beast():
    if tool == "📊 إكسيل الوحش":
        st.subheader("📊 محرك إكسيل الذكي (The Beast Engine)")
        
        # إنشاء تبويبين: واحد للرفع وواحد للإدخال اليدوي
        tab1, tab2 = st.tabs(["📂 رفع ملفات", "⌨️ إدخال يدوي"])
        
        with tab1:
            uploaded_file = st.file_uploader("قم برفع ملف Excel أو CSV للبدء في التحليل", type=['xlsx', 'csv', 'xls'])
            if uploaded_file:
                try:
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)
                    st.success("✅ تم تحميل الملف بنجاح!")
                    st.dataframe(df, use_container_width=True)
                except Exception as e:
                    st.error(f"حدث خطأ أثناء قراءة الملف: {e}")
        
        with tab2:
            st.write("أدخل بياناتك مباشرة في الجدول أدناه (يمكنك إضافة صفوف جديدة):")
            # إنشاء جدول بيانات فارغ افتراضي
            init_df = pd.DataFrame(
                columns=["التاريخ", "البيان", "المبلغ", "ملاحظات"],
                index=range(5)
            )
            edited_df = st.data_editor(init_df, num_rows="dynamic", use_container_width=True)
            
            if st.button("🚀 معالجة البيانات اليدوية"):
                final_df = edited_df.dropna(how='all')
                st.write("البيانات الجاهزة للتحليل:")
                st.table(final_df)

    elif tool == "🤖 AI Vision":
        st.subheader("🤖 تحليل الصور بالذكاء الاصطناعي")
        st.info("هذه الميزة تتطلب ربط API Key الخاص بـ Gemini أو GPT-4V.")
        st.file_uploader("ارفع صورة لتحليل محتواها", type=['png', 'jpg', 'jpeg'])

    else:
        st.warning(f"الأداة '{tool}' قيد البرمجة حالياً وسوف تتوفر في التحديث القادم.")

# 6. تشغيل المحرك مباشرة (بدون شروط معقدة)
start_beast()
