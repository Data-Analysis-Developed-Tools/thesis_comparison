import pandas as pd
import numpy as np
import streamlit as st
from scipy import stats

# 🔹 Titolo della pagina
st.markdown("<h3 style='text-align: center;'>📊 INDIVIDUAZIONE DEGLI OUTLIER</h3>", unsafe_allow_html=True)

# ✅ Controlliamo che "num_cols" e "df" siano disponibili
if "num_cols" not in st.session_state or "df" not in st.session_state:
    st.warning("⚠️ I dati non sono disponibili. Assicurati di completare l'Analisi Preliminare prima di procedere.")
    st.stop()

num_cols = st.session_state["num_cols"]
df = st.session_state["df"]

# **Definizione delle funzioni per i test di outlier**

### ✅ Test di Grubbs
def grubbs_test(data, alpha=0.05):
    """Identifica un singolo outlier nei dati normalmente distribuiti."""
    mean = np.mean(data)
    std_dev = np.std(data, ddof=1)
    G = np.abs(data - mean) / std_dev
    n = len(data)

    t = stats.t.ppf(1 - alpha / (2 * n), n - 2)
    G_crit = ((n - 1) / np.sqrt(n)) * np.sqrt(t**2 / (n - 2 + t**2))

    return G > G_crit, G, G_crit

### ✅ Test di Dixon (Q-test)
def dixon_q_test(data, alpha=0.05):
    """Identifica un outlier nei dataset piccoli."""
    data_sorted = np.sort(data)
    if len(data_sorted) < 3:
        return False, None, None  # Non applicabile se ci sono meno di 3 valori

    Q_exp = (data_sorted[-1] - data_sorted[-2]) / (data_sorted[-1] - data_sorted[0])
    Q_crit = {5: 0.71, 10: 0.41, 20: 0.29}  # Valori critici tabulati
    n = len(data_sorted)

    if n in Q_crit:
        return Q_exp > Q_crit[n], Q_exp, Q_crit[n]
    else:
        return False, Q_exp, None  # Non applicabile per n non tabulati

### ✅ Test di Rosner
def rosner_test(data, alpha=0.05, max_outliers=3):
    """Identifica più outlier contemporaneamente."""
    outliers = []
    data_copy = np.copy(data)

    for _ in range(max_outliers):
        mean = np.mean(data_copy)
        std_dev = np.std(data_copy, ddof=1)
        R = np.abs(data_copy - mean) / std_dev

        n = len(data_copy)
        t = stats.t.ppf(1 - alpha / (2 * n), n - 2)
        R_crit = ((n - 1) / np.sqrt(n)) * np.sqrt(t**2 / (n - 2 + t**2))

        max_R_index = np.argmax(R)
        if R[max_R_index] > R_crit:
            outliers.append(float(data_copy[max_R_index]))  # Convertiamo il valore in float normale
            data_copy = np.delete(data_copy, max_R_index)
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
        "Dettagli Dixon": f"Q={Q_value:.2f}, Q crit={Q_crit:.2f}" if Q_crit else "Non applicabile",
        "Dettagli Rosner": f"Outliers: {', '.join(map(str, outliers_rosner))}" if outliers_rosner else "Nessun outlier"
    })

# **Visualizzazione risultati**
results_df = pd.DataFrame(outlier_results)
st.subheader("📊 **Risultati dei Test di Outlier**")
st.dataframe(results_df, width=900)

# **Spiegazione dei test**
st.markdown("""
### 📌 **Descrizione dei test utilizzati**
✔ **Test di Grubbs**: Identifica un singolo outlier nei dati normalmente distribuiti. Utilizzato in contesti normativi come **ASTM E178** e **ISO 5725**.  
✔ **Test di Dixon (Q-test)**: Adatto per dataset **piccoli**. Raccomandato dall'**IUPAC** per la validazione di metodi chimici.  
✔ **Test di Rosner**: Permette di identificare **più outlier contemporaneamente**. Applicato nei laboratori chimici per analisi robuste.  
""")

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
