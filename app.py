import streamlit as st
import pandas as pd
import os

# إعدادات الصفحة
st.set_page_config(page_title="Smart Analyst Beast", layout="wide")

# Theme
if 'theme' not in st.session_state:
    st.session_state.theme = 'Dark'

bg_color = "#0e1117" if st.session_state.theme == 'Dark' else "#ffffff"
text_color = "#D4AF37" if st.session_state.theme == 'Dark' else "#000000"

st.markdown(f"""
<style>
.stApp {{ background-color: {bg_color}; color: {text_color}; }}
</style>
""", unsafe_allow_html=True)


# Header
col_logo, col_space, col_lang, col_set = st.columns([2,6,1,1])

with col_logo:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", width=120)

with col_set:
    if st.button("Toggle Theme"):
        st.session_state.theme = 'Light' if st.session_state.theme == 'Dark' else 'Dark'
        st.rerun()


# Sidebar
with st.sidebar:
    choice = st.radio("الأدوات", [
        "Home",
        "Excel Master",
        "Power BI",
        "Python Lab",
        "AI Brain"
    ])


# Dataset موحد
if 'dataset' not in st.session_state:
    st.session_state.dataset = pd.DataFrame()


# ================= Home =================
if choice == "Home":

    st.title("Smart Analyst Beast")

    uploaded = st.file_uploader(
        "ارفع ملف Excel أو CSV",
        type=['xlsx', 'csv']
    )

    if uploaded:

        if uploaded.name.endswith('xlsx'):
            df = pd.read_excel(uploaded)
        else:
            df = pd.read_csv(uploaded)

        st.session_state.dataset = df
        st.success("تم رفع البيانات بنجاح 🔥")



# ================= Excel =================
elif choice == "Excel Master":

    df = st.session_state.dataset.copy()

    if df.empty:
        st.warning("ارفع بيانات الأول من الصفحة الرئيسية")
    else:

        df = st.data_editor(df, num_rows="dynamic")

        df["Total"] = df.iloc[:,1] * df.iloc[:,2]

        st.write("### Summary")

        st.write("Total =", df["Total"].sum())
        st.write("Average =", df["Total"].mean())

        if st.button("Create Pivot"):
            pivot = pd.pivot_table(
                df,
                index=df.columns[0],
                values="Total",
                aggfunc="sum"
            )
            st.dataframe(pivot)

        st.session_state.dataset = df



# ================= Dashboard =================
elif choice == "Power BI":

    df = st.session_state.dataset.copy()

    if df.empty:
        st.warning("ارفع بيانات الأول")
    else:

        st.subheader("Dashboard")

        st.line_chart(df.select_dtypes('number'))
        st.bar_chart(df.groupby(df.columns[0]).sum())



# ================= Python =================
elif choice == "Python Lab":

    code = st.text_area("اكتب كود Python")

    if st.button("Run"):
        try:
            exec(code)
        except Exception as e:
            st.error(e)



# ================= AI =================
elif choice == "AI Brain":

    df = st.session_state.dataset.copy()

    if df.empty:
        st.warning("ارفع بيانات الأول")
    else:

        if st.button("Generate Insights"):

            numeric = df.select_dtypes('number')

            st.write("أكبر رقم:", numeric.max().max())
            st.write("أصغر رقم:", numeric.min().min())
            st.write("المتوسط العام:", numeric.mean().mean())
