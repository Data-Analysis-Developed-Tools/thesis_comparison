import pandas as pd
import streamlit as st

# 🔹 Titolo della pagina
st.markdown("<h3 style='text-align: center;'>📊 APPLICAZIONE DEL TEST STATISTICO</h3>", unsafe_allow_html=True)

# ✅ Verifica se i dati necessari sono disponibili in session_state
required_vars = ["num_cols", "df", "inequality_ratio"]
missing_vars = [var for var in required_vars if var not in st.session_state]

if missing_vars:
    st.error(f"⚠️ Dati mancanti! Torna alla sezione 'Analisi Preliminare' ed esegui l'analisi prima di procedere.\n\nMancano: {', '.join(missing_vars)}")
    st.stop()

# ✅ Recuperiamo i dati dal session_state
num_cols = st.session_state["num_cols"]
df = st.session_state["df"]
inequality_ratio = st.session_state["inequality_ratio"]

# **Scelta del test statistico in base ai dati**
st.subheader("📌 **Selezione del Test Statistico**")

if len(num_cols) == 2:
    st.write("🔹 **Caso: 2 tesi a confronto**")
    if inequality_ratio > 3:
        st.write("⚠️ Le osservazioni sono molto sbilanciate. Si consiglia il **Test di Welch**.")
    else:
        st.write("✅ Le osservazioni sono bilanciate. Si può utilizzare il **T-test classico**.")

elif len(num_cols) > 2:
    st.write("🔹 **Caso: Più di 2 tesi a confronto**")
    if inequality_ratio > 3:
        st.write("⚠️ Le osservazioni sono molto sbilanciate. Si consiglia il **Test di Welch ANOVA + Games-Howell**.")
    else:
        st.write("✅ Le osservazioni sono bilanciate. Si può utilizzare il **Test ANOVA + Tukey HSD**.")

# **Pulsante per tornare alla Home**
st.markdown("""
    <a href="/analisi_preliminare" target="_blank">
        <button style="background-color:#4CAF50;color:white;padding:10px;border:none;border-radius:5px;cursor:pointer;">
            🔄 Torna all'Analisi Preliminare
        </button>
    </a>
""", unsafe_allow_html=True)
