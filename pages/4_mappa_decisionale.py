import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

# Etichette nodi
nodi = {
    "xlsx": "File .xlsx caricato",
    "num_tesi": "Numero delle tesi",
    "tesi_2": "2 tesi",
    "tesi_gt2": ">2 tesi",
    "var_2_eq": "Varianze uguali",
    "var_2_diff": "Varianze diverse",
    "var_gt2_eq": "Varianze uguali",
    "var_gt2_diff": "Varianze diverse",
    "norm_2_eq_yes": "Tutte distribuzioni normali",
    "norm_2_eq_no": "Almeno una non normale",
    "norm_gt2_eq_yes": "Tutte distribuzioni normali",
    "norm_gt2_eq_no": "Almeno una non normale",
    "norm_gt2_diff_yes": "Tutte distribuzioni normali",
    "norm_gt2_diff_no": "Almeno una non normale",
    "bilanciamento_2": "Bilanciamento osservazioni?",
    "bilanciamento_gt2": "Bilanciamento osservazioni?",
    "student_t": "t-test di Student",
    "welch_t": "t-test di Welch",
    "mann_whitney": "Mann-Whitney U",
    "anova_test": "ANOVA",
    "tukey_hsd": "Tukey HSD",
    "welch_anova": "Welch ANOVA",
    "games_howell": "Games-Howell",
    "kruskal_gt2_eq": "Kruskal-Wallis",
    "dunn_gt2_eq": "Dunn + Bonferroni"
}

# Aggiunta nodi
for nodo, label in nodi.items():
    G.add_node(nodo, label=label)

# Connessioni aggiornate
edges = [
    ("xlsx", "num_tesi"),
    ("num_tesi", "tesi_2"), ("num_tesi", "tesi_gt2"),

    ("tesi_2", "var_2_eq"), ("tesi_2", "var_2_diff"),
    ("var_2_eq", "norm_2_eq_yes"), ("var_2_eq", "norm_2_eq_no"),
    ("var_2_diff", "norm_2_eq_no"), ("var_2_diff", "welch_t"),
    ("norm_2_eq_yes", "bilanciamento_2"),
    ("bilanciamento_2", "student_t"), ("bilanciamento_2", "welch_t"),
    ("norm_2_eq_no", "mann_whitney"),

    ("tesi_gt2", "var_gt2_eq"), ("tesi_gt2", "var_gt2_diff"),
    ("var_gt2_eq", "norm_gt2_eq_yes"), ("var_gt2_eq", "norm_gt2_eq_no"),
    ("norm_gt2_eq_yes", "bilanciamento_gt2"),
    ("bilanciamento_gt2", "anova_test"), ("bilanciamento_gt2", "welch_anova"),
    ("anova_test", "tukey_hsd"),

    ("norm_gt2_eq_no", "kruskal_gt2_eq"),
    ("kruskal_gt2_eq", "dunn_gt2_eq"),

    ("var_gt2_diff", "norm_gt2_diff_yes"), ("var_gt2_diff", "norm_gt2_diff_no"),
    ("norm_gt2_diff_yes", "games_howell"),      # ✅ Collegamento diretto aggiornato
    ("norm_gt2_diff_no", "games_howell"),       # ✅ Esisteva già ed è corretto

    ("welch_anova", "games_howell")  # 🔄 mantenuto solo per percorsi con tutte normali
]
G.add_edges_from(edges)

# Layout manuale
pos = {
    "xlsx": (0, 10), "num_tesi": (0, 9),
    "tesi_2": (-6, 8), "tesi_gt2": (6, 8),
    "var_2_eq": (-7, 7), "var_2_diff": (-5, 7),
    "norm_2_eq_yes": (-8, 6), "norm_2_eq_no": (-6, 6),
    "bilanciamento_2": (-8, 5),
    "student_t": (-9, 4), "welch_t": (-7, 4), "mann_whitney": (-6, 4),
    "var_gt2_eq": (5, 7), "var_gt2_diff": (7, 7),
    "norm_gt2_eq_yes": (4.5, 6), "norm_gt2_eq_no": (5.5, 6),
    "norm_gt2_diff_yes": (6.5, 6), "norm_gt2_diff_no": (7.5, 6),
    "bilanciamento_gt2": (4.5, 5),
    "anova_test": (4.2, 4), "welch_anova": (5.2, 4),
    "tukey_hsd": (4.2, 3),
    "games_howell": (6.8, 3),
    "kruskal_gt2_eq": (5.5, 5), "dunn_gt2_eq": (5.5, 4)
}

# Disegno del grafo
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
nx.draw_networkx_labels(
    G, pos,
    labels=nx.get_node_attributes(G, 'label'),
    font_size=9,
    font_weight="bold"
)

plt.title("Mappa Decisionale per la Scelta del Test Statistico", fontsize=14)
plt.axis('off')
plt.tight_layout()
plt.show()
