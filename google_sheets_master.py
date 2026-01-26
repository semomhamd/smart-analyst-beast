import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import plotly.express as px

def run_sheets_app():
    # --- واجهة المستخدم الاحترافية ---
    st.markdown("<h2 style='color:#D4AF37; text-align:center;'>🌐 Beast Cloud Intelligence</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#888;'>الذاكرة السحابية النشطة | MIA8444 Edition</p>", unsafe_allow_html=True)

    # خانة إدخال الرابط
    sheet_url = st.text_input("🔗 ضع رابط Google Sheet هنا:", placeholder="https://docs.google.com/spreadsheets/d/...")

    if sheet_url:
        try:
            with st.spinner("⏳ جاري سحب البيانات من السحابة وتحليلها..."):
                # 1. إعداد المصادقة (تأكد من وجود ملف creds.json)
                scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
                creds = Credentials.from_service_account_file("creds.json", scopes=scope)
                client = gspread.authorize(creds)
                
                # 2. فتح الشيت وقراءة البيانات
                sh = client.open_by_url(sheet_url)
                df = pd.DataFrame(sh.get_worksheet(0).get_all_records())

            if not df.empty:
                st.success(f"✅ تم الاتصال بـ '{sh.title}'")

                # --- 3. لوحة المؤشرات (KPIs) ---
                num_cols = df.select_dtypes(include=['number']).columns
                if len(num_cols) > 0:
                    k1, k2, k3 = st.columns(3)
                    with k1:
                        st.metric("إجمالي القيم (SUM)", f"{df[num_cols[0]].sum():,.0f}")
                    with k2:
                        st.metric("المتوسط (AVG)", f"{df[num_cols[0]].mean():,.1f}")
                    with k3:
                        st.metric("أعلى سجل (MAX)", f"{df[num_cols[0]].max():,.0f}")

                    # --- 4. الرسوم البيانية عالية المستوى (Plotly) ---
                    st.markdown("---")
                    c1, c2 = st.columns(2)
                    
                    with c1:
                        fig_pie = px.pie(df, names=df.columns[0], values=num_cols[0], 
                                         hole=0.5, template="plotly_dark",
                                         color_discrete_sequence=['#D4AF37', '#E5E4E2', '#808080'])
                        fig_pie.update_layout(title="تحليل الحصص والنسب", title_x=0.5)
                        st.plotly_chart(fig_pie, use_container_width=True)

                    with c2:
                        fig_trend = px.area(df, x=df.columns[0], y=num_cols[0],
                                            template="plotly_dark", color_discrete_sequence=['#D4AF37'])
                        fig_trend.update_layout(title="منحنى الأداء الزمني", title_x=0.5)
                        st.plotly_chart(fig_trend, use_container_width=True)

                # --- 5. استعراض البيانات السحابية ---
                with st.expander("🔍 معاينة قاعدة البيانات الحية"):
                    st.dataframe(df.style.background_gradient(cmap='YlOrBr'), use_container_width=True)
            
        except Exception as e:
            st.error("⚠️ فشل الاتصال: تأكد من مشاركة الشيت مع البريد الموجود في creds.json")

# التوقيع MIA8444
st.markdown("<br><p style='text-align:center; color:#555;'>Designed by MIA8444 | Beast Edition 2026</p>", unsafe_allow_html=True)
