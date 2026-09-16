Hai perfettamente ragione, ti chiedo scusa: nella riga di separazione mi è sfuggito il cancelletto (#). Python ha provato a leggerla come codice anziché come commento, e quel 2A ha fatto scattare l'errore di sintassi.

Ecco il codice corretto al 100%, con tutti i commenti protetti dal cancelletto # e pronto per essere incollato su GitHub senza alcun intoppo:

Python
import streamlit as st

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="2gether - Decision Support System",
    page_icon="🩺",
    layout="wide"
)

# --- LOGO AZIENDALE IN ALTO A DESTRA (2GETHER) ---
logo_html = """
2gether

"""
st.markdown(logo_html, unsafe_allow_html=True)

st.title("Decision Support System - Percorso Clinico Integrato (Mieloma)")

--- INIZIALIZZAZIONE DATABASE DI SESSIONE ---
if "db_pazienti_generale" not in st.session_state:
st.session_state["db_pazienti_generale"] = {}

db_attivo = st.session_state["db_pazienti_generale"]

--- FUNZIONE INTERNA PER LA PRIMA VISITA & ESAMI ---
def render_anagrafica_e_anamnesi_unificata(sigla_organo="MM", prefix="mm_prima"):
st.subheader("1. Anagrafica Paziente")
col1, col2, col3 = st.columns(3)
with col1:
nome = st.text_input("Nome", key=f"{prefix}_nome")
with col2:
cognome = st.text_input("Cognome", key=f"{prefix}_cognome")
with col3:
id_univoco = st.text_input("Codice Univoco / ID", value=f"{sigla_organo}-0001", key=f"{prefix}_id")

col_d1, col_d2 = st.columns(2)
with col_d1:
    data_nascita = st.date_input("Data di Nascita", key=f"{prefix}_data_nascita")
with col_d2:
    eta = st.number_input("Età", min_value=18, max_value=120, value=70, key=f"{prefix}_eta")

st.markdown("---")
st.subheader("2. Valutazione Clinica & Performance Status")

col_sc1, col_sc2, col_sc3 = st.columns(3)
with col_sc1:
    ecog = st.selectbox("ECOG Performance Status", ["0 - Completamente attivo", "1 - Sintomatico ma ambulante", "2 - Allettato < 50% del giorno", "3 - Allettato > 50% del giorno", "4 - Completamente allettato"], key=f"{prefix}_ecog")
with col_sc2:
    charlson_score = st.number_input("Charlson Comorbidity Index (CCI)", min_value=0, max_value=15, value=2, key=f"{prefix}_charlson")
with col_sc3:
    g8_score = st.number_input("G8 Screening Geriatrico (max 17)", min_value=0.0, max_value=17.0, value=14.0, step=0.5, key=f"{prefix}_g8")

aspettativa_maggiore_10 = True
if eta > 80 or charlson_score >= 3 or g8_score <= 14:
    aspettativa_maggiore_10 = False

st.markdown("---")
st.subheader("3. Esami Ematochimici ed Emocromo di Ingresso")

col_w1, col_w2, col_w3 = st.columns(3)
with col_w1:
    wbc_tot = st.number_input("WBC Totali (x10^3/uL)", min_value=0.0, max_value=100.0, value=7.0, step=0.1, key=f"{prefix}_wbc")
    neutrofili_ass = st.number_input("Neutrofili Assoluti (x10^3/uL)", min_value=0.0, max_value=50.0, value=4.2, key=f"{prefix}_neu_a")
with col_w2:
    linfociti_ass = st.number_input("Linfociti Assoluti (x10^3/uL)", min_value=0.0, max_value=50.0, value=2.1, key=f"{prefix}_lin_a")
    monociti_ass = st.number_input("Monociti Assoluti (x10^3/uL)", min_value=0.0, max_value=20.0, value=0.4, key=f"{prefix}_mon_a")
with col_w3:
    eosinofili_ass = st.number_input("Eosinofili Assoluti (x10^3/uL)", min_value=0.0, max_value=10.0, value=0.1, key=f"{prefix}_eos_a")
    basofili_ass = st.number_input("Basofili Assoluti (x10^3/uL)", min_value=0.0, max_value=5.0, value=0.02, key=f"{prefix}_bas_a")

anomalie_leucocitarie = st.text_input("Segnalazioni morfologiche / Cellule immature / Blasti:", value="Assenti", key=f"{prefix}_anomalie_wbc")

col_r1, col_r2, col_r3 = st.columns(3)
with col_r1:
    emoglobina = st.number_input("Emoglobina - Hb (g/dL)", min_value=3.0, max_value=20.0, value=13.5, step=0.1, key=f"{prefix}_hb")
    ematocrito = st.number_input("Ematocrito - Hct (%)", min_value=10.0, max_value=60.0, value=40.0, key=f"{prefix}_hct")
with col_r2:
    mcv = st.number_input("MCV (fL)", min_value=50.0, max_value=130.0, value=88.0, key=f"{prefix}_mcv")
    rdw = st.number_input("RDW (%)", min_value=5.0, max_value=30.0, value=13.0, key=f"{prefix}_rdw")
with col_r3:
    piastrine = st.number_input("Piastrine - PLT (x10^3/uL)", min_value=10, max_value=1000, value=250, key=f"{prefix}_plt")
    reticolociti = st.number_input("Reticolociti (%)", min_value=0.0, max_value=20.0, value=1.0, key=f"{prefix}_ret")

col_e1, col_e2, col_e3 = st.columns(3)
with col_e1:
    creatinina = st.number_input("Creatinina (mg/dL)", min_value=0.1, max_value=15.0, value=1.0, step=0.1, key=f"{prefix}_creat")
with col_e2:
    azotemia = st.number_input("Azotemia / BUN (mg/dL)", min_value=5.0, max_value=200.0, value=35.0, key=f"{prefix}_azotemia")
with col_e3:
    ldh = st.number_input("LDH (U/L)", min_value=50.0, max_value=2000.0, value=220.0, key=f"{prefix}_ldh")

paziente_info = {
    "nome": nome,
    "cognome": cognome,
    "id_univoco": id_univoco,
    "data_nascita": str(data_nascita),
    "eta": eta,
    "ecog": ecog,
    "charlson_score": charlson_score,
    "g8_score": g8_score,
    "aspettativa_vita_maggiore_10_anni": aspettativa_maggiore_10,
    "emocromo": {
        "wbc_tot": wbc_tot, "neutrofili_ass": neutrofili_ass, "linfociti_ass": linfociti_ass,
        "monociti_ass": monociti_ass, "eosinofili_ass": eosinofili_ass, "basofili_ass": basofili_ass,
        "anomalie_wbc": anomalie_leucocitarie, "hb": emoglobina, "hct": ematocrito,
        "mcv": mcv, "rdw": rdw, "plt": piastrine, "reticolociti": reticolociti
    },
    "ematochimici": {"creatinina": creatinina, "azotemia": azotemia, "ldh": ldh}
}
return paziente_info
def formatta_anamnesi_per_pdf_unificata(paziente_info):
emo = paziente_info.get("emocromo", {})
emat = paziente_info.get("ematochimici", {})
return (
f"Valutazione Clinica & Performance Status:\n"
f"• ECOG: {paziente_info.get('ecog')}\n"
f"• Charlson Comorbidity Index: {paziente_info.get('charlson_score')}\n"
f"• Screening G8: {paziente_info.get('g8_score')}/17\n\n"
f"Emocromo & Esami:\n"
f"• Hb: {emo.get('hb')} g/dL | PLT: {emo.get('plt')} x10^3/uL | WBC: {emo.get('wbc_tot')} x10^3/uL\n"
f"• Creatinina: {emat.get('creatinina')} mg/dL | LDH: {emat.get('ldh')} U/L"
)

--- MENU LATERALE: GESTIONE DEL TRAFFICO CLINICO ---
fase_corrente = st.sidebar.radio(
"Seleziona Fase del Percorso:",
[
"1. Prima Visita & Bivio Decisionale",
"2A. Seconda Visita (Accertamenti Ulteriori)",
"2B. Diagnosi Istologica / Esito Midollo",
"3. Protocollo Terapia & Visite Iterative",
"4. Follow-up / Exitus"
]
)

st.sidebar.markdown("---")
st.sidebar.info("Usa l'ID univoco per mantenere la continuità clinica del paziente lungo il flusso.")

--- FASE 1: PRIMA VISITA & BIVIO ---
if fase_corrente == "1. Prima Visita & Bivio Decisionale":
st.subheader("Fase 1: Prima Visita & Inquadramento Iniziale")

paziente_info = render_anagrafica_e_anamnesi_unificata(sigla_organo="MM", prefix="mm_prima")
id_paziente = str(paziente_info["id_univoco"]).strip().upper()

st.markdown("---")
st.subheader("Bivio Decisionale (Destinazione clinica in uscita):")
scelta_bivio = st.selectbox(
    "Seleziona l'esito della valutazione clinica iniziale:",
    [
        "Seleziona...",
        "1. Esclusione patologia (Paziente fuori dall'app / Chiusura percorso)",
        "2. Necessari accertamenti ulteriori (Invia a Seconda Visita)",
        "3. Indicazione a puntato midollare / biopsia (Invia a Diagnosi Istologica)"
    ]
)

if st.button("Registra Prima Visita e Smista Paziente", type="primary"):
    if paziente_info["nome"] and paziente_info["cognome"] and id_paziente and scelta_bivio != "Seleziona...":
        stato_iniziale = scelta_bivio.split(". ")[1]
        db_attivo[id_paziente] = {
            "anagrafica": paziente_info,
            "stato_attuale": stato_iniziale,
            "storico_eventi": [{
                "fase": "Prima Visita",
                "esito_bivio": stato_iniziale,
                "dettagli": formatta_anamnesi_per_pdf_unificata(paziente_info)
            }]
        }
        st.success(f"Paziente registrato! ID: **{id_paziente}** | Indirizzato a: **{stato_iniziale}**")
    else:
        st.warning("Compila Nome, Cognome, ID e seleziona una destinazione valida nel bivio.")
--- FASE 2A: SECONDA VISITA (ACCERTAMENTI ULTERIORI) ---
elif fase_corrente == "2A. Seconda Visita (Accertamenti Ulteriori)":
st.subheader("Fase 2A: Rivalutazione Post-Accertamenti")
id_search = st.text_input("Inserisci ID Univoco Paziente:").strip().upper()
if id_search:
if id_search in db_attivo:
paz = db_attivo[id_search]
st.success(f"Paziente Trovato: {paz['anagrafica']['cognome']} {paz['anagrafica']['nome']}")

        decisione_post_accertamenti = st.selectbox(
            "Esito rivalutazione:",
            [
                "Sospetto decaduto -> Chiusura percorso",
                "Conferma sospetto -> Invia a Puntato Midollare / Biopsia"
            ]
        )
        note_2a = st.text_area("Note cliniche della seconda visita:")
        
        if st.button("Aggiorna Stato Paziente"):
            paz["storico_eventi"].append({"fase": "Seconda Visita", "dettagli": note_2a, "esito": decisione_post_accertamenti})
            paz["stato_attuale"] = decisione_post_accertamenti
            st.success("Stato aggiornato con successo!")
    else:
        st.error("Paziente non trovato.")
--- FASE 2B: DIAGNOSI ISTOLOGICA / ESITO MIDOLLO ---
elif fase_corrente == "2B. Diagnosi Istologica / Esito Midollo":
st.subheader("Fase 2B: Valutazione Aspirato / Biopsia Midollare")
id_search = st.text_input("Inserisci ID Univoco Paziente per Esito Midollo:").strip().upper()
if id_search:
if id_search in db_attivo:
paz = db_attivo[id_search]
st.success(f"Paziente Trovato: {paz['anagrafica']['cognome']} {paz['anagrafica']['nome']}")

        referto_midollo = st.text_area("Referto Istologico / Citologico midollare:")
        necessita_terapia = st.radio("Il quadro richiede l'avvio di un trattamento terapeutico?", ["Sì, avvia a Protocollo Terapia", "No, sorveglianza / solo supporto"])
        
        if st.button("Salva Esito Midollo"):
            paz["storico_eventi"].append({"fase": "Diagnosi Istologica / Midollo", "dettagli": referto_midollo, "scelta": necessita_terapia})
            paz["stato_attuale"] = "In Trattamento" if "Sì" in necessita_terapia else "Sorveglianza Clinica"
            st.success("Esito registrato. Il paziente è instradato correttamente.")
    else:
        st.error("Paziente non trovato.")
--- FASE 3: PROTOCOLLO TERAPIA & VISITE ITERATIVE ---
elif fase_corrente == "3. Protocollo Terapia & Visite Iterative":
st.subheader("Fase 3: Gestione Terapie e Visite di Controllo Iterative")
id_search = st.text_input("Inserisci ID Univoco Paziente in Trattamento:").strip().upper()
if id_search:
if id_search in db_attivo:
paz = db_attivo[id_search]
st.info(f"Paziente: {paz['anagrafica']['cognome']} {paz['anagrafica']['nome']} | Età: {paz['anagrafica']['eta']} | CCI: {paz['anagrafica']['charlson_score']}")

        st.markdown("### Selezione Terapia (Ponderata su Età e Comorbidità)")
        linea_terapia = st.selectbox("Protocollo Terapeutico Adeguato:", ["Terapia Intensiva + Autotrapianto (Idoneo)", "Terapia a Minor Intensità / Orale (Non Idoneo / Fragile)", "Terapia di Supporto Palliata"])
        dettagli_visita_terapia = st.text_area("Note cliniche della nuova visita di controllo / ciclo:")
        
        prossimo_passo = st.radio("Esito / Direzione post-visita:", ["Prosegui in terapia (Apri nuova visita successiva)", "Passa a Follow-up", "Registra Exitus"])
        
        if st.button("Registra Nuova Visita / Evento"):
            paz["storico_eventi"].append({"fase": f"Visita di Controllo / Terapia ({linea_terapia})", "dettagli": dettagli_visita_terapia})
            paz["stato_attuale"] = prossimo_passo
            st.success("Visita registrata e aggiunta allo storico cronologico del paziente.")
    else:
        st.error("Paziente non trovato.")
--- FASE 4: FOLLOW-UP / EXITUS ---
elif fase_corrente == "4. Follow-up / Exitus":
st.subheader("Fase 4: Gestione Follow-up e Chiusura Percorso")
id_search = st.text_input("Inserisci ID Univoco Paziente per Follow-up/Exitus:").strip().upper()
if id_search:
if id_search in db_attivo:
paz = db_attivo[id_search]
st.success(f"Paziente: {paz['anagrafica']['cognome']} {paz['anagrafica']['nome']}")

        stato_finale_fu = st.selectbox("Stato clinico di controllo:", ["In Follow-up Attivo", "Registra Exitus (Decesso)"])
        note_fu = st.text_area("Note cliniche del controllo:")
        
        if st.button("Aggiorna Stato Finale"):
            paz["storico_eventi"].append({"fase": "Follow-up / Chiusura", "stato": stato_finale_fu, "dettagli": note_fu})
            paz["stato_attuale"] = stato_finale_fu
            st.success(f"Stato aggiornato a: **{stato_finale_fu}**")
            
        with st.expander("Visualizza Cronologia Completa ed Eventi del Paziente"):
            for ev in paz["storico_eventi"]:
                st.markdown(f"**Fase:** {ev.get('fase')}")
                st.text(ev.get('dettagli'))
                st.markdown("---")
    else:
        st.error("Paziente non trovato.")
