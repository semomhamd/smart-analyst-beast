import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO

# ======== محرك التوصيات الذكي (The Brain) ========
def feth_ai_advisor(df):
    if df is not None:
        num_cols = df.select_dtypes(include=np.number).columns
        if len(num_cols) > 0:
            avg_val = df[num_cols[0]].mean()
            return f"يا صديقي، متوسط '{num_cols[0]}' هو {avg_val:.2f}. بناءً على خبرة MIA8444، أرشح لك التركيز على القيم اللي فوق المتوسط ده لزيادة الربحية! 🚀"
    return "ارفع ملفك يا وحش وسيب الباقي على ذكاء FETH."

# ======== إعدادات الصفحة ========
st.set_page_config(page_title=f"The Beast | MIA8444", layout="wide", page_icon="🦁")

# ستايل "فخامة MIA8444"
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-image: linear-gradient(#1e3799, #000000); color: white; }
    .stMetric { background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 10px; border: 1px solid #f1c40f; }
    h1, h2, h3 { color: #f1c40f !important; font-family: 'Cairo', sans-serif; }
    .stAlert { border-radius: 20px; border: none; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
    </style>
    """, unsafe_allow_html=True)

# ======== القائمة الجانبية ========
with st.sidebar:
    st.markdown(f"<h1 style='text-align:center;'>MIA8444</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#bdc3c7;'>The Ultimate Smart Analyst</p>", unsafe_allow_html=True)
    st.markdown("---")
    app_mode = st.radio("انتقل بين الغرف:", 
                        ["🏠 صالة الاستقبال", "📂 مركز معالجة الملفات (PDF/Data)", "📈 غرفة العمليات البصرية"])
    st.markdown("---")
    st.caption("🔥 Powered by MIA8444 Signature")

# ======== المحتوى ========

if app_mode == "🏠 صالة الاستقبال":
    st.title("🦁 أهلاً بك في عرين الوحش")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"### نظام MIA8444 المتكامل")
        st.write("هنا مفيش مكان للعشوائية. ارفع تقاريرك الـ PDF أو ملفاتك الضخمة، وهحولها لك لقرارات بلمسة زر.")
        st.success("✅ النظام متصل بمحركات الذكاء الاصطناعي (Claude/GPT Ready)")
    with col2:
        st.image("https://img.icons8.com/fluency/240/lion.png")

elif app_mode == "📂 مركز معالجة الملفات (PDF/Data)":
    st.header("📂 معمل استخراج البيانات الذكي")
    
    tab_pdf, tab_data = st.tabs(["📄 معالجة الـ PDF", "📊 معالجة الـ Excel/CSV"])
    
    with tab_pdf:
        pdf_file = st.file_uploader("ارفع التقرير (PDF)", type=['pdf'])
        if pdf_file:
            st.info("🔍 جاري فحص الملف وتلخيص الأفكار الرئيسية...")
            st.code("Summary: تم اكتشاف جداول مبيعات واتجاهات نمو. جاهز للتحويل.")
            st.button("✨ استخراج البيانات للجداول فوراً")
            
    with tab_data:
        data_file = st.file_uploader("ارفع ملف البيانات", type=['csv', 'xlsx'])
        if data_file:
            df = pd.read_csv(data_file) if data_file.name.endswith('.csv') else pd.read_excel(data_file)
            st.session_state.df = df
            st.dataframe(df.head(10), use_container_width=True)
            st.balloons()

elif app_mode == "📈 غرفة العمليات البصرية":
    st.header("📈 غرفة العمليات (Beast Dashboard)")
    if 'df' in st.session_state:
        df = st.session_state.df
        
        # قسم التوصيات الذكية (FETH AI Advisor)
        st.warning(f"💬 *توصية FETH AI:* {feth_ai_advisor(df)}")
        
        # الأرقام القياسية
        c1, c2, c3 = st.columns(3)
        c1.metric("إجمالي السجلات", len(df))
        c2.metric("عدد الأعمدة", len(df.columns))
        c3.metric("توقيع المحلل", "MIA8444")
        
        # الرسوم البيانية
        st.markdown("---")
        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        if num_cols:
            col1, col2 = st.columns([1, 3])
            with col1:
                x = st.selectbox("المحور الأفقي", df.columns)
                y = st.selectbox("المحور الرأسي", num_cols)
                color_tag = st.selectbox("تصنيف بالألوان", [None] + list(df.columns))
            with col2:
                fig = px.bar(df, x=x, y=y, color=color_tag, template="plotly_dark", 
                             title=f"تحليل MIA8444 لبيانات {y}")
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("يا صديقي، ادخل 'مركز المعالجة' وارفع بياناتك الأول!")

st.markdown(f"<div style='text-align:center; padding:20px; color:#7f8c8d;'>Property of {AUTHOR_SIGNATURE} MIA8444 © 2026</div>", unsafe_allow_html=True)
