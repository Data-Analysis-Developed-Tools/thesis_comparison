import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx

st.markdown("<h3 style='text-align: center;'>📊 MAPPA DECISIONALE DEL TEST STATISTICO</h3>", unsafe_allow_html=True)

# ✅ Controllo dati disponibili
required_vars = ["num_cols", "varianze_uguali"]
missing = [var for var in required_vars if var not in st.session_state]

if missing:
    st.error(f"⚠️ Dati mancanti! Torna alla sezione 'Analisi Preliminare'. Variabili mancanti: {', '.join(missing)}")
    st.stop()

# ✅ Recupera dati
num_tesi = len(st.session_state["num_cols"])
varianze_uguali = st.session_state["varianze_uguali"]

# 🔹 Creazione del grafo
G = nx.DiGraph()

# 🔹 Definizione dei nodi
nodes = {
    "start": "📂 File .xlsx caricato",
    "num_tesi": "🔍 Numero delle tesi",
    "tesi_2": "📊 2 tesi",
    "tesi_maggiori": "📊 Più di 2 tesi",
    "levene_2": "📉 Confronto delle varianze (Levene)",
    "levene_maggiori": "📉 Confronto delle varianze (Levene)",
    "uguali_2": "✅ Varianze statisticamente uguali",
    "diverse_2": "❌ Varianze statisticamente diverse",
    "uguali_maggiori": "✅ Varianze statisticamente uguali",
    "diverse_maggiori": "❌ Varianze statisticamente diverse"
}

# Aggiunta nodi al grafo
G.add_nodes_from(nodes.keys())

# 🔹 Definizione delle connessioni
edges = [
    ("start", "num_tesi"),
    ("num_tesi", "tesi_2"),
    ("num_tesi", "tesi_maggiori"),
    ("tesi_2", "levene_2"),
    ("tesi_maggiori", "levene_maggiori"),
    ("levene_2", "uguali_2"),
    ("levene_2", "diverse_2"),
    ("levene_maggiori", "uguali_maggiori"),
    ("levene_maggiori", "diverse_maggiori")
]
G.add_edges_from(edges)

# 🔹 Determina il percorso attivo basato sui dati
path = ["start", "num_tesi"]
if num_tesi == 2:
    path.append("tesi_2")
    path.append("levene_2")
    if varianze_uguali:
        path.append("uguali_2")
    else:
        path.append("diverse_2")
else:
    path.append("tesi_maggiori")
    path.append("levene_maggiori")
    if varianze_uguali:
        path.append("uguali_maggiori")
    else:
        path.append("diverse_maggiori")

# 🔹 **Usiamo il layout gerarchico senza `pygraphviz`**
pos = nx.multipartite_layout(G, subset_key=lambda n: list(nodes.keys()).index(n))

# 🎨 **Disegna il grafo**
plt.figure(figsize=(10, 12))  # 🔄 Layout verticale più alto

# **Disegna tutti i nodi in grigio chiaro per mostrare l'intero percorso**
nx.draw(G, pos, with_labels=False, node_color="lightgray", edge_color="gray",
        node_size=2500, alpha=0.7, arrows=True, arrowsize=35, width=3)

# **Evidenzia il percorso selezionato in BLU con frecce più grandi**
highlight_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
highlight_nodes = path

nx.draw_networkx_nodes(G, pos, nodelist=highlight_nodes, node_color="lightblue", node_size=3000)
nx.draw_networkx_edges(G, pos, edgelist=highlight_edges, edge_color="blue", width=4.5, arrows=True, arrowsize=35)

# **Posizionamento delle etichette ottimizzato**
label_pos = {key: (x, y - 0.05) for key, (x, y) in pos.items()}  # 🔄 Abbassiamo il testo per evitare sovrapposizioni
nx.draw_networkx_labels(G, label_pos, labels=nodes, font_size=10, font_weight="bold")

st.pyplot(plt)

# 🔹 **Messaggio riassuntivo**
st.markdown(f"""
### ✅ **Analisi completata!**
- 🔍 **Numero di tesi:** {num_tesi}
- 📊 **Varianze uguali?** {"✅ Sì" if varianze_uguali else "❌ No"}
""")
