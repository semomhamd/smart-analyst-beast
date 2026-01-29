import pandas as pd
import streamlit as st

class SmartBeastAnalyst:
    def _init_(self, dataframe):
        self.df = dataframe
        self.signature = "MIA8444"

    def get_basic_stats(self):
        """تحليل إحصائي سريع وشامل"""
        stats = {
            "rows": self.df.shape[0],
            "cols": self.df.shape[1],
            "numeric_summary": self.df.describe().to_dict(),
            "missing_values": self.df.isnull().sum().sum()
        }
        return stats

    def generate_ai_insights(self):
        """توليد تحليلات ذكية بأسلوب الوحش التقني"""
        st.subheader(f"🚀 تحليل الذكاء الاصطناعي - بصمة {self.signature}")
        
        # تحليل الأعمدة الرقمية
        numeric_cols = self.df.select_dtypes(include=['number']).columns
        
        if len(numeric_cols) > 0:
            for col in numeric_cols:
                max_val = self.df[col].max()
                min_val = self.df[col].min()
                avg_val = self.df[col].mean()
                
                # رسالة ذكية لكل عمود
                st.info(f"📊 *عمود {col}:* المتوسط هو {avg_val:.2f}. "
                        f"أعلى قيمة سجلناها هي {max_val} وأقل قيمة هي {min_val}.")
        
        # كشف القيم المفقودة
        if self.df.isnull().sum().sum() > 0:
            st.warning("⚠️ يا وحش، فيه بيانات ناقصة! محتاجين نستخدم 'Cleaner Pro' لتنظيفها.")
        else:
            st.success("✅ البيانات زي الفل وجاهزة للاكتساح!")

    def show_beast_footer(self):
        """توقيع الملكية الخاص بك"""
        st.markdown("---")
        st.markdown(f"<p style='text-align: center; color: gold;'>Smart Analyst Beast - Powered by {self.signature}</p>", unsafe_allow_index=True)

# دالة التشغيل الأساسية اللي هتنادي عليها في app.py
def run_analysis(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
        analyst = SmartBeastAnalyst(df)
        analyst.generate_ai_insights()
        analyst.show_beast_footer()
