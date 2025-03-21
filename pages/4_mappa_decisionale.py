import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx

st.markdown("<h3 style='text-align: center;'>📊 MAPPA DECISIONALE PER LA SCELTA DEL TEST STATISTICO</h3>", unsafe_allow_html=True)

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
nodi = {
    "Input": "📂 File .xlsx in input",
    "Tesi": "📊 Numero delle tesi",
    "Levene": "📊 Confronto varianze (Levene)",
    "Uguali": "✅ Varianze uguali",
    "Diverse": "❌ Varianze diverse",
    "Shapiro": "📉 Test di Normalità (Shapiro-Wilk)",
    "Bilanciamento": "⚖️ Dati sbilanciati?",
    "Kruskal": "Test: Kruskal-Wallis",
    "Mann-Whitney": "Test: Mann-Whitney U",
    "Welch": "Test: Welch ANOVA",
    "Tukey": "Test: ANOVA + Tukey HSD",
    "T-test": "Test: T-test classico",
    "T-test Welch": "Test: T-test di Welch"
}

# 🔹 Aggiunta nodi al grafo
G.add_nodes_from(nodi.keys())

# 🔹 Definizione delle connessioni
G.add_edges_from([
    ("Input", "Tesi"),
    ("Tesi", "Levene"),
    ("Levene", "Uguali"),
    ("Levene", "Diverse"),
    ("Uguali", "Shapiro"),
    ("Diverse", "Shapiro"),
    ("Shapiro", "Bilanciamento"),
    ("Bilanciamento", "Kruskal"),
    ("Bilanciamento", "Mann-Whitney"),
    ("Bilanciamento", "Welch"),
    ("Bilanciamento", "Tukey"),
    ("Bilanciamento", "T-test"),
    ("Bilanciamento", "T-test Welch")
])

# 🔹 Determina il percorso attivo basato sui dati
path = ["Input", "Tesi", "Levene"]

if varianze_uguali:
    path.append("Uguali")
else:
    path.append("Diverse")

path.append("Shapiro")

if almeno_una_non_normale:
    path.append("Kruskal" if num_tesi > 2 else "Mann-Whitney")
else:
    if inequality_ratio > 3:
        path.append("Welch" if num_tesi > 2 else "T-test Welch")
    else:
        path.append("Tukey" if num_tesi > 2 else "T-test")

# 🔹 Imposta il layout per evitare il bug della posizione dei nodi
pos = nx.spring_layout(G, seed=42)

# 🔹 Disegna il grafo
plt.figure(figsize=(12, 6))
nx.draw(G, pos, with_labels=True, labels=nodi, node_color="lightgray", edge_color="gray", node_size=3000, font_size=8, font_weight="bold")

# 🔹 Evidenzia il percorso selezionato
highlight_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
highlight_nodes = path

nx.draw_networkx_nodes(G, pos, nodelist=highlight_nodes, node_color="lightblue", node_size=3500)
nx.draw_networkx_edges(G, pos, edgelist=highlight_edges, edge_color="blue", width=2.5)

st.pyplot(plt)

# 🔹 Messaggio riassuntivo
st.markdown(f"""
### ✅ **Analisi completata!**
- 🔍 **Numero di tesi:** {num_tesi}
- 📊 **Varianze uguali?** {"✅ Sì" if varianze_uguali else "❌ No"}
- 📉 **Almeno una distribuzione non normale?** {"❌ Sì" if almeno_una_non_normale else "✅ No"}
- ⚖️ **Rapporto Max/Min:** {inequality_ratio:.2f}

### 📌 **Test statistico selezionato:**
📝 **{nodi[path[-1]]}**
""")
