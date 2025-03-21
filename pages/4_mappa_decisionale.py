import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx

st.markdown("<h3 style='text-align: center;'>📊 VISUALIZZAZIONE DEL PROCESSO DI SELEZIONE</h3>", unsafe_allow_html=True)

# ✅ Controllo che i dati siano presenti
required_vars = ["num_cols", "inequality_ratio", "varianze_uguali", "almeno_una_non_normale"]
missing = [var for var in required_vars if var not in st.session_state]

if missing:
    st.error(f"⚠️ Dati mancanti! Torna alla sezione 'Analisi Preliminare'. Variabili mancanti: {', '.join(missing)}")
    st.stop()

# ✅ Recupera informazioni
num_tesi = len(st.session_state["num_cols"])
inequality_ratio = st.session_state["inequality_ratio"]
varianze_uguali = st.session_state["varianze_uguali"]
almeno_una_non_normale = st.session_state["almeno_una_non_normale"]

# 🔹 Creazione del grafo del diagramma di flusso
G = nx.DiGraph()

# 🔹 Definizione dei nodi principali
G.add_nodes_from([
    "File .xlsx in input",
    "Numero delle tesi",
    "Confronto varianze (test di Levene)",
    "Statisticamente uguali",
    "Statisticamente diverse",
    "Almeno una tesi non normale? (Shapiro-Wilk)",
    "Le osservazioni sono molto sbilanciate?",
    "Test selezionato"
])

# 🔹 Aggiunta delle connessioni per la logica del diagramma
G.add_edges_from([
    ("File .xlsx in input", "Numero delle tesi"),
    ("Numero delle tesi", "Confronto varianze (test di Levene)"),
    ("Confronto varianze (test di Levene)", "Statisticamente uguali"),
    ("Confronto varianze (test di Levene)", "Statisticamente diverse"),
    ("Statisticamente uguali", "Almeno una tesi non normale? (Shapiro-Wilk)"),
    ("Statisticamente diverse", "Almeno una tesi non normale? (Shapiro-Wilk)"),
    ("Almeno una tesi non normale? (Shapiro-Wilk)", "Le osservazioni sono molto sbilanciate?"),
    ("Le osservazioni sono molto sbilanciate?", "Test selezionato")
])

# 🔹 Determinazione del percorso corretto basato sui dati
path = ["File .xlsx in input", "Numero delle tesi"]

if num_tesi == 2:
    path.append("Confronto varianze (test di Levene)")
    if varianze_uguali:
        path.append("Statisticamente uguali")
    else:
        path.append("Statisticamente diverse")
    
    path.append("Almeno una tesi non normale? (Shapiro-Wilk)")
    if almeno_una_non_normale:
        path.append("Test selezionato: Mann-Whitney U")
    else:
        if inequality_ratio > 3:
            path.append("Test selezionato: T-test di Welch")
        else:
            path.append("Test selezionato: T-test classico")
else:
    path.append("Confronto varianze (test di Levene)")
    if varianze_uguali:
        path.append("Statisticamente uguali")
    else:
        path.append("Statisticamente diverse")
    
    path.append("Almeno una tesi non normale? (Shapiro-Wilk)")
    if almeno_una_non_normale:
        path.append("Test selezionato: Kruskal-Wallis")
    else:
        if inequality_ratio > 3:
            path.append("Test selezionato: Welch ANOVA")
        else:
            path.append("Test selezionato: ANOVA + Tukey HSD")

# 🔹 Creazione della visualizzazione con evidenziazione del percorso scelto
plt.figure(figsize=(10, 6))
pos = nx.spring_layout(G, seed=42)

nx.draw(G, pos, with_labels=True, node_color="lightgray", edge_color="gray", node_size=2000, font_size=8, font_weight="bold")

# 🔹 Evidenziazione del percorso selezionato
highlight_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
highlight_nodes = path

nx.draw_networkx_nodes(G, pos, nodelist=highlight_nodes, node_color="lightblue", node_size=2500)
nx.draw_networkx_edges(G, pos, edgelist=highlight_edges, edge_color="blue", width=2.5)

st.pyplot(plt)

# 🔹 Messaggio riassuntivo per l'utente
st.markdown(f"""
### ✅ **Analisi completata!**
- 🔍 **Numero di tesi:** {num_tesi}
- 📊 **Varianze uguali?** {"✅ Sì" if varianze_uguali else "❌ No"}
- 📉 **Almeno una distribuzione non normale?** {"❌ Sì" if almeno_una_non_normale else "✅ No"}
- ⚖️ **Rapporto Max/Min:** {inequality_ratio:.2f}

### 📌 **Test statistico selezionato:**
📝 **{path[-1]}**
""")
