import streamlit as st
import utils  # Importa il modulo con le funzioni grafiche e di branding

# Configurazione della pagina Streamlit
st.set_page_config(
    page_title="Myel-UP - Decision Support System",
    page_icon="🩸",
    layout="wide"
)

# 1. Renderizza l'intestazione brandizzata in alto a destra (da utils.py)
utils.render_header_brand()

# 2. Inizializzazione dello Session State per i dati globali del paziente
if "paziente_info" not in st.session_state:
    st.session_state["paziente_info"] = {
        "nome": "",
        "cognome": "",
        "id_univoco": "MM-0001",
        "eta": 70,
        "ecog": "0 - Completamente attivo",
        "charlson_score": 2,
        "g8_score": 14.0
    }

# 3. Sidebar per la navigazione tra i moduli del percorso clinico
st.sidebar.title("Navigazione Myel-UP")
st.sidebar.markdown("---")

scelta_modulo = st.sidebar.radio(
    "Seleziona Modulo:",
    [
        "Anagrafica & Anamnesi", 
        "Quadro Istologico / CRAB", 
        "Valutazione Trattamenti (Phase 3)", 
        "Seconda Visita & Rivalutazione", 
        "Follow-up & Report Unificato"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "**Myel-UP DSS**\n\n"
    "Sistema di supporto decisionale basato su linee guida internazionali (IMWG/NCCN) per il Mieloma Multiplo."
)

# 4. Mostra sempre il box del paziente attivo in cima a ogni pagina (se l'anagrafica è compilata)
if st.session_state["paziente_info"]["cognome"] or st.session_state["paziente_info"]["nome"]:
    utils.crea_box_paziente_corrente(st.session_state["paziente_info"])

# 5. Logica di smistamento alle schermate dei moduli
if scelta_modulo == "Anagrafica & Anamnesi":
    st.header("Anagrafica & Anamnesi Paziente")
    st.write("Inserisci i dati anagrafici, le scale di valutazione clinica (ECOG, G8, Charlson) e l'emocromo avanzato.")
    
    # Campi di input rapido salvati direttamente nello state
    col1, col2, col3 = st.columns(3)
    with col1:
        st.session_state["paziente_info"]["nome"] = st.text_input("Nome", value=st.session_state["paziente_info"]["nome"])
    with col2:
        st.session_state["paziente_info"]["cognome"] = st.text_input("Cognome", value=st.session_state["paziente_info"]["cognome"])
    with col3:
        st.session_state["paziente_info"]["id_univoco"] = st.text_input("Codice Univoco / ID", value=st.session_state["paziente_info"]["id_univoco"])

    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        st.session_state["paziente_info"]["ecog"] = st.selectbox(
            "ECOG Performance Status", 
            ["0 - Completamente attivo", "1 - Sintomatico ma ambulante", "2 - Allettato < 50% del giorno", "3 - Allettato > 50% del giorno", "4 - Completamente allettato"],
            index=0
        )
    with col_s2:
        st.session_state["paziente_info"]["charlson_score"] = st.number_input("Charlson Comorbidity Index (CCI)", min_value=0, max_value=15, value=st.session_state["paziente_info"]["charlson_score"])
    with col_s3:
        st.session_state["paziente_info"]["g8_score"] = st.number_input("G8 Screening Geriatrico (max 17)", min_value=0.0, max_value=17.0, value=st.session_state["paziente_info"]["g8_score"])

    st.success("Dati anagrafici e clinici di base aggiornati nella sessione di Myel-UP.")

elif scelta_modulo == "Quadro Istologico / CRAB":
    st.header("Quadro Istologico & Criteri CRAB")
    st.info("Modulo in fase di collegamento strutturato con i file dedicati.")

elif scelta_modulo == "Valutazione Trattamenti (Phase 3)":
    st.header("Valutazione Trattamenti (PERSEUS, MAIA, IKEMA)")
    st.info("Modulo di supporto decisionale basato sui trial clinici randomizzati.")

elif scelta_modulo == "Seconda Visita & Rivalutazione":
    st.header("Seconda Visita & Rivalutazione Clinica")
    st.info("Modulo per il controllo successivo e l'andamento della terapia.")

elif scelta_modulo == "Follow-up & Report Unificato":
    st.header("Follow-up & Esportazione Report Unificato")
    
    # Esempio di utilizzo della funzione di generazione report unificato da utils.py
    testi_moduli_esempio = {
        "Anamnesi": f"Paziente: {st.session_state['paziente_info']['cognome']} {st.session_state['paziente_info']['nome']} (ID: {st.session_state['paziente_info']['id_univoco']})\nECOG: {st.session_state['paziente_info']['ecog']}",
        "Trattamenti": "Nessun trattamento registrato in questa sessione di test."
    }
    
    if st.button("Genera Report Clinico Globale"):
        report_finale = utils.genera_struttura_referto_unificato(testi_moduli_esempio)
        st.text_area("Anteprima Testo Report:", value=report_finale, height=300)
        st.download_button(
            label="Scarica Report in formato di testo / PDF",
            data=report_finale,
            file_name=f"Report_MyelUP_{st.session_state['paziente_info']['id_univoco']}.txt",
            mime="text/plain"
        )
