import pandas as pd
import streamlit as st
from scipy.stats import f_oneway, kruskal
from scipy.stats import ttest_ind, mannwhitneyu
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# 🔹 Titolo
st.markdown("<h3 style='text-align: center;'>📊 APPLICAZIONE DEL TEST STATISTICO</h3>", unsafe_allow_html=True)

# ✅ Verifica se tutte le variabili sono presenti
required_vars = [
    "num_cols", "df", "inequality_ratio",
    "varianze_uguali", "almeno_una_non_normale"
]
missing = [var for var in required_vars if var not in st.session_state]

if missing:
    st.error(f"⚠️ Dati mancanti. Torna alla sezione 'Analisi Preliminare'. Variabili mancanti: {', '.join(missing)}")
    st.stop()

# ✅ Recupero delle variabili
num_cols = st.session_state["num_cols"]
df = st.session_state["df"]
inequality_ratio = st.session_state["inequality_ratio"]
varianze_uguali = st.session_state["varianze_uguali"]
almeno_una_non_normale = st.session_state["almeno_una_non_normale"]
alpha = st.session_state["alpha"] if "alpha" in st.session_state else 0.05

st.subheader("📌 Selezione automatica del test")

if len(num_cols) == 2:
    st.markdown("🔹 **Confronto tra due tesi**")
    t1, t2 = num_cols[0], num_cols[1]
    data1 = df[t1].dropna()
    data2 = df[t2].dropna()

    if almeno_una_non_normale:
        st.warning("⚠️ Distribuzione non normale. Applicazione del **Test di Mann-Whitney U**.")
        stat, p = mannwhitneyu(data1, data2)
        test_name = "Mann-Whitney U"
    elif not varianze_uguali:
        st.warning("⚠️ Varianze diseguali. Applicazione del **T-test di Welch**.")
        stat, p = ttest_ind(data1, data2, equal_var=False)
        test_name = "T-test di Welch"
    else:
        st.success("✅ Condizioni soddisfatte. Applicazione del **T-test classico**.")
        stat, p = ttest_ind(data1, data2, equal_var=True)
        test_name = "T-test classico"

    st.write(f"**Test eseguito**: {test_name}")
    st.write(f"**Statistiche**: {stat:.4f}")
    st.write(f"**p-value**: {p:.4f}")
    st.success("✅ Nessuna differenza significativa") if p > alpha else st.error("❌ Differenza significativa tra le due tesi")

elif len(num_cols) > 2:
    st.markdown("🔹 **Confronto tra più di due tesi**")
    data_groups = [df[col].dropna() for col in num_cols]

    if almeno_una_non_normale:
        st.warning("⚠️ Distribuzione non normale. Applicazione del **Test di Kruskal-Wallis**.")
        stat, p = kruskal(*data_groups)
        test_name = "Kruskal-Wallis"
    elif not varianze_uguali or inequality_ratio > 3:
        st.warning("⚠️ Dati disomogenei. Applicazione del **Welch ANOVA** (solo statistiche).")
        stat, p = f_oneway(*data_groups)
        test_name = "Welch ANOVA (semplificata)"
    else:
        st.success("✅ Condizioni soddisfatte. Applicazione del **ANOVA + Tukey HSD**.")
        stat, p = f_oneway(*data_groups)
        test_name = "ANOVA"

    st.write(f"**Test eseguito**: {test_name}")
    st.write(f"**Statistiche**: {stat:.4f}")
    st.write(f"**p-value**: {p:.4f}")
    st.success("✅ Nessuna differenza significativa") if p > alpha else st.error("❌ Differenze significative tra i gruppi")

    # Analisi post-hoc
    if test_name == "ANOVA" and p <= alpha:
        st.subheader("📊 Analisi post-hoc (Tukey HSD)")
        melted = df.melt(var_name="Tesi", value_name="Valore")
        tukey = pairwise_tukeyhsd(endog=melted["Valore"], groups=melted["Tesi"], alpha=alpha)
        st.text(tukey)

# 🔁 Pulsante per tornare indietro
st.markdown("""
    <a href="/analisi_preliminare" target="_blank">
        <button style="background-color:#4CAF50;color:white;padding:10px;border:none;border-radius:5px;cursor:pointer;">
            ⬅️ Torna all'Analisi Preliminare
        </button>
    </a>
""", unsafe_allow_html=True)
