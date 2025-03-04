import streamlit as st
import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.stats.multicomp as mc
import pingouin as pg
import scikit_posthocs as sp  # Per il test di Dunn
from data_loader import load_data

# 🌟 Titolo principale con dimensione doppia
st.markdown("<h1 style='text-align: center; font-size: 170%;'>📊 Comparison Test Between Theses</h1>", unsafe_allow_html=True)

# 📂 Sidebar - Caricamento file
st.sidebar.header("⚙️ Settings")

# 📌 Istruzioni nella sidebar
st.sidebar.markdown("""
📌 **Instructions:**
- Thesis **name in first line**  
- **No header** for repetition lines
""")

# 📂 File uploader
uploaded_file = st.sidebar.file_uploader("📂 Upload an Excel file (.xlsx)", type=["xlsx"])

# 🔍 Controllo se il file è stato caricato
if uploaded_file:
    df = load_data(uploaded_file)  # 📂 Carica i dati

    # ✅ Controllo se i dati sono validi
    if df is not None and not df.empty:
        st.write("✅ **Data uploaded successfully!**")
        st.write(df.head())  # Mostra anteprima dei dati

        # 📊 Mostra il numero di tesi nel dataset nella sidebar
        num_theses = len(df.columns)
        st.sidebar.subheader("📊 Dataset Overview")
        st.sidebar.write(f"🔢 **Number of Theses:** {num_theses}")

        # 🔍 Test di normalità (Shapiro-Wilk)
        st.sidebar.subheader("📈 Normality & Variance Tests")
        st.sidebar.write("🧪 **Normality test used: Shapiro-Wilk**")
        
        normality_results = {}
        for thesis in df.columns:
            stat, p_value = stats.shapiro(df[thesis].dropna())  # Rimuove i NaN prima del test
            normality_results[thesis] = p_value

        # 📊 Mostra risultati del test di normalità
        for thesis, p_val in normality_results.items():
            result_text = f"✅ Normal" if p_val > 0.05 else f"⚠️ Not Normal"
            st.sidebar.write(f"**{thesis}**: p = {p_val:.4f} ({result_text})")

        # 🔍 Test di Levene per la varianza
        stat_levene, p_levene = stats.levene(*[df[col].dropna() for col in df.columns])
        variance_homogeneity = p_levene > 0.05
        levene_result_text = "✅ Variances are homogeneous" if variance_homogeneity else "⚠️ Variances are heterogeneous"
        st.sidebar.write(f"**Levene's Test**: p = {p_levene:.4f} ({levene_result_text})")

        # 📌 Esecuzione dei test statistici
        df_melted = df.melt(var_name="Thesis", value_name="Value")

        if num_theses == 2:  # Se ci sono solo due tesi
            st.subheader("📊 Performing **Two-group Comparison Test**")

            group1 = df.iloc[:, 0].dropna()
            group2 = df.iloc[:, 1].dropna()

            if all(p > 0.05 for p in normality_results.values()):  # Entrambe le tesi sono normali
                stat_ttest, p_ttest = stats.ttest_ind(group1, group2, equal_var=variance_homogeneity)
                st.write(f"**T-test Statistic**: {stat_ttest:.4f}, **p-value**: {p_ttest:.4f}")

                if p_ttest < 0.05:
                    st.info("🔬 The T-test indicates that the two theses are significantly different.")
                else:
                    st.info("✅ The T-test does not detect significant differences between the two theses.")

            else:  # Almeno una tesi non è normale → Usa Mann-Whitney U test
                stat_mann, p_mann = stats.mannwhitneyu(group1, group2, alternative="two-sided")
                st.write(f"**Mann-Whitney U Statistic**: {stat_mann:.4f}, **p-value**: {p_mann:.4f}")

                if p_mann < 0.05:
                    st.info("🔬 The Mann-Whitney U test indicates that the two theses are significantly different.")
                else:
                    st.info("✅ The Mann-Whitney U test does not detect significant differences between the two theses.")

        elif num_theses > 2:  # Se ci sono più di 2 tesi
            if variance_homogeneity and any(p < 0.05 for p in normality_results.values()):
                # 📊 **Kruskal-Wallis per dati non normali ma varianze simili**
                st.subheader("📉 Performing **Kruskal-Wallis Test**")
                kw_stat, p_kruskal = stats.kruskal(*[df[col].dropna() for col in df.columns])
                st.write(f"**Kruskal-Wallis Statistic**: {kw_stat:.4f}, **p-value**: {p_kruskal:.4f}")

                if p_kruskal < 0.05:
                    st.info("🔬 The Kruskal-Wallis test indicates that at least one thesis is significantly different.")

                    # 📉 **Test di Dunn per confronti post-hoc**
                    st.subheader("📉 Performing **Dunn's Post-Hoc Test**")
                    dunn_results = sp.posthoc_dunn(df, p_adjust='bonferroni')
                    st.dataframe(dunn_results, use_container_width=True)

                    # Interpretazione risultati di Dunn
                    significant_pairs = dunn_results[dunn_results < 0.05]
                    if not significant_pairs.empty:
                        st.info("✅ Dunn's test detected significant differences between these thesis pairs:")
                        for idx, row in significant_pairs.iterrows():
                            for col in significant_pairs.columns:
                                if row[col] < 0.05 and idx != col:
                                    st.write(f"- {idx} vs {col} (p = {row[col]:.4f})")
                    else:
                        st.info("✅ Dunn's test does not detect significant differences between the theses.")

            else:
                # 📊 **ANOVA standard per dati normali e varianze omogenee**
                st.subheader("🏆 Performing **Standard ANOVA**")
                anova = pg.anova(data=df_melted, dv="Value", between="Thesis", detailed=True)
                st.dataframe(anova, use_container_width=True)

                if anova["p-unc"].values[0] < 0.05:
                    st.info("🔬 ANOVA indicates that at least one thesis is significantly different.")
                    # 📊 **Test di Tukey HSD**
                    st.subheader("📊 Performing **Tukey's Post-Hoc Test**")
                    tukey = mc.pairwise_tukeyhsd(df_melted["Value"], df_melted["Thesis"])
                    tukey_df = pd.DataFrame(data=tukey.summary().data[1:], columns=tukey.summary().data[0])
                    st.dataframe(tukey_df, use_container_width=True)

else:
    st.sidebar.warning("📂 Upload an Excel file to proceed.")
