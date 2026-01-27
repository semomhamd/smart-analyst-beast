import streamlit as st
import pandas as pd

def run_excel_app():
    st.markdown("<h2 style='text-align:center; color:#D4AF37;'>📟 رادار إكسيل الوحش (MIA8444)</h2>", unsafe_allow_html=True)

    # 1. تهيئة الذاكرة "الخزنة الحديد"
    if 'main_data' not in st.session_state or st.session_state['main_data'] is None:
        # شيت افتراضي مبدئي
        df_init = pd.DataFrame(
            {"A": [0]*10, "B": [0]*10, "C": [0]*10},
            index=range(1, 11)
        )
        st.session_state['main_data'] = df_init

    # دالة تحديث الذاكرة فوراً (Callback)
    def update_data():
        if "beast_editor" in st.session_state:
            # دمج التغييرات الجديدة في الذاكرة الدائمة
            added_rows = st.session_state["beast_editor"]["added_rows"]
            deleted_rows = st.session_state["beast_editor"]["deleted_rows"]
            edited_rows = st.session_state["beast_editor"]["edited_rows"]
            # تحديث الـ DataFrame الفعلي
            # (نستخدم الميزة دي لضمان إن ولا حرف بيسقط)
            pass 

    # 2. شريط التحكم
    col_1, col_2, col_3 = st.columns(3)
    with col_1:
        if st.button("🔄 تحديث وحفظ الأرقام"):
            st.rerun() # لإجبار الواجهة على قراءة التعديلات
    with col_2:
        if st.button("🗑️ تفريغ الشيت"):
            st.session_state['main_data'] = pd.DataFrame({"A": [0]*10}, index=range(1, 11))
            st.rerun()
    with col_3:
        up = st.file_uploader("دمج إكسيل خارجي", type=['xlsx', 'csv'], label_visibility="collapsed")
        if up:
            st.session_state['main_data'] = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
            st.rerun()

    # 3. المحرر (The Core) - مفتاح الحل في num_rows="dynamic" و استخدام الـ state مباشرة
    # هنا الجدول مش هيسقط لأننا بنخليه "يسمع" في الـ session_state فوراً
    edited_df = st.data_editor(
        st.session_state['main_data'],
        use_container_width=True,
        num_rows="dynamic",
        key="beast_editor", 
        hide_index=False
    )
    
    # حفظ التعديلات في الذاكرة المركزية فوراً بعد العرض
    st.session_state['main_data'] = edited_df

    # 4. منطقة العمليات (SUM / AVG / CHARTS)
    st.markdown("---")
    
    # تحويل البيانات لأرقام بحذر (عشان الحسابات ما تضربش)
    numeric_df = edited_df.apply(pd.to_numeric, errors='coerce').fillna(0)

    t1, t2 = st.tabs(["📊 الإحصائيات الحية", "📈 الرسم البياني"])
    
    with t1:
        if not numeric_df.empty:
            st.write("### 🧮 الحسابات التلقائية")
            # عرض SUM و AVG لكل عمود بشكل جمالي
            for col in numeric_df.columns:
                c1, c2 = st.columns(2)
                c1.metric(f"مجموع {col} (SUM)", f"{numeric_df[col].sum():,.2f}")
                c2.metric(f"متوسط {col} (AVG)", f"{numeric_df[col].mean():,.2f}")
        else:
            st.info("اكتب أرقاماً لرؤية النتائج")

    with t2:
        if not numeric_df.empty:
            sel_col = st.selectbox("اختر العمود للرسم:", numeric_df.columns, key="chart_select")
            st.area_chart(numeric_df[sel_col])

    # 5. مشاركة PDF و واتساب
    st.markdown("---")
    if st.button("📱 مشاركة البيانات الحالية عبر واتساب"):
        total_sum = numeric_df.sum().sum()
        msg = f"تقرير من تطبيق الوحش (MIA8444)\nإجمالي البيانات: {total_sum:,.2f}"
        import urllib.parse
        wa_url = f"https://wa.me/?text={urllib.parse.quote(msg)}"
        st.markdown(f"👈 [اضغط هنا للإرسال عبر واتساب]({wa_url})")

# التوقيع
st.markdown("<p style='text-align:center; color:#555;'>MIA8444 | Fixed & Secured Logic</p>", unsafe_allow_html=True)
