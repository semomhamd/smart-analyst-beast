import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
import io
import base64
from io import BytesIO
import hashlib
import json
import os

warnings.filterwarnings('ignore')

# ======= الإعدادات الأساسية =======
AUTHOR_SIGNATURE = "MIA8444"
APP_NAME = "Smart Analyst The Beast"
APP_VERSION = "5.0.0-Enterprise"
LOGO_FILE = "8888.jpg"

st.set_page_config(
    page_title=f"{AUTHOR_SIGNATURE} | {APP_NAME}",
    page_icon="🦁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======= تهيئة Session State =======
def init_session():
    defaults = {
        'beast_df': None,
        'original_df': None,
        'cleaning_log': [],
        'forecast_results': None,
        'report_data': {},
        'upload_count': 0,
        'excel_data': None,
        'theme': 'dark',
        'language': 'ar'
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session()

# ======= نظام اللغات =======
LANG = {
    'ar': {
        'upload_section': '📤 رفع وإنشاء البيانات',
        'power_query_section': '⚡ Power Query والتنظيف',
        'dashboard_section': '📊 Power BI Dashboard',
        'ai_section': '🧠 التنبؤ الذكي AI',
        'report_section': '📄 التقرير الاحترافي',
    },
    'en': {
        'upload_section': '📤 Upload & Create Data',
        'power_query_section': '⚡ Power Query & Cleaning',
        'dashboard_section': '📊 Power BI Dashboard',
        'ai_section': '🧠 AI Prediction Engine',
        'report_section': '📄 Professional Report',
    }
}

def txt(key):
    return LANG[st.session_state.language].get(key, key)

# ======= CSS =======
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;700;900&display=swap');
    * { font-family: 'Tajawal', sans-serif; direction: rtl; }
    .stApp { background: linear-gradient(135deg, #0a0e17 0%, #1a1f2e 50%, #0f172a 100%); color: #f8fafc; }
    .main-header {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 900;
        text-align: center;
    }
    .section-card {
        background: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 24px;
        padding: 2rem;
        margin: 1rem 0;
    }
    .kpi-card {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        color: white;
    }
    .kpi-value { font-size: 2rem; font-weight: 900; }
    .recommendation-item {
        background: rgba(16, 185, 129, 0.1);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-right: 3px solid #10b981;
    }
    .logo-container { text-align: center; padding: 1rem; }
    .logo-container img { max-width: 120px; border-radius: 15px; }
</style>
""", unsafe_allow_html=True)

# ======= Sidebar =======
with st.sidebar:
    st.markdown("<div class='logo-container'>", unsafe_allow_html=True)
    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, use_container_width=True)
    else:
        st.markdown("<div style='font-size: 4rem;'>🦁</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown(f"<h1 class='main-header' style='font-size:1.5rem;'>{APP_NAME}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:#94a3b8;'>v{APP_VERSION} | {AUTHOR_SIGNATURE}</p>")
    st.markdown("---")
    
    sections = [txt('upload_section'), txt('power_query_section'), txt('dashboard_section'), 
                txt('ai_section'), txt('report_section')]
    selected_section = st.radio("القائمة:", sections, label_visibility="collapsed")
    
    with st.expander("⚙️ الإعدادات"):
        lang = st.selectbox("اللغة:", ["العربية 🇸🇦", "English 🇬🇧"])
        st.session_state.language = 'ar' if 'العربية' in lang else 'en'
    
    st.markdown("---")
    st.markdown("### 📊 حالة البيانات")
    if st.session_state.beast_df is not None:
        df = st.session_state.beast_df
        st.success(f"✅ {len(df):,} سجل | {len(df.columns)} عمود")
    else:
        st.info("ℹ️ لا توجد بيانات")

# ======= القسم 1: رفع البيانات =======
def render_upload():
    st.markdown(f"<h1 class='main-header'>{txt('upload_section')}</h1>", unsafe_allow_html=True)
    
    tabs = st.tabs(["📁 رفع ملفات", "🎲 بيانات اختبار", "📊 Excel احترافي"])
    
    with tabs[0]:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        files = st.file_uploader("اختر الملفات:", type=['csv', 'xlsx', 'json'], accept_multiple_files=True)
        
        if files:
            for file in files:
                try:
                    if file.name.endswith('.csv'):
                        df = pd.read_csv(file)
                    elif file.name.endswith('.xlsx'):
                        df = pd.read_excel(file, engine='openpyxl')
                    else:
                        df = pd.read_json(file)
                    
                    st.success(f"✅ {file.name}: {len(df):,} سجل")
                    
                    if st.button(f"استخدام {file.name}", key=file.name):
                        st.session_state.beast_df = df.copy()
                        st.success("تم التحميل!")
                        
                except Exception as e:
                    st.error(f"❌ خطأ في {file.name}: {e}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tabs[1]:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            n_records = st.number_input("عدد السجلات:", 10, 100000, 1000, step=100)
            data_type = st.selectbox("النوع:", ["مبيعات 💰", "عملاء 👥", "موظفين 👔"])
        
        with col2:
            if st.button("🚀 توليد", use_container_width=True):
                np.random.seed(42)
                
                if "مبيعات" in data_type:
                    df = pd.DataFrame({
                        'التاريخ': pd.date_range('2024-01-01', periods=n_records, freq='D'),
                        'المبيعات': np.random.normal(50000, 15000, n_records).clip(0).round(2),
                        'العملاء': np.random.poisson(150, n_records),
                        'المنطقة': np.random.choice(['الشمال', 'الجنوب', 'الشرق', 'الغرب'], n_records),
                        'الفئة': np.random.choice(['إلكترونيات', 'ملابس', 'أغذية'], n_records)
                    })
                elif "عملاء" in data_type:
                    df = pd.DataFrame({
                        'معرف_العميل': [f'CUST_{i:06d}' for i in range(1, n_records+1)],
                        'العمر': np.random.randint(18, 80, n_records),
                        'المدينة': np.random.choice(['الرياض', 'جدة', 'الدمام'], n_records),
                        'التصنيف': np.random.choice(['VIP', 'نشط', 'جديد'], n_records, p=[0.1, 0.6, 0.3])
                    })
                else:
                    df = pd.DataFrame({
                        'معرف_الموظف': [f'EMP_{i:05d}' for i in range(1, n_records+1)],
                        'القسم': np.random.choice(['IT', 'المبيعات', 'المالية'], n_records),
                        'المرتب': np.random.normal(15000, 5000, n_records).clip(5000).round(2)
                    })
                
                st.session_state.beast_df = df
                st.success(f"✅ تم توليد {len(df):,} سجل!")
                st.dataframe(df.head())
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tabs[2]:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.subheader("📊 محرر Excel")
        
        if st.session_state.excel_data is None:
            st.session_state.excel_data = pd.DataFrame('', index=range(10), columns=[f'عمود_{chr(65+i)}' for i in range(5)])
        
        edited = st.data_editor(st.session_state.excel_data, num_rows="dynamic", height=300)
        st.session_state.excel_data = edited
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 حفظ في النظام", use_container_width=True):
                st.session_state.beast_df = edited.copy()
                st.success("تم الحفظ!")
        with col2:
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                edited.to_excel(writer, index=False)
            st.download_button("📥 تصدير Excel", buffer.getvalue(), "data.xlsx", 
                             "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# ======= القسم 2: Power Query =======
def render_power_query():
    st.markdown(f"<h1 class='main-header'>{txt('power_query_section')}</h1>", unsafe_allow_html=True)
    
    if st.session_state.beast_df is None:
        st.warning("⚠️ ارفع البيانات أولاً")
        return
    
    df = st.session_state.beast_df
    
    # KPIs
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    cols = st.columns(4)
    metrics = [
        ("السجلات", len(df), "#3b82f6"),
        ("الفراغات", f"{df.isnull().sum().sum()/df.size*100:.1f}%", "#ef4444"),
        ("التكرارات", df.duplicated().sum(), "#f59e0b"),
        ("الجودة", f"{max(0, 100-df.isnull().sum().sum()/df.size*100):.0f}%", "#10b981")
    ]
    
    for col, (label, val, color) in zip(cols, metrics):
        with col:
            st.markdown(f"""
            <div style='background: {color}20; border-radius: 12px; padding: 1rem; text-align: center; border: 1px solid {color};'>
                <div style='color: {color}; font-size: 0.9rem;'>{label}</div>
                <div style='color: {color}; font-size: 1.5rem; font-weight: 700;'>{val}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # أدوات التنظيف
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.subheader("🛠️ أدوات التنظيف")
    
    clean_cols = st.columns(4)
    actions = [
        ("🗑️ حذف تكرار", lambda: df.drop_duplicates()),
        ("📝 تعبئة فراغات", lambda: df.fillna(df.median(numeric_only=True))),
        ("✂️ حذف فراغات", lambda: df.dropna()),
        ("🔤 توحيد نص", lambda: df.apply(lambda x: x.str.strip().str.title() if x.dtype == 'object' else x))
    ]
    
    for col, (label, action) in zip(clean_cols, actions):
        with col:
            if st.button(label, use_container_width=True):
                try:
                    new_df = action()
                    st.session_state.beast_df = new_df
                    st.session_state.cleaning_log.append(label)
                    st.success("تم!")
                except Exception as e:
                    st.error(f"خطأ: {e}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ======= القسم 3: Dashboard =======
def render_dashboard():
    st.markdown(f"<h1 class='main-header'>{txt('dashboard_section')}</h1>", unsafe_allow_html=True)
    
    if st.session_state.beast_df is None:
        st.warning("⚠️ ارفع البيانات أولاً")
        return
    
    df = st.session_state.beast_df
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    # فلاتر
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    filt_cols = st.columns([2, 2, 1])
    with filt_cols[0]:
        if categorical_cols:
            filter_val = st.multiselect("فلتر:", df[categorical_cols[0]].unique(), default=list(df[categorical_cols[0]].unique())[:3])
    with filt_cols[1]:
        if numeric_cols:
            metric = st.selectbox("المؤشر:", numeric_cols)
    with filt_cols[2]:
        st.button("🔄 تحديث")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # KPIs
    if numeric_cols:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        kpi_cols = st.columns(4)
        
        total = df[metric].sum()
        avg = df[metric].mean()
        max_val = df[metric].max()
        growth = ((df[metric].iloc[-1] - df[metric].iloc[0]) / abs(df[metric].iloc[0]) * 100) if len(df) > 1 and df[metric].iloc[0] != 0 else 0
        
        kpi_data = [("المجموع", total, "💰"), ("المتوسط", avg, "📊"), ("الأقصى", max_val, "🏆"), ("النمو", f"{growth:+.1f}%", "📈")]
        
        for col, (label, val, icon) in zip(kpi_cols, kpi_data):
            with col:
                st.markdown(f"<div class='kpi-card'><div>{icon} {label}</div><div class='kpi-value'>{val:,.0f}</div></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # رسوم بيانية
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        chart_tabs = st.tabs(["📈 خطي", "🥧 دائري", "📊 أعمدة", "🔥 حراري"])
        
        with chart_tabs[0]:
            fig = px.line(df, y=metric, template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        
        with chart_tabs[1]:
            if categorical_cols:
                pie_data = df.groupby(categorical_cols[0])[metric].sum()
                fig = px.pie(values=pie_data.values, names=pie_data.index, hole=0.5, template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
        
        with chart_tabs[2]:
            fig = px.bar(df.head(20), y=metric, template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        
        with chart_tabs[3]:
            if len(numeric_cols) > 1:
                corr = df[numeric_cols].corr()
                fig = px.imshow(corr, text_auto=True, template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# ======= القسم 4: AI Prediction =======
def render_ai():
    st.markdown(f"<h1 class='main-header'>{txt('ai_section')}</h1>", unsafe_allow_html=True)
    
    if st.session_state.beast_df is None:
        st.warning("⚠️ ارفع البيانات أولاً")
        return
    
    df = st.session_state.beast_df
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if not numeric_cols:
        st.error("❌ لا توجد أعمدة رقمية")
        return
    
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        target = st.selectbox("المؤشر:", numeric_cols)
    with col2:
        periods = st.slider("الفترة:", 7, 365, 30)
    with col3:
        model = st.selectbox("النموذج:", ["Linear", "Polynomial"])
    
    if st.button("🔮 تنبؤ", use_container_width=True):
        with st.spinner("جاري التحليل..."):
            try:
                from sklearn.linear_model import LinearRegression
                from sklearn.preprocessing import PolynomialFeatures
                
                y = df[target].dropna().values
                X = np.arange(len(y)).reshape(-1, 1)
                
                if model == "Polynomial":
                    poly = PolynomialFeatures(degree=2)
                    X = poly.fit_transform(X)
                    model_obj = LinearRegression()
                    model_obj.fit(X, y)
                    future_X = poly.transform(np.arange(len(y), len(y)+periods).reshape(-1, 1))
                else:
                    model_obj = LinearRegression()
                    model_obj.fit(X, y)
                    future_X = np.arange(len(y), len(y)+periods).reshape(-1, 1)
                
                predictions = model_obj.predict(future_X)
                predictions = np.maximum(predictions, 0)  # منع السالب
                
                # حفظ النتائج
                st.session_state.forecast_results = {
                    'target': target,
                    'periods': periods,
                    'predictions': predictions.tolist()
                }
                
                # عرض النتائج
                result_cols = st.columns(4)
                result_cols[0].metric("المتوسط", f"{np.mean(predictions):,.0f}")
                result_cols[1].metric("القمة", f"{np.max(predictions):,.0f}")
                result_cols[2].metric("الحد الأدنى", f"{np.min(predictions):,.0f}")
                result_cols[3].metric("الاتجاه", "📈 صاعد" if predictions[-1] > predictions[0] else "📉 هابط")
                
                # رسم
                fig = go.Figure()
                fig.add_trace(go.Scatter(y=y, name='تاريخي', line=dict(color='#3b82f6')))
                fig.add_trace(go.Scatter(x=list(range(len(y), len(y)+periods)), y=predictions, 
                                       name='تنبؤ', line=dict(color='#10b981', dash='dash')))
                fig.update_layout(template="plotly_dark", title=f"تنبؤ {target}")
                st.plotly_chart(fig, use_container_width=True)
                
                # جدول
                forecast_df = pd.DataFrame({
                    'اليوم': range(1, periods+1),
                    'التنبؤ': predictions.round(2)
                })
                st.dataframe(forecast_df, use_container_width=True)
                
                # توصيات
                st.subheader("💡 التوصيات")
                if predictions[-1] > predictions[0]:
                    st.markdown("<div class='recommendation-item'>📈 اتجاه إيجابي - زود المخزون</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='recommendation-item'>📉 اتجاه سلبي - راجع التكاليف</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ خطأ: {e}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ======= القسم 5: Report =======
def render_report():
    st.markdown(f"<h1 class='main-header'>{txt('report_section')}</h1>", unsafe_allow_html=True)
    
    if st.session_state.beast_df is None:
        st.warning("⚠️ ارفع البيانات أولاً")
        return
    
    df = st.session_state.beast_df
    
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    
    # إعدادات
    col1, col2 = st.columns(2)
    with col1:
        report_lang = st.selectbox("اللغة:", ["العربية 🇸🇦", "English 🇬🇧"])
    with col2:
        st.selectbox("النمط:", ["احترافي أخضر", "أزرق تقني"])
    
    # معاينة
    st.subheader("👁️ معاينة")
    st.markdown(f"""
    <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #059669, #10b981); 
                border-radius: 15px; color: white;'>
        <h2>🦁 {APP_NAME}</h2>
        <p>التاريخ: {datetime.now().strftime('%Y/%m/%d')}</p>
        <p>السجلات: {len(df):,} | الأعمدة: {len(df.columns)}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # تصدير
    export_cols = st.columns(2)
    
    with export_cols[0]:
        if st.button("📄 PDF", use_container_width=True):
            try:
                from reportlab.lib.pagesizes import A4
                from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer
                from reportlab.lib.styles import getSampleStyleSheet
                from reportlab.lib import colors
                
                buffer = BytesIO()
                doc = SimpleDocTemplate(buffer, pagesize=A4)
                elements = []
                styles = getSampleStyleSheet()
                
                # عنوان
                elements.append(Paragraph(APP_NAME, styles['Title']))
                elements.append(Spacer(1, 20))
                elements.append(Paragraph(f"التاريخ: {datetime.now().strftime('%Y/%m/%d')}", styles['Normal']))
                elements.append(Spacer(1, 20))
                
                # جدول
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                if numeric_cols:
                    data = [['المؤشر', 'المجموع', 'المتوسط']]
                    for col in numeric_cols[:5]:
                        data.append([col, f"{df[col].sum():,.0f}", f"{df[col].mean():,.0f}"])
                    
                    table = Table(data)
                    table.setStyle([
                        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#059669')),
                        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                    ])
                    elements.append(table)
                
                doc.build(elements)
                buffer.seek(0)
                
                st.download_button("⬇️ تحميل PDF", buffer.getvalue(), 
                                 f"{APP_NAME.replace(' ', '_')}_Report.pdf", "application/pdf",
                                 use_container_width=True)
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ خطأ: {e}")
    
    with export_cols[1]:
        # واتساب
        msg = f"🦁 {APP_NAME}%0A📅 {datetime.now().strftime('%Y/%m/%d')}%0A📊 {len(df):,} سجل"
        whatsapp_url = f"https://wa.me/?text={msg}"
        st.markdown(f"<a href='{whatsapp_url}' target='_blank'><button style='width:100%; padding:0.5rem; background:#25d366; color:white; border:none; border-radius:8px;'>📱 واتساب</button></a>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ======= التشغيل الرئيسي =======
if selected_section == txt('upload_section'):
    render_upload()
elif selected_section == txt('power_query_section'):
    render_power_query()
elif selected_section == txt('dashboard_section'):
    render_dashboard()
elif selected_section == txt('ai_section'):
    render_ai()
elif selected_section == txt('report_section'):
    render_report()

# ======= Footer =======
st.markdown(f"""
<div style='text-align: center; padding: 2rem; margin-top: 3rem; border-top: 1px solid #1e293b; color: #64748b;'>
    <div style='font-size: 2rem;'>🦁</div>
    <h3 style='color: #10b981;'>{APP_NAME}</h3>
    <p>© 2026 | {AUTHOR_SIGNATURE} | All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)
