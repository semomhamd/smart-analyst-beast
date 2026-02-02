import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
from io import BytesIO

# 1. إعدادات الهوية الفخمة (MIA8444)
st.set_page_config(page_title="Smart Analyst Beast PRO", layout="wide", page_icon="🦁")

# لمسة CSS احترافية لتنسيق الألوان
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    [data-testid="stSidebar"] { background-color: #161b22; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; border-left: 5px solid #3b82f6; }
    div.stButton > button:first-child { background-color: #3b82f6; color: white; border-radius: 10px; }
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

# استدعاء البيانات الحالية
df = st.session_state['main_df']

# --- الأقسام ---

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
        if st.button("توليد بيانات اختبار"):
            test_data = pd.DataFrame({
                'التاريخ': pd.date_range(start='2025-01-01', periods=10),
                'المنتج': ['موبايل', 'ساعة', 'لابتوب']*3 + ['سماعة'],
                'المبيعات': [1200, 800, 5000, 1500, 900, 4800, 1100, 700, 5200, 1600],
                'التكلفة': [1000, 600, 4000, 1200, 700, 3800, 900, 500, 4200, 1300]
            })
            st.session_state['main_df'] = test_data
            st.success("تم توليد البيانات!")
            st.rerun()

# 4. محرر الإكسل الاحترافي (SnaAyas Pro) - الميزة اللي طلبتها
elif choice == "📊 محرر الاكسل (Pro)":
    st.header("📊 محرر الجداول الذكي (SnaAyas)")
    
    # لو مفيش بيانات مرفوعة، بنعمل شيت فاضي "إكسل عادي"
    if df.empty:
        st.info("💡 مفيش بيانات مرفوعة؟ ولا يهمك، افتح شيت فاضي وابدأ شغل:")
        if 'empty_df' not in st.session_state:
            # بنعمل جدول فاضي 10 صفوف في 5 أعمدة
            st.session_state['empty_df'] = pd.DataFrame(
                "", 
                index=range(10), 
                columns=['المنتج', 'الكمية', 'سعر الوحدة', 'المبيعات', 'ملاحظات']
            )
        work_df = st.session_state['empty_df']
    else:
        work_df = df

    st.write("📝 *ادخل بياناتك هنا (كأنك في إكسل):*")
    # محرر تفاعلي يسمح بإضافة صفوف وأعمدة وتعديل كل شيء
    edited_df = st.data_editor(
        work_df, 
        num_rows="dynamic", 
        use_container_width=True,
        key="excel_editor"
    )
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("💾 اعتماد هذه البيانات في التطبيق"):
            # بنحول الأعمدة الرقمية لأرقام عشان الذكاء الاصطناعي يحللها صح
            for col in edited_df.columns:
                try:
                    edited_df[col] = pd.to_numeric(edited_df[col])
                except:
                    pass
            st.session_state['main_df'] = edited_df
            st.success("تم نقل البيانات من الشيت لذاكرة الوحش! 🦁")
    
    with c2:
        # التصدير الفخم
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            edited_df.to_excel(writer, index=False, sheet_name='MIA8444_Sheet')
            workbook  = writer.book
            worksheet = writer.sheets['MIA8444_Sheet']
            header_fmt = workbook.add_format({'bold': True, 'bg_color': '#1F4E78', 'font_color': 'white', 'border': 1})
            for col_num, value in enumerate(edited_df.columns.values):
                worksheet.write(0, col_num, value, header_fmt)
        
        st.download_button(
            label="📥 تحميل هذا الشيت كملف إكسل",
            data=buffer.getvalue(),
            file_name="MIA8444_Worksheet.xlsx",
            mime="application/vnd.ms-excel"
        )

# (باقي الأقسام تظل كما هي لضمان عمل التطبيق)
elif choice == "📸 الرؤية الذكية (OCR)":
    st.header("📸 محرك الرؤية الذكي")
    cam = st.camera_input("صور الجدول")
elif choice == "🧼 منظف البيانات الذكي":
    st.header("🧼 وحدة التنظيف")
    if not df.empty:
        if st.button("تنظيف"): 
            st.session_state['main_df'] = df.drop_duplicates().fillna(0)
            st.success("تم!")
    else: st.warning("ارفع ملف أو اكتب في الشيت الأول.")
elif choice == "🧠 المحلل الذكي":
    st.header("🧠 تحليل MIA8444")
    if not df.empty: st.table(df.describe())
elif choice == "📈 التنبؤ المالي (AI)":
    st.header("📈 التنبؤ")
    if not df.empty and 'المبيعات' in df.columns:
        fig = px.line(df, y='المبيعات', title="مسار المبيعات")
        st.plotly_chart(fig)
elif choice == "🖥️ داشبورد الإدارة":
    st.header("🖥️ الداشبورد")
    if not df.empty:
        st.metric("إجمالي المبيعات", f"{df['المبيعات'].sum() if 'المبيعات' in df.columns else 0:,}")
elif choice == "📄 تقرير PDF النهائي":
    st.header("📄 تصدير التقرير")
    st.button("تحميل PDF")

st.write("---")
st.markdown("<center>Smart Analyst Beast | Powered by MIA8444</center>", unsafe_allow_html=True)
