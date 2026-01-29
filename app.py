import streamlit as st import pandas as pd import os

================= 1️⃣ إعدادات الصفحة =================

st.set_page_config(page_title="Smart Analyst Beast", layout="wide")

================= 2️⃣ Theme + اللوجو + Language + Settings =================

if 'theme' not in st.session_state: st.session_state.theme = 'Dark'

bg_color = "#0e1117" if st.session_state.theme == 'Dark' else "#ffffff" text_color = "#D4AF37" if st.session_state.theme == 'Dark' else "#000000"

st.markdown(f""" <style> .stApp {{ background-color: {bg_color}; color: {text_color}; }} .footer {{ position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; font-size: 12px; color: #888; padding: 5px; background: transparent; }} </style> """, unsafe_allow_html=True)

Header: Logo + Language + Settings

col_logo, col_space, col_lang, col_set = st.columns([2,6,1,1]) with col_logo: if os.path.exists("8888.jpg"): st.image("8888.jpg", width=120) with col_lang: st.button("🌐 AR/EN") with col_set: with st.expander("⚙️ إعدادات"): if st.button("تبديل النمط Light/Dark"): st.session_state.theme = 'Light' if st.session_state.theme == 'Dark' else 'Dark' st.experimental_rerun()

================= 3️⃣ Sidebar =================

with st.sidebar: st.markdown("## 🛠️ الأدوات") choice = st.radio("", [ "🏠 الرئيسية", "📊 Excel Master", "🧹 Power Query", "📈 Power BI", "🐍 Python Lab", "👁️ OCR Engine", "☁️ Google Sheets", "🖼️ Tableau", "🗄️ SQL Lab", "🤖 AI Brain (Core)" ])

================= 4️⃣ Unified Dataset =================

if 'dataset' not in st.session_state: st.session_state.dataset = pd.DataFrame()

================= 5️⃣ Main Content =================

if choice == "🏠 الرئيسية": st.title("The Ultimate Financial Brain") st.write("مرحباً بك في لوحة تحكم MIA8444") uploaded = st.file_uploader("ارفع أي ملف بيانات (Excel/CSV/ODS) هنا", type=['xlsx','csv','ods']) if uploaded: if uploaded.name.endswith(('xlsx','ods')): st.session_state.dataset = pd.read_excel(uploaded) else: st.session_state.dataset = pd.read_csv(uploaded) st.success("تم رفع البيانات وربطها بالترسانة!")

elif choice == "📊 Excel Master": st.header("📊 Excel Master - Data Editor") df = st.session_state.dataset.copy() if df.empty: st.info("البيانات فارغة، ممكن تبدأ تدخل بيانات يدوي.") df = pd.DataFrame({"Item": [], "Quantity": [], "Price": []})

df = st.data_editor(df, num_rows="dynamic")

if not df.empty:
    df['Total'] = df['Quantity'].fillna(0) * df['Price'].fillna(0)
    df['Discounted'] = df['Total'].apply(lambda x: x*0.9 if x>50 else x)
    st.markdown("### الأعمدة المحسوبة")
    st.dataframe(df)

    # أمثلة SUM, AVERAGE, COUNT
    st.write(f"*Total Quantity:* {df['Quantity'].sum()}")
    st.write(f"*Average Price:* {df['Price'].mean()}")
    st.write(f"*Count of Items:* {df['Item'].count()}")

    # Pivot Table مباشر
    st.markdown("### Pivot Table")
    if st.button("اعرض Pivot Table"):
        pivot = pd.pivot_table(df, index='Item', values=['Quantity','Total'], aggfunc={'Quantity':'sum','Total':'sum'})
        st.dataframe(pivot)

st.session_state.dataset = df

elif choice == "📈 Power BI": st.header("📈 Power BI Dashboard") df = st.session_state.dataset.copy() if df.empty: st.info("ارفع بيانات في الصفحة الرئيسية عشان تولد داشبورد") else: if st.button("Generate Dashboard"): st.subheader("📊 Sales Overview") st.line_chart(df[['Quantity','Total']]) st.bar_chart(df.groupby('Item')['Total'].sum())

elif choice == "🐍 Python Lab": st.header("🐍 Python Lab") df = st.session_state.dataset.copy() code = st.text_area("اكتب كود Python هنا") if st.button("Run Code"): try: exec(code) except Exception as e: st.error(f"Error: {e}")

elif choice == "🤖 AI Brain (Core)": st.header("🤖 AI Brain - Insights") df = st.session_state.dataset.copy() if df.empty: st.info("ارفع بيانات في الصفحة الرئيسية عشان تولد Insights") else: if st.button("Generate Insights"): top_item = df.groupby('Item')['Total'].sum().idxmax() max_total = df['Total'].max() min_total = df['Total'].min() st.write(f"📌 الأعلى مبيعًا: {top_item}") st.write(f"💰 أكبر قيمة: {max_total}") st.write(f"🔻 أقل قيمة: {min_total}")

باقي الأدوات تحت التطوير

else: st.header(f"{choice} - تحت التطوير") df = st.session_state.dataset.copy() st.session_state.dataset = df

================= 6️⃣ Footer =================

st.markdown(f"""

<div class="footer">
Property of Smart Analyst Beast | Signature MIA8444 | v1.0
</div>
""", unsafe_allow_html=True)
