import streamlit as st
import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.stats.multicomp as mc
import pingouin as pg
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
        num_groups = len(df.columns)

        if all(p > 0.05 for p in normality_results.values()):  # Dati normali
            if variance_homogeneity:
                st.subheader("🏆 Performing **Standard ANOVA**")
                anova = pg.anova(data=df_melted, dv="Value", between="Thesis", detailed=True)
                st.dataframe(anova, use_container_width=True)

                if anova["p-unc"].values[0] < 0.05:
                    st.info("🔬 ANOVA indicates that at least one thesis is significantly different from the others.")

                    # 📊 **Test di Tukey HSD**
                    st.subheader("📊 Performing **Tukey's Post-Hoc Test**")
                    tukey = mc.pairwise_tukeyhsd(df_melted["Value"], df_melted["Thesis"])
                    tukey_df = pd.DataFrame(data=tukey.summary().data[1:], columns=tukey.summary().data[0])
                    st.dataframe(tukey_df, use_container_width=True)

                    tukey_significant = tukey_df[tukey_df["p-adj"] < 0.05]
                    if not tukey_significant.empty:
                        st.info("✅ Tukey's test detected significant differences between these thesis pairs:")
                        for _, row in tukey_significant.iterrows():
                            st.write(f"- {row['group1']} vs {row['group2']} (p = {row['p-adj']:.4f})")
                    else:
                        st.info("❌ Tukey's test does not detect significant differences between the theses.")

                else:
                    st.info("✅ ANOVA does not detect significant differences.")

            else:
                st.subheader("📈 Performing **Welch's ANOVA** (for unequal variances)")
                welch_anova = pg.welch_anova(data=df_melted, dv="Value", between="Thesis")
                st.dataframe(welch_anova, use_container_width=True)

        else:  # Dati non normali
            if num_groups == 2:
                st.subheader("📊 Performing **Mann-Whitney U Test** (for 2 non-normal groups)")
                u_stat, p_mann = stats.mannwhitneyu(df.iloc[:, 0].dropna(), df.iloc[:, 1].dropna(), alternative="two-sided")
                st.write(f"**Mann-Whitney U Statistic**: {u_stat:.4f}, **p-value**: {p_mann:.4f}")
            else:
                st.subheader("📉 Performing **Kruskal-Wallis Test** (for multiple non-normal groups)")
                kw_stat, p_kruskal = stats.kruskal(*[df[col].dropna() for col in df.columns])
                st.write(f"**Kruskal-Wallis Statistic**: {kw_stat:.4f}, **p-value**: {p_kruskal:.4f}")

                if p_kruskal < 0.05:
                    st.info("🔬 Kruskal-Wallis test suggests significant differences. Consider pairwise tests.")
                    # 📉 **Test di Games-Howell**
                    st.subheader("📉 Performing **Games-Howell Post-Hoc Test**")
                    games_howell = pg.pairwise_gameshowell(data=df_melted, dv="Value", between="Thesis")
                    st.dataframe(games_howell, use_container_width=True)

                    games_significant = games_howell[games_howell["pval"] < 0.05]
                    if not games_significant.empty:
                        st.info("✅ Games-Howell test detected significant differences between these thesis pairs:")
                        for _, row in games_significant.iterrows():
                            st.write(f"- {row['A']} vs {row['B']} (p = {row['pval']:.4f})")
                    else:
                        st.info("❌ Games-Howell test does not detect significant differences between the theses.")

else:
    st.sidebar.warning("📂 Upload an Excel file to proceed.")
