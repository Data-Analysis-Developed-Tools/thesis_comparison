import streamlit as st
import pandas as pd
import scipy.stats as stats
import pingouin as pg
from data_loader import load_data

# 🌟 Nuovo titolo con dimensione doppia
st.markdown("<h1 style='text-align: center; font-size: 170%;'>📊 Comparison Test Between Theses</h1>", unsafe_allow_html=True)

# 📂 Caricamento del file nella barra laterale
st.sidebar.header("⚙️ Settings")
uploaded_file = st.sidebar.file_uploader("📂 Upload an Excel file (.xlsx)", type=["xlsx"])

# 📌 Istruzioni aggiuntive sotto il caricamento del file
st.sidebar.markdown("📌 **Thesis name in first line. No header for repetition lines.**")
