import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

st.markdown("<h3 style='text-align: center;'>📊 Mappa Decisionale – Selezione del Test Statistico</h3>", unsafe_allow_html=True)

# Creazione del grafo diretto
G = nx.DiGraph()

# Definizione dei nodi
nodes = {
    "xlsx": "📂 File\n.xlsx\ncaricato",
    "num_tesi": "🔍 Numero\ndelle tesi",
    "tesi_2": "📊 2\ntesi",
    "tesi_gt2": "📊 >2\ntesi",

    "var_2_eq": "✅ Varianze\nuguali",
    "var_2_diff": "❌ Varianze\ndiverse",
    "var_gt2_eq": "✅ Varianze\nuguali",
    "var_gt2_diff": "❌ Varianze\ndiverse",

    "norm_2_eq_yes": "✅ Tutte le\ndistribuzioni\nnormali",
    "norm_2_eq_no": "❌ Almeno una\nnon normale",
    "norm_2_diff_yes": "✅ Tutte le\ndistribuzioni\nnormali",
    "norm_2_diff_no": "❌ Almeno una\nnon normale",
    "norm_gt2_eq_yes": "✅ Tutte le\ndistribuzioni\nnormali",
    "norm_gt2_eq_no": "❌ Almeno una\nnon normale",
    "norm_gt2_diff_yes": "✅ Tutte le\ndistribuzioni\nnormali",
    "norm_gt2_diff_no": "❌ Almeno una\nnon normale",

    "bilanciamento": "⚖️ Bilanciamento\ndelle tesi",
    "bilanciate": "✅ Tesi\nbilanciate",
    "sbilanciate": "❌ Tesi\nsbilanciate",

    "bilanciamento_gt2": "⚖️ Bilanciamento\ndelle tesi",
    "bilanciate_gt2": "✅ Tesi\nbilanciate",
    "sbilanciate_gt2": "❌ Tesi\nsbilanciate",

    # Nodi di decisione finale
    "anova_tukey": "🧪 ANOVA\n+ Tukey HSD",
    "kruskal": "🧪 Kruskal-Wallis\n(+ Dunn, Bonferroni)",
    "welch_games": "🧪 Welch ANOVA\n+ Games-Howell",
    "t_test": "🧪 T-test",
    "welch_ttest": "🧪 T-test\ndi Welch",
    "mann_whitney": "🧪 Mann-Whitney\nU test",
    "games": "🧪 Games-Howell\ntest"
}

G.add_nodes_from(nodes.keys())

# Connessioni tra i nodi
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

    ("norm_2_eq_no", "mann_whitney"),
    ("norm_2_diff_no", "mann_whitney"),
    ("norm_2_diff_yes", "welch_ttest"),

    ("norm_2_eq_yes", "bilanciamento"),
    ("bilanciamento", "bilanciate"),
    ("bilanciamento", "sbilanciate"),
    ("bilanciate", "t_test"),
    ("sbilanciate", "welch_ttest"),

    ("norm_gt2_eq_yes", "bilanciamento_gt2"),
    ("bilanciamento_gt2", "bilanciate_gt2"),
    ("bilanciamento_gt2", "sbilanciate_gt2"),
    ("bilanciate_gt2", "anova_tukey"),
    ("sbilanciate_gt2", "welch_games"),

    ("norm_gt2_eq_no", "kruskal"),
    ("norm_gt2_diff_no", "kruskal"),
    ("norm_gt2_diff_yes", "welch_games"),
]

G.add_edges_from(edges)

# 📌 Posizionamento dei nodi per la visualizzazione corretta
pos = {
    "xlsx": (0, 8),
    "num_tesi": (0, 7),
    "tesi_2": (-2, 6),
    "tesi_gt2": (2, 6),

    "var_2_eq": (-3, 5),
    "var_2_diff": (-1, 5),
    "var_gt2_eq": (1, 5),
    "var_gt2_diff": (3, 5),

    "norm_2_eq_yes": (-3.5, 4),
    "norm_2_eq_no": (-2.5, 4),
    "norm_2_diff_yes": (-1.5, 4),
    "norm_2_diff_no": (-0.5, 4),
    "norm_gt2_eq_yes": (0.5, 4),
    "norm_gt2_eq_no": (1.5, 4),
    "norm_gt2_diff_yes": (2.5, 4),
    "norm_gt2_diff_no": (3.5, 4),

    "bilanciamento": (-3.5, 3),
    "bilanciamento_gt2": (0.5, 3),

    "bilanciate": (-4, 2),
    "sbilanciate": (-3, 2),
    "bilanciate_gt2": (0, 2),
    "sbilanciate_gt2": (1, 2),

    # Test finali
    "anova_tukey": (-1, 1),
    "kruskal": (1, 1),
    "welch_games": (3, 1),
    "t_test": (-4, 1),
    "welch_ttest": (-3, 1),
    "mann_whitney": (-2.5, 1),
    "games": (2, 1)
}

# Disegno del grafo
plt.figure(figsize=(16, 12))
nx.draw_networkx_nodes(G, pos, node_color="lightgray", node_size=3000)
nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=30, width=2, edge_color="gray")
nx.draw_networkx_labels(G, pos, labels=nodes, font_size=9, font_weight="bold")

st.pyplot(plt)
