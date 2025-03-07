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
# Funzione per calcolare il coefficiente di squilibrio
def calcola_squilibrio(gruppi):
    # Calcolo del coefficiente di squilibrio
    max_n = max(gruppi)
    min_n = min(gruppi)
    squilibrio = max_n / min_n
    return squilibrio

# Funzione per il commento in base al coefficiente
def commenta_squilibrio(squilibrio):
    if squilibrio < 1.5:
        return "I gruppi sono bilanciati."
    elif 1.5 <= squilibrio <= 2:
        return "Lo squilibrio è moderato."
    else:
        return "Lo squilibrio è forte, considerare l'uso di Welch ANOVA."

# Crea una lista di numeri di osservazioni per i gruppi
# Esempio: [10, 20, 30] (inserisci i tuoi dati)
gruppi = [10, 20, 30]

# Calcola il coefficiente di squilibrio
squilibrio = calcola_squilibrio(gruppi)

# Scrivere il risultato nella barra laterale
st.sidebar.header("Informazioni sul Bilanciamento")
st.sidebar.write(f"Coefficiente di Squilibrio: {squilibrio:.2f}")
st.sidebar.write(commenta_squilibrio(squilibrio))

# 📂 Caricamento file
uploaded_file = st.sidebar.file_uploader("📂 Carica un file Excel (.xlsx)", type=["xlsx"])

# 🔍 Controllo se il file è stato caricato
if uploaded_file:
    df = load_data(uploaded_file)  # 📂 Carica i dati

    if df is not None and not df.empty:
        st.write("✅ **Dati caricati con successo!**")
        st.write(df.head())  # Mostra anteprima dei dati

        num_theses = len(df.columns)
        st.sidebar.subheader("📊 Panoramica del Dataset")
        st.sidebar.write(f"🔢 **Numero di Tesi:** {num_theses}")

        # 🔍 Test di normalità (Shapiro-Wilk)
        st.sidebar.subheader("📈 Test di Normalità e Varianza")
        st.sidebar.write("🧪 **Test di Normalità usato: Shapiro-Wilk**")
        
        normality_results = {}
        for thesis in df.columns:
            stat, p_value = stats.shapiro(df[thesis].dropna())  # Rimuove i NaN prima del test
            normality_results[thesis] = p_value

        # 📊 Mostra risultati del test di normalità
        for thesis, p_val in normality_results.items():
            result_text = "✅ Normale" if p_val > 0.05 else "⚠️ Non Normale"
            st.sidebar.write(f"**{thesis}**: p = {p_val:.4f} ({result_text})")

        # 🔍 Test di Levene per la varianza
        stat_levene, p_levene = stats.levene(*[df[col].dropna() for col in df.columns])
        variance_homogeneity = p_levene > 0.05
        levene_result_text = "✅ Varianze omogenee" if variance_homogeneity else "⚠️ Varianze eterogenee"
        st.sidebar.write(f"**Test di Levene**: p = {p_levene:.4f} ({levene_result_text})")

        # 📌 Decisione su quale test eseguire
        df_melted = df.melt(var_name="Tesi", value_name="Valore")

        if num_theses > 2:
            if variance_homogeneity and all(p > 0.05 for p in normality_results.values()):
                st.subheader("📉 Esecuzione di **ANOVA**")
                anova = pg.anova(data=df_melted, dv="Valore", between="Tesi", detailed=True)
                st.dataframe(anova, use_container_width=True)
                if anova["p-unc"].values[0] < 0.05:
                    st.subheader("📊 Test Post-Hoc: **Tukey HSD**")
                    tukey = mc.pairwise_tukeyhsd(df_melted["Valore"], df_melted["Tesi"])
                    st.dataframe(pd.DataFrame(data=tukey.summary().data[1:], columns=tukey.summary().data[0]), use_container_width=True)
            elif not variance_homogeneity and all(p > 0.05 for p in normality_results.values()):
                st.subheader("📉 Esecuzione di **Welch ANOVA e Games-Howell**")
                welch = pg.welch_anova(data=df_melted, dv="Valore", between="Tesi")
                st.dataframe(welch, use_container_width=True)
                if welch["p-unc"].values[0] < 0.05:
                    st.subheader("📊 Test Post-Hoc: **Games-Howell**")
                    gh = pg.pairwise_gameshowell(data=df_melted, dv="Valore", between="Tesi")
                    st.dataframe(gh, use_container_width=True)
            elif variance_homogeneity and any(p <= 0.05 for p in normality_results.values()):
                st.subheader("📉 Esecuzione di **Kruskal-Wallis e Test di Dunn**")
                kw = stats.kruskal(*[df[col].dropna() for col in df.columns])
                st.write(f"**Kruskal-Wallis**: statistica = {kw.statistic:.4f}, p-value = {kw.pvalue:.4f}")
                if kw.pvalue < 0.05:
                    dunn = sp.posthoc_dunn(df_melted, val_col="Valore", group_col="Tesi", p_adjust='bonferroni')
                    st.subheader("📊 Test Post-Hoc: **Dunn con Bonferroni**")
                    st.dataframe(dunn, use_container_width=True)
            else:
                st.subheader("📉 Esecuzione di **Games-Howell**")
                gh = pg.pairwise_gameshowell(data=df_melted, dv="Valore", between="Tesi")
                st.dataframe(gh, use_container_width=True)
else:
    st.sidebar.warning("📂 Carica un file Excel per procedere.")
