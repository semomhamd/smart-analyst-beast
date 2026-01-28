import streamlit as st

def run_powerbi():
    # عنوان الأداة بتنسيق ذهبي فخم
    st.markdown("<h2 style='text-align:center; color:#D4AF37;'>📈 Power BI Analyst Center</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#ffffff;'>مركز تحليل وربط تقارير البور بي أي الذكي</p>", unsafe_allow_html=True)
    
    st.info("💡 هنا يمكنك ربط تقارير Power BI المنشورة (Embed) لعرضها مباشرة داخل الوحش.")

    # خانة إدخال الرابط (URL)
    report_url = st.text_input("قم بلصق رابط تقرير Power BI (Embed URL) هنا:", 
                               placeholder="https://app.powerbi.com/view?r=...")

    if report_url:
        if "app.powerbi.com" in report_url:
            st.success("✅ تم التعرف على الرابط، جاري تحميل التقرير...")
            # عرض التقرير داخل iFrame احترافي
            st.markdown(f"""
                <iframe title="PowerBI Report" width="100%" height="600" 
                src="{report_url}" frameborder="0" allowFullScreen="true">
                </iframe>
            """, unsafe_allow_html=True)
        else:
            st.error("❌ عذراً، هذا الرابط لا يبدو كرابط Power BI صحيح.")

    st.markdown("---")
    # توقيعك MIA8444 ثابت في كل أداة
    st.markdown("<p style='text-align:center; font-size:12px; color:#555;'>MIA8444 | Smart Analyst BI Engine</p>", unsafe_allow_html=True)

if _name_ == "_main_":
