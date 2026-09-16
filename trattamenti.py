import streamlit as st

def render_scelta_trattamento(paziente_info, prefix="trattamenti"):
    """
    Gestisce la sezione delle opzioni terapeutiche a linee guida per il Mieloma Multiplo,
    tenendo conto dell'eleggibilità al trapianto, delle linee di terapia e delle evidenze 
    da studi clinici di fase 3 conclusi.
    """
    st.subheader("💊 Programma Terapeutico & Linee Guida (Mieloma Multiplo)")

    # Valutazione automatica preliminare dell'eleggibilità al trapianto basata su età e performance status
    eta = paziente_info.get("eta", 70)
    g8 = paziente_info.get("g8_score", 14.0)
    charlson = paziente_info.get("charlson_score", 2)
    
    # Criterio di massima orientativo clinico
    eleggibile_default = True if eta < 70 and g8 > 14 and charlson < 3 else False

    col_e1, col_e2 = st.columns(2)
    with col_e1:
        eleggibilita_trapianto = st.selectbox(
            "Eleggibilità al Trapianto Autologo (ASCT):",
            [
                "Eleggibile a Trapianto (Fit / Transplant-Eligible)",
                "Non Eleggibile a Trapianto (Unfit / Transplant-Ineligible)",
                "Valutazione in corso / Borderline"
            ],
            index=0 if eleggibile_default else 1,
            key=f"{prefix}_eleggibilita"
        )
    with col_e2:
        linea_terapia = st.selectbox(
            "Linea di Trattamento:",
            [
                "Prima Linea (Newly Diagnosed - NDMM)",
                "Prima Linea di Salvataggio (1° Relapse / Refractory)",
                "Seconde o successive Linee di Salvataggio (≥ 2° Relapse)"
            ],
            key=f"{prefix}_linea"
        )

    st.markdown("---")
    st.markdown("#### Selezione del Regime Farmacologico basato su Linee Guida ed Evidenze di Fase 3")

    regime_scelto = ""
    studio_fase_3 = ""

    # Logica condizionale per proporre i regimi corretti
    if "Prima Linea (Newly Diagnosed - NDMM)" in linea_terapia:
        if "Eleggibile" in eleggibilita_trapianto:
            regime_scelto = st.selectbox(
                "Regime di Induzione/Consolidamento (1° Linea TE):",
                [
                    "Dara-VRd (Daratuzumab + Bortezomib + Lenalidomide + Desametasone)",
                    "VRd (Bortezomib + Lenalidomide + Desametasone)",
                    "Dara-VTd (Daratuzumab + Bortezomib + Talidomide + Desametasone)",
                    "VTd (Bortezomib + Talidomide + Desametasone)"
                ],
                key=f"{prefix}_regime_te_1l"
            )
            # Associazione studio di fase 3
            if "Dara-VRd" in regime_scelto:
                studio_fase_3 = "PERSEUS (Sperimentazione di fase 3: Dara-VRd + mantenimento con Dara-Len vs VRd)"
            elif "VRd" in regime_scelto:
                studio_fase_3 = "SWOG S0777 (Studio di fase 3: VRd vs Rd in pazienti non sottoposti a trapianto immediato)"
            elif "Dara-VTd" in regime_scelto:
                studio_fase_3 = "CASSIOPEIA (Studio di fase 3: Dara-VTd vs VTd nel setting trapiantato)"
            else:
                studio_fase_3 = "GIMEMA MHD-RVd / Altri trial registrativi di induzione"
        else:
            regime_scelto = st.selectbox(
                "Regime di Prima Linea (1° Linea TTE - Non Eleggibile):",
                [
                    "Dara-Rd (Daratuzumab + Lenalidomide + Desametasone)",
                    "VRd-Lite (Bortezomib ridotto + Lenalidomide + Desametasone)",
                    "Dara-VMP (Daratuzumab + Melfalan + Prednisone + Bortezomib)",
                    "Rd (Lenalidomide + Desametasone a dosi aggiustate)"
                ],
                key=f"{prefix}_regime_tte_1l"
            )
            # Associazione studio di fase 3
            if "Dara-Rd" in regime_scelto:
                studio_fase_3 = "MAIA (Studio di fase 3: Dara-Rd vs Rd in pazienti anziani/non eleggibili)"
            elif "Dara-VMP" in regime_scelto:
                studio_fase_3 = "ALCYONE (Studio di fase 3: Dara-VMP vs VMP)"
            elif "VRd-Lite" in regime_scelto:
                studio_fase_3 = "EVOLUTION / Expert clinical trials per fit/frail"
            else:
                studio_fase_3 = "FIRST trial (Rd continuo fino a progressione)"
    else:
        # Linee di ricaduta / refrattarietà (Relapsed / Refractory)
        regime_scelto = st.selectbox(
            "Regime per Mieloma Recidivato/Refrattario (RRMM):",
            [
                "Dara-Kd (Daratuzumab + Carfilzomib + Desametasone)",
                "Isa-Kd (Isatuximab + Carfilzomib + Desametasone)",
                "Kd-d (Carfilzomib + Desametasone + Daratuzumab / Pomalidomide)",
                "Isa-Pd (Isatuximab + Pomalidomide + Desametasone)",
                "Dara-Vd (Daratuzumab + Bortezomib + Desametasone)",
                "Sel-Xd (Selinexor + Bortezomib + Desametasone)",
                "Belantamab mafodotin o Terapie Cellulari / CAR-T / Bispecifici (Linee avanzate)"
            ],
            key=f"{prefix}_regime_rrmm"
        )
        # Associazione studio di fase 3
        if "Dara-Kd" in regime_scelto:
            studio_fase_3 = "CASTOR (per Dara-Vd) / CANDOR (per Dara-Kd - Fase 3)"
        elif "Isa-Kd" in regime_scelto:
            studio_fase_3 = "IKEMA (Studio di fase 3: Isatuximab + Carfilzomib + Desametasone)"
        elif "Isa-Pd" in regime_scelto:
            studio_fase_3 = "ICARIA-MM (Studio di fase 3: Isatuximab + Pomalidomide + Desametasone)"
        elif "Sel-Xd" in regime_scelto:
            studio_fase_3 = "BOSTON (Studio di fase 3: Selinexor + Bortezomib + Desametasone)"
        else:
            studio_fase_3 = "Trial clinici registrativi avanzati / Real World Evidence"

    st.markdown(f"📌 **Evidenza Scientifica / Studio di Fase 3 di Riferimento:** `{studio_fase_3}`")

    # Gestione del Mantenimento
    mantenimento = st.selectbox(
        "Strategia di Mantenimento prevista post-trattamento / post-trapianto:",
        [
            "Nessun mantenimento programmato",
            "Lenalidomide in monoterapia",
            "Daratuzumab (+/- Lenalidomide)",
            "Inibitori del proteasoma (Bortezomib / Ixazomib - specie in alto rischio)"
        ],
        key=f"{prefix}_mantenimento"
    )

    note_terapia = st.text_area(
        "Note cliniche sulla tollerabilità, modifiche di dosaggio o profilassi (es. tromboembolica, infettiva, ossea con bisfosfonati):",
        value="Profilassi con Acido Zoledronico / Denosumab attiva. Profilassi antivirale (Aciclovir) e antitrombotica impostate.",
        key=f"{prefix}_note_terapia"
    )

    # Dizionario strutturato dei trattamenti da passare al "cervellone" (app.py)
    trattamento_info = {
        "eleggibilita_trapianto": eleggibilita_trapianto,
        "linea_terapia": linea_terapia,
        "regime_scelto": regime_scelto,
        "studio_fase_3": studio_fase_3,
        "mantenimento": mantenimiento,
        "note_terapia": note_terapia
    }

    return trattamento_info


def formatta_trattamenti_per_pdf(trattamento_info):
    """
    Formatta in testo ordinato il programma terapeutico e gli studi clinici di riferimento 
    per l'inclusione nel referto clinico/PDF.
    """
    testo = (
        f"Programma Terapeutico & Linee Guida:\n"
        f"• Eleggibilità Trapianto: {trattamento_info.get('eleggibilita_trapianto')}\n"
        f"• Linea di Trattamento: {trattamento_info.get('linea_terapia')}\n"
        f"• Regime Farmacologico Scelto: {trattamento_info.get('regime_scelto')}\n"
        f"• Evidenza / Studio di Fase 3: {trattamento_info.get('studio_fase_3')}\n"
        f"• Strategia di Mantenimento: {trattamento_info.get('mantenimento')}\n"
        f"• Note di Supporto e Gestione: {trattamento_info.get('note_terapia')}"
    )
    return testo
