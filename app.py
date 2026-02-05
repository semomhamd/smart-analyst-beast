import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io
import base64

# ======== استيراد آمن للمكتبات ========
try:
    from st_aggrid import AgGrid, GridOptionsBuilder
    AGGRID_AVAILABLE = True
except ImportError:
    AGGRID_AVAILABLE = False

try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False

try:
    import duckdb
    DUCKDB_AVAILABLE = True
except ImportError:
    DUCKDB_AVAILABLE = False

try:
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    from sklearn.linear_model import LinearRegression
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

# ======== إعدادات الصفحة ========
st.set_page_config(
    page_title="Smart Analyst Beast PRO", 
    layout="wide", 
    page_icon="🦁",
    initial_sidebar_state="expanded"
)

# ======== CSS مخصص ========
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ======== الذاكرة الدائمة ========
if 'beast_vault' not in st.session_state:
    st.session_state['beast_vault'] = None
if 'sql_history' not in st.session_state:
    st.session_state['sql_history'] = []
if 'query_results' not in st.session_state:
    st.session_state['query_results'] = None

# ======== القائمة الجانبية ========
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h1 style='font-size: 4rem; margin: 0;'>🦁</h1>
        <h2 style='color: #FF6B6B; margin: 5px 0;'>Smart Analyst Beast</h2>
        <p style='color: #95A5A6; font-size: 12px;'>PRO Edition v2.0</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    
    menu_map = {
        "🏠 الرئيسية": "Home",
        "📥 مركز البيانات": "Data",
        "📊 Excel Pro": "Excel",
        "🧠 المحلل الذكي": "Analyst",
        "🔮 التنبؤ بالمستقبل": "Forecast",
        "🎯 التحليل الاستراتيجي": "Strategic",
        "🖥️ الداشبورد": "Dash",
        "🗄️ SQL داخلي": "SQL",
        "🤖 المساعد الذكي": "AI",
        "💾 التصدير": "Export"
    }
    
    choice = st.radio("القائمة:", list(menu_map.keys()), label_visibility="collapsed")
    
    st.write("---")
    st.markdown("### ⚡ أدوات سريعة")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ مسح", use_container_width=True):
            st.session_state['beast_vault'] = None
            st.session_state['sql_history'] = []
            st.rerun()
    
    with col2:
        if st.button("📊 تجريبي", use_container_width=True):
            rows = 10000
            data = {
                'ID': range(1, rows + 1),
                'التاريخ': [datetime(2024, 1, 1) + timedelta(days=np.random.randint(0, 365)) for _ in range(rows)],
                'المنتج': [f"منتج_{np.random.randint(1, 100)}" for _ in range(rows)],
                'الفئة': [np.random.choice(['إلكترونيات', 'ملابس', 'أغذية', 'أثاث', 'رياضة']) for _ in range(rows)],
                'المبيعات': np.random.uniform(1000, 100000, size=rows).round(2),
                'الكمية': np.random.randint(1, 100, size=rows),
                'الفرع': [np.random.choice(['القاهرة', 'دبي', 'الرياض', 'جدة', 'لندن', 'نيويورك']) for _ in range(rows)],
                'التقييم': np.random.randint(1, 6, size=rows),
                'التكلفة': np.random.uniform(500, 50000, size=rows).round(2),
                'العميل': [f"عميل_{np.random.randint(1, 1000)}" for _ in range(rows)]
            }
            st.session_state['beast_vault'] = pd.DataFrame(data)
            st.success(f"✅ {rows:,} صف!")
            st.rerun()
    
    if st.button("🚀 50,000 صف (اختبار)", use_container_width=True):
        rows = 50000
        data = {
            'ID': range(1, rows + 1),
            'التاريخ': [datetime(2024, 1, 1) + timedelta(days=np.random.randint(0, 365)) for _ in range(rows)],
            'المنتج': [f"منتج_{np.random.randint(1, 500)}" for _ in range(rows)],
            'المبيعات': np.random.uniform(1000, 500000, size=rows).round(2),
            'الكمية': np.random.randint(1, 500, size=rows),
            'الفرع': [np.random.choice(['القاهرة', 'دبي', 'الرياض', 'جدة', 'لندن', 'باريس']) for _ in range(rows)],
        }
        st.session_state['beast_vault'] = pd.DataFrame(data)
        st.success(f"✅ {rows:,} صف محمل!")
        st.rerun()
    
    st.write("---")
    st.caption("🔒 MIA8444 | Beast Engine v2.0")

df = st.session_state['beast_vault']

# ======== دوال مساعدة ========
def get_download_link(df, filename, file_type):
    if file_type == 'csv':
        data = df.to_csv(index=False)
        b64 = base64.b64encode(data.encode()).decode()
        return f'<a href="data:file/csv;base64,{b64}" download="{filename}" style="text-decoration:none;"><button style="background:#4ECDC4;color:white;padding:10px 20px;border:none;border-radius:5px;cursor:pointer;">📥 CSV</button></a>'
    elif file_type == 'excel':
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Data', index=False)
        b64 = base64.b64encode(output.getvalue()).decode()
        return f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}" style="text-decoration:none;"><button style="background:#FF6B6B;color:white;padding:10px 20px;border:none;border-radius:5px;cursor:pointer;">📥 Excel</button></a>'

def run_sql_query(df, query):
    if not DUCKDB_AVAILABLE:
        return None, "مكتبة DuckDB غير مثبتة"
    
    try:
        con = duckdb.connect(database=':memory:')
        con.register('data', df)
        result = con.execute(query).fetchdf()
        con.close()
        return result, None
    except Exception as e:
        return None, str(e)

# ======== الصفحات ========

if menu_map[choice] == "Home":
    st.markdown('<h1 class="main-header">🦁 Smart Analyst Beast PRO</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h3>منصة تحليل البيانات الشاملة | Excel + SQL + Python + AI</h3>
        <p style='color: #95A5A6;'>100% مجاني • 100% عربي • يعمل على أي جهاز</p>
    </div>
    """, unsafe_allow_html=True)
    
    if df is not None:
        st.subheader("📊 حالة النظام")
        c1, c2, c3, c4, c5 = st.columns(5)
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        with c1:
            st.metric("📊 الصفوف", f"{len(df):,}")
        with c2:
            st.metric("📋 الأعمدة", len(df.columns))
        with c3:
            if len(numeric_cols) > 0:
                st.metric("💰 الإجمالي", f"{df[numeric_cols[0]].sum():,.0f}")
        with c4:
            st.metric("📅 التاريخ", datetime.now().strftime("%d/%m"))
        with c5:
            st.metric("⏰ الوقت", datetime.now().strftime("%H:%M"))
        
        st.subheader("👁️ معاينة البيانات")
        st.dataframe(df.head(8), use_container_width=True, height=300)
        
        st.subheader("💡 رؤى ذكية")
        cols = st.columns(3)
        
        if 'المنتج' in df.columns and 'المبيعات' in df.columns:
            best_product = df.groupby('المنتج')['المبيعات'].sum().idxmax()
            best_value = df.groupby('المنتج')['المبيعات'].sum().max()
            cols[0].info(f"🏆 الأفضل مبيعاً: *{best_product}* ({best_value:,.0f})")
        
        if 'الفرع' in df.columns and 'المبيعات' in df.columns:
            best_branch = df.groupby('الفرع')['المبيعات'].sum().idxmax()
            cols[1].info(f"🏬 الأفضل فرعاً: *{best_branch}*")
        
        if 'التقييم' in df.columns:
            avg_rating = df['التقييم'].mean()
            cols[2].info(f"⭐ متوسط التقييم: *{avg_rating:.1f}/5*")
    else:
        st.warning("⚠️ لا توجد بيانات. استخدم 'بيانات تجريبية' من القائمة الجانبية")

elif menu_map[choice] == "Data":
    st.header("📥 مركز إدارة البيانات")
    
    tab1, tab2 = st.tabs(["📤 رفع ملف", "🔗 قاعدة بيانات"])
    
    with tab1:
        uploaded = st.file_uploader("ارفع Excel أو CSV", type=['xlsx', 'csv', 'xls'])
        if uploaded:
            try:
                if uploaded.name.endswith('.csv'):
                    df_new = pd.read_csv(uploaded)
                else:
                    df_new = pd.read_excel(uploaded)
                
                st.session_state['beast_vault'] = df_new
                st.success(f"✅ تم استيراد {len(df_new):,} صف!")
                st.dataframe(df_new.head(), use_container_width=True)
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")
    
    with tab2:
        st.info("🚧 قريباً: دعم MySQL و PostgreSQL")

elif menu_map[choice] == "Excel":
    st.header("📊 Excel Pro - محرك الجداول")
    
    if df is not None:
        if AGGRID_AVAILABLE:
            gb = GridOptionsBuilder.from_dataframe(df)
            gb.configure_pagination(paginationPageSize=25)
            gb.configure_default_column(editable=True, filterable=True, sortable=True)
            gb.configure_side_bar()
            
            grid = AgGrid(df, gridOptions=gb.build(), theme='alpine', height=600)
            
            if st.button("💾 حفظ التعديلات", type="primary"):
                st.session_state['beast_vault'] = pd.DataFrame(grid['data'])
                st.success("✅ تم الحفظ!")
                st.balloons()
        else:
            st.data_editor(df, use_container_width=True, height=600)
    else:
        st.error("❌ لا توجد بيانات")

elif menu_map[choice] == "Analyst":
    st.header("🧠 المحلل الذكي")
    
    if df is not None:
        analysis = st.selectbox("نوع التحليل:", [
            "📊 إحصائيات وصفية",
            "📈 مصفوفة الارتباطات", 
            "🔍 تجزئة العملاء (K-Means)",
            "📉 انحدار خطي"
        ])
        
        if analysis == "📊 إحصائيات وصفية":
            st.dataframe(df.describe(), use_container_width=True)
            
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_cols:
                col = st.selectbox("اختر عمود:", numeric_cols)
                c1, c2 = st.columns(2)
                c1.plotly_chart(px.histogram(df, x=col), use_container_width=True)
                c2.plotly_chart(px.box(df, y=col), use_container_width=True)
        
        elif analysis == "📈 مصفوفة الارتباطات":
            numeric_df = df.select_dtypes(include=[np.number])
            if len(numeric_df.columns) > 1:
                corr = numeric_df.corr()
                st.plotly_chart(px.imshow(corr, text_auto=True, color_continuous_scale='RdBu_r'), use_container_width=True)
        
        elif analysis == "🔍 تجزئة العملاء (K-Means)" and SKLEARN_AVAILABLE:
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if len(numeric_cols) >= 2:
                features = st.multiselect("اختر متغيرين:", numeric_cols, default=numeric_cols[:2])
                if len(features) == 2:
                    n_clusters = st.slider("عدد المجموعات:", 2, 8, 3)
                    X = df[features].dropna()
                    X_scaled = StandardScaler().fit_transform(X)
                    clusters = KMeans(n_clusters=n_clusters, random_state=42).fit_predict(X_scaled)
                    st.plotly_chart(px.scatter(X, x=features[0], y=features[1], color=clusters.astype(str)), use_container_width=True)
        
        elif analysis == "📉 انحدار خطي" and SKLEARN_AVAILABLE:
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if len(numeric_cols) >= 2:
                x_col = st.selectbox("X:", numeric_cols)
                y_col = st.selectbox("Y:", [c for c in numeric_cols if c != x_col])
                fig = px.scatter(df, x=x_col, y=y_col, trendline="ols")
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("❌ لا توجد بيانات")

elif menu_map[choice] == "Forecast":
    st.header("🔮 التنبؤ بالمستقبل")
    
    if df is not None and PROPHET_AVAILABLE:
        date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
        if not date_cols:
            for col in df.columns:
                try:
                    df[col] = pd.to_datetime(df[col])
                    date_cols.append(col)
                    break
                except:
                    continue
        
        if date_cols:
            date_col = st.selectbox("عمود التاريخ:", date_cols)
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if numeric_cols:
                target = st.selectbox("المتغير:", numeric_cols)
                periods = st.slider("فترة التنبؤ (يوم):", 7, 365, 30)
                
                if st.button("🚀 تنبؤ", type="primary"):
                    with st.spinner("جاري التحليل..."):
                        df_prophet = df[[date_col, target]].rename(columns={date_col: 'ds', target: 'y'}).dropna()
                        if len(df_prophet) > 30:
                            model = Prophet()
                            model.fit(df_prophet)
                            future = model.make_future_dataframe(periods=periods)
                            forecast = model.predict(future)
                            
                            fig = px.line(forecast, x='ds', y=['yhat', 'yhat_lower', 'yhat_upper'])
                            st.plotly_chart(fig, use_container_width=True)
                            st.dataframe(forecast[['ds', 'yhat']].tail(periods), use_container_width=True)
                        else:
                            st.error("⚠️ يحتاج 30 صف على الأقل")
    else:
        st.error("❌ لا توجد بيانات أو Prophet غير مثبت")

elif menu_map[choice] == "Strategic":
    st.header("🎯 التحليل الاستراتيجي (BCG Matrix)")
    
    if df is not None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        cat_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if len(numeric_cols) >= 2 and cat_cols:
            growth = st.selectbox("معدل النمو:", numeric_cols)
            share = st.selectbox("الحصة السوقية:", [c for c in numeric_cols if c != growth])
            category = st.selectbox("التصنيف:", cat_cols)
            
            df['growth_rate'] = df[growth] / df[growth].mean()
            df['market_share'] = df[share] / df[share].mean()
            
            fig = px.scatter(df, x='market_share', y='growth_rate', size=share, color=category,
                           title="مصفوفة BCG")
            fig.add_hline(y=1, line_dash="dash")
            fig.add_vline(x=1, line_dash="dash")
            fig.add_annotation(x=0.5, y=1.5, text="❓ علامات استفهام")
            fig.add_annotation(x=1.5, y=1.5, text="⭐ نجوم")
            fig.add_annotation(x=0.5, y=0.5, text="🐄 أبقار حلوب")
            fig.add_annotation(x=1.5, y=0.5, text="🐕 كلاب")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("❌ لا توجد بيانات")

elif menu_map[choice] == "Dash":
    st.header("🖥️ الداشبورد التفاعلي")
    
    if df is not None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if numeric_cols:
            kpi = st.selectbox("المؤشر الرئيسي:", numeric_cols)
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("الإجمالي", f"{df[kpi].sum():,.0f}")
            c2.metric("المتوسط", f"{df[kpi].mean():,.0f}")
            c3.metric("الأعلى", f"{df[kpi].max():,.0f}")
            c4.metric("العدد", f"{len(df):,}")
            
            c1, c2 = st.columns(2)
            with c1:
                if 'الفئة' in df.columns:
                    st.plotly_chart(px.pie(df, values=kpi, names='الفئة'), use_container_width=True)
            with c2:
                if 'الفرع' in df.columns:
                    st.bar_chart(df.groupby('الفرع')[kpi].sum())
    else:
        st.error("❌ لا توجد بيانات")

elif menu_map[choice] == "SQL":
    st.header("🗄️ محرك SQL الداخلي")
    
    if not DUCKDB_AVAILABLE:
        st.error("❌ مكتبة DuckDB غير مثبتة. نفذ: pip install duckdb")
    elif df is None:
        st.warning("⚠️ لا توجد بيانات. استورد بيانات أولاً")
    else:
        st.success(f"✅ جاهز للاستعلام! الجدول متاح باسم: data ({len(df):,} صف)")
        
        st.markdown("### 📝 أمثلة على الاستعلامات:")
        examples = {
            "كل البيانات": "SELECT * FROM data LIMIT 100",
            "إجمالي المبيعات حسب الفرع": "SELECT الفرع, SUM(المبيعات) as total_sales FROM data GROUP BY الفرع ORDER BY total_sales DESC",
            "متوسط التقييم": "SELECT AVG(التقييم) as avg_rating FROM data",
            "أفضل 10 منتجات": "SELECT المنتج, SUM(المبيعات) as total FROM data GROUP BY المنتج ORDER BY total DESC LIMIT 10",
            "مبيعات الشهر": "SELECT strftime('%Y-%m', التاريخ) as month, SUM(المبيعات) as sales FROM data GROUP BY month ORDER BY month",
            "تصفية شرطية": "SELECT * FROM data WHERE المبيعات > 50000 AND التقييم >= 4",
            "عدد الصفوف": "SELECT COUNT(*) as count FROM data"
        }
        
        selected_example = st.selectbox("اختر مثالاً:", list(examples.keys()))
        
        query = st.text_area(
            "اكتب استعلام SQL:",
            value=examples[selected_example],
            height=150,
            help="استخدم data كاسم للجدول"
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            run = st.button("▶️ تشغيل", type="primary", use_container_width=True)
        with col2:
            if st.button("💾 حفظ في المفضلة"):
                if query not in st.session_state['sql_history']:
                    st.session_state['sql_history'].append(query)
                    st.success("✅ تم الحفظ!")
        
        if run:
            with st.spinner("⏳ جاري التنفيذ..."):
                result, error = run_sql_query(df, query)
                
                if error:
                    st.error(f"❌ خطأ في SQL: {error}")
                else:
                    st.success(f"✅ تم استرجاع {len(result):,} صف")
                    st.session_state['query_results'] = result
                    st.dataframe(result, use_container_width=True)
                    
                    if len(result) > 0:
                        st.markdown("### 📥 تصدير النتيجة:")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(get_download_link(result, "query_result.csv", "csv"), unsafe_allow_html=True)
                        with col2:
                            st.markdown(get_download_link(result, "query_result.xlsx", "excel"), unsafe_allow_html=True)
        
        if st.session_state['sql_history']:
            with st.expander("📜 سجل الاستعلامات المحفوظة"):
                for i, q in enumerate(st.session_state['sql_history'], 1):
                    st.code(q, language='sql')

elif menu_map[choice] == "AI":
    st.header("🤖 المساعد الذكي")
    
    if df is not None:
        question = st.text_input("اسأل عن بياناتك:", placeholder="مثال: ما إجمالي مبيعات الرياض؟")
        
        if question:
            response = f"*تحليل:* {question}\n\n"
            
            if "إجمالي" in question or "مجموع" in question:
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    total = df[numeric_cols[0]].sum()
                    response += f"الإجمالي: *{total:,.2f}*"
            
            elif "متوسط" in question:
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    avg = df[numeric_cols[0]].mean()
                    response += f"المتوسط: *{avg:,.2f}*"
            
            elif "عدد" in question:
                response += f"عدد الصفوف: *{len(df):,}*"
            
            else:
                response += f"البيانات تحتوي على {len(df):,} صف و {len(df.columns)} عمود."
            
            st.success(response)
    else:
        st.warning("⚠️ لا توجد بيانات")

elif menu_map[choice] == "Export":
    st.header("💾 مركز التصدير")
    
    if df is not None:
        st.markdown("### 📥 اختيار التنسيق:")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(get_download_link(df, f"beast_data_{datetime.now().strftime('%Y%m%d')}.csv", "csv"), unsafe_allow_html=True)
        with col2:
            st.markdown(get_download_link(df, f"beast_data_{datetime.now().strftime('%Y%m%d')}.xlsx", "excel"), unsafe_allow_html=True)
        with col3:
            json_data = df.to_json(orient='records', force_ascii=False)
            st.download_button("📥 JSON", json_data, f"beast_data_{datetime.now().strftime('%Y%m%d')}.json", "application/json")
        
        st.markdown("---")
        if st.button("📄 توليد تقرير ملخص", use_container_width=True):
            report = f"""
            تقرير Smart Analyst Beast
            =========================
            التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M')}
            
            ملخص البيانات:
            - الصفوف: {len(df):,}
            - الأعمدة: {len(df.columns)}
            - الأعمدة: {', '.join(df.columns[:10])}{'...' if len(df.columns) > 10 else ''}
            
            الإحصائيات:
            {df.describe().to_string()}
            """
            st.download_button("⬇️ تحميل التقرير", report, f"report_{datetime.now().strftime('%Y%m%d')}.txt", "text/plain")
    else:
        st.error("❌ لا توجد بيانات")

st.write("---")
st.caption("🦁 Smart Analyst Beast PRO v2.0 | صنع بحب ❤️")

if __name__ == "__main__":
    pass
