import streamlit as st
import pandas as pd

st.title("📊 Analisi dei Dati - App")

# ⏳ Attendi finché `data_loader.py` non ha terminato l'elaborazione
if "final_data" not in st.session_state or st.session_state["final_data"] is None:
    st.warning("⚠️ Attendi il completamento dell'analisi in `data_loader.py` prima di procedere.")
    st.stop()

# ✅ Ora possiamo usare i dati finalizzati
df = st.session_state["final_data"]
test_results = st.session_state["test_results"]

# 📊 Mostra i dati
st.subheader("📂 Dati Caricati e Analizzati")
st.dataframe(df)

# 📈 Mostra i risultati dei test
st.subheader("📊 Risultati dei Test")
for thesis, p_value in test_results.items():
    result_text = "✅ Normale" if p_value > st.session_state["confidence_level"] else "⚠️ Non Normale"
    st.write(f"**{thesis}**: p = {p_value:.4f} ({result_text})")
