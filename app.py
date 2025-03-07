import numpy as np
import pandas as pd
from scipy.stats import f_oneway, levene
import statsmodels.api as sm
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from scikit_posthocs import posthoc_gameshowell  # Per il test di Games-Howell

# Funzione per Welch ANOVA
def welch_anova(*groups):
    return f_oneway(*groups)

# Funzione per il test di Games-Howell
def games_howell(data, groups):
    return posthoc_gameshowell(data, groups)

# Funzione principale per il caso specifico: >2 tesi, varianze disomogenee, distribuzioni normali
def analyze_data(df):
    """Analizza il dataset per il caso specifico richiesto"""

    # Separare le colonne del dataset
    tesi = [df.iloc[:, i].dropna() for i in range(df.shape[1])]
    
    # Welch ANOVA
    welch_result = welch_anova(*tesi)
    p_value_welch = welch_result.pvalue

    print("\n--- RISULTATI ---")
    print(f"Welch ANOVA: statistic={welch_result.statistic:.4f}, p-value={p_value_welch:.4f}")

    # Se Welch ANOVA è significativo, procedere con Games-Howell
    if p_value_welch < 0.05:
        print("\nIl test Welch ANOVA è significativo (p < 0.05). Eseguo il test Games-Howell...")

        # Preparazione dati per Games-Howell
        data = np.concatenate(tesi)
        groups = np.concatenate([[i] * len(tesi[i]) for i in range(len(tesi))])

        # Eseguire Games-Howell
        games_howell_results = games_howell(data, groups)

        # Mostrare i risultati di Games-Howell
        print("\nRisultati del test di Games-Howell:")
        print(games_howell_results)

    else:
        print("\nIl test Welch ANOVA NON è significativo (p ≥ 0.05), quindi NON eseguo il test Games-Howell.")

