import pandas as pd
import streamlit as st

# Opzioni per la significatività statistica
sig_levels = {
    "90% (α = 0.10)": 0.10,
    "95% (α = 0.05)": 0.05,
    "99% (α = 0.01)": 0.01,
    "99.9% (α = 0.001)": 0.001
}

# Memorizzazione dello stato della selezione
if "significance_level" not in st.session_state:
    st.session_state["significance_level"] = 0.05  # Default: 95%

# Dropdown per la selezione del livello di significatività
selected_level = st.selectbox(
    "📊 Seleziona il livello di significatività:",
    options=list(sig_levels.keys()),
    index=1  # 95% di default
)

# Salvataggio del valore scelto
st.session_state["significance_level"] = sig_levels[selected_level]

# Upload file
uploaded_file = st.file_uploader("📂 Carica un file Excel (.xlsx)", type=["xlsx"])

def load_data(uploaded_file):
    """Carica il file Excel e lo trasforma in DataFrame."""
    try:
        df = pd.read_excel(uploaded_file)
        df = df.dropna()  # Rimuove i valori mancanti
        return df
    except Exception as e:
        st.error(f"❌ Errore nel caricamento del file: {e}")
        return None

# Controllo sulla rimozione del file
if uploaded_file is not None:
    df = load_data(uploaded_file)
    if df is not None:
        st.write("✅ **File caricato con successo!**")
        st.dataframe(df.head())  # Mostra un'anteprima del DataFrame
        st.write(f"🔬 **Livello di significatività selezionato:** {selected_level} (α = {st.session_state['significance_level']})")
else:
    # Resetta il livello di significatività se il file viene rimosso
    if "significance_level" in st.session_state:
        del st.session_state["significance_level"]
    st.rerun()  # Forza il ricaricamento dell'interfaccia per mostrare di nuovo la selezione
