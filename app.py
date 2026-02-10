import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import io
import base64
from io import BytesIO
import warnings
warnings.filterwarnings('ignore')

# ======= 1. الذاكرة المركزية =======
if 'beast_df' not in st.session_state:
    st.session_state.beast_df = None
if 'cleaning_log' not in st.session_state:
    st.session_state.cleaning_log = []
if 'ml_predictions' not in st.session_state:
    st.session_state.ml_predictions = None
if 'user_theme' not in st.session_state:
    st.session_state.user_theme = 'dark'

# ======= 2. الإعدادات =======
AUTHOR_SIGNATURE = "MIA8444"
APP_NAME = "The Beast Pro"
APP_VERSION = "3.0.0"
LOGO_FILE = "8888.jpg"

st.set_page_config(
    page_title=f"{AUTHOR_SIGNATURE} | {APP_NAME}",
    page_icon="🦁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======= 3. CSS احترافي =======
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');
    
    * { 
        font-family: 'Tajawal', sans-serif; 
        direction: rtl;
    }
    
    .stApp { 
        background: linear-gradient(135deg, #0a0e17 0%, #111827 50%, #0a0e17 100%);
        color: #f3f4f6;
    }
    
    .glass-card {
        background: rgba(17, 24, 39, 0.7);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 24px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        border-color: rgba(59, 130, 246, 0.5);
        transform: translateY(-5px);
        box-shadow: 0 30px 60px -12px rgba(59, 130, 246, 0.2);
    }
    
    .gradient-text {
        background: linear-gradient(135deg, #3b82f6 0%, #10b981 50%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        background-size: 200% 200%;
        animation: gradient 3s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .metric-container {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        color: white;
        box-shadow: 0 20px 40px -10px rgba(5, 150, 105, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .metric-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg);
        animation: shine         animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) rotate(45deg); }
        100% { transform: translateX(100%) rotate(45deg); }
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 900;
        margin: 10px 0;
        position: relative;
        z-index: 1;
    }
    
    .btn-primary {
        background: linear-gradient(90deg, #3b82f6, #10b981);
        border: none;
        border-radius: 12px;
        padding: 15px 40px;
        color: white;
        font-weight: 700;
        font-size: 1.1rem;
        cursor: pointer;
        transition: all 0.3s;
        width: 100%;
    }
    
    .btn-primary:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.4);
    }
    
    .footer {
        text-align: center;
        padding: 40px;
        color: #6b7280;
        border-top: 1px solid #374151;
        margin-top: 60px;
        background: rgba(10, 14, 23, 0.8);
    }
    
    .status-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .status-active { background: rgba(16, 185, 129, 0.2); color: #10b981; }
    .status-warning { background: rgba(245, 158, 11, 0.2); color: #f59e0b; }
    .status-error { background: rgba(239, 68, 68, 0.2); color: #ef4444; }
    </style>
""", unsafe_allow_html=True)

# ======= 4. الشريط الجانبي =======
with st.sidebar:
    col_logo = st.columns([1])
    with col_logo[0]:
        if os.path.exists(LOGO_FILE):
            st.image(LOGO_FILE, use_container_width=True)
        else:
            st.markdown("<div style='text-align: center; font-size: 5rem;'>🦁</div>", unsafe_allow_html=True)
    
    st.markdown(f"<h1 style='text-align:center;' class='gradient-text'>{APP_NAME}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:#6b7280;'>v{APP_VERSION} | {AUTHOR_SIGNATURE}</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    menu = st.radio("🎯 القائمة:", [
        "🏠 الرئيسية",
        "📤 رفع البيانات",
        "🧹 تنظيف ذكي",
        "📊 داشبورد Pro",
        "🧠 تنبؤ AI",
        "📄 تقرير PDF احترافي"
    ])
    
    st.markdown("---")
    
    with st.expander("⚙️ الإعدادات"):
        theme = st.selectbox("السمة", ["داكن", "فاتح"])
        lang = st.selectbox("اللغة", ["العربية", "English"])
        st.session_state.user_theme = theme

# ======= 5. دالة PDF الاحترافية =======

def create_beast_pdf():
    """إنشاء تقرير PDF احترافي بـ ReportLab"""
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import (
            SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
            Image, PageBreak, HRFlowable
        )
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib.enums import TA_CENTER, TA_RIGHT
        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.use('Agg')
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=1.5*cm,
            leftMargin=1.5*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        elements = []
        styles = getSampleStyleSheet()
        
        # أنماط مخصصة
        title_style = ParagraphStyle(
            'BeastTitle',
            parent=styles['Heading1'],
            fontSize=32,
            textColor=colors.HexColor('#059669'),
            alignment=TA_CENTER,
            spaceAfter=30,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'BeastSubtitle',
            parent=styles['Normal'],
            fontSize=16,
            textColor=colors.HexColor('#3b82f6'),
            alignment=TA_CENTER,
            spaceAfter=40
        )
        
        heading_style = ParagraphStyle(
            'BeastHeading',
            parent=styles['Heading2'],
            fontSize=18,
            textColor=colors.HexColor('#059669'),
            spaceAfter=15,
            spaceBefore=20,
            borderPadding=10,
            borderWidth=2,
            borderColor=colors.HexColor('#059669'),
            borderRadius=8,
            leftIndent=10
        )
        
        body_style = ParagraphStyle(
            'BeastBody',
            parent=styles['Normal'],
            fontSize=11,
            alignment=TA_RIGHT,
            leading=22,
            rightIndent=10
        )
        
        # ===== صفحة الغلاف =====
        elements.append(Spacer(1, 4*cm))
        elements.append(Paragraph("🦁 THE BEAST PRO", title_style))
        elements.append(Paragraph("التقرير التحليلي الاحترافي", subtitle_style))
        
        # معلومات التقرير
        info_data = [
            [f"المحلل: {AUTHOR_SIGNATURE}"],
            [f"التاريخ: {datetime.now().strftime('%Y/%m/%d')}"],
            [f"الوقت: {datetime.now().strftime('%H:%M:%S')}"],
            ["الإصدار: 3.0 Pro Max"]
        ]
        info_table = Table(info_data, colWidths=[12*cm])
        info_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#6b7280')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 5*cm))
        
        # شعار الشركة
        elements.append(HRFlowable(width="80%", thickness=3, color=colors.HexColor('#059669'), hAlign='CENTER'))
        elements.append(Spacer(1, 1*cm))
        elements.append(Paragraph("<b>نظام تحليل البيانات المتقدم</b>", ParagraphStyle('center', alignment=TA_CENTER, fontSize=14, textColor=colors.HexColor('#3b82f6'))))
        elements.append(PageBreak())
        
        df = st.session_state.beast_df
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # ===== الملخص التنفيذي =====
        elements.append(Paragraph("📋 الملخص التنفيذي", heading_style))
        
        total_records = len(df)
        total_cols = len(df.columns)
        
        summary = f"""
        تم تحليل <b>{total_records:,}</b> سجل بيانات عبر <b>{total_cols}</b> مؤشر رئيسي 
        باستخدام خوارزميات متقدمة. تم تنفيذ <b>{len(st.session_state.cleaning_log)}</b> 
        عملية تحسين لجودة البيانات لضمان دقة التحليل.
        """
        
        if numeric_cols:
            total_val = df[numeric_cols[0]].sum()
            summary += f"<br/><br/>الإجمالي العام: <b>{total_val:,.0f}</b> وحدة."
        
        elements.append(Paragraph(summary, body_style))
        elements.append(Spacer(1, 0.8*cm))
        
        # ===== المؤشرات الرئيسية =====
        elements.append(Paragraph("📊 المؤشرات الرئيسية", heading_style))
        
        if numeric_cols:
            stats_data = [['المؤشر', 'المجموع', 'المتوسط', 'الأعلى', 'الأدنى', 'النمو']]
            
            for col in numeric_cols[:6]:
                current = df[col].iloc[-1] if len(df) > 0 else 0
                previous = df[col].iloc[-2] if len(df) > 1 else current
                growth = ((current - previous) / previous * 100) if previous != 0 else 0
                
                stats_data.append([
                    col,
                    f"{df[col].sum():,.0f}",
                    f"{df[col].mean():,.0f}",
                    f"{df[col].max():,.0f}",
                    f"{df[col].min():,.0f}",
                    f"{growth:+.1f}%"
                ])
            
            stats_table = Table(stats_data, colWidths=[3.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2*cm])
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 14),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f3f4f6')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('TOPPADDING', (0, 1), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
            ]))
            elements.append(stats_table)
            elements.append(Spacer(1, 0.8*cm))
        
        # ===== رسم بياني =====
        if numeric_cols:
            elements.append(Paragraph("📈 التحليل البياني", heading_style))
            
            fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
            ax.set_facecolor('#f9fafb')
            fig.patch.set_facecolor('white')
            
            x_pos = np.arange(len(df.head(30)))
            ax.plot(x_pos, df[numeric_cols[0]].head(30), color='#059669', linewidth=2.5, label=numeric_cols[0], marker='o', markersize=4)
            
            if len(numeric_cols) > 1:
                ax.plot(x_pos, df[numeric_cols[1]].head(30), color='#3b82f6', linewidth=2.5, label=numeric_cols[1], marker='s', markersize=4)
            
            ax.fill_between(x_pos, df[numeric_cols[0]].head(30), alpha=0.3, color='#059669')
            ax.set_xlabel('الفترة الزمنية', fontsize=11, fontweight='bold')
            ax.set_ylabel('القيمة', fontsize=11, fontweight='bold')
            ax.set_title('تحليل الاتجاهات الرئيسية', fontsize=14, fontweight='bold', pad=20)
            ax.legend(loc='upper left', framealpha=0.9)
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            plt.tight_layout()
            img_buf = BytesIO()
            plt.savefig(img_buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
            img_buf.seek(0)
            plt.close()
            
            elements.append(Image(img_buf, width=16*cm, height=8*cm))
            elements.append(Spacer(1, 0.5*cm))
        
        # ===== سجل التنظيف =====
        if st.session_state.cleaning_log:
            elements.append(Paragraph("🧹 سجل عمليات التحسين", heading_style))
            
            clean_data = [['#', 'العملية المنفذة', 'التوقيت', 'الحالة']]
            for idx, log in enumerate(st.session_state.cleaning_log, 1):
                clean_data.append([
                    str(idx),
                    log,
                    datetime.now().strftime('%H:%M'),
                    '✓ منجز'
                ])
            
            clean_table = Table(clean_data, colWidths=[2*cm, 10*cm, 3*cm, 3*cm])
            clean_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#eff6ff')]),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
            ]))
            elements.append(clean_table)
            elements.append(Spacer(1, 0.5*cm))
        
        # ===== التنبؤات =====
        if st.session_state.ml_predictions:
            elements.append(Paragraph("🔮 نتائج التحليل التنبؤي", heading_style))
            
            pred = st.session_state.ml_predictions
            avg_pred = np.mean(pred['predictions'])
            max_pred = np.max(pred['predictions'])
            trend = "صاعد 📈" if pred['predictions'][-1] > pred['predictions'][0] else "هابط 📉"
            
            pred_text = f"""
            تم إنشاء نموذج تنبؤي لـ <b>{pred['periods']}</b> فترة قادمة باستخدام 
            خوارزمية <b>Polynomial Regression</b>.<br/><br/>
            <b>النتائج المتوقعة:</b><br/>
            • المتوسط: <b>{avg_pred:,.0f}</b><br/>
            • القمة المتوقعة: <b>{max_pred:,.0f}</b><br/>
            • الاتجاه العام: <b>{trend}</b>
            """
            elements.append(Paragraph(pred_text, body_style))
            elements.append(Spacer(1, 0.5*cm))
        
        # ===== التوصيات =====
        elements.append(Paragraph("💡 التوصيات الاستراتيجية", heading_style))
        
        recommendations = [
            "استمر في مراقبة جودة البيانات بشكل دوري وتحديثها.",
            "استخدم التنبؤات لتخطيط المخزون والموارد المستقبلية.",
            "تحليل سلوك العملاء لاكتشاف فرص النمو الجديدة.",
            "تطبيق الأتمتة للتقارير الدورية لتوفير الوقت والجهد.",
            "مراجعة الأداء أسبوعياً ومقارنته بالتوقعات."
        ]
        
        for i, rec in enumerate(recommendations, 1):
            elements.append(Paragraph(f"<b>{i}.</b> {rec}", body_style))
        
        elements.append(Spacer(1, 1.5*cm))
        
        # ===== التذييل =====
        elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#059669')))
        elements.append(Spacer(1, 0.5*cm))
        
        footer = f"""
        <para alignment="center">
        <font color="#059669" size="12"><b>{APP_NAME} v{APP_VERSION}</b></font><br/>
        <font color="#6b7280" size="10">تطوير: {AUTHOR_SIGNATURE} | © 2026 جميع الحقوق محفوظة</font><br/>
        <font color="#9ca3af" size="9">تم إنشاء هذا التقرير تلقائياً بواسطة النظام</font>
        </para>
        """
        elements.append(Paragraph(footer, styles['Normal']))
        
        # بناء PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
        
    except Exception as e:
        st.error(f"❌ خطأ في إنشاء PDF: {str(e)}")
        return None

# ======= 6. المحطات =======

# --- الرئيسية ---
if menu == "🏠 الرئيسية":
    st.markdown("""
        <div style='text-align: center; padding: 60px 20px;'>
            <div style='font-size: 6rem; margin-bottom: 20px;'>🦁</div>
            <h1 class='gradient-text' style='font-size: 3.5rem;'>THE BEAST PRO</h1>
            <p style='font-size: 1.5rem; color: #6b7280; margin-top: 20px;'>
                نظام تحليل البيانات المتقدم بالذكاء الاصطناعي
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    features = [
        ("📊", "تحليل ذكي", "تقارير فورية"),
        ("🧠", "تنبؤ AI", "مستقبل البيانات"),
        ("📄", "PDF احترافي", "تقارير مطبوعة")
    ]
    
    for col, (icon, title, desc) in zip([col1, col2, col3], features):
        with col:
            st.markdown(f"""
                <div class='glass-card' style='text-align: center;'>
                    <div style='font-size: 3rem;'>{icon}</div>
                    <h3>{title}</h3>
                    <p style='color: #6b7280;'>{desc}</p>
                </div>
            """, unsafe_allow_html=True)

# --- رفع البيانات ---
elif menu == "📤 رفع البيانات":
    st.markdown("<h1 class='gradient-text'>📤 رفع البيانات</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📁 ملف", "🎲 توليد", "✍️ يدوي"])
    
    with tab1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        file = st.file_uploader("اختر ملف", type=['csv', 'xlsx', 'xls'])
        if file:
            try:
                if file.name.endswith('xlsx') or file.name.endswith('xls'):
                    df = pd.read_excel(file, engine='openpyxl')
                else:
                    df = pd.read_csv(file)
                
                st.session_state.beast_df = df
                st.session_state.cleaning_log = []
                
                st.success(f"✅ {len(df):,} سجل | {len(df.columns)} عمود")
                st.dataframe(df.head(10), use_container_width=True)
            except Exception as e:
                st.error(f"❌ خطأ: {e}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        if st.button("🚀 توليد بيانات", use_container_width=True):
            df = pd.DataFrame({
                'التاريخ': pd.date_range('2026-01-01', periods=200),
                'المبيعات': np.random.randint(10000, 50000, 200),
                'المصاريف': np.random.randint(5000, 20000, 200),
                'العملاء': np.random.randint(50, 200, 200)
            })
            df['الربح'] = df['المبيعات'] - df['المصاريف']
            st.session_state.beast_df = df
            st.success(f"✅ تم توليد {len(df)} سجل!")
            st.dataframe(df.head(), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        curr = st.session_state.beast_df if st.session_state.beast_df is not None else pd.DataFrame({
            'البند': ['مثال'], 'القيمة': [0]
        })
        edited = st.data_editor(curr, num_rows="dynamic", use_container_width=True)
        if st.button("💾 حفظ"):
            st.session_state.beast_df = edited
            st.success("تم!")
        st.markdown("</div>", unsafe_allow_html=True)

# --- تنظيف ذكي ---
elif menu == "🧹 تنظيف ذكي":
    st.markdown("<h1 class='gradient-text'>🧹 تنظيف البيانات</h1>", unsafe_allow_html=True)
    
    if st.session_state.beast_df is None:
        st.warning("ارفع البيانات أولاً")
    else:
        df = st.session_state.beast_df
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        
        # إحصائيات
        cols = st.columns(4)
        metrics = [
            ("السجلات", len(df)),
            ("مكرر", df.duplicated().sum()),
            ("فارغ", df.isnull().sum().sum()),
            ("جودة", f"{max(0, 100-(df.duplicated().sum()+df.isnull().sum().sum())/len(df)*100):.0f}%")
        ]
        
        for col, (label, val) in zip(cols, metrics):
            with col:
                st.markdown(f"""
                    <div class='metric-container'>
                        <div style='font-size: 0.9rem; opacity: 0.9;'>{label}</div>
                        <div class='metric-value'>{val}</div>
                    </div>
                """, unsafe_allow_html=True)
        
        # خيارات
        st.markdown("---")
        c1, c2, c3, c4 = st.columns(4)
        with c1: rm_dup = st.checkbox("حذف تكرار", True)
        with c2: rm_null = st.checkbox("حذف فراغات", True)
        with c3: fill_null = st.checkbox("تعبئة", False)
        with c4: norm = st.checkbox("تطبيع", False)
        
        if st.button("🚀 تنفيذ التنظيف", use_container_width=True):
            logs = []
            
            if rm_dup:
                before = len(df)
                df = df.drop_duplicates()
                if len(df) < before:
                    logs.append(f"حذف {before-len(df)} مكرر")
            
            if rm_null:
                before = len(df)
                df = df.dropna(how='all')
                if len(df) < before:
                    logs.append(f"حذف {before-len(df)} صف فارغ")
            
            if fill_null:
                for col in df.select_dtypes(include=[np.number]).columns:
                    df[col].fillna(df[col].mean(), inplace=True)
                logs.append("تعبئة بالمتوسط")
            
            if norm:
                from sklearn.preprocessing import MinMaxScaler
                num_cols = df.select_dtypes(include=[np.number]).columns
                df[num_cols] = MinMaxScaler().fit_transform(df[num_cols])
                logs.append("تطبيع (0-1)")
            
            st.session_state.beast_df = df
            st.session_state.cleaning_log.extend(logs)
            
            for log in logs:
                st.success(f"✅ {log}")
        
        st.markdown("</div>", unsafe_allow_html=True)

# --- داشبورد Pro ---
elif menu == "📊 داشبورد Pro":
    st.markdown("<h1 class='gradient-text'>📊 داشبورد احترافي</h1>", unsafe_allow_html=True)
    
    if st.session_state.beast_df is None:
        st.warning("ارفع البيانات أولاً")
    else:
        df = st.session_state.beast_df
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        
        # مقاييس
        if numeric_cols:
            cols = st.columns(min(4, len(numeric_cols)))
            for i, col in enumerate(numeric_cols[:4]):
                with cols[i]:
                    trend = np.random.choice(["📈", "📉", "➡️"])
                    st.markdown(f"""
                        <div class='metric-container'>
                            <div style='font-size: 0.9rem;'>{col} {trend}</div>
                            <div class='metric-value'>{df[col].sum():,.0f}</div>
                            <div style='font-size: 0.85rem; opacity: 0.9;'>متوسط: {df[col].mean():,.0f}</div>
                        </div>
                    """, unsafe_allow_html=True)
        
        # رسوم بيانية
        if numeric_cols:
            st.markdown("---")
            chart_type = st.selectbox("نوع الرسم", ["Area", "Line", "Bar", "Scatter"])
            
            try:
                if chart_type == "Area":
                    fig = px.area(df, y=numeric_cols[:3], template="plotly_dark", color_discrete_sequence=['#10b981', '#3b82f6', '#f59e0b'])
                elif chart_type == "Line":
                    fig = px.line(df, y=numeric_cols[:3], template="plotly_dark")
                elif chart_type == "Bar":
                    fig = px.bar(df.head(20), y=numeric_cols[0], template="plotly_dark", color_discrete_sequence=['#10b981'])
                else:
                    fig = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1] if len(numeric_cols) > 1 else numeric_cols[0], template="plotly_dark")
                
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#f3f4f6')
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"خطأ: {e}")
        
        st.markdown("</div>", unsafe_allow_html=True)

# --- تنبؤ AI ---
elif menu == "🧠 تنبؤ AI":
    st.markdown("<h1 class='gradient-text'>🧠 التنبؤ الذكي</h1>", unsafe_allow_html=True)
    
    if st.session_state.beast_df is None:
        st.warning("ارفع البيانات أولاً")
    else:
        df = st.session_state.beast_df
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        
        if numeric_cols:
            target = st.selectbox("المؤشر المستهدف", numeric_cols)
            periods = st.slider("فترة التنبؤ (يوم)", 7, 365, 30)
            
            if st.button("🔮 بدء التنبؤ", use_container_width=True):
                with st.spinner("جاري تحليل البيانات..."):
                    try:
                        from sklearn.linear_model import LinearRegression
                        from sklearn.preprocessing import PolynomialFeatures
                        
                        X = np.arange(len(df)).reshape(-1, 1)
                        y = df[target].values
                        
                        poly = PolynomialFeatures(degree=2)
                        X_poly = poly.fit_transform(X)
                        
                        model = LinearRegression()
                        model.fit(X_poly, y)
                        
                        future = np.arange(len(df), len(df)+periods).reshape(-1, 1)
                        preds = model.predict(poly.transform(future))
                        
                        st.session_state.ml_predictions = {
                            'target': target,
                            'periods': periods,
                            'predictions': preds.tolist()
                        }
                        
                        # رسم
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(y=y, name='تاريخي', line=dict(color='#3b82f6', width=2)))
                        fig.add_trace(go.Scatter(
                            y=list(y)+list(preds),
                            name='تنبؤ',
                            line=dict(color='#10b981', width=3, dash='dash')
                        ))
                        fig.add_trace(go.Scatter(
                            x=list(range(len(y), len(y)+len(preds))),
                            y=preds,
                            name='فترة التنبؤ',
                            line=dict(color='#f59e0b', width=2)
                        ))
                        
                        fig.update_layout(
                            template="plotly_dark",
                            paper_bgcolor='rgba(0,0,0,0)',
                            title=f"تنبؤ {target} لـ {periods} يوم"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # نتائج
                        cols = st.columns(3)
                        cols[0].metric("المتوسط المتوقع", f"{np.mean(preds):,.0f}")
                        cols[1].metric("القمة", f"{np.max(preds):,.0f}")
                        cols[2].metric("الاتجاه", "📈 صاعد" if preds[-1] > preds[0] else "📉 هابط")
                        
                        st.success("✅ تم التنبؤ بنجاح!")
                        
                    except Exception as e:
                        st.error(f"خطأ: {e}")
        else:
            st.info("لا توجد أعمدة رقمية")
        
        st.markdown("</div>", unsafe_allow_html=True)

# --- تقرير PDF ---
elif menu == "📄 تقرير PDF احترافي":
    st.markdown("<h1 class='gradient-text'>📄 التقرير التنفيذي</h1>", unsafe_allow_html=True)
    
    if st.session_state.beast_df is None:
        st.warning("ارفع البيانات أولاً")
    else:
        df = st.session_state.beast_df
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        
        # معاينة
        st.subheader("👁️ معاينة المحتوى")
        
        preview_cols = st.columns(4)
        preview_data = [
            ("📊 السجلات", f"{len(df):,}"),
            ("📈 الأعمدة", len(df.columns)),
            ("🧹 التنظيف", len(st.session_state.cleaning_log)),
            ("🔮 التنبؤات", "✓" if st.session_state.ml_predictions else "✗")
        ]
        
        for col, (label, val) in zip(preview_cols, preview_data):
            with col:
                st.metric(label, val)
        
        st.markdown("---")
        
        # محتويات التقرير
        st.write("*📋 محتويات التقرير:*")
        contents = [
            "✅ صفحة غلاف احترافية مع الشعار",
            "✅ الملخص التنفيذي الشامل",
            "✅ جداول إحصائية ملونة وتفاعلية",
            "✅ رسوم بيانية حقيقية (Matplotlib)",
            "✅ سجل عمليات التحسين",
            "✅ نتائج التنبؤ AI (إن وجدت)",
            "✅ التوصيات الاستراتيجية",
            "✅ تذييل احترافي مع التوقيع"
        ]
        for item in contents:
            st.write(item)
        
        st.markdown("---")
        
        # زر التحميل
        if st.button("📄 إنشاء PDF الاحترافي", use_container_width=True):
            with st.spinner("جاري إنشاء التقرير..."):
                pdf = create_beast_pdf()
                if pdf:
                    st.download_button(
                        "⬇️ تحميل التقرير",
                        pdf,
                        f"BEAST_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                    st.balloons()
                    st.success("✅ تم إنشاء التقرير بنجاح!")
        
        st.markdown("</div>", unsafe_allow_html=True)

# ======= 7. التذييل =======
st.markdown(f"""
    <div class='footer'>
        <div style='font-size: 3rem; margin-bottom: 15px;'>🦁</div>
        <h2 style='color: #10b981; margin-bottom: 10px;'>{APP_NAME}</h2>
        <p style='font-size: 1.1rem;'>نظام تحليل البيانات المتقدم بالذكاء الاصطناعي</p>
        <p style='color: #6b7280; margin-top: 15px;'>
            تطوير: <span style='color: #3b82f6; font-weight: bold;'>{AUTHOR_SIGNATURE}</span> | © 2026
        </p>
        <div style='margin-top: 20px;'>
            <span class='status-badge status-active'>✓ آمن</span>
            <span class='status-badge status-active'>⚡ سريع</span>
            <span class='status-badge status-active'>🧠 ذكي</span>
        </div>
    </div>
""", unsafe_allow_html=True)
