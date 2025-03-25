import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

st.markdown("<h3 style='text-align: center;'>📊 Mappa Decisionale – Selezione del Test Statistico</h3>", unsafe_allow_html=True)

# Creazione del grafo
G = nx.DiGraph()

# Nodi iniziali
G.add_node("xlsx", label="📂 File .xlsx\nCaricato")
G.add_node("num_tesi", label="🔍 Numero\ndelle tesi")
G.add_node("tesi_2", label="📊 2 Tesi")
G.add_node("tesi_gt2", label="📊 >2 Tesi")

# Nodi confronto varianze
G.add_node("var_2_eq", label="✅ Varianze\nUguali")
G.add_node("var_2_diff", label="❌ Varianze\nDiverse")
G.add_node("var_gt2_eq", label="✅ Varianze\nUguali")
G.add_node("var_gt2_diff", label="❌ Varianze\nDiverse")

# Nodi normalità
G.add_node("norm_2_eq_yes", label="✅ Tutte le\nDistribuzioni Normali")
G.add_node("norm_2_eq_no", label="❌ Almeno una\nNon Normale")
G.add_node("norm_gt2_diff_no", label="❌ Almeno una\nNon Normale")
G.add_node("norm_gt2_diff_yes", label="✅ Tutte le\nDistribuzioni Normali")
G.add_node("norm_gt2_eq_no", label="❌ Almeno una\nNon Normale")
G.add_node("norm_gt2_eq_yes", label="✅ Tutte le\nDistribuzioni Normali")

# Nodo controllo bilanciamento
G.add_node("bilanciamento_ok", label="⚖️ Osservazioni\nbilanciate?")
G.add_node("anova_test", label="🧪 ANOVA test")
G.add_node("tukey_hsd", label="🧪 Tukey HSD test")

# Nodi test statistici
G.add_node("mann_whitney", label="🧪 Mann-Whitney U test")
G.add_node("welch_anova", label="🧪 Welch ANOVA test")
G.add_node("games_howell", label="🧪 Games-Howell test")
G.add_node("kruskal_gt2_eq", label="🧪 Kruskal-Wallis test")
G.add_node("dunn_gt2_eq", label="🧪 Dunn test\n(+ Bonferroni)")

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
    ("tesi_gt2", "var_gt2_diff"),

    ("var_gt2_diff", "norm_gt2_diff_no"),
    ("var_gt2_diff", "norm_gt2_diff_yes"),
    ("norm_gt2_diff_no", "games_howell"),
    ("norm_gt2_diff_yes", "welch_anova"),
    ("welch_anova", "games_howell"),

    ("var_gt2_eq", "norm_gt2_eq_no"),
    ("norm_gt2_eq_no", "kruskal_gt2_eq"),
    ("kruskal_gt2_eq", "dunn_gt2_eq"),

    ("var_gt2_eq", "norm_gt2_eq_yes"),
    ("norm_gt2_eq_yes", "bilanciamento_ok"),
    ("bilanciamento_ok", "anova_test"),
    ("anova_test", "tukey_hsd")
]
G.add_edges_from(edges)

# Posizionamento nodi
pos = {
    "xlsx": (0, 7),
    "num_tesi": (0, 6),
    "tesi_2": (-4, 5),
    "tesi_gt2": (4, 5),

    "var_2_eq": (-4.5, 4),
    "var_2_diff": (-3.5, 4),
    "norm_2_eq_yes": (-5.2, 3),
    "norm_2_eq_no": (-4.2, 3),
    "mann_whitney": (-4.2, 2),

    "var_gt2_eq": (3.5, 4),
    "var_gt2_diff": (4.5, 4),
    "norm_gt2_eq_no": (3.5, 3),
    "kruskal_gt2_eq": (3.5, 2),
    "dunn_gt2_eq": (3.5, 1),

    "norm_gt2_eq_yes": (4.5, 3),
    "bilanciamento_ok": (4.5, 2),
    "anova_test": (4.5, 1),
    "tukey_hsd": (4.5, 0),

    "norm_gt2_diff_no": (5.2, 3),
    "norm_gt2_diff_yes": (5.8, 3),
    "welch_anova": (5.8, 2),
    "games_howell": (5.5, 1)
}

# Etichette
labels = nx.get_node_attributes(G, 'label')

# Disegno del grafo
plt.figure(figsize=(16, 10))
nx.draw(G, pos, with_labels=False, node_color="lightgray", node_size=3200, arrows=True, edge_color="gray", width=1.5)
nx.draw_networkx_labels(G, pos, labels=labels, font_size=8.5, font_weight="bold")
plt.title("📌 Mappa Decisionale – ANOVA e Tukey HSD per casi bilanciati", fontsize=12)
plt.axis('off')
plt.tight_layout()
st.pyplot(plt)
