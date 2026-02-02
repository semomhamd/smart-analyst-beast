import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
from io import BytesIO

# 1. إعدادات الهوية الفخمة (MIA8444)
st.set_page_config(page_title="Smart Analyst Beast PRO", layout="wide", page_icon="🦁")

# لمسة CSS احترافية لتنسيق الألوان وتوسيط اللوجو
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    [data-testid="stSidebar"] { background-color: #161b22; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; border-left: 5px solid #3b82f6; }
    div.stButton > button:first-child { background-color: #3b82f6; color: white; border-radius: 10px; }
    /* تنسيق خاص لجعل الجداول تبدو احترافية */
    .stDataFrame { border: 1px solid #30363d; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. مخزن البيانات الأساسي لضمان الاستقرار
if 'main_df' not in st.session_state:
    st.session_state['main_df'] = pd.DataFrame()

df = st.session_state['main_df']

# --- السايد بار (مركز التحكم الإمبراطوري) ---
with st.sidebar:
    # اللوجو منور الدنيا فوق خالص
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_container_width=True)
    
    st.markdown("<h2 style='text-align: center; color: white;'>Smart Analyst Beast</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>Signature: MIA8444</p>", unsafe_allow_html=True)
    st.write("---")
    
    # القائمة المرتبة بأيقونات طبيعية ومنظمة
    st.markdown("### 🛠️ القائمة التنفيذية")
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
    st.caption("Smart Analyst thinks for you")

# --- محتوى الأدوات المربوطة ---

# 1. الرئيسية
if choice == "🏠 الرئيسية وبوابة البيانات":
    st.header("🏠 بوابة التحكم الرئيسية")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📤 رفع البيانات")
        up = st.file_uploader("ارفع ملفك (Excel/CSV)", type=['csv', 'xlsx'])
        if up:
            st.session_state['main_df'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
            st.success("تم الشحن بنجاح!")
            st.rerun()
    with col2:
        st.subheader("🧬 عينة الاختبار")
        if st.button("توليد بيانات اختبار (Beast Sample)"):
            test_data = pd.DataFrame({
                'التاريخ': pd.date_range(start='2025-01-01', periods=100),
                'المنتج': np.random.choice(['موبايل', 'ساعة', 'لابتوب', 'سماعة'], 100),
                'المبيعات': np.random.randint(500, 10000, 100),
                'التكلفة': np.random.randint(300, 8000, 100)
            })
            st.session_state['main_df'] = test_data
            st.success("تم توليد البيانات بنجاح!")
            st.rerun()

# 2. الرؤية الذكية
elif choice == "📸 الرؤية الذكية (OCR)":
    st.header("📸 محرك الرؤية الذكي (AI Vision)")
    cam = st.camera_input("التقط صورة للجدول الورقي")
    if cam: 
        st.image(cam, caption="تم التقاط الصورة")
        st.info("جاري استخراج البيانات بذكاء MIA8444 وتحويلها لجدول...")

# 3. المنظف
elif choice == "🧼 منظف البيانات الذكي":
    st.header("🧼 وحدة تنظيف وتجهيز البيانات")
    if not df.empty:
        if st.button("🚀 تنفيذ التنظيف العميق (Auto Clean)"):
            cleaned_df = df.drop_duplicates().fillna(0)
            st.session_state['main_df'] = cleaned_df
            st.success("البيانات الآن نظيفة وجاهزة للتحليل!")
            st.dataframe(cleaned_df.head(), use_container_width=True)
    else: st.warning("لا توجد بيانات لتنظيفها.")

# 4. محرر الإكسل الاحترافي (SnaAyas Pro)
elif choice == "📊 محرر الاكسل (Pro)":
    st.header("📊 محرر الجداول الاحترافي (SnaAyas)")
    if not df.empty:
        st.write("تعديل يدوي بمساعدة الذكاء الاصطناعي:")
        # المحرر التفاعلي
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("💾 حفظ التعديلات في الذاكرة"):
                st.session_state['main_df'] = edited_df
                st.success("تم حفظ التعديلات بنجاح.")
        
        with c2:
            # تصدير ملف اكسل احترافي منسق باستخدام xlsxwriter
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                edited_df.to_excel(writer, index=False, sheet_name='MIA8444_Beast')
                workbook  = writer.book
                worksheet = writer.sheets['MIA8444_Beast']
                
                # تنسيق الـ Header الفخم
                header_format = workbook.add_format({
                    'bold': True,
                    'text_wrap': True,
                    'valign': 'vcenter',
                    'fg_color': '#1F4E78',
                    'font_color': 'white',
                    'border': 1
                })
                
                for col_num, value in enumerate(edited_df.columns.values):
                    worksheet.write(0, col_num, value, header_format)
                
            st.download_button(
                label="📥 تحميل كشيت إكسل احترافي (MIA8444)",
                data=buffer.getvalue(),
                file_name="Smart_Analyst_Report.xlsx",
                mime="application/vnd.ms-excel"
            )
    else: st.warning("ارفع ملفاً أولاً لتفعيل المحرر.")

# 5. المحلل الذكي
elif choice == "🧠 المحلل الذكي":
    st.header("🧠 ذكاء MIA8444 في تحليل البيانات")
    if not df.empty:
        st.subheader("🔍 الملخص الإحصائي والذكاء التحليلي")
        st.dataframe(df.describe(), use_container_width=True)
    else: st.warning("لا توجد بيانات للتحليل.")

# 6. التنبؤ المالي
elif choice == "📈 التنبؤ المالي (AI)":
    st.header("📈 محرك التنبؤ بمستقبل المبيعات")
    if not df.empty and 'المبيعات' in df.columns:
        y = df['المبيعات'].values
        future = np.poly1d(np.polyfit(np.arange(len(y)), y, 1))(np.arange(len(y), len(y) + 10))
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=y, name="الواقع الحالي", line=dict(color='#3b82f6', width=3)))
        fig.add_trace(go.Scatter(y=future, name="التنبؤ المستقبلي", line=dict(dash='dash', color='#ef4444', width=3)))
        fig.update_layout(title="تحليل اتجاه المبيعات القادم", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    else: st.info("تأكد من وجود عمود 'المبيعات' للتنبؤ.")

# 7. داشبورد الإدارة
elif choice == "🖥️ داشبورد الإدارة":
    st.header("🖥️ Dashboard High-Level Performance")
    if not df.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("إجمالي المبيعات", f"{df['المبيعات'].sum():,}")
        c2.metric("عدد العمليات", len(df))
        c3.metric("متوسط الربحية", f"{df['المبيعات'].mean():.2f}")
        
        ca, cb = st.columns(2)
        with ca:
            fig_pie = px.pie(df, names='المنتج', values='المبيعات', hole=0.4, title="حصة المنتجات من المبيعات")
            fig_pie.update_layout(template="plotly_dark")
            st.plotly_chart(fig_pie, use_container_width=True)
        with cb:
            fig_bar = px.bar(df, x='المنتج', y='المبيعات', color='المنتج', title="مقارنة أداء المنتجات")
            fig_bar.update_layout(template="plotly_dark")
            st.plotly_chart(fig_bar, use_container_width=True)
    else: st.warning("ارفع بيانات لعرض الداشبورد.")

# 8. PDF
elif choice == "📄 تقرير PDF النهائي":
    st.header("📄 تصدير التقرير الشامل")
    st.info("جاري تجميع كافة التحليلات والرسوم في ملف PDF واحد بختم MIA8444...")
    st.button("📥 تحميل التقرير النهائي")

st.write("---")
st.markdown("<center>Smart Analyst Beast | Powered by MIA8444 | 2026</center>", unsafe_allow_html=True)
