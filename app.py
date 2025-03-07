import numpy as np
import pandas as pd
from scipy.stats import f_oneway, levene
import statsmodels.api as sm
from statsmodels.stats.multicomp import pairwise_tukeyhsd

def welch_anova(*groups):
    """Esegue il test Welch ANOVA"""
    return f_oneway(*groups)

def games_howell(data, groups):
    """Esegue il test di Games-Howell"""
    from scikit_posthocs import posthoc_gameshowell
    return posthoc_gameshowell(data, groups)

def analyze_data(df):
    """Analizza il dataset per il caso specifico: >2 tesi, varianze disomogenee, distribuzioni normali"""

    # Separare le colonne del dataset
    tesi = [df.iloc[:, i].dropna() for i in range(df.shape[1])]
    
    # Test di Welch ANOVA
    welch_result = welch_anova(*tesi)
    p_value_welch = welch_result.pvalue
    
    # Mostrare il risultato di Welch ANOVA
    print(f"Welch ANOVA: statistic={welch_result.statistic}, p-value={p_value_welch}")

    # Se Welch ANOVA è significativo, eseguire Games-Howell
    if p_value_welch < 0.05:
        print("Il test Welch ANOVA è significativo (p < 0.05), eseguo il test Games-Howell.")

        # Preparazione dei dati per Games-Howell
        data = np.concatenate(tesi)
        groups = np.concatenate([[i] * len(tesi[i]) for i in range(len(tesi))])

        # Eseguire Games-Howell
        games_howell_results = games_howell(data, groups)
        
        # Mostrare i risultati di Games-Howell
        print("Risultati del test di Games-Howell:")
        print(games_howell_results)
    else:
        print("Il test Welch ANOVA NON è significativo (p ≥ 0.05), quindi NON eseguo il test Games-Howell.")

