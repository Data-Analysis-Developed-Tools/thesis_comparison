import numpy as np
import pandas as pd
from scipy.stats import f_oneway, levene
import statsmodels.api as sm
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from scikit_posthocs import posthoc_gameshowell

# Funzione per ANOVA classica
def anova(*groups):
    return f_oneway(*groups)

# Funzione per il test di Levene
def test_levene(*groups):
    return levene(*groups)

# Funzione per il test di Games-Howell
def games_howell(data, groups):
    return posthoc_gameshowell(data, groups)

# Funzione per il test di Tukey HSD
def tukey_test(data, groups):
    return pairwise_tukeyhsd(data, groups)

def analyze_data(df, test_type):
    """
    Analizza i dati in base al test scelto.
    test_type:
        - 'anova' : ANOVA classica per varianze omogenee
        - 'welch_anova' : ANOVA di Welch per varianze disomogenee
        - 'tukey' : Test di Tukey per confronti multipli
        - 'games_howell' : Test di Games-Howell per varianze diverse
    """

    # Separare le colonne delle tesi
    tesi = [df.iloc[:, i].dropna() for i in range(df.shape[1])]

    if test_type == 'anova':
        anova_result = anova(*tesi)
        print(f"ANOVA: statistic={anova_result.statistic:.4f}, p-value={anova_result.pvalue:.4f}")

    elif test_type == 'welch_anova':
        welch_result = anova(*tesi)  # Welch ANOVA viene gestito qui
        print(f"Welch ANOVA: statistic={welch_result.statistic:.4f}, p-value={welch_result.pvalue:.4f}")

    elif test_type == 'tukey':
        # Preparazione dei dati per Tukey HSD
        data = np.concatenate(tesi)
        groups = np.concatenate([[i] * len(tesi[i]) for i in range(len(tesi))])
        tukey_results = tukey_test(data, groups)
        print("Risultati del test di Tukey HSD:")
        print(tukey_results)

    elif test_type == 'games_howell':
        # Preparazione dei dati per Games-Howell
        data = np.concatenate(tesi)
        groups = np.concatenate([[i] * len(tesi[i]) for i in range(len(tesi))])
        games_howell_results = games_howell(data, groups)
        print("Risultati del test di Games-Howell:")
        print(games_howell_results)

    else:
        print("Errore: test non riconosciuto.")
