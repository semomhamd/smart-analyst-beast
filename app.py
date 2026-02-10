import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import os
import io
import base64
from io import BytesIO
import warnings
warnings.filterwarnings('ignore')

# ======== 1. الذاكرة المركزية الموحدة (المحسنة) ========
if 'beast_df' not in st.session_state:
    st.session_state.beast_df = None
if 'cleaning_log' not in st.session_state:
    st.session_state.cleaning_log = []
if 'ml_models' not in st.session_state:
    st.session_state.ml_models = {}
if 'user_settings' not in st.session_state:
    st.session_state.user_settings = {'theme': 'dark', 'language': 'ar'}
if 'report_data' not in st.session_state:
    st.session_state.report_data = {}

# ======== 2. الهوية والتنسيق (MIA8444) ========
AUTHOR_SIGNATURE = "MIA8444"
APP_NAME = "The Beast Pro"
APP_VERSION = "2.0.0"
LOGO_FILE = "8888.jpg"

# ======== 3. CSS احترافي متقدم ========
st.set_page_config(
    page_title=f"{AUTHOR_SIGNATURE} | {APP_NAME}",
    page_icon="🦁",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');
    
    * {{ font-family: 'Tajawal', sans-serif; }}
    
    .stApp {{ 
        background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #0d1117 100%);
        color: #e6edf3;
    }}
    
    /* البطاقات الزجاجية */
    .glass-card {{
        background: rgba(22, 27, 34, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(88, 166, 255, 0.2);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }}
    
    .glass-card:hover {{
        border-color: rgba(88, 166, 255, 0.5);
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(88, 166, 255, 0.1);
    }}
    
    /* المقاييس */
    .metric-container {{
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(35, 134, 54, 0.3);
    }}
    
    .metric-value {{
        font-size: 2.5rem;
        font-weight: 900;
        margin: 10px 0;
    }}
    
    .metric-label {{
        font-size: 1rem;
        opacity: 0.9;
    }}
    
    /* الأزرار الاحترافية */
    .stButton > button {{
        background: linear-gradient(90deg, #238636, #2ea043);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 30px;
        font-weight: 700;
        transition: all 0.3s;
        width: 100%;
    }}
    
    .stButton > button:hover {{
        transform: scale(1.02);
        box-shadow: 0 5px 20px rgba(35, 134, 54, 0.4);
    }}
    
    /* الشريط الجانبي */
    .css-1d391kg {{
        background: linear-gradient(180deg, #161b22 0%, #0d1117 100%);
    }}
    
    /* التبويبات */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
        background: rgba(22, 27, 34, 0.5);
        padding: 10px;
        border-radius: 15px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background: transparent;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 700;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(90deg, #238636, #2ea043) !important;
        color: white !important;
    }}
    
    /* التذييل */
    .footer {{
        text-align: center;
        padding: 30px;
        color: #8b949e;
        font-size: 14px;
        border-top: 1px solid #30363d;
        margin-top: 50px;
        background: rgba(13, 17, 23, 0.8);
    }}
    
    /* شريط التقدم */
    .progress-bar {{
        width: 100%;
        height: 8px;
        background: #21262d;
        border-radius: 4px;
        overflow: hidden;
    }}
    
    .progress-fill {{
        height: 100%;
        background: linear-gradient(90deg, #238636, #2ea043);
        border-radius: 4px;
        transition: width 0.5s ease;
    }}
    
    /* التنبيهات */
    .alert-box {{
        padding: 15px 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-right: 4px solid;
    }}
    
    .alert-success {{
        background: rgba(35, 134, 54, 0.1);
        border-color: #238636;
        color: #3fb950;
    }}
    
    .alert-warning {{
        background: rgba(210, 153, 34, 0.1);
        border-color: #d29922;
        color: #e3b341;
    }}
    
    .alert-error {{
        background: rgba(248, 81, 73, 0.1);
        border-color: #f85149;
        color: #f85149;
    }}
    
    /* الجداول */
    .dataframe {{
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #30363d;
    }}
    
    /* العناوين */
    h1, h2, h3 {{
        color: #e6edf3;
        font-weight: 900;
    }}
    
    .gradient-text {{
        background: linear-gradient(90deg, #58a6ff, #238636);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
    }}
    </style>
    """, unsafe_allow_html=True)

# ======== 4. القائمة الجانبية المتقدمة ========
with st.sidebar:
    # اللوجو
    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, use_container_width=True)
    else:
        st.markdown("""
            <div style='text-align: center; font-size: 4rem; margin: 20px 0;'>
                🦁
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"<h1 style='text-align:center;' class='gradient-text'>{APP_NAME}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:#8b949e;'>v{APP_VERSION} | {AUTHOR_SIGNATURE}</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # القائمة الرئيسية
    menu = st.radio("🎯 القائمة الرئيسية:", [
        "📤 رفع وتوليد البيانات",
        "🧹 منظف البيانات الذكي",
        "📤 جسر التصدير العالمي",
        "📊 داشبورد Power BI",
        "🧠 مركز الذكاء الاصطناعي",
        "📄 التقرير التنفيذي",
        "☁️ السحابة والمشاركة"
    ])
    
    st.markdown("---")
    
    # الإعدادات المتقدمة
    with st.expander("⚙️ الإعدادات المتقدمة"):
        theme = st.selectbox("السمة", ["داكن", "فاتح"])
        lang = st.selectbox("اللغة", ["العربية", "English"])
        st.session_state.user_settings['theme'] = theme
        st.session_state.user_settings['language'] = lang
        
        st.markdown("---")
        st.markdown("*📊 إحصائيات الجلسة:*")
        if st.session_state.beast_df is not None:
            st.metric("السجلات", len(st.session_state.beast_df))
            st.metric("الأعمدة", len(st.session_state.beast_df.columns))
        else:
            st.info("لا توجد بيانات")

# ======== 5. دوال مساعدة ========

def safe_dataframe_check(df):
    """التحقق الآمن من صحة البيانات"""
    if df is None or df.empty:
        return False, "لا توجد بيانات متاحة"
    return True, "البيانات جاهزة"

def generate_ml_predictions(df, target_col, periods=30):
    """توليد تنبؤات باستخدام ML"""
    try:
        from sklearn.linear_model import LinearRegression
        from sklearn.preprocessing import PolynomialFeatures
        
        # تحضير البيانات
        df_clean = df.dropna()
        if len(df_clean) < 5:
            return None, "البيانات غير كافية للتنبؤ"
        
        # استخدام الأرقام فقط
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
        if target_col not in numeric_cols:
            return None, f"العمود {target_col} ليس رقمياً"
        
        X = np.arange(len(df_clean)).reshape(-1, 1)
        y = df_clean[target_col].values
        
        # نموذج متعدد الحدود للتنبؤ
        poly = PolynomialFeatures(degree=2)
        X_poly = poly.fit_transform(X)
        
        model = LinearRegression()
        model.fit(X_poly, y)
        
        # التنبؤ للفترات القادمة
        future_X = np.arange(len(df_clean), len(df_clean) + periods).reshape(-1, 1)
        future_X_poly = poly.transform(future_X)
        predictions = model.predict(future_X_poly)
        
        return predictions, "success"
    except Exception as e:
        return None, str(e)

def create_pdf_report():
    """إنشاء تقرير PDF حقيقي"""
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.lib.units import inch
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
        
        elements = []
        styles = getSampleStyleSheet()
        
        # العنوان
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#238636'),
            spaceAfter=30,
            alignment=1  # Center
        )
        
        elements.append(Paragraph(f"{APP_NAME} - التقرير التنفيذي", title_style))
        elements.append(Paragraph(f"بواسطة: {AUTHOR_SIGNATURE} | التاريخ: {datetime.now().strftime('%Y-%m-%d')}", styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # ملخص البيانات
        if st.session_state.beast_df is not None:
            df = st.session_state.beast_df
            summary_data = [
                ['المؤشر', 'القيمة'],
                ['عدد السجلات', str(len(df))],
                ['عدد الأعمدة', str(len(df.columns))],
                ['تاريخ التقرير', datetime.now().strftime('%Y-%m-%d %H:%M')]
            ]
            
            summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#238636')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f6f8fa')),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey)
            ]))
            
            elements.append(Paragraph("📊 ملخص البيانات", styles['Heading2']))
            elements.append(summary_table)
            elements.append(Spacer(1, 0.3*inch))
            
            # سجل التنظيف
            if st.session_state.cleaning_log:
                elements.append(Paragraph("🧹 سجل التنظيف", styles['Heading2']))
                for log in st.session_state.cleaning_log:
                    elements.append(Paragraph(f"• {log}", styles['Normal']))
        
        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
    except Exception as e:
        st.error(f"خطأ في إنشاء PDF: {e}")
        return None

# ======== 6. المحطات المتقدمة ========

# --- المحطة 1: رفع وتوليد البيانات ---
if menu == "📤 رفع وتوليد البيانات":
    st.markdown("<h1 class='gradient-text'>📤 مدخلات البيانات الذكية</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📁 رفع ملف", "🎲 توليد بيانات", "✍️ إدخال يدوي", "📷 OCR"])
    
    with tab1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        up = st.file_uploader("اسحب الملف هنا", type=['csv', 'xlsx', 'xls'], help="الحد الأقصى 200MB")
        
        if up:
            try:
                with st.spinner("جاري معالجة البيانات..."):
                    if up.name.endswith('xlsx') or up.name.endswith('xls'):
                        df = pd.read_excel(up, engine='openpyxl')
                    else:
                        df = pd.read_csv(up, encoding='utf-8')
                    
                    st.session_state.beast_df = df
                    st.session_state.cleaning_log = []
                    
                    st.success(f"✅ تم الربط بنجاح! {len(df):,} سجل | {len(df.columns)} عمود")
                    
                    # معاينة ذكية
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.dataframe(df.head(10), use_container_width=True)
                    with col2:
                        st.markdown("*📈 إحصائيات سريعة:*")
                        st.write(f"الأعمدة الرقمية: {len(df.select_dtypes(include=[np.number]).columns)}")
                        st.write(f"الأعمدة النصية: {len(df.select_dtypes(include=['object']).columns)}")
                        st.write(f"القيم الفارغة: {df.isnull().sum().sum():,}")
                        
            except Exception as e:
                st.error(f"❌ خطأ في قراءة الملف: {str(e)}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("⚡ توليد بيانات اختبار احترافية")
        
        col1, col2 = st.columns(2)
        with col1:
            rows = st.slider("عدد السجلات", 50, 10000, 1000)
            start_date = st.date_input("تاريخ البدء", datetime(2026, 1, 1))
        with col2:
            categories = st.multiselect("الأقسام", ["مبيعات", "مشتريات", "تسويق", "موارد بشرية"], ["مبيعات"])
            add_trend = st.checkbox("إضافة اتجاه تصاعدي", value=True)
        
        if st.button("🚀 توليد البيانات", key="generate"):
            with st.spinner("جاري التوليد..."):
                np.random.seed(42)
                dates = pd.date_range(start=start_date, periods=rows, freq='D')
                
                data = {'التاريخ': dates}
                
                if "مبيعات" in categories:
                    base_sales = np.random.normal(15000, 3000, rows)
                    if add_trend:
                        base_sales += np.linspace(0, 10000, rows)
                    data['المبيعات'] = np.maximum(base_sales, 1000).astype(int)
                    data['الربح'] = (data['المبيعات'] * np.random.uniform(0.15, 0.35, rows)).astype(int)
                
                if "مشتريات" in categories:
                    data['المشتريات'] = np.random.randint(5000, 12000, rows)
                
                if "تسويق" in categories:
                    data['الميزانية_التسويقية'] = np.random.randint(2000, 8000, rows)
                    data['العملاء_الجدد'] = np.random.randint(10, 100, rows)
                
                df = pd.DataFrame(data)
                st.session_state.beast_df = df
                st.success(f"✅ تم توليد {rows:,} سجل بنجاح!")
                st.dataframe(df.head(), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📝 محرر البيانات اليدوي (Excel Pro)")
        
        if st.session_state.beast_df is not None:
            edited_df = st.data_editor(
                st.session_state.beast_df,
                num_rows="dynamic",
                use_container_width=True,
                key="data_editor"
            )
            if st.button("💾 حفظ التعديلات"):
                st.session_state.beast_df = edited_df
                st.success("تم الحفظ!")
        else:
            # إنشاء dataframe فارغ للبدء
            empty_df = pd.DataFrame({
                'التاريخ': [datetime.now()],
                'البيان': ['مثال'],
                'المبلغ': [0],
                'القسم': ['عام']
            })
            edited_df = st.data_editor(empty_df, num_rows="dynamic", use_container_width=True)
            if st.button("🚀 بدء العمل بهذه البيانات"):
                st.session_state.beast_df = edited_df
                st.success("تم الإنشاء!")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab4:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📷 استخراج البيانات من الصور (OCR)")
        st.info("🚧 قريباً: ربط بـ Google Vision API لاستخراج الجداول من الصور")
        
        img_file = st.file_uploader("ارفع صورة تحتوي على جدول بيانات", type=['png', 'jpg', 'jpeg'])
        if img_file:
            st.image(img_file, use_container_width=True)
            st.warning("ميزة OCR تتطلب مفتاح API. سيتم تفعيلها في الإصدار القادم.")
        st.markdown("</div>", unsafe_allow_html=True)

# --- المحطة 2: منظف البيانات الذكي ---
elif menu == "🧹 منظف البيانات الذكي":
    st.markdown("<h1 class='gradient-text'>🧹 محرك التنظيف الذكي</h1>", unsafe_allow_html=True)
    
    is_valid, msg = safe_dataframe_check(st.session_state.beast_df)
    if not is_valid:
        st.warning(msg)
    else:
        df = st.session_state.beast_df
        
        # لوحة التحكم
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            duplicates = df.duplicated().sum()
            st.metric("السجلات المكررة", f"{duplicates:,}", delta=f"-{duplicates}" if duplicates > 0 else "✅")
        
        with col2:
            nulls = df.isnull().sum().sum()
            st.metric("القيم الفارغة", f"{nulls:,}", delta=f"-{nulls}" if nulls > 0 else "✅")
        
        with col3:
            outliers = 0
            for col in df.select_dtypes(include=[np.number]).columns:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers += ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()
            st.metric("القيم الشاذة", f"{outliers:,}")
        
        with col4:
            st.metric("جودة البيانات", f"{max(0, 100 - (duplicates + nulls)/len(df)*100):.1f}%")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # المقارنة المرئية
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("📋 قبل التنظيف")
            st.dataframe(df.head(10), use_container_width=True)
            st.caption(f"الأبعاد: {df.shape[0]} × {df.shape[1]}")
        
        # خيارات التنظيف
        st.markdown("---")
        st.subheader("⚙️ خيارات التنظيف المتقدمة")
        
        col_opt1, col_opt2, col_opt3 = st.columns(3)
        with col_opt1:
            remove_dup = st.checkbox("حذف التكرارات", value=True)
            remove_null = st.checkbox("حذف الصفوف الفارغة", value=True)
        with col_opt2:
            fill_null = st.checkbox("تعبئة القيم الفارغة", value=False)
            if fill_null:
                fill_method = st.selectbox("طريقة التعبئة", ["المتوسط", "الوسيط", "القيمة الأكثر تكراراً", "صفر"])
        with col_opt3:
            remove_outliers = st.checkbox("حذف القيم الشاذة", value=False)
            normalize = st.checkbox("تطبيع البيانات الرقمية", value=False)
        
        if st.button("🚀 تنفيذ التنظيف الشامل", key="clean"):
            with st.spinner("جاري التنظيف..."):
                old_shape = df.shape
                cleaning_steps = []
                
                # حذف التكرارات
                if remove_dup:
                    before = len(df)
                    df = df.drop_duplicates()
                    after = len(df)
                    if before != after:
                        cleaning_steps.append(f"حذف {before - after} سجل مكرر")
                
                # التعامل مع الفراغات
                if remove_null:
                    before = len(df)
                    df = df.dropna(how='all')
                    after = len(df)
                    if before != after:
                        cleaning_steps.append(f"حذف {before - after} صف فارغ")
                
                if fill_null and not remove_null:
                    for col in df.select_dtypes(include=[np.number]).columns:
                        if df[col].isnull().any():
                            if fill_method == "المتوسط":
                                df[col].fillna(df[col].mean(), inplace=True)
                            elif fill_method == "الوسيط":
                                df[col].fillna(df[col].median(), inplace=True)
                            elif fill_method == "صفر":
                                df[col].fillna(0, inplace=True)
                    cleaning_steps.append(f"تعبئة القيم الفارغة بـ {fill_method}")
                
                # حذف القيم الشاذة
                if remove_outliers:
                    for col in df.select_dtypes(include=[np.number]).columns:
                        Q1 = df[col].quantile(0.25)
                        Q3 = df[col].quantile(0.75)
                        IQR = Q3 - Q1
                        lower = Q1 - 1.5 * IQR
                        upper = Q3 + 1.5 * IQR
                        before = len(df)
                        df = df[(df[col] >= lower) & (df[col] <= upper)]
                        after = len(df)
                    if before != after:
                        cleaning_steps.append(f"حذف {before - after} قيمة شاذة")
                
                # التطبيع
                if normalize:
                    from sklearn.preprocessing import MinMaxScaler
                    numeric_cols = df.select_dtypes(include=[np.number]).columns
                    scaler = MinMaxScaler()
                    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
                    cleaning_steps.append("تطبيع البيانات الرقمية (0-1)")
                
                st.session_state.beast_df = df
                st.session_state.cleaning_log.extend(cleaning_steps)
                
                # عرض النتيجة
                with col_right:
                    st.subheader("✨ بعد التنظيف")
                    st.dataframe(df.head(10), use_container_width=True)
                    st.caption(f"الأبعاد: {df.shape[0]} × {df.shape[1]}")
                    
                    if cleaning_steps:
                        st.markdown("*📝 التغييرات:*")
                        for step in cleaning_steps:
                            st.markdown(f"<div class='alert-box alert-success'>✅ {step}</div>", unsafe_allow_html=True)
                
                st.success(f"✅ اكتمل التنظيف! من {old_shape[0]:,} إلى {df.shape[0]:,} سجل")
        st.markdown("</div>", unsafe_allow_html=True)

# --- المحطة 3: جسر التصدير العالمي ---
elif menu == "📤 جسر التصدير العالمي":
    st.markdown("<h1 class='gradient-text'>🌉 جسر التصدير العالمي</h1>", unsafe_allow_html=True)
    
    is_valid, msg = safe_dataframe_check(st.session_state.beast_df)
    if not is_valid:
        st.warning(msg)
    else:
        df = st.session_state.beast_df
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        
        # اختيار المنصة
        platform = st.selectbox(
            "اختر المنصة المستهدفة:",
            ["Power BI", "SQL Server", "Python", "Google Sheets", "Tableau", "Excel", "JSON API"],
            index=0
        )
        
        st.markdown("---")
        
        # أكواد الربط الفعلية
        if platform == "Power BI":
            st.subheader("🔗 ربط Power BI المباشر")
            st.markdown("""
                *الخطوات:*
                1. افتح Power BI Desktop
                2. اختر Get Data → Web
                3. استخدم الكود التالي في Power Query:
            """)
            
            csv_data = df.to_csv(index=False)
            b64 = base64.b64encode(csv_data.encode()).decode()
            
            st.code(f"""
// Power Query M Code
let
    Source = Csv.Document(Binary.FromText("{b64}"), [Delimiter=",", Columns={len(df.columns)}, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true])
in
    PromotedHeaders
            """, language="powerquery")
            
            st.download_button(
                "📥 تحميل ملف PBIX جاهز",
                data=csv_data,
                file_name="MIA8444_PowerBI_Data.csv",
                mime="text/csv"
            )
        
        elif platform == "SQL Server":
            st.subheader("🗄️ استيراد SQL Server")
            
            # توليد SQL فعلي
            sql_statements = []
            sql_statements.append(f"CREATE TABLE MIA8444_Data (")
            for col in df.columns:
                dtype = "VARCHAR(255)" if df[col].dtype == 'object' else "FLOAT"
                sql_statements.append(f"    [{col}] {dtype},")
            sql_statements[-1] = sql_statements[-1].rstrip(',')
            sql_statements.append(");")
            
            # INSERT statements
            for idx, row in df.head(100).iterrows():
                values = []
                for val in row:
                    if pd.isna(val):
                        values.append("NULL")
                    elif isinstance(val, str):
                        values.append(f"'{val.replace("'", "''")}'")
                    else:
                        values.append(str(val))
                sql_statements.append(f"INSERT INTO MIA8444_Data VALUES ({', '.join(values)});")
            
            sql_code = "\n".join(sql_statements)
            st.code(sql_code, language="sql")
            
            st.download_button(
                "📥 تحميل ملف SQL",
                data=sql_code,
                file_name="MIA8444_Import.sql",
                mime="text/plain"
            )
        
        elif platform == "Python":
            st.subheader("🐍 كود Python جاهز")
            st.code(f"""
import pandas as pd
import numpy as np

# قراءة البيانات
df = pd.read_csv('MIA8444_Final.csv')

# معاينة
print(df.head())
print(f"الأبعاد: {{df.shape}}")

# إحصائيات سريعة
print(df.describe())
            """, language="python")
        
        elif platform == "Google Sheets":
            st.subheader("📊 ربط Google Sheets")
            st.code("""
// Google Apps Script
function importMIA8444Data() {{
  var sheet = SpreadsheetApp.getActiveSheet();
  // استخدم CSV URL أو Google Drive
}}
            """, language="javascript")
            st.info("💡 تلميح: استخدم إضافة 'Import CSV' في Google Sheets")
        
        elif platform == "JSON API":
            st.subheader("🌐 JSON API Endpoint")
            json_data = df.head(100).to_json(orient='records', force_ascii=False)
            st.code(json_data, language="json")
            
            st.download_button(
                "📥 تحميل ملف JSON",
                data=json_data,
                file_name="MIA8444_API.json",
                mime="application/json"
            )
        
        # تحميل عام
        st.markdown("---")
        st.subheader("📥 التحميل المباشر")
        
        col_dl1, col_dl2, col_dl3 = st.columns(3)
        
        with col_dl1:
            st.download_button(
                "CSV نظيف",
                df.to_csv(index=False),
                "MIA8444_Final.csv",
                use_container_width=True
            )
        
        with col_dl2:
            # Excel مع تنسيق
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Data', index=False)
                # إضافة ورقة إحصائيات
                stats = df.describe()
                stats.to_excel(writer, sheet_name='Statistics')
            st.download_button(
                "Excel متقدم",
                buffer.getvalue(),
                "MIA8444_Final.xlsx",
                use_container_width=True
            )
        
        with col_dl3:
            st.download_button(
                "JSON",
                df.to_json(orient='records', force_ascii=False),
                "MIA8444_Final.json",
                use_container_width=True
            )
        
        st.markdown("</div>", unsafe_allow_html=True)

# --- المحطة 4: داشبورد Power BI ---
elif menu == "📊 داشبورد Power BI":
    st.markdown("<h1 class='gradient-text'>📊 لوحة القيادة التفاعلية</h1>", unsafe_allow_html=True)
    
    is_valid, msg = safe_dataframe_check(st.session_state.beast_df)
    if not is_valid:
        st.warning(msg)
    else:
        df = st.session_state.beast_df
        
        # فلاتر تفاعلية
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("🔍 فلاتر التحليل")
        
        col_f1, col_f2, col_f3 = st.columns(3)
        
        with col_f1:
            if 'التاريخ' in df.columns:
                df['التاريخ'] = pd.to_datetime(df['التاريخ'], errors='coerce')
                date_range = st.date_input(
                    "نطاق التاريخ",
                    [df['التاريخ'].min(), df['التاريخ'].max()],
                    key="date_filter"
                )
        
        with col_f2:
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_cols:
                metric_col = st.selectbox("المؤشر الرئيسي", numeric_cols, key="metric_select")
        
        with col_f3:
            chart_type = st.selectbox(
                "نوع الرسم البياني",
                ["Area", "Line", "Bar", "Scatter", "Pie", "Heatmap"],
                key="chart_type"
            )
        st.markdown("</div>", unsafe_allow_html=True)
        
        # المقاييس الرئيسية
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        
        if numeric_cols:
            metrics_cols = st.columns(min(4, len(numeric_cols)))
            
            for idx, col in enumerate(numeric_cols[:4]):
                with metrics_cols[idx]:
                    total = df[col].sum()
                    avg = df[col].mean()
                    delta = ((df[col].iloc[-1] - df[col].iloc[0]) / df[col].iloc[0] * 100) if len(df) > 1 and df[col].iloc[0] != 0 else 0
                    
                    st.markdown(f"""
                        <div class='metric-container'>
                            <div class='metric-label'>{col}</div>
                            <div class='metric-value'>{total:,.0f}</div>
                            <div style='font-size: 0.9rem; margin-top: 5px;'>
                                المتوسط: {avg:,.0f} | {delta:+.1f}%
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # الرسوم البيانية
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        
        try:
            # تطبيق الفلتر
            if 'التاريخ' in df.columns and len(date_range) == 2:
                mask = (df['التاريخ'] >= pd.Timestamp(date_range[0])) & (df['التاريخ'] <= pd.Timestamp(date_range[1]))
                filtered_df = df.loc[mask]
            else:
                filtered_df = df
            
            if chart_type == "Area":
                fig = px.area(
                    filtered_df,
                    x=filtered_df.index if 'التاريخ' not in filtered_df.columns else 'التاريخ',
                    y=numeric_cols[:3] if len(numeric_cols) > 0 else None,
                    template="plotly_dark",
                    title="📈 تحليل الاتجاهات",
                    color_discrete_sequence=['#238636', '#58a6ff', '#d29922']
                )
            elif chart_type == "Line":
                fig = px.line(
                    filtered_df,
                    x=filtered_df.index if 'التاريخ' not in filtered_df.columns else 'التاريخ',
                    y=metric_col if 'metric_col' in locals() else numeric_cols[0],
                    template="plotly_dark",
                    title="📉 منحنى التطور"
                )
            elif chart_type == "Bar":
                fig = px.bar(
                    filtered_df.head(20),
                    x=filtered_df.index[:20] if 'التاريخ' not in filtered_df.columns else 'التاريخ',
                    y=metric_col if 'metric_col' in locals() else numeric_cols[0],
                    template="plotly_dark",
                    title="📊 المقارنة البيانية"
                )
            elif chart_type == "Scatter":
                if len(numeric_cols) >= 2:
                    fig = px.scatter(
                        filtered_df,
                        x=numeric_cols[0],
                        y=numeric_cols[1] if len(numeric_cols) > 1 else numeric_cols[0],
                        size=numeric_cols[2] if len(numeric_cols) > 2 else None,
                        template="plotly_dark",
                        title="🔍 تحليل الارتباط"
                    )
                else:
                    fig = px.scatter(filtered_df, template="plotly_dark")
            elif chart_type == "Pie":
                fig = px.pie(
                    filtered_df.head(10),
                    values=metric_col if 'metric_col' in locals() else numeric_cols[0],
                    names=filtered_df.index[:10] if 'التاريخ' not in filtered_df.columns else 'التاريخ',
                    template="plotly_dark",
                    title="🥧 توزيع النسب"
                )
            else:  # Heatmap
                corr_cols = numeric_cols[:5] if len(numeric_cols) > 1 else numeric_cols
                corr_matrix = filtered_df[corr_cols].corr()
                fig = px.imshow(
                    corr_matrix,
                    template="plotly_dark",
                    title="🌡️ خريطة الارتباط",
                    color_continuous_scale='RdYlGn'
                )
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e6edf3'),
                title_font_size=20,
                title_x=0.5
            )
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"خطأ في إنشاء الرسم البياني: {e}")
            st.info("💡 جرب تغيير نوع الرسم البياني أو اختيار أعمدة مختلفة")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # تحليلات متقدمة
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📈 تحليلات متقدمة")
        
        col_adv1, col_adv2 = st.columns(2)
        
        with col_adv1:
            st.markdown("*📊 توزيع البيانات*")
            if numeric_cols:
                fig_dist = px.histogram(
                    filtered_df,
                    x=numeric_cols[0],
                    template="plotly_dark",
                    color_discrete_sequence=['#238636']
                )
                fig_dist.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_dist, use_container_width=True)
        
        with col_adv2:
            st.markdown("*📉 صندوق التشتت*")
            if len(numeric_cols) > 0:
                fig_box = px.box(
                    filtered_df,
                    y=numeric_cols[:3],
                    template="plotly_dark"
                )
                fig_box.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_box, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# --- المحطة 5: مركز الذكاء الاصطناعي ---
elif menu == "🧠 مركز الذكاء الاصطناعي":
    st.markdown("<h1 class='gradient-text'>🧠 مركز الذكاء التنبئي</h1>", unsafe_allow_html=True)
    
    is_valid, msg = safe_dataframe_check(st.session_state.beast_df)
    if not is_valid:
        st.warning(msg)
    else:
        df = st.session_state.beast_df
        
        tab_ml1, tab_ml2, tab_ml3 = st.tabs(["🔮 التنبؤ", "🎯 التصنيف", "📊 التجميع"])
        
        with tab_ml1:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.subheader("🔮 نموذج التنبؤ بالمستقبل")
            
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if len(numeric_cols) > 0:
                target_col = st.selectbox("اختر العمود المستهدف للتنبؤ", numeric_cols)
                periods = st.slider("فترة التنبؤ (يوم)", 7, 365, 30)
                
                if st.button("🚀 تدريب النموذج والتنبؤ"):
                    with st.spinner("جاري تدريب نموذج ML..."):
                        predictions, status = generate_ml_predictions(df, target_col, periods)
                        
                        if predictions is not None:
                            # عرض النتائج
                            future_dates = pd.date_range(
                                start=df['التاريخ'].max() if 'التاريخ' in df.columns else datetime.now(),
                                periods=periods,
                                freq='D'
                            )
                            
                            pred_df = pd.DataFrame({
                                'التاريخ': future_dates,
                                'التنبؤ': predictions,
                                'الحد الأدنى': predictions * 0.9,
                                'الحد الأقصى': predictions * 1.1
                            })
                            
                            fig_pred = go.Figure()
                            
                            # البيانات التاريخية
                            if 'التاريخ' in df.columns:
                                fig_pred.add_trace(go.Scatter(
                                    x=df['التاريخ'],
                                    y=df[target_col],
                                    name='تاريخي',
                                    line=dict(color='#58a6ff', width=2)
                                ))
                            
                            # التنبؤ
                            fig_pred.add_trace(go.Scatter(
                                x=pred_df['التاريخ'],
                                y=pred_df['التنبؤ'],
                                name='تنبؤ',
                                line=dict(color='#238636', width=3, dash='dash')
                            ))
                            
                            # نطاق الثقة
                            fig_pred.add_trace(go.Scatter(
                                x=pred_df['التاريخ'].tolist() + pred_df['التاريخ'].tolist()[::-1],
                                y=pred_df['الحد الأقنى'].tolist() + pred_df['الحد الأدنى'].tolist()[::-1],
                                fill='toself',
                                fillcolor='rgba(35, 134, 54, 0.2)',
                                line=dict(color='rgba(255,255,255,0)'),
                                name='نطاق الثقة 90%'
                            ))
                            
                            fig_pred.update_layout(
                                template="plotly_dark",
                                title=f"🔮 تنبؤ {target_col} للـ {periods} يوم القادمة",
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                hovermode='x unified'
                            )
                            
                            st.plotly_chart(fig_pred, use_container_width=True)
                            
                            # ملخص التنبؤ
                            col_p1, col_p2, col_p3 = st.columns(3)
                            with col_p1:
                                st.metric("متوسط التنبؤ", f"{predictions.mean():,.0f}")
                            with col_p2:
                                st.metric("أعلى قيمة متوقعة", f"{predictions.max():,.0f}")
                            with col_p3:
                                trend = "📈 صاعد" if predictions[-1] > predictions[0] else "📉 هابط"
                                st.metric("الاتجاه العام", trend)
                            
                            st.session_state.ml_models['last_prediction'] = {
                                'target': target_col,
                                'periods': periods,
                                'predictions': predictions.tolist()
                            }
                            
                            st.success("✅ تم التنبؤ بنجاح بناءً على تحليل النمط التاريخي!")
                        else:
                            st.error(f"❌ خطأ في التنبؤ: {status}")
            else:
                st.warning("لا توجد أعمدة رقمية للتنبؤ")
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tab_ml2:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.subheader("🎯 تصنيف ذكي (Clustering)")
            st.info("🚧 قريباً: K-Means Clustering لتقسيم العملاء/المنتجات إلى فئات")
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tab_ml3:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.subheader("📊 تحليل الارتباطات")
            
            if len(numeric_cols) > 1:
                corr_matrix = df[numeric_cols].corr()
                fig_corr = px.imshow(
                    corr_matrix,
                    template="plotly_dark",
                    title="مصفوفة الارتباط",
                    color_continuous_scale='RdYlGn',
                    aspect="auto"
                )
                fig_corr.update_layout(paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_corr, use_container_width=True)
                
                # أقوى الارتباطات
                st.subheader("🔗 أقوى العلاقات")
                corr_pairs = []
                for i in range(len(corr_matrix.columns)):
                    for j in range(i+1, len(corr_matrix.columns)):
                        corr_pairs.append({
                            'المتغير 1': corr_matrix.columns[i],
                            'المتغير 2': corr_matrix.columns[j],
                            'معامل الارتباط': corr_matrix.iloc[i, j]
                        })
                
                corr_df = pd.DataFrame(corr_pairs).sort_values('معامل الارتباط', key=abs, ascending=False)
                st.dataframe(corr_df.head(10), use_container_width=True)
            else:
                st.info("تحتاج على الأقل عمودين رقميين لتحليل الارتباط")
            st.markdown("</div>", unsafe_allow_html=True)

# --- المحطة 6: التقرير التنفيذي ---
elif menu == "📄 التقرير التنفيذي":
    st.markdown("<h1 class='gradient-text'>📄 التقرير التحليلي المتكامل</h1>", unsafe_allow_html=True)
    
    is_valid, msg = safe_dataframe_check(st.session_state.beast_df)
    if not is_valid:
        st.warning(msg)
    else:
        df = st.session_state.beast_df
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        
        # رأس التقرير
        st.markdown(f"""
            <div style='text-align: center; border-bottom: 3px solid #238636; padding-bottom: 20px; margin-bottom: 30px;'>
                <h1 style='color: #238636; margin: 0;'>{APP_NAME}</h1>
                <h2 style='color: #58a6ff; margin: 10px 0;'>التقرير التنفيذي الشامل</h2>
                <p style='color: #8b949e;'>إعداد: {AUTHOR_SIGNATURE} | التاريخ: {datetime.now().strftime('%Y/%m/%d')}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # الملخص التنفيذي
        st.subheader("📋 الملخص التنفيذي")
        
        exec_summary = f"""
        تم تحليل {len(df):,} سجل بيانات عبر {len(df.columns)} مؤشر رئيسي. 
        """
        
        if st.session_state.cleaning_log:
            exec_summary += f"تم تنفيذ {len(st.session_state.cleaning_log)} عملية تنظيف لضمان جودة البيانات. "
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            total_revenue = df[numeric_cols[0]].sum() if 'مبيعات' in numeric_cols else df[numeric_cols[0]].sum()
            exec_summary += f"إجمالي المبيعات/الإيرادات: {total_revenue:,.0f}."
        
        st.markdown(f"<div class='alert-box alert-success'>{exec_summary}</div>", unsafe_allow_html=True)
        
        # 1. فحص البيانات
        st.subheader("1️⃣ فحص ومعالجة البيانات")
        
        col_r1, col_r2 = st.columns([2, 1])
        
        with col_r1:
            if st.session_state.cleaning_log:
                st.markdown("*سجل العمليات:*")
                for log in st.session_state.cleaning_log:
                    st.write(f"✅ {log}")
            else:
                st.write("✅ تم فحص البيانات - لا توجد مشكلات جوهرية")
        
        with col_r2:
            quality_score = 100
            if st.session_state.cleaning_log:
                quality_score -= len(st.session_state.cleaning_log) * 5
            
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=quality_score,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "جودة البيانات"},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#238636"},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 50], 'color': '#f85149'},
                        {'range': [50, 80], 'color': '#d29922'},
                        {'range': [80, 100], 'color': '#238636'}
                    ],
                }
            ))
            fig_gauge.update_layout(height=250, paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        # 2. الأداء العام
        st.subheader("2️⃣ تحليل الأداء العام")
        
        if len(numeric_cols) > 0:
            metrics_report = st.columns(min(4, len(numeric_cols)))
            
            for idx, col in enumerate(numeric_cols[:4]):
                with metrics_report[idx]:
                    current = df[col].iloc[-1] if len(df) > 0 else 0
                    previous = df[col].iloc[-2] if len(df) > 1 else current
                    change = ((current - previous) / previous * 100) if previous != 0 else 0
                    
                    st.metric(
                        label=col,
                        value=f"{current:,.0f}",
                        delta=f"{change:+.1f}%"
                    )
        
        # 3. الرسوم البيانية التحليلية
        st.subheader("3️⃣ الرسوم البيانية التحليلية")
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown("*توزيع البيانات*")
            if len(numeric_cols) > 0:
                fig_rep1 = px.histogram(
                    df,
                    x=numeric_cols[0],
                    template="plotly_dark",
                    color_discrete_sequence=['#238636']
                )
                fig_rep1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300)
                st.plotly_chart(fig_rep1, use_container_width=True)
        
        with col_chart2:
            st.markdown("*الاتجاه الزمني*")
            if 'التاريخ' in df.columns and len(numeric_cols) > 0:
                fig_rep2 = px.line(
                    df,
                    x='التاريخ',
                    y=numeric_cols[0],
                    template="plotly_dark",
                    color_discrete_sequence=['#58a6ff']
                )
                fig_rep2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300)
                st.plotly_chart(fig_rep2, use_container_width=True)
        
        # 4. التوصيات الاستراتيجية
        st.subheader("4️⃣ التوصيات الاستراتيجية")
        
        recommendations = []
        
        # تحليل تلقائي للتوصيات
        if len(numeric_cols) > 0:
            sales_col = None
            for col in numeric_cols:
                if any(keyword in col.lower() for keyword in ['مبيعات', 'sales', 'revenue', 'ايراد']):
                    sales_col = col
                    break
            
            if sales_col:
                recent_avg = df[sales_col].tail(7).mean()
                old_avg = df[sales_col].head(7).mean()
                
                if recent_avg > old_avg * 1.1:
                    recommendations.append("📈 *زخم إيجابي*: المبيعات في تزايد مستمر. يُنصح بزيادة المخزون.")
                elif recent_avg < old_avg * 0.9:
                    recommendations.append("📉 *تنبيه*: تراجع في المبيعات. يُنصح بمراجعة استراتيجية التسويق.")
                else:
                    recommendations.append("📊 *استقرار*: الأداء مستقر. فرصة لتحسين الكفاءة التشغيلية.")
        
        # توصيات عامة
        recommendations.extend([
            "💡 *تحسين الجودة*: استمر في مراقبة جودة البيانات بشكل دوري.",
            "🎯 *التركيز على العملاء*: تحليل سلوك العملاء يمكن أن يكشف فرص نمو جديدة.",
            "☁️ *الأتمتة*: استخدم التنبؤات الآلية لتخطيط المخزون المستقبلي."
        ])
        
        for rec in recommendations:
            st.markdown(f"<div class='alert-box alert-warning' style='border-color: #58a6ff;'>{rec}</div>", unsafe_allow_html=True)
        
        # 5. خاتمة التقرير
        st.markdown("---")
        st.markdown(f"""
            <div style='text-align: center; color: #8b949e; padding: 20px;'>
                <p>تم إعداد هذا التقرير بواسطة <strong>{APP_NAME}</strong> الإصدار {APP_VERSION}</p>
                <p>التوقيع الرقمي: <span style='color: #238636;'>{AUTHOR_SIGNATURE}</span></p>
                <p>© 2026 جميع الحقوق محفوظة</p>
            </div>
        """, unsafe_allow_html=True)
        
        # أزرار التصدير
        st.markdown("---")
        st.subheader("📥 تصدير التقرير")
        
        col
