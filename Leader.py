import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
import numpy as np

st.image("https://raw.githubusercontent.com/Haltosrl/Leader.app/main/.devcontainer/Logo%20Holibuy.png", caption="Holibuy", width=100)

# Titolo dell'app con emoji
st.title("Leader - Opportunità di Guadagno")

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
diretti_annuali = st.sidebar.number_input("Quanti diretti posso fare in un anno", min_value=0, value=24, step=1)

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
gain_card_direct = 70
gain_card_level_2 = 35
gain_card_level_3 = 20
gain_card_level_4 = 10

guadagno_annuale_diretti = (gain_direct / 100) * price * 12 * diretti_annuali + gain_card_direct * diretti_annuali

# Calcolo dei nuovi clienti fatti dai livelli successivi
percentuale_diretti_leader = st.sidebar.number_input("Percentuale dei diretti che diventerà leader (%)", min_value=0, max_value=100, value=10, step=1)
nuovi_clienti_livello_2_annuali = (percentuale_diretti_leader / 100) * diretti_annuali * diretti_annuali
nuovi_clienti_livello_3_annuali = (percentuale_diretti_leader / 100) * nuovi_clienti_livello_2_annuali * diretti_annuali
nuovi_clienti_livello_4_annuali = (percentuale_diretti_leader / 100) * nuovi_clienti_livello_3_annuali * diretti_annuali

# Guadagno del Leader sui livelli della Holibuy Card
gain_card_level_2_annuali = nuovi_clienti_livello_2_annuali * gain_card_level_2
gain_card_level_3_annuali = nuovi_clienti_livello_3_annuali * gain_card_level_3
gain_card_level_4_annuali = nuovi_clienti_livello_4_annuali * gain_card_level_4

# Guadagno del Leader anno per anno per 19 anni
guadagni_19_anni = []
totale_cumulato_annuale = 0
for anno in range(1, 20):
    guadagno_annuale = 0
    guadagno_livello_2 = 0
    guadagno_livello_3 = 0
    guadagno_livello_4 = 0

    # Calcolo dei clienti attivi per ogni livello considerando i 10 anni di durata
    if anno <= 10:
        clienti_attivi_diretti = diretti_annuali * anno
    else:
        clienti_attivi_diretti = diretti_annuali * (20 - anno)

    clienti_attivi_livello_2 = nuovi_clienti_livello_2_annuali * min(anno, 10) if anno <= 10 else nuovi_clienti_livello_2_annuali * (20 - anno)
    clienti_attivi_livello_3 = nuovi_clienti_livello_3_annuali * min(anno, 10) if anno <= 10 else nuovi_clienti_livello_3_annuali * (20 - anno)
    clienti_attivi_livello_4 = nuovi_clienti_livello_4_annuali * min(anno, 10) if anno <= 10 else nuovi_clienti_livello_4_annuali * (20 - anno)

    guadagno_annuale += (gain_direct / 100) * price * 12 * clienti_attivi_diretti + gain_card_direct * clienti_attivi_diretti
    guadagno_livello_2 += (gain_second / 100) * price * 12 * clienti_attivi_livello_2 + gain_card_level_2 * clienti_attivi_livello_2
    guadagno_livello_3 += (gain_third / 100) * price * 12 * clienti_attivi_livello_3 + gain_card_level_3 * clienti_attivi_livello_3
    guadagno_livello_4 += (gain_fourth / 100) * price * 12 * clienti_attivi_livello_4 + gain_card_level_4 * clienti_attivi_livello_4

    totale_annuale = guadagno_annuale + guadagno_livello_2 + guadagno_livello_3 + guadagno_livello_4
    guadagni_19_anni.append({'Anno': anno, 'Diretto (€)': f"{guadagno_annuale:,.2f}".replace('.', ',').replace(',', '.', 1), 'Livello 2 (€)': f"{guadagno_livello_2:,.2f}".replace('.', ',').replace(',', '.', 1), 'Livello 3 (€)': f"{guadagno_livello_3:,.2f}".replace('.', ',').replace(',', '.', 1), 'Livello 4 (€)': f"{guadagno_livello_4:,.2f}".replace('.', ',').replace(',', '.', 1), 'Totale (€)': f"{totale_annuale:,.2f}".replace('.', ',').replace(',', '.', 1), 'Tot. Mese (€)': f"{totale_annuale / 12:,.2f}".replace('.', ',').replace(',', '.', 1)})
    totale_cumulato_annuale += totale_annuale

# Mostrare i guadagni in una tabella interattiva
guadagni_df = pd.DataFrame(guadagni_19_anni).set_index('Anno')

st.write("### Guadagno del Leader (Anno per Anno)")
st.dataframe(guadagni_df.style.set_properties(**{'font-size': '12pt'}), width=1400)

# Mostrare il numero di clienti in una nuova tabella
clienti_19_anni = []
for anno in range(1, 20):
    if anno <= 10:
        totale_clienti_annuali_livello_1 = diretti_annuali * anno
    else:
        totale_clienti_annuali_livello_1 = diretti_annuali * (20 - anno)

    totale_clienti_annuali_livello_2 = nuovi_clienti_livello_2_annuali * min(anno, 10) if anno <= 10 else nuovi_clienti_livello_2_annuali * (20 - anno)
    totale_clienti_annuali_livello_3 = nuovi_clienti_livello_3_annuali * min(anno, 10) if anno <= 10 else nuovi_clienti_livello_3_annuali * (20 - anno)
    totale_clienti_annuali_livello_4 = nuovi_clienti_livello_4_annuali * min(anno, 10) if anno <= 10 else nuovi_clienti_livello_4_annuali * (20 - anno)

    clienti_19_anni.append({'Anno': anno, 'Diretto': totale_clienti_annuali_livello_1, 'Livello 2': int(totale_clienti_annuali_livello_2), 'Livello 3': int(totale_clienti_annuali_livello_3), 'Livello 4': int(totale_clienti_annuali_livello_4)})

clienti_df = pd.DataFrame(clienti_19_anni).set_index('Anno')
st.write("### Numero di Clienti (Anno per Anno)")
st.dataframe(clienti_df.style.set_properties(**{'font-size': '10pt'}), width=1400)

# Totale dei guadagni al termine dei 19 anni
media_annuale = totale_cumulato_annuale / 19

st.sidebar.markdown(f"<div style='background-color: #E6FFE6; padding: 10px; border-radius: 5px;'><b>Totale guadagni del Leader sui diretti al termine dei 19 anni: <span style='font-size: 1.5em;'><b>€{totale_cumulato_annuale:,.2f}</b></span></b></div>".replace('.', ',').replace(',', '.', 1), unsafe_allow_html=True)
st.sidebar.markdown(f"<div style='background-color: #E6FFE6; padding: 10px; border-radius: 5px;'><b>Media annuale dei guadagni del Leader al termine dei 19 anni: <span style='font-size: 1.5em;'><b>€{media_annuale:,.2f}</b></span></b></div>".replace('.', ',').replace(',', '.', 1), unsafe_allow_html=True)

# Guadagno totale del Leader del primo anno
guadagno_primo_anno = guadagni_19_anni[0]['Totale (€)']
st.sidebar.markdown(f"<div style='background-color: #f0ffff; padding: 10px; border-radius: 5px;'><b>Guadagno del Leader Primo Anno: <span style='font-size: 1.5em;'><b>€{guadagno_primo_anno}</b></span></b></div>", unsafe_allow_html=True)
# Guadagno mensile del Leader del primo anno
guadagno_primo_anno_mese = guadagni_19_anni[0]['Tot. Mese (€)']
st.sidebar.markdown(f"<div style='background-color: #f0ffff; padding: 10px; border-radius: 5px;'><b>Guadagno mensile del Leader per 10 anni, se lavorasse solo 1 anno: <span style='font-size: 1.5em;'><b>€{guadagno_primo_anno_mese}</b></span></b></div>", unsafe_allow_html=True)

# Calcolo del Fondo di Accantonamento (FDA)
fda_19_anni = []
percentuale_fda_direct = 16 / 100
percentuale_fda_level_2 = 22 / 100
percentuale_fda_level_3 = 24 / 100
percentuale_fda_level_4 = 26 / 100
fda_contributo = 7

totale_fda_cumulato_decimo_anno = 0
totale_fda_cumulato_ventesimo_anno = 0

for anno in range(1, 20):
    if anno <= 10:
        fda_diretto = diretti_annuali * anno * 12 * fda_contributo * percentuale_fda_direct
    else:
        fda_diretto = diretti_annuali * (20 - anno) * 12 * fda_contributo * percentuale_fda_direct

    fda_level_2 = nuovi_clienti_livello_2_annuali * min(anno, 10) * 12 * fda_contributo * percentuale_fda_level_2 if anno <= 10 else nuovi_clienti_livello_2_annuali * (20 - anno) * 12 * fda_contributo * percentuale_fda_level_2
    fda_level_3 = nuovi_clienti_livello_3_annuali * min(anno, 10) * 12 * fda_contributo * percentuale_fda_level_3 if anno <= 10 else nuovi_clienti_livello_3_annuali * (20 - anno) * 12 * fda_contributo * percentuale_fda_level_3
    fda_level_4 = nuovi_clienti_livello_4_annuali * min(anno, 10) * 12 * fda_contributo * percentuale_fda_level_4 if anno <= 10 else nuovi_clienti_livello_4_annuali * (20 - anno) * 12 * fda_contributo * percentuale_fda_level_4

    totale_fda_annuale = fda_diretto + fda_level_2 + fda_level_3 + fda_level_4
    fda_19_anni.append({'Anno': anno, 'FDA Diretto (€)': f"{fda_diretto:,.2f}".replace('.', ',').replace(',', '.', 1), 'FDA Livello 2 (€)': f"{fda_level_2:,.2f}".replace('.', ',').replace(',', '.', 1), 'FDA Livello 3 (€)': f"{fda_level_3:,.2f}".replace('.', ',').replace(',', '.', 1), 'FDA Livello 4 (€)': f"{fda_level_4:,.2f}".replace('.', ',').replace(',', '.', 1), 'Totale FDA (€)': f"{totale_fda_annuale:,.2f}".replace('.', ',').replace(',', '.', 1)})

    if anno <= 10:
        totale_fda_cumulato_decimo_anno += totale_fda_annuale
    totale_fda_cumulato_ventesimo_anno += totale_fda_annuale

# Mostrare il Fondo di Accantonamento (FDA) in una tabella interattiva
fda_df = pd.DataFrame(fda_19_anni).set_index('Anno')

st.write("### Fondo di Accantonamento (FDA) del Leader (Anno per Anno) Se il Leader si mantiene sopra la media di 18 Nuovi clienti all'anno")
st.dataframe(fda_df.style.set_properties(**{'font-size': '10pt'}), width=1400)

# Totale accantonamento al decimo e al ventesimo anno
st.sidebar.markdown(f"<div style='background-color: #E6FFE6; padding: 10px; border-radius: 5px;'><b>Totale accantonamento al decimo anno: <span style='font-size: 1.5em;'><b>€{totale_fda_cumulato_decimo_anno:,.2f}</b></span></b></div>".replace('.', ',').replace(',', '.', 1), unsafe_allow_html=True)
st.sidebar.markdown(f"<div style='background-color: #E6FFE6; padding: 10px; border-radius: 5px;'><b>Totale accantonamento al ventesimo anno: <span style='font-size: 1.5em;'><b>€{totale_fda_cumulato_ventesimo_anno:,.2f}</b></span></b></div>".replace('.', ',').replace(',', '.', 1), unsafe_allow_html=True)
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
