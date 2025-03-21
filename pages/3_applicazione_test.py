import streamlit as st
import pandas as pd
from scipy.stats import ttest_ind, mannwhitneyu, kruskal
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.oneway import anova_oneway

# 🔹 Titolo dell'analisi
st.title("📊 Selezione ed Esecuzione del Test Statistico")

# ✅ Recuperiamo il file Excel da `st.session_state`
if "uploaded_file" not in st.session_state:
    st.error("⚠️ Nessun file ricevuto. Assicurati di avviare questa pagina da `app.py`.")
    st.stop()

uploaded_file = st.session_state["uploaded_file"]
df = pd.read_excel(uploaded_file)

st.success(f"✅ File `{uploaded_file.name}` caricato correttamente!")
st.dataframe(df.head())  # Mostra un'anteprima del DataFrame

# ✅ Recuperiamo il livello di significatività da `st.session_state`
alpha = st.session_state.get("alpha", 0.05)
st.write(f"🔬 **Livello di significatività selezionato:** α = {alpha}")

# ✅ Recuperiamo gli esiti dei test preliminari
num_cols = st.session_state["num_cols"]
inequality_ratio = st.session_state["inequality_ratio"]
varianze_uguali = st.session_state["varianze_uguali"]
almeno_una_non_normale = st.session_state["almeno_una_non_normale"]

st.write(f"📌 **Numero di colonne analizzate:** {len(num_cols)}")
st.write(f"📊 **Rapporto Max/Min delle osservazioni:** {inequality_ratio:.2f}")
st.write(f"📈 **Varianze uguali:** {'✅ Sì' if varianze_uguali else '❌ No'}")
st.write(f"📊 **Almeno una distribuzione non normale:** {'❌ Sì' if almeno_una_non_normale else '✅ No'}")

# **Selezione ed esecuzione del test statistico**
st.subheader("🧪 Test Selezionato ed Esecuzione")

if len(num_cols) < 2:
    st.warning("⚠️ Sono necessarie almeno due tesi per effettuare un confronto statistico.")
else:
    n_tesi = len(num_cols)

    if n_tesi == 2:
        # **Caso con 2 tesi**
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

    else:  
        # **Caso con più di 2 tesi**
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

    if p < alpha:
        st.error("❌ **Le tesi mostrano differenze statisticamente significative!**")
    else:
        st.success("✅ **Non ci sono differenze statisticamente significative tra le tesi.**")
