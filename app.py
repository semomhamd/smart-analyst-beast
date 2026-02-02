import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
from io import BytesIO

# 1. إعدادات الهوية الفخمة (MIA8444)
st.set_page_config(page_title="Smart Analyst Beast PRO", layout="wide", page_icon="🦁")

# تنسيق CSS فخم لإظهار الداشبورد بشكل احترافي
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    [data-testid="stSidebar"] { background-color: #161b22; }
    /* تنسيق الكروت (Metrics) زي ما في الصورة بالضبط */
    [data-testid="stMetricValue"] { font-size: 35px; color: #ffffff; }
    [data-testid="stMetricLabel"] { font-size: 18px; color: #888; }
    .stMetric { background-color: #1f2937; padding: 20px; border-radius: 12px; border-top: 4px solid #3b82f6; }
    </style>
    """, unsafe_allow_html=True)

# 2. مخزن البيانات الأساسي
if 'main_df' not in st.session_state:
    st.session_state['main_df'] = pd.DataFrame()

# --- السايد بار ---
with st.sidebar:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_container_width=True)
    
    st.markdown("<h2 style='text-align: center; color: white;'>Smart Analyst Beast</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>Signature: MIA8444</p>", unsafe_allow_html=True)
    st.write("---")
    
    menu = {
        "🏠 الرئيسية وبوابة البيانات": "الرئيسية",
        "📸 الرؤية الذكية (OCR)": "OCR",
        "🧼 منظف البيانات الذكي": "Clean",
        "📊 محرر الاكسل (Pro)": "Excel",
        "🧠 المحلل الذكي": "Analysis",
        "📈 التنبؤ المالي (AI)": "Forecast",
        "🖥️ داشبورد الإدارة": "Dashboard",
        "📄 تقرير PDF النهائي": "PDF"
    }
    
    choice = st.radio("انتقل بين الأدوات بدقة:", list(menu.keys()))
    st.write("---")
    st.success("System Status: Active 🟢")

# استدعاء البيانات
df = st.session_state['main_df']

# --- المحتوى ---

# 1. الرئيسية
if choice == "🏠 الرئيسية وبوابة البيانات":
    st.header("🏠 بوابة التحكم الرئيسية")
    col1, col2 = st.columns(2)
    with col1:
        up = st.file_uploader("ارفع ملفك (Excel/CSV)", type=['csv', 'xlsx'])
        if up:
            st.session_state['main_df'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
            st.success("تم الشحن بنجاح!")
            st.rerun()
    with col2:
        if st.button("🧬 توليد بيانات اختبار احترافية"):
            test_data = pd.DataFrame({
                'التاريخ': pd.date_range(start='2025-01-01', periods=50),
                'المنتج': np.random.choice(['موبايل', 'ساعة', 'لابتوب', 'سماعة'], 50),
                'المبيعات': np.random.randint(1000, 15000, 50),
                'الكمية': np.random.randint(1, 20, 50)
            })
            st.session_state['main_df'] = test_data
            st.rerun()

# 4. محرر الإكسل (SnaAyas Pro)
elif choice == "📊 محرر الاكسل (Pro)":
    st.header("📊 محرر الجداول الذكي (SnaAyas)")
    if df.empty:
        if 'empty_df' not in st.session_state:
            st.session_state['empty_df'] = pd.DataFrame("", index=range(10), columns=['المنتج', 'المبيعات', 'الكمية', 'ملاحظات'])
        work_df = st.session_state['empty_df']
    else: work_df = df

    edited_df = st.data_editor(work_df, num_rows="dynamic", use_container_width=True)
    
    if st.button("💾 حفظ واعتماد البيانات"):
        for col in ['المبيعات', 'الكمية']:
            if col in edited_df.columns:
                edited_df[col] = pd.to_numeric(edited_df[col], errors='coerce').fillna(0)
        st.session_state['main_df'] = edited_df
        st.success("تم الحفظ! اذهب الآن للداشبورد لرؤية النتائج.")

# 7. داشبورد الإدارة (النسخة الفخمة المظبوطة)
elif choice == "🖥️ داشبورد الإدارة":
    st.header("🖥️ Dashboard Performance (MIA8444)")
    
    if not df.empty:
        # التأكد من وجود عمود مبيعات للتحليل
        if 'المبيعات' in df.columns:
            # الصف الأول: الكروت الرئيسية (Metrics)
            c1, c2, c3 = st.columns(3)
            total_sales = df['المبيعات'].sum()
            avg_sales = df['المبيعات'].mean()
            total_ops = len(df)
            
            c1.metric("إجمالي المبيعات", f"{total_sales:,.0f}")
            c2.metric("عدد العمليات", f"{total_ops}")
            c3.metric("متوسط المبيعات", f"{avg_sales:,.2f}")
            
            st.write("---")
            
            # الصف الثاني: الرسوم البيانية الكبيرة
            col_chart1, col_chart2 = st.columns([1, 1])
            
            with col_chart1:
                # توزيع المبيعات (Donut Chart) كما في الصورة
                fig_pie = px.pie(df, names='المنتج' if 'المنتج' in df.columns else df.columns[0], 
                                 values='المبيعات', hole=0.5, 
                                 title="توزيع المبيعات حسب المنتج")
                fig_pie.update_layout(template="plotly_dark", showlegend=True)
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col_chart2:
                # أداء المنتجات (Bar Chart) ملون واحترافي
                fig_bar = px.bar(df, x='المنتج' if 'المنتج' in df.columns else df.columns[0], 
                                 y='المبيعات', color='المنتج' if 'المنتج' in df.columns else None,
                                 title="مقارنة أداء المنتجات المباشر",
                                 text_auto='.2s')
                fig_bar.update_layout(template="plotly_dark", xaxis_title="المنتج", yaxis_title="المبيعات")
                st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.warning("البيانات لا تحتوي على عمود 'المبيعات'. يرجى تسمية عمود الأرقام بـ 'المبيعات' ليعمل الداشبورد.")
    else:
        st.warning("ارفع بياناتك أو أدخلها في محرر الإكسل أولاً لتنشيط الداشبورد.")

# باقي الأقسام (مختصرة لضمان عمل الكود)
elif choice == "📸 الرؤية الذكية (OCR)": st.header("📸 AI Vision OCR")
elif choice == "🧼 منظف البيانات الذكي": st.header("🧼 Data Cleaner")
elif choice == "🧠 المحلل الذكي": st.header("🧠 Smart Analysis")
elif choice == "📈 التنبؤ المالي (AI)": st.header("📈 AI Forecast")
elif choice == "📄 تقرير PDF النهائي": st.header("📄 Export Report")

st.write("---")
st.markdown("<center>Smart Analyst Beast | Powered by MIA8444</center>", unsafe_allow_html=True)
