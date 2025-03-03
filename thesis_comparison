import streamlit as st
import pandas as pd
from data_loader import load_data
from anova_analysis import run_anova_tests

# 🌟 Titolo dell'app
st.title("📊 Analisi ANOVA con Test Post-Hoc")

# 📂 Caricamento del file nella barra laterale
st.sidebar.header("⚙️ Impostazioni")
uploaded_file = st.sidebar.file_uploader("📂 Carica un file Excel (.xlsx)", type=["xlsx"])

# 📌 Controllo se è stato caricato un file
if uploaded_file:
    df = load_data(uploaded_file)  # 🔄 Carica i dati
    if df is not None:
        st.write("✅ **Dati caricati con successo!**")
        st.write(df.head())  # Mostra l'anteprima dei dati

        # 🏃‍♂️ Esegui i test
        results = run_anova_tests(df)

        # 📝 Mostra i risultati in Streamlit
        for test_name, result in results.items():
            st.subheader(test_name)
            st.write(result)
else:
    st.sidebar.warning("📂 Carica un file Excel per procedere.")
