# Ricreiamo il grafo senza emoji e con etichette in italiano semplice

import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

# Etichette dei nodi
nodi = {
    "xlsx": "File Excel caricato",
    "num_tesi": "Numero delle tesi",
    "tesi_2": "2 Tesi",
    "tesi_gt2": ">2 Tesi",
    "var_2_eq": "Varianze uguali",
    "var_2_diff": "Varianze diverse",
    "var_gt2_eq": "Varianze uguali",
    "var_gt2_diff": "Varianze diverse",
    "norm_2_eq_yes": "Tutte le distribuzioni normali",
    "norm_2_eq_no": "Almeno una distribuzione non normale",
    "norm_2_diff_yes": "Tutte le distribuzioni normali",
    "norm_gt2_eq_yes": "Tutte le distribuzioni normali",
    "norm_gt2_eq_no": "Almeno una distribuzione non normale",
    "norm_gt2_diff_yes": "Tutte le distribuzioni normali",
    "norm_gt2_diff_no": "Almeno una distribuzione non normale",
    "bilanciamento_2": "Numerosità bilanciate?",
    "bilanciamento_gt2": "Numerosità bilanciate?",
    "student_t": "t-test di Student",
    "welch_t": "t-test di Welch",
    "mann_whitney": "Mann-Whitney U test",
    "anova_test": "ANOVA",
    "tukey_hsd": "Tukey HSD",
    "welch_anova": "Welch ANOVA",
    "games_howell": "Games-Howell",
    "kruskal_test": "Kruskal-Wallis",
    "dunn_test": "Dunn con Bonferroni"
}

# Aggiungi nodi
for nodo, label in nodi.items():
    G.add_node(nodo, label=label)

# Connessioni (archi)
edges = [
    ("xlsx", "num_tesi"),
    ("num_tesi", "tesi_2"), ("num_tesi", "tesi_gt2"),
    ("tesi_2", "var_2_eq"), ("tesi_2", "var_2_diff"),
    ("var_2_eq", "norm_2_eq_yes"), ("var_2_eq", "norm_2_eq_no"),
    ("var_2_diff", "norm_2_diff_yes"), ("var_2_diff", "norm_2_eq_no"),
    ("norm_2_eq_yes", "bilanciamento_2"),
    ("bilanciamento_2", "student_t"), ("bilanciamento_2", "welch_t"),
    ("norm_2_diff_yes", "welch_t"),
    ("norm_2_eq_no", "mann_whitney"),
    ("tesi_gt2", "var_gt2_eq"), ("tesi_gt2", "var_gt2_diff"),
    ("var_gt2_eq", "norm_gt2_eq_yes"), ("var_gt2_eq", "norm_gt2_eq_no"),
    ("norm_gt2_eq_yes", "bilanciamento_gt2"),
    ("bilanciamento_gt2", "anova_test"), ("bilanciamento_gt2", "welch_anova"),
    ("anova_test", "tukey_hsd"),
    ("norm_gt2_eq_no", "kruskal_test"), ("kruskal_test", "dunn_test"),
    ("var_gt2_diff", "norm_gt2_diff_yes"), ("var_gt2_diff", "norm_gt2_diff_no"),
    ("norm_gt2_diff_yes", "welch_anova"), ("norm_gt2_diff_no", "kruskal_test"),
    ("welch_anova", "games_howell")
]
G.add_edges_from(edges)

# Posizioni dei nodi
pos = {
    "xlsx": (0, 10), "num_tesi": (0, 9),
    "tesi_2": (-6, 8), "tesi_gt2": (6, 8),
    "var_2_eq": (-7, 7), "var_2_diff": (-5, 7),
    "norm_2_eq_yes": (-7.5, 6), "norm_2_eq_no": (-6, 6),
    "norm_2_diff_yes": (-5, 6),
    "bilanciamento_2": (-7.5, 5),
    "student_t": (-8, 4), "welch_t": (-6.5, 4),
    "mann_whitney": (-6, 4),
    "var_gt2_eq": (5, 7), "var_gt2_diff": (7, 7),
    "norm_gt2_eq_yes": (4.8, 6), "norm_gt2_eq_no": (5.8, 6),
    "norm_gt2_diff_yes": (6.8, 6), "norm_gt2_diff_no": (7.5, 6),
    "bilanciamento_gt2": (4.8, 5),
    "anova_test": (4.5, 4), "welch_anova": (6, 4),
    "tukey_hsd": (4.5, 3), "games_howell": (6, 3),
    "kruskal_test": (7.5, 5), "dunn_test": (7.5, 4)
}

# Disegna il grafo
plt.figure(figsize=(20, 13))
nx.draw(
    G, pos,
    with_labels=False,
    node_color="lightgray",
    node_size=3600,
    edge_color="gray",
    width=1.6,
    arrows=True,
    arrowstyle='-|>',
    arrowsize=30
)
nx.draw_networkx_labels(G, pos, labels=nx.get_node_attributes(G, 'label'),
                        font_size=9, font_weight="bold")
plt.title("Mappa Decisionale per la Scelta del Test Statistico", fontsize=14)
plt.axis('off')
plt.show()
