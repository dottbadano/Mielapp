import streamlit as st

def render_anagrafica_e_anamnesi_unificata(sigla_organo="MM", prefix="mm"):
    """
    Rende l'interfaccia unificata di anagrafica, anamnesi, scale geriatriche/cliniche (G8, Charlson, ECOG)
    e un emocromo avanzato con formula completa ed esami ematochimici di base.
    """
    st.subheader("Anagrafica Paziente")
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
    st.subheader("Valutazione Clinica & Performance Status")
    
    col_sc1, col_sc2, col_sc3 = st.columns(3)
    with col_sc1:
        ecog = st.selectbox("ECOG Performance Status", ["0 - Completamente attivo", "1 - Sintomatico ma ambulante", "2 - Allettato < 50% del giorno", "3 - Allettato > 50% del giorno", "4 - Completamente allettato"], key=f"{prefix}_ecog")
    with col_sc2:
        charlson_score = st.number_input("Charlson Comorbidity Index (CCI)", min_value=0, max_value=15, value=2, key=f"{prefix}_charlson")
    with col_sc3:
        g8_score = st.number_input("G8 Screening Geriatrico (max 17)", min_value=0.0, max_value=17.0, value=14.0, step=0.5, key=f"{prefix}_g8")

    aspettativa_vita_maggiore_10_anni = True
    if eta > 80 or charlson_score >= 3 or g8_score <= 14:
        aspettativa_vita_maggiore_10_anni = False

    st.markdown("---")
    st.subheader("🩸 Emocromo Avanzato & Esami Ematochimici")
    
    st.markdown("#### 1. Serie Bianca (Leucociti e Formula Completa - Valori Assoluti e %)")
    col_w1, col_w2, col_w3 = st.columns(3)
    with col_w1:
        wbc_tot = st.number_input("WBC Totali (x10^3/uL)", min_value=0.0, max_value=100.0, value=7.0, step=0.1, key=f"{prefix}_wbc")
        neutrofili_perc = st.number_input("Neutrofili (%)", min_value=0.0, max_value=100.0, value=60.0, key=f"{prefix}_neu_p")
        neutrofili_ass = st.number_input("Neutrofili Assoluti (x10^3/uL)", min_value=0.0, max_value=50.0, value=4.2, key=f"{prefix}_neu_a")
    with col_w2:
        linfociti_perc = st.number_input("Linfociti (%)", min_value=0.0, max_value=100.0, value=30.0, key=f"{prefix}_lin_p")
        linfociti_ass = st.number_input("Linfociti Assoluti (x10^3/uL)", min_value=0.0, max_value=50.0, value=2.1, key=f"{prefix}_lin_a")
        monociti_perc = st.number_input("Monociti (%)", min_value=0.0, max_value=100.0, value=6.0, key=f"{prefix}_mon_p")
    with col_w3:
        monociti_ass = st.number_input("Monociti Assoluti (x10^3/uL)", min_value=0.0, max_value=20.0, value=0.4, key=f"{prefix}_mon_a")
        eosinofili_ass = st.number_input("Eosinofili Assoluti (x10^3/uL)", min_value=0.0, max_value=10.0, value=0.1, key=f"{prefix}_eos_a")
        basofili_ass = st.number_input("Basofili Assoluti (x10^3/uL)", min_value=0.0, max_value=5.0, value=0.02, key=f"{prefix}_bas_a")

    # Menu a tendina standardizzato per le alterazioni morfologiche
    anomalie_leucocitarie = st.selectbox(
        "Segnalazioni morfologiche / Cellule immature / Blasti:",
        [
            "Assenti",
            "Presenza di Blasti",
            "Cellule immature / Metamielociti / Mielociti",
            "Linfociti atipici / reattivi",
            "Anisopoichilocitosi marcata",
            "Presenza di eritroblasti circolanti",
            "Altre alterazioni morfologiche"
        ],
        key=f"{prefix}_anomalie_wbc"
    )

    st.markdown("#### 2. Serie Rossa & Piastrinica")
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

    st.markdown("#### 3. Funzionalità Renale ed Indici Sistemici")
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
        "aspettativa_vita_maggiore_10_anni": aspettativa_vita_maggiore_10_anni,
        "emocromo": {
            "wbc_tot": wbc_tot,
            "neutrofili_ass": neutrofili_ass,
            "linfociti_ass": linfociti_ass,
            "monociti_ass": monociti_ass,
            "eosinofili_ass": eosinofili_ass,
            "basofili_ass": basofili_ass,
            "anomalie_wbc": anomalie_leucocitarie,
            "hb": emoglobina,
            "hct": ematocrito,
            "mcv": mcv,
            "rdw": rdw,
            "plt": piastrine,
            "reticolociti": reticolociti
        },
        "ematochimici": {
            "creatinina": creatinina,
            "azotemia": azotemia,
            "ldh": ldh
        }
    }

    return paziente_info

def formatta_anamnesi_per_pdf_unificata(paziente_info):
    """
    Formatta in testo ordinato i dati dell'anamnesi e dell'emocromo avanzato per l'inclusione nel referto PDF.
    """
    emo = paziente_info.get("emocromo", {})
    emat = paziente_info.get("ematochimici", {})
    
    testo = (
        f"Valutazione Clinica & Performance Status:\n"
        f"• ECOG: {paziente_info.get('ecog')}\n"
        f"• Charlson Comorbidity Index: {paziente_info.get('charlson_score')}\n"
        f"• Screening G8: {paziente_info.get('g8_score')}/17\n\n"
        f"Emocromo Avanzato:\n"
        f"• WBC Totali: {emo.get('wbc_tot')} x10^3/uL\n"
        f"• Formula Assoluta -> Neutrofili: {emo.get('neutrofili_ass')} | Linfociti: {emo.get('linfociti_ass')} | Monociti: {emo.get('monociti_ass')} | Eosinofili: {emo.get('eosinofili_ass')} | Basofili: {emo.get('basofili_ass')} x10^3/uL\n"
        f"• Segnalazioni morfologiche / Blasti: {emo.get('anomalie_wbc')}\n"
        f"• Emoglobina (Hb): {emo.get('hb')} g/dL | Ematocrito: {emo.get('hct')}% | MCV: {emo.get('mcv')} fL | RDW: {emo.get('rdw')}%\n"
        f"• Piastrine (PLT): {emo.get('plt')} x10^3/uL | Reticolociti: {emo.get('reticolociti')}%\n\n"
        f"Esami Ematochimici di Supporto:\n"
        f"• Creatinina: {emat.get('creatinina')} mg/dL | Azotemia: {emat.get('azotemia')} mg/dL | LDH: {emat.get('ldh')} U/L"
    )
    return testo
