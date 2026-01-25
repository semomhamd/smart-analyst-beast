import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import requests
from io import BytesIO, StringIO

# ================== 1. إعدادات الهوية والصفحة ==================
st.set_page_config(
    page_title="Smart Analyst Beast",
    page_icon="🐉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تهيئة حالة المستخدم
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'master_data' not in st.session_state: st.session_state.master_data = None

# ================== 2. محرك التصميم الاحترافي (Advanced CSS) ==================
st.markdown("""
<style>
    /* تحسين شكل التطبيق الكلي */
    .stApp { background-color: #0E1117; color: #E0E0E0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* تصميم العنوان الرئيسي */
    .main-header {
        background: linear-gradient(90deg, #00C853, #00E676);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 50px; font-weight: 900; text-align: center; margin-bottom: 0px;
    }
    
    /* توقيع MIA8444 */
    .signature {
        font-size: 14px; font-family: 'Courier New', monospace;
        color: #00C853; text-align: center; letter-spacing: 3px;
        margin-top: -10px; opacity: 0.8; font-weight: bold;
    }

    /* جملة التطبيق الشهيرة */
    .slogan {
        text-align: center; color: #9E9E9E; font-style: italic;
        margin: 20px 0; border-top: 1px solid #333; border-bottom: 1px solid #333; padding: 10px;
    }

    /* تحسين الأزرار */
    .stButton>button {
        background: linear-gradient(45deg, #00C853, #009624);
        color: white; border: none; border-radius: 8px;
        font-weight: bold; transition: 0.3s all; height: 3.5em;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,200,83,0.4); }

    /* الشريط الجانبي */
    [data-testid="stSidebar"] { background-color: #161B22 !important; border-right: 2px solid #00C853; }
</style>
""", unsafe_allow_html=True)

# ================== 3. نظام الدخول المتعدد (Gatekeeper) ==================
def login_screen():
    st.markdown("<div class='main-header'>SMART ANALYST BEAST</div>", unsafe_allow_html=True)
    st.markdown("<div class='signature'>by MIA8444</div>", unsafe_allow_html=True)
    
    # محاولة تحميل اللوجو من الرابط الذي قدمته
    try:
        logo_url = "https://raw.githubusercontent.com/username/repo/branch/99afc3d2-b6ef-4eda-977f-2fdc4b6621dd.jpg"
        st.image(logo_url, width=180)
    except:
        st.markdown("<h1 style='text-align:center;'>🐲</h1>", unsafe_allow_html=True)

    with st.container():
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.markdown("<p style='text-align:center;'>Authorized Personnel Only</p>", unsafe_allow_html=True)
            user = st.text_input("Username")
            pw = st.text_input("Password", type="password")
            if st.button("AUTHENTICATE"):
                if (user == "semomohamed" and pw == "123456") or (user == "mai8444" and pw == "admin"):
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Invalid Authentication Credentials")

if not st.session_state.logged_in:
    login_screen()
    st.stop()

# ================== 4. القائمة الجانبية المتقدمة (Sidebar) ==================
with st.sidebar:
    st.markdown("<div style='text-align:center;'><h1 style='color:#00C853;'>🐲</h1></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center; color:white;'>User: <b>{st.session_state.user}</b></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; font-size:10px; color:#00C853;'>MIA8444 SYSTEM v2.5</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    # أدوات سريعة
    st.write("🛠️ Quick Actions")
    if st.button("Clear Cache"): st.cache_data.clear()
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# ================== 5. الواجهة الرئيسية والعمليات ==================
st.markdown("<div class='main-header'>SMART ANALYST BEAST</div>", unsafe_allow_html=True)
st.markdown("<div class='signature'>Designed & Engineered by MIA8444</div>", unsafe_allow_html=True)
st.markdown("<div class='slogan'>\"You don't have to be a data analyst.. Smart Analyst thinks for you\"</div>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📂 DATA INTAKE", "🧠 SMART CLEANER", "📊 ANALYTICS", "📤 EXPORT"])

# --- Tab 1: معالجة رفع الملفات بدقة ---
with tab1:
    st.subheader("📥 Multi-Source Data Upload")
    uploaded_files = st.file_uploader("Upload CSV, Excel, or Invoice Images", accept_multiple_files=True)
    
    if uploaded_files:
        all_dfs = []
        for file in uploaded_files:
            try:
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                elif file.name.endswith(('.xlsx', '.xls')):
                    df = pd.read_excel(file)
                else:
                    st.warning(f"File {file.name} is an image/pdf. OCR Module standby.")
                    continue
                all_dfs.append(df)
            except Exception as e:
                st.error(f"Error loading {file.name}: {e}")
        
        if all_dfs:
            st.session_state.master_data = pd.concat(all_dfs, ignore_index=True)
            st.success("✅ Files Merged and Loaded into Memory.")
            st.dataframe(st.session_state.master_data.head(10), use_container_width=True)

# --- Tab 2: عمليات التنظيف في الخلفية (Power Query Logic) ---
with tab2:
    st.subheader("🧹 Backend Data Transformation")
    if st.session_state.master_data is not None:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Remove Duplicates"):
                st.session_state.master_data.drop_duplicates(inplace=True)
                st.toast("Duplicates Removed!")
        with col2:
            if st.button("Fix Column Names"):
                st.session_state.master_data.columns = [c.strip().replace(" ", "_").upper() for c in st.session_state.master_data.columns]
                st.toast("Headers Standardized!")
        st.dataframe(st.session_state.master_data.head(10), use_container_width=True)
    else:
        st.info("Waiting for data intake...")

# --- Tab 3: محرك التحليل (Visualization Engine) ---
with tab3:
    st.subheader("📊 Beast Analytics Dashboard")
    if st.session_state.master_data is not None:
        # عملية تحليل بسيطة لإظهار القدرة
        numeric_cols = st.session_state.master_data.select_dtypes(include=[np.number]).columns
        if not numeric_cols.empty:
            selected_col = st.selectbox("Select Metric to Analyze", numeric_cols)
            st.line_chart(st.session_state.master_data[selected_col])
        else:
            st.warning("No numeric data found for charting.")
    else:
        st.info("Connect data source to view analytics.")

# --- Tab 4: التصدير عالي الجودة ---
with tab4:
    st.subheader("📤 Professional Export Center")
    if st.session_state.master_data is not None:
        csv_data = st.session_state.master_data.to_csv(index=False).encode('utf-8')
        st.download_button("Download Cleaned Dataset (CSV)", data=csv_data, file_name="beast_cleaned_data.csv", mime="text/csv")
        st.button("Generate Professional PDF Report (MIA8444 Template)")
    else:
        st.warning("No data available for export.")

# ================== 6. Footer ==================
st.markdown("---")
st.markdown("<p style='text-align:center; color:#444;'>MIA8444 Enterprise Systems | Integrated Data Beast v2.5</p>", unsafe_allow_html=True)
