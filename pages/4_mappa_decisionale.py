import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

st.markdown("<h3 style='text-align: center;'>📊 Mappa Decisionale – Selezione del Test Statistico</h3>", unsafe_allow_html=True)

# Creazione del grafo
G = nx.DiGraph()

# Nodi principali
G.add_node("xlsx", label="📂 File .xlsx\nCaricato")
G.add_node("num_tesi", label="🔍 Numero\ndelle tesi")
G.add_node("tesi_2", label="📊 2 Tesi")
G.add_node("tesi_gt2", label="📊 >2 Tesi")

# Nodi varianze
G.add_node("var_2_eq", label="✅ Varianze\nUguali")
G.add_node("var_2_diff", label="❌ Varianze\nDiverse")
G.add_node("var_gt2_eq", label="✅ Varianze\nUguali")
G.add_node("var_gt2_diff", label="❌ Varianze\nDiverse")

# Nodi normalità
G.add_node("norm_2_eq_yes", label="✅ Tutte le\nDistribuzioni Normali")
G.add_node("norm_2_eq_no", label="❌ Almeno una\nNon Normale")

# Nodo foglia
G.add_node("mann_whitney", label="🧪 Mann-Whitney U test")

# Connessioni
edges = [
    ("xlsx", "num_tesi"),
    ("num_tesi", "tesi_2"),
    ("num_tesi", "tesi_gt2"),
    ("tesi_2", "var_2_eq"),
    ("tesi_2", "var_2_diff"),
    ("var_2_eq", "norm_2_eq_yes"),
    ("var_2_eq", "norm_2_eq_no"),
    ("var_2_diff", "norm_2_eq_no"),
    ("norm_2_eq_no", "mann_whitney"),
    ("tesi_gt2", "var_gt2_eq"),
    ("tesi_gt2", "var_gt2_diff")
]
G.add_edges_from(edges)

# Posizionamento nodi
pos = {
    "xlsx": (0, 6),
    "num_tesi": (0, 5),
    "tesi_2": (-2, 4),
    "tesi_gt2": (2, 4),
    "var_2_eq": (-2.5, 3),
    "var_2_diff": (-1.5, 3),
    "norm_2_eq_yes": (-3, 2),
    "norm_2_eq_no": (-2, 2),
    "mann_whitney": (-2, 1),
    "var_gt2_eq": (1.5, 3),
    "var_gt2_diff": (2.5, 3)
}

# Etichette visive
labels = nx.get_node_attributes(G, 'label')

# Disegno del grafo
plt.figure(figsize=(12, 7))
nx.draw(G, pos, with_labels=False, node_color="lightgray", node_size=3000, arrows=True, edge_color="gray")
nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, font_weight="bold")
plt.title("📌 Aggiunto confronto varianze per tesi > 2", fontsize=12)
plt.axis('off')
plt.tight_layout()
st.pyplot(plt)
