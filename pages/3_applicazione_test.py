import pandas as pd
import streamlit as st
from scipy.stats import ttest_ind, f_oneway, shapiro

# 🔹 Titolo della pagina
st.markdown("<h3 style='text-align: center;'>📊 APPLICAZIONE DEL TEST STATISTICO</h3>", unsafe_allow_html=True)

# ✅ Verifica se i dati necessari sono disponibili in session_state
required_vars = ["num_cols", "df", "inequality_ratio", "alpha", "varianze_uguali", "almeno_una_non_normale"]
missing_vars = [var for var in required_vars if var not in st.session_state]

if missing_vars:
    st.error(f"⚠️ Dati mancanti! Torna alla sezione 'Analisi Preliminare' ed esegui l'analisi prima di procedere.\n\nMancano: {', '.join(missing_vars)}")
    st.stop()

# ✅ Recuperiamo i dati dal session_state
num_cols = st.session_state["num_cols"]
df = st.session_state["df"]
inequality_ratio = st.session_state["inequality_ratio"]
alpha = st.session_state["alpha"]
varianze_uguali = st.session_state["varianze_uguali"]
almeno_una_non_normale = st.session_state["almeno_una_non_normale"]

# **Selezione e applicazione del test statistico**
st.subheader("📊 **Selezione e Applicazione del Test Statistico**")

# Caso con due tesi
if len(num_cols) == 2:
    st.write("🔹 **Caso: 2 tesi a confronto**")

    # Se le varianze sono uguali
    if varianze_uguali:
        st.write("✅ Le varianze sono uguali, quindi applicheremo il **T-test classico**.")
        t_stat, p_value = ttest_ind(df[num_cols[0]].dropna(), df[num_cols[1]].dropna())
    else:
        st.write("⚠️ Le varianze sono diverse, quindi applicheremo il **Test di Welch**.")
        t_stat, p_value = ttest_ind(df[num_cols[0]].dropna(), df[num_cols[1]].dropna(), equal_var=False)

# Caso con più di due tesi
elif len(num_cols) > 2:
    st.write("🔹 **Caso: Più di 2 tesi a confronto**")

    # Se le varianze sono uguali
    if varianze_uguali:
        st.write("✅ Le varianze sono uguali, quindi applicheremo il **Test ANOVA**.")
        f_stat, p_value = f_oneway(*[df[col].dropna() for col in num_cols])
    else:
        st.write("⚠️ Le varianze sono diverse, quindi applicheremo il **Test di Welch ANOVA + Games-Howell**.")
        # Test di Welch ANOVA e Games-Howell da implementare

# Mostra i risultati
st.write(f"**Statistiche del Test:** t = {t_stat:.4f}, p-value = {p_value:.4f}")

if p_value < alpha:
    st.success(f"✅ Il risultato è statisticamente significativo (p ≤ {alpha}).")
else:
    st.error(f"❌ Il risultato non è significativo (p > {alpha}).")

# **Pulsante per tornare alla Home**
st.markdown("""
    <a href="/analisi_preliminare" target="_blank">
        <button style="background-color:#4CAF50;color:white;padding:10px;border:none;border-radius:5px;cursor:pointer;">
            🔄 Torna all'Analisi Preliminare
        </button>
    </a>
""", unsafe_allow_html=True)

# **Pulsante per tornare alla pagina precedente**
st.markdown("""
    <a href="/individuazione_outlier" target="_blank">
        <button style="background-color:#4CAF50;color:white;padding:10px;border:none;border-radius:5px;cursor:pointer;">
            🔄 Torna all'Individuazione degli Outlier
        </button>
    </a>
""", unsafe_allow_html=True)
