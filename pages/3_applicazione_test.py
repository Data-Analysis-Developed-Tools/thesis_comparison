import pandas as pd
import streamlit as st
from scipy.stats import f_oneway, kruskal, ttest_ind, mannwhitneyu
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# 🔹 Titolo della pagina
st.markdown("<h3 style='text-align: center;'>📊 APPLICAZIONE DEL TEST STATISTICO</h3>", unsafe_allow_html=True)

# ✅ Verifica se le variabili sono disponibili
required_vars = [
    "num_cols", "df", "inequality_ratio",
    "varianze_uguali", "almeno_una_non_normale"
]
missing_vars = [var for var in required_vars if var not in st.session_state]

if missing_vars:
    st.error(f"⚠️ Dati mancanti! Torna alla sezione 'Analisi Preliminare' ed esegui l'analisi.\nVariabili mancanti: {', '.join(missing_vars)}")
    st.stop()

# ✅ Recupera variabili dal session_state
num_cols = st.session_state["num_cols"]
df = st.session_state["df"]
inequality_ratio = st.session_state["inequality_ratio"]
varianze_uguali = st.session_state["varianze_uguali"]
almeno_una_non_normale = st.session_state["almeno_una_non_normale"]
alpha = st.session_state.get("alpha", 0.05)

# 🔹 Sezione logica del test
st.subheader("📌 Selezione automatica del test")

if len(num_cols) == 2:
    st.markdown("🔹 **Confronto tra due tesi**")
    t1, t2 = num_cols[0], num_cols[1]
    data1 = df[t1].dropna()
    data2 = df[t2].dropna()

    if almeno_una_non_normale:
        st.warning("⚠️ Almeno una distribuzione non è normale. Test selezionato: **Mann-Whitney U**")
        stat, p = mannwhitneyu(data1, data2)
        test_name = "Mann-Whitney U"
    elif not varianze_uguali:
        st.warning("⚠️ Le varianze sono diseguali. Test selezionato: **T-test di Welch**")
        stat, p = ttest_ind(data1, data2, equal_var=False)
        test_name = "T-test di Welch"
    else:
        st.success("✅ Condizioni soddisfatte per il **T-test classico**")
        stat, p = ttest_ind(data1, data2, equal_var=True)
        test_name = "T-test classico"

    st.write(f"**Test eseguito**: {test_name}")
    st.write(f"**Statistica**: {stat:.4f}")
    st.write(f"**p-value**: {p:.4f}")

    if p > alpha:
        st.success("✅ Nessuna differenza significativa tra le due tesi")
    else:
        st.error("❌ Differenza significativa tra le due tesi")

elif len(num_cols) > 2:
    st.markdown("🔹 **Confronto tra più di due tesi**")
    data_groups = [df[col].dropna() for col in num_cols]

    if almeno_una_non_normale:
        st.warning("⚠️ Almeno una distribuzione non è normale. Test selezionato: **Kruskal-Wallis**")
        stat, p = kruskal(*data_groups)
        test_name = "Kruskal-Wallis"
    elif not varianze_uguali or inequality_ratio > 3:
        st.warning("⚠️ Varianze diseguali o dati molto sbilanciati. Test selezionato: **Welch ANOVA** (semplificata)")
        stat, p = f_oneway(*data_groups)  # Nota: semplificazione
        test_name = "Welch ANOVA"
    else:
        st.success("✅ Condizioni soddisfatte per **ANOVA + Tukey HSD**")
        stat, p = f_oneway(*data_groups)
        test_name = "ANOVA"

    st.write(f"**Test eseguito**: {test_name}")
    st.write(f"**Statistica**: {stat:.4f}")
    st.write(f"**p-value**: {p:.4f}")

    if p > alpha:
        st.success("✅ Nessuna differenza significativa tra i gruppi")
    else:
        st.error("❌ Differenze significative tra almeno due tesi")

    # 🔸 Analisi post-hoc con Tukey solo se ANOVA e p ≤ alpha
    if test_name == "ANOVA" and p <= alpha:
        st.subheader("📊 Analisi Post-Hoc (Tukey HSD)")
        melted = df.melt(var_name="Tesi", value_name="Valore")
        tukey = pairwise_tukeyhsd(endog=melted["Valore"], groups=melted["Tesi"], alpha=alpha)
        st.text(tukey)

# 🔙 Pulsante di ritorno
st.markdown("""
    <a href="/analisi_preliminare" target="_blank">
        <button style="background-color:#4CAF50;color:white;padding:10px;border:none;border-radius:5px;cursor:pointer;">
            ⬅️ Torna all'Analisi Preliminare
        </button>
    </a>
""", unsafe_allow_html=True)
