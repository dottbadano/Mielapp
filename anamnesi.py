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

def estrai_valore_regex(pattern, testo):
    match = re.search(pattern, testo, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None

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
        st.warning("Data di nascita non valida. Impostata temporaneamente a 01/01/1960.")

    oggi = datetime.today().date()
    eta = oggi.year - data_nascita.year - ((oggi.month, oggi.day) < (data_nascita.month, data_nascita.day))

    st.info(f"📊 **Età Anagrafica:** {eta} anni")

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

    st.markdown("#### Allergie & Tabagismo")
    ha_allergie = st.checkbox("Il paziente presenta allergie note", key=f"{prefix}_ha_allergie")
    specifica_allergie = st.text_input("Specificare allergie", key=f"{prefix}_specifica_allergie") if ha_allergie else ""

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        tabagismo = st.selectbox("Tabagismo:", ["Non fumatore", "Ex fumatore", "Fumatore attivo"], key=f"{prefix}_tabagismo")
    with col_t2:
        sig_die = st.number_input("Sigarette / die", min_value=1, max_value=100, value=10, step=1, key=f"{prefix}_sig_die") if tabagismo == "Fumatore attivo" else 0

    st.markdown("---")
    st.markdown("### 🩺 Esame Obiettivo")
    eo_generale_normale = st.checkbox("Condizioni generali e cute nella norma", value=True, key=f"{prefix}_eo_gen_norm")
    eo_generale_note = st.text_input("Dettagli alterazioni generali", key=f"{prefix}_eo_gen_note") if not eo_generale_normale else ""

    eo_cardio_normale = st.checkbox("Apparato cardiocircolatorio nella norma", value=True, key=f"{prefix}_eo_cardio_norm")
    eo_cardio_note = st.text_input("Dettagli alterazioni cardiocircolatorie", key=f"{prefix}_eo_cardio_note") if not eo_cardio_normale else ""

    eo_resp_normale = st.checkbox("Apparato respiratorio nella norma", value=True, key=f"{prefix}_eo_resp_norm")
    eo_resp_note = st.text_input("Dettagli alterazioni respiratorie", key=f"{prefix}_eo_resp_note") if not eo_resp_normale else ""

    eo_addome_normale = st.checkbox("Addome nella norma", value=True, key=f"{prefix}_eo_add_norm")
    eo_addome_note = st.text_input("Dettagli alterazioni addominali", key=f"{prefix}_eo_add_note") if not eo_addome_normale else ""

    eo_scheletro_normale = st.checkbox("Sistema scheletrico nella norma", value=True, key=f"{prefix}_eo_skel_norm")
    eo_scheletro_note = st.text_input("Dettagli reperti scheletrici", key=f"{prefix}_eo_skel_note") if not eo_scheletro_normale else ""

    eo_neuro_normale = st.checkbox("Esame neurologico nella norma", value=True, key=f"{prefix}_eo_neur_norm")
    eo_neuro_note = st.text_input("Dettagli alterazioni neurologiche", key=f"{prefix}_eo_neur_note") if not eo_neuro_normale else ""

    st.markdown("---")
    st.markdown("### 🧠 Valutazione Geriatrica & Comorbilità")
    g8_score = 14  # Valore di default sicuro
    charlson_totale = 2
    aspettativa_ok, charlson_ponderato = stima_aspettativa_di_vita(eta, charlson_totale, g8_score, ecog)

    st.markdown("---")
    st.markdown("### 💧 Esami Ematochimici")
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        creatinina = st.number_input("Creatinina (mg/dL)", min_value=0.2, max_value=15.0, value=0.9, step=0.1, key=f"{prefix}_creatinina")
    with col_r2:
        egfr = st.number_input("eGFR (mL/min)", min_value=5, max_value=150, value=90, step=1, key=f"{prefix}_egfr")

    col_e1, col_e2, col_e3 = st.columns(3)
    with col_e1:
        emoglobina = st.number_input("Emoglobina (g/dL)", min_value=3.0, max_value=20.0, value=14.0, step=0.1, key=f"{prefix}_hb")
    with col_e2:
        wbc = st.number_input("WBC (10^3/uL)", min_value=0.5, max_value=100.0, value=7.0, step=0.1, key=f"{prefix}_wbc")
    with col_e3:
        plt = st.number_input("Piastrine (10^3/uL)", min_value=10, max_value=1000, value=200, step=1, key=f"{prefix}_plt")

    ast, alt, ggt = 25.0, 25.0, 30.0

    st.markdown("---")
    st.markdown("### 🔬 Criteri IMWG / CRAB")
    col_cr1, col_cr2 = st.columns(2)
    with col_cr1:
        ipercalcemia = st.checkbox("Ipercalcemia (> 11 mg/dL)", key=f"{prefix}_ipercalcemia")
        insuff_renale = st.checkbox("Insufficienza renale", key=f"{prefix}_insuff_renale")
    with col_cr2:
        anemia_clinica = st.checkbox("Anemia marcata", key=f"{prefix}_anemia_clinica")
        lesioni_ossee = st.checkbox("Lesioni litiche / Dolore osseo", key=f"{prefix}_lesioni_ossee")

    merita_biopsia = bool(ipercalcemia or insuff_renale or anemia_clinica or lesioni_ossee)
    motivo_biopsia = ["Criteri CRAB soddisfatti"] if merita_biopsia else []
    ulteriori_accertamenti_scelta = "Nessuno" if merita_biopsia else "Follow-up clinico"

    parere_medico = "Concordo"
    opzione_terapeutica_scelta = "Nessuna"
    motivazione_disaccordo = ""
    caregiver_supporto = "Autonomo"
    familiarita_attiva = []
    interventi = ""
    farmacologica = ""

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
        "gds": "Non valutato",
        "mmse_eseguito": False,
        "mmse_valore": "",
        "charlson_score": charlson_totale,
        "charlson_ponderato": charlson_ponderato,
        "aspettativa_vita_maggiore_10_anni": aspettativa_ok,
        "ha_allergie": ha_allergie,
        "specifica_allergie": specifica_allergie.strip(),
        "tabagismo": tabagismo,
        "sig_die": sig_die,
        "eo_generale_normale": eo_generale_normale,
        "eo_generale_note": eo_generale_note.strip(),
        "eo_cardio_normale": eo_cardio_normale,
        "eo_cardio_note": eo_cardio_note.strip(),
        "eo_resp_normale": eo_resp_normale,
        "eo_resp_note": eo_resp_note.strip(),
        "eo_addome_normale": eo_addome_normale,
        "eo_addome_note": eo_addome_note.strip(),
        "eo_scheletro_normale": eo_scheletro_normale,
        "eo_scheletro_note": eo_scheletro_note.strip(),
        "eo_neuro_normale": eo_neuro_normale,
        "eo_neuro_note": eo_neuro_note.strip(),
        "creatinina": creatinina,
        "egfr": egfr,
        "emoglobina": emoglobina,
        "wbc": wbc,
        "plt": plt,
        "ast": ast,
        "alt": alt,
        "ggt": ggt,
        "merita_biopsia": merita_biopsia,
        "motivo_biopsia": motivo_biopsia,
        "ulteriori_accertamenti_scelta": ulteriori_accertamenti_scelta,
        "parere_medico": parere_medico,
        "opzione_terapeutica_scelta": opzione_terapeutica_scelta,
        "motivazione_disaccordo": motivazione_disaccordo.strip(),
        "caregiver": caregiver_supporto,
        "familiarita": familiarita_attiva,
        "interventi": interventi.strip(),
        "farmacologica": farmacologica.strip()
    }

def formatta_anamnesi_per_pdf_unificata(paziente_info):
    testo_biopsia = (
        "Il quadro clinico soddisfa i criteri IMWG per sospetto di neoplasia plasmacellulare."
        if paziente_info.get('merita_biopsia') else
        "Il quadro non richiede biopsia immediata."
    )
    righe = [
        "================================================================================",
        "REFERTO CLINICO SPECIALISTICO ONCO-HEMATOLOGICAL EVALUATION",
        "================================================================================",
        f"Codice Univoco Paziente (ID): {paziente_info.get('id_univoco', 'N/D')}",
        f"Generalità: {paziente_info.get('cognome', '')} {paziente_info.get('nome', '')}",
        f"Valutazione IMWG: {testo_biopsia}",
        f"Note di supporto: {paziente_info.get('caregiver', 'Non valutato')}."
    ]
    return "\n".join(righe)
