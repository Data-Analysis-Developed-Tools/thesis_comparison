import streamlit as st
import pandas as pd

# 🔹 Recuperiamo i parametri dalla URL
query_params = st.experimental_get_query_params()
alpha = float(query_params.get("alpha", [0.05])[0])  # Livello di significatività
file_name = query_params.get("file_name", [""])[0]  # Nome del file Excel

st.title("📊 Selezione ed Esecuzione del Test Statistico")

# Se il file_name è vuoto, mostra un messaggio di errore
if not file_name:
    st.error("⚠️ Nessun file ricevuto. Assicurati di avviare questa pagina da `app.py`.")
    st.stop()

# Carichiamo il file Excel dal nome passato
uploaded_file_path = f"./{file_name}"  # Assumendo che sia salvato nella directory
try:
    df = pd.read_excel(uploaded_file_path)
    st.success(f"✅ File `{file_name}` caricato correttamente!")
    st.dataframe(df.head())
except Exception as e:
    st.error(f"❌ Errore nel caricamento del file: {e}")
    st.stop()


import streamlit as st
from scipy.stats import ttest_ind, mannwhitneyu, kruskal
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.oneway import anova_oneway

st.title("📊 Selezione ed Esecuzione del Test Statistico")

# **🔹 Recuperiamo i risultati di `app.py`**
if "num_cols" not in st.session_state:
    st.error("⚠️ I risultati dei test preliminari non sono disponibili. Esegui prima `app.py`!")
    st.stop()

num_cols = st.session_state["num_cols"]
inequality_ratio = st.session_state["inequality_ratio"]
varianze_uguali = st.session_state["varianze_uguali"]
almeno_una_non_normale = st.session_state["almeno_una_non_normale"]
df = st.session_state["df"]

if len(num_cols) < 2:
    st.warning("⚠️ Sono necessarie almeno due tesi per effettuare un confronto statistico.")
else:
    n_tesi = len(num_cols)

    # **Scelta ed esecuzione del test appropriato**
    st.subheader("🧪 Test Selezionato ed Esecuzione")

    if n_tesi == 2:
        if varianze_uguali:
            if almeno_una_non_normale:
                st.write("📌 **Scelto test di Mann-Whitney U (dati non normali)**")
                stat, p = mannwhitneyu(df[num_cols[0]].dropna(), df[num_cols[1]].dropna())
            else:
                if inequality_ratio > 5:
                    st.write("📌 **Scelto t-test di Welch (varianze uguali, ma numeri sbilanciati)**")
                    stat, p = ttest_ind(df[num_cols[0]].dropna(), df[num_cols[1]].dropna(), equal_var=False)
                else:
                    st.write("📌 **Scelto t-test standard (varianze uguali, dati normali)**")
                    stat, p = ttest_ind(df[num_cols[0]].dropna(), df[num_cols[1]].dropna(), equal_var=True)
        else:
            st.write("📌 **Scelto test di Mann-Whitney U (varianze diverse)**")
            stat, p = mannwhitneyu(df[num_cols[0]].dropna(), df[num_cols[1]].dropna())

    else:  # n_tesi > 2
        if varianze_uguali:
            if almeno_una_non_normale:
                st.write("📌 **Scelto test di Kruskal-Wallis (dati non normali)**")
                stat, p = kruskal(*[df[col].dropna() for col in num_cols])
            else:
                if inequality_ratio > 5:
                    st.write("📌 **Scelto Welch ANOVA + Games-Howell (varianze uguali, numeri sbilanciati)**")
                    anova_res = anova_oneway([df[col].dropna() for col in num_cols], use_var="unequal")
                    stat, p = anova_res.statistic, anova_res.pvalue
                else:
                    st.write("📌 **Scelto test ANOVA + Tukey HSD (varianze uguali, dati normali)**")
                    stat, p = anova_oneway([df[col].dropna() for col in num_cols], use_var="equal").statistic, anova_oneway([df[col].dropna() for col in num_cols], use_var="equal").pvalue
                    tukey = pairwise_tukeyhsd(df.melt()["value"], df.melt()["variable"])
                    st.write("### 📊 Risultati Tukey HSD:")
                    st.write(tukey.summary())

        else:
            st.write("📌 **Scelto test di Games-Howell (varianze diverse)**")
            anova_res = anova_oneway([df[col].dropna() for col in num_cols], use_var="unequal")
            stat, p = anova_res.statistic, anova_res.pvalue

    # **Visualizzazione risultati del test**
    st.write(f"🔬 **Statistiche test:** {stat:.4f}")
    st.write(f"📌 **p-value:** {p:.4f}")

    if p < 0.05:
        st.error("❌ **Le tesi mostrano differenze statisticamente significative!**")
    else:
        st.success("✅ **Non ci sono differenze statisticamente significative tra le tesi.**")
