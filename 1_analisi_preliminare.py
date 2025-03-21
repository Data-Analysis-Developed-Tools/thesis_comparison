import pandas as pd
import streamlit as st
from scipy.stats import levene, shapiro

# 🔹 Titolo
st.markdown("<h3 style='text-align: center;'>📊 ANALISI PRELIMINARE DELLE TESI</h3>", unsafe_allow_html=True)

# 🔹 Opzioni per livello di significatività
sig_levels = {
    "90% (α = 0.10)": 0.10,
    "95% (α = 0.05)": 0.05,
    "99% (α = 0.01)": 0.01,
    "99.9% (α = 0.001)": 0.001
}

# 🔹 Inizializza session_state se non presente
if "uploaded_file" not in st.session_state:
    st.session_state["uploaded_file"] = None
    st.session_state["alpha"] = 0.05
    st.session_state["results_df"] = None
    st.session_state["normalita_df"] = None
    st.session_state["num_cols"] = None
    st.session_state["df"] = None
    st.session_state["inequality_ratio"] = None
    st.session_state["varianze_uguali"] = None
    st.session_state["almeno_una_non_normale"] = None

# 🔹 Selezione livello di significatività
selected_level = st.selectbox(
    "📊 Seleziona il livello di significatività prima di caricare il file:",
    options=list(sig_levels.keys()),
    index=1
)
alpha = sig_levels[selected_level]
st.session_state["alpha"] = alpha

# 🔹 Upload file
uploaded_file = st.file_uploader("📂 Carica un file Excel (.xlsx)", type=["xlsx"])
if uploaded_file is not None:
    st.session_state["uploaded_file"] = uploaded_file

def load_data(uploaded_file):
    try:
        df = pd.read_excel(uploaded_file)
        return df
    except Exception as e:
        st.error(f"❌ Errore nel caricamento del file: {e}")
        return None

# 🔹 Analisi se file disponibile
if st.session_state["uploaded_file"] is not None:
    df = load_data(st.session_state["uploaded_file"])
    if df is not None:
        st.write("✅ **File caricato con successo!**")
        st.dataframe(df.head())
        st.write(f"🔬 **Livello di significatività selezionato:** {selected_level} (α = {alpha})")

        num_cols = df.select_dtypes(include=["number"]).columns

        if len(num_cols) < 2:
            st.warning("⚠️ Sono necessarie almeno due colonne numeriche.")
        else:
            # 🔸 Calcolo rapporto di disuguaglianza
            count_values = df[num_cols].count()
            min_n = count_values.min()
            max_n = count_values.max()
            inequality_ratio = max_n / min_n if min_n > 0 else float('inf')

            if inequality_ratio <= 1.5:
                balance_comment = "Dati ben bilanciati tra le tesi"
            elif inequality_ratio <= 3:
                balance_comment = "Dati moderatamente sbilanciati"
            elif inequality_ratio <= 5:
                balance_comment = "Dati sbilanciati, attenzione all'analisi"
            else:
                balance_comment = "Dati fortemente sbilanciati, possibile distorsione nei test statistici"

            # 🔸 Test di Levene
            levene_stat, levene_p = levene(*[df[col].dropna() for col in num_cols])
            varianze_uguali = levene_p > alpha

            # 🔸 Test di Shapiro-Wilk
            normalita_results = []
            almeno_una_non_normale = False

            for col in num_cols:
                shapiro_stat, shapiro_p = shapiro(df[col].dropna())
                normale = shapiro_p > alpha
                normalita_results.append([
                    col,
                    f"{shapiro_stat:.4f}",
                    f"{shapiro_p:.4f}",
                    "✅ Sì" if normale else "❌ No"
                ])
                if not normale:
                    almeno_una_non_normale = True

            normalita_df = pd.DataFrame(
                normalita_results,
                columns=["Tesi", "Statistica Shapiro-Wilk", "p-value", "Distribuzione Normale"]
            )

            # 🔸 Riepilogo tabellare dei risultati preliminari
            results_df = pd.DataFrame({
                "Parametro": [
                    "Numero Min. Osservazioni",
                    "Numero Max. Osservazioni",
                    "Rapporto Max/Min",
                    "Statistiche Levene",
                    "p-value Levene",
                    "Varianze Uguali",
                    "Test di normalità: Shapiro-Wilk",
                    "Almeno una distribuzione NON normale"
                ],
                "Valore": [
                    min_n,
                    max_n,
                    f"{inequality_ratio:.2f}",
                    f"{levene_stat:.4f}",
                    f"{levene_p:.4f}",
                    "✅ Sì" if varianze_uguali else "❌ No",
                    "Eseguito su ogni tesi",
                    "❌ Sì" if almeno_una_non_normale else "✅ No"
                ],
                "Commento": [
                    "Minimo numero di osservazioni tra le tesi",
                    "Massimo numero di osservazioni tra le tesi",
                    balance_comment,
                    "Valore della statistica di Levene per l'uguaglianza delle varianze",
                    "Se p ≤ α, le varianze sono significativamente diverse",
                    "Se 'Sì', le varianze possono essere considerate uguali",
                    "Verifica se ogni tesi segue una distribuzione normale",
                    "Se 'Sì', almeno una tesi non segue una distribuzione normale"
                ]
            })

            # 🔸 Salvataggio risultati per le altre pagine
            st.session_state["df"] = df.copy()
            st.session_state["num_cols"] = num_cols
            st.session_state["inequality_ratio"] = inequality_ratio
            st.session_state["varianze_uguali"] = varianze_uguali
            st.session_state["almeno_una_non_normale"] = almeno_una_non_normale
            st.session_state["results_df"] = results_df
            st.session_state["normalita_df"] = normalita_df

# 🔹 Visualizzazione dei risultati se già calcolati
if st.session_state["results_df"] is not None:
    st.subheader("📊 **Risultati dell'Analisi Preliminare**")
    st.dataframe(st.session_state["results_df"], width=750)

if st.session_state["normalita_df"] is not None:
    st.subheader("📊 **Dettaglio del Test di Normalità (Shapiro-Wilk)**")
    st.dataframe(st.session_state["normalita_df"], width=750)

# 🔹 Navigazione
st.markdown("""
    <a href="/individuazione_outlier" target="_blank">
        <button style="background-color:#4CAF50;color:white;padding:10px;border:none;border-radius:5px;cursor:pointer;">
            🚀 Passa all'Individuazione degli Outlier
        </button>
    </a>
""", unsafe_allow_html=True)

st.markdown("""
    <a href="/applicazione_test" target="_blank">
        <button style="background-color:#4CAF50;color:white;padding:10px;border:none;border-radius:5px;cursor:pointer;">
            📊 Applica il Test Statistico
        </button>
    </a>
""", unsafe_allow_html=True)
