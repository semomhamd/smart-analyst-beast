import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image
import os
from io import BytesIO

# 1. إعدادات الهوية والاحترافية (MIA8444)
st.set_page_config(page_title="Smart Analyst Beast PRO", page_icon="🦁", layout="wide")

# الجملة الرسمية - الهوية الفلسفية للتطبيق
slogan = "You don't have to be a data analyst.. Smart Analyst thinks for you"

if 'db' not in st.session_state:
    st.session_state['db'] = pd.DataFrame()

# 2. السايد بار (الهوية الكاملة والتحكم)
with st.sidebar:
    if os.path.exists("8888.jpg"):
        st.image("8888.jpg", use_column_width=True)
    
    st.markdown(f"<center><b>{slogan}</b></center>", unsafe_allow_html=True)
    st.write("---")
    
    with st.expander("⚙️ الإعدادات (Settings)"):
        st.selectbox("اللغة", ["العربية", "English"])
        st.selectbox("المظهر", ["Dark Mode", "Light Mode"])
    
    st.write("---")
    # القائمة المحدثة بكل المميزات العالية
    menu = ["الرئيسية", "منظف البيانات", "الاكسل برو", "المحلل الذكي", "الرؤية الذكية (OCR)", "المستشار المالي (AI)", "الرسوم البيانيه", "التقرير النهائي"]
    choice = st.radio("القائمة الرئيسية:", menu)
    st.write("---")
    st.info(f"App: Smart Analyst Beast\nSignature: MIA8444")

# محرك العمليات
df = st.session_state['db']

# --- وظيفة التنبؤ المالي (AI Forecasting) ---
def run_forecasting(data):
    st.subheader("📉 مستشار التوقعات الذكي")
    num_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    if len(num_cols) > 0:
        target = st.selectbox("اختر العمود للتنبؤ بمستقبله:", num_cols)
        # خوارزمية تنبؤ بسيطة وفعالة (Linear Trend)
        y = data[target].values
        x = np.arange(len(y)).reshape(-1, 1)
        # حساب التوقعات للـ 5 فترات القادمة
        next_indices = np.arange(len(y), len(y) + 5).reshape(-1, 1)
        prediction = np.poly1d(np.polyfit(x.flatten(), y, 1))(next_indices.flatten())
        
        st.write(f"🔮 *التوقع للفترات الـ 5 القادمة لـ {target}:*")
        pred_df = pd.DataFrame({'الفترة القادمة': [f"T+{i+1}" for i in range(5)], 'التوقع': prediction})
        st.table(pred_df)
        
        fig = px.line(title=f"مسار التنبؤ لـ {target}")
        fig.add_scatter(y=y, name="البيانات الحالية")
        fig.add_scatter(y=prediction, x=np.arange(len(y), len(y) + 5), name="التوقعات المستقبلية")
        st.plotly_chart(fig, use_container_width=True)

# 3. تشغيل الصفحات
if choice == "الرئيسية":
    st.header("🏠 بوابة البيانات الذكية")
    col1, col2 = st.columns([3, 1])
    with col1:
        up = st.file_uploader("ارفع ملف Excel أو CSV", type=["csv", "xlsx"])
        if up:
            st.session_state['db'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
            st.success("تم شحن الوحش بالبيانات!")
    with col2:
        if st.button("🚀 بيانات اختبار"):
            st.session_state['db'] = pd.DataFrame({
                'المنتج': ['موبايل', 'ساعة', 'سماعة'] * 10,
                'المبيعات': np.random.randint(100, 1000, 30),
                'الكمية': np.random.randint(1, 20, 30)
            })
            st.rerun()

elif choice == "منظف البيانات":
    st.header("✨ منظف البيانات الاحترافي")
    if not df.empty:
        if st.button("🚀 تنظيف عميق (Deep Clean)"):
            st.session_state['db'] = df.dropna(how='all').drop_duplicates().fillna(0)
            st.success("البيانات أصبحت فلة!")
            st.dataframe(st.session_state['db'].head())
    else: st.warning("ارفع بياناتك الأول")

elif choice == "الاكسل برو":
    st.header("📊 محرر الاكسل الذكي")
    if not df.empty:
        df_ed = st.data_editor(df, use_container_width=True)
        st.session_state['db'] = df_ed
        num_cols = df_ed.select_dtypes(include=[np.number]).columns.tolist()
        if num_cols:
            st.write("---")
            target = st.selectbox("عمود الحساب الرقمي:", num_cols)
            idx = st.selectbox("تصنيف حسب:", [c for c in df_ed.columns if c != target])
            res = df_ed.groupby(idx)[target].sum().reset_index()
            res.columns = [idx, f"إجمالي {target}"]
            st.dataframe(res, use_container_width=True)

elif choice == "المحلل الذكي":
    st.header("🧠 المحلل الذكي (AI Analysis)")
    if not df.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.write("📊 *الوصف الإحصائي:*")
            st.dataframe(df.describe())
        with col2:
            st.write("🔍 *تحليل جودة البيانات:*")
            st.write(f"- عدد السجلات: {len(df)}")
            st.write(f"- الأعمدة: {', '.join(df.columns)}")
    else: st.warning("لا توجد بيانات")

elif choice == "الرؤية الذكية (OCR)":
    st.header("👁️ رؤية الوحش (OCR Vision)")
    cam = st.camera_input("صور التقرير الورقي")
    if cam: st.info("جاري تفعيل محرك قراءة الصور في التحديث القادم...")

elif choice == "المستشار المالي (AI)":
    st.header("🔮 مستشار التنبؤ المستقبلي")
    if not df.empty:
        run_forecasting(df)
    else: st.warning("ارفع بيانات تحتوي على أرقام للتنبؤ بها")

elif choice == "الرسوم البيانيه":
    st.header("📈 الرسوم البيانيه")
    if not df.empty:
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if num_cols:
            x_ax = st.selectbox("المحور الأفقي:", df.columns)
            y_ax = st.selectbox("المحور الرأسي:", num_cols)
            fig = px.bar(df, x=x_ax, y=y_ax, color=x_ax, template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

elif choice == "التقرير النهائي":
    st.header("📄 تصدير التقرير النهائي")
    if not df.empty:
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='MIA8444_Beast')
        st.download_button(label="📥 تحميل التقرير (Excel)", data=output.getvalue(), file_name="MIA8444_Beast_Report.xlsx")
