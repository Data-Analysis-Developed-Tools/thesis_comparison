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

        if num_theses > 2 and variance_homogeneity and all(p > 0.05 for p in normality_results.values()):
            st.subheader("📉 Esecuzione di **ANOVA**")
            anova = pg.anova(data=df_melted, dv="Valore", between="Tesi", detailed=True)
            st.dataframe(anova, use_container_width=True)

            # 🔹 Interpretazione ANOVA
            if anova["p-unc"].values[0] < 0.05:
                st.write("✅ Il test ANOVA ha identificato almeno una differenza significativa tra le tesi (p-value = {:.4f}).".format(anova["p-unc"].values[0]))
                
                st.subheader("📊 Test Post-Hoc: **Tukey HSD**")
                tukey = mc.pairwise_tukeyhsd(df_melted["Valore"], df_melted["Tesi"])
                tukey_df = pd.DataFrame(data=tukey.summary().data[1:], columns=tukey.summary().data[0])
                st.dataframe(tukey_df, use_container_width=True)

                # 📌 Estrazione delle coppie significativamente diverse con il nome corretto delle colonne
                tukey_df.columns = ["group1", "group2", "meandiff", "p-adj", "lower", "upper", "reject"]
                significant_pairs = tukey_df[tukey_df["reject"] == True]

                if not significant_pairs.empty:
                    st.write("✅ Il test di Tukey HSD evidenzia le seguenti tesi significativamente diverse:")
                    for _, row in significant_pairs.iterrows():
                        st.write(f"🔹 {row['group1']} vs {row['group2']} (p-value = {row['p-adj']:.4f})")
                else:
                    st.write("⚠️ Il test di Tukey HSD non ha rilevato differenze significative tra le tesi.")
            else:
                st.write("⚠️ Il test ANOVA non ha identificato differenze significative tra le tesi (p-value = {:.4f}).".format(anova["p-unc"].values[0]))

else:
    st.sidebar.warning("📂 Carica un file Excel per procedere.")
