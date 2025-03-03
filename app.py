import streamlit as st
import pandas as pd
import scipy.stats as stats
import pingouin as pg
from data_loader import load_data

# 🌟 Nuovo titolo con dimensione intermedia
st.markdown("<h2 style='text-align: center; font-size: 85%;'>📊 Comparison Test Between Theses</h2>", unsafe_allow_html=True)

# 📂 Caricamento del file nella barra laterale
st.sidebar.header("⚙️ Settings")
uploaded_file = st.sidebar.file_uploader("📂 Upload an Excel file (.xlsx)", type=["xlsx"])

# 📌 Istruzioni aggiuntive sotto il caricamento del file
st.sidebar.markdown("📌 **Thesis name in first line. No header for repetition lines.**")

# 📊 Selezione della verifica di normalità
st.sidebar.subheader("📈 Normality & Variance Tests")
st.sidebar.write("🧪 **Normality test used: Shapiro-Wilk**")  # Indica il test utilizzato

normality_results = {}
variance_homogeneity = None

# 📌 Controllo se è stato caricato un file
if uploaded_file:
    df = load_data(uploaded_file)  # 🔄 Carica i dati
    if df is not None:
        st.write("✅ **Data uploaded successfully!**")
        st.write(df.head())  # Mostra l'anteprima dei dati

        # 🔍 **Test di normalità Shapiro-Wilk per ogni tesi**
        for thesis in df.columns:
            stat, p_value = stats.shapiro(df[thesis].dropna())  # Rimuove i NaN prima del test
            normality_results[thesis] = p_value

        # 📊 Mostra i risultati nella sidebar
        for thesis, p_val in normality_results.items():
            result_text = f"✅ Normal" if p_val > 0.05 else f"⚠️ Not Normal"
            st.sidebar.write(f"**{thesis}**: p = {p_val:.4f} ({result_text})")

        # ❌ Se almeno una tesi non è normale, avvisa l'utente
        data_are_normal = all(p > 0.05 for p in normality_results.values())
        if not data_are_normal:
            st.sidebar.warning("⚠️ At least one thesis does not follow a normal distribution. Using non-parametric tests (Kruskal-Wallis or Mann-Whitney).")

        # 📊 Test di Levene per l'uguaglianza delle varianze
        stat_levene, p_levene = stats.levene(*[df[col].dropna() for col in df.columns])
        variance_homogeneity = p_levene > 0.05  # True = varianze uguali, False = varianze diverse
        levene_result_text = "✅ Variances are homogeneous" if variance_homogeneity else "⚠️ Variances are heterogeneous"
        st.sidebar.write(f"**Levene's Test**: p = {p_levene:.4f} ({levene_result_text})")

        # 📌 Scelta automatica del test
        num_groups = len(df.columns)

        if data_are_normal:
            if variance_homogeneity:
                st.subheader("🏆 Performing **Standard ANOVA**")
                anova = pg.anova(data=df.melt(var_name="Thesis", value_name="Value"), dv="Value", between="Thesis", detailed=True)
                st.dataframe(anova, use_container_width=True)
            else:
                st.subheader("📈 Performing **Welch's ANOVA (for unequal variances)**")
                welch_anova = pg.welch_anova(data=df.melt(var_name="Thesis", value_name="Value"), dv="Value", between="Thesis")
                st.dataframe(welch_anova, use_container_width=True)

        else:  # Se i dati non sono normali
            if num_groups == 2:
                st.subheader("📊 Performing **Mann-Whitney U Test** (for 2 non-normal groups)")
                u_stat, p_mann = stats.mannwhitneyu(df.iloc[:, 0].dropna(), df.iloc[:, 1].dropna(), alternative="two-sided")
                st.write(f"**Mann-Whitney U Statistic**: {u_stat:.4f}, **p-value**: {p_mann:.4f}")
            else:
                st.subheader("📉 Performing **Kruskal-Wallis Test** (for multiple non-normal groups)")
                kw_stat, p_kruskal = stats.kruskal(*[df[col].dropna() for col in df.columns])
                st.write(f"**Kruskal-Wallis Statistic**: {kw_stat:.4f}, **p-value**: {p_kruskal:.4f}")

                # 📌 Commento interpretativo per Kruskal-Wallis
                if p_kruskal < 0.05:
                    st.info("🔬 The Kruskal-Wallis test suggests that at least one thesis differs significantly from the others. Consider performing pairwise comparisons for further analysis.")
                else:
                    st.info("✅ The Kruskal-Wallis test indicates no significant differences between the theses.")

else:
    st.sidebar.warning("📂 Upload an Excel file to proceed.")
