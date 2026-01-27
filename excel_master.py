import streamlit as st
import pandas as pd

def run_excel_app():
    st.markdown("<h2 style='text-align:center; color:#D4AF37;'>📟 بيئة إكسيل الوحش الحقيقية</h2>", unsafe_allow_html=True)

    # 1. تهيئة الذاكرة (لو مفيش بيانات ابدأ بشيت نظيف)
    if 'main_data' not in st.session_state or st.session_state['main_data'] is None:
        rows, cols = 15, 6
        columns = [chr(65 + i) for i in range(cols)]
        st.session_state['main_data'] = pd.DataFrame("", index=range(1, rows+1), columns=columns)

    # 2. شريط الأدوات العلوي
    col_t1, col_t2, col_t3 = st.columns([1, 1, 1])
    with col_t1:
        if st.button("➕ إضافة صف جديد"):
            new_row = pd.DataFrame("", index=[len(st.session_state['main_data']) + 1], columns=st.session_state['main_data'].columns)
            st.session_state['main_data'] = pd.concat([st.session_state['main_data'], new_row])
            st.rerun()
    with col_t2:
        if st.button("🗑️ مسح الشيت بالكامل"):
            st.session_state['main_data'] = None
            st.rerun()
    with col_t3:
        # ميزة الرفع المباشر داخل الشيت
        up = st.file_uploader("دمج ملف إكسيل", type=['xlsx', 'csv'], label_visibility="collapsed")
        if up:
            st.session_state['main_data'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
            st.rerun()

    st.info("💡 اكتب الأرقام في الجدول، وهتلاقي الحسابات والرسومات بتحدث تحت لوحدها!")

    # 3. المحرر السحري (المربوط بالذاكرة فوراً)
    # السر هنا في استخدام on_change أو تحديث الحالة مباشرة
    edited_df = st.data_editor(
        st.session_state['main_data'],
        use_container_width=True,
        num_rows="dynamic",
        key="beast_editor_v1" # مفتاح فريد لضمان التحديث
    )
    
    # تحديث الذاكرة المركزية
    st.session_state['main_data'] = edited_df

    # 4. منطقة العمليات والرسومات (تشتغل تلقائياً)
    st.markdown("---")
    tab1, tab2, tab3 = st.tabs(["🧮 الحسابات (SUM/AVG)", "📈 الرسوم البيانية", "📱 مشاركة واتساب"])

    # تجهيز البيانات الرقمية للعمليات
    numeric_df = edited_df.apply(pd.to_numeric, errors='coerce')

    with tab1:
        st.write("### 🔢 ملخص الأرقام")
        if not numeric_df.dropna(how='all', axis=1).empty:
            # حسابات مخصصة
            cols_to_show = numeric_df.dropna(how='all', axis=1).columns
            for col in cols_to_show:
                c1, c2, c3 = st.columns(3)
                col_sum = numeric_df[col].sum()
                col_avg = numeric_df[col].mean()
                c1.metric(f"مجموع {col}", f"{col_sum:,.2f}")
                c2.metric(f"متوسط {col}", f"{col_avg:,.2f}")
                c3.metric(f"أعلى قيمة", f"{numeric_df[col].max():,.2f}")
        else:
            st.warning("أدخل أرقاماً في الجدول لتظهر الحسابات هنا.")

    with tab2:
        st.write("### 📊 الرسم البياني الحي")
        available_cols = numeric_df.dropna(how='all', axis=1).columns
        if not available_cols.empty:
            selected_col = st.selectbox("اختر العمود للرسم:", available_cols)
            chart_style = st.radio("نوع الرسم:", ["Line", "Bar", "Area"], horizontal=True)
            
            if chart_style == "Line": st.line_chart(numeric_df[selected_col])
            elif chart_style == "Bar": st.bar_chart(numeric_df[selected_col])
            else: st.area_chart(numeric_df[selected_col])
        else:
            st.info("لا توجد بيانات رقمية للرسم بعد.")

    with tab3:
        st.write("### 📤 تصدير ومشاركة")
        phone = st.text_input("رقم الواتساب (مثال: 2010...)")
        if st.button("📱 توليد رابط المشاركة"):
            msg = f"تقرير الوحش MIA8444 جاهز! إجمالي المبالغ: {numeric_df.sum().sum()}"
            import urllib.parse
            url = f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"
            st.markdown(f"[اضغط هنا للإرسال للرقم {phone}]({url})")

# التوقيع
st.markdown("<p style='text-align:center; color:#555;'>MIA8444 | Verified Beast Code</p>", unsafe_allow_html=True)
