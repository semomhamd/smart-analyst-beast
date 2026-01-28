import streamlit as st
import pandas as pd
from core_engine import load_file, clean_df
import base64

# ================== إعداد الصفحة ==================
st.set_page_config(
    page_title="Smart Analyst Beast",
    page_icon="🐉",
    layout="wide"
)

# ================== Session State ==================
if "dataset" not in st.session_state:
    st.session_state.dataset = pd.DataFrame()

if "lang" not in st.session_state:
    st.session_state.lang = "AR"

# ================== Logo ==================
st.image("assets/logo.png", width=120)

# ================== Header ==================
st.markdown("## 🐉 Smart Analyst Beast")
st.caption("حوّل الداتا لحكاية مفهومة")

# ================== Sidebar ==================
with st.sidebar:
    st.markdown("## ⚙️ الإعدادات")

    st.session_state.lang = st.selectbox(
        "🌍 اللغة",
        ["AR", "EN"]
    )

    uploaded = st.file_uploader(
        "📤 ارفع ملف",
        type=["xlsx", "xls", "csv"]
    )

    if uploaded:
        try:
            df = load_file(uploaded)
            st.session_state.dataset = clean_df(df)
            st.success("تم تحميل الملف ✔️")
        except Exception as e:
            st.error(str(e))

# ================== Manual Excel Input ==================
st.markdown("## ✍️ إدخال يدوي (زي Excel)")
manual_df = st.data_editor(
    st.session_state.dataset if not st.session_state.dataset.empty else pd.DataFrame(
        columns=["Column 1", "Column 2"]
    ),
    num_rows="dynamic",
    use_container_width=True
)

st.session_state.dataset = manual_df

# ================== Preview ==================
if not st.session_state.dataset.empty:
    st.markdown("## 👀 معاينة البيانات")
    st.dataframe(st.session_state.dataset, use_container_width=True)

    cols = st.session_state.dataset.columns.tolist()

    # ================== Charts ==================
    st.markdown("## 📊 الرسومات")

    col1, col2, col3 = st.columns(3)

    with col1:
        x = st.selectbox("X", cols)
    with col2:
        y = st.selectbox("Y", cols)
    with col3:
        chart_type = st.selectbox("نوع الرسم", ["Bar", "Line", "Pie"])

    chart_df = st.session_state.dataset[[x, y]].dropna()

    if chart_type == "Bar":
        st.bar_chart(chart_df.set_index(x))
    elif chart_type == "Line":
        st.line_chart(chart_df.set_index(x))
    elif chart_type == "Pie":
        st.write("⚠️ Pie محتاج قيم رقمية")
        st.pyplot(chart_df.groupby(x)[y].sum().plot.pie(autopct="%1.1f%%").figure)

    # ================== Download ==================
    st.markdown("## 📥 تحميل")
    csv = chart_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ تحميل CSV",
        csv,
        "data.csv",
        "text/csv"
    )

    # ================== WhatsApp Share ==================
    st.markdown("## 📤 مشاركة")
    text = "شوف التحليل ده 🔥"
    whatsapp_link = f"https://wa.me/?text={text}"
    st.markdown(f"[📲 مشاركة واتساب]({whatsapp_link})")

else:
    st.info("⬅️ ابدأ برفع ملف أو إدخال بيانات")
