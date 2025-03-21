import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

st.markdown("<h3 style='text-align: center;'>📊 Mappa Decisionale – Selezione del Test Statistico</h3>", unsafe_allow_html=True)

# Creazione del grafo diretto
G = nx.DiGraph()

# Etichette multilivello (testo verticale)
nodes = {
    "xlsx": "📂 File\n.xlsx\ncaricato",
    "num_tesi": "🔍 Numero\ndelle tesi",
    "tesi_2": "📊 2\ntesi",
    "tesi_gt2": "📊 >2\ntesi",

    "var_2_eq": "✅ Varianze\nstatisticamente\nuguali",
    "var_2_diff": "❌ Varianze\nstatisticamente\ndiverse",
    "var_gt2_eq": "✅ Varianze\nstatisticamente\nuguali",
    "var_gt2_diff": "❌ Varianze\nstatisticamente\ndiverse",

    "norm_2_eq_yes": "✅ Tutte le\ndistribuzioni\nnormali",
    "norm_2_eq_no": "❌ Almeno una\ndistribuzione\nnon normale",
    "norm_2_diff_yes": "✅ Tutte le\ndistribuzioni\nnormali",
    "norm_2_diff_no": "❌ Almeno una\ndistribuzione\nnon normale",
    "norm_gt2_eq_yes": "✅ Tutte le\ndistribuzioni\nnormali",
    "norm_gt2_eq_no": "❌ Almeno una\ndistribuzione\nnon normale",
    "norm_gt2_diff_yes": "✅ Tutte le\ndistribuzioni\nnormali",
    "norm_gt2_diff_no": "❌ Almeno una\ndistribuzione\nnon normale",

    # 🔹 Nuova dicotomia: bilanciamento tra le due tesi
    "bilanciamento": "⚖️ Bilanciamento\ndelle tesi",
    "bilanciate": "✅ Tesi\nbilanciate",
    "sbilanciate": "❌ Tesi\nsbilanciate",

    # Nodi-foglia (test finali)
    "t_test": "🧪 T-test",
    "welch_ttest": "🧪 T-test\ndi Welch",
    "mann_whitney": "🧪 Mann-Whitney\nU test",
    "kruskal": "🧪 Kruskal-Wallis\n(+ Bonferroni)",
    "games": "🧪 Games-Howell\ntest",
    "welch_games": "🧪 Welch ANOVA\n+ Games-Howell"
}

G.add_nodes_from(nodes.keys())

# Connessioni principali
edges = [
    ("xlsx", "num_tesi"),
    ("num_tesi", "tesi_2"),
    ("num_tesi", "tesi_gt2"),

    ("tesi_2", "var_2_eq"),
    ("tesi_2", "var_2_diff"),
    ("tesi_gt2", "var_gt2_eq"),
    ("tesi_gt2", "var_gt2_diff"),

    ("var_2_eq", "norm_2_eq_yes"),
    ("var_2_eq", "norm_2_eq_no"),
    ("var_2_diff", "norm_2_diff_yes"),
    ("var_2_diff", "norm_2_diff_no"),
    ("var_gt2_eq", "norm_gt2_eq_yes"),
    ("var_gt2_eq", "norm_gt2_eq_no"),
    ("var_gt2_diff", "norm_gt2_diff_yes"),
    ("var_gt2_diff", "norm_gt2_diff_no"),

    # Rami Mann-Whitney
    ("norm_2_diff_no", "mann_whitney"),
    ("norm_2_eq_no", "mann_whitney"),

    # Welch per varianze diverse + normali
    ("norm_2_diff_yes", "welch_ttest"),

    # 🔹 Nuova logica: bilanciamento numerico (solo se var_2_eq + normali)
    ("norm_2_eq_yes", "bilanciamento"),
    ("bilanciamento", "bilanciate"),
    ("bilanciamento", "sbilanciate"),
    ("bilanciate", "t_test"),
    ("sbilanciate", "welch_ttest"),

    # Altri test finali
    ("norm_gt2_eq_no", "kruskal"),
    ("norm_gt2_diff_no", "games"),
    ("norm_2_diff_yes", "welch_games")
]

G.add_edges_from(edges)

# Layout personalizzato verticale
pos = {
    "xlsx": (0, 7),
    "num_tesi": (0, 6),
    "tesi_2": (-2, 5),
    "tesi_gt2": (2, 5),

    "var_2_eq": (-3, 4),
    "var_2_diff": (-1, 4),
    "var_gt2_eq": (1, 4),
    "var_gt2_diff": (3, 4),

    "norm_2_eq_yes": (-3.5, 3),
    "norm_2_eq_no": (-2.5, 3),
    "norm_2_diff_yes": (-1.5, 3),
    "norm_2_diff_no": (-0.5, 3),
    "norm_gt2_eq_yes": (0.5, 3),
    "norm_gt2_eq_no": (1.5, 3),
    "norm_gt2_diff_yes": (2.5, 3),
    "norm_gt2_diff_no": (3.5, 3),

    "bilanciamento": (-3.5, 2),
    "bilanciate": (-4, 1.5),
    "sbilanciate": (-3, 1.5),

    # Test finali
    "t_test": (-4, 0.5),
    "welch_ttest": (-1, 0.5),
    "mann_whitney": (-2, 0.5),
    "kruskal": (1.5, 2),
    "games": (3.5, 2),
    "welch_games": (-0.5, 2)
}

# Disegno del grafo
plt.figure(figsize=(15, 11))
nx.draw_networkx_nodes(G, pos, node_color="lightgray", node_size=3000)
nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle='-|>', arrowsize=30, width=2, edge_color="gray")
nx.draw_networkx_labels(G, pos, labels=nodes, font_size=9, font_weight="bold")

st.pyplot(plt)
