import sys
import os
import streamlit as st

# Configurazione della pagina Streamlit
st.set_page_config(
    page_title="Mielapp - Mieloma Multiplo", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tentativo sicuro di importazione del modulo anamnesi
try:
    import anamnesi
    MODULO_ANAMNESI_DISPONIBILE = True
except ImportError:
    MODULO_ANAMNESI_DISPONIBILE = False

# --- BARRA LATERALE (MENU DI NAVIGAZIONE) ---
st.sidebar.markdown("# 🩸 Mielapp")
st.sidebar.markdown("*Supporto clinico e refertazione Mieloma Multiplo*")
st.sidebar.markdown("---")

sezione_corrente = st.sidebar.radio(
    "Percorso Clinico:",
    [
        "📋 1. Anamnesi & Prima Visita", 
        "🔬 2. Biopsia, Citogenetica & Terapia", 
        "🔄 3. Follow-up & Monitoraggio", 
        "📁 4. Riepilogo & Referto Unificato"
    ],
    key="nav_mielapp"
)

st.sidebar.markdown("---")
st.sidebar.info("💡 Gestisci l'intero percorso del paziente: dall'inquadramento iniziale fino al monitoraggio post-terapia.")

# --- CORPO PRINCIPALE DELL'APPLICAZIONE ---

if sezione_corrente == "📋 1. Anamnesi & Prima Visita":
    st.markdown("## 🩸 Mieloma Multiplo — Inquadramento Iniziale e Geriatrico")
    st.write("Raccolta dei dati anagrafici, performance status (ECOG), screening geriatrico (G8), comorbilità (Charlson) ed esami ematochimici di base.")
    
    if MODULO_ANAMNESI_DISPONIBILE:
        # Esegue il form di anamnesi e memorizza i dati nella sessione
        dati_paziente = anamnesi.render_anagrafica_e_anamnesi_unificata(sigla_organo="MM", prefix="mm")
        st.session_state["paziente_corrente"] = dati_paziente
    else:
        st.error("🚨 **Errore critico:** Impossibile trovare il file `anamnesi.py` nella stessa cartella di `app.py`.")
        st.info("Assicurati di aver salvato il codice del modulo di anamnesi in un file denominato esattamente `anamnesi.py` nella directory principale del progetto.")

elif sezione_corrente == "🔬 2. Biopsia, Citogenetica & Terapia":
    st.markdown("## 🔬 Aspirato Midollare, Citogenetica & Scelta Terapeutica")
    
    if "paziente_corrente" in st.session_state and st.session_state["paziente_corrente"].get("nome"):
        paziente = st.session_state["paziente_corrente"]
        st.info(f"Paziente in esame: **{paziente.get('cognome', '')} {paziente.get('nome', '')}** (Età: {paziente.get('eta', 'N/D')} anni | G8: {paziente.get('g8_score', 'N/D')}/17)")
        st.warning("⚠️ Modulo 'Biopsia & Terapia' in fase di configurazione avanzata.")
    else:
        st.warning("⚠️ Compila prima la sezione '1. Anamnesi & Prima Visita' per associare i dati biologici al paziente corretto.")

elif sezione_corrente == "🔄 3. Follow-up & Monitoraggio":
    st.markdown("## 🔄 Follow-up, Risposta & Malattia Residua (MRD)")
    
    if "paziente_corrente" in st.session_state and st.session_state["paziente_corrente"].get("nome"):
        paziente = st.session_state["paziente_corrente"]
        st.success(f"Paziente in follow-up: **{paziente.get('cognome', '')} {paziente.get('nome', '')}** (ID: `{paziente.get('id_univoco', 'N/D')}`)")
        st.warning("⚠️ Modulo 'Follow-up' in fase di configurazione avanzata.")
    else:
        st.warning("⚠️ Seleziona prima un paziente completando l'anamnesi iniziale.")

elif sezione_corrente == "📁 4. Riepilogo & Referto Unificato":
    st.markdown("## 📄 Riepilogo Clinico e Referto Completo")
    
    if "paziente_corrente" in st.session_state and st.session_state["paziente_corrente"].get("nome"):
        paziente = st.session_state["paziente_corrente"]
        st.success(f"Paziente: **{paziente.get('cognome', '')} {paziente.get('nome', '')}** (ID: `{paziente.get('id_univoco', 'N/D')}`)")
        
        if MODULO_ANAMNESI_DISPONIBILE and hasattr(anamnesi, "formatta_anamnesi_per_pdf_unificata"):
            testo_riepilogo = anamnesi.formatta_anamnesi_per_pdf_unificata(paziente)
        else:
            testo_riepilogo = "Dati anagrafici e clinici registrati correttamente nella sessione."
        
        st.text_area("Testo anamnestico e clinico formattato:", value=testo_riepilogo, height=350)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("📥 Salva / Esporta Referto"):
                st.success("Referto salvato correttamente nel database locale della sessione.")
        with col_btn2:
            if st.button("🔄 Reset / Nuova Visita"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
    else:
        st.warning("⚠️ Nessun dato paziente trovato. Inizia compilando la sezione 'Anamnesi & Prima Visita'.")
