import streamlit as st
import pandas as pd
import numpy as np

# -------------------------------------------------------
# هويتك هي الأساس          MIA8444
# -------------------------------------------------------
st.set_page_config(page_title="Smart Analyst Beast", layout="wide")

# الذاكرة اللي بتحفظ تعبك
if 'db' not in st.session_state:
    st.session_state['db'] = None

# -------------------------------------------------------
# السايد بار (الترسانة الحقيقية)
# -------------------------------------------------------
with st.sidebar:
    st.title("🦁 MIA8444 Beast")
    tool = st.radio("الترسانة:", [
        "🏠 الرئيسية",
        "📄 الشيت الذكي",
        "🧹 المنظف",
        "🧠 الذكاء الاصطناعي",
        "📊 الرسوم",
        "☁️ السحابة",
        "📑 التصدير",
        "⚙️ الإعدادات"
    ])
    st.write("---")
    st.caption("النسخة الفخمة النهائية – 2026")

# -------------------------------------------------------
# الصفحات الرئيسية
# -------------------------------------------------------
if tool == "🏠 الرئيسية":
    st.header("مرحباً بك يا حبيب قلبي [cite: 2026-01-27]")
    st.markdown("ارفع ملفك (csv أو excel) وهنبدأ الشغل الفوري 🚀")

    up = st.file_uploader("ارفع ملفك هنا", type=["csv", "xlsx", "xls"])
    if up is not None:
        try:
            if up.name.lower().endswith(('.xlsx', '.xls')):
                st.session_state['db'] = pd.read_excel(up)
            else:
                st.session_state['db'] = pd.read_csv(up)
            st.success("تم ترويض الملف بنجاح! ✅")
            st.dataframe(st.session_state['db'].head(5))
        except Exception as e:
            st.error(f"حصل خطأ أثناء قراءة الملف: {e}")

# -------------------------------------------------------
elif tool == "📄 الشيت الذكي":
    st.header("📝 محرك المعادلات (Duo)")

    # لو مفيش بيانات → شيت فاضي افتراضي
    if st.session_state['db'] is None:
        default_data = pd.DataFrame([['', 0, 0]], columns=['الصنف', 'الكمية', 'السعر'])
        st.info("ما فيش بيانات محملة بعد، جرب الشيت الفاضي ده:")
    else:
        default_data = st.session_state['db']

    # الجدول التفاعلي
    edited_df = st.data_editor(
        default_data,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "الكمية": st.column_config.NumberColumn(min_value=0, step=1),
            "السعر": st.column_config.NumberColumn(min_value=0.0, format="%.2f"),
        }
    )

    if st.button("⚡ تشغيل كل دوال الإكسيل", type="primary"):
        try:
            edited_df['الإجمالي'] = (
                pd.to_numeric(edited_df['الكمية'], errors='coerce') *
                pd.to_numeric(edited_df['السعر'], errors='coerce')
            ).fillna(0)
            st.session_state['db'] = edited_df
            st.success("المعادلات اشتغلت يا وحش! MIA8444")
            st.balloons()
            st.dataframe(edited_df)
        except Exception as e:
            st.error(f"مشكلة في الحسابات: {e}")

# -------------------------------------------------------
elif tool == "🧠 الذكاء الاصطناعي":
    st.header("🧠 مخ الذكاء الاصطناعي")

    if st.session_state.get('db') is None:
        st.error("فين الملف؟ ارفع ملف في الصفحة الرئيسية الأول.")
    else:
        df = st.session_state['db']

        # تنظيف واختيار الأعمدة الرقمية بأمان
        numeric_df = df.apply(pd.to_numeric, errors='coerce')
        numeric_cols = numeric_df.select_dtypes(include=np.number).columns

        if len(numeric_cols) == 0:
            st.warning("ما فيش أعمدة رقمية صالحة في الجدول حاليًا.")
        else:
            # ─────────────── التلات اقتراحات ───────────────
            max_val = numeric_df[numeric_cols].max().max()
            total_qty = df.get('الكمية', pd.Series(dtype=float)).sum()
            avg_price = df.get('السعر', pd.Series(dtype=float)).mean()

            col1, col2, col3 = st.columns(3)

            with col1:
                if pd.notna(max_val):
                    st.metric("أكبر قيمة", f"{max_val:,.2f}")
                else:
                    st.metric("أكبر قيمة", "—")

            with col2:
                st.metric("إجمالي الكميات", f"{total_qty:,.0f}")

            with col3:
                if pd.notna(avg_price):
                    st.metric("متوسط السعر", f"{avg_price:,.2f}")
                else:
                    st.metric("متوسط السعر", "—")

            st.markdown("---")
            st.caption("يمكن توسيع الصفحة دي بسهولة (أكثر الأصناف تكرارًا، إجمالي المبيعات، إلخ)")

# -------------------------------------------------------
# باقي الصفحات (placeholder حاليًا – يمكن تطويرها لاحقًا)
# -------------------------------------------------------
elif tool == "🧹 المنظف":
    st.header("🧹 منظف البيانات")
    st.info("قريبًا... (إزالة التكرارات، تعبئة القيم الناقصة، تنظيف النصوص)")

elif tool == "📊 الرسوم":
    st.header("📊 الرسوم البيانية")
    st.info("قريبًا... (بار، خط، دائرة، heatmap)")

elif tool == "☁️ السحابة":
    st.header("☁️ التخزين السحابي")
    st.info("قريبًا... (Google Drive / Dropbox / S3)")

elif tool == "📑 التصدير":
    st.header("📑 تصدير النتائج")
    st.info("قريبًا... (Excel, CSV, PDF)")

elif tool == "⚙️ الإعدادات":
    st.header("⚙️ الإعدادات")
    st.info("قريبًا... (تغيير الثيم، اللغة، إلخ)")

# Footer بسيط
st.markdown("---")
st.caption("MIA8444 Smart Analyst Beast – كل الحقوق محفوظة © 2026")
