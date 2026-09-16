import streamlit as st
import utils
import anamnesi
import seconda_visita
import istologico
import trattamenti

# Configurazione della pagina Streamlit
st.set_page_config(
    page_title="Myel-UP - Decision Support System",
    page_icon="🩸",
    layout="wide"
)

# 1. Renderizza l'intestazione brandizzata in alto a destra (da utils.py)
utils.render_header_brand()

# 2. Inizializzazione dello Session State per i dati globali dei vari moduli
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

if "seconda_visita_info" not in st.session_state:
    st.session_state["seconda_visita_info"] = {}

if "istologico_info" not in st.session_state:
    st.session_state["istologico_info"] = {}

if "trattamento_info" not in st.session_state:
    st.session_state["trattamento_info"] = {}

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
    
    paziente_aggiornato = anamnesi.render_anagrafica_e_anamnesi_unificata(sigla_organo="MM", prefix="mm")
    st.session_state["paziente_info"] = paziente_aggiornato

elif scelta_modulo == "Quadro Istologico / CRAB":
    st.header("Quadro Istologico & Criteri CRAB")
    st.write("Registrazione del referto bioptico/aspirato midollare e assetto citogenetico FISH.")
    
    st.session_state["istologico_info"] = istologico.render_esame_istologico(prefix="istologico")

elif scelta_modulo == "Valutazione Trattamenti (Phase 3)":
    st.header("Valutazione Trattamenti (PERSEUS, MAIA, IKEMA, CANDOR)")
    st.write("Supporto decisionale basato su trial clinici randomizzati e linee guida IMWG/NCCN.")
    
    st.session_state["trattamento_info"] = trattamenti.render_scelta_trattamento(
        st.session_state["paziente_info"], 
        prefix="trattamenti"
    )

elif scelta_modulo == "Seconda Visita & Rivalutazione":
    st.header("Seconda Visita & Accertamenti Diagnostici")
    st.write("Gestione degli esami di laboratorio avanzati, imaging e criteri SLIM-CRAB.")
    
    st.session_state["seconda_visita_info"] = seconda_visita.render_seconda_visita(prefix="seconda_visita")

elif scelta_modulo == "Follow-up & Report Unificato":
    st.header("Follow-up & Esportazione Report Unificato")
    st.write("Verifica il riepilogo globale dai moduli attivi e genera il referto clinico stampabile.")
    
    # Recupero in modo sicuro dei testi formattati dai singoli moduli
    testo_anamnesi_report = anamnesi.formatta_anamnesi_per_pdf_unificata(st.session_state["paziente_info"])
    
    testo_seconda_visita_report = seconda_visita.formatta_seconda_visita_per_pdf(st.session_state["seconda_visita_info"]) if st.session_state.get("seconda_visita_info") else "Seconda visita non registrata."
    
    testo_istologico_report = istologico.formatta_istologico_per_pdf(st.session_state["istologico_info"]) if st.session_state.get("istologico_info") else "Quadro istologico non registrato."
    
    testo_trattamenti_report = trattamenti.formatta_trattamenti_per_pdf(st.session_state["trattamento_info"]) if st.session_state.get("trattamento_info") else "Trattamento non registrato."

    # Dizionario globale che unisce tutti i moduli per l'export
    moduli_per_report = {
        "Anamnesi & Clinica": testo_anamnesi_report,
        "Seconda Visita & Diagnostica": testo_seconda_visita_report,
        "Quadro Istologico & FISH": testo_istologico_report,
        "Programma Terapeutico & Fase 3": testo_trattamenti_report
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
