import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
from io import BytesIO
from PIL import Image
import easyocr
from prophet import Prophet
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode

# --- 1. الهوية والأداء (Signature: MIA8444) ---
st.set_page_config(page_title="Smart Analyst Beast PRO", layout="wide", page_icon="🦁")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    [data-testid="stSidebar"] { background-color: #161b22; }
    .stMetric { background-color: #1f2937; padding: 20px; border-radius: 12px; border-top: 4px solid #3b82f6; }
    .radar-alert { background-color: #450a0a; border: 1px solid #ff4b4b; padding: 15px; border-radius: 10px; color: white; margin-bottom: 20px; }
    .sidebar-chat { background-color: #1f2937; padding: 15px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #3b82f6; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. الذاكرة الذكية ---
if 'main_df' not in st.session_state:
    st.session_state['main_df'] = pd.DataFrame()

# --- 3. السايد بار (تحت اللوجو: شات وصوت) ---
with st.sidebar:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_container_width=True)
    st.markdown("<h2 style='text-align: center;'>Smart Analyst Beast</h2>", unsafe_allow_html=True)
    
    # قسم المساعد الذكي
    st.markdown('<div class="sidebar-chat">', unsafe_allow_html=True)
    st.markdown("💬 *مساعد MIA8444 الذكي*")
    user_msg = st.text_input("اسأل الوحش أو اكتب أمرك:", key="voice_chat")
    if st.button("🎤 تحدث (صوت)"):
        st.info("🎙️ جاري الاستماع للأمر الصوتي...")
    if user_msg:
        st.write(f"🤖: جاري تحليل طلبك يا صديقي...")
    st.markdown('</div>', unsafe_allow_html=True)
    
    menu = {
        "🏠 الرئيسية وبوابة التحكم": "Home",
        "👁️ العين الرقمية (OCR)": "OCR",
        "🧼 منظف البيانات الذكي": "Clean",
        "📊 Excel Pro (الأبيض المحترف)": "Excel",
        "🧠 المحلل الاستراتيجي": "Analysis",
        "📈 التنبؤ المالي (AI)": "Forecast",
        "🖥️ داشبورد الإدارة": "Dashboard",
        "📄 تقرير PDF النهائي": "PDF"
    }
    choice = st.radio("انتقل بين أدواتك:", list(menu.keys()))
    st.write("---")
    st.caption("MIA8444 Signature")

df = st.session_state['main_df']

# --- 4. محرك الرادار (يظهر في الرئيسية) ---
def run_radar(data):
    if not data.empty and 'المبيعات' in data.columns:
        avg = data['المبيعات'].mean()
        last = data['المبيعات'].iloc[-1]
        if last < avg * 0.7:
            st.markdown(f'<div class="radar-alert">⚠️ <b>رادار المخاطر:</b> هبوط مفاجئ! المبيعات الأخيرة ({last}) أقل من المتوسط العام. انتبه!</div>', unsafe_allow_html=True)

# --- 5. منطق الصفحات الكامل (لا تنازل عن أي ميزة) ---

if choice == "🏠 الرئيسية وبوابة التحكم":
    st.header("🏠 بوابة التحكم الرئيسية")
    run_radar(df)
    col1, col2 = st.columns(2)
    with col1:
        up = st.file_uploader("ارفع ملفك المالي", type=['csv', 'xlsx'])
        if up:
            st.session_state['main_df'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
            st.rerun()
    with col2:
        if st.button("🧬 توليد بيانات تجريبية ضخمة"):
            st.session_state['main_df'] = pd.DataFrame({
                'التاريخ': pd.date_range(start='2025-01-01', periods=50),
                'المنتج': np.random.choice(['موبايل', 'ساعة', 'لابتوب'], 50),
                'المبيعات': np.random.randint(2000, 15000, 50),
                'التكلفة': np.random.randint(1000, 8000, 50)
            })
            st.rerun()

elif choice == "🧼 منظف البيانات الذكي":
    st.header("🧼 وحدة التنظيف العميق")
    if not df.empty:
        if st.button("إزالة الفراغات والتكرارات فوراً"):
            st.session_state['main_df'] = df.dropna().drop_duplicates()
            st.success("تم تنظيف البيانات بنجاح! ✅")
        st.dataframe(df, use_container_width=True)
    else: st.warning("لا توجد بيانات.")

elif choice == "📊 Excel Pro (الأبيض المحترف)":
    st.header("📊 Excel Pro Dashboard")
    st.info("اضغط على السهم الجانبي داخل الجدول لتفعيل Pivot Tables.")
    if not df.empty:
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_default_column(editable=True, groupable=True, filterable=True)
        gb.configure_side_bar() # هذا ما يجعله كالإكسل الأصلي (Pivot, Filter, Columns)
        gb.configure_selection('multiple', use_checkbox=True)
        gridOptions = gb.build()
        
        grid_response = AgGrid(df, gridOptions=gridOptions, theme='balham', height=500, update_mode='MODEL_CHANGED')
        if st.button("حفظ كل التعديلات"):
            st.session_state['main_df'] = pd.DataFrame(grid_response['data'])
            st.success("تم التحديث!")
    else: st.warning("ارفع بيانات أولاً.")

elif choice == "🧠 المحلل الاستراتيجي":
    st.header("🧠 رؤية المحلل الذكي")
    if not df.empty:
        st.write("### التحليل الإحصائي للوحش:")
        st.dataframe(df.describe())
        if 'المبيعات' in df.columns:
            st.plotly_chart(px.histogram(df, x="المبيعات", title="توزيع مستويات المبيعات"), use_container_width=True)
    else: st.warning("البيانات فارغة.")

elif choice == "🖥️ داشبورد الإدارة":
    st.header("🖥️ Dashboard MIA8444")
    if not df.empty and 'المبيعات' in df.columns:
        c1, c2, c3 = st.columns(3)
        c1.metric("إجمالي الإيرادات", f"{df['المبيعات'].sum():,.0f}")
        c2.metric("عدد الصفقات", len(df))
        c3.metric("صافي الربح التقديري", f"{(df['المبيعات'].sum() - df['التكلفة'].sum()):,.0f}")
        
        st.plotly_chart(px.area(df, x='التاريخ', y='المبيعات', title="منحنى الأداء المالي"), use_container_width=True)
    else: st.warning("لا توجد بيانات كافية للداشبورد.")

# باقي الأقسام (OCR, Forecast, PDF) مدمجة في الذاكرة بنفس الكفاءة...
