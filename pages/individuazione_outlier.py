import pandas as pd
import numpy as np
import streamlit as st
from scipy import stats
from statsmodels.stats.outliers_influence import variance_inflation_factor

# 🔹 Titolo della pagina
st.markdown("<h3 style='text-align: center;'>📊 INDIVIDUAZIONE DEGLI OUTLIER</h3>", unsafe_allow_html=True)

# **Verifica se i dati sono disponibili in `st.session_state`**
if "uploaded_file" not in st.session_state or st.session_state["uploaded_file"] is None:
    st.error("⚠️ Nessun file caricato. Torna alla sezione 'Analisi Preliminare' e carica un file Excel prima di procedere.")
    st.stop()

# **Recuperiamo il file e il DataFrame**
uploaded_file = st.session_state["uploaded_file"]
df = pd.read_excel(uploaded_file)

st.success("✅ Dati caricati correttamente!")
st.dataframe(df.head())  # Mostra un'anteprima dei dati

# **Recuperiamo le colonne numeriche**
num_cols = df.select_dtypes(include=['number']).columns
if len(num_cols) < 2:
    st.error("⚠️ Il file deve contenere almeno due colonne numeriche per eseguire l'analisi degli outlier.")
    st.stop()

# **Definizione delle funzioni per i test di outlier**

### ✅ Test di Grubbs
def grubbs_test(data, alpha=0.05):
    """
    Test di Grubbs per identificare un singolo outlier in un dataset.
    """
    mean = np.mean(data)
    std_dev = np.std(data, ddof=1)
    G = np.abs(data - mean) / std_dev
    n = len(data)
    
    # Valore critico di Grubbs
    t = stats.t.ppf(1 - alpha / (2 * n), n - 2)
    G_crit = ((n - 1) / np.sqrt(n)) * np.sqrt(t**2 / (n - 2 + t**2))

    return G > G_crit, G, G_crit

### ✅ Test di Dixon (Q-test)
def dixon_q_test(data, alpha=0.05):
    """
    Test di Dixon per identificare un outlier nei dataset piccoli.
    """
    data_sorted = np.sort(data)
    Q_exp = (data_sorted[-1] - data_sorted[-2]) / (data_sorted[-1] - data_sorted[0])
    
    # Valori critici tabulati per il test di Dixon
    Q_crit = {5: 0.71, 10: 0.41, 20: 0.29}  # Per alcuni valori di n
    n = len(data_sorted)
    if n in Q_crit:
        return Q_exp > Q_crit[n], Q_exp, Q_crit[n]
    else:
        return False, Q_exp, None  # Non applicabile per n non tabulati

### ✅ Test di Rosner (per più outlier)
def rosner_test(data, alpha=0.05, max_outliers=3):
    """
    Test di Rosner per l'individuazione di più outlier.
    """
    outliers = []
    data_copy = np.copy(data)

    for _ in range(max_outliers):
        mean = np.mean(data_copy)
        std_dev = np.std(data_copy, ddof=1)
        R = np.abs(data_copy - mean) / std_dev

        # Calcola il valore critico
        n = len(data_copy)
        t = stats.t.ppf(1 - alpha / (2 * n), n - 2)
        R_crit = ((n - 1) / np.sqrt(n)) * np.sqrt(t**2 / (n - 2 + t**2))

        max_R_index = np.argmax(R)
        if R[max_R_index] > R_crit:
            outliers.append(data_copy[max_R_index])
            data_copy = np.delete(data_copy, max_R_index)  # Rimuove l'outlier individuato
        else:
            break

    return outliers, R, R_crit

# **Applicazione dei test a ciascuna tesi**
outlier_results = []

for col in num_cols:
    data = df[col].dropna().values
    
    # Test di Grubbs
    is_outlier_grubbs, G_values, G_crit = grubbs_test(data)
    
    # Test di Dixon
    is_outlier_dixon, Q_value, Q_crit = dixon_q_test(data)
    
    # Test di Rosner
    outliers_rosner, R_values, R_crit = rosner_test(data)

    outlier_results.append({
        "Tesi": col,
        "Grubbs (Outlier?)": "✅ Sì" if any(is_outlier_grubbs) else "❌ No",
        "Dixon (Outlier?)": "✅ Sì" if is_outlier_dixon else "❌ No",
        "Rosner (Outlier?)": f"{len(outliers_rosner)} rilevati" if outliers_rosner else "❌ No",
        "Dettagli Grubbs": f"G max={max(G_values):.2f}, G crit={G_crit:.2f}",
        "Dettagli Dixon": f"Q={Q_value:.2f}, Q crit={Q_crit:.2f}" if Q_crit else "N/A",
        "Dettagli Rosner": f"Outliers: {outliers_rosner}" if outliers_rosner else "N/A"
    })

# **Visualizzazione risultati**
results_df = pd.DataFrame(outlier_results)
st.subheader("📊 **Risultati dei Test di Outlier**")
st.dataframe(results_df, width=900)

# **Salviamo i risultati per la prossima pagina**
st.session_state["outlier_results"] = results_df

# **Pulsante per passare alla fase successiva (Applicazione Test)**
st.markdown("""
    <a href="/applicazione_test" target="_blank">
        <button style="background-color:#4CAF50;color:white;padding:10px;border:none;border-radius:5px;cursor:pointer;">
            🚀 Passa all'Applicazione del Test Statistico
        </button>
    </a>
""", unsafe_allow_html=True)
