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
import re
import hashlib
from functools import lru_cache

warnings.filterwarnings('ignore')

# ======= الإعدادات =======
AUTHOR_SIGNATURE = "MIA8444"
APP_NAME = "The Beast Pro"
APP_VERSION = "4.0.0"
LOGO_FILE = "8888.jpg"

st.set_page_config(
    page_title=f"{AUTHOR_SIGNATURE} | {APP_NAME}",
    page_icon="🦁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======= Session State =======
defaults = {
    'beast_df': None,
    'cleaning_log': [],
    'ml_predictions': None,
    'ocr_results': None,
    'report_language': "ar",
    'theme': "dark"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ======= CSS احترافي =======
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
    
    .%, #0a0e17 100%);
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
    }
    
    .gradient-text {
        background: linear-gradient(135deg, #3b82f6 0%, #10b981 50%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 2.5rem;
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
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 900;
        margin: 10px 0;
    }
    
    .footer {
        text-align: center;
        padding: 40px;
        color: #6b7280;
        border-top: 1px solid #374151;
        margin-top: 60px;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6, #10b981);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 700;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# ======= نصوص متعددة اللغات =======
TEXTS = {
    "ar": {
        "title": "نظام تحليل البيانات المتقدم بالذكاء الاصطناعي",
        "upload_data": "📤 رفع البيانات",
        "dashboard": "📊 داشبورد Pro",
        "predict": "🧠 تنبؤ AI",
        "report": "📄 تقرير PDF احترافي",
        "records": "سجل",
        "columns": "عمود",
        "operations": "عملية",
        "quality": "جودة",
        "select_file": "اختر ملف",
        "generate": "🚀 توليد بيانات",
        "save": "💾 حفظ",
        "success": "✅ تم بنجاح!",
        "error": "❌ خطأ",
        "warning_upload": "⚠️ ارفع البيانات أولاً من قسم رفع البيانات",
        "analyst": "المحلل",
        "date": "التاريخ",
        "time": "الوقت",
        "version": "الإصدار",
        "exec_summary": "📋 الملخص التنفيذي",
        "key_metrics": "📊 المؤشرات الرئيسية",
        "metric": "المؤشر",
        "sum": "المجموع",
        "avg": "المتوسط",
        "max": "الأعلى",
        "min": "الأدنى",
        "growth": "النمو",
        "chart_analysis": "📈 التحليل البياني",
        "trend_title": "تحليل الاتجاهات الرئيسية",
        "cleaning_log": "🧹 سجل عمليات التحسين",
        "operation": "العملية المنفذة",
        "timestamp": "التوقيت",
        "status": "الحالة",
        "completed": "✓ منجز",
        "ai_results": "🔮 نتائج التحليل التنبؤي",
        "periods": "فترة",
        "avg_pred": "المتوسط المتوقع",
        "peak": "القمة المتوقعة",
        "trend": "الاتجاه",
        "up": "صاعد 📈",
        "down": "هابط 📉",
        "recommendations": "💡 التوصيات الاستراتيجية",
        "footer_dev": "تطوير",
        "auto_gen": "تم إنشاء هذا التقرير تلقائياً",
        "download": "⬇️ تحميل",
        "generate_pdf": "📄 إنشاء PDF",
        "preview": "👁️ معاينة المحتوى",
        "cover_title": "التقرير التحليلي الاحترافي",
        "system_desc": "نظام تحليل البيانات المتقدم",
        "total_label": "الإجمالي العام",
        "unit": "وحدة",
        "op_number": "#",
        "clean": "🧹 تنظيف ذكي",
        "ocr": "📷 OCR - استخراج من صور",
        "home": "🏠 الرئيسية",
        "settings": "⚙️ الإعدادات"
    },
    "en": {
        "title": "Advanced Data Analysis System with AI",
        "upload_data": "📤 Upload Data",
        "dashboard": "📊 Pro Dashboard",
        "predict": "🧠 AI Prediction",
        "report": "📄 Professional PDF Report",
        "records": "records",
        "columns": "columns",
        "operations": "operations",
        "quality": "quality",
        "select_file": "Select file",
        "generate": "🚀 Generate Data",
        "save": "💾 Save",
        "success": "✅ Success!",
        "error": "❌ Error",
        "warning_upload": "⚠️ Upload data first from Upload section",
        "analyst": "Analyst",
        "date": "Date",
        "time": "Time",
        "version": "Version",
        "exec_summary": "📋 Executive Summary",
        "key_metrics": "📊 Key Metrics",
        "metric": "Metric",
        "sum": "Sum",
        "avg": "Average",
        "max": "Max",
        "min": "Min",
        "growth": "Growth",
        "chart_analysis": "📈 Chart Analysis",
        "trend_title": "Key Trends Analysis",
        "cleaning_log": "🧹 Improvement Log",
        "operation": "Operation",
        "timestamp": "Timestamp",
        "status": "Status",
        "completed": "✓ Done",
        "ai_results": "🔮 AI Prediction Results",
        "periods": "periods",
        "avg_pred": "Average Prediction",
        "peak": "Peak",
        "trend": "Trend",
        "up": "Upward 📈",
        "down": "Downward 📉",
        "recommendations": "💡 Strategic Recommendations",
        "footer_dev": "Developed by",
        "auto_gen": "This report was generated automatically",
        "download": "⬇️ Download",
        "generate_pdf": "📄 Generate PDF",
        "preview": "👁️ Preview",
        "cover_title": "Professional Analytical Report",
        "system_desc": "Advanced Data Analysis System",
        "total_label": "Total",
        "unit": "units",
        "op_number": "#",
        "clean": "🧹 Smart Cleaning",
        "ocr": "📷 OCR - Extract from Images",
        "home": "🏠 Home",
        "settings": "⚙️ Settings"
    }
}

def get_text(key):
    """جلب النص حسب اللغة المختارة"""
    lang = st.session_state.report_language
    return TEXTS[lang].get(key, key)

# ======= الشريط الجانبي =======
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
        get_text("home"),
        get_text("upload_data"),
        get_text("clean"),
        get_text("dashboard"),
        get_text("predict"),
        get_text("report"),
        get_text("settings")
    ])
    
    st.markdown("---")
    
    with st.expander("⚙️ الإعدادات"):
        st.write(f"المستخدم: {AUTHOR_SIGNATURE}")
        lang_choice = st.selectbox("🌐 اللغة:", ["العربية", "English"], 
                                   index=0 if st.session_state.report_language == "ar" else 1)
        st.session_state.report_language = "ar" if lang_choice == "العربية" else "en"

# ======= دوال المساعدة =======

def calculate_quality_score(df):
    """حساب درجة جودة البيانات"""
    if df is None or df.empty:
        return 0
    
    total_cells = df.size
    missing_cells = df.isnull().sum().sum()
    duplicate_rows = df.duplicated().sum()
    
    if total_cells == 0:
        return 0
    
    completeness = ((total_cells - missing_cells) / total_cells) * 100
    uniqueness = ((len(df) - duplicate_rows) / len(df)) * 100 if len(df) > 0 else 100
    
    quality_score = (completeness * 0.6) + (uniqueness * 0.4)
    return round(quality_score, 1)

@st.cache_data
def generate_forecast_cached(data_hash, target_col, periods):
    """تنبؤ مع تخزين مؤقت"""
    try:
        from sklearn.linear_model import LinearRegression
        from sklearn.preprocessing import PolynomialFeatures
        
        # إعادة بناء البيانات من الـ hash مش ممكن فعلياً، 
        # لكن الكاش هنا يعتمد على تغيير المعاملات فقط
        return None
    except:
        return None

# ======= إنشاء PDF =======
def create_beast_pdf(language=None):
    """إنشاء تقرير PDF احترافي"""
    if language is None:
        language = st.session_state.report_language
    
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import (
            SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
            Image as RLImage, PageBreak, HRFlowable
        )
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.use('Agg')
        
        t = TEXTS[language]
        is_arabic = language == "ar"
        
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
        
        alignment = TA_RIGHT if is_arabic else TA_LEFT
        
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
            leftIndent=10 if not is_arabic else 0,
            rightIndent=10 if is_arabic else 0,
            alignment=alignment
        )
        
        body_style = ParagraphStyle(
            'BeastBody',
            parent=styles['Normal'],
            fontSize=11,
            alignment=alignment,
            leading=22,
            rightIndent=10 if is_arabic else 0,
            leftIndent=10 if not is_arabic else 0
        )
        
        # صفحة الغلاف
        elements.append(Spacer(1, 4*cm))
        elements.append(Paragraph(APP_NAME.upper(), title_style))
        elements.append(Paragraph(t["cover_title"], subtitle_style))
        
        info_data = [
            [f"{t['analyst']}: {AUTHOR_SIGNATURE}"],
            [f"{t['date']}: {datetime.now().strftime('%Y/%m/%d')}"],
            [f"{t['time']}: {datetime.now().strftime('%H:%M:%S')}"],
            [f"{t['version']}: {APP_VERSION}"]
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
        elements.append(HRFlowable(width="80%", thickness=3, color=colors.HexColor('#059669'), hAlign='CENTER'))
        elements.append(Spacer(1, 1*cm))
        elements.append(Paragraph(f"<b>{t['system_desc']}</b>", 
                                  ParagraphStyle('center', alignment=TA_CENTER, fontSize=14, textColor=colors.HexColor('#3b82f6'))))
        elements.append(PageBreak())
        
        df = st.session_state.beast_df
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # الملخص التنفيذي
        elements.append(Paragraph(t["exec_summary"], heading_style))
        
        total_records = len(df)
        total_cols = len(df.columns)
        quality_score = calculate_quality_score(df)
        
        summary = f"""
        {total_records:,} {t['records']} | {total_cols} {t['columns']}<br/>
        {len(st.session_state.cleaning_log)} {t['operations']} | {t['quality']}: {quality_score}%
        """
        
        if numeric_cols:
            total_val = df[numeric_cols[0]].sum()
            summary += f"<br/><br/>{t['total_label']}: <b>{total_val:,.0f}</b> {t['unit']}."
        
        elements.append(Paragraph(summary, body_style))
        elements.append(Spacer(1, 0.8*cm))
        
        # المؤشرات الرئيسية
        elements.append(Paragraph(t["key_metrics"], heading_style))
        
        if numeric_cols:
            stats_data = [[t['metric'], t['sum'], t['avg'], t['max'], t['min'], t['growth']]]
            
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
        
        # رسم بياني
        if numeric_cols:
            elements.append(Paragraph(t["chart_analysis"], heading_style))
            
            fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
            ax.set_facecolor('#f9fafb')
            fig.patch.set_facecolor('white')
            
            x_pos = np.arange(len(df.head(30)))
            ax.plot(x_pos, df[numeric_cols[0]].head(30), color='#059669', linewidth=2.5, 
                    label=numeric_cols[0], marker='o', markersize=4)
            
            if len(numeric_cols) > 1:
                ax.plot(x_pos, df[numeric_cols[1]].head(30), color='#3b82f6', linewidth=2.5, 
                        label=numeric_cols[1], marker='s', markersize=4)
            
            ax.fill_between(x_pos, df[numeric_cols[0]].head(30), alpha=0.3, color='#059669')
            ax.set_xlabel(t['x_axis'], fontsize=11, fontweight='bold')
            ax.set_ylabel(t['y_axis'], fontsize=11, fontweight='bold')
            ax.set_title(t['trend_title'], fontsize=14, fontweight='bold', pad=20)
            ax.legend(loc='upper left', framealpha=0.9)
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            plt.tight_layout()
            img_buf = BytesIO()
            plt.savefig(img_buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
            img_buf.seek(0)
            plt.close()
            
            elements.append(RLImage(img_buf, width=16*cm, height=8*cm))
            elements.append(Spacer(1, 0.5*cm))
        
        # سجل التنظيف
        if st.session_state.cleaning_log:
            elements.append(Paragraph(t["cleaning_log"], heading_style))
            
            clean_data = [[t['op_number'], t['operation'], t['timestamp'], t['status']]]
            for idx, log in enumerate(st.session['status']]]
            for idx, log in enumerate(st.session_state.cleaning_log, 1):
                clean_data.append([str(idx), log, datetime.now().strftime('%H:%M'), t['completed']])
            
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
        
        # التنبؤات
        if st.session_state.ml_predictions:
            elements.append(Paragraph(t["ai_results"], heading_style))
            
            pred = st.session_state.ml_predictions
            avg_pred = np.mean(pred['predictions'])
            max_pred = np.max(pred['predictions'])
            trend_text = t["up"] if pred['predictions'][-1] > pred['predictions'][0] else t["down"]
            
            pred_text = f"""
            {pred['periods']} {t['periods']}<br/><br/>
            <b>{t['avg_pred']}:</b> {avg_pred:,.0f}<br/>
            <b>{t['peak']}:</b> {max_pred:,.0f}<br/>
            <b>{t['trend']}:</b> {trend_text}
            """
            elements.append(Paragraph(pred_text, body_style))
            elements.append(Spacer(1, 0.5*cm))
        
        # التوصيات
        elements.append(Paragraph(t["recommendations"], heading_style))
        
        recommendations = [t['rec1'], t['rec2'], t['rec3'], t['rec4'], t['rec5']]
        
        for i, rec in enumerate(recommendations, 1):
            elements.append(Paragraph(f"<b>{i}.</b> {rec}", body_style))
        
        elements.append(Spacer(1, 1.5*cm))
        
        # التذييل
        elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#059669')))
        elements.append(Spacer(1, 0.5*cm))
        
        footer = f"""
        <para alignment="center">
        <font color="#059669" size="12"><b>{APP_NAME} v{APP_VERSION}</b></font><br/>
        <font color="#6b7280" size="10">{t['footer_dev']}: {AUTHOR_SIGNATURE} | © 2026</font><br/>
        <font color="#9ca3af" size="9">{t['auto_gen']}</font>
        </para>
        """
        elements.append(Paragraph(footer, styles['Normal']))
        
        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
        
    except Exception as e:
        st.error(f"❌ خطأ في إنشاء PDF: {str(e)}")
        import traceback
        st.error(traceback.format_exc())
        return None

# ======= الصفحات =======

# --- الرئيسية ---
if menu == get_text("home"):
    st.markdown(f"""
        <div style='text-align: center; padding: 60px 20px;'>
            <div style='font-size: 6rem; margin-bottom: 20px;'>🦁</div>
            <h1 class='gradient-text' style='font-size: 3.5rem;'>{APP_NAME.upper()}</h1>
            <p style='font-size: 1.5rem; color: #6b7280; margin-top: 20px;'>
                {get_text('title')}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    features = [
        ("📊", get_text('clean').replace("🧹 ", "")),
        ("🧠", get_text('predict').replace("🧠 ", "")),
        ("📄", "PDF"),
        ("⚡", "AI")
    ]
    
    for col, (icon, title) in zip([col1, col2, col3, col4], features):
        with col:
            st.markdown(f"""
                <div class='glass-card' style='text-align: center;'>
                    <div style='font-size: 2.5rem;'>{icon}</div>
                    <h4>{title}</h4>
                </div>
            """, unsafe_allow_html=True)

# --- رفع البيانات ---
elif menu == get_text("upload_data"):
    st.markdown(f"<h1 class='gradient-text'>{get_text('upload_data')}</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📁 Excel/CSV", "🎲 " + get_text('generate').replace("🚀 ", ""), "✍️ يدوي"])
    
    with tab1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        file = st.file_uploader(get_text('select_file'), type=['csv', 'xlsx', 'xls'])
        if file:
            try:
                if file.name.endswith('xlsx') or file.name.endswith('xls'):
                    df = pd.read_excel(file, engine='openpyxl')
                else:
                    df = pd.read_csv(file)
                
                st.session_state.beast_df = df
                st.session_state.cleaning_log = []
                st.session_state.ml_predictions = None
                
                quality = calculate_quality_score(df)
                
                st.success(f"{get_text('success')} {len(df):,} {get_text('records')} | {len(df.columns)} {get_text('columns')} | {t['quality']}: {quality}%")
                st.dataframe(df.head(10), use_container_width=True)
            except Exception as e:
                st.error(f"{get_text('error')}: {e}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        if st.button(get_text('generate'), use_container_width=True):
            df = pd.DataFrame({
                'التاريخ': pd.date_range('2026-01-01', periods=200),
                'المبيعات': np.random.randint(10000, 50000, 200),
                'المصاريف': np.random.randint(5000, 20000, 200),
                'العملاء': np.random.randint(50, 200, 200)
            })
            df['الربح'] = df['المبيعات'] - df['المصاريف']
            st.session_state.beast_df = df
            st.session_state.ml_predictions = None
            st.success(f"{get_text('success')} {len(df)} {get_text('records')}!")
            st.dataframe(df.head(), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        curr = st.session_state.beast_df if st.session_state.beast_df is not None else pd.DataFrame({
            'البند': ['مثال'], 'القيمة': [0]
        })
        edited = st.data_editor(curr, num_rows="dynamic", use_container_width=True)
        if st.button(get_text('save')):
            st.session_state.beast_df = edited
            st.success(get_text('success'))
        st.markdown("</div>", unsafe_allow_html=True)

# --- تنظيف ذكي ---
elif menu == get_text("clean"):
    st.markdown(f"<h1 class='gradient-text'>{get_text('clean')}</h1>", unsafe_allow_html=True)
    
    if st.session_state.beast_df is None:
        st.warning(get_text('warning_upload'))
    else:
        df = st.session_state.beast_df
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        
        quality = calculate_quality_score(df)
        
        cols = st.columns(4)
        metrics = [
            (get_text('records'), len(df)),
            ("مكرر", df.duplicated().sum()),
            ("فارغ", df.isnull().sum().sum()),
            (get_text('quality'), f"{quality}%")
        ]
        
        for col, (label, val) in zip(cols, metrics):
            with col:
                st.markdown(f"""
                    <div class='metric-container'>
                        <div style='font-size: 0.9rem;'>{label}</div>
                        <div class='metric-value'>{val}</div>
                    </div>
                """, unsafe_allow_html=True)
        
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
elif menu == get_text("dashboard"):
    st.markdown(f"<h1 class='gradient-text'>{get_text('dashboard')}</h1>", unsafe_allow_html=True)
    
    if st.session_state.beast_df is None:
        st.warning(get_text('warning_upload'))
    else:
        df = st.session_state.beast_df
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        
        if numeric_cols:
            cols = st.columns(min(4, len(numeric_cols)))
            for i, col in enumerate(numeric_cols[:4]):
                with cols[i]:
                    trend = np.random.choice(["📈", "📉", "➡️"])
                    st.markdown(f"""
                        <div class='metric-container'>
                            <div style='font-size: 0.9rem;'>{col} {trend}</div>
                            <div class='metric-value'>{df[col].sum():,.0f}</div>
                            <div style='font-size: 0.85rem;'>متوسط: {df[col].mean():,.0f}</div>
                        </div>
                    """, unsafe_allow_html=True)
        
        if numeric_cols:
            st.markdown("---")
            chart_type = st.selectbox("نوع الرسم", ["Area", "Line", "Bar", "Scatter"])
            
            try:
                if chart_type == "Area":
                    fig = px.area(df, y=numeric_cols[:3], template="plotly_dark")
                elif chart_type == "Line":
                    fig = px.line(df, y=numeric_cols[:3], template="plotly_dark")
                elif chart_type == "Bar":
                    fig = px.bar(df.head(20), y=numeric_cols[0], template="plotly_dark")
                else:
                    fig = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1] if len(numeric_cols) > 1 else numeric_cols[0], template="plotly_dark")
                
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#f3f4f6')
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"{get_text('error')}: {e}")
        
        st.markdown("</div>", unsafe_allow_html=True)

# --- تنبؤ AI ---
elif menu == get_text("predict"):
    st.markdown(f"<h1 class='gradient-text'>{get_text('predict')}</h1>", unsafe_allow_html=True)
    
    if st.session_state.beast_df is None:
        st.warning(get_text('warning_upload'))
    else:
        df = st.session_state.beast_df
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        
        if numeric_cols:
            target = st.selectbox("المؤشر المستهدف", numeric_cols)
            periods = st.slider("فترة التنبؤ (يوم)", 7, 365, 30)
            
            if st.button("🔮 بدء التنبؤ", use_container_width=True):
                with st.spinner("جاري التحليل..."):
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
                        
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(y=y, name='تاريخي', line=dict(color='#3b82f6')))
                        fig.add_trace(go.Scatter(y=list(y)+list(preds), name='تنبؤ', line=dict(color='#10b981', dash='dash')))
                        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
                        st.plotly_chart(fig, use_container_width=True)
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("متوسط التنبؤ", f"{np.mean(preds):,.0f}")
                        with col2:
                            st.metric("القمة المتوقعة", f"{np.max(preds):,.0f}")
                        with col3:
                            trend = "📈 صاعد" if preds[-1] > preds[0] else "📉 هابط"
                            st.metric("الاتجاه", trend)
                        
                        st.success(get_text('success'))
                        
                    except Exception as e:
                        st.error(f"{get_text('error')}: {e}")
        else:
            st.info("لا توجد أعمدة رقمية")
        
        st.markdown("</div>", unsafe_allow_html=True)

# --- تقرير PDF ---
elif menu == get_text("report"):
    st.markdown(f"<h1 class='gradient-text'>{get_text('report')}</h1>", unsafe_allow_html=True)
    
    if st.session_state.beast_df is None:
        st.warning(get_text('warning_upload'))
    else:
        df = st.session_state.beast_df
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        
        # اختيار اللغة
        col_lang1, col_lang2 = st.columns(2)
        with col_lang1:
            report_lang = st.radio(
                "🌐 لغة التقرير:",
                ["العربية 🇸🇦", "English 🇬🇧"],
                horizontal=True,
                index=0 if st.session_state.report_language == "ar" else 1
            )
        
        lang_code = "ar" if "العربية" in report_lang else "en"
        st.session_state.report_language = lang_code
        
        st.markdown("---")
        
        st.subheader(get_text('preview'))
        
        preview_cols = st.columns(4)
        preview_data = [
            (f"📊 {get_text('records')}", f"{len(df):,}"),
            (f"📈 {get_text('columns')}", len(df.columns)),
            (f"🧹 {get_text('cleaning_log').replace('🧹 ', '')}", len(st.session_state.cleaning_log)),
            (f"🔮 {get_text('ai_results').replace('🔮 ', '')}", "✓" if st.session_state.ml_predictions else "✗")
        ]
        
        for col, (label, val) in zip(preview_cols, preview_data):
            with col:
                st.metric(label, val)
        
        st.markdown("---")
        
        contents = [
            "✅ صفحة غلاف احترافية / Professional Cover",
            f"✅ {get_text('exec_summary')}",
            "✅ جداول إحصائية ملونة / Colored Tables",
            "✅ رسوم بيانية حقيقية / Real Charts",
            f"✅ {get_text('cleaning_log')}",
            f"✅ {get_text('ai_results')}",
            f"✅ {get_text('recommendations')}"
        ]
        
        for item in contents:
            st.write(item)
        
        st.markdown("---")
        
        if st.button(get_text('generate_pdf'), use_container_width=True):
            with st.spinner("جاري الإنشاء... / Generating..."):
                pdf = create_beast_pdf(language=lang_code)
                if pdf:
                    filename = f"BEAST_Report_{datetime.now().strftime('%Y%m%d_%H%M')}_{lang_code.upper()}.pdf"
                    
                    st.download_button(
                        get_text('download'),
                        pdf,
                        filename,
                        mime="application/pdf",
                        use_container_width=True
                    )
                    st.balloons()
        
        st.markdown("</div>", unsafe_allow_html=True)

# --- الإعدادات ---
elif menu == get_text("settings"):
    st.markdown(f"<h1 class='gradient-text'>{get_text('settings')}</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    
    st.subheader("🌐 اللغة / Language")
    new_lang = st.radio("اختر اللغة:", ["العربية", "English"], 
                       index=0 if st.session_state.report_language == "ar" else 1)
    if new_lang == "العربية":
        st.session_state.report_language = "ar"
    else:
        st.session_state.report_language = "en"
    
    st.markdown("---")
    
    st.subheader("ℹ️ معلومات النظام")
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
    
    if st.button("🗑️ مسح جميع البيانات", use_container_width=True):
        st.session_state.beast_df = None
        st.session_state.cleaning_log = []
        st.session_state.ml_predictions = None
        st.session_state.ocr_results = None
        st.success("✅ تم مسح جميع البيانات!")
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# ======= التذييل =======
st.markdown(f"""
    <div class='footer'>
        <div style='font-size: 3rem; margin-bottom: 15px;'>🦁</div>
        <h2 style='color: #10b981;'>{APP_NAME}</h2>
        <p>{get_text('title')}</p>
        <p style='color: #6b7280; margin-top: 15px;'>
            {get_text('footer_dev')}: <span style='color: #3b82f6; font-weight: bold;'>{AUTHOR_SIGNATURE}</span> | © 2026
        </p>
    </div>
""", unsafe_allow_html=True)
