import streamlit as st
import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.stats.multicomp as mc
import pingouin as pg
import scikit_posthocs as sp  # Per il test di Dunn
from data_loader import load_data

# 🌟 Titolo principale con dimensione doppia
st.markdown("<h1 style='text-align: center; font-size: 170%;'>📊 Confronto tra Tesi</h1>", unsafe_allow_html=True)

# 📂 Sidebar - Caricamento file
st.sidebar.header("⚙️ Impostazioni")

# 📌 Istruzioni nella sidebar
st.sidebar.markdown("""
📌 **Istruzioni:**
- Il **nome della tesi** deve essere nella prima riga
- **Nessuna intestazione** per le righe di ripetizione
""")

# 📂 Caricamento file
uploaded_file = st.sidebar.file_uploader("📂 Carica un file Excel (.xlsx)", type=["xlsx"])

# Definizione preventiva della variabile per evitare NameError
num_osservazioni = None

# 🔍 Controllo se il file è stato caricato
if uploaded_file:
    df = load_data(uploaded_file)  # 📂 Carica i dati

    if df is not None and not df.empty:
        st.write("✅ **Dati caricati con successo!**")
        st.write(df.head())  # Mostra anteprima dei dati

        num_theses = len(df.columns)
        st.sidebar.subheader("📊 Panoramica del Dataset")
        st.sidebar.write(f"🔢 **Numero di Tesi:** {num_theses}")

        # 🔄 Assicuriamoci che le celle vuote o con spazi vengano convertite in veri NaN
        df = df.applymap(lambda x: None if pd.isna(x) or str(x).strip() == "" else x)

        # 🔢 Conta il numero effettivo di osservazioni per ciascuna tesi (solo valori non nulli)
        num_osservazioni = [df[col].count() for col in df.columns]  # Conta solo celle non vuote
        num_osservazioni = [int(n) for n in num_osservazioni]  # Converte np.int64 in int normale

        # 🏆 Prendi il numero di osservazioni massimo tra tutte le tesi
        max_osservazioni = max(num_osservazioni)

# Se `num_osservazioni` è ancora `None`, assegniamo un valore predefinito per evitare errori
if num_osservazioni is None:
    num_osservazioni = []
    max_osservazioni = 0

# 📌 Mostra il risultato nella sidebar
st.sidebar.header("Informazioni sul Bilanciamento")
st.sidebar.write(f"🔢 Numero massimo di osservazioni tra le tesi: {max_osservazioni}")

# 📊 Calcolo del coefficiente di squilibrio
if len(num_osservazioni) > 1 and len(set(num_osservazioni)) > 1:  # Se almeno un gruppo ha dimensione diversa
    squilibrio = max(num_osservazioni) / min(num_osservazioni)
else:
    squilibrio = 1  # Nessuno squilibrio se tutte le tesi hanno lo stesso numero di osservazioni

st.sidebar.write(f"⚖️ Coefficiente di Squilibrio: {squilibrio:.2f}")

# 🔍 Fornisce il commento
if squilibrio < 1.5:
    commento = "✅ I gruppi sono bilanciati."
elif 1.5 <= squilibrio <= 2:
    commento = "⚠️ Lo squilibrio è moderato."
else:
    commento = "❗ Lo squilibrio è forte, considerare l'uso di Welch ANOVA."

st.sidebar.write(commento)
