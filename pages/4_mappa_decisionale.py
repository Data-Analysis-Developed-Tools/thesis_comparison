import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

st.markdown("<h3 style='text-align: center;'>📊 Mappa Decisionale – Selezione del Test Statistico</h3>", unsafe_allow_html=True)

# Creazione del grafo diretto
G = nx.DiGraph()

# Dizionario dei nodi con etichette
nodes = {
    "xlsx": "📂 File .xlsx caricato",
    "num_tesi": "🔍 Numero delle tesi",
    "tesi_2": "📊 2 tesi",
    "tesi_gt2": "📊 >2 tesi",

    # Confronto varianze
    "var_2_eq": "✅ Varianze uguali",
    "var_2_diff": "❌ Varianze diverse",
    "var_gt2_eq": "✅ Varianze uguali",
    "var_gt2_diff": "❌ Varianze diverse",

    # Normalità distribuzioni
    "norm_2_eq_yes": "✅ Tutte distribuzioni normali",
    "norm_2_eq_no": "❌ Almeno una non normale",
    "norm_2_diff_yes": "✅ Tutte distribuzioni normali",
    "norm_2_diff_no": "❌ Almeno una non normale",

    "norm_gt2_eq_yes": "✅ Tutte distribuzioni normali",
    "norm_gt2_eq_no": "❌ Almeno una non normale",
    "norm_gt2_diff_yes": "✅ Tutte distribuzioni normali",
    "norm_gt2_diff_no": "❌ Almeno una non normale"
}

# Aggiungiamo tutti i nodi
G.add_nodes_from(nodes.keys())

# Connessioni (archi) tra nodi
edges = [
    ("xlsx", "num_tesi"),
    ("num_tesi", "tesi_2"),
    ("num_tesi", "tesi_gt2"),

    # Confronto varianze per 2 tesi
    ("tesi_2", "var_2_eq"),
    ("tesi_2", "var_2_diff"),

    # Confronto varianze per >2 tesi
    ("tesi_gt2", "var_gt2_eq"),
    ("tesi_gt2", "var_gt2_diff"),

    # Dicotomia normalità - 2 tesi
    ("var_2_eq", "norm_2_eq_yes"),
    ("var_2_eq", "norm_2_eq_no"),
    ("var_2_diff", "norm_2_diff_yes"),
    ("var_2_diff", "norm_2_diff_no"),

    # Dicotomia normalità - >2 tesi
    ("var_gt2_eq", "norm_gt2_eq_yes"),
    ("var_gt2_eq", "norm_gt2_eq_no"),
    ("var_gt2_diff", "norm_gt2_diff_yes"),
    ("var_gt2_diff", "norm_gt2_diff_no")
]

G.add_edges_from(edges)

# Posizioni verticali personalizzate (layout manuale top-down)
pos = {
    "xlsx": (0, 6),
    "num_tesi": (0, 5),
    "tesi_2": (-2, 4),
    "tesi_gt2": (2, 4),

    "var_2_eq": (-3, 3),
    "var_2_diff": (-1, 3),
    "var_gt2_eq": (1, 3),
    "var_gt2_diff": (3, 3),

    "norm_2_eq_yes": (-3.5, 2),
    "norm_2_eq_no": (-2.5, 2),
    "norm_2_diff_yes": (-1.5, 2),
    "norm_2_diff_no": (-0.5, 2),

    "norm_gt2_eq_yes": (0.5, 2),
    "norm_gt2_eq_no": (1.5, 2),
    "norm_gt2_diff_yes": (2.5, 2),
    "norm_gt2_diff_no": (3.5, 2),
}

# Disegno del grafo
plt.figure(figsize=(13, 10))
nx.draw_networkx_nodes(G, pos, node_color="lightgray", node_size=3000)
nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle='-|>', arrowsize=30, width=2, edge_color="gray")
nx.draw_networkx_labels(G, pos, labels=nodes, font_size=9, font_weight="bold")

st.pyplot(plt)
