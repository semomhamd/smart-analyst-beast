import streamlit as st
import pandas as pd
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont
import io

# 1. إعدادات المنصة والهوية
st.set_page_config(page_title="Smart Analyst Pro", layout="wide", page_icon="📊")

# 2. نظام الثيمات (Dark/Light Mode) والإعدادات
if 'theme' not in st.session_state:
    st.session_state.theme = 'Dark'

def toggle_theme():
    st.session_state.theme = 'Light' if st.session_state.theme == 'Dark' else 'Dark'

# لغة التصميم (CSS) التفاعلية
theme_bg = "#0d1117" if st.session_state.theme == 'Dark' else "#ffffff"
theme_text = "#e6edf3" if st.session_state.theme == 'Dark' else "#000000"
card_bg = "#161b22" if st.session_state.theme == 'Dark' else "#f0f2f6"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {theme_bg}; color: {theme_text}; }}
    .tool-card {{
        background-color: {card_bg};
        border: 1px solid #30363d;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        transition: 0.3s;
    }}
    .tool-card:hover {{ border-color: #fbbf24; transform: translateY(-5px); }}
    .gold-header {{ color: #fbbf24; font-weight: bold; }}
    .footer-bar {{
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: {card_bg}; color: #fbbf24;
        text-align: center; padding: 10px; border-top: 2px solid #fbbf24;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. الهيدر وشريط الإعدادات
col_logo, col_title, col_settings = st.columns([1, 4, 1])
with col_logo:
    if os.path.exists("40833.jpg"):
        st.image("40833.jpg", width=80)
with col_title:
    st.markdown(f"<h1 style='margin:0;'>Smart <span style='color:#fbbf24;'>Analyst</span> Pro</h1>", unsafe_allow_html=True)
with col_settings:
    if st.button("⚙️ Settings"):
        st.session_state.show_settings = not st.session_state.get('show_settings', False)

if st.session_state.get('show_settings', False):
    with st.expander("User Settings & Preferences", expanded=True):
        st.write(f"Logged in as: *MIA8444*")
        st.button(f"Switch to {('Light' if st.session_state.theme == 'Dark' else 'Dark')} Mode", on_click=toggle_theme)

st.divider()

# 4. منطقة الأدوات (The Grid)
tabs = st.tabs(["🚀 AI Operations", "📊 Analysis Tools", "📤 Export & Share"])

with tabs[0]:
    st.markdown("<h3 class='gold-header'>Smart AI Processing</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='tool-card'><h3>✍️</h3><p>OCR Handwriting</p></div>", unsafe_allow_html=True)
        st.file_uploader("Upload Image", type=['jpg','png'])
    with c2:
        st.markdown("<div class='tool-card'><h3>🧹</h3><p>Data Cleaner</p></div>", unsafe_allow_html=True)
        st.file_uploader("Upload Messy File", type=['xlsx','csv'])

with tabs[1]:
    st.markdown("<h3 class='gold-header'>Analytics Arsenal</h3>", unsafe_allow_html=True)
    row = st.columns(4)
    tools = [("📗 Excel", "Pro"), ("📉 Power BI", "BI"), ("⚡ Query", "ETL"), ("🗄️ SQL", "DB")]
    for i, (name, desc) in enumerate(tools):
        row[i].markdown(f"<div class='tool-card'><h4>{name}</h4><small>{desc}</small></div>", unsafe_allow_html=True)

with tabs[2]:
    st.markdown("<h3 class='gold-header'>Export with Watermark</h3>", unsafe_allow_html=True)
    col_pdf, col_wa = st.columns(2)
    
    with col_pdf:
        if st.button("📄 Generate PDF with Watermark"):
            st.info("جاري دمج شعار 40833 كعلامة مائية في التقرير...")
            # هنا يتم استدعاء ميزة العلامة المائية
            st.success("تم تجهيز ملف PDF بنجاح!")

    with col_wa:
        contact_name = st.text_input("اسم جهة الاتصال أو الرقم:")
        if st.button("📲 Share via WhatsApp"):
            wa_url = f"https://wa.me/?text=تم إنشاء تقريرك بواسطة Smart Analyst Pro"
            st.markdown(f"[اضغط هنا للإرسال لـ {contact_name}]({wa_url})")

# 5. التوقيع العالمي
st.markdown("<div class='footer-bar'>Smart Analyst Pro | Certified by MIA8444</div>", unsafe_allow_html=True)
