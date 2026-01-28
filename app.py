import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import duckdb
from datetime import datetime
from io import BytesIO

from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# ======================================================
# Page Config
# ======================================================
st.set_page_config(
    page_title="Smart Analyst Beast",
    layout="wide",
    page_icon="🐉"
)

# ======================================================
# Session State
# ======================================================
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

if "lang" not in st.session_state:
    st.session_state.lang = "AR"

if "dataset" not in st.session_state:
    st.session_state.dataset = pd.DataFrame()

if "current_view" not in st.session_state:
    st.session_state.current_view = "Excel"

# ======================================================
# Theme
# ======================================================
bg = "#0e1117" if st.session_state.theme == "Dark" else "#ffffff"
txt = "#D4AF37" if st.session_state.theme == "Dark" else "#000000"

st.markdown(f"""
<style>
.stApp {{
    background-color: {bg};
    color: {txt};
}}
.footer {{
    text-align:center;
    font-size:12px;
    color:#888;
    margin-top:30px;
}}
</style>
""", unsafe_allow_html=True)

# ======================================================
# Header
# ======================================================
h1, h2, h3 = st.columns([6,1,1])

with h1:
    try:
        st.image("8888.jpg", width=120)
    except:
        st.markdown("### 🐉 Smart Analyst Beast")

with h2:
    def toggle_lang():
        st.session_state.lang = "EN" if st.session_state.lang == "AR" else "AR"
    st.button("🌐 AR / EN", on_click=toggle_lang)

with h3:
    with st.popover("⚙️"):
        def toggle_theme():
            st.session_state.theme = "Light" if st.session_state.theme=="Dark" else "Dark"
        st.button("Toggle Theme", on_click=toggle_theme)

# ======================================================
# Sidebar
# ======================================================
tool = st.sidebar.radio(
    "🛠️ Tools",
    ["Excel", "Charts", "SQL", "Report"]
)

st.session_state.current_view = tool

# ======================================================
# Helpers
# ======================================================
def ai_summary(df: pd.DataFrame) -> str:
    if df.empty:
        return "لا توجد بيانات."
    return f"""
    عدد الصفوف: {df.shape[0]}
    عدد الأعمدة: {df.shape[1]}
    أعمدة رقمية: {len(df.select_dtypes(include=np.number).columns)}
    """

def generate_pdf(df, title="Smart Analyst Beast"):
    buffer = BytesIO()
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    elements = []

    try:
        elements.append(Image("8888.jpg", width=80, height=80))
    except:
        pass

    elements.append(Paragraph(title, styles["Title"]))
    elements.append(
        Paragraph(
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            styles["Normal"]
        )
    )

    if not df.empty:
        table_data = [df.columns.tolist()] + df.head(20).astype(str).values.tolist()
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0),colors.gold),
            ('GRID',(0,0),(-1,-1),0.5,colors.black),
            ('FONT',(0,0),(-1,0),'Helvetica-Bold')
        ]))
        elements.append(table)

    elements.append(Paragraph("Signature: MIA8444", styles["Italic"]))

    doc.build(elements)
    buffer.seek(0)
    return buffer

# ======================================================
# Excel View
# ======================================================
if tool == "Excel":
    st.header("📊 Excel-like Sheet")

    file = st.file_uploader(
        "ارفع CSV أو Excel (أي نوع بيانات)",
        type=["csv","xlsx"]
    )

    if file:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file, dtype=str)
        else:
            df = pd.read_excel(file, dtype=str)

        st.session_state.dataset = df

    if not st.session_state.dataset.empty:
        st.markdown("### ✍️ إدخال وتعديل يدوي")
        edited = st.data_editor(
            st.session_state.dataset,
            num_rows="dynamic",
            use_container_width=True
        )
        st.session_state.dataset = edited

        st.markdown("### 🧠 AI Insight")
        st.code(ai_summary(edited))

# ======================================================
# Charts View
# ======================================================
elif tool == "Charts":
    st.header("📈 Charts")

    df = st.session_state.dataset
    if df.empty:
        st.warning("ارفع بيانات الأول")
    else:
        cols = df.columns.tolist()
        nums = df.select_dtypes(include=np.number).columns.tolist()

        if not nums:
            st.warning("لا يوجد أعمدة رقمية")
        else:
            x = st.selectbox("X", cols)
            y = st.selectbox("Y", nums)

            cdf = df[[x,y]].dropna()
            cdf[x] = cdf[x].astype(str)

            chart = alt.Chart(cdf).mark_bar(color="#D4AF37").encode(
                x=alt.X(x, sort=None),
                y=y
            )

            st.altair_chart(chart, use_container_width=True)

# ======================================================
# SQL View
# ======================================================
elif tool == "SQL":
    st.header("🧪 SQL Lab")

    df = st.session_state.dataset
    if df.empty:
        st.warning("ارفع بيانات الأول")
    else:
        q = st.text_area(
            "اكتب SQL",
            "SELECT * FROM df LIMIT 10"
        )

        if st.button("Run"):
            try:
                res = duckdb.query(q).df()
                st.dataframe(res)
            except Exception as e:
                st.error(str(e))

# ======================================================
# Report View
# ======================================================
elif tool == "Report":
    st.header("📄 Report")

    df = st.session_state.dataset
    if df.empty:
        st.warning("ارفع بيانات الأول")
    else:
        st.dataframe(df.head(20))
        st.markdown("### 🧠 AI Summary")
        st.code(ai_summary(df))

# ======================================================
# 🔥 Unified Export Button
# ======================================================
st.divider()
st.subheader("📤 مشاركة ذكية")

if st.button("📄 تصدير PDF + جاهز واتساب"):
    pdf = generate_pdf(
        st.session_state.dataset,
        title=f"Smart Analyst Beast – {st.session_state.current_view}"
    )

    st.success("تم تجهيز الملف ✔️")
    st.download_button(
        "⬇️ تحميل PDF",
        pdf,
        file_name="Smart_Analyst_Beast.pdf",
        mime="application/pdf"
    )

    st.info("جاهز للإرسال على WhatsApp (API لاحقًا)")

# ======================================================
# Footer
# ======================================================
st.markdown("""
<div class="footer">
Smart Analyst Beast © | Signature MIA8444
</div>
""", unsafe_allow_html=True)
