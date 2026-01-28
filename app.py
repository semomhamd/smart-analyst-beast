[14:12، 2026/1/28] Semo Lamar: logo_path = "8888.jpg"
if os.path.exists(logo_path):
    st.image(logo_path, width=120)
else:
    st.warning(f"اللوجو مش موجود! تأكد من وجود الملف: {logo_path}")
[14:29، 2026/1/28] Semo Lamar: import streamlit as st
import pandas as pd
from pivottablejs import pivot_ui
import os

# ================= 1️⃣ إعدادات الصفحة =================
st.set_page_config(page_title="Smart Analyst Beast", layout="wide")

# ================= 2️⃣ Theme + اللوجو =================
if 'theme' not in st.session_state:
    st.session_state.theme = 'Dark'

bg_color = "#0e1117" if st.session_state.theme == 'Dark' else "#ffffff"
text_color = "#D4AF37" if st.session_state.theme == 'Dark' else "#000000"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; color: {text_color}; }}
    .footer {{ position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; font-size: 12px; color: #888; padding: 5px; background: transparent; }}
    </style>
""", unsafe_allow_html=True)

# Header: Logo + Language + Settings
col_logo, col_space, col_lang, col_set = st.columns([2,6,1,1])
with col_logo:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", width=120)
with col_lang:
    st.button("🌐 AR/EN")
with col_set:
    with st.expander("⚙️ إعدادات"):
        if st.button("تبديل النمط Light/Dark"):
            st.session_state.theme = 'Light' if st.session_state.theme == 'Dark' else 'Dark'
            st.experimental_rerun()

# ================= 3️⃣ القائمة الجانبية =================
with st.sidebar:
    st.markdown("## 🛠️ الأدوات")
    choice = st.radio("", [
        "🏠 الرئيسية",
        "📊 Excel Master",
        "🧹 Power Query",
        "📈 Power BI",
        "🐍 Python Lab",
        "👁️ OCR Engine",
        "☁️ Google Sheets",
        "🖼️ Tableau",
        "🗄️ SQL Lab",
        "🤖 AI Brain (Core)"
    ])

# ================= 4️⃣ Dataset موحد =================
if 'dataset' not in st.session_state:
    st.session_state.dataset = pd.DataFrame()

# ================= 5️⃣ Main Content =================
if choice == "🏠 الرئيسية":
    st.title("The Ultimate Financial Brain")
    st.write("مرحباً بك في لوحة تحكم MIA8444")
    uploaded = st.file_uploader("ارفع أي ملف بيانات (Excel/CSV/ODS) هنا", type=['xlsx','csv','ods'])
    if uploaded:
        if uploaded.name.endswith('xlsx') or uploaded.name.endswith('ods'):
            st.session_state.dataset = pd.read_excel(uploaded)
        else:
            st.session_state.dataset = pd.read_csv(uploaded)
        st.success("تم رفع البيانات وربطها بالترسانة!")

elif choice == "📊 Excel Master":
    st.header("📊 Excel Master - Data Editor")
    df = st.session_state.dataset.copy()

    if df.empty:
        st.info("البيانات فارغة، ممكن تبدأ تدخل بيانات يدوي.")
        # مثال: هيكل بيانات افتراضي
        df = pd.DataFrame({
            "Item": [],
            "Quantity": [],
            "Price": []
        })

    # Data Editor تفاعلي
    df = st.data_editor(df, num_rows="dynamic")

    # أعمدة محسوبة ديناميكي
    if not df.empty:
        df['Total'] = df['Quantity'].fillna(0) * df['Price'].fillna(0)
        df['Discounted'] = df['Total'].apply(lambda x: x*0.9 if x>50 else x)
        st.markdown("### الأعمدة المحسوبة")
        st.dataframe(df)

        # مثال SUM/AVERAGE/COUNT
        st.write(f"*Total Quantity:* {df['Quantity'].sum()}")
        st.write(f"*Average Price:* {df['Price'].mean()}")
        st.write(f"*Count of Items:* {df['Item'].count()}")

        # Pivot Table
        st.markdown("### Pivot Table")
        pivot_ui(df)  # يفتح نافذة Pivot Table

    # حفظ التغييرات للـ Session
    st.session_state.dataset = df

elif choice == "🧹 Power Query":
    st.header("Power Query - Data Cleaning")
    df = st.session_state.dataset.copy()
    st.write("هنا ممكن تعمل تنظيف للبيانات، إزالة قيم مكررة، تحويل الأنواع، إلخ...")
    st.session_state.dataset = df

elif choice == "📈 Power BI":
    st.header("Power BI Hub - Visualizations")
    df = st.session_state.dataset.copy()
    st.write("هنا تقدر تعمل Charts، Graphs، Measures، Filters")
    st.session_state.dataset = df

elif choice == "🐍 Python Lab":
    st.header("Python Lab - Advanced Analytics")
    df = st.session_state.dataset.copy()
    st.write("هنا ممكن تكتب كود Python لتحليل البيانات والتنبؤات")
    st.session_state.dataset = df

elif choice == "🗄️ SQL Lab":
    st.header("SQL Lab - Queries")
    df = st.session_state.dataset.copy()
    st.write("هنا ممكن تكتب Queries على البيانات")
    st.session_state.dataset = df

elif choice == "☁️ Google Sheets":
    st.header("Google Sheets Sync")
    df = st.session_state.dataset.copy()
    st.write("ربط البيانات مع Google Sheets وSync تلقائي")
    st.session_state.dataset = df

elif choice == "🖼️ Tableau":
    st.header("Tableau Connector")
    df = st.session_state.dataset.copy()
    st.write("ربط البيانات مع Tableau وعرض Dashboards")
    st.session_state.dataset = df

elif choice == "👁️ OCR Engine":
    st.header("OCR Engine - Extract from Images")
    st.write("ارفع صورة والفواتير تتحول لبيانات رقمية")
    st.session_state.dataset = st.session_state.dataset

elif choice == "🤖 AI Brain (Core)":
    st.header("AI Brain - Insights & Suggestions")
    df = st.session_state.dataset.copy()
    st.text_input("اسأل الوحش عن بياناتك:", placeholder="اكتب سؤالك هنا...")
    st.write("الذكاء الاصطناعي يحلل البيانات ويقترح Insights / Formulas / Reports")
    st.session_state.dataset = df

# ================= 6️⃣ Footer =================
st.markdown(f"""
<div class="footer">
Property of Smart Analyst Beast | Signature MIA8444 | v1.0
</div>
""", unsafe_allow_html=True)
