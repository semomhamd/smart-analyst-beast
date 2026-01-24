import streamlit as st
import pandas as pd
import numpy as np
import os
import google.generativeai as genai
from datetime import datetime

# إعداد الصفحة والستايل المظلم
st.set_page_config(page_title="Smart Analyst Beast", page_icon="🐉", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #121212; color: white; }
    [data-testid="stSidebar"] { background-color: #1E1E1E !important; }
    .stButton>button { background-color: #00C853; color: white; border-radius: 8px; border: none; height: 3em; font-weight: bold; }
    .stTabs [data-baseweb="tab-list"] { background-color: #121212; }
    .stTabs [data-baseweb="tab"] { color: white; background-color: #1E1E1E; border-radius: 5px; margin: 2px; }
    </style>
    """, unsafe_allow_input=True)

# القائمة الجانبية (Sidebar)
with st.sidebar:
    st.title("⚙️ Settings")
    lang = st.selectbox("Language", ["العربية", "English"])
    st.markdown("---")
    st.write("👤 User: MIA8444")
    st.write("🚀 Version: 2.5.0")
