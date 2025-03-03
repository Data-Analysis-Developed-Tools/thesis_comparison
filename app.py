import streamlit as st
import pandas as pd
from data_loader import load_data
from tests import run_anova_tests

# 🌟 Nuovo titolo con dimensione intermedia
st.markdown("<h2 style='text-align: center; font-size: 85%;'>📊 Comparison Test Between Theses</h2>", unsafe_allow_html=True)

# 📂 Caricamento del file nella barra laterale
st.sidebar.header("⚙️ Settings")
uploaded_file = st.sidebar.file_uploader("📂 Upload an Excel file (.xlsx)", type=["xlsx"])

# 📌 Istruzioni aggiuntive sotto il caricamento del file
st.sidebar.markdown("📌 **Thesis name in first line. No header for repetition lines.**")

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

            # 📌 Converte i risultati in DataFrame se necessario
            if isinstance(result, pd.DataFrame):
                st.dataframe(result, use_container_width=True)
            elif isinstance(result, dict):
                st.json(result)  # Per debug, mostra i dizionari
            else:
                st.write(result)  # Per stringhe e altri valori

            # 📌 Mostra il commento interpretativo per ogni test
            if test_name in interpretations:
                st.info(interpretations[test_name])

else:
    st.sidebar.warning("📂 Upload an Excel file to proceed.")
