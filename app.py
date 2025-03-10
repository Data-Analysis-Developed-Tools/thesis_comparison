import streamlit as st
import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.stats.multicomp as mc
import pingouin as pg
import scikit_posthocs as sp  # Per il test di Dunn
from data_loader import load_data, preliminary_tests

# 🌟 Titolo principale con dimensione doppia
st.markdown("<h1 style='text-align: center; font-size: 170%;'>📊 Confronto tra Tesi</h1>", unsafe_allow_html=True)

# 📂 Sidebar - Caricamento file
st.sidebar.header("⚙️ Impostazioni")
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

        # Esegui test preliminari
        normality_results, variance_homogeneity = preliminary_tests(df)

        # 📌 Decisione su quale test eseguire
        df_melted = df.melt(var_name="Tesi", value_name="Valore")
        num_theses = len(df.columns)

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
