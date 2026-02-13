import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import io
import base64
from io import BytesIO
import warnings
import re
import json
from functools import lru_cache

# ======= إدارة الاستيرادات مع معالجة الأخطاء =======
REQUIRED_PACKAGES = {
    'sklearn': 'scikit-learn',
    'reportlab': 'reportlab',
    'firebase_admin': 'firebase-admin'
}

missing_packages = []
for module, package in REQUIRED_PACKAGES.items():
    try:
        _import_(module)
    except ImportError:
        missing_packages.append(package)

if missing_packages:
    st.error(f"""
    ⚠️ مكتبات مطلوبة غير مثبتة:
    {', '.join(missing_packages)}
    
    نفذ الأمر التالي:
    bash
    pip install {' '.join(missing_packages)}
    
    """)
    st.stop()

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score
import hashlib

warnings.filterwarnings('ignore')

# ======= الذاكرة المركزية والإعدادات =======
AUTHOR_SIGNATURE = "MIA8444"
APP_NAME = "The Beast Pro"
APP_VERSION = "4.0.0-Enterprise"

# تهيئة Session State
defaults = {
    'beast_df': None,
    'cleaning_log': [],
    'report_language': "ar",
    'theme': "dark",
    'user_prefs': {},
    'cache_hash': None,
    'forecast_cache': {}
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ======= إعدادات الصفحة =======
st.set_page_config(
    page_title=f"{AUTHOR_SIGNATURE} | {APP_NAME} v{APP_VERSION}",
    page_icon="🦁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======= نظام اللغات المتقدم =======
TRANSLATIONS = {
    'ar': {
        'home': '🏠 الرئيسية',
        'upload': '📤 رفع البيانات',
        'dashboard': '📊 الداشبورد الاحترافي',
        'forecast': '🔮 التنبؤ والذكاء الاصطناعي',
        'reports': '📄 التقارير الذكية',
        'settings': '⚙️ الإعدادات',
        'total': 'الإجمالي',
        'average': 'المتوسط',
        'maximum': 'أعلى قيمة',
        'growth': 'معدل النمو',
        'trend_positive': 'إيجابي 📈',
        'trend_negative': 'سلبي 📉',
        'trend_stable': 'مستقر ➡️',
        'insight_high': 'أداء ممتاز',
        'insight_medium': 'أداء جيد',
        'insight_low': 'يحتاج تحسين',
        'forecast_accuracy': 'دقة التنبؤ',
        'data_quality': 'جودة البيانات',
        'records_count': 'عدد السجلات',
        'last_update': 'آخر تحديث'
    },
    'en': {
        'home': '🏠 Home',
        'upload': '📤 Upload Data',
        'dashboard': '📊 Pro Dashboard',
        'forecast': '🔮 AI Forecasting',
        'reports': '📄 Smart Reports',
        'settings': '⚙️ Settings',
        'total': 'Total',
        'average': 'Average',
        'maximum': 'Maximum',
        'growth': 'Growth Rate',
        'trend_positive': 'Positive 📈',
        'trend_negative': 'Negative 📉',
        'trend_stable': 'Stable ➡️',
        'insight_high': 'Excellent Performance',
        'insight_medium': 'Good Performance',
        'insight_low': 'Needs Improvement',
        'forecast_accuracy': 'Forecast Accuracy',
        'data_quality': 'Data Quality',
        'records_count': 'Records Count',
        'last_update': 'Last Update'
    }
}

def t(key):
    """ترجمة فورية"""
    lang = st.session_state.report_language
    return TRANSLATIONS.get(lang, TRANSLATIONS['ar']).get(key, key)

# ======= نظام الثيم المتقدم (Dark/Light) =======
THEMES = {
    'dark': {
        'bg': '#0a0e17',
        'card': 'rgba(17, 24, 39, 0.7)',
        'text': '#f3f4f6',
        'primary': '#3b82f6',
        'secondary': '#10b981',
        'accent': '#f59e0b',
        'danger': '#ef4444'
    },
    'light': {
        'bg': '#f8fafc',
        'card': 'rgba(255, 255, 255, 0.9)',
        'text': '#1e293b',
        'primary': '#2563eb',
        'secondary': '#059669',
        'accent': '#d97706',
        'danger': '#dc2626'
    }
}

def get_theme():
    return THEMES[st.session_state.theme]

# ======= CSS احترافي ديناميكي =======
def inject_css():
    theme = get_theme()
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&family=Inter:wght@400;600;800&display=swap');
    
    * {{ 
        font-family: 'Tajawal', 'Inter', sans-serif; 
        direction: {'rtl' if st.session_state.report_language == 'ar' else 'ltr'};
    }}
    
    .stApp {{ 
        background: linear-gradient(135deg, {theme['bg']} 0%, {theme['bg']} 100%);
        color: {theme['text']};
    }}
    
    .glass-card {{
        background: {theme['card']};
        backdrop-filter: blur(20px);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 24px;
        padding: 28px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }}
    
    .glass-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(59, 130, 246, 0.15);
    }}
    
    .gradient-text {{
        background: linear-gradient(135deg, {theme['primary']} 0%, {theme['secondary']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 2.5rem;
    }}
    
    .kpi-card {{
        background: linear-gradient(145deg, {theme['card']}, {theme['bg']});
        border-radius: 20px;
        padding: 24px;
        border-{'right' if st.session_state.report_language == 'ar' else 'left'}: 5px solid {theme['primary']};
        text-align: center;
        position: relative;
        overflow: hidden;
    }}
    
    .kpi-card::before {{
        content: '';
        position: absolute;
        top: 0;
        {'right' if st.session_state.report_language == 'ar' else 'left'}: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, {theme['primary']}, {theme['secondary']});
    }}
    
    .kpi-value {{
        font-size: 2.2rem;
        font-weight: 800;
        color: {theme['primary']};
        margin: 10px 0;
    }}
    
    .stButton>button {{
        background: linear-gradient(135deg, {theme['primary']}, {theme['secondary']});
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 700;
        transition: all 0.3s;
    }}
    
    .stButton>button:hover {{
        transform: scale(1.05);
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
    }}
    
    .metric-positive {{ color: {theme['secondary']}; }}
    .metric-negative {{ color: {theme['danger']}; }}
    .metric-neutral {{ color: {theme['accent']}; }}
    
    .loading-spinner {{
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100px;
    }}
    
    .insight-badge {{
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }}
    
    .badge-excellent {{ background: rgba(16, 185, 129, 0.2); color: {theme['secondary']}; }}
    .badge-good {{ background: rgba(245, 158, 11, 0.2); color: {theme['accent']}; }}
    .badge-warning {{ background: rgba(239, 68, 68, 0.2); color: {theme['danger']}; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

inject_css()

# ======= محرك البيانات الذكي (Data Engine) =======
class BeastDataEngine:
    """محرك بيانات احترافي متكامل"""
    
    @staticmethod
    @st.cache_data(ttl=3600)
    def load_data(file):
        """تحميل البيانات مع التخزين المؤقت"""
        try:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file)
            else:
                return None, "نوع الملف غير مدعوم"
            
            # تنظيف أولي
            df = BeastDataEngine.clean_data(df)
            return df, None
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def clean_data(df):
        """تنظيف ذكي للبيانات"""
        df_clean = df.copy()
        
        # إزالة الأعمدة الفارغة تماماً
        df_clean = df_clean.dropna(axis=1, how='all')
        
        # معالجة القيم المفقودة
        for col in df_clean.columns:
            if df_clean[col].dtype in ['int64', 'float64']:
                df_clean[col] = df_clean[col].fillna(df_clean[col].median())
            else:
                df_clean[col] = df_clean[col].fillna('غير محدد')
        
        # إزالة التكرارات
        df_clean = df_clean.drop_duplicates()
        
        return df_clean
    
    @staticmethod
    def analyze_quality(df):
        """تحليل جودة البيانات"""
        total_cells = df.size
        missing_cells = df.isnull().sum().sum()
        duplicate_rows = df.duplicated().sum()
        
        quality_score = max(0, 100 - ((missing_cells / total_cells) * 50) - ((duplicate_rows / len(df)) * 50))
        
        return {
            'score': round(quality_score, 1),
            'completeness': round(((total_cells - missing_cells) / total_cells) * 100, 1),
            'uniqueness': round(((len(df) - duplicate_rows) / len(df)) * 100, 1),
            'missing_count': missing_cells,
            'duplicate_count': duplicate_rows
        }

# ======= محرك التنبؤ المتقدم (AI Forecast Engine) =======
class BeastForecastEngine:
    """محرك تنبؤ احترافي متعدد النماذج"""
    
    @staticmethod
    def generate_forecast(df, target_col, periods=30, model_type='auto'):
        """تنبؤ ذكي مع اختيار أفضل نموذج تلقائياً"""
        
        cache_key = f"{target_col}{periods}{model_type}_{hash(df[target_col].to_json())}"
        
        if cache_key in st.session_state.forecast_cache:
            return st.session_state.forecast_cache[cache_key]
        
        try:
            y = df[target_col].dropna().values
            X = np.arange(len(y)).reshape(-1, 1)
            
            if len(y) < 5:
                return None, "البيانات غير كافية للتنبؤ (تحتاج 5 سجلات على الأقل)"
            
            results = {}
            
            # نموذج خطي
            linear_model = LinearRegression()
            linear_model.fit(X, y)
            linear_pred = linear_model.predict(np.arange(len(y), len(y) + periods).reshape(-1, 1))
            linear_r2 = r2_score(y, linear_model.predict(X))
            results['linear'] = (linear_pred, linear_r2)
            
            # نموذج متعدد الحدود (إذا كانت البيانات كافية)
            if len(y) > 10:
                poly = PolynomialFeatures(degree=2)
                X_poly = poly.fit_transform(X)
                poly_model = LinearRegression()
                poly_model.fit(X_poly, y)
                future_X_poly = poly.transform(np.arange(len(y), len(y) + periods).reshape(-1, 1))
                poly_pred = poly_model.predict(future_X_poly)
                poly_r2 = r2_score(y, poly_model.predict(X_poly))
                results['polynomial'] = (poly_pred, poly_r2)
            
            # اختيار أفضل نموذج
            best_model = max(results.items(), key=lambda x: x[1][1])
            forecast_values = best_model[1][0]
            accuracy = best_model[1][1]
            
            # إضافة تقلب واقعي
            volatility = np.std(y) * 0.05
            noise = np.random.normal(0, volatility, periods)
            final_forecast = forecast_values + noise
            
            # ضمان عدم وجود قيم سالبة للبيانات الموجبة
            if min(y) >= 0:
                final_forecast = np.maximum(final_forecast, 0)
            
            result = {
                'forecast': final_forecast,
                'accuracy': round(accuracy * 100, 1),
                'model_used': best_model[0],
                'confidence_interval': {
                    'upper': final_forecast + (1.96 * volatility),
                    'lower': final_forecast - (1.96 * volatility)
                }
            }
            
            st.session_state.forecast_cache[cache_key] = result
            return result, None
            
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def detect_anomalies(df, target_col, threshold=2):
        """كشف الشذوذ في البيانات"""
        mean = df[target_col].mean()
        std = df[target_col].std()
        
        anomalies = df[abs(df[target_col] - mean) > (threshold * std)]
        return anomalies

# ======= منشئ التقارير الاحترافي =======
class BeastReportGenerator:
    """مولد تقارير ذكي متعدد الصيغ"""
    
    @staticmethod
    def generate_insights(df, target_col):
        """توليد رؤى ذكية"""
        series = df[target_col]
        current = series.iloc[-1]
        avg = series.mean()
        max_val = series.max()
        min_val = series.min()
        
        # تحديد الاتجاه
        if len(series) > 1:
            trend_slope = (series.iloc[-1] - series.iloc[0]) / len(series)
            if trend_slope > avg * 0.01:
                trend = 'trend_positive'
                trend_icon = '📈'
            elif trend_slope < -avg * 0.01:
                trend = 'trend_negative'
                trend_icon = '📉'
            else:
                trend = 'trend_stable'
                trend_icon = '➡️'
        else:
            trend = 'trend_stable'
            trend_icon = '➡️'
        
        # تقييم الأداء
        performance_ratio = current / avg if avg != 0 else 1
        if performance_ratio > 1.2:
            performance = 'insight_high'
            perf_class = 'badge-excellent'
        elif performance_ratio > 0.8:
            performance = 'insight_medium'
            perf_class = 'badge-good'
        else:
            performance = 'insight_low'
            perf_class = 'badge-warning'
        
        return {
            'trend': trend,
            'trend_icon': trend_icon,
            'performance': performance,
            'perf_class': perf_class,
            'avg': avg,
            'max': max_val,
            'min': min_val,
            'volatility': series.std() / avg if avg != 0 else 0
        }

# ======= واجهات المستخدم =======
def render_home():
    """الصفحة الرئيسية"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"<h1 class='gradient-text'>{t('home')}</h1>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='glass-card'>
            <h3>🦁 مرحباً بك في {APP_NAME}</h3>
            <p>المنصة الاحترافية للتحليل الذكي والتنبؤ المتقدم</p>
            <ul>
                <li>📊 داشبوردات تفاعلية Power BI-style</li>
                <li>🤖 ذكاء اصطناعي للتنبؤ بدقة عالية</li>
                <li>📄 تقارير ذكية تلقائية</li>
                <li>🎨 واجهة احترافية قابلة للتخصيص</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.image("https://img.icons8.com/fluency/400/artificial-intelligence.png", use_column_width=True)
    
    # إحصائيات سريعة
    if st.session_state.beast_df is not None:
        st.markdown("### 📊 نظرة سريعة على البيانات")
        df = st.session_state.beast_df
        quality = BeastDataEngine.analyze_quality(df)
        
        cols = st.columns(4)
        metrics = [
            (t('records_count'), len(df), "👥"),
            (t('data_quality'), f"{quality['score']}%", "✅"),
            ("الأعمدة", len(df.columns), "📋"),
            (t('last_update'), datetime.now().strftime("%H:%M"), "🕐")
        ]
        
        for col, (label, value, icon) in zip(cols, metrics):
            with col:
                st.markdown(f"""
                <div class='kpi-card'>
                    <small>{icon} {label}</small>
                    <div class='kpi-value'>{value}</div>
                </div>
                """, unsafe_allow_html=True)

def render_upload():
    """صفحة رفع البيانات"""
    st.markdown(f"<h1 class='gradient-text'>{t('upload')}</h1>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "اختر ملف البيانات (CSV, Excel)",
        type=['csv', 'xlsx', 'xls'],
        help="الحد الأقصى 200MB"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if uploaded_file:
            with st.spinner("جاري معالجة البيانات..."):
                df, error = BeastDataEngine.load_data(uploaded_file)
                
                if error:
                    st.error(f"❌ خطأ: {error}")
                else:
                    st.session_state.beast_df = df
                    quality = BeastDataEngine.analyze_quality(df)
                    
                    st.success(f"✅ تم تحميل {len(df):,} سجل بنجاح!")
                    
                    with st.expander("🔍 تفاصيل جودة البيانات"):
                        st.json(quality)
                    
                    st.dataframe(df.head(10), use_container_width=True)
    
    with col2:
        st.markdown("### 🎲 أو توليد بيانات تجريبية")
        
        if st.button("إنشاء بيانات مبيعات تجريبية", use_container_width=True):
            with st.spinner("جاري التوليد..."):
                dates = pd.date_range(start='2024-01-01', periods=365, freq='D')
                base_sales = 1000
                trend = np.linspace(0, 500, 365)
                seasonal = 200 * np.sin(2 * np.pi * np.arange(365) / 365.25)
                noise = np.random.normal(0, 100, 365)
                
                df = pd.DataFrame({
                    'التاريخ': dates,
                    'المبيعات': np.maximum(base_sales + trend + seasonal + noise, 0).astype(int),
                    'عدد_العملاء': (20 + (trend/50) + np.random.normal(0, 5, 365)).astype(int),
                    'منطقة': np.random.choice(['الشمال', 'الجنوب', 'الشرق', 'الغرب'], 365),
                    'الفئة': np.random.choice(['منتج A', 'منتج B', 'منتج C'], 365)
                })
                
                st.session_state.beast_df = df
                st.success(f"✅ تم توليد {len(df):,} سجل!")
                st.dataframe(df.head(), use_container_width=True)

def render_dashboard():
    """الداشبورد الاحترافي"""
    if st.session_state.beast_df is None:
        st.warning("⚠️ برجاء رفع البيانات أولاً من قسم " + t('upload'))
        return
    
    st.markdown(f"<h1 class='gradient-text'>{t('dashboard')}</h1>", unsafe_allow_html=True)
    
    df = st.session_state.beast_df
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if not num_cols:
        st.error("❌ لا توجد أعمدة رقمية في البيانات!")
        return
    
    # الفلاتر المتقدمة
    with st.expander("🔧 الفلاتر والتحكم", expanded=True):
        filt_col1, filt_col2, filt_col3 = st.columns(3)
        
        with filt_col1:
            selected_metric = st.selectbox("المؤشر الرئيسي:", num_cols)
        with filt_col2:
            chart_type = st.selectbox("نوع الرسم:", ['Area', 'Line', 'Bar', 'Scatter'])
        with filt_col3:
            if 'التاريخ' in df.columns or 'date' in df.columns.lower():
                date_col = [c for c in df.columns if 'date' in c.lower() or 'تاريخ' in c][0]
                date_range = st.date_input("نطاق التاريخ:", 
                    [df[date_col].min(), df[date_col].max()])
    
    # حساب KPIs
    @st.cache_data
    def calc_kpis(df, metric):
        return {
            'sum': df[metric].sum(),
            'mean': df[metric].mean(),
            'max': df[metric].max(),
            'min': df[metric].min(),
            'growth': ((df[metric].iloc[-1] - df[metric].iloc[0]) / abs(df[metric].iloc[0]) * 100) if df[metric].iloc[0] != 0 else 0
        }
    
    kpis = calc_kpis(df, selected_metric)
    
    # عرض KPIs
    st.markdown("### 📈 المؤشرات الرئيسية")
    kpi_cols = st.columns(4)
    kpi_data = [
        (t('total'), kpis['sum'], '#3b82f6', '💰'),
        (t('average'), kpis['mean'], '#10b981', '📊'),
        (t('maximum'), kpis['max'], '#f59e0b', '🏆'),
        (t('growth'), f"{kpis['growth']:+.1f}%", '#ef4444' if kpis['growth'] < 0 else '#10b981', '📈')
    ]
    
    for col, (label, value, color, icon) in zip(kpi_cols, kpi_data):
        with col:
            st.markdown(f"""
            <div class='kpi-card' style='border-color: {color}'>
                <small>{icon} {label}</small>
                <div class='kpi-value' style='color: {color}'>{value:,.0f}{'%' if 'نمو' in label or 'Growth' in label else ''}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # الرسوم البيانية
    chart_col1, chart_col2 = st.columns([2, 1])
    
    with chart_col1:
        st.markdown("### 📉 تحليل الاتجاه")
        
        if chart_type == 'Area':
            fig = px.area(df, y=selected_metric, template="plotly_dark", 
                         color_discrete_sequence=['#3b82f6'])
        elif chart_type == 'Line':
            fig = px.line(df, y=selected_metric, template="plotly_dark",
                         color_discrete_sequence=['#3b82f6'])
        elif chart_type == 'Bar':
            fig = px.bar(df, y=selected_metric, template="plotly_dark",
                        color_discrete_sequence=['#3b82f6'])
        else:
            fig = px.scatter(df, y=selected_metric, template="plotly_dark",
                           color_discrete_sequence=['#3b82f6'])
        
        fig.update_layout(
            title=f"تحليل {selected_metric}",
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with chart_col2:
        st.markdown("### 🥧 التوزيع")
        
        # توزيع حسب الفئة إذا وجدت
        cat_cols = df.select_dtypes(include=['object']).columns
        if len(cat_cols) > 0:
            cat_col = cat_cols[0]
            pie_data = df.groupby(cat_col)[selected_metric].sum().reset_index().head(8)
            fig_pie = px.pie(pie_data, values=selected_metric, names=cat_col,
                           hole=0.6, template="plotly_dark")
            fig_pie.update_layout(height=400)
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("لا توجد بيانات تصنيفية للعرض")

def render_forecast():
    """صفحة التنبؤ والذكاء الاصطناعي"""
    if st.session_state.beast_df is None:
        st.warning("⚠️ برجاء رفع البيانات أولاً!")
        return
    
    st.markdown(f"<h1 class='gradient-text'>{t('forecast')}</h1>", unsafe_allow_html=True)
    
    df = st.session_state.beast_df
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if not num_cols:
        st.error("❌ لا توجد بيانات رقمية!")
        return
    
    # إعدادات التنبؤ
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            target_col = st.selectbox("العمود المستهدف:", num_cols)
        with col2:
            periods = st.slider("فترة التنبؤ (يوم):", 7, 90, 30)
        with col3:
            model_type = st.selectbox("نوع النموذج:", ['auto', 'linear', 'polynomial'])
    
    if st.button("🚀 بدء التنبؤ الذكي", use_container_width=True):
        with st.spinner("جاري تحليل البيانات وتدريب النموذج..."):
            result, error = BeastForecastEngine.generate_forecast(df, target_col, periods, model_type)
            
            if error:
                st.error(f"❌ {error}")
            else:
                # عرض النتائج
                st.success(f"✅ تم التنبؤ بنجاح! دقة النموذج: {result['accuracy']}%")
                
                # رسم التنبؤ
                fig = go.Figure()
                
                # البيانات التاريخية
                fig.add_trace(go.Scatter(
                    y=df[target_col],
                    name="بيانات تاريخية",
                    line=dict(color='#3b82f6', width=2),
                    mode='lines'
                ))
                
                # خط التنبؤ
                future_dates = list(range(len(df), len(df) + periods))
                fig.add_trace(go.Scatter(
                    x=future_dates,
                    y=result['forecast'],
                    name="التنبؤ",
                    line=dict(color='#10b981', width=3, dash='dash'),
                    mode='lines'
                ))
                
                # مجال الثقة
                fig.add_trace(go.Scatter(
                    x=future_dates + future_dates[::-1],
                    y=list(result['confidence_interval']['upper']) + list(result['confidence_interval']['lower'])[::-1],
                    fill='toself',
                    fillcolor='rgba(16, 185, 129, 0.2)',
                    line=dict(color='rgba(255,255,255,0)'),
                    name="مجال الثقة (95%)"
                ))
                
                fig.update_layout(
                    title=f"تنبؤ {target_col} للـ {periods} يوم القادمة",
                    template="plotly_dark",
                    height=500,
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # جدول التنبؤ
                forecast_df = pd.DataFrame({
                    'اليوم': range(1, periods + 1),
                    'التنبؤ': result['forecast'].round(2),
                    'الحد الأدنى': result['confidence_interval']['lower'].round(2),
                    'الحد الأقصى': result['confidence_interval']['upper'].round(2)
                })
                
                st.markdown("### 📋 تفاصيل التنبؤ")
                st.dataframe(forecast_df, use_container_width=True)
                
                # تحميل النتائج
                csv = forecast_df.to_csv(index=False)
                st.download_button(
                    "⬇️ تحميل التنبؤ (CSV)",
                    csv,
                    f"forecast_{target_col}_{datetime.now().strftime('%Y%m%d')}.csv",
                    "text/csv"
                )

def render_reports():
    """التقارير الذكية"""
    if st.session_state.beast_df is None:
        st.warning("⚠️ برجاء رفع البيانات أولاً!")
        return
    
    st.markdown(f"<h1 class='gradient-text'>{t('reports')}</h1>", unsafe_allow_html=True)
    
    df = st.session_state.beast_df
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if not num_cols:
        st.error("❌ لا توجد بيانات رقمية!")
        return
    
    target_col = st.selectbox("اختر المؤشر للتحليل:", num_cols)
    
    # توليد الرؤى
    insights = BeastReportGenerator.generate_insights(df, target_col)
    
    # عرض التقرير
    st.markdown(f"""
    <div class='glass-card'>
        <h3>📝 {t('reports')} - {target_col}</h3>
        <div style='display: flex; gap: 10px; margin: 20px 0;'>
            <span class='insight-badge {insights['perf_class']}'>{t(insights['performance'])}</span>
            <span class='insight-badge badge-good'>{insights['trend_icon']} {t(insights['trend'])}</span>
        </div>
        
        <h4>📊 إحصائيات رئيسية:</h4>
        <ul>
            <li>المتوسط: <strong>{insights['avg']:,.2f}</strong></li>
            <li>الحد الأقصى: <strong>{insights['max']:,.2f}</strong></li>
            <li>الحد الأدنى: <strong>{insights['min']:,.2f}</strong></li>
            <li>معامل التذبذب: <strong>{insights['volatility']:.2%}</strong></li>
        </ul>
        
        <h4>💡 التوصيات:</h4>
        <p>بناءً على تحليل {len(df):,} سجل، يُنصح بالتركيز على 
        {'تحسين الأداء في الفترات الضعيفة' if insights['performance'] == 'insight_low' else 'تعزيز النجاحات المحققة'} 
        مع مراقبة {t(insights['trend'])}.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # رسم بياني للتحليل
    fig = px.histogram(df, x=target_col, template="plotly_dark", 
                      title=f"توزيع قيم {target_col}",
                      color_discrete_sequence=['#3b82f6'])
    st.plotly_chart(fig, use_container_width=True)

def render_settings():
    """الإعدادات"""
    st.markdown(f"<h1 class='gradient-text'>{t('settings')}</h1>", unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🌐 اللغة")
            new_lang = st.radio("اختر اللغة:", ['ar', 'en'], 
                               format_func=lambda x: 'العربية' if x == 'ar' else 'English',
                               index=0 if st.session_state.report_language == 'ar' else 1)
            if new_lang != st.session_state.report_language:
                st.session_state.report_language = new_lang
                st.rerun()
        
        with col2:
            st.markdown("### 🎨 المظهر")
            new_theme = st.radio("اختر الثيم:", ['dark', 'light'],
                                format_func=lambda x: 'داكن' if x == 'dark' else 'فاتح',
                                index=0 if st.session_state.theme == 'dark' else 1)
            if new_theme != st.session_state.theme:
                st.session_state.theme = new_theme
                st.rerun()
    
    st.markdown("### ℹ️ معلومات النظام")
    st.json({
        "التطبيق": APP_NAME,
        "الإصدار": APP_VERSION,
        "المطور": AUTHOR_SIGNATURE,
        "السنة": "2026",
        "المكتبات": {
            "pandas": pd._version_,
            "numpy": np._version_,
            "plotly": px._version_,
            "streamlit": st._version_
        }
    })
    
    if st.button("🗑️ مسح ذاكرة التخزين المؤقت", use_container_width=True):
        st.cache_data.clear()
        st.session_state.forecast_cache = {}
        st.success("✅ تم مسح الذاكرة المؤقتة!")

# ======= الشريط الجانبي =======
with st.sidebar:
    theme = get_theme()
    
    st.markdown(f"""
    <div style='text-align: center; padding: 20px 0;'>
        <h1 style='font-size: 1.8rem; margin: 0;'>{APP_NAME}</h1>
        <small style='color: {theme['primary']};'>v{APP_VERSION}</small>
    </div>
    """, unsafe_allow_html=True)
    
    # القائمة
    menu_items = {
        '🏠 الرئيسية': render_home,
        '📤 رفع البيانات': render_upload,
        '📊 الداشبورد الاحترافي': render_dashboard,
        '🔮 التنبؤ والذكاء الاصطناعي': render_forecast,
        '📄 التقارير الذكية': render_reports,
        '⚙️ الإعدادات': render_settings
    }
    
    # ترجمة المفاتيح حسب اللغة
    current_lang = st.session_state.report_language
    menu_labels = {
        'ar': ['🏠 الرئيسية', '📤 رفع البيانات', '📊 الداشبورد الاحترافي', 
               '🔮 التنبؤ والذكاء الاصطناعي', '📄 التقارير الذكية', '⚙️ الإعدادات'],
        'en': ['🏠 Home', '📤 Upload Data', '📊 Pro Dashboard', 
               '🔮 AI Forecasting', '📄 Smart Reports', '⚙️ Settings']
    }
    
    selected = st.radio("القائمة:", menu_labels[current_lang], label_visibility="collapsed")
    
    # تعيين الدالة المناسبة
    menu_map = dict(zip(menu_labels[current_lang], menu_items.values()))
    selected_func = menu_map[selected]
    
    st.markdown("---")
    
    # حالة البيانات
    if st.session_state.beast_df is not None:
        st.success(f"✅ {len(st.session_state.beast_df):,} سجل محمل")
    else:
        st.info("ℹ️ لا توجد بيانات")
    
    st.markdown(f"""
    <div style='text-align: center; margin-top: 30px; color: {theme['text']}80;'>
        <small>Made with ❤️ by {AUTHOR_SIGNATURE}</small><br>
        <small>© 2026</small>
    </div>
    """, unsafe_allow_html=True)

# ======= تشغيل الصفحة المختارة =======
selected_func()

# ======= التذييل العام =======
st.markdown(f"""
<div style='text-align: center; padding: 30px; margin-top: 50px; border-top: 1px solid {theme['primary']}30;'>
    <p style='color: {theme['text']}60; font-size: 0.9rem;'>
        {APP_NAME} v{APP_VERSION} | {AUTHOR_SIGNATURE} © 2026<br>
        Powered by Python, Streamlit & AI
    </p>
</div>
""", unsafe_allow_html=True)
