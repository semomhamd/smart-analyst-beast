import streamlit as st
import pandas as pd
import numpy as np
import os
import google.generativeai as genai
from datetime import datetime
import io

# ================== 1. إعدادات الثيم والجماليات ==================
st.set_page_config(page_title="Smart Analyst Beast", page_icon="🐉", layout="wide")

# نظام تبديل الدارك واللايت مود في الإعدادات
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

theme_css = {
    'dark': {"bg": "#0E1117", "text": "white", "card": "#1E1E1E", "btn": "#00C853"},
    'light': {"bg": "#F0F2F6", "text": "black", "card": "white", "btn": "#00A36C"}
}

curr = theme_css[st.session_state.theme]

st.markdown(f"""
    <style>
    .stApp {{ background-color: {curr['bg']}; color: {curr['text']}; }}
    [data-testid="st…
