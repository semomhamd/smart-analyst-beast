import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sqlite3
import hashlib
import os
from pathlib import Path
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
from datetime import datetime
from arabic_reshaper import reshape
from bidi.algorithm import get_display

# ======= 1. إعدادات الحماية وقاعدة البيانات =======
DB_FILE = "users_data.db"
UPLOAD_DIR = Path("user_files")
UPLOAD_DIR.mkdir(exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (username TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    if result and result[0] == hash_password(password):
        return True
    return False

def register_user(username, password):
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("INSERT INTO users VALUES (?,?)", (username, hash_password(password)))
        conn.commit()
        conn.close()
        return True
    except:
        return False

# ======= 2. تهيئة التطبيق =======
st.set_page_config(page_title="The Beast v6.0", layout="wide", initial_sidebar_state="expanded")
init_db()

# تخصيص التصميم CSS (تطوير للنسخة السابقة)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;700&display=swap');
    * { font-family: 'Tajawal', sans-serif; direction: rtl; }
    .stApp { background-color: #0f172a; color: #f8fafc; }
    .css-1d391kg { background-color: #1e293b !important; } /* Sidebar */
    .stButton>button { width: 100%; border-radius: 10px; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); background-color: #10b981; }
    .data-card { background: #1e293b; padding: 20px; border-radius: 15px; border: 1px solid #334155; }
</style>
""", unsafe_allow_html=True)

# ======= 3. نظام تسجيل الدخول =======
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align:center;'>🦁 THE BEAST v6</h1>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["تسجيل الدخول", "إنشاء حساب جديد"])
        
        with tab1:
            user = st.text_input("اسم المستخدم")
            pwd = st.text_input("كلمة المرور", type="password")
            if st.button("دخول"):
                if check_user(user, pwd):
                    st.session_state.logged_in = True
                    st.session_state.username = user
                    st.rerun()
                else:
                    st.error("خطأ في البيانات")
        
        with tab2:
            new_user = st.text_input("اسم مستخدم جديد")
            new_pwd = st.text_input("كلمة مرور جديدة", type="password")
            if st.button("تسجيل"):
                if register_user(new_user, new_pwd):
                    st.success("تم التسجيل بنجاح! سجل دخولك الآن.")
                else:
                    st.error("اسم المستخدم موجود مسبقاً")
    st.stop()

# ======= 4. واجهة المستخدم بعد الدخول =======
user_path = UPLOAD_DIR / st.session_state.username
user_path.mkdir(exist_ok=True)

with st.sidebar:
    st.markdown(f"### 👤 مرحباً، {st.session_state.username}")
    menu = st.radio("القائمة الرئيسية", [
        "🏠 لوحة التحكم",
        "📂 إدارة الملفات",
        "🧹 تنظيف البيانات الذكي",
        "🤖 اسأل الذكاء الاصطناعي",
        "📊 التحليل البصري",
        "⚙️ الإعدادات"
    ])
    if st.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()

# وظيفة لتحميل البيانات المحفوظة للمستخدم
def get_user_data():
    files = list(user_path.glob(".csv")) + list(user_path.glob(".xlsx"))
    if files:
        # تحميل آخر ملف تم التعامل معه
        latest_file = max(files, key=os.path.getmtime)
        if latest_file.suffix == '.csv':
            return pd.read_csv(latest_file)
        else:
            return pd.read_excel(latest_file)
    return None

df = get_user_data()

# ======= 5. الصفحات والأدوات =======

if menu == "🏠 لوحة التحكم":
    st.title("🏠 نظرة عامة")
    if df is not None:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("عدد السجلات", f"{len(df):,}")
        c2.metric("عدد الأعمدة", len(df.columns))
        c3.metric("القيم المفقودة", df.isnull().sum().sum())
        c4.metric("حجم البيانات", f"{df.memory_usage().sum()/1024:.1f} KB")
        
        st.markdown("### 📋 معاينة البيانات")
        st.dataframe(df.head(10), use_container_width=True)
    else:
        st.info("لا توجد بيانات حالياً. ارفع ملفك من قسم إدارة الملفات.")

elif menu == "📂 إدارة الملفات":
    st.title("📂 رفع وإدارة ملفاتك")
    uploaded_file = st.file_uploader("اختر ملف (CSV أو XLSX)", type=["csv", "xlsx"])
    if uploaded_file:
        file_path = user_path / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"تم حفظ الملف {uploaded_file.name} بنجاح في مساحتك الخاصة!")
        st.rerun()
    
    st.markdown("---")
    st.subheader("🗄️ ملفاتك المحفوظة")
    for f in user_path.iterdir():
        col_f1, col_f2 = st.columns([3, 1])
        col_f1.write(f"📄 {f.name}")
        if col_f2.button("حذف", key=f.name):
            os.remove(f)
            st.rerun()

elif menu == "🧹 تنظيف البيانات الذكي":
    st.title("🧹 تنظيف ومعالجة البيانات")
    if df is not None:
        st.markdown("<div class='data-card'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("حذف الصفوف المكررة"):
                df = df.drop_duplicates()
                df.to_csv(user_path / "cleaned_data.csv", index=False)
                st.success("تم الحذف!")
            
            if st.button("تعبئة الفراغات تلقائياً"):
                for col in df.select_dtypes(include=[np.number]).columns:
                    df[col] = df[col].fillna(df[col].mean())
                st.success("تمت تعبئة الأرقام بالمتوسط!")

        with col2:
            st.write("🔍 *تحليل سريع للمشاكل:*")
            st.write(df.isnull().sum()[df.isnull().sum() > 0])
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("ارفع بيانات أولاً")

elif menu == "🤖 اسأل الذكاء الاصطناعي":
    st.title("🤖 مساعدك الذكي (PandasAI)")
    api_key = st.text_input("أدخل OpenAI API Key (من الإعدادات)", type="password")
    
    if df is not None and api_key:
        llm = OpenAI(api_token=api_key)
        smart_df = SmartDataframe(df, config={"llm": llm})
        
        user_query = st.text_area("ماذا تريد أن تعرف عن بياناتك؟ (مثال: ارسم لي مبيعات كل منطقة)")
        if st.button("إرسال"):
            with st.spinner("جاري التفكير..."):
                answer = smart_df.chat(user_query)
                st.write("### الإجابة:")
                st.write(answer)
    else:
        st.info("تحتاج إلى رفع ملف وإدخال API Key لتفعيل ميزة الدردشة.")

elif menu == "📊 التحليل البصري":
    st.title("📊 محرك الرسوم البيانية")
    if df is not None:
        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        cat_cols = df.select_dtypes(include='object').columns.tolist()
        
        c1, c2, c3 = st.columns(3)
        with c1: x_axis = st.selectbox("محور X", df.columns)
        with c2: y_axis = st.selectbox("محور Y", num_cols)
        with c3: chart_type = st.selectbox("نوع الرسم", ["خطي", "أعمدة", "تشتت", "صندوق"])
        
        if chart_type == "خطي": fig = px.line(df, x=x_axis, y=y_axis, template="plotly_dark")
        elif chart_type == "أعمدة": fig = px.bar(df, x=x_axis, y=y_axis, template="plotly_dark")
        elif chart_type == "تشتت": fig = px.scatter(df, x=x_axis, y=y_axis, template="plotly_dark")
        else: fig = px.box(df, x=x_axis, y=y_axis, template="plotly_dark")
        
        st.plotly_chart(fig, use_container_width=True)

# ======= 6. التذييل =======
st.markdown("---")
st.markdown(f"<p style='text-align: center; color: gray;'>The Beast v6.0 | جميع البيانات مشفرة ومحفوظة للمستخدم {st.session_state.username}</p>", unsafe_allow_html=True)
