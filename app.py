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

        # 📌 Mostra il risultato nella sidebar
        st.sidebar.header("Informazioni sul Bilanciamento")
        st.sidebar.write(f"🔢 Numero osservazioni per tesi: {num_osservazioni}")

        # 📊 Calcolo del coefficiente di squilibrio
        if len(set(num_osservazioni)) > 1:  # Se almeno un gruppo ha dimensione diversa
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
