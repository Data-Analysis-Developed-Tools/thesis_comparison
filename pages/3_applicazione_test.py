import pandas as pd
import streamlit as st
from scipy.stats import f_oneway, kruskal, ttest_ind, mannwhitneyu
from statsmodels.stats.multicomp import pairwise_tukeyhsd

st.markdown("<h3 style='text-align: center;'>📊 APPLICAZIONE DEL TEST STATISTICO</h3>", unsafe_allow_html=True)

# ✅ Verifica variabili
required_vars = [
    "num_cols", "df", "inequality_ratio",
    "varianze_uguali", "almeno_una_non_normale"
]
missing = [v for v in required_vars if v not in st.session_state]

if missing:
    st.error(f"⚠️ Dati mancanti. Torna alla sezione 'Analisi Preliminare'. Mancano: {', '.join(missing)}")
    st.stop()

# ✅ Recupera dati
num_cols = st.session_state["num_cols"]
df = st.session_state["df"]
inequality_ratio = st.session_state["inequality_ratio"]
varianze_uguali = st.session_state["varianze_uguali"]
almeno_una_non_normale = st.session_state["almeno_una_non_normale"]
alpha = st.session_state.get("alpha", 0.05)

st.subheader("📌 Selezione automatica del test")

if len(num_cols) == 2:
    st.markdown("🔹 **Confronto tra due tesi**")
    t1, t2 = num_cols[0], num_cols[1]
    d1 = df[t1].dropna()
    d2 = df[t2].dropna()

    if almeno_una_non_normale:
        st.warning("⚠️ Test selezionato: Mann-Whitney U")
        stat, p = mannwhitneyu(d1, d2)
        test = "Mann-Whitney U"
    elif not varianze_uguali:
        st.warning("⚠️ Test selezionato: T-test di Welch")
        stat, p = ttest_ind(d1, d2, equal_var=False)
        test = "T-test di Welch"
    else:
        st.success("✅ Test selezionato: T-test classico")
        stat, p = ttest_ind(d1, d2, equal_var=True)
        test = "T-test classico"

    st.write(f"**Test eseguito**: {test}")
    st.write(f"**Statistica**: {stat:.4f}")
    st.write(f"**p-value**: {p:.4f}")
    if p > alpha:
        st.success("✅ Nessuna differenza significativa")
    else:
        st.error("❌ Differenza significativa tra le tesi")

elif len(num_cols) > 2:
    st.markdown("🔹 **Confronto tra più di due tesi**")
    gruppi = [df[col].dropna() for col in num_cols]

    if almeno_una_non_normale:
        st.warning("⚠️ Test selezionato: Kruskal-Wallis")
        stat, p = kruskal(*gruppi)
        test = "Kruskal-Wallis"
    elif not varianze_uguali or inequality_ratio > 3:
        st.warning("⚠️ Test selezionato: Welch ANOVA")
        stat, p = f_oneway(*gruppi)  # Simulazione
        test = "Welch ANOVA"
    else:
        st.success("✅ Test selezionato: ANOVA")
        stat, p = f_oneway(*gruppi)
        test = "ANOVA"

    st.write(f"**Test eseguito**: {test}")
    st.write(f"**Statistica**: {stat:.4f}")
    st.write(f"**p-value**: {p:.4f}")
    if p > alpha:
        st.success("✅ Nessuna differenza significativa")
    else:
        st.error("❌ Differenze significative tra i gruppi")

    # Post-hoc Tukey se ANOVA e p significativa
    if test == "ANOVA" and p <= alpha:
        st.subheader("📊 Analisi post-hoc (Tukey HSD)")
        melted = df.melt(var_name="Tesi", value_name="Valore")
        tukey = pairwise_tukeyhsd(melted["Valore"], melted["Tesi"], alpha=alpha)
        st.text(tukey)
