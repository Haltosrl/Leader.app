import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
import numpy as np

# Titolo dell'app con emoji
st.title("🚀 Leader - Opportunità di Guadagno")

# Descrizione
st.markdown("""
Gain Leader ti permette di calcolare i guadagni di un leader nel modello multilivello.

💡 **Modifica i valori per vedere come cambiano i guadagni!**
""")

# Creiamo un DataFrame vuoto con dimensioni predefinite
data = pd.DataFrame(np.zeros((5, 3)), columns=[f"Col_{i+1}" for i in range(3)])

# Rimuovere il menu a tendina dalla tabella e usare una selezione esterna
st.sidebar.header("Impostazioni Unità Immobiliare")
ui_type = st.sidebar.selectbox("Seleziona l'Unità Immobiliare (UI)", ["Monolocale", "Bilocale", "Trilocale"])
data['Col_1'] = ui_type

# Prezzo mensile dell'Unità Immobiliare
if ui_type == "Monolocale":
    capienza_massima = 3
    price = 60
elif ui_type == "Bilocale":
    capienza_massima = 5
    price = 75
elif ui_type == "Trilocale":
    capienza_massima = 7
    price = 95

vat = price * 0.10
price_with_vat = price * 1.10

# Mostrare dettagli sull'Unità Immobiliare
st.subheader("💼 Dettagli dell'Unità Immobiliare")
st.markdown(f"<small>Prezzo Mensile (IVA esclusa): €{price:,.2f}</small>", unsafe_allow_html=True)
st.markdown(f"<small>IVA (10%): €{vat:,.2f}</small>", unsafe_allow_html=True)
st.markdown(f"<small>Prezzo Mensile (IVA inclusa): €{price_with_vat:,.2f}</small>", unsafe_allow_html=True)


st.markdown(f"<small>Capienza Massima: {capienza_massima} persone</small>", unsafe_allow_html=True)

# Calcolo del totale annuale e totale pagato in 10 anni
annual_total = price_with_vat * 12
total_10_years = annual_total * 10

st.subheader("💰 Totale Pagato")
col1, col2 = st.columns(2)
col1.metric(label="Totale Annuale", value=f"€{annual_total:,.2f}".replace('.', ',').replace(',', '.', 1), label_visibility='collapsed')
col1.markdown(f"<small>Totale Annuale: €{annual_total:,.2f}</small>", unsafe_allow_html=True)
col2.metric(label="Totale in 10 Anni", value=f"€{total_10_years:,.2f}".replace('.', ',').replace(',', '.', 1), label_visibility='collapsed')
col2.markdown(f"<small>Totale in 10 Anni: €{total_10_years:,.2f}</small>", unsafe_allow_html=True)

# Variabile: quanti diretti posso fare in un anno
st.sidebar.header("Impostazioni Guadagni")
diretti_annuali = st.sidebar.number_input("Quanti diretti posso fare in un anno", min_value=0, value=24, step=1, format="%d")

# Variabile: percentuale dei diretti che diventerà leader
percentuale_diretti_leader = st.sidebar.number_input("Percentuale dei diretti che diventerà leader (%)", min_value=0, max_value=100, value=10, step=1, format="%d")
percentuale_diretti_leader_str = f"{percentuale_diretti_leader}%"

# Calcolo del numero di diretti che diventeranno leader
numero_diretti_leader = (percentuale_diretti_leader / 100) * diretti_annuali
st.write(f"**Numero di diretti che diventeranno leader**: {numero_diretti_leader:.2f} ({percentuale_diretti_leader_str})")

# Calcolo dei nuovi clienti fatti dai livelli successivi
nuovi_clienti_livello_2_annuali = numero_diretti_leader * diretti_annuali
numero_leader_livello_2 = (percentuale_diretti_leader / 100) * nuovi_clienti_livello_2_annuali
nuovi_clienti_livello_3_annuali = numero_leader_livello_2 * diretti_annuali
numero_leader_livello_3 = (percentuale_diretti_leader / 100) * nuovi_clienti_livello_3_annuali
nuovi_clienti_livello_4_annuali = numero_leader_livello_3 * diretti_annuali

st.subheader("📊 Nuovi Clienti per Livello")
col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Livello 1 (Diretti)", value=f"{diretti_annuali}")
col2.metric(label="Livello 2", value=f"{nuovi_clienti_livello_2_annuali:.2f}")
col3.metric(label="Livello 3", value=f"{nuovi_clienti_livello_3_annuali:.2f}")
col4.metric(label="Livello 4", value=f"{nuovi_clienti_livello_4_annuali:.2f}")

# Guadagni sui vari livelli
st.sidebar.header("Percentuali di Guadagno per Livello")
gain_direct = 12
st.sidebar.write(f"Guadagno sul Diretto: {gain_direct}%")
gain_second = 6
st.sidebar.write(f"Guadagno sul Secondo Livello: {gain_second}%")
gain_third = 4
st.sidebar.write(f"Guadagno sul Terzo Livello: {gain_third}%")
gain_fourth = 2
st.sidebar.write(f"Guadagno sul Quarto Livello: {gain_fourth}%")

# Guadagno del Leader sui diretti in un anno
guadagno_annuale_diretti = (gain_direct / 100) * price * 12 * diretti_annuali

# Guadagno del Leader anno per anno per 19 anni
guadagni_19_anni = []
totale_cumulato_annuale = 0
for anno in range(1, 20):
    if anno <= 10:
        guadagno_annuale = (gain_direct / 100) * price * 12 * diretti_annuali * anno
    else:
        guadagno_annuale = (gain_direct / 100) * price * 12 * diretti_annuali * (20 - anno)
    guadagno_livello_2 = (gain_second / 100) * price * 12 * nuovi_clienti_livello_2_annuali * (anno if anno <= 10 else (20 - anno))
    guadagno_livello_3 = (gain_third / 100) * price * 12 * nuovi_clienti_livello_3_annuali * (anno if anno <= 10 else (20 - anno))
    guadagno_livello_4 = (gain_fourth / 100) * price * 12 * nuovi_clienti_livello_4_annuali * (anno if anno <= 10 else (20 - anno))
    totale_annuale = guadagno_annuale + guadagno_livello_2 + guadagno_livello_3 + guadagno_livello_4
    guadagni_19_anni.append({'Anno': anno, 'Diretto (€)': f"{guadagno_annuale:,.2f}".replace('.', ',').replace(',', '.', 1), 'Livello 2 (€)': f"{guadagno_livello_2:,.2f}".replace('.', ',').replace(',', '.', 1), 'Livello 3 (€)': f"{guadagno_livello_3:,.2f}".replace('.', ',').replace(',', '.', 1), 'Livello 4 (€)': f"{guadagno_livello_4:,.2f}".replace('.', ',').replace(',', '.', 1), 'Totale (€)': f"{totale_annuale:,.2f}".replace('.', ',').replace(',', '.', 1), 'Tot. Mese (€)': f"{totale_annuale / 12:,.2f}".replace('.', ',').replace(',', '.', 1)})
    totale_cumulato_annuale += totale_annuale

# Mostrare i guadagni in una tabella interattiva
guadagni_df = pd.DataFrame(guadagni_19_anni).set_index('Anno')


st.write("### Guadagno del Leader (Anno per Anno)")
st.dataframe(guadagni_df.style.set_properties(**{'font-size': '10pt'}), width=1400)

# Mostrare il numero di clienti in una nuova tabella
clienti_19_anni = []
totale_clienti_annuali_livello_1 = diretti_annuali
totale_clienti_annuali_livello_2 = nuovi_clienti_livello_2_annuali
totale_clienti_annuali_livello_3 = nuovi_clienti_livello_3_annuali
totale_clienti_annuali_livello_4 = nuovi_clienti_livello_4_annuali

for anno in range(1, 20):
    if anno <= 10:
        totale_clienti_annuali_livello_1 = diretti_annuali * anno
        totale_clienti_annuali_livello_2 = nuovi_clienti_livello_2_annuali * anno
        totale_clienti_annuali_livello_3 = nuovi_clienti_livello_3_annuali * anno
        totale_clienti_annuali_livello_4 = nuovi_clienti_livello_4_annuali * anno
    else:
        totale_clienti_annuali_livello_1 = diretti_annuali * (20 - anno)
        totale_clienti_annuali_livello_2 = nuovi_clienti_livello_2_annuali * (20 - anno)
        totale_clienti_annuali_livello_3 = nuovi_clienti_livello_3_annuali * (20 - anno)
        totale_clienti_annuali_livello_4 = nuovi_clienti_livello_4_annuali * (20 - anno)
    clienti_19_anni.append({'Anno': anno, 'Diretto': totale_clienti_annuali_livello_1, 'Livello 2': int(totale_clienti_annuali_livello_2), 'Livello 3': int(totale_clienti_annuali_livello_3), 'Livello 4': int(totale_clienti_annuali_livello_4)})

clienti_df = pd.DataFrame(clienti_19_anni).set_index('Anno')
st.write("### Numero di Clienti (Anno per Anno)")
st.dataframe(clienti_df.style.set_properties(**{'font-size': '10pt'}), width=1400)

# Totale dei guadagni al termine dei 19 anni
st.success(f"Totale guadagni del Leader sui diretti al termine dei 19 anni: €{totale_cumulato_annuale:,.2f}".replace('.', ',').replace(',', '.', 1))

# Calcolo della media annuale al termine dei 19 anni
media_annuale = totale_cumulato_annuale / 19
st.info(f"Media annuale dei guadagni del Leader al termine dei 19 anni: €{media_annuale:,.2f}".replace('.', ',').replace(',', '.', 1))

# Guadagno annuale del Leader sui diretti
st.metric(label="Guadagno annuale del Leader sui diretti", value=f"€{guadagno_annuale_diretti:,.2f}".replace('.', ',').replace(',', '.', 1))

# Descrizione del prodotto venduto
st.subheader("🏠 Prodotto Venduto")
st.write("Il leader vende una vacanza per 10 anni, ossia un appartamento dove trascorrere una vacanza. I pagamenti mensili sono per 10 anni e ogni pagamento dà diritto al leader di percepire il guadagno come descritto, a seconda del livello.")

# Mostrare il prezzo mensile dell'Unità Immobiliare (IVA inclusa)
st.metric(label=f"Prezzo mensile (IVA inclusa) per {ui_type}", value=f"€{price_with_vat:,.2f}".replace('.', ',').replace(',', '.', 1))

# Nota finale
st.markdown("""
---
💬 **Nota**: Puoi modificare i valori nel foglio laterale per vedere come cambiano i risultati delle operazioni.
""")

# Aggiungi un pulsante con il link a Holibuy
st.markdown("""
    <a href="https://sites.google.com/view/holibuy/home-page?authuser=2" target="_blank">
        <button style="background-color: #4CAF50; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer;">Holibuy</button>
    </a>
    """, unsafe_allow_html=True)

