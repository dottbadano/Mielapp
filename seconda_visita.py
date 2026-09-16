import streamlit as st

def render_seconda_visita(prefix="seconda_visita"):
    """
    Rende l'interfaccia per la gestione della Seconda Visita e degli accertamenti diagnostici 
    ulteriori (imaging, esami di laboratorio avanzati per gammonpatie) prescritti in caso di 
    dubbio o completamento stadiativo nel Mieloma Multiplo.
    """
    st.subheader("🔍 Seconda Visita & Accertamenti Diagnostici Ulteriori")
    st.markdown("Modulo di completamento stadiativo e strumentale per pazienti inviati dalla Prima Visita.")

    # 1. Indagini di Laboratorio Avanzate (Monoclonale & Funzionalità)
    st.markdown("#### 1. Esami Laboratorio per Proteinuria & Componente Monoclonale")
    col_l1, col_l2, col_l3 = st.columns(3)
    with col_l1:
        proteinuria_24h = st.number_input(
            "Proteinuria delle 24h (g/24h):",
            min_value=0.0, max_value=50.0, value=0.15, step=0.05,
            key=f"{prefix}_prot_24h"
        )
    with col_l2:
        catene_kappa = st.number_input(
            "Catene Leggere Libere Kappa - FLC Kappa (mg/L):",
            min_value=0.0, max_value=10000.0, value=10.0, step=0.5,
            key=f"{prefix}_kappa"
        )
    with col_l3:
        catene_lambda = st.number_input(
            "Catene Leggere Libere Lambda - FLC Lambda (mg/L):",
            min_value=0.0, max_value=10000.0, value=12.0, step=0.5,
            key=f"{prefix}_lambda"
        )

    # Calcolo automatico del rapporto FLC kappa/lambda
    rapporto_flc = round(catene_kappa / catene_lambda, 2) if catene_lambda > 0 else 0.0
    st.info(f"📊 Rapporto calcolato FLC Kappa/Lambda: **{rapporto_flc}** (Valore di riferimento normale: 0.26 - 1.65)")

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        immunofissazione_siero = st.selectbox(
            "Immunofissazione Siero (IFE):",
            [
                "Negativa",
                "Componente monoclonale IgG Kappa",
                "Componente monoclonale IgG Lambda",
                "Componente monoclonale IgA Kappa",
                "Componente monoclonale IgA Lambda",
                "Componente monoclonale a sole catene leggere (Bence Jones)",
                "Biclonalità"
            ],
            key=f"{prefix}_ife_siero"
        )
    with col_m2:
        beta2_microglobulina = st.number_input(
            "Beta-2 Microglobulina sierica (mg/L):",
            min_value=0.5, max_value=20.0, value=2.5, step=0.1,
            key=f"{prefix}_b2m"
        )

    # 2. Imaging e Diagnostica per Immagini (CRAB / Lesioni ossee)
    st.markdown("#### 2. Imaging per la Ricerca di Lesioni Osteolitiche / Focali")
    
    imaging_eseguito = st.multiselect(
        "Indagini radiologiche / di imaging prescritte ed eseguite:",
        [
            "TC Total-Body Low-Dose (gold standard scheletrico)",
            "Risonanza Magnetica (RM) colonna/bacino o cranio",
            "PET-TC con 18F-FDG",
            "Radiografia scheletrica convenzionale (Rx scheletro in toto - obsoleto ma valutato)"
        ],
        default=["TC Total-Body Low-Dose (gold standard scheletrico)"],
        key=f"{prefix}_imaging_list"
    )

    lesioni_scheletriche = st.selectbox(
        "Esito dell'imaging sullo scheletro / organi bersaglio:",
        [
            "Nessuna lesione osteolitica o focale evidente",
            "Presenza di lesioni osteolitiche focali (≥ 1 lesione)",
            "Osteopenia diffusa / osteoporosi severa / fratture patologiche",
            "Plasmacitomi extramedollari o fococolai alla RM"
        ],
        key=f"{prefix}_esito_imaging"
    )

    # 3. Criteri CRAB / Decisione in Uscita dalla Seconda Visita
    st.markdown("#### 3. Criteri SLIM-CRAB e Destinazione Clinica in Uscita")
    
    presenza_crab = st.multiselect(
        "Segni o sintomi CRAB / SLIM attivi riscontrati:",
        [
            "Nessun criterio CRAB/SLIM attivo (Possibile Smoldering)",
            "C - Calcemia elevata (> 11 mg/dL)",
            "R - Insufficienza Renale (Creatinina > 2 mg/dL o Clearance < 40 mL/min)",
            "A - Anemia (Emoglobina < 10 g/dL o < 2 g/dL rispetto alla norma)",
            "B - Lesioni ossee (Bone lesions / litiche)",
            "S - Infiltrazione midollare plasmacellulare ≥ 60%",
            "L - Rapporto FLC coinvolte/non coinvolte ≥ 100",
            "M - Più di una lesione focale alla RM"
        ],
        default=["Nessun criterio CRAB/SLIM attivo (Possibile Smoldering)"],
        key=f"{prefix}_crab"
    )

    destinazione_successiva = st.selectbox(
        "Indirizzo del paziente al termine della Seconda Visita:",
        [
            "Invia a Diagnosi Istologica (Puntato/Biopsia Midollare)",
            "Avvia direttamente al Modulo di Trattamento (Mieloma Sintomatico attivo)",
            "Sorveglianza Clinica / Follow-up (Mieloma Asintomatico / Smoldering o MGUS)",
            "Chiusura percorso / Altra patologia"
        ],
        key=f"{prefix}_bivio_2v"
    )

    note_seconda_visita = st.text_area(
        "Conclusioni cliniche e programma della seconda visita:",
        placeholder="Inserire sintesi della valutazione specialistica...",
        key=f"{prefix}_note_2v"
    )

    # Struttura dati da restituire al "cervellone" (app.py)
    seconda_visita_info = {
        "laboratorio_avanzato": {
            "proteinuria_24h": proteinuria_24h,
            "catene_kappa": catene_kappa,
            "catene_lambda": catene_lambda,
            "rapporto_flc": rapporto_flc,
            "immunofissazione_siero": immunofissazione_siera if 'immunofissazione_siera' in locals() else immunofissazione_siero,
            "beta2_microglobulina": beta2_microglobulina
        },
        "imaging": {
            "indagini_eseguite": imaging_eseguito,
            "esito_imaging": lesioni_scheletriche
        },
        "criteri_crab": presenza_crab,
        "destinazione_successiva": destinazione_successiva,
        "note": note_seconda_visita
    }

    return seconda_visita_info


def formatta_seconda_visita_per_pdf(seconda_visita_info):
    """
    Formatta in testo ordinato i dati della seconda visita per l'inclusione nel referto clinico/PDF.
    """
    lab = seconda_visita_info.get("laboratorio_avanzato", {})
    img = seconda_visita_info.get("imaging", {})
    imaging_str = ", ".join(img.get("indagini_eseguite", []))
    crab_str = ", ".join(seconda_visita_info.get("criteri_crab", []))
    
    testo = (
        f"Referto Seconda Visita & Accertamenti Diagnostici:\n"
        f"• Proteinuria 24h: {lab.get('proteinuria_24h')} g/24h | FLC Kappa/Lambda: {lab.get('rapporto_flc')} (K: {lab.get('catene_kappa')} / L: {lab.get('catene_lambda')} mg/L)\n"
        f"• IFE Siero: {lab.get('immunofissazione_siero')} | Beta-2 Microglobulina: {lab.get('beta2_microglobulina')} mg/L\n"
        f"• Imaging Eseguito: {imaging_str}\n"
        f"• Esito Scheletrico/Focale: {img.get('esito_imaging')}\n"
        f"• Criteri SLIM-CRAB Rilevati: {crab_str}\n"
        f"• Destinazione Clinica in Uscita: {seconda_visita_info.get('destinazione_successiva')}\n"
        f"• Note Cliniche: {seconda_visita_info.get('note')}"
    )
    return testo
