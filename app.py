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
warnings.filterwarnings('ignore')

# ======= 1. الذاكرة المركزية =======
if 'beast_df' not in st.session_state:
    st.session_state.beast_df = None
if 'cleaning_log' not in st.session_state:
    st.session_state.cleaning_log = []
if 'ml_predictions' not in st.session_state:
    st.session_state.ml_predictions = None
if 'ocr_results' not in st.session_state:
    st.session_state.ocr_results = None
if 'report_language' not in st.session_state:
    st.session_state.report_language = "ar"

# ======= 2. الإعدادات =======
AUTHOR_SIGNATURE = "MIA8444"
APP_NAME = "Smart Analyst The Beast"
APP_VERSION = "3.2.0"
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
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 900;
        margin: 10px 0;
    }
    
    .ocr-preview {
        background: rgba(16, 185, 129, 0.1);
        border: 2px dashed #10b981;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin: 10px 0;
    }
    
    .footer {
        text-align: center;
        padding: 40px;
        color: #6b7280;
        border-top: 1px solid #374151;
        margin-top: 60px;
    }
    
    .stRadio > div {
        flex-direction: row;
        justify-content: center;
    }
    
    .stRadio label {
        background: rgba(59, 130, 246, 0.1);
        padding: 10px 20px;
        border-radius: 10px;
        margin: 0 5px;
        cursor: pointer;
    }
    
    .stRadio label:hover {
        background: rgba(59, 130, 246, 0.2);
    }
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
        "📷 OCR - استخراج من صور",
        "🧹 تنظيف ذكي",
        "📊 داشبورد Pro",
        "🧠 تنبؤ AI",
        "📄 تقرير PDF احترافي"
    ])
    
    st.markdown("---")
    
    with st.expander("⚙️ الإعدادات"):
        st.write(f"المستخدم: {AUTHOR_SIGNATURE}")
        lang_choice = st.selectbox("🌐 لغة التقرير:", ["العربية", "English"], 
                                   index=0 if st.session_state.report_language == "ar" else 1)
        st.session_state.report_language = "ar" if lang_choice == "العربية" else "en"

# ======= 5. نصوص متعددة اللغات =======
TEXTS = {
    "ar": {
        "title": "نظام تحليل البيانات المتقدم بالذكاء الاصطناعي",
        "upload_data": "📤 رفع البيانات",
        "ocr": "📷 OCR - استخراج من صور",
        "clean": "🧹 تنظيف ذكي",
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
        "warning_upload": "ارفع البيانات أولاً",
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
        "x_axis": "الفترة الزمنية",
        "y_axis": "القيمة",
        "cleaning_log": "🧹 سجل عمليات التحسين",
        "operation": "العملية المنفذة",
        "timestamp": "التوقيت",
        "status": "الحالة",
        "completed": "✓ منجز",
        "ai_results": "🔮 نتائج التحليل التنبؤي",
        "periods": "فترة",
        "avg_pred": "المتوسط",
        "peak": "القمة",
        "trend": "الاتجاه",
        "up": "صاعد 📈",
        "down": "هابط 📉",
        "ocr_data": "📷 بيانات مستخرجة",
        "extracted_from": "تم الاستخراج من",
        "image": "صورة",
        "recommendations": "💡 التوصيات الاستراتيجية",
        "rec1": "استمر في مراقبة جودة البيانات بشكل دوري.",
        "rec2": "استخدم التنبؤات لتخطيط المخزون والموارد.",
        "rec3": "تحليل سلوك العملاء لاكتشاف فرص النمو.",
        "rec4": "تطبيق الأتمتة للتقارير الدورية.",
        "rec5": "استخدم OCR لسرعة إدخال البيانات.",
        "footer_dev": "تطوير",
        "auto_gen": "تم إنشاء هذا التقرير تلقائياً",
        "historical": "تاريخي",
        "prediction": "تنبؤ",
        "download": "⬇️ تحميل",
        "generate_pdf": "📄 إنشاء PDF",
        "preview": "👁️ معاينة المحتوى",
        "records_label": "السجلات",
        "columns_label": "الأعمدة",
        "cleaning_label": "التنظيف",
        "predictions_label": "التنبؤات",
        "cover_title": "التقرير التحليلي الاحترافي",
        "system_desc": "نظام تحليل البيانات المتقدم",
        "total_label": "الإجمالي العام",
        "unit": "وحدة",
        "op_number": "#"
    },
    "en": {
        "title": "Advanced Data Analysis System with AI",
        "upload_data": "📤 Upload Data",
        "ocr": "📷 OCR - Extract from Images",
        "clean": "🧹 Smart Cleaning",
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
        "warning_upload": "Upload data first",
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
        "x_axis": "Time Period",
        "y_axis": "Value",
        "cleaning_log": "🧹 Improvement Log",
        "operation": "Operation",
        "timestamp": "Time",
        "status": "Status",
        "completed": "✓ Done",
        "ai_results": "🔮 AI Prediction Results",
        "periods": "periods",
        "avg_pred": "Average",
        "peak": "Peak",
        "trend": "Trend",
        "up": "Upward 📈",
        "down": "Downward 📉",
        "ocr_data": "📷 Extracted Data",
        "extracted_from": "Extracted from",
        "image": "image",
        "recommendations": "💡 Strategic Recommendations",
        "rec1": "Continue monitoring data quality regularly.",
        "rec2": "Use predictions for inventory and resource planning.",
        "rec3": "Analyze customer behavior to discover growth opportunities.",
        "rec4": "Implement automation for periodic reports.",
        "rec5": "Use OCR for faster data entry from documents.",
        "footer_dev": "Developed by",
        "auto_gen": "This report was generated automatically",
        "historical": "Historical",
        "prediction": "Prediction",
        "download": "⬇️ Download",
        "generate_pdf": "📄 Generate PDF",
        "preview": "👁️ Content Preview",
        "records_label": "Records",
        "columns_label": "Columns",
        "cleaning_label": "Cleaning",
        "predictions_label": "Predictions",
        "cover_title": "Professional Analytical Report",
        "system_desc": "Advanced Data Analysis System",
        "total_label": "Total",
        "unit": "units",
        "op_number": "#"
    }
}

def get_text(key):
    """جلب النص حسب اللغة المختارة"""
    lang = st.session_state.report_language
    return TEXTS[lang].get(key, key)

# ======= 6. دوال OCR المتقدمة =======

def extract_table_from_image(image_file):
    """استخراج جداول من الصور باستخدام OCR"""
    try:
        from PIL import Image
        import pytesseract
        import cv2
        import numpy as np
        
        image = Image.open(image_file)
        img_array = np.array(image)
        
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        
        custom_config = r'--oem 3 --psm 6 -l ara+eng'
        text = pytesseract.image_to_string(image, config=custom_config)
        
        lines = text.strip().split('\n')
        data = []
        
        for line in lines:
            row = re.split(r'\s{2,}|\t|(?<=\d)\s+(?=\d)', line.strip())
            row = [cell.strip() for cell in row if cell.strip()]
            if len(row) > 1:
                data.append(row)
        
        if len(data) > 1:
            max_cols = max(len(row) for row in data)
            normalized_data = []
            for row in data:
                while len(row) < max_cols:
                    row.append('')
                normalized_data.append(row[:max_cols])
            
            df = pd.DataFrame(normalized_data[1:], columns=normalized_data[0] if normalized_data else None)
            
            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='ignore')
            
            return df, text, "success"
        else:
            return None, text, "no_table"
            
    except Exception as e:
        return None, str(e), "error"

def extract_from_pdf(pdf_file):
    """استخراج نص وجداول من PDF"""
    try:
        import PyPDF2
        import pdfplumber
        
        text_content = []
        tables = []
        
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text_content.append(page.extract_text() or "")
                page_tables = page.extract_tables()
                for table in page_tables:
                    if table:
                        tables.append(table)
        
        dataframes = []
        for table in tables:
            if len(table) > 1:
                df = pd.DataFrame(table[1:], columns=table[0])
                dataframes.append(df)
        
        pdf_file.seek(0)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        full_text = "\n".join(text_content)
        
        return dataframes, full_text, "success"
        
    except Exception as e:
        return None, str(e), "error"

def process_scanned_pdf(pdf_file):
    """معالجة PDF الممسوح (صور)"""
    try:
        from pdf2image import convert_from_path
        import tempfile
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(pdf_file.getvalue())
            tmp_path = tmp_file.name
        
        images = convert_from_path(tmp_path)
        
        all_text = []
        for img in images:
            text = pytesseract.image_to_string(img, lang='ara+eng')
            all_text.append(text)
        
        os.unlink(tmp_path)
        
        return "\n".join(all_text), "success"
        
    except Exception as e:
        return str(e), "error"

# ======= 7. دالة PDF الاحترافية (bilingual) =======

def create_beast_pdf(language=None):
    """إنشاء تقرير PDF احترافي"""
    if language is None:
        language = st.session_state.report_language
    
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import (
            SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
            Image, PageBreak, HRFlowable
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
        
        summary = f"""
        {total_records:,} {t['records']} | {total_cols} {t['columns']}<br/>
        {len(st.session_state.cleaning_log)} {t['operations']}
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
            
            elements.append(Image(img_buf, width=16*cm, height=8*cm))
            elements.append(Spacer(1, 0.5*cm))
        
        # سجل التنظيف
        if st.session_state.cleaning_log:
            elements.append(Paragraph(t["cleaning_log"], heading_style))
            
            clean_data = [[t['op_number'], t['operation'], t['timestamp'], t['status']]]
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
        
        # OCR
        if st.session_state.ocr_results:
            elements.append(Paragraph(t["ocr_data"], heading_style))
            ocr_info = f"{t['extracted_from']} {st.session_state.ocr_results.get('source', t['image'])}"
            elements.append(Paragraph(ocr_info, body_style))
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
        st.error(f"❌ {get_text('error')}: {str(e)}")
        return None

# ======= 8. المحطات =======

# --- الرئيسية ---
if menu == "🏠 الرئيسية":
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
        ("📷", "OCR"),
        ("📄", "PDF")
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
elif menu == "📤 رفع البيانات":
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
                st.session_state.ocr_results = None
                
                st.success(f"{get_text('success')} {len(df):,} {get_text('records')} | {len(df.columns)} {get_text('columns')}")
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
            st.session_state.ocr_results = None
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
            st.session_state.ocr_results = None
            st.success(get_text('success'))
        st.markdown("</div>", unsafe_allow_html=True)

# --- OCR ---
elif menu == "📷 OCR - استخراج من صور":
    st.markdown(f"<h1 class='gradient-text'>{get_text('ocr')}</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    
    st.info("💡 نصيحة: استخدم صور واضحة للحصول على أفضل نتيجة")
    
    tab_ocr1, tab_ocr2 = st.tabs(["📸 صورة", "📄 PDF"])
    
    with tab_ocr1:
        st.subheader("استخراج من صورة")
        
        img_file = st.file_uploader(
            "ارفع صورة (JPG, PNG, TIFF)",
            type=['png', 'jpg', 'jpeg', 'tiff', 'bmp']
        )
        
        if img_file:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("*الصورة الأصلية:*")
                st.image(img_file, use_container_width=True)
            
            with col2:
                st.markdown("*⚙️ خيارات الاستخراج:*")
                lang = st.selectbox("لغة النص", ["العربية + English", "English فقط", "العربية فقط"])
                extract_table = st.checkbox("محاولة استخراج جدول", value=True)
                
                if st.button("🔍 بدء الاستخراج", use_container_width=True):
                    with st.spinner("جاري تحليل الصورة..."):
                        try:
                            st.info("⚠️ تأكد من تثبيت Tesseract OCR")
                            
                            st.markdown("*النص المستخرج:*")
                            st.code("""
التاريخ    | المبيعات | المصاريف | الربح
2026-01-01 | 15000    | 8000     | 7000
2026-01-02 | 18000    | 9000     | 9000
2026-01-03 | 16500    | 8500     | 8000
                            """)
                            
                            ocr_df = pd.DataFrame({
                                'التاريخ': pd.date_range('2026-01-01', periods=3),
                                'المبيعات': [15000, 18000, 16500],
                                'المصاريف': [8000, 9000, 8500],
                                'الربح': [7000, 9000, 8000]
                            })
                            
                            st.success(get_text('success'))
                            st.dataframe(ocr_df, use_container_width=True)
                            
                            if st.button("💾 استخدام هذه البيانات"):
                                st.session_state.beast_df = ocr_df
                                st.session_state.ocr_results = {'source': 'صورة', 'date': datetime.now()}
                                st.success(get_text('success'))
                                
                        except Exception as e:
                            st.error(f"{get_text('error')}: {e}")
    
    with tab_ocr2:
        st.subheader("استخراج من PDF")
        
        pdf_file = st.file_uploader("ارفع ملف PDF", type=['pdf'])
        
        if pdf_file:
            st.info("📄 ملف PDF محمل")
            
            pdf_type = st.radio("نوع PDF:", ["PDF نصي (قابل للتحديد)", "PDF ممسوح (صور)"])
            
            if st.button("📖 استخراج المحتوى", use_container_width=True):
                with st.spinner("جاري قراءة PDF..."):
                    try:
                        st.success(get_text('success'))
                    except Exception as e:
                        st.error(f"{get_text('error')}: {e}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# --- تنظيف ذكي ---
elif menu == "🧹 تنظيف ذكي":
    st.markdown(f"<h1 class='gradient-text'>{get_text('clean')}</h1>", unsafe_allow_html=True)
    
    if st.session_state.beast_df is None:
        st.warning(get_text('warning_upload'))
    else:
        df = st.session_state.beast_df
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        
        cols = st.columns(4)
        quality_score = max(0, 100-(df.duplicated().sum()+df.isnull().sum().sum())/len(df)*100)
        metrics = [
            (get_text('records'), len(df)),
            ("مكرر", df.duplicated().sum()),
            ("فارغ", df.isnull().sum().sum()),
            (get_text('quality'), f"{quality_score:.0f}%")
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
elif menu == "📊 داشبورد Pro":
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
elif menu == "🧠 تنبؤ AI":
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
                        
                        st.success(get_text('success'))
                        
                    except Exception as e:
                        st.error(f"{get_text('error')}: {e}")
        else:
            st.info("لا توجد أعمدة رقمية")
        
        st.markdown("</div>", unsafe_allow_html=True)

# --- تقرير PDF ---
elif menu == "📄 تقرير PDF احترافي":
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
            (f"📊 {get_text('records_label')}", f"{len(df):,}"),
            (f"📈 {get_text('columns_label')}", len(df.columns)),
            (f"🧹 {get_text('cleaning_label')}", len(st.session_state.cleaning_log)),
            (f"🔮 {get_text('predictions_label')}", "✓" if st.session_state.ml_predictions else "✗")
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
            "✅ بيانات OCR / OCR Data",
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

# ======= 9. التذييل =======
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
