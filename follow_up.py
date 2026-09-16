import streamlit as st

def render_follow_up(trattamento_info, prefix="follow_up"):
    """
    Rende l'interfaccia di follow-up personalizzata in base al regime terapeutico 
    e al contesto clinico precedente (es. post-trapianto con mantenimento, post-terapia TTE, o sorveglianza).
    """
    st.subheader("🔄 Follow-up Clinico & Monitoraggio di Malattia (Linee Guida IMWG)")
    
    # Recuperiamo il contesto dal modulo trattamenti per personalizzare il follow-up
    regime = trattamento_info.get("regime_scelto", "Non specificato")
    mantenimento = trattamento_info.get("mantenimento", "Nessun mantenimento")
    linea = trattamento_info.get("linea_terapia", "")

    st.markdown(f"**Contesto di derivazione:** Regime `{regime}` | Mantenimento: `{mantenimento}`")

    # 1. Scelta della Tempistica del Controllo
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        intervallo_visita = st.selectbox(
            "Intervallo temporale raccomandato per la prossima rivalutazione:",
            [
                "Ogni 4 settimane (durante induzione / terapia attiva o mantenimento intensivo)",
                "Ogni 3 mesi (primo-secondo anno di follow-up / post-ASCT)",
                "Ogni 6 mesi (pazienti in remissione stabile a lungo termine > 2 anni)",
                "Controllo straordinario per sospetta progressione (sintomi CRAB / rialzo FLC)"
            ],
            key=f"{prefix}_intervallo"
        )
    with col_f2:
        stato_clinico_attuale = st.selectbox(
            "Stato di risposta clinica stimato al controllo:",
            [
                "Risposta Completa Stretta (sCR) / Negatività MRD",
                "Risposta Completa (CR)",
                "Risposta Parziale Ottimale (VGPR / PR)",
                "Malattia Stabile (SD)",
                "Progressione di Malattia (PD) / Recidiva clinica o biochimica"
            ],
            key=f"{prefix}_stato_risposta"
        )

    st.markdown("---")
    st.markdown("#### 2. Esami di Laboratorio & Strumentali Prescritti per il Follow-up Specifico")

    # Personalizzazione dei pannelli in base al tipo di trattamento/mantenimento
    if "Mantenimento" in mantenimento or "Lenalidomide" in mantenimento:
        st.info("ℹ️ **Protocollo specifico post-trapianto / mantenimento con Lenalidomide:** Monitoraggio stretto mensile della conta piastrinica e neutrofila (rischio citopenia), controllo renale e monitoraggio della tromboprofilassi.")
        default_lab = ["Emocromo completo con formula", "Creatinina / Azotemia / Elettroliti", "Ratio FLC / Catene leggere libere", "Elettroforesi sieroproteica con IFE siero"]
    elif "Recidivato" in linea or "Salvataggio" in linea:
        st.info("ℹ️ **Protocollo di follow-up per linee avanzate / RRMM:** Richiesto monitoraggio ravvicinato della componente monoclonale, LDH e valutazione clinica per tossicità d'organo o neuropatie.")
        default_lab = ["Emocromo completo con formula", "Creatinina / Azotemia / LDH / Calcemia", "Ratio FLC / Catene leggere libere", "Elettroforesi sieroproteica con IFE siero", "Proteinuria delle 24h"]
    else:
        default_lab = ["Emocromo completo con formula", "Creatinina / Azotemia", "Ratio FLC / Catene leggere libere", "Elettroforesi sieroproteica"]

    esami_richiesti = st.multiselect(
        "Pannello ematochimico e di clonilità prescritto in questo follow-up:",
        [
            "Emocromo completo con formula",
            "Creatinina / Azotemia / Elettroliti (Sodio, Potassio, Calcio)",
            "Lattico-deidrogenasi (LDH) e Beta-2 Microglobulina",
            "Elettroforesi sieroproteica (SPE) con Immunofissazione sierica (IFE)",
            "Dosaggio immunoglobuline quantitative (IgG, IgA, IgM)",
            "Catene leggere libere sieriche (FLC Kappa/Lambda)",
            "Proteinuria delle 24h / Clearance creatinina"
        ],
        default=default_lab,
        key=f"{prefix}_esami_lab"
    )

    # Indagini di riscontro di malattia o ristadiazione a scadenze prefissate
    st.markdown("**Approfondimenti di Ristadiazione / Imaging (se indicati):**")
    col_i1, col_i2 = st.columns(2)
    with col_i1:
        ripetizione_midollo = st.selectbox(
            "Controllo Aspirato / Biopsia Midollare (Valutazione MRD / Risposta):",
            [
                "Non indicato in questo controllo",
                "Indicato per rivalutazione risposta completa (CR) / Conferma sCR",
                "Indicato per studio della Malattia Minima Residua (MRD) multiparametrica / NGS",
                "Indicato per sospetta progressione midollare"
            ],
            key=f"{prefix}_ripetizione_midollo"
        )
    with col_i2:
        ripetizione_imaging = st.selectbox(
            "Controllo Radiologico / Imaging di Ristadiazione:",
            [
                "Non indicato",
                "TC Total-Body Low-Dose di controllo (annuale o a giudizio clinico)",
                "Risonanza Magnetica (RM) per rivalutazione lesioni focali",
                "PET-TC con 18F-FDG per rivalutazione attività metabolica"
            ],
            key=f"{prefix}_ripetizione_imaging"
        )

    # 3. Decisione / Azione in Esito al Follow-up
    st.markdown("#### 3. Decisione Strategica in Uscita dal Follow-up")
    azione_futura = st.selectbox(
        "Condotta clinica pianificata per il prossimo accesso:",
        [
            "Proseguimento della terapia / mantenimento in corso senza variazioni",
            "Modifica / Riduzione dosaggio per tossicità o eventi avversi",
            "Sospensione definitiva del trattamento / Fine programma",
            "Switch terapeutico per ripresa di malattia / Fallimento secondario"
        ],
        key=f"{prefix}_azione"
    )

    note_follow_up = st.text_area(
        "Note cliniche di follow-up e raccomandazioni per il paziente:",
        placeholder="Inserire eventuali prescrizioni di supporto (es. bisfosfonati, emotrasfusioni, fattori di crescita G-CSF)...",
        key=f"{prefix}_note_fu"
    )

    # Dizionario strutturato da passare al cervellone (app.py)
    follow_up_info = {
        "intervallo_visita": intervallo_visita,
        "stato_risposta": stato_clinico_attuale,
        "esami_lab": esami_richiesti,
        "ripetizione_midollo": ripetizione_midollo,
        "ripetizione_imaging": ripetizione_imaging,
        "azione_futura": azione_futura,
        "note": note_follow_up
    }

    return follow_up_info


def formatta_follow_up_per_pdf(follow_up_info):
    """
    Formatta in testo ordinato i dati del follow-up per l'inclusione nel referto clinico/PDF.
    """
    esami_str = ", ".join(follow_up_info.get("esami_lab", []))
    
    testo = (
        f"Programma di Follow-up & Monitoraggio (Linee Guida IMWG):\n"
        f"• Intervallo Visita Raccomandato: {follow_up_info.get('intervallo_visita')}\n"
        f"• Stato di Risposta Clinica: {follow_up_info.get('stato_risposta')}\n"
        f"• Pannello Esami Prescritti: {esami_str}\n"
        f"• Rivalutazione Midollare (MRD): {follow_up_info.get('ripetizione_midollo')}\n"
        f"• Rivalutazione Imaging: {follow_up_info.get('ripetizione_imaging')}\n"
        f"• Condotta Clinica in Uscita: {follow_up_info.get('azione_futura')}\n"
        f"• Note di Gestione Clinica: {follow_up_info.get('note')}"
    )
    return testo
