import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.stats.multicomp as mc
import pingouin as pg

def run_anova_tests(df):
    """Esegue ANOVA e test post-hoc sui dati forniti, restituendo i risultati e le interpretazioni."""
    results = {}
    interpretations = {}

    # 📌 Trasforma i dati in formato lungo per ANOVA
    df_melted = df.melt(var_name="Thesis", value_name="Value")

    # 📊 Test di Levene (uguaglianza delle varianze)
    stat_levene, p_levene = stats.levene(*[df[col].dropna() for col in df.columns])
    results["Levene's Test"] = f"Statistic: {stat_levene:.4f}, p-value: {p_levene:.4f}"

    if p_levene < 0.05:
        interpretations["Levene's Test"] = "⚠️ The variances between the theses are significantly different. Consider using Games-Howell."
    else:
        interpretations["Levene's Test"] = "✅ The variances between the theses are NOT significantly different. Tukey's test can be used."

    # 🏆 Test ANOVA
    anova = pg.anova(data=df_melted, dv="Value", between="Thesis", detailed=True)
    results["ANOVA"] = anova

    if anova["p-unc"].values[0] < 0.05:
        interpretations["ANOVA"] = "🔬 ANOVA indicates that at least one thesis is significantly different from the others."
    else:
        interpretations["ANOVA"] = "❌ ANOVA does not detect significant differences between the theses."

    # 🔬 Test post-hoc di Tukey HSD
    tukey = mc.pairwise_tukeyhsd(df_melted["Value"], df_melted["Thesis"])
    tukey_df = pd.DataFrame(data=tukey.summary().data[1:], columns=tukey.summary().data[0])
    results["Tukey's Post-Hoc Test"] = tukey_df

    significant_tukey = tukey_df[tukey_df["p-adj"] < 0.05]
    if not significant_tukey.empty:
        interpretations["Tukey's Post-Hoc Test"] = "✅ Significant differences detected between these theses:\n"
        for _, row in significant_tukey.iterrows():
            interpretations["Tukey's Post-Hoc Test"] += f"- {row['group1']} vs {row['group2']} (p = {row['p-adj']:.4f})\n"
    else:
        interpretations["Tukey's Post-Hoc Test"] = "❌ Tukey's test does not detect significant differences between the theses."

    # 📈 Test post-hoc di Bonferroni
    bonferroni = pg.pairwise_ttests(data=df_melted, dv="Value", between="Thesis", padjust="bonferroni")
    results["Bonferroni's Post-Hoc Test"] = bonferroni

    significant_bonferroni = bonferroni[bonferroni["p-corr"] < 0.05]
    if not significant_bonferroni.empty:
        interpretations["Bonferroni's Post-Hoc Test"] = "✅ Significant differences detected between these theses:\n"
        for _, row in significant_bonferroni.iterrows():
            interpretations["Bonferroni's Post-Hoc Test"] += f"- {row['A']} vs {row['B']} (p = {row['p-corr']:.4f})\n"
    else:
        interpretations["Bonferroni's Post-Hoc Test"] = "❌ Bonferroni's test does not detect significant differences between the theses."

    # 📉 Test post-hoc di Games-Howell
    games_howell = pg.pairwise_gameshowell(data=df_melted, dv="Value", between="Thesis")
    results["Games-Howell's Post-Hoc Test"] = games_howell

    significant_games = games_howell[games_howell["pval"] < 0.05]
    if not significant_games.empty:
        interpretations["Games-Howell's Post-Hoc Test"] = "✅ Significant differences detected between these theses:\n"
        for _, row in significant_games.iterrows():
            interpretations["Games-Howell's Post-Hoc Test"] += f"- {row['A']} vs {row['B']} (p = {row['pval']:.4f})\n"
    else:
        interpretations["Games-Howell's Post-Hoc Test"] = "❌ Games-Howell's test does not detect significant differences between the theses."

    return results, interpretations
