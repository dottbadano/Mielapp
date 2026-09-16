import streamlit as st
import anamnesi  # Importa il modulo anamnesi.py

st.title("Gestione Clinica Mieloma Multiplo")

# Richiama la funzione corretta definita in anamnesi.py
dati_paziente = anamnesi.render_anagrafica_e_anamnesi_unificata(sigla_organo="MM", prefix="mm")

# Pulsante per la generazione del referto discorsivo medico-legale
if st.button("Genera Referto PDF / Testuale"):
    if dati_paziente["nome"] and dati_paziente["cognome"]:
        referto_generato = anamnesi.formatta_anamnesi_per_pdf_unificata(dati_paziente)
        
        st.success("Referto generato con successo!")
        st.text_area("Anteprima Referto Medico-Legale", referto_generato, height=350)
        
        # Opzionale: Download diretto come file di testo/pdf
        st.download_button(
            label="Scarica Referto (TXT)",
            data=referto_generato,
            file_name=f"Referto_{dati_paziente['cognome']}_{dati_paziente['id_univoco']}.txt",
            mime="text/plain"
        )
    else:
        st.warning("Inserisci almeno Nome e Cognome del paziente per generare il referto.")
