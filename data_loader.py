import pandas as pd
import streamlit as st
import scipy.stats as stats

# Inizializza session_state per gestire i dati
if "final_data" not in st.session_state:
    st.session_state["final_data"] = None  # Contiene i dati finalizzati per app.py

if "confidence_level" not in st.session_state:
    st.session_state["confidence_level"] = None

if "file_uploaded" not in st.session_state:
    st.session_state["file_uploaded"] = False

# 📂 Caricamento del file
uploaded_file = st.sidebar.file_uploader("📂 Carica un file Excel (.xlsx)", type=["xlsx"])

# 🔹 Reset se il file viene rimosso
if uploaded_file is None:
    st.session_state["file_uploaded"] = False
    st.session_state["confidence_level"] = None
    st.session_state["final_data"] = None  # Cancella i dati precedenti

def load_data(uploaded_file):
    """Carica il file Excel e lo trasforma in DataFrame."""
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            st.session_state["file_uploaded"] = True
            return df
        except Exception as e:
            st.error(f"❌ Errore nel caricamento del file: {e}")
            return None
    return None

df = load_data(uploaded_file)

# 🔹 Mostra il menu SOLO dopo che il file è stato caricato
if st.session_state["file_uploaded"]:
    st.sidebar.subheader("⚙️ Selezione del Livello di Confidenza")

    confidence_options = {"90%": 0.10, "95%": 0.05, "99%": 0.01, "99.9%": 0.001}

    if st.session_state["confidence_level"] is None:
        selected_confidence = st.sidebar.selectbox(
            "📊 Scegli il livello di confidenza statistica:",
            options=list(confidence_options.keys()),
            index=1  # Default: 95%
        )

        if st.sidebar.button("✅ Conferma Livello di Confidenza"):
            st.session_state["confidence_level"] = confidence_options[selected_confidence]
            st.experimental_rerun()

    else:
        st.sidebar.success(f"✅ Livello di confidenza selezionato: {selected_confidence}")

# 🔹 Se il livello di confidenza non è stato selezionato, blocca il workflow
if st.session_state["file_uploaded"] and st.session_state["confidence_level"] is None:
    st.warning("⚠️ Seleziona il livello di confidenza per continuare.")
    st.stop()

# ✅ Esegui i test SOLO dopo la selezione del livello di confidenza
if df is not None and st.session_state["confidence_level"] is not None:
    
    def imbalance_coefficient(observations):
        """Calcola il Coefficiente di Squilibrio (I) adattandolo al numero di gruppi."""
        k = len(observations)
        if k == 2:
            n1, n2 = observations
            I = abs(n1 - n2) / (n1 + n2) if (n1 + n2) > 0 else None
        else:
            mean_n = sum(observations) / k
            I = sum(abs(n - mean_n) for n in observations) / (k * mean_n) if mean_n > 0 else None
        return I

    def preliminary_tests(df):
        """Esegue i test preliminari e mostra i risultati nella sidebar."""
        
        num_theses = len(df.columns)
        st.sidebar.subheader("📊 Panoramica del Dataset")
        st.sidebar.write(f"🔢 **Numero di Tesi:** {num_theses}")

        observations_per_thesis = {col: df[col].notna().sum() for col in df.columns}
        for thesis, count in observations_per_thesis.items():
            st.sidebar.write(f"**{thesis}**: {count} osservazioni")

        alpha = st.session_state["confidence_level"]
        normality_results = {}
        for thesis in df.columns:
            stat, p_value = stats.shapiro(df[thesis].dropna())
            result_text = "✅ Normale" if p_value > alpha else "⚠️ Non Normale"
            normality_results[thesis] = p_value
            st.sidebar.write(f"**{thesis}**: p = {p_value:.4f} ({result_text})")

        return normality_results

    # 📝 Esegui i test
    test_results = preliminary_tests(df)

    # ✅ Passa i dati ad `app.py`
    st.session_state["final_data"] = df  # Salva il dataframe pronto per app.py
    st.session_state["test_results"] = test_results  # Salva i risultati dei test
    st.sidebar.success("✅ Analisi completata! Passa a `app.py` per la visualizzazione.")

