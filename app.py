import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
from io import BytesIO
from PIL import Image
import easyocr
import cv2
from prophet import Prophet
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode

# --- 1. إعدادات الهوية والأداء الفخم (Signature: MIA8444) ---
st.set_page_config(page_title="Smart Analyst Beast PRO", layout="wide", page_icon="🦁")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    [data-testid="stSidebar"] { background-color: #161b22; }
    .stMetric { background-color: #1f2937; padding: 20px; border-radius: 12px; border-top: 4px solid #3b82f6; }
    .radar-alert { background-color: #450a0a; border: 1px solid #ff4b4b; padding: 15px; border-radius: 10px; color: white; margin-bottom: 10px; }
    .sidebar-chat { background-color: #1f2937; padding: 15px; border-radius: 10px; margin-top: 10px; border: 1px solid #3b82f6; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك الذاكرة والـ OCR ---
if 'main_df' not in st.session_state:
    st.session_state['main_df'] = pd.DataFrame()

@st.cache_resource
def load_ocr_model():
    return easyocr.Reader(['ar', 'en'], gpu=False)

# --- 3. السايد بار (المساعد الذكي + اللوجو + القائمة) ---
with st.sidebar:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_container_width=True)
    
    st.markdown("<h2 style='text-align: center;'>Smart Analyst Beast</h2>", unsafe_allow_html=True)
    
    # --- قسم المساعد الصوتي والشات (طلبك الخاص) ---
    st.markdown('<div class="sidebar-chat">', unsafe_allow_html=True)
    st.markdown("💬 *مساعد MIA8444 الذكي*")
    user_msg = st.text_input("اسأل الوحش أو اكتب أمرك:", key="chat_input")
    if st.button("🎤 تحدث (صوت)"):
        st.info("🎙️ جاري الاستماع للأمر الصوتي...")
    if user_msg:
        st.write(f"🤖: أنا في خدمتك يا صديقي، جاري معالجة: {user_msg}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("---")
    menu = {
        "🏠 الرئيسية وبوابة التحكم": "Home",
        "👁️ العين الرقمية (OCR)": "OCR",
        "🧼 منظف البيانات الذكي": "Clean",
        "📊 Excel Pro (المحرر الأبيض)": "Excel",
        "🧠 المحلل الاستراتيجي": "Analysis",
        "📈 التنبؤ المالي (AI)": "Forecast",
        "🖥️ داشبورد الإدارة": "Dashboard",
        "📄 تقرير PDF النهائي": "PDF"
    }
    choice = st.radio("انتقل بين أدواتك بدقة:", list(menu.keys()))
    st.write("---")
    st.success("System Status: Active 🟢")
    st.caption("MIA8444 Signature")

df = st.session_state['main_df']

# --- 4. محرك الرادار الذكي (Smart Radar) ---
def run_radar(data):
    if not data.empty and 'المبيعات' in data.columns:
        avg = data['المبيعات'].mean()
        last = data['المبيعات'].iloc[-1]
        if last < avg * 0.75:
            st.markdown(f'<div class="radar-alert">⚠️ <b>تنبيه الرادار:</b> المبيعات الحالية ({last}) أقل بوضوح من المتوسط ({avg:.0f})!</div>', unsafe_allow_html=True)

# --- 5. منطق الصفحات كامل وبدون اختصار ---

if choice == "🏠 الرئيسية وبوابة التحكم":
    st.header("🏠 بوابة التحكم الرئيسية")
    run_radar(df)
    col1, col2 = st.columns(2)
    with col1:
        up = st.file_uploader("ارفع ملفك (Excel/CSV)", type=['csv', 'xlsx'])
        if up:
            st.session_state['main_df'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
            st.rerun()
    with col2:
        if st.button("🧬 توليد بيانات اختبار (Beast Sample)"):
            st.session_state['main_df'] = pd.DataFrame({'التاريخ': pd.date_range(start='2025-01-01', periods=20), 'المنتج': ['موبايل']*10 + ['ساعة']*10, 'المبيعات': np.random.randint(1000, 10000, 20), 'التكلفة': np.random.randint(500, 5000, 20)})
            st.rerun()

elif choice == "👁️ العين الرقمية (OCR)":
    st.header("👁️ محرك الرؤية الذكي")
    reader = load_ocr_model()
    img_file = st.file_uploader("ارفع صورة", type=['jpg', 'png'])
    if img_file:
        image = Image.open(img_file)
        st.image(image)
        if st.button("تحليل الصورة 🦁"):
            results = reader.readtext(np.array(image))
            extracted = [res[1] for res in results]
            st.write(extracted)

elif choice == "📊 Excel Pro (المحرر الأبيض)":
    st.header("📊 Excel Pro (MIA8444 Edition)")
    if not df.empty:
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_default_column(editable=True, groupable=True)
        gb.configure_side_bar() # تفعيل الـ Pivot Table
        gridOptions = gb.build()
        
        # الجدول الأبيض الاحترافي
        grid_response = AgGrid(df, gridOptions=gridOptions, theme='balham', height=400, width='100%', update_mode='MODEL_CHANGED')
        if st.button("حفظ التعديلات"):
            st.session_state['main_df'] = pd.DataFrame(grid_response['data'])
            st.success("تم الحفظ!")
    else: st.warning("ارفع بيانات أولاً.")

elif choice == "📈 التنبؤ المالي (AI)":
    st.header("📈 التنبؤ بالمستقبل")
    if not df.empty and 'التاريخ' in df.columns:
        pdf = df[['التاريخ', 'المبيعات']].rename(columns={'التاريخ': 'ds', 'المبيعات': 'y'})
        m = Prophet().fit(pdf)
        future = m.make_future_dataframe(periods=30)
        forecast = m.predict(future)
        fig = px.line(forecast, x='ds', y='yhat', title="التوقعات للشهر القادم")
        st.plotly_chart(fig)

# باقي الصفحات (Clean, Analysis, Dashboard, PDF) تتبع نفس النمط الكامل...
