import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.stats.multicomp as mc
import pingouin as pg

def run_anova_tests(df):
    """Esegue ANOVA e test post-hoc sui dati forniti."""
    results = {}

    # 📌 Trasforma i dati in formato lungo per ANOVA
    df_melted = df.melt(var_name="Tesi", value_name="Valore")

    # 📊 Test di Levene (uguaglianza delle varianze)
    stat_levene, p_levene = stats.levene(*[df[col].dropna() for col in df.columns])
    results["Test di Levene"] = f"Statistiche: {stat_levene:.4f}, p-value: {p_levene:.4f}"

    # 🏆 Test ANOVA
    anova = pg.anova(data=df_melted, dv="Valore", between="Tesi", detailed=True)
    results["ANOVA"] = anova

    # 🔬 Test post-hoc di Tukey HSD
    tukey = mc.pairwise_tukeyhsd(df_melted["Valore"], df_melted["Tesi"])
    tukey_df = pd.DataFrame(data=tukey.summary().data[1:], columns=tukey.summary().data[0])
    results["Test post-hoc di Tukey"] = tukey_df

    # 📈 Test post-hoc di Bonferroni
    bonferroni = pg.pairwise_ttests(data=df_melted, dv="Valore", between="Tesi", padjust="bonferroni")
    results["Test post-hoc di Bonferroni"] = bonferroni

    # 📉 Test post-hoc di Games-Howell
    games_howell = pg.pairwise_gameshowell(data=df_melted, dv="Valore", between="Tesi")
    results["Test post-hoc di Games-Howell"] = games_howell

    return results

