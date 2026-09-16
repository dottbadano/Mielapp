import streamlit as st
import utils
import anamnesi  # Importa il modulo di anamnesi che abbiamo appena analizzato

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

# 4. Mostra sempre il box del paziente attivo in cima a ogni pagina se i campi anagrafici essenziali sono attivi
if st.session_state["paziente_info"].get("cognome") or st.session_state["paziente_info"].get("nome"):
    utils.crea_box_paziente_corrente(st.session_state["paziente_info"])

# 5. Logica di smistamento coordinata con i moduli esterni
if scelta_modulo == "Anagrafica & Anamnesi":
    st.header("Anagrafica & Anamnesi Paziente")
    st.write("Compila i dati clinici, anagrafici e l'emocromo avanzato. I dati vengono salvati in automatico nella sessione.")
    
    # Richiama la funzione pulita dal file anamnesi.py e aggiorna lo state globale
    paziente_aggiornato = anamnesi.render_anagrafica_e_anamnesi_unificata(sigla_organo="MM", prefix="mm")
    st.session_state["paziente_info"] = paziente_aggiornato

elif scelta_modulo == "Quadro Istologico / CRAB":
    st.header("Quadro Istologico & Criteri CRAB")
    st.info("Modulo in fase di collegamento strutturato.")

elif scelta_modulo == "Valutazione Trattamenti (Phase 3)":
    st.header("Valutazione Trattamenti (PERSEUS, MAIA, IKEMA)")
    st.info("Modulo di supporto decisionale basato sui trial clinici randomizzati.")

elif scelta_modulo == "Seconda Visita & Rivalutazione":
    st.header("Seconda Visita & Rivalutazione Clinica")
    st.info("Modulo per il controllo successivo e l'andamento della terapia.")

elif scelta_modulo == "Follow-up & Report Unificato":
    st.header("Follow-up & Esportazione Report Unificato")
    st.write("Verifica il riepilogo globale e genera il referto clinico stampabile.")
    
    # Genera il testo dell'anamnesi usando la funzione dedicata del modulo anamnesi
    testo_anamnesi_report = anamnesi.formatta_anamnesi_per_pdf_unificata(st.session_state["paziente_info"])
    
    # Dizionario che raccoglie i testi dai vari moduli per l'export unificato
    moduli_per_report = {
        "Anamnesi & Clinica": testo_anamnesi_report,
        "Trattamenti": "Nessun trattamento registrato in questa sessione."
    }
    
    if st.button("Genera Report Clinico Globale"):
        report_finale = utils.genera_struttura_referto_unificato(moduli_per_report)
        st.text_area("Anteprima Testo Report:", value=report_finale, height=350)
        st.download_button(
            label="Scarica Report Clinico (Formato Testo/PDF)",
            data=report_finale,
            file_name=f"Report_MyelUP_{st.session_state['paziente_info'].get('id_univoco', 'MM')}.txt",
            mime="text/plain"
        )
