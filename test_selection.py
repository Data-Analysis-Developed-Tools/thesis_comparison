import streamlit as st
from scipy.stats import ttest_ind, mannwhitneyu, kruskal
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.oneway import anova_oneway

# Importiamo i risultati calcolati in app.py
from app import num_cols, inequality_ratio, varianze_uguali, almeno_una_non_normale, df

st.title("📊 Selezione ed Esecuzione del Test Statistico")

if len(num_cols) < 2:
    st.warning("⚠️ Sono necessarie almeno due tesi per effettuare un confronto statistico.")
else:
    n_tesi = len(num_cols)

    # **Scelta ed esecuzione del test appropriato**
    st.subheader("🧪 Test Selezionato ed Esecuzione")

    if n_tesi == 2:
        if varianze_uguali:
            if almeno_una_non_normale:
                st.write("📌 **Scelto test di Mann-Whitney U (dati non normali)**")
                stat, p = mannwhitneyu(df[num_cols[0]].dropna(), df[num_cols[1]].dropna())
            else:
                if inequality_ratio > 5:
                    st.write("📌 **Scelto t-test di Welch (varianze uguali, ma numeri sbilanciati)**")
                    stat, p = ttest_ind(df[num_cols[0]].dropna(), df[num_cols[1]].dropna(), equal_var=False)
                else:
                    st.write("📌 **Scelto t-test standard (varianze uguali, dati normali)**")
                    stat, p = ttest_ind(df[num_cols[0]].dropna(), df[num_cols[1]].dropna(), equal_var=True)
        else:
            st.write("📌 **Scelto test di Mann-Whitney U (varianze diverse)**")
            stat, p = mannwhitneyu(df[num_cols[0]].dropna(), df[num_cols[1]].dropna())

    else:  # n_tesi > 2
        if varianze_uguali:
            if almeno_una_non_normale:
                st.write("📌 **Scelto test di Kruskal-Wallis (dati non normali)**")
                stat, p = kruskal(*[df[col].dropna() for col in num_cols])
            else:
                if inequality_ratio > 5:
                    st.write("📌 **Scelto Welch ANOVA + Games-Howell (varianze uguali, numeri sbilanciati)**")
                    anova_res = anova_oneway([df[col].dropna() for col in num_cols], use_var="unequal")
                    stat, p = anova_res.statistic, anova_res.pvalue
                else:
                    st.write("📌 **Scelto test ANOVA + Tukey HSD (varianze uguali, dati normali)**")
                    stat, p = anova_oneway([df[col].dropna() for col in num_cols], use_var="equal").statistic, anova_oneway([df[col].dropna() for col in num_cols], use_var="equal").pvalue
                    tukey = pairwise_tukeyhsd(df.melt()["value"], df.melt()["variable"])
                    st.write("### 📊 Risultati Tukey HSD:")
                    st.write(tukey.summary())

        else:
            st.write("📌 **Scelto test di Games-Howell (varianze diverse)**")
            anova_res = anova_oneway([df[col].dropna() for col in num_cols], use_var="unequal")
            stat, p = anova_res.statistic, anova_res.pvalue

    # **Visualizzazione risultati del test**
    st.write(f"🔬 **Statistiche test:** {stat:.4f}")
    st.write(f"📌 **p-value:** {p:.4f}")

    if p < 0.05:
        st.error("❌ **Le tesi mostrano differenze statisticamente significative!**")
    else:
        st.success("✅ **Non ci sono differenze statisticamente significative tra le tesi.**")
