# ... tutto il codice dei test (Grubbs, Dixon, Rosner) rimane invariato ...

# Visualizzazione risultati
results_df = pd.DataFrame(outlier_results)
st.subheader("📊 **Risultati dei Test di Outlier**")
st.dataframe(results_df, width=900)

# Spiegazione dei test
st.markdown("""
### 📌 **Descrizione dei test utilizzati**
✔ **Test di Grubbs**: Identifica un singolo outlier nei dati normalmente distribuiti. Utilizzato in contesti normativi come **ASTM E178** e **ISO 5725**.  
✔ **Test di Dixon (Q-test)**: Adatto per dataset **piccoli**. Raccomandato dall'**IUPAC** per la validazione di metodi chimici.  
✔ **Test di Rosner**: Permette di identificare **più outlier contemporaneamente**. Applicato nei laboratori chimici per analisi robuste.  
""")

# Salva risultati per uso successivo (facoltativo)
st.session_state["outlier_results"] = results_df
