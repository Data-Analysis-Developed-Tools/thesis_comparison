# SOSTITUISCI queste righe all’interno della lista "edges"

edges = [
    ("xlsx", "num_tesi"),
    ("num_tesi", "tesi_2"),
    ("num_tesi", "tesi_gt2"),

    ("tesi_2", "var_2_eq"),
    ("tesi_2", "var_2_diff"),

    ("var_2_eq", "norm_2_eq_yes"),
    ("var_2_eq", "norm_2_eq_no"),
    ("var_2_diff", "norm_2_eq_no"),
    ("var_2_diff", "welch_t"),
    ("norm_2_eq_no", "mann_whitney"),

    ("norm_2_eq_yes", "bilanciamento_2"),
    ("bilanciamento_2", "student_t"),
    ("bilanciamento_2", "welch_t"),

    ("tesi_gt2", "var_gt2_eq"),
    ("tesi_gt2", "var_gt2_diff"),

    ("var_gt2_diff", "norm_gt2_diff_no"),
    ("var_gt2_diff", "norm_gt2_diff_yes"),
    ("norm_gt2_diff_no", "games_howell"),
    ("norm_gt2_diff_yes", "games_howell"),  # 🔁 cambiato da welch_anova

    # ("welch_anova", "games_howell"),  # ⛔️ rimosso questo passaggio intermedio

    ("var_gt2_eq", "norm_gt2_eq_no"),
    ("norm_gt2_eq_no", "kruskal_gt2_eq"),
    ("kruskal_gt2_eq", "dunn_gt2_eq"),

    ("var_gt2_eq", "norm_gt2_eq_yes"),
    ("norm_gt2_eq_yes", "bilanciamento_gt2"),
    ("bilanciamento_gt2", "anova_test"),
    ("anova_test", "tukey_hsd"),
    ("bilanciamento_gt2", "welch_anova")
]
