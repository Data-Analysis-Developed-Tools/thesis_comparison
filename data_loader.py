import pandas as pd
import streamlit as st
import scipy.stats as stats

# 🛠️ Inizializza `session_state`
if "final_data" not in st.session_state:
    st.session_state["final_data"] = None

if "confidence_level" not in st.session_state:
    st.session_state["confidence_level"] = None

if "file_uploaded" not in st.session_state:
    st.session_state["file_uploaded"] = False

if "preliminary_tests" not in st.session_state:
    st.session_state["preliminary_tests"] = None

# 📂 Caricamento del file
uploaded_file = st.sidebar.file_uploader("📂 Carica un file Excel (.xlsx)", type=["xlsx"])

# 🔹 Reset se il file viene rimosso
if uploaded_file is None:
    st.session_state["file_uploaded"] = False
    st.session_state["confidence_level"] = None
    st.session_state["preliminary_tests"] = None
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
            st.rerun()  # 🔄 Forza il refresh dopo la conferma

    else:
        # ✅ Usa il valore memorizzato nel session state invece di una variabile non definita
        confidence_display = [key for key, value in confidence_options.items() if value == st.session_state["confidence_level"]][0]
        st.sidebar.success(f"✅ Livello di confidenza selezionato: {confidence_display}")

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
        """Esegue i test preliminari e salva i risultati."""
        
        num_theses = len(df.columns)  # Numero di tesi
        observations_per_thesis = {col: df[col].notna().sum() for col in df.columns}
        obs_values = list(observations_per_thesis.values())
        imbalance_index = imbalance_coefficient(obs_values)

        alpha = st.session_state["confidence_level"]
        normality_results = {col: stats.shapiro(df[col].dropna())[1] for col in df.columns}
        levene_stat, levene_p = stats.levene(*[df[col].dropna() for col in df.columns])

        return {
            "num_theses": num_theses,
            "observations": observations_per_thesis,
            "imbalance_index": imbalance_index,
            "normality_results": normality_results,
            "levene_p": levene_p
        }

    # 📝 Esegui i test preliminari
    test_results = preliminary_tests(df)

    # ✅ Passa i dati ad `app.py`
    st.session_state["final_data"] = df  # Salva il dataframe
    st.session_state["preliminary_tests"] = test_results  # Salva i risultati dei test

    # 📌 Visualizza i risultati nella sidebar
    st.sidebar.success("✅ Test preliminari completati!")
    st.sidebar.write(f"📊 **Numero di tesi a confronto:** {test_results['num_theses']}")
    st.sidebar.write(f"⚖️ **Indice di Squilibrio (I):** {test_results['imbalance_index']:.4f}")

    levene_text = "✅ Varianze omogenee" if test_results["levene_p"] > alpha else "⚠️ Varianze eterogenee"
    st.sidebar.write(f"📏 **Test di Levene (omogeneità della varianza):** p = {test_results['levene_p']:.4f} ({levene_text})")

    st.sidebar.subheader("📈 **Test di Normalità (Shapiro-Wilk)**")
    for thesis, p_value in test_results["normality_results"].items():
        result_text = "✅ Normale" if p_value > alpha else "⚠️ Non Normale"
        st.sidebar.write(f"**{thesis}**: p = {p_value:.4f} ({result_text})")

    st.sidebar.info("Passa ad `app.py` per continuare l'analisi statistica!")
