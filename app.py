import pandas as pd
import streamlit as st
from scipy.stats import levene, shapiro

# Titolo dell'app
st.markdown("<h3 style='text-align: center;'>📊 CONFRONTO FRA TESI CON VARIE RIPETIZIONI, PER VALUTAZIONE SOMIGLIANZE/DIFFERENZE</h3>", unsafe_allow_html=True)

# Opzioni per la significatività statistica
sig_levels = {
    "90% (α = 0.10)": 0.10,
    "95% (α = 0.05)": 0.05,
    "99% (α = 0.01)": 0.01,
    "99.9% (α = 0.001)": 0.001
}

# Selezione del livello di significatività
selected_level = st.selectbox(
    "📊 Seleziona il livello di significatività prima di caricare il file:",
    options=list(sig_levels.keys()),
    index=1  # Default: 95%
)

# Memorizzazione del valore scelto
alpha = sig_levels[selected_level]

# Upload del file Excel
uploaded_file = st.file_uploader("📂 Carica un file Excel (.xlsx)", type=["xlsx"])

def load_data(uploaded_file):
    """Carica il file Excel e lo trasforma in DataFrame."""
    try:
        df = pd.read_excel(uploaded_file)
        return df
    except Exception as e:
        st.error(f"❌ Errore nel caricamento del file: {e}")
        return None

# Se un file è stato caricato, eseguire l'analisi
if uploaded_file is not None:
    df = load_data(uploaded_file)
    if df is not None:
        st.write("✅ **File caricato con successo!**")
        st.dataframe(df.head())  # Mostra un'anteprima del DataFrame
        st.write(f"🔬 **Livello di significatività selezionato:** {selected_level} (α = {alpha})")

        # Verifica se ci sono almeno due colonne numeriche
        num_cols = df.select_dtypes(include=['number']).columns
        st.write(f"📌 **Colonne numeriche trovate:** {list(num_cols)}")

        if len(num_cols) < 2:
            st.warning("⚠️ Sono necessarie almeno due colonne numeriche per il test di Levene.")
        else:
            # **Calcolo del Rapporto di Disuguaglianza (Max/Min)**
            st.subheader("📊 Rapporto di Disuguaglianza (Max/Min) delle Numerosità")

            # Contare le osservazioni PRIMA di eliminare i NaN
            count_values = df[num_cols].count()
            min_n = count_values.min()
            max_n = count_values.max()
            inequality_ratio = max_n / min_n if min_n > 0 else float('inf')

            # Debugging output
            st.write(f"🔹 **Numero minimo di osservazioni:** {min_n}")
            st.write(f"🔹 **Numero massimo di osservazioni:** {max_n}")
            st.write(f"🔹 **Rapporto Max/Min:** {inequality_ratio:.2f}")

            # Nuove soglie di avviso per la disomogeneità
            if inequality_ratio > 10:
                st.error("❌ Il rapporto Max/Min è >10, la disomogeneità è molto alta! L'analisi potrebbe non essere affidabile.")
            elif inequality_ratio > 5:
                st.warning("⚠️ Il rapporto tra la tesi con più osservazioni e quella con meno è elevato (>5). Potrebbe essere necessario riequilibrare i dati.")
            else:
                st.success("✅ La distribuzione delle osservazioni tra le tesi è accettabile.")

            # **Test di Levene per l'uguaglianza delle varianze**
            st.subheader("📈 Test di Levene - Omogeneità delle Varianze")

            levene_stat, levene_p = levene(*[df[col].dropna() for col in num_cols])
            varianze_uguali = levene_p > alpha  # Definizione della variabile

            st.write(f"**Statistiche test di Levene:** {levene_stat:.4f}")
            st.write(f"**p-value:** {levene_p:.4f}")

            if varianze_uguali:
                st.success(f"✅ Le varianze possono essere considerate uguali (p > {alpha})")
            else:
                st.error(f"❌ Le varianze sono significativamente diverse (p ≤ {alpha})")

            # **Test di Shapiro-Wilk per la normalità**
            st.subheader("📊 Test di Shapiro-Wilk - Normalità della Distribuzione")

            normalita = {}
            for col in num_cols:
                shapiro_stat, shapiro_p = shapiro(df[col].dropna())
                normalita[col] = shapiro_p > alpha  # True se la colonna è normale
                st.write(f"**Colonna:** {col}")
                st.write(f"**Statistiche test di Shapiro-Wilk:** {shapiro_stat:.4f}")
                st.write(f"**p-value:** {shapiro_p:.4f}")

                # **Messaggio di commento per la normalità**
                if normalita[col]:
                    st.success(f"✅ I dati nella colonna '{col}' **seguono una distribuzione normale** (p > {alpha}).")
                else:
                    st.error(f"❌ I dati nella colonna '{col}' **non seguono una distribuzione normale** (p ≤ {alpha}).")

            almeno_una_non_normale = not all(normalita.values())  # Definizione della variabile

            # ✅ Esportiamo i risultati per `test_selection.py`
            st.session_state["num_cols"] = num_cols
            st.session_state["inequality_ratio"] = inequality_ratio
            st.session_state["varianze_uguali"] = varianze_uguali
            st.session_state["almeno_una_non_normale"] = almeno_una_non_normale
            st.session_state["df"] = df

            # **Pulsante per eseguire direttamente test_selection.py all'interno di un iframe**
            if st.button("🚀 Esegui il test statistico appropriato"):
                st.success("📊 **Analisi statistica in corso...**")
                st.markdown('<iframe src="test_selection.py" width="100%" height="600"></iframe>', unsafe_allow_html=True)
