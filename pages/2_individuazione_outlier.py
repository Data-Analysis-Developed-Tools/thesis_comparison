import pandas as pd
import numpy as np
import streamlit as st
from scipy import stats

st.markdown("<h3 style='text-align: center;'>📊 INDIVIDUAZIONE DEGLI OUTLIER</h3>", unsafe_allow_html=True)

# ✅ Controllo dati
if "num_cols" not in st.session_state or "df" not in st.session_state:
    st.warning("⚠️ I dati non sono disponibili. Torna alla sezione 'Analisi Preliminare'.")
    st.stop()

num_cols = st.session_state["num_cols"]
df = st.session_state["df"]

# 🔹 Funzioni dei test

def grubbs_test(data, alpha=0.05):
    mean = np.mean(data)
    std_dev = np.std(data, ddof=1)
    G = np.abs(data - mean) / std_dev
    n = len(data)
    t = stats.t.ppf(1 - alpha / (2 * n), n - 2)
    G_crit = ((n - 1) / np.sqrt(n)) * np.sqrt(t**2 / (n - 2 + t**2))
    return G > G_crit, G, G_crit

def dixon_q_test(data, alpha=0.05):
    data_sorted = np.sort(data)
    if len(data_sorted) < 3:
        return False, None, None
    Q_exp = (data_sorted[-1] - data_sorted[-2]) / (data_sorted[-1] - data_sorted[0])
    Q_crit = {5: 0.71, 10: 0.41, 20: 0.29}
    n = len(data_sorted)
    if n in Q_crit:
        return Q_exp > Q_crit[n], Q_exp, Q_crit[n]
    else:
        return False, Q_exp, None

def rosner_test(data, alpha=0.05, max_outliers=3):
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
            outliers.append(float(data_copy[max_R_index]))
            data_copy = np.delete(data_copy, max_R_index)
        else:
            break
    return outliers, R, R_crit

# 🔹 Applicazione dei test
outlier_results = []
grubbs_outliers = {}
dixon_outliers = {}
rosner_outliers = {}

for col in num_cols:
    data = df[col].dropna().values
    is_outlier_grubbs, G_values, G_crit = grubbs_test(data)
    is_outlier_dixon, Q_value, Q_crit = dixon_q_test(data)
    rosner_outs, R_values, R_crit = rosner_test(data)

    grubbs_outliers[col] = list(df[col][(np.abs((df[col] - df[col].mean()) / df[col].std(ddof=1)) > G_crit)].dropna().values) if any(is_outlier_grubbs) else []
    dixon_outliers[col] = [df[col].max()] if is_outlier_dixon else []
    rosner_outliers[col] = rosner_outs

    outlier_results.append({
        "Tesi": col,
        "Grubbs (Outlier?)": "✅ Sì" if any(is_outlier_grubbs) else "❌ No",
        "Dixon (Outlier?)": "✅ Sì" if is_outlier_dixon else "❌ No",
        "Rosner (Outlier?)": f"{len(rosner_outs)} rilevati" if rosner_outs else "❌ No",
        "Dettagli Grubbs": f"G max={max(G_values):.2f}, G crit={G_crit:.2f}",
        "Dettagli Dixon": f"Q={Q_value:.2f}, Q crit={Q_crit:.2f}" if Q_crit else "Non applicabile",
        "Dettagli Rosner": f"Outliers: {', '.join(map(str, rosner_outs))}" if rosner_outs else "Nessun outlier"
    })

# 🔹 Visualizza i risultati
st.subheader("📊 **Risultati dei Test di Outlier**")
results_df = pd.DataFrame(outlier_results)
st.dataframe(results_df, width=900)

# 🔹 Spiegazione dei test
st.markdown("""
### 📌 **Descrizione dei test utilizzati**
✔ **Grubbs**: Singolo outlier, distribuzioni normali – *ASTM E178, ISO 5725*  
✔ **Dixon (Q-test)**: Dataset piccoli – *IUPAC*  
✔ **Rosner**: Multipli outlier – usato nei laboratori chimici  
""")

# 🔹 Scelta dell’utente per rimozione outlier
st.markdown("---")
st.subheader("🧹 **Filtra i dati rimuovendo outlier**")
remove_grubbs = st.checkbox("❎ Rimuovi outlier individuati da Grubbs")
remove_dixon = st.checkbox("❎ Rimuovi outlier individuati da Dixon (Q-test)")
remove_rosner = st.checkbox("❎ Rimuovi outlier individuati da Rosner")
remove_all = st.checkbox("✅ Rimuovi tutti gli outlier identificati")

# 🔹 Costruzione nuovo DataFrame
filtered_df = df.copy()

if remove_all or any([remove_grubbs, remove_dixon, remove_rosner]):
    for col in num_cols:
        original_col = filtered_df[col]
        values_to_remove = set()

        if remove_grubbs or remove_all:
            values_to_remove.update(grubbs_outliers[col])
        if remove_dixon or remove_all:
            values_to_remove.update(dixon_outliers[col])
        if remove_rosner or remove_all:
            values_to_remove.update(rosner_outliers[col])

        filtered_df[col] = original_col.apply(lambda x: np.nan if x in values_to_remove else x)

    # 🔁 Sostituiamo il dataset nel session_state
    st.session_state["df"] = filtered_df.copy()
    st.success("✅ Dataset aggiornato: gli outlier selezionati sono stati rimossi e il dataset è stato salvato per l'analisi successiva.")

# 🔹 Salva anche il DataFrame dei risultati dei test
st.session_state["outlier_results"] = results_df
