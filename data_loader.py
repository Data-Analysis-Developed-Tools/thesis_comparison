import pandas as pd
import streamlit as st
import scipy.stats as stats

# 🔍 Selezione del livello di confidenza (sempre visibile)
st.sidebar.subheader("📊 Impostazioni Statistiche")
confidence_options = {"90%": 0.10, "95%": 0.05, "99%": 0.01, "99.9%": 0.001}
selected_confidence = st.sidebar.selectbox(
    "📊 Scegli il livello di confidenza statistica:",
    options=list(confidence_options.keys()),
    index=1  # Default: 95%
)
alpha = confidence_options[selected_confidence]
st.session_state["confidence_level"] = alpha  # Salviamo il valore scelto

def load_data(uploaded_file):
    """Carica il file Excel e lo trasforma in DataFrame."""
    try:
        df = pd.read_excel(uploaded_file)
        return df  # Non rimuovo i NaN per non alterare il numero di osservazioni
    except Exception as e:
        st.error(f"❌ Errore nel caricamento del file: {e}")
        return None

def imbalance_coefficient(observations):
    """Calcola il Coefficiente di Squilibrio (I) adattandolo al numero di gruppi."""
    k = len(observations)

    if k == 2:
        # Caso speciale per 2 gruppi: differenza relativa
        n1, n2 = observations
        I = abs(n1 - n2) / (n1 + n2) if (n1 + n2) > 0 else None
    else:
        # Formula standard per k > 2
        mean_n = sum(observations) / k
        I = sum(abs(n - mean_n) for n in observations) / (k * mean_n) if mean_n > 0 else None

    return I

def preliminary_tests(df):
    """Esegue i test preliminari e mostra i risultati nella sidebar."""
    
    num_theses = len(df.columns)
    st.sidebar.subheader("📊 Panoramica del Dataset")
    st.sidebar.write(f"🔢 **Numero di Tesi:** {num_theses}")

    # 🔍 Conta le osservazioni non nulle per ogni tesi
    st.sidebar.subheader("📊 Numero di Osservazioni per Tesi")
    observations_per_thesis = {col: df[col].notna().sum() for col in df.columns}
    for thesis, count in observations_per_thesis.items():
        st.sidebar.write(f"**{thesis}**: {count} osservazioni")

    # 📊 Calcolo del Coefficiente di Squilibrio (I)
    obs_values = list(observations_per_thesis.values())
    I_index = imbalance_coefficient(obs_values)

    if I_index is not None:
        st.sidebar.subheader("⚖️ Coefficiente di Squilibrio")
        st.sidebar.write(f"📊 **I = {I_index:.4f}**")
        if I_index < 0.10:
            st.sidebar.success("✅ **Gruppi bilanciati**")
        elif I_index < 0.20:
            st.sidebar.warning("⚠️ **Moderato sbilanciamento**")
        else:
            st.sidebar.error("❌ **Forte sbilanciamento**")

    # 🔍 Test di normalità (Shapiro-Wilk) usando il livello di confidenza selezionato
    st.sidebar.subheader("📈 Test di Normalità e Varianza")
    st.sidebar.write("🧪 **Test di Normalità usato: Shapiro-Wilk**")
    
    normality_results = {}
    for thesis in df.columns:
        stat, p_value = stats.shapiro(df[thesis].dropna())  # Rimuove i NaN prima del test
        result_text = "✅ Normale" if p_value > alpha else "⚠️ Non Normale"
        normality_results[thesis] = p_value
        st.sidebar.write(f"**{thesis}**: p = {p_value:.4f} ({result_text})")

    # 🔍 Test di Levene per la varianza usando il livello di confidenza selezionato
    stat_levene, p_levene = stats.levene(*[df[col].dropna() for col in df.columns])
    variance_homogeneity = p_levene > alpha
    levene_result_text = "✅ Varianze omogenee" if variance_homogeneity else "⚠️ Varianze eterogenee"
    st.sidebar.write(f"**Test di Levene**: p = {p_levene:.4f} ({levene_result_text})")

    return normality_results, variance_homogeneity
