import streamlit as st
import pandas as pd
import scipy.stats as stats

st.title("📊 Analisi Statistica - Confronto fra Tesi")

# ⏳ Attendi finché `data_loader.py` non ha terminato l'elaborazione
if "final_data" not in st.session_state or st.session_state["final_data"] is None:
    st.warning("⚠️ Attendi il completamento dei test preliminari in `data_loader.py` prima di procedere.")
    st.stop()

df = st.session_state["final_data"]
test_results = st.session_state["preliminary_tests"]
alpha = st.session_state["confidence_level"]

# 📊 Mostra i dati
st.subheader("📂 Dati Caricati e Analizzati")
st.dataframe(df)

# 📈 Mostra i risultati dei test preliminari
st.subheader("📊 Risultati dei Test Preliminari")
st.write(f"**Indice di Squilibrio:** {test_results['imbalance_index']:.4f}")

for thesis, p_value in test_results["normality_results"].items():
    result_text = "✅ Normale" if p_value > alpha else "⚠️ Non Normale"
    st.write(f"**{thesis}**: p = {p_value:.4f} ({result_text})")

levene_text = "✅ Varianze omogenee" if test_results["levene_p"] > alpha else "⚠️ Varianze eterogenee"
st.write(f"**Test di Levene:** p = {test_results['levene_p']:.4f} ({levene_text})")

# 🔍 **Avvio del processo decisionale (Albero)**
st.subheader("📊 Selezione del Test Statistico")
num_theses = len(df.columns)
is_normal = all(p > alpha for p in test_results["normality_results"].values())
is_homogeneous = test_results["levene_p"] > alpha

if num_theses == 2:
    if is_homogeneous:
        if is_normal:
            st.write("✅ **Applico il T-test Standard**")
        else:
            st.write("⚠️ **Applico Mann-Whitney U Test**")
    else:
        st.write("⚠️ **Applico il T-test di Welch**")
else:
    if is_homogeneous:
        if is_normal:
            st.write("✅ **Applico ANOVA + Tukey HSD**")
        else:
            st.write("⚠️ **Applico Welch ANOVA + Games-Howell**")
    else:
        st.write("⚠️ **Applico Kruskal-Wallis + Test di Dunn**")
