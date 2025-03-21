import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

st.markdown("<h3 style='text-align: center;'>📊 Mappa Decisionale – Selezione del Test Statistico</h3>", unsafe_allow_html=True)

# Creazione del grafo diretto
G = nx.DiGraph()

# Etichette multilivello
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

    # Dicotomie bilanciamento
    "bilanciamento": "⚖️ Bilanciamento\ndelle tesi",
    "bilanciate": "✅ Tesi\nbilanciate",
    "sbilanciate": "❌ Tesi\nsbilanciate",

    "bilanciamento_gt2": "⚖️ Bilanciamento\ndelle tesi",
    "bilanciate_gt2": "✅ Tesi\nbilanciate",
    "sbilanciate_gt2": "❌ Tesi\nsbilanciate",

    # Nuovi nodi intermedi per separare i test finali
    "anova_intermedio": "📊 ANOVA\nDecisione Finale",
    "kruskal_intermedio": "📊 Kruskal-Wallis\nDecisione Finale",
    "welch_intermedio": "📊 Welch ANOVA\nDecisione Finale",

    # Nodi-foglia (test finali)
    "t_test": "🧪 T-test",
    "welch_ttest": "🧪 T-test\ndi Welch",
    "mann_whitney": "🧪 Mann-Whitney\nU test",
    "kruskal": "🧪 Kruskal-Wallis\n(+ Dunn, Bonferroni)",
    "games": "🧪 Games-Howell\ntest",
    "welch_games": "🧪 Welch ANOVA\n+ Games-Howell",
    "anova_tukey": "🧪 ANOVA\n+ Tukey HSD"
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

    # Rami Mann-Whitney
    ("norm_2_diff_no", "mann_whitney"),
    ("norm_2_eq_no", "mann_whitney"),

    # Welch T-test
    ("norm_2_diff_yes", "welch_ttest"),

    # Bilanciamento per 2 tesi
    ("norm_2_eq_yes", "bilanciamento"),
    ("bilanciamento", "bilanciate"),
    ("bilanciamento", "sbilanciate"),
    ("bilanciate", "t_test"),
    ("sbilanciate", "welch_ttest"),

    # Bilanciamento per >2 tesi
    ("norm_gt2_eq_yes", "bilanciamento_gt2"),
    ("bilanciamento_gt2", "bilanciate_gt2"),
    ("bilanciamento_gt2", "sbilanciate_gt2"),
    ("bilanciate_gt2", "anova_intermedio"),
    ("sbilanciate_gt2", "welch_intermedio"),

    # Nuovo livello di separazione dei test finali
    ("norm_gt2_eq_no", "kruskal_intermedio"),
    ("norm_gt2_diff_no", "kruskal_intermedio"),
    ("norm_gt2_diff_yes", "welch_intermedio"),

    # Test finali
    ("anova_intermedio", "anova_tukey"),
    ("kruskal_intermedio", "kruskal"),
    ("welch_intermedio", "welch_games"),
]

G.add_edges_from(edges)

# 📌 Posizionamento dei nodi (corretta posizione per tutti)
pos = {
    "xlsx": (0, 9),
    "num_tesi": (0, 8),
    "tesi_2": (-2, 7),
    "tesi_gt2": (2, 7),

    "var_2_eq": (-3, 6),
    "var_2_diff": (-1, 6),
    "var_gt2_eq": (1, 6),
    "var_gt2_diff": (3, 6),

    "norm_2_eq_yes": (-3.5, 5),
    "norm_2_eq_no": (-2.5, 5),
    "norm_2_diff_yes": (-1.5, 5),
    "norm_2_diff_no": (-0.5, 5),
    "norm_gt2_eq_yes": (0.5, 5),
    "norm_gt2_eq_no": (1.5, 5),
    "norm_gt2_diff_yes": (2.5, 5),
    "norm_gt2_diff_no": (3.5, 5),

    "bilanciamento": (-3.5, 4),
    "bilanciamento_gt2": (0.5, 4),

    "bilanciate": (-4, 3),
    "sbilanciate": (-3, 3),
    "bilanciate_gt2": (0, 3),
    "sbilanciate_gt2": (1, 3),

    "anova_intermedio": (-1, 2),
    "kruskal_intermedio": (1, 2),
    "welch_intermedio": (3, 2),

    # Nodi finali
    "anova_tukey": (-1, 1),
    "kruskal": (1, 1),
    "welch_games": (3, 1)
}

# Disegno del grafo
plt.figure(figsize=(16, 12))
nx.draw_networkx_nodes(G, pos, node_color="lightgray", node_size=3000)
nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=30, width=2, edge_color="gray")
nx.draw_networkx_labels(G, pos, labels=nodes, font_size=9, font_weight="bold")

st.pyplot(plt)
