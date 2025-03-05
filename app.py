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

        if num_theses == 2:
            st.subheader("📊 Confronto tra due tesi")
            group1 = df.iloc[:, 0].dropna()
            group2 = df.iloc[:, 1].dropna()

            if all(p > 0.05 for p in normality_results.values()):
                if variance_homogeneity:
                    stat_ttest, p_ttest = stats.ttest_ind(group1, group2, equal_var=True)
                    st.write(f"**T-test**: statistica = {stat_ttest:.4f}, p-value = {p_ttest:.4f}")
                    st.write("✅ Il test T-test mostra che la Tesi 1 e la Tesi 2 {} significativamente diverse (p-value = {:.4f}).".format("sono" if p_ttest < 0.05 else "non sono", p_ttest))
                else:
                    stat_ttest, p_ttest = stats.ttest_ind(group1, group2, equal_var=False)
                    st.write(f"**Welch's T-test**: statistica = {stat_ttest:.4f}, p-value = {p_ttest:.4f}")
                    st.write("✅ Il test di Welch indica che la Tesi 1 e la Tesi 2 {} significativamente diverse (p-value = {:.4f}).".format("sono" if p_ttest < 0.05 else "non sono", p_ttest))
            else:
                stat_mann, p_mann = stats.mannwhitneyu(group1, group2, alternative="two-sided")
                st.write(f"**Test di Mann-Whitney U**: statistica = {stat_mann:.4f}, p-value = {p_mann:.4f}")
                st.write("✅ Il test di Mann-Whitney mostra che la Tesi 1 e la Tesi 2 {} significativamente diverse (p-value = {:.4f}).".format("sono" if p_mann < 0.05 else "non sono", p_mann))

        elif num_theses > 2:
            if variance_homogeneity:
                if all(p > 0.05 for p in normality_results.values()):
                    st.subheader("📉 Esecuzione di **ANOVA**")
                    anova = pg.anova(data=df_melted, dv="Valore", between="Tesi", detailed=True)
                    st.dataframe(anova, use_container_width=True)
                    st.write("✅ Il test ANOVA indica che {} le tesi messe a confronto sono significativamente diverse (p-value = {:.4f}).".format("" if anova["p-unc"].values[0] < 0.05 else "non", anova["p-unc"].values[0]))
                    if anova["p-unc"].values[0] < 0.05:
                        st.subheader("📊 Test Post-Hoc: **Tukey HSD**")
                        tukey = mc.pairwise_tukeyhsd(df_melted["Valore"], df_melted["Tesi"])
                        tukey_df = pd.DataFrame(data=tukey.summary().data[1:], columns=tukey.summary().data[0])
                        st.dataframe(tukey_df, use_container_width=True)
                        st.write("✅ Il test di Tukey HSD evidenzia che le seguenti tesi sono significativamente diverse:")
                        for row in tukey_df.itertuples():
                            if row.pvalue < 0.05:
                                st.write(f"🔹 {row.group1} vs {row.group2} (p-value = {row.pvalue:.4f})")
else:
    st.sidebar.warning("📂 Carica un file Excel per procedere.")
