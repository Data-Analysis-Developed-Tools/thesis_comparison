import streamlit as st
import pandas as pd
import scipy.stats as stats
import pingouin as pg
from data_loader import load_data

# 🌟 Titolo principale con dimensione doppia
st.markdown("<h1 style='text-align: center; font-size: 170%;'>📊 Comparison Test Between Theses</h1>", unsafe_allow_html=True)

# 📂 Sidebar - Caricamento file
st.sidebar.header("⚙️ Settings")

# 📌 Istruzioni nella sidebar
st.sidebar.markdown("""
📌 **Instructions:**
- Thesis **name in first line**  
- **No header** for repetition lines
""")

# 📂 File uploader
uploaded_file = st.sidebar.file_uploader("📂 Upload an Excel file (.xlsx)", type=["xlsx"])

# 🔍 Controllo se il file è stato caricato
if uploaded_file:
    df = load_data(uploaded_file)  # 📂 Carica i dati

    # ✅ Controllo se i dati sono validi
    if df is not None and not df.empty:
        st.write("✅ **Data uploaded successfully!**")
        st.write(df.head())  # Mostra anteprima dei dati

        # 🔍 Test di normalità (Shapiro-Wilk)
        st.sidebar.subheader("📈 Normality & Variance Tests")
        st.sidebar.write("🧪 **Normality test used: Shapiro-Wilk**")
        
        normality_results = {}
        for thesis in df.columns:
            stat, p_value = stats.shapiro(df[thesis].dropna())  # Rimuove i NaN prima del test
            normality_results[thesis] = p_value

        # 📊 Mostra risultati del test di normalità
        for thesis, p_val in normality_results.items():
            result_text = f"✅ Normal" if p_val > 0.05 else f"⚠️ Not Normal"
            st.sidebar.write(f"**{thesis}**: p = {p_val:.4f} ({result_text})")

        # 🔍 Test di Levene per la varianza
        stat_levene, p_levene = stats.levene(*[df[col].dropna() for col in df.columns])
        variance_homogeneity = p_levene > 0.05
        levene_result_text = "✅ Variances are homogeneous" if variance_homogeneity else "⚠️ Variances are heterogeneous"
        st.sidebar.write(f"**Levene's Test**: p = {p_levene:.4f} ({levene_result_text})")

        # 📌 Esecuzione dei test statistici
        num_groups = len(df.columns)

        if all(p > 0.05 for p in normality_results.values()):  # Dati normali
            if variance_homogeneity:
                st.subheader("🏆 Performing **Standard ANOVA**")
                anova = pg.anova(data=df.melt(var_name="Thesis", value_name="Value"), dv="Value", between="Thesis", detailed=True)
                st.dataframe(anova, use_container_width=True)
            else:
                st.subheader("📈 Performing **Welch's ANOVA** (for unequal variances)")
                welch_anova = pg.welch_anova(data=df.melt(var_name="Thesis", value_name="Value"), dv="Value", between="Thesis")
                st.dataframe(welch_anova, use_container_width=True)

else:
    st.sidebar.warning("📂 Upload an Excel file to proceed.")
