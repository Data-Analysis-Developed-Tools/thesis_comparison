import pandas as pd
import streamlit as st
from scipy.stats import levene, shapiro

# 🔹 Titolo dell'app
st.markdown("<h3 style='text-align: center;'>📊 CONFRONTO FRA TESI CON VARIE RIPETIZIONI</h3>", unsafe_allow_html=True)

# Opzioni per la significatività statistica
sig_levels = {
    "90% (α = 0.10)": 0.10,
    "95% (α = 0.05)": 0.05,
    "99% (α = 0.01)": 0.01,
    "99.9% (α = 0.001)": 0.001
}

# Selezione del livello di significatività
selected_level = st.selectbox(
    "📊 Seleziona il livello di significatività prima di caricare il file:",
    options=list(sig_levels.keys()),
    index=1  # Default: 95%
)

# Memorizzazione del valore scelto
alpha = sig_levels[selected_level]

# Upload del file Excel
uploaded_file = st.file_uploader("📂 Carica un file Excel (.xlsx)", type=["xlsx"])

def load_data(uploaded_file):
    """Carica il file Excel e lo trasforma in DataFrame."""
    try:
        df = pd.read_excel(uploaded_file)
        return df
    except Exception as e:
        st.error(f"❌ Errore nel caricamento del file: {e}")
        return None

# Se un file è stato caricato, eseguire l'analisi
if uploaded_file is not None:
    df = load_data(uploaded_file)
    if df is not None:
        st.write("✅ **File caricato con successo!**")
        st.dataframe(df.head())  # Mostra un'anteprima del DataFrame
        st.write(f"🔬 **Livello di significatività selezionato:** {selected_level} (α = {alpha})")

        # **Salviamo il file e il livello di significatività in `st.session_state`**
        st.session_state["uploaded_file"] = uploaded_file
        st.session_state["alpha"] = alpha

        # Verifica se ci sono almeno due colonne numeriche
        num_cols = df.select_dtypes(include=['number']).columns

        if len(num_cols) < 2:
            st.warning("⚠️ Sono necessarie almeno due colonne numeriche per il test di Levene.")
        else:
            # **Calcolo del Rapporto di Disuguaglianza (Max/Min)**
            count_values = df[num_cols].count()
            min_n = count_values.min()
            max_n = count_values.max()
            inequality_ratio = max_n / min_n if min_n > 0 else float('inf')

            # **Test di Levene per l'uguaglianza delle varianze**
            levene_stat, levene_p = levene(*[df[col].dropna() for col in num_cols])
            varianze_uguali = levene_p > alpha

            # **Test di Shapiro-Wilk per la normalità**
            normalita = {col: shapiro(df[col].dropna())[1] > alpha for col in num_cols}
            almeno_una_non_normale = not all(normalita.values())

            # ✅ Esportiamo i risultati per `test_selection.py`
            st.session_state["num_cols"] = num_cols
            st.session_state["inequality_ratio"] = inequality_ratio
            st.session_state["varianze_uguali"] = varianze_uguali
            st.session_state["almeno_una_non_normale"] = almeno_una_non_normale

            # **Output compatto sotto forma di tabella**
            results_df = pd.DataFrame({
                "Parametro": ["Numero Min. Osservazioni", "Numero Max. Osservazioni", "Rapporto Max/Min", 
                              "Statistiche Levene", "p-value Levene", "Varianze Uguali", 
                              "Almeno una distribuzione NON normale"],
                "Valore": [min_n, max_n, f"{inequality_ratio:.2f}", 
                           f"{levene_stat:.4f}", f"{levene_p:.4f}", 
                           "✅ Sì" if varianze_uguali else "❌ No",
                           "❌ Sì" if almeno_una_non_normale else "✅ No"]
            })

            st.subheader("📊 **Risultati dell'Analisi Preliminare**")
            st.dataframe(results_df, width=600)

            # **Pulsante per aprire test_selection.py**
            st.markdown("""
                <a href="/test_selection" target="_blank">
                    <button style="background-color:#4CAF50;color:white;padding:10px;border:none;border-radius:5px;cursor:pointer;">
                        🚀 Esegui il test statistico appropriato
                    </button>
                </a>
            """, unsafe_allow_html=True)
