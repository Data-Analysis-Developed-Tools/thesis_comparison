import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx

st.markdown("<h3 style='text-align: center;'>📊 MAPPA DECISIONALE DEL TEST STATISTICO</h3>", unsafe_allow_html=True)

# ✅ Controllo dati disponibili
required_vars = ["num_cols", "inequality_ratio", "varianze_uguali", "almeno_una_non_normale"]
missing = [var for var in required_vars if var not in st.session_state]

if missing:
    st.error(f"⚠️ Dati mancanti! Torna alla sezione 'Analisi Preliminare'. Variabili mancanti: {', '.join(missing)}")
    st.stop()

# ✅ Recupera dati
num_tesi = len(st.session_state["num_cols"])
inequality_ratio = st.session_state["inequality_ratio"]
varianze_uguali = st.session_state["varianze_uguali"]
almeno_una_non_normale = st.session_state["almeno_una_non_normale"]

# 🔹 Creazione del grafo
G = nx.DiGraph()

# 🔹 Definizione dei nodi
nodes = {
    "start": "📂 File .xlsx caricato",
    "num_tesi": f"📊 Numero tesi: {num_tesi}",
    "levene": "📊 Confronto varianze (Levene)",
    "uguali": "✅ Varianze uguali",
    "diverse": "❌ Varianze diverse",
    "shapiro": "📉 Test di Normalità (Shapiro-Wilk)",
    "bilanciamento": "⚖️ Controllo bilanciamento",
    "kruskal": "📊 Test selezionato: Kruskal-Wallis",
    "mann_whitney": "📊 Test selezionato: Mann-Whitney U",
    "welch_anova": "📊 Test selezionato: Welch ANOVA",
    "tukey": "📊 Test selezionato: ANOVA + Tukey HSD",
    "t_test": "📊 Test selezionato: T-test classico",
    "t_test_welch": "📊 Test selezionato: T-test di Welch",
    "games_howell": "📊 Test selezionato: Welch ANOVA + Games-Howell"
}

# Aggiunta nodi al grafo
G.add_nodes_from(nodes.keys())

# 🔹 Definizione delle connessioni
edges = [
    ("start", "num_tesi"),
    ("num_tesi", "levene"),
    ("levene", "uguali"),
    ("levene", "diverse"),
    ("uguali", "shapiro"),
    ("diverse", "shapiro"),
    ("shapiro", "bilanciamento"),
    ("bilanciamento", "kruskal"),
    ("bilanciamento", "mann_whitney"),
    ("bilanciamento", "welch_anova"),
    ("bilanciamento", "tukey"),
    ("bilanciamento", "t_test"),
    ("bilanciamento", "t_test_welch"),
    ("bilanciamento", "games_howell")
]
G.add_edges_from(edges)

# 🔹 Determina il percorso attivo basato sui dati
path = ["start", "num_tesi", "levene"]
if varianze_uguali:
    path.append("uguali")
else:
    path.append("diverse")

path.append("shapiro")
path.append("bilanciamento")

if almeno_una_non_normale:
    if num_tesi > 2:
        path.append("kruskal")
    else:
        path.append("mann_whitney")
else:
    if inequality_ratio > 3:
        if num_tesi > 2:
            path.append("games_howell")
        else:
            path.append("t_test_welch")
    else:
        if num_tesi > 2:
            path.append("tukey")
        else:
            path.append("t_test")

# 🔹 Imposta il layout **senza `pygraphviz`**
pos = nx.shell_layout(G)

# 🎨 **Disegna il grafo**
plt.figure(figsize=(12, 8))

# **Disegna tutti i nodi in grigio chiaro per mostrare l'intero percorso**
nx.draw(G, pos, with_labels=True, labels=nodes, node_color="lightgray", edge_color="gray",
        node_size=2500, font_size=9, font_weight="bold", alpha=0.7)

# **Evidenzia il percorso selezionato in BLU**
highlight_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
highlight_nodes = path

nx.draw_networkx_nodes(G, pos, nodelist=highlight_nodes, node_color="lightblue", node_size=3000)
nx.draw_networkx_edges(G, pos, edgelist=highlight_edges, edge_color="blue", width=2.5)

st.pyplot(plt)

# 🔹 **Messaggio riassuntivo**
st.markdown(f"""
### ✅ **Analisi completata!**
- 🔍 **Numero di tesi:** {num_tesi}
- 📊 **Varianze uguali?** {"✅ Sì" if varianze_uguali else "❌ No"}
- 📉 **Almeno una distribuzione non normale?** {"❌ Sì" if almeno_una_non_normale else "✅ No"}
- ⚖️ **Rapporto Max/Min:** {inequality_ratio:.2f}

### 📌 **Test statistico selezionato:**
📝 **{nodes[path[-1]]}**
""")
