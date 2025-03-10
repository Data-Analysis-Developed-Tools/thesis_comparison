import pandas as pd
import streamlit as st
import scipy.stats as stats

def load_data(uploaded_file):
    """Carica il file Excel e lo trasforma in DataFrame."""
    try:
        df = pd.read_excel(uploaded_file)
        return df  # Non rimuovo i NaN per non alterare il numero di osservazioni
    except Exception as e:
        st.error(f"❌ Errore nel caricamento del file: {e}")
        return None

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

    # 🔍 Test di normalità (Shapiro-Wilk)
    st.sidebar.subheader("📈 Test di Normalità e Varianza")
    st.sidebar.write("🧪 **Test di Normalità usato: Shapiro-Wilk**")
    
    normality_results = {}
    for thesis in df.columns:
        stat, p_value = stats.shapiro(df[thesis].dropna())  # Rimuove i NaN prima del test
        normality_results[thesis] = p_value

    # 📊 Mostra risultati del test di normalità
    for thesis, p_val in normality_results.items():
        result_text = "✅ Normale" if p_val > 0.05 else "⚠️ Non Normale"
        st.sidebar.write(f"**{thesis}**: p = {p_val:.4f} ({result_text})")

    # 🔍 Test di Levene per la varianza
    stat_levene, p_levene = stats.levene(*[df[col].dropna() for col in df.columns])
    variance_homogeneity = p_levene > 0.05
    levene_result_text = "✅ Varianze omogenee" if variance_homogeneity else "⚠️ Varianze eterogenee"
    st.sidebar.write(f"**Test di Levene**: p = {p_levene:.4f} ({levene_result_text})")

    return normality_results, variance_homogeneity
