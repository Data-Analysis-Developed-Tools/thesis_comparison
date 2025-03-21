import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx

st.set_page_config(layout="wide")
st.markdown("<h3 style='text-align: center;'>📊 MAPPA DECISIONALE – FASE 1</h3>", unsafe_allow_html=True)

# 🔹 Definizione nodi e collegamenti
G = nx.DiGraph()

# Nodi principali
G.add_node("file", label="📂 File .xlsx caricato")
G.add_node("num_tesi", label="🔍 Numero delle tesi")
G.add_node("2_tesi", label="📊 2 tesi")
G.add_node(">2_tesi", label="📊 Più di 2 tesi")
G.add_node("var_uguali_2", label="✅ Varianze uguali")
G.add_node("var_diverse_2", label="❌ Varianze diverse")
G.add_node("var_uguali_n", label="✅ Varianze uguali")
G.add_node("var_diverse_n", label="❌ Varianze diverse")

# Connessioni
edges = [
    ("file", "num_tesi"),
    ("num_tesi", "2_tesi"),
    ("num_tesi", ">2_tesi"),
    ("2_tesi", "var_uguali_2"),
    ("2_tesi", "var_diverse_2"),
    (">2_tesi", "var_uguali_n"),
    (">2_tesi", "var_diverse_n"),
]
G.add_edges_from(edges)

# Layout verticale
pos = {
    "file": (0, 4),
    "num_tesi": (0, 3),
    "2_tesi": (-1.5, 2),
    ">2_tesi": (1.5, 2),
    "var_uguali_2": (-2, 1),
    "var_diverse_2": (-1, 1),
    "var_uguali_n": (1, 1),
    "var_diverse_n": (2, 1)
}

# Estrai etichette dai nodi
labels = nx.get_node_attributes(G, "label")

# Disegno
plt.figure(figsize=(12, 6))
nx.draw(G, pos, with_labels=False, node_size=3000, node_color="lightgray", edge_color="gray", arrows=True, arrowsize=25, width=2)
nx.draw_networkx_labels(G, pos, labels, font_size=10, font_weight="bold")
st.pyplot(plt)
