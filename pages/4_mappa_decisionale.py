import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

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

# 🔹 Determina il percorso attivo basato sui dati
decisioni = []
decisioni.append("📂 File .xlsx caricato")
decisioni.append(f"📊 Numero tesi: {num_tesi}")

if num_tesi == 2:
    decisioni.append("📊 Confronto varianze (Levene)")
    if varianze_uguali:
        decisioni.append("✅ Varianze uguali")
    else:
        decisioni.append("❌ Varianze diverse")

    decisioni.append("📉 Test di Normalità (Shapiro-Wilk)")
    if almeno_una_non_normale:
        decisioni.append("📊 **Test selezionato: Mann-Whitney U**")
    else:
        if inequality_ratio > 3:
            decisioni.append("📊 **Test selezionato: T-test di Welch**")
        else:
            decisioni.append("📊 **Test selezionato: T-test classico**")
else:
    decisioni.append("📊 Confronto varianze (Levene)")
    if varianze_uguali:
        decisioni.append("✅ Varianze uguali")
    else:
        decisioni.append("❌ Varianze diverse")

    decisioni.append("📉 Test di Normalità (Shapiro-Wilk)")
    if almeno_una_non_normale:
        decisioni.append("📊 **Test selezionato: Kruskal-Wallis**")
    else:
        if inequality_ratio > 3:
            decisioni.append("📊 **Test selezionato: Welch ANOVA**")
        else:
            decisioni.append("📊 **Test selezionato: ANOVA + Tukey HSD**")

# 🎨 **Creazione del grafico**
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, len(decisioni) + 1)
ax.axis("off")

# 🔹 **Disegna i rettangoli e le connessioni**
for i, step in enumerate(decisioni):
    ax.add_patch(patches.FancyBboxPatch((3, len(decisioni) - i), 4, 0.8, 
                                        boxstyle="round,pad=0.3", 
                                        edgecolor="black", facecolor="lightblue"))
    ax.text(5, len(decisioni) - i + 0.4, step, ha="center", va="center", fontsize=10, weight="bold")

    # Connessioni
    if i > 0:
        ax.annotate("", xy=(5, len(decisioni) - i + 0.8), xytext=(5, len(decisioni) - i + 1.2),
                    arrowprops=dict(arrowstyle="->", lw=2, color="black"))

# 🎯 **Mostra il grafico**
st.pyplot(fig)

# 🔹 **Messaggio riassuntivo**
st.markdown(f"""
### ✅ **Analisi completata!**
- 🔍 **Numero di tesi:** {num_tesi}
- 📊 **Varianze uguali?** {"✅ Sì" if varianze_uguali else "❌ No"}
- 📉 **Almeno una distribuzione non normale?** {"❌ Sì" if almeno_una_non_normale else "✅ No"}
- ⚖️ **Rapporto Max/Min:** {inequality_ratio:.2f}

### 📌 **Test statistico selezionato:**
📝 **{decisioni[-1]}**
""")
