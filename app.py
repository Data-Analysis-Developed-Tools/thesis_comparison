import streamlit as st
import pandas as pd
from data_loader import load_data
from tests import run_anova_tests

# 🌟 Nuovo titolo
st.title("📊 Comparison Test Between Theses")

# 📂 Caricamento del file nella barra laterale
st.sidebar.header("⚙️ Settings")
uploaded_file = st.sidebar.file_uploader("📂 Upload an Excel file (.xlsx)", type=["xlsx"])

# 📌 Controllo se è stato caricato un file
if uploaded_file:
    df = load_data(uploaded_file)  # 🔄 Carica i dati
    if df is not None:
        st.write("✅ **Data uploaded successfully!**")
        st.write(df.head())  # Mostra l'anteprima dei dati

        # 🏃‍♂️ Esegui i test
        results, interpretations = run_anova_tests(df)

        # 📝 Mostra i risultati in Streamlit
        for test_name, result in results.items():
            st.subheader(test_name)
            st.write(result)

            # 📌 Mostra il commento interpretativo per ogni test
            if test_name in interpretations:
                st.info(interpretations[test_name])

else:
    st.sidebar.warning("📂 Upload an Excel file to proceed.")
