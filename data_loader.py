import pandas as pd
import streamlit as st

def load_data(uploaded_file):
    """Carica il file Excel e lo trasforma in DataFrame."""
    try:
        df = pd.read_excel(uploaded_file)
        df = df.dropna()  # Rimuove i valori mancanti
        return df
    except Exception as e:
        st.error(f"❌ Errore nel caricamento del file: {e}")
        return None
