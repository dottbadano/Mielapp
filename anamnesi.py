from datetime import datetime
import random
import string
import re
import streamlit as st

try:
    from pypdf import PdfReader
    PYPDF_DISPONIBILE = True
except ImportError:
    PYPDF_DISPONIBILE = False

def genera_codice_univoco_organo(nome, cognome, organo_lettera="MM"):
    n = nome.strip()
    c = cognome.strip()
    if len(n) < 2 or len(c) < 2:
        return ""
    return f"{n[0].upper()}{c[1].upper()}{c[0].upper()}{n[1].upper()}-{''.join(random.choices(string.digits, k=6))}-{organo_lettera.upper()[:2]}"

def stima_aspettativa_di_vita(eta, charlson_score, g8_score, ecog_str):
    bonus_fitness = 0
    if "0" in ecog_str or "1" in ecog_str:
        bonus_fitness += 2
    if g8_score >= 14:
        bonus_fitness += 2
    elif g8_score >= 11:
        bonus_fitness += 1

    charlson_ponderato = max(0, charlson_score - bonus_fitness)
    aspettativa_maggiore_di_10 = True
    if eta >= 80 and charlson_ponderato >= 5:
        aspettativa_maggiore_di_10 = False
    elif charlson_ponderato >= 6 and g8_score < 11:
        aspettativa_maggiore_di_10 = False

    return aspettativa_maggiore_di_10, charlson_ponderato

def render_anagrafica_e_anamnesi_unificata(sigla_organo="MM", prefix="mm"):
    st.markdown("### 📋 Anagrafica & Identificazione")

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        cognome = st.text_input("Cognome Paziente", key=f"input_cognome_{prefix}")
    with col_b:
        nome = st.text_input("Nome Paziente", key=f"input_nome_{prefix}")

    id_key = f"input_id_{prefix}"
    if id_key not in st.session_state:
        st.session_state[id_key] = ""

    nuovo_id = genera_codice_univoco_organo(nome, cognome, sigla_organo)
    if nuovo_id and not st.session_state[id_key]:
        st.session_state[id_key] = nuovo_id

    with col_c:
        codice_paziente = st.text_input("Codice Univoco / ID (Richiamabile)", key=id_key)

    st.markdown("**Data di Nascita (GG / MM / AAAA)**")
    col_d1, col_d2, col_d3 = st.columns(3)
    with col_d1:
        giorno_n = st.number_input("Giorno", min_value=1, max_value=31, value=1, step=1, key=f"input_giorno_{prefix}")
    with col_d2:
        mese_n = st.number_input("Mese", min_value=1, max_value=12, value=1, step=1, key=f"input_mese_{prefix}")
    with col_d3:
        anno_n = st.number_input("Anno", min_value=1900, max_value=2026, value=1960, step=1, key=f"input_anno_{prefix}")

    try:
        data_nascita = datetime(int(anno_n), int(mese_n), int(giorno_n)).date()
    except ValueError:
        data_nascita = datetime(1960, 1, 1).date()
        st.warning("Data de nascita non valida. Impostata temporaneamente a 01/01/1960.")

    oggi = datetime.today().date()
    eta = oggi.year - data_nascita.year - ((oggi.month, oggi.day) < (data_nascita.month, data_nascita.day))

    st.info(f"📊 **Età Anagrafica:** {eta} anni")

    # --- CAREGIVER E SUPPORTO SPOSTATO ALL'INIZIO ---
    st.markdown("---")
    st.markdown("### 🤝 Rete di Supporto e Caregiver")
    caregiver_supporto = st.selectbox(
        "Contesto socio-familiare e supporto:",
        ["Non valutato", "Autonomo (Senza caregiver)", "Caregiver familiare presente", "Assistenza domiciliare strutturata"],
        key=f"{prefix}_caregiver"
    )

    st.markdown("---")
    st.markdown("### 🏃‍♂️ Performance Status & Parametri Antropometrici")

    col_ant1, col_ant2 = st.columns(2)
    with col_ant1:
        peso = st.number_input("Peso (kg)", min_value=30.0, max_value=250.0, value=75.0, step=0.5, key=f"input_peso_{prefix}")
    with col_ant2:
        altezza = st.number_input("Altezza (cm)", min_value=100.0, max_value=250.0, value=175.0, step=1.0, key=f"input_altezza_{prefix}")

    altezza_m = altezza / 100.0
    bmi_valore = round(peso / (altezza_m ** 2), 1) if altezza_m > 0 else 0.0
    st.caption(f"⚖️ **BMI Calcolato:** `{bmi_valore}`")

    ecog = st.selectbox(
        "ECOG Performance Status:",
        [
            "0 - Pienamente attivo e autonomo",
            "1 - Sintomatico ma ambulante",
            "2 - Allettato <50% del giorno",
            "3 - Allettato >50% del giorno",
            "4 - Completamente allettato e dipendente"
        ],
        key=f"{prefix}_ecog"
    )

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        adl = st.selectbox(
            "Scala ADL:",
            ["Non valutato", "Indipendente (6/6)", "Parzialmente dipendente (3-5/6)", "Fortemente dipendente (0-2/6)"],
            key=f"{prefix}_adl"
        )
    with col_p2:
        iadl = st.selectbox(
            "Scala IADL:",
            ["Non valutato", "Indipendente (8/8)", "Parzialmente dipendente (4-7/8)", "Fortemente dipendente (0-3/8)"],
            key=f"{prefix}_iadl"
        )

    st.markdown("---")
    st.markdown("### 🧠 Valutazione Geriatrica & Comorbilità")
    with st.expander("Screening G8 e Charlson Index", expanded=False):
        g8_score = st.slider("Punteggio G8 (0-17)", 0, 17, 14, key=f"{prefix}_g8_slider")
        charlson_base = st.number_input("Charlson Comorbidity Index (base)", 0, 15, 2, key=f"{prefix}_charlson_base")

    bonus_eta_charlson = 4 if eta >= 80 else (3 if eta >= 70 else (2 if eta >= 60 else (1 if eta >= 50 else 0)))
    charlson_totale = charlson_base + bonus_eta_charlson
    aspettativa_ok, charlson_ponderato = stima_aspettativa_di_vita(eta, charlson_totale, g8_score, ecog)

    st.info(f"📈 **CCI Corretto:** `{charlson_totale}` | **G8:** `{g8_score}/17`")

    # --- SEZIONE 1: ESAMI DI LABORATORIO (SANGUE E URINE) ---
    st.markdown("---")
    st.markdown("### 🧪 Esami di Laboratorio già eseguiti (Sangue e Urine in Ingresso)")
    st.write("Verifica o inserisci i valori ematochimici e specialistici portati dal paziente:")

    col_lab1, col_lab2 = st.columns(2)
    with col_lab1:
        gia_emocromo = st.checkbox("Emocromo completo", value=True, key=f"{prefix}_gia_emocromo")
        emoglobina = st.number_input("Emoglobina (g/dL)", min_value=3.0, max_value=20.0, value=13.5, step=0.1, key=f"{prefix}_hb") if gia_emocromo else 13.5
        wbc = st.number_input("WBC (10^3/uL)", min_value=0.5, max_value=100.0, value=7.0, step=0.1, key=f"{prefix}_wbc") if gia_emocromo else 7.0
        plt = st.number_input("Piastrine (10^3/uL)", min_value=10, max_value=1000, value=200, step=1, key=f"{prefix}_plt") if gia_emocromo else 200

        creatinina = st.number_input("Creatinina (mg/dL)", min_value=0.2, max_value=15.0, value=0.9, step=0.1, key=f"{prefix}_creatinina")
        egfr = st.number_input("eGFR (mL/min)", min_value=5, max_value=150, value=90, step=1, key=f"{prefix}_egfr")

    with col_lab2:
        calcemia = st.number_input("Calcemia totale (mg/dL)", min_value=5.0, max_value=16.0, value=9.5, step=0.1, key=f"{prefix}_calcemia")
        ldh = st.number_input("LDH (U/L)", min_value=50.0, max_value=1000.0, value=200.0, step=5.0, key=f"{prefix}_ldh")
        beta2_microglobulina = st.number_input("Beta-2 Microglobulina (mg/L)", min_value=0.5, max_value=20.0, value=2.0, step=0.1, key=f"{prefix}_beta2")
        albuminemia = st.number_input("Albuminemia (g/dL)", min_value=1.0, max_value=6.0, value=4.0, step=0.1, key=f"{prefix}_albumina")

    st.markdown("#### 🔬 Profilo Monoclonale di Laboratorio (Siero / Urine)")
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        flag_spep_eseguita = st.checkbox("Elettroforesi sieroproteica (SPEP) eseguita", value=True, key=f"{prefix}_spep_eseg")
        valore_picco = st.text_input("Riscontro Picco Monoclonale (es. IgG Kappa, 1.2 g/dL)", key=f"{prefix}_val_picco") if flag_spep_eseguita else ""

        flag_ife_siero_eseguita = st.checkbox("Immunofissazione sierica eseguita", value=True, key=f"{prefix}_ife_siero_eseg")
    with col_m2:
        flag_flc_eseguita = st.checkbox("Catene Leggere Libere (FLC) dosate", value=True, key=f"{prefix}_flc_eseg")
        valore_flc = st.text_input("Valori FLC / Rapporto K/L alterato", key=f"{prefix}_val_flc") if flag_flc_eseguita else ""

        flag_bence_eseguita = st.checkbox("Proteinuria di Bence-Jones / Urine 24h eseguita", value=False, key=f"{prefix}_bence_eseg")

    # --- SEZIONE 2: ESAMI DIAGNOSTICI / RADIOLOGICI ---
    st.markdown("---")
    st.markdown("### 🩻 Esami Diagnostici & Radiologici già eseguiti (Imaging / Altro)")
    st.write("Registra la presenza di referti radiologici o strumentali portati in visione:")

    col_img1, col_img2 = st.columns(2)
    with col_img1:
        flag_rx_scheletro = st.checkbox("RX Scheletro in toto / Studio radiologico standard", value=False, key=f"{prefix}_rx_skel")
        flag_tc_low_dose = st.checkbox("TC a basso dosaggio total-body (WBLDCT)", value=False, key=f"{prefix}_tc_ld")
    with col_img2:
        flag_rm_colonna = st.checkbox("Risonanza Magnetica (RM) rachide / bacino o focalizzata", value=False, key=f"{prefix}_rm_col")
        flag_ecocardio = st.checkbox("Ecocardiogramma / ECG (es. per sospetto amiloidosi)", value=False, key=f"{prefix}_ecocardio")

    st.markdown("---")
    st.markdown("### 🎯 Indicatori Clinici di Sospetto / Criteri CRAB")
    col_cr1, col_cr2 = st.columns(2)
    with col_cr1:
        ipercalcemia = st.checkbox("Ipercalcemia (> 11 mg/dL)", value=(calcemia > 11.0), key=f"{prefix}_ipercalcemia")
        insuff_renale = st.checkbox("Insufficienza renale (Creatinina > 2 o eGFR < 40)", value=(creatinina > 2.0 or egfr < 40), key=f"{prefix}_insuff_renale")
    with col_cr2:
        anemia_clinica = st.checkbox("Anemia marcata (Hb < 10 g/dL)", value=(emoglobina < 10.0), key=f"{prefix}_anemia_clinica")
        lesioni_ossee = st.checkbox("Lesioni ossee / Osteolisi refertate nei diagnostici", key=f"{prefix}_lesioni_ossee")

    # --- SEZIONE 3: GENERAZIONE DINAMICA DEGLI ESAMI DA RICHIEDERE ALLA FINE ---
    st.markdown("---")
    st.markdown("### ⚖️ Esami di Approfondimento e Completamento Consigliati (In base alla valutazione)")

    merita_biopsia = False
    motivo_biopsia = []
    if ipercalcemia or insuff_renale or anemia_clinica or lesioni_ossee or (flag_spep_eseguita and valore_picco != ""):
        merita_biopsia = True
        if ipercalcemia: motivo_biopsia.append("Ipercalcemia (C)")
        if insuff_renale: motivo_biopsia.append("Danno renale (R)")
        if anemia_clinica: motivo_biopsia.append("Anemia (A)")
        if lesioni_ossee: motivo_biopsia.append("Lesioni ossee (B)")
        if flag_spep_eseguita and valore_picco != "": motivo_biopsia.append("Componente monoclonale attiva")

    esami_finali_consigliati = []
    
    # Completamento laboratori mancanti
    if not flag_spep_eseguita:
        esami_finali_consigliati.append("Completare Laboratorio: Elettroforesi sieroproteica (SPEP)")
    if not flag_ife_siero_eseguita:
        esami_finali_consigliati.append("Completare Laboratorio: Immunofissazione sierica")
    if not flag_flc_eseguita:
        esami_finali_consigliati.append("Completare Laboratorio: Dosaggio Catene Leggere Libere (FLC)")
    if not flag_bence_eseguita:
        esami_finali_consigliati.append("Completare Laboratorio: Proteinuria di Bence-Jones / 24 ore")

    # Completamento diagnostica / radiologia mancante
    if not flag_tc_low_dose and not flag_rx_scheletro and not flag_rm_colonna:
        esami_finali_consigliati.append("Completare Diagnostica: TC total-body a basso dosaggio (WBLDCT)")

    # Istologia midollare
    if merita_biopsia:
        st.success("✅ **Indicazione Ematologica:** Criteri di danno d'organo / IMWG soddisfatti. **Indicato completamento con Biopsia Osteomidollare (BOM).**")
        esami_finali_consigliati.append("Esecuzione Biopsia Osteomidollare (BOM) con aspirato per studio citofluorimetrico e FISH")
    else:
        st.warning("⚠️ **Indicazione Ematologica:** Quadro meritevole di inquadramento per potenziale MGUS / Mieloma Smoldering.")
        esami_finali_consigliati.append("Controllo clinico-laboratoristico a 3-6 mesi")

    st.markdown("**📋 Lista finale degli esami prescritti / da allegare al piano di cura:**")
    for esame in esami_finali_consigliati:
        st.markdown(f"- 🔹 {esame}")

    # --- ACCORDO / DISACCORDO MEDICO ---
    st.markdown("---")
    st.markdown("### 👨‍⚕️ Validazione del Medico Ematologo")
    parere_medico = st.radio(
        "Concordi con il percorso diagnostico impostato?",
        ["Concordo", "Disaccordo"],
        key=f"{prefix}_parere_medico"
    )

    opzione_terapeutica_scelta = "Nessuna (Iter diagnostico / stadiazione in corso)"
    motivazione_disaccordo = ""

    if parere_medico == "Disaccordo":
        opzioni_terapeutiche_mm = [
            "Sorveglianza attiva / Watch and Wait",
            "Terapia d'induzione con quadruplice farmaco (es. Dara-VRd)",
            "Terapia d'induzione con Bortezomib + Lenalidomide + Desametasone (VRd)",
            "Terapia per pazienti non elegibili a trapianto (es. Dara-Rd)",
            "Terapia di supporto esclusiva"
        ]
        opzione_terapeutica_scelta = st.selectbox("Seleziona opzione terapeutica alternativa:", opzioni_terapeutiche_mm, key=f"{prefix}_menu_terapie")
        motivazione_disaccordo = st.text_area("Motivazione clinica del disaccordo:", key=f"{prefix}_motivazione_testo")

    return {
        "nome": nome.strip(),
        "cognome": cognome.strip(),
        "id_univoco": st.session_state[id_key].strip(),
        "data_nascita": str(data_nascita),
        "eta": eta,
        "peso": peso,
        "altezza": altezza,
        "bmi": bmi_valore,
        "ecog": ecog,
        "adl": adl,
        "iadl": iadl,
        "g8_score": g8_score,
        "charlson_score": charlson_totale,
        "charlson_ponderato": charlson_ponderato,
        "emoglobina": emoglobina,
        "wbc": wbc,
        "plt": plt,
        "creatinina": creatinina,
        "egfr": egfr,
        "calcemia": calcemia,
        "ldh": ldh,
        "beta2": beta2_microglobulina,
        "albumina": albuminemia,
        "flag_spep_eseguita": flag_spep_eseguita,
        "valore_picco": valore_picco.strip(),
        "flag_flc_eseguita": flag_flc_eseguita,
        "valore_flc": valore_flc.strip(),
        "flag_tc_low_dose": flag_tc_low_dose,
        "flag_rx_scheletro": flag_rx_scheletro,
        "merita_biopsia": merita_biopsia,
        "motivo_biopsia": motivo_biopsia,
        "esami_finali_consigliati": esami_finali_consigliati,
        "parere_medico": parere_medico,
        "opzione_terapeutica_scelta": opzione_terapeutica_scelta,
        "motivazione_disaccordo": motivazione_disaccordo.strip(),
        "caregiver": caregiver_supporto
    }

def render_anamnesi_e_valutazione(sigla_organo="MM", prefix="mm"):
    return render_anagrafica_e_anamnesi_unificata(sigla_organo=sigla_organo, prefix=prefix)
