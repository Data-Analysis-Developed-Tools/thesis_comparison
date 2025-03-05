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

    if df is not None and not df.empty:
        st.write("✅ **Data uploaded successfully!**")
        st.write(df.head())  # Mostra anteprima dei dati

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

        # 📌 Decisione su quale test eseguire
        df_melted = df.melt(var_name="Thesis", value_name="Value")

        if num_theses == 2:
            st.subheader("📊 Performing **Two-group Comparison Test**")
            group1 = df.iloc[:, 0].dropna()
            group2 = df.iloc[:, 1].dropna()

            if all(p > 0.05 for p in normality_results.values()):
                if variance_homogeneity:
                    stat_ttest, p_ttest = stats.ttest_ind(group1, group2, equal_var=True)
                    st.write(f"**T-test Statistic**: {stat_ttest:.4f}, **p-value**: {p_ttest:.4f}")
                    st.write("**Interpretation:** The t-test is significant if p-value < 0.05, indicating a difference between groups.")
                else:
                    stat_ttest, p_ttest = stats.ttest_ind(group1, group2, equal_var=False)
                    st.write(f"**Welch's T-test Statistic**: {stat_ttest:.4f}, **p-value**: {p_ttest:.4f}")
                    st.write("**Interpretation:** The Welch's t-test accounts for unequal variances; significance is determined if p-value < 0.05.")
            else:
                stat_mann, p_mann = stats.mannwhitneyu(group1, group2, alternative="two-sided")
                st.write(f"**Mann-Whitney U Statistic**: {stat_mann:.4f}, **p-value**: {p_mann:.4f}")
                st.write("**Interpretation:** The Mann-Whitney test is non-parametric; significance is determined if p-value < 0.05.")

        elif num_theses > 2:
            if not variance_homogeneity:
                if any(p < 0.05 for p in normality_results.values()):
                    st.subheader("📉 Performing **Games-Howell Test**")
                    games_howell = pg.pairwise_gameshowell(data=df_melted, dv="Value", between="Thesis")
                    st.dataframe(games_howell, use_container_width=True)
                    st.write("**Interpretation:** Significant differences are marked by p-values < 0.05.")
                else:
                    st.subheader("📉 Performing **Welch ANOVA**")
                    welch_anova = pg.welch_anova(data=df_melted, dv="Value", between="Thesis")
                    st.dataframe(welch_anova, use_container_width=True)
                    st.write("**Interpretation:** Welch ANOVA tests for differences; significance is p-value < 0.05.")
                    if welch_anova["p-unc"].values[0] < 0.05:
                        st.subheader("📉 Performing **Games-Howell Test**")
                        games_howell = pg.pairwise_gameshowell(data=df_melted, dv="Value", between="Thesis")
                        st.dataframe(games_howell, use_container_width=True)
                        st.write("**Interpretation:** Significant differences are marked by p-values < 0.05.")
            else:
                if any(p < 0.05 for p in normality_results.values()):
                    st.subheader("📉 Performing **Kruskal-Wallis Test**")
                    kw_stat, p_kruskal = stats.kruskal(*[df[col].dropna() for col in df.columns])
                    st.write(f"**Kruskal-Wallis Statistic**: {kw_stat:.4f}, **p-value**: {p_kruskal:.4f}")
                    st.write("**Interpretation:** Kruskal-Wallis is a non-parametric test; significance is p-value < 0.05.")
                    if p_kruskal < 0.05:
                        st.subheader("📊 Performing **Dunn's Post-Hoc Test (Bonferroni Correction)**")
                        df_long = df.melt(var_name="Thesis", value_name="Value").dropna()
                        dunn_results = sp.posthoc_dunn(df_long, val_col="Value", group_col="Thesis", p_adjust='bonferroni')
                        st.dataframe(dunn_results, use_container_width=True)
                        st.write("**Interpretation:** Significant differences are marked by p-values < 0.05.")
else:
    st.sidebar.warning("📂 Upload an Excel file to proceed.")
