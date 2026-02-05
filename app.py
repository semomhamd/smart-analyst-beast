import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import io
import base64

# ======== استيراد آمن ========
try:
    from st_aggrid import AgGrid, GridOptionsBuilder
    AGGRID_AVAILABLE = True
except ImportError:
    AGGRID_AVAILABLE = False

try:
    import duckdb
    DUCKDB_AVAILABLE = True
except ImportError:
    DUCKDB_AVAILABLE = False

try:
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

# ======== إعدادات ========
st.set_page_config(page_title="Smart Analyst Beast", layout="wide", page_icon="🦁")

if 'beast_vault' not in st.session_state:
    st.session_state['beast_vault'] = None
if 'sql_history' not in st.session_state:
    st.session_state['sql_history'] = []

# ======== Sidebar ========
with st.sidebar:
    st.title("🦁 Smart Analyst Beast")
    st.write("v2.0 - Lite Edition")
    
    menu = st.radio("القائمة:", [
        "🏠 الرئيسية",
        "📥 رفع بيانات",
        "📊 Excel Pro", 
        "🧠 تحليل ذكي",
        "🗄️ SQL داخلي",
        "💾 تصدير"
    ])
    
    if st.button("📊 بيانات تجريبية"):
        data = {
            'ID': range(1, 1001),
            'المنتج': [f"منتج_{i%50}" for i in range(1000)],
            'الفئة': np.random.choice(['إلكترونيات', 'ملابس', 'أغذية'], 1000),
            'المبيعات': np.random.randint(1000, 100000, 1000),
            'الفرع': np.random.choice(['القاهرة', 'دبي', 'الرياض'], 1000),
            'التقييم': np.random.randint(1, 6, 1000)
        }
        st.session_state['beast_vault'] = pd.DataFrame(data)
        st.rerun()

df = st.session_state['beast_vault']

# ======== الدوال ========
def get_download_link(df, filename, file_type):
    if file_type == 'csv':
        data = df.to_csv(index=False)
        b64 = base64.b64encode(data.encode()).decode()
        return f'<a href="data:file/csv;base64,{b64}" download="{filename}"><button>📥 CSV</button></a>'
    else:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Data', index=False)
        b64 = base64.b64encode(output.getvalue()).decode()
        return f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}"><button>📥 Excel</button></a>'

def run_sql_query(df, query):
    try:
        con = duckdb.connect(database=':memory:')
        con.register('data', df)
        result = con.execute(query).fetchdf()
        con.close()
        return result, None
    except Exception as e:
        return None, str(e)

# ======== الصفحات ========

if menu == "🏠 الرئيسية":
    st.title("🦁 Smart Analyst Beast")
    st.write("منصة تحليل البيانات الشاملة")
    
    if df is not None:
        st.metric("الصفوف", len(df))
        st.dataframe(df.head())
    else:
        st.info("استخدم 'بيانات تجريبية' من القائمة")

elif menu == "📥 رفع بيانات":
    st.header("رفع ملف")
    uploaded = st.file_uploader("اختر ملف", type=['csv', 'xlsx'])
    if uploaded:
        if uploaded.name.endswith('.csv'):
            df_new = pd.read_csv(uploaded)
        else:
            df_new = pd.read_excel(uploaded)
        st.session_state['beast_vault'] = df_new
        st.success(f"تم استيراد {len(df_new)} صف!")

elif menu == "📊 Excel Pro":
    st.header("Excel Pro")
    if df is not None:
        if AGGRID_AVAILABLE:
            gb = GridOptionsBuilder.from_dataframe(df)
            gb.configure_pagination(paginationPageSize=20)
            gb.configure_default_column(editable=True)
            grid = AgGrid(df, gridOptions=gb.build(), height=500)
            if st.button("حفظ"):
                st.session_state['beast_vault'] = pd.DataFrame(grid['data'])
        else:
            st.dataframe(df)

elif menu == "🧠 تحليل ذكي":
    st.header("تحليل ذكي")
    if df is not None:
        st.dataframe(df.describe())
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            col = st.selectbox("اختر عمود:", numeric_cols)
            st.plotly_chart(px.histogram(df, x=col))

elif menu == "🗄️ SQL داخلي":
    st.header("SQL داخلي")
    if df is not None and DUCKDB_AVAILABLE:
        query = st.text_area("اكتب SQL:", "SELECT * FROM data LIMIT 10")
        if st.button("تشغيل"):
            result, error = run_sql_query(df, query)
            if error:
                st.error(error)
            else:
                st.dataframe(result)
    else:
        st.warning("لا توجد بيانات أو DuckDB غير مثبت")

elif menu == "💾 تصدير":
    st.header("تصدير")
    if df is not None:
        st.markdown(get_download_link(df, "data.csv", "csv"), unsafe_allow_html=True)

st.write("---")
st.caption("Smart Analyst Beast v2.0")
