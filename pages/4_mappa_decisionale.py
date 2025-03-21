import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

st.markdown("<h3 style='text-align: center;'>📊 Mappa Decisionale – Selezione del Test Statistico</h3>", unsafe_allow_html=True)

# Creazione del grafo diretto
G = nx.DiGraph()

# Definizione dei nodi con etichette descrittive
nodes = {
    "xlsx": "📂 File .xlsx\nCaricato",
    "num_tesi": "🔍 Numero\ndelle tesi",
    "tesi_2": "📊 2 Tesi",
    "tesi_gt2": "📊 >2 Tesi",

    "var_2_eq": "✅ Varianze\nUguali",
    "var_2_diff": "❌ Varianze\nDiverse",
    "var_gt2_eq": "✅ Varianze\nUguali",
    "var_gt2_diff": "❌ Varianze\nDiverse",

    "norm_2_eq_yes": "✅ Tutte le\nDistribuzioni Normali",
    "norm_2_eq_no": "❌ Almeno una\nNon Normale",
    "norm_2_diff_yes": "✅ Tutte le\nDistribuzioni Normali",
    "norm_2_diff_no": "❌ Almeno una\nNon Normale",
    "norm_gt2_eq_yes": "✅ Tutte le\nDistribuzioni Normali",
    "norm_gt2_eq_no": "❌ Almeno una\nNon Normale",
    "norm_gt2_diff_yes": "✅ Tutte le\nDistribuzioni Normali",
    "norm_gt2_diff_no": "❌ Almeno una\nNon Normale",

    "bilanciamento": "⚖️ Bilanciamento\nDelle Tesi",
    "bilanciate": "✅ Tesi\nBilanciate",
    "sbilanciate": "❌ Tesi\nSbilanciate",

    "bilanciamento_gt2": "⚖️ Bilanciamento\nDelle Tesi",
    "bilanciate_gt2": "✅ Tesi\nBilanciate",
    "sbilanciate_gt2": "❌ Tesi\nSbilanciate",

    # Nodi di decisione finale
    "anova_tukey": "🧪 ANOVA\n+ Tukey HSD",
    "kruskal": "🧪 Kruskal-Wallis\n+ Dunn Bonferroni",
    "welch_games": "🧪 Welch ANOVA\n+ Games-Howell",
    "t_test": "🧪 T-test",
    "welch_ttest": "🧪 T-test di Welch",
    "mann_whitney": "🧪 Mann-Whitney U test",
    "games": "🧪 Games-Howell test"
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

# 📌 Posizionamento dei nodi (versione precedente ripristinata)
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

    # Test finali (ripristinati con la versione precedente)
    "anova_tukey": (-3, 2),
    "kruskal": (-1, 2),
    "welch_games": (1, 2),
    "t_test": (-5, 2),
    "welch_ttest": (-4, 2),
    "mann_whitney": (-2, 2),
    "games": (3, 2)
}

# Disegno del grafo
plt.figure(figsize=(16, 12))
nx.draw_networkx_nodes(G, pos, node_color="lightgray", node_size=3000)
nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=30, width=2, edge_color="gray")
nx.draw_networkx_labels(G, pos, labels=nodes, font_size=9, font_weight="bold")

st.pyplot(plt)
