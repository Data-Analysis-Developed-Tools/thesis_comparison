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
    "norm_gt2_diff_no": "❌ Almeno una\nNon Normale"
}

G.add_nodes_from(nodes.keys())

# Connessioni tra i nodi fino alle scelte di normalità (ora senza connessioni inferiori)
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
    ("var_gt2_diff", "norm_gt2_diff_no")
]

G.add_edges_from(edges)

# 📌 Posizionamento dei nodi (mantenendo la struttura senza connessioni inferiori)
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
    "norm_gt2_diff_no": (3.5, 5)
}

# Disegno del grafo senza connessioni inferiori
plt.figure(figsize=(16, 10))
nx.draw_networkx_nodes(G, pos, node_color="lightgray", node_size=3000)
nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=30, width=2, edge_color="gray")
nx.draw_networkx_labels(G, pos, labels=nodes, font_size=9, font_weight="bold")

st.pyplot(plt)
